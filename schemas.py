from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: str = "pais"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
