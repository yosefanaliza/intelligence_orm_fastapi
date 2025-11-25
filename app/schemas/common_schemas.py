"""
Common Request/Response Schemas
"""
from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None


class SuccessResponse(BaseModel):
    """Schema for success responses"""
    message: str
    data: Optional[Any] = None
