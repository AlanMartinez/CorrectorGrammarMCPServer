from openai import OpenAIError
import openai
import logging
import uuid
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from config.constants import (
    ERROR_API_KEY_MISSING,
    ERROR_OPENAI_API,
    ERROR_SERVER
)
from utils.response_wrapper import ResponseWrapper
from services.prompts import DEFAULT_SYSTEM_MESSAGE, create_topic_system_message

logger = logging.getLogger(__name__)

class RoleplayService:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_API_KEY_MISSING)
        openai.api_key = OPENAI_API_KEY
        self.model = OPENAI_MODEL
        self.conversations = {}
    
    def _get_or_create_conversation(self, client_id: str) -> list:
        """Get existing conversation or create a new one for the client."""
        if client_id not in self.conversations:
            self.conversations[client_id] = []
        return self.conversations[client_id]
    
    def _update_conversation(self, client_id: str, role: str, content: str):
        """Add a message to the conversation history."""
        # Validate role is one of the allowed values
        valid_roles = ['system', 'assistant', 'user']
        if role not in valid_roles:
            logger.warning(f"Invalid role '{role}' provided, defaulting to 'user'")
            role = 'user'
            
        conversation = self._get_or_create_conversation(client_id)
        conversation.append({"role": role, "content": content})
        # Keep only the last 10 messages to prevent context from growing too large
        if len(conversation) > 10:
            conversation.pop(0)
    
    def _create_system_message(self, topics: list[str]) -> dict:
        """Create a system message incorporating the specified topics."""
        return {
            "role": "system",
            "content": create_topic_system_message(topics)
        }
    
    def chat(self, text: str, client_id: str = None, role: str = "user", topics: list[str] = None) -> dict:
        try:
            if not client_id:
                client_id = str(uuid.uuid4())
                logger.info(f"Created new conversation with ID: {client_id}")
            
            self._update_conversation(client_id, role, text)
            
            conversation = self._get_or_create_conversation(client_id)
            
            # Add system message if this is the first message or topics are provided
            if len(conversation) == 1 or topics:
                # If topics are provided, create a new system message with them
                if topics:
                    system_message = self._create_system_message(topics)
                    # Replace existing system message if it exists
                    if conversation and conversation[0]["role"] == "system":
                        conversation[0] = system_message
                    else:
                        conversation.insert(0, system_message)
                # If no topics provided but first message, use default system message
                elif len(conversation) == 1:
                    system_message = {
                        "role": "system",
                        "content": DEFAULT_SYSTEM_MESSAGE
                    }
                    conversation.insert(0, system_message)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=conversation,
                temperature=0.7,  # Add some creativity while maintaining coherence
                presence_penalty=0.6,  # Encourage the model to talk about new topics
                frequency_penalty=0.3  # Reduce repetition
            )
            
            assistant_response = response.choices[0].message.content.strip()
            
            self._update_conversation(client_id, "assistant", assistant_response)
            
            return ResponseWrapper.success({
                "response": assistant_response,
                "client_id": client_id
            })
            
        except OpenAIError as e:
            error_message = str(e)
            logger.error(f"OpenAI API error: {error_message}")
            
            return ResponseWrapper.error(
                error_type="OpenAI API error",
                message=ERROR_OPENAI_API,
                details=error_message
            )
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return ResponseWrapper.error(
                error_type="Server error",
                message=ERROR_SERVER,
                details=str(e)
            ) 