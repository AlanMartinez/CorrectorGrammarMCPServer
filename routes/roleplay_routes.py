from fastapi import APIRouter, Depends, HTTPException, status
from services.roleplay_service import RoleplayService
from utils.response_wrapper import ResponseWrapper
from utils.auth import get_current_user
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()
roleplay_service = RoleplayService()

class ChatRequest(BaseModel):
    text: str
    role: str = "user"
    topics: Optional[List[str]] = None

@router.post("/chat")
async def chat(
    request: ChatRequest,
    token_data: dict = Depends(get_current_user)
):
    try:
        response = roleplay_service.chat(
            text=request.text,
            client_id=token_data.get("user_id"),
            role=request.role,
            topics=request.topics
        )
        return ResponseWrapper.success(response)
    except Exception as e:
        return ResponseWrapper.error(str(e))

@router.post("/start")
async def start_roleplay(
    topic: str,
    token_data: dict = Depends(get_current_user)
):
    try:
        response = roleplay_service.start_roleplay(
            client_id=token_data.get("user_id"),  # Get client_id from token
            topic=topic
        )
        return ResponseWrapper.success(response)
    except Exception as e:
        return ResponseWrapper.error(str(e))

@router.post("/end")
async def end_roleplay(
    token_data: dict = Depends(get_current_user)
):
    try:
        response = roleplay_service.end_roleplay(
            client_id=token_data.get("user_id")  # Get client_id from token
        )
        return ResponseWrapper.success(response)
    except Exception as e:
        return ResponseWrapper.error(str(e)) 