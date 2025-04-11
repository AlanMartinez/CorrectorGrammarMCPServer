from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config.settings import SECRET_KEY, ALGORITHM, VALIDATE_TOKEN_URL
from models.user import User
import httpx
import logging

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class TokenData:
    def __init__(self, email: str, user_id: str):
        self.email = email
        self.user_id = user_id

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        logger.info(f"Validating token with URL: {VALIDATE_TOKEN_URL}")
        logger.info(f"Token being validated: {token}")
        
        # Call external token validation service with GET
        async with httpx.AsyncClient() as client:
            response = await client.get(
                VALIDATE_TOKEN_URL,
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                logger.error(f"Token validation failed with status: {response.status_code}")
                raise credentials_exception
                
            token_data = response.json()
            return token_data
            
    except Exception as e:
        logger.error(f"Error during token validation: {str(e)}")
        raise credentials_exception