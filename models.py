from sqlalchemy import create_engine, Column, Integer, String, Boolean
import sqlalchemy
from pydantic import BaseModel
from migrations import Base

# db model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    qrCode = Column(String, unique=True)
    isCollection = Column(Boolean, index=True)

# Create model
class ItemCreate(BaseModel):
    name: str
    description: str
    qrCode: str
    isCollection: bool
    
# Response model
class ItemResponse(BaseModel):
    id: int
    name: str
    description: str
    qrCode: str
    isCollection: bool