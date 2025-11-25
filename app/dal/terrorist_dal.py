from typing import Optional
from sqlmodel import Session, select, col
from app.models import Terrorist
from db.database import get_engine


def create_terrorist(name: str, affiliation: Optional[str] = None, location: Optional[str] = None) -> Terrorist:
    """CREATE - Add a new terrorist to the database"""
    engine = get_engine()
    with Session(engine) as session:
        terrorist = Terrorist(name=name, affiliation=affiliation, location=location)
        session.add(terrorist)
        session.commit()
        session.refresh(terrorist)
        print(f"✓ Added new terrorist: {terrorist.name}")
        return terrorist


def get_terrorist_by_id(terrorist_id: int) -> Optional[Terrorist]:
    """READ - Get a terrorist by ID"""
    engine = get_engine()
    with Session(engine) as session:
        return session.get(Terrorist, terrorist_id)


def get_terrorist_by_name(name: str) -> Optional[Terrorist]:
    """READ - Get a terrorist by exact name"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Terrorist).where(Terrorist.name == name)
        terrorist = session.exec(statement).first()
        return terrorist


def search_terrorists_by_name(name: str):
    """READ - Search terrorists by partial name match"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Terrorist).where(col(Terrorist.name).contains(name))
        terrorists = session.exec(statement).all()
        return terrorists


def get_all_terrorists():
    """READ - Get all terrorists"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Terrorist)
        terrorists = session.exec(statement).all()
        return terrorists
