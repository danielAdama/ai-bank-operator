from pydantic import BaseModel, Field, schema
from uuid import UUID, uuid4
from datetime import datetime
import datetime as dt
from typing import List, Optional, Union, Dict, Any

class ChatHistorySchema(BaseModel):
    user_id: str
    user_message: str
    ai_message: Union[None, str] = Field(default=None, hidden=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, hidden=True)

    class Config:
        from_attributes = True

        #To hide fields from API input
        @staticmethod
        def json_schema_extra(schema: dict, _):
            props = {}
            for k, v in schema.get('properties', {}).items():
                if not v.get("hidden", False):
                    props[k] = v
            schema["properties"] = props

class ChatHistorySchemaIn(ChatHistorySchema):
    id: UUID = Field(default_factory=uuid4, primary_key=True, hidden=True)

class ChatHistorySchemaOut(ChatHistorySchema):
    id: UUID