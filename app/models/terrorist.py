from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .report import Report


class Terrorist(SQLModel, table=True):
    """Terrorist model - Person being tracked in intelligence reports"""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)
    affiliation: Optional[str] = Field(default=None, max_length=100)
    location: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationship: One terrorist can have many reports about them
    reports: List["Report"] = Relationship(back_populates="terrorist")
