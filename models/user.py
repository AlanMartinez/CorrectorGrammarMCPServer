from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    user_id: str
    email: str
    sub: Optional[str] = None  # JWT subject (usually email)
    
    class Config:
        from_attributes = True 