import json
import os
from typing import Optional


CURRENT_AGENT_FILE = "current_agent.json"


def save_current_agent(agent_id: int, username: str, name: str):
    """Save the currently logged-in agent to a file"""
    agent_data = {
        "id": agent_id,
        "username": username,
        "name": name
    }
    with open(CURRENT_AGENT_FILE, "w", encoding="utf-8") as f:
        json.dump(agent_data, f, ensure_ascii=False, indent=2)


def load_current_agent() -> Optional[dict]:
    """Load the currently logged-in agent from file"""
    if not os.path.exists(CURRENT_AGENT_FILE):
        return None
    
    try:
        with open(CURRENT_AGENT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def clear_current_agent():
    """Clear the current agent (logout)"""
    if os.path.exists(CURRENT_AGENT_FILE):
        os.remove(CURRENT_AGENT_FILE)
