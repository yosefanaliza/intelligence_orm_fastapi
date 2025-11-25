"""
Agent Service - Business Logic Layer for Agent Operations
"""
from typing import Optional, List
from app.models import Agent
from app.dal import agent_dal


def create_agent(name: str, username: str, password: str) -> Agent:
    """
    Create a new agent
    
    Args:
        name: Full name of the agent
        username: Unique username
        password: Password for authentication
        
    Returns:
        Created Agent object
        
    Raises:
        ValueError: If username already exists
    """
    # Check if username already exists
    existing_agent = agent_dal.get_agent_by_username(username)
    if existing_agent:
        raise ValueError(f"Username '{username}' already exists")
    
    # Create the agent
    return agent_dal.create_agent(name, username, password)


def authenticate_agent(username: str, password: str) -> Optional[Agent]:
    """
    Authenticate an agent
    
    Args:
        username: Agent's username
        password: Agent's password
        
    Returns:
        Agent object if authentication successful, None otherwise
    """
    return agent_dal.authenticate_agent(username, password)


def get_agent_by_id(agent_id: int) -> Optional[Agent]:
    """
    Get agent by ID
    
    Args:
        agent_id: ID of the agent
        
    Returns:
        Agent object if found, None otherwise
    """
    return agent_dal.get_agent_by_id(agent_id)


def get_agent_by_username(username: str) -> Optional[Agent]:
    """
    Get agent by username
    
    Args:
        username: Username of the agent
        
    Returns:
        Agent object if found, None otherwise
    """
    return agent_dal.get_agent_by_username(username)


def get_all_agents():
    """
    Get all agents
    
    Returns:
        List of all agents
    """
    return agent_dal.get_all_agents()
