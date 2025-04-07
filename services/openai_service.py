from openai import OpenAI, OpenAIError
import logging
from config.settings import OPENAI_API_KEY, OPENAI_MODEL

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def correct_text(self, text: str) -> dict:
        prompt = (
            "You are an English teacher. Fix the grammar and spelling of this text:\n\n"
            f"{text}\n\n"
            "Corrected version:"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You correct grammar and explain mistakes."},
                    {"role": "user", "content": prompt}
                ]
            )
            return {"corrected": response.choices[0].message.content.strip()}
        except OpenAIError as e:
            error_message = str(e)
            logger.error(f"OpenAI API error: {error_message}")
            
            if "insufficient_quota" in error_message:
                return {
                    "error": "API quota exceeded",
                    "message": "The OpenAI API quota has been exceeded. Please check your billing details or try again later.",
                    "details": "Visit https://platform.openai.com/account/billing to check your quota and billing status."
                }
            else:
                return {
                    "error": "OpenAI API error",
                    "message": "An error occurred while processing your request.",
                    "details": error_message
                }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                "error": "Server error",
                "message": "An unexpected error occurred while processing your request.",
                "details": str(e)
            } 