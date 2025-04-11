from fastapi import APIRouter
from models.roleplay_model import RoleplayInput
from services.roleplay_service import RoleplayService

router = APIRouter()
roleplay_service = RoleplayService()

@router.post("/chat")
def chat(input: RoleplayInput):
    """
    Process a chat message with context preservation.
    
    Args:
        input: RoleplayInput object containing the message text and optional client_id
        
    Returns:
        dict: Response with the assistant's reply and client_id for future reference
    """
    return roleplay_service.chat(
        text=input.text,
        client_id=input.client_id,
        role=input.role,
        topics=input.topics
    ) 