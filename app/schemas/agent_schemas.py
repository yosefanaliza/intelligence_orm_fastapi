"""
Agent Request/Response Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class AgentCreate(BaseModel):
    """Schema for creating a new agent"""
    name: str = Field(..., min_length=1, max_length=100, description="Full name of the agent")
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=4, max_length=100, description="Password")


class AgentLogin(BaseModel):
    """Schema for agent login"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class AgentResponse(BaseModel):
    """Schema for agent response"""
    id: int
    name: str
    username: str
    created_at: datetime
    
    class Config:
        from_attributes = True
