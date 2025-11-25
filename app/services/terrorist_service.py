"""
Terrorist Service - Business Logic Layer for Terrorist Operations
"""
from typing import Optional, List
from app.models import Terrorist
from app.dal import terrorist_dal


def create_terrorist(
    name: str, 
    affiliation: Optional[str] = None, 
    location: Optional[str] = None
) -> Terrorist:
    """
    Create a new terrorist record
    
    Args:
        name: Full name of the terrorist
        affiliation: Organization affiliation
        location: Area of activity
        
    Returns:
        Created Terrorist object
    """
    return terrorist_dal.create_terrorist(name, affiliation, location)


def get_terrorist_by_id(terrorist_id: int) -> Optional[Terrorist]:
    """
    Get terrorist by ID
    
    Args:
        terrorist_id: ID of the terrorist
        
    Returns:
        Terrorist object if found, None otherwise
    """
    return terrorist_dal.get_terrorist_by_id(terrorist_id)


def get_terrorist_by_name(name: str) -> Optional[Terrorist]:
    """
    Get terrorist by exact name
    
    Args:
        name: Exact name of the terrorist
        
    Returns:
        Terrorist object if found, None otherwise
    """
    return terrorist_dal.get_terrorist_by_name(name)


def search_terrorists_by_name(name: str) -> List[Terrorist]:
    """
    Search terrorists by partial name match
    
    Args:
        name: Partial name to search for
        
    Returns:
        List of matching terrorists
    """
    return terrorist_dal.search_terrorists_by_name(name)


def get_all_terrorists() -> List[Terrorist]:
    """
    Get all terrorists
    
    Returns:
        List of all terrorists
    """
    return terrorist_dal.get_all_terrorists()


def get_or_create_terrorist(
    name: str, 
    affiliation: Optional[str] = None, 
    location: Optional[str] = None
) -> Terrorist:
    """
    Get existing terrorist by name or create new one if not found
    
    Args:
        name: Name of the terrorist
        affiliation: Organization affiliation
        location: Area of activity
        
    Returns:
        Terrorist object (existing or newly created)
    """
    terrorist = get_terrorist_by_name(name)
    if not terrorist:
        terrorist = create_terrorist(name, affiliation, location)
    return terrorist
