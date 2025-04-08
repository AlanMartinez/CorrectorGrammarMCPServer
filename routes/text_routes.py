from fastapi import APIRouter
from models.input_model import TextInput
from services.openai_service import OpenAIService
from config.constants import RESPONSE_SUCCESS, RESPONSE_DATA

router = APIRouter(prefix="/grammar")
openai_service = OpenAIService()

@router.post("/correct")
def correct_english(input: TextInput):
    """
    Correct English text and provide explanations.
    
    Args:
        input: TextInput object containing the text to correct
        
    Returns:
        dict: Standardized response with success status and data/error
    """
    return openai_service.correct_text(input.text) 