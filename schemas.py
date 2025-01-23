from pydantic import BaseModel
from datetime import datetime
from enum import Enum


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
    status: AbbreviationEnum.PENDING


class AbbreviationResponse(AbbreviationCreate):
    status: AbbreviationEnum

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    exp: datetime