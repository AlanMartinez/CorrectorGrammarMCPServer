from fastapi import APIRouter, Depends
from models.input_model import TextInput
from services.openai_service import OpenAIService
from config.constants import RESPONSE_SUCCESS, RESPONSE_DATA
from utils.auth import get_current_user

router = APIRouter(prefix="/grammar")
openai_service = OpenAIService()

@router.post("/correct")
def correct_english(input: TextInput, token_data: dict = Depends(get_current_user)):
    """
    Correct English text and provide explanations.
    
    Args:
        input: TextInput object containing the text to correct
        
    Returns:
        dict: Standardized response with success status and data/error
    """
    return openai_service.correct_text(input.text) 