"""
Report Service - Business Logic Layer for Report Operations
"""
from typing import Optional, List, Tuple
from app.models import Report, Terrorist
from app.dal import report_dal
from app.services import agent_service, terrorist_service


def create_report(content: str, agent_id: int, terrorist_id: int) -> Report:
    """
    Create a new intelligence report
    
    Args:
        content: Content of the report
        agent_id: ID of the agent creating the report
        terrorist_id: ID of the terrorist being reported on
        
    Returns:
        Created Report object
        
    Raises:
        ValueError: If agent_id or terrorist_id is invalid
    """
    # Validate agent exists
    agent = agent_service.get_agent_by_id(agent_id)
    if not agent:
        raise ValueError(f"Agent with ID {agent_id} not found")
    
    # Validate terrorist exists
    terrorist = terrorist_service.get_terrorist_by_id(terrorist_id)
    if not terrorist:
        raise ValueError(f"Terrorist with ID {terrorist_id} not found")
    
    return report_dal.create_report(content, agent_id, terrorist_id)


def get_report_by_id(report_id: int) -> Optional[Report]:
    """
    Get report by ID
    
    Args:
        report_id: ID of the report
        
    Returns:
        Report object if found, None otherwise
    """
    return report_dal.get_report_by_id(report_id)


def get_all_reports() -> List[Report]:
    """
    Get all reports
    
    Returns:
        List of all reports
    """
    return list(report_dal.get_all_reports())


def get_reports_by_agent(agent_id: int) -> List[Report]:
    """
    Get all reports written by a specific agent
    
    Args:
        agent_id: ID of the agent
        
    Returns:
        List of reports by the agent
    """
    return list(report_dal.get_reports_by_agent(agent_id))


def get_reports_by_terrorist(
    terrorist_id: int, 
    limit: Optional[int] = None
) -> List[Report]:
    """
    Get reports about a specific terrorist
    
    Args:
        terrorist_id: ID of the terrorist
        limit: Maximum number of reports to return
        
    Returns:
        List of reports about the terrorist
    """
    return list(report_dal.get_reports_by_terrorist(terrorist_id, limit))


def search_reports_by_content(keyword: str) -> List[Report]:
    """
    Search reports by keyword in content
    
    Args:
        keyword: Keyword to search for
        
    Returns:
        List of matching reports
    """
    return list(report_dal.search_reports_by_content(keyword))


def search_reports_by_text(keyword: str) -> List[Report]:
    """
    Search reports by keyword in content (alias for search_reports_by_content)
    
    Args:
        keyword: Keyword to search for
        
    Returns:
        List of matching reports
    """
    return search_reports_by_content(keyword)


def search_reports_by_terrorist(terrorist_id: int) -> dict:
    """
    Search reports by terrorist ID, returning count and first 5 reports
    
    Args:
        terrorist_id: ID of the terrorist
        
    Returns:
        Dict with total_count and reports list
    """
    total_count = count_reports_by_terrorist(terrorist_id)
    reports = get_reports_by_terrorist(terrorist_id, limit=5)
    return {
        "total_count": total_count,
        "reports": reports
    }


def delete_report(report_id: int, agent_id: Optional[int] = None) -> bool:
    """
    Delete a report
    
    Args:
        report_id: ID of the report to delete
        agent_id: Optional - ID of the agent requesting deletion (for authorization)
        
    Returns:
        True if deleted successfully, False otherwise
        
    Raises:
        PermissionError: If agent_id is provided and doesn't match report's author
    """
    # Check authorization if agent_id is provided
    if agent_id is not None:
        report = get_report_by_id(report_id)
        if report and report.agent_id != agent_id:
            raise PermissionError("You can only delete your own reports")
    
    return report_dal.delete_report(report_id)


def count_reports_by_terrorist(terrorist_id: int) -> int:
    """
    Count reports for a specific terrorist
    
    Args:
        terrorist_id: ID of the terrorist
        
    Returns:
        Number of reports
    """
    return report_dal.count_reports_by_terrorist(terrorist_id)


def get_dangerous_terrorists(min_reports: int = 5) -> List[Tuple[Terrorist, int]]:
    """
    Get terrorists with more than min_reports reports
    
    Args:
        min_reports: Minimum number of reports to be considered dangerous
        
    Returns:
        List of tuples (Terrorist, report_count)
    """
    return list(report_dal.get_dangerous_terrorists(min_reports))


def get_super_dangerous_terrorists() -> List[Tuple[Terrorist, int]]:
    """
    Get super dangerous terrorists (>10 reports with weapon keywords)
    
    Returns:
        List of tuples (Terrorist, report_count)
    """
    return report_dal.get_super_dangerous_terrorists()
