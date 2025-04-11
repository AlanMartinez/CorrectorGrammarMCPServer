from pydantic import BaseModel
from typing import Optional

class RoleplayInput(BaseModel):
    text: str
    client_id: Optional[str] = None
    role: Optional[str] = "user"
    topics: Optional[list[str]] = None