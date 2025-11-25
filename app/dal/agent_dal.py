from typing import Optional
from sqlmodel import Session, select, col
from app.models import Agent
from db.database import get_engine


def create_agent(name: str, username: str, password: str) -> Agent:
    """CREATE - Add a new agent to the database"""
    engine = get_engine()
    with Session(engine) as session:
        agent = Agent(name=name, username=username, password=password)
        session.add(agent)
        session.commit()
        session.refresh(agent)
        print(f"✓ Created new agent: {agent.name} (username: {agent.username})")
        return agent


def get_agent_by_username(username: str) -> Optional[Agent]:
    """READ - Get an agent by username"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Agent).where(Agent.username == username)
        agent = session.exec(statement).first()
        return agent


def get_agent_by_id(agent_id: int) -> Optional[Agent]:
    """READ - Get an agent by ID"""
    engine = get_engine()
    with Session(engine) as session:
        return session.get(Agent, agent_id)


def authenticate_agent(username: str, password: str) -> Optional[Agent]:
    """Authenticate an agent by username and password"""
    agent = get_agent_by_username(username)
    if agent and agent.password == password:
        return agent
    return None


def get_all_agents():
    """READ - Get all agents"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(Agent)
        agents = session.exec(statement).all()
        return agents
