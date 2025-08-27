from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from db.db_connection import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class News(Base):
    __tablename__ = "news"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    link = Column(String(1000), nullable=True)
    pub_date = Column(String(255), nullable=True)  # Store as string to preserve original format
    category = Column(String(100), nullable=True)
    image = Column(String(1000), nullable=True)
    publisher = Column(String(200), nullable=True)
    tag = Column(String(100), nullable=False, index=True)  # e.g., "international_news"
    summary = Column(Text, nullable=True)
    is_summarized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# Pydantic models for API requests/responses
class NewsCreate(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    link: Optional[str] = None
    pub_date: Optional[str] = None  # Store as string
    category: Optional[str] = None
    image: Optional[str] = None
    publisher: Optional[str] = None
    tag: str
    summary: Optional[str] = None
    is_summarized: bool = False


class NewsResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    link: Optional[str] = None
    pub_date: Optional[str] = None  # Return as string
    category: Optional[str] = None
    image: Optional[str] = None
    publisher: Optional[str] = None
    tag: str
    summary: Optional[str] = None
    is_summarized: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }
