from typing import Any, Dict, Optional
from config.constants import (
    RESPONSE_SUCCESS,
    RESPONSE_DATA,
    RESPONSE_ERROR,
    RESPONSE_MESSAGE,
    RESPONSE_DETAILS
)

class ResponseWrapper:
    @staticmethod
    def success(data: Any) -> Dict:
        """
        Create a success response.
        
        Args:
            data: The data to include in the response
            
        Returns:
            Dict: A standardized success response
        """
        return {
            RESPONSE_SUCCESS: True,
            RESPONSE_DATA: data
        }
    
    @staticmethod
    def error(error_type: str, message: str, details: Optional[str] = None) -> Dict:
        """
        Create an error response.
        
        Args:
            error_type: The type of error
            message: A user-friendly error message
            details: Optional detailed error information
            
        Returns:
            Dict: A standardized error response
        """
        response = {
            RESPONSE_SUCCESS: False,
            RESPONSE_ERROR: error_type,
            RESPONSE_MESSAGE: message
        }
        
        if details:
            response[RESPONSE_DETAILS] = details
            
        return response 