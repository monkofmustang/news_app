from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from db.db_connection import Base
from pydantic import BaseModel
from typing import Optional


class Subscribers(Base):
    __tablename__ = "subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    mobNumber = Column(Integer, unique=True, nullable=False, index=True)
    state = Column(String(255), nullable=True)


# Pydantic models for API requests/responses
class SubscriberCreate(BaseModel):
    name: Optional[str] = None
    mobNumber: int
    state: Optional[str] = None


class SubscriberResponse(BaseModel):
    id: int
    name: Optional[str] = None
    mobNumber: int
    state: Optional[str] = None
    
    class Config:
        from_attributes = True

