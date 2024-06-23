import json
import re
from typing import List, Dict, AnyStr, Union, Optional
from groq import Groq
import os

class BankOperator:
    def __init__(
            self, 
            system_msg: AnyStr,
            tools: List, 
            client: Groq,
            names_to_functions: Optional[Union[Dict, None]] = None,
            model: str = "llama3-70b-8192", 
            max_tokens: int = 100,
            temperature: float = 0.7
        ):
        self.system_msg = system_msg
        self.messages = []
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.tools = tools
        self.names_to_functions = names_to_functions
        self.messages.append({"role": "system", "content": self.system_msg})
    
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
            chat_history = [{"role": "system", "content": self.system_msg}]
            for item in chat_history_passed:
                if item['sender'] == 'Human':
                    chat_history.append({"role": "user", "content": item['message']['text']})
                elif item['sender'] == 'AI':
                    chat_history.append({"role": "assistant", "content": item['message']})

            return chat_history

    def run_conversation(self, user_prompt, query):
        self.messages.append({'role': 'user', 'content': user_prompt.format(query=query)})

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

        # Step 2: Check if the model wants to use a tool
        if tool_calls:
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                function_to_call = self.names_to_functions.get(function_name)
                if function_to_call:
                    try:
                        function_response = function_to_call(**function_args) if function_args else function_to_call()
                    except TypeError as ex:
                        print(f"Error calling function {function_name}: {ex}")
                else:
                    print(f"Function {function_name} not found in names_to_functions")
                
                self.messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })
        
        # Step 3: Process both the function response if used or process the users input without function use.
        completion2 = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )
        conversation = completion2.choices[0].message.content
        self.messages.append({'role': 'assistant', 'content': conversation})

        return conversation