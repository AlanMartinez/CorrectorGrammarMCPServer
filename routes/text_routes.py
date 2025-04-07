from fastapi import APIRouter
from models.input_model import TextInput
from services.openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()

@router.post("/correct")
def correct_english(input: TextInput):
    return openai_service.correct_text(input.text) 