import json
import re
import redis
from typing import List, Dict, AnyStr, Union, Optional
from groq import Groq
from openai import OpenAI
from config import OPENAI_MODEL
import os
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class BankOperator:
    def __init__(
            self, 
            system_prompt: AnyStr,
            tools: List,
            client: Union[Groq, OpenAI],
            redis_client: redis.Redis,
            names_to_functions: Optional[Union[Dict, None]] = None,
            model: str = "llama3-70b-8192", 
            max_tokens: int = 150,
            temperature: float = 0.7,
            user_id: str = "test-user"
        ):
        self.system_prompt = system_prompt
        self.messages = []
        self.client = client
        self.redis_client = redis_client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tools = tools
        self.names_to_functions = names_to_functions
        self.user_id = user_id
        self.messages = self.load_messages()

    def load_messages(self):
        # Load messages from Redis
        messages = self.redis_client.get(f"{self.user_id}_messages")
        if messages:
            return json.loads(messages)
        return [{"role": "system", "content": self.system_prompt}]
    
    def save_messages(self):
        # Save messages to Redis
        self.redis_client.set(f"{self.user_id}_messages", json.dumps(self.messages))
    
    def intelligent_chat_history_conversion(self, chat_history_passed=None):
        pattern = "Query: (.*)\n\n\n"

        if chat_history_passed is None:
            history = []
            for m in self.messages:
                if m["role"] in ["user", "assistant"]:
                    history.append(m)

            formatted_chat_history = []
            for message in history:
                if message["role"] == "user":
                    match = re.search(pattern, message["content"], re.DOTALL)
                    if match:
                        formatted_chat_history.append({
                            'sender': 'Human',
                            'message': {"text": match.group(1)}
                        })
                elif message["role"] == "assistant":
                    if message["content"]:
                        formatted_chat_history.append({
                            'sender': 'AI',
                            'message': {"text": message["content"]}
                        })
            return formatted_chat_history
        
        elif chat_history_passed is not None and isinstance(chat_history_passed, List):
            chat_history = [{"role": "system", "content": self.system_prompt}]
            for item in chat_history_passed:
                if item['sender'] == 'Human':
                    chat_history.append({"role": "user", "content": item['message']['text']})
                elif item['sender'] == 'AI':
                    chat_history.append({"role": "assistant", "content": item['message']})

            return chat_history

    def run_conversation(self, user_prompt, query):
        self.messages.append({'role': 'user', 'content': user_prompt.format(query=query)})
        self.save_messages()  # Cache message

        if isinstance(self.client, OpenAI):
            self.model = OPENAI_MODEL

        # Step1: Check if the users question requires calling a function
        completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            tools=self.tools,
            tool_choice="auto",
            temperature=0
        )
        
        response_message = completion.choices[0].message
        tool_calls = response_message.tool_calls

        logger.info(response_message)

        # Step 2: Check if the model wants to use a tool
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                if not self.names_to_functions:
                   raise ValueError(f"names_to_functions is not provided {self.names_to_functions}")
                
                function_to_call = self.names_to_functions.get(function_name)
                if function_to_call:
                    try:
                        function_response = function_to_call(**function_args) if function_args else function_to_call()
                    except TypeError as ex:
                        logger.error(f"Calling function {function_name}: {ex}")
                    else:
                        if isinstance(self.client, OpenAI):
                            self.messages.append({
                                "role": "assistant",
                                "content": function_response,
                            })
                        else:
                            logger.info(f"Switching to Groq as client for function calling. Make sure you are using Groq as client")
                
                if isinstance(self.client, Groq):
                    self.messages.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": function_response
                            }
                        )
        
        # Step 3: Process both the function response if used or process the users input without function use.
        completion2 = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        conversation = completion2.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': conversation})
        self.save_messages() 

        return conversation