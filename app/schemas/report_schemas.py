"""
Report Request/Response Schemas
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ReportCreate(BaseModel):
    """Schema for creating a new report"""
    content: str = Field(..., min_length=1, description="Content of the intelligence report")
    agent_id: int = Field(..., description="ID of the agent creating the report")
    terrorist_id: int = Field(..., description="ID of the terrorist being reported on")


class ReportResponse(BaseModel):
    """Schema for report response"""
    id: int
    content: str
    agent_id: int
    terrorist_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ReportSearchResponse(BaseModel):
    """Schema for report search results with additional info"""
    id: int
    content: str
    agent_id: int
    terrorist_id: int
    created_at: datetime
    terrorist_name: Optional[str] = None
    agent_name: Optional[str] = None
    
    class Config:
        from_attributes = True


class DangerousTerroristResponse(BaseModel):
    """Schema for dangerous terrorist with report count"""
    terrorist_id: int
    terrorist_name: str
    affiliation: Optional[str]
    location: Optional[str]
    report_count: int
