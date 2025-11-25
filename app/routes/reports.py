"""
Report endpoint routes
"""
from typing import List
from fastapi import APIRouter, Query, HTTPException, status
from app.schemas.report_schemas import (
    ReportCreate,
    ReportResponse,
    ReportSearchResponse,
    DangerousTerroristResponse,
)
from app.services import report_service

router = APIRouter()


@router.post("/", response_model=ReportResponse, status_code=201)
def create_report_endpoint(report_data: ReportCreate):
    """
    Create a new intelligence report
    
    - **content**: Content of the intelligence report
    - **agent_id**: ID of the agent creating the report
    - **terrorist_id**: ID of the terrorist being reported on
    """
    try:
        report = report_service.create_report(
            content=report_data.content,
            agent_id=report_data.agent_id,
            terrorist_id=report_data.terrorist_id
        )
        return ReportResponse.model_validate(report)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create report: {str(e)}"
        )


@router.delete("/{report_id}")
def delete_report_endpoint(
    report_id: int,
    agent_id: int = Query(None, description="ID of the agent requesting deletion")
):
    """
    Delete a report
    
    - **report_id**: ID of the report to delete
    - **agent_id**: Optional - ID of the agent requesting deletion (for authorization)
    """
    try:
        success = report_service.delete_report(report_id, agent_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Report with ID {report_id} not found"
            )
        
        return {"message": f"Report {report_id} deleted successfully"}
    except PermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete report: {str(e)}"
        )


@router.get("/search/text", response_model=List[ReportSearchResponse])
def search_reports_by_text_endpoint(
    keyword: str = Query(..., description="Keyword to search for in report content")
):
    """
    Search reports by keyword in content
    
    - **keyword**: Keyword to search for
    """
    try:
        reports = report_service.search_reports_by_text(keyword)
        return [ReportSearchResponse.model_validate(r) for r in reports]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/search/terrorist/{terrorist_id}")
def search_reports_by_terrorist_endpoint(terrorist_id: int):
    """
    Search reports by terrorist ID
    
    Returns total count and first 5 reports
    
    - **terrorist_id**: ID of the terrorist
    """
    try:
        result = report_service.search_reports_by_terrorist(terrorist_id)
        return {
            "total_count": result["total_count"],
            "reports": [ReportSearchResponse.model_validate(r) for r in result["reports"]]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/dangerous", response_model=List[DangerousTerroristResponse])
def get_dangerous_terrorists_endpoint():
    """
    Get dangerous terrorists (more than 5 reports)
    
    Returns list of terrorists with their report counts
    """
    try:
        terrorists = report_service.get_dangerous_terrorists()
        return [DangerousTerroristResponse.model_validate(t) for t in terrorists]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve dangerous terrorists: {str(e)}"
        )


@router.get("/super-dangerous", response_model=List[DangerousTerroristResponse])
def get_super_dangerous_terrorists_endpoint():
    """
    Get super dangerous terrorists
    
    Criteria: >10 reports AND contains weapon keywords (פיגוע, סכין, רובה, אקדח, פצצה)
    
    Returns list of terrorists with their report counts
    """
    try:
        terrorists = report_service.get_super_dangerous_terrorists()
        return [DangerousTerroristResponse.model_validate(t) for t in terrorists]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve super dangerous terrorists: {str(e)}"
        )
