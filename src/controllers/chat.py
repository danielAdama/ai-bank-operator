import pathlib
import sys

current_dir = pathlib.Path(__file__).parent
previous_dir = current_dir.parent.parent
sys.path.append(str(previous_dir))

from typing import Union, Dict
from uuid import UUID
from gen_ai.BankLLM import BankOperator
from gen_ai.utils.tools import tools
from gen_ai.utils import names_to_functions

from fastapi import APIRouter, status, HTTPException
from schemas.chat import (
    ChatHistorySchemaIn, 
    ChatHistorySchemaOut
)
from services import load_file
from services.response_check import (
    handle_error_render_json_response, 
    handle_success_render_json_response
)
from config import PROMPT_DIR, OPENAI_MODEL, client, redis_client

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

system_template = load_file(PROMPT_DIR / "system_template.txt")
user_template = load_file(PROMPT_DIR / "user_template.txt")
chat_controller = APIRouter()

@chat_controller.post(
        '/messages/',
        response_model=Dict[str, Union[str, ChatHistorySchemaOut]]
    )
async def send_message(
    data: ChatHistorySchemaIn,
    ):
    """
    chat with the Large Language Model.

    Parameters:
        data (ChatHistorySchemaIn): Message data.

    Returns:
        dict: A dictionary containing a success message if the message is successful or not.
    
    :return: Response indicating the status and the stored message data.
    """
    try:
        chatbot = BankOperator(
            system_prompt=system_template,
            tools=tools,
            client=client,
            redis_client=redis_client,
            names_to_functions=names_to_functions,
            user_id=data.user_id
        )
        
        reply = chatbot.run_conversation(
            user_template,
            data.user_message
        )
        data.ai_message = reply

        logger.info(chatbot.intelligent_chat_history_conversion())
        
        return handle_success_render_json_response(
            msg="Message processed successfully", 
            data=data,
            status_code=status.HTTP_200_OK
        )
    except Exception as ex:
        logger.error(f"processing your message: {ex}")
        return handle_error_render_json_response(
            ex, 
            data={"message": "Error processing your message"}, 
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )