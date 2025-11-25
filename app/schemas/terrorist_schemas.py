"""
Terrorist Request/Response Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TerroristCreate(BaseModel):
    """Schema for creating a new terrorist"""
    name: str = Field(..., min_length=1, max_length=100, description="Full name")
    affiliation: Optional[str] = Field(None, max_length=100, description="Organization affiliation")
    location: Optional[str] = Field(None, max_length=100, description="Area of activity")


class TerroristResponse(BaseModel):
    """Schema for terrorist response"""
    id: int
    name: str
    affiliation: Optional[str]
    location: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
