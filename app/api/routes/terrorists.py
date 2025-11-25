"""
Terrorist endpoint routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.engine import Engine
from app.api.schemas.terrorist_schemas import TerroristCreate, TerroristResponse
from app.api.services import terrorist_service
from db.database import get_engine

router = APIRouter()


@router.post("/", response_model=TerroristResponse, status_code=201)
def create_terrorist_endpoint(
    terrorist_data: TerroristCreate,
    engine: Engine = Depends(get_engine)
):
    """
    Create a new terrorist record
    
    - **name**: Full name of the terrorist
    - **affiliation**: Organization affiliation (optional)
    - **location**: Area of activity (optional)
    """
    try:
        terrorist = terrorist_service.create_terrorist(
            engine,
            name=terrorist_data.name,
            affiliation=terrorist_data.affiliation,
            location=terrorist_data.location
        )
        return TerroristResponse.model_validate(terrorist)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create terrorist: {str(e)}"
        )


@router.get("/{terrorist_id}", response_model=TerroristResponse)
def get_terrorist_endpoint(
    terrorist_id: int,
    engine: Engine = Depends(get_engine)
):
    """
    Get terrorist by ID
    
    - **terrorist_id**: ID of the terrorist
    """
    try:
        terrorist = terrorist_service.get_terrorist_by_id(engine, terrorist_id)
        if not terrorist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Terrorist with ID {terrorist_id} not found"
            )
        return TerroristResponse.model_validate(terrorist)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve terrorist: {str(e)}"
        )
