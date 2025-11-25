from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .report import Report


class Agent(SQLModel, table=True):
    """Agent model - Intelligence agent who writes reports"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    username: str = Field(unique=True, index=True, max_length=50)
    password: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship: One agent can write many reports
    reports: List["Report"] = Relationship(back_populates="agent")
