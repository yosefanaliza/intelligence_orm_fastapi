from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .agent import Agent
    from .terrorist import Terrorist


class Report(SQLModel, table=True):
    """Report model - Intelligence report about a terrorist written by an agent"""
    # __tablename__ = "reports"

    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Foreign Keys
    agent_id: int = Field(foreign_key="agent.id")
    terrorist_id: int = Field(foreign_key="terrorist.id")

    # Relationships
    agent: "Agent" = Relationship(back_populates="reports")
    terrorist: "Terrorist" = Relationship(back_populates="reports")
