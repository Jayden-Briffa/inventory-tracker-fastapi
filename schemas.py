from pydantic import BaseModel

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