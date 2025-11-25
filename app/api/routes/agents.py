"""
Agent endpoint routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Engine
from app.api.schemas.agent_schemas import AgentCreate, AgentLogin, AgentResponse
from app.api.services import agent_service
from db.database import get_engine

router = APIRouter()


@router.post("/register", response_model=AgentResponse, status_code=201)
def register_agent_endpoint(
    agent_data: AgentCreate,
    engine: Engine = Depends(get_engine)
):
    """
    Register a new agent
    
    - **name**: Full name of the agent
    - **username**: Unique username (min 3 characters)
    - **password**: Password (min 4 characters)
    """
    try:
        agent = agent_service.create_agent(
            engine,
            name=agent_data.name,
            username=agent_data.username,
            password=agent_data.password
        )
        return AgentResponse.model_validate(agent)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )


@router.post("/login", response_model=AgentResponse)
def login_agent_endpoint(
    login_data: AgentLogin,
    engine: Engine = Depends(get_engine)
):
    """
    Authenticate an agent
    
    - **username**: Agent's username
    - **password**: Agent's password
    """
    try:
        agent = agent_service.authenticate_agent(
            engine,
            username=login_data.username,
            password=login_data.password
        )
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        return AgentResponse.model_validate(agent)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
