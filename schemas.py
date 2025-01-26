from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class AbbreviationEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AbbreviationCreate(BaseModel):
    abbreviation: str
    meaning: str
    

class AbbreviationUpdate(BaseModel):
    abbreviation: Optional[str] = None
    meaning: Optional[str] = None
    status: Optional[AbbreviationEnum] = None


class AbbreviationResponse(AbbreviationCreate):
    id: int
    status: AbbreviationEnum


    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    exp: datetime