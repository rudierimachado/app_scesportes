from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: Optional[str] = "pais"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class MatchBase(BaseModel):
    home_team: str
    away_team: str
    date: str
    status: str = "agendado"
    home_score: int = 0
    away_score: int = 0

class MatchCreate(MatchBase):
    pass

class Match(MatchBase):
    id: int
    user_id: Optional[int] = None

    class Config:
        from_attributes = True

class MatchEventBase(BaseModel):
    type: str
    team: str
    description: str
    timestamp: str

class MatchEventCreate(MatchEventBase):
    match_id: int

class MatchEvent(MatchEventBase):
    id: int
    match_id: int

    class Config:
        from_attributes = True
