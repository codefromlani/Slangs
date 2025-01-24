from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from passlib.context import CryptContext
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    date_joined = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=True)

    def __repr__(self):
        return f"<User(username={self.username})>"
    
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
    

class AbbreviationEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Abbreviation(Base):
    __tablename__ = "abbreviations"
    id = Column(Integer, primary_key=True, index=True)
    abbreviation = Column(String, unique=True, index=True)
    meaning = Column(Text)
    status = Column(SQLAlchemyEnum(AbbreviationEnum), index=True, default=AbbreviationEnum.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime)

    def __repr__(self):
        return f"<Abbreviation(abbreviation={self.abbreviation}, meaning={self.meaning}, approved={self.status})>"