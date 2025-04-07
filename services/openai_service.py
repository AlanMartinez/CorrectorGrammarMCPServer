from openai import OpenAI, OpenAIError
import logging
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from services.prompts import TextCorrectionPrompts
from config.constants import (
    SECTION_CORRECTED,
    SECTION_EXPLANATION,
    ERROR_API_KEY_MISSING,
    ERROR_OPENAI_API,
    ERROR_SERVER,
    ERROR_PARSING
)
from utils.response_wrapper import ResponseWrapper

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError(ERROR_API_KEY_MISSING)
            
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_MODEL

    def _parse_response(self, response_text: str) -> dict:
        """Parse the response text into corrected text and explanation."""
        try:
            # Split the response into sections by looking for the section headers
            corrected = ""
            explanation = ""
            
            # Find the corrected section
            if SECTION_CORRECTED in response_text:
                corrected_start = response_text.find(SECTION_CORRECTED) + len(SECTION_CORRECTED)
                if SECTION_EXPLANATION in response_text:
                    corrected_end = response_text.find(SECTION_EXPLANATION)
                    corrected = response_text[corrected_start:corrected_end].strip()
                else:
                    corrected = response_text[corrected_start:].strip()
            
            # Find the explanation section
            if SECTION_EXPLANATION in response_text:
                explanation_start = response_text.find(SECTION_EXPLANATION) + len(SECTION_EXPLANATION)
                explanation = response_text[explanation_start:].strip()
            
            return {
                "corrected": corrected,
                "explanation": explanation
            }
            
        except Exception as e:
            logger.error(f"Error parsing response: {str(e)}")
            return {
                "corrected": response_text,
                "explanation": ERROR_PARSING
            }

    def correct_text(self, text: str) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": TextCorrectionPrompts.get_system_prompt()},
                    {"role": "user", "content": TextCorrectionPrompts.get_correction_prompt(text)}
                ]
            )
            
            response_text = response.choices[0].message.content.strip()
            parsed_response = self._parse_response(response_text)
            return ResponseWrapper.success(parsed_response)
            
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