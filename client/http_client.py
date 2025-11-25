"""
HTTP Client Utilities for Terminal Client

This module provides functions to make HTTP requests to the API server.
It handles request formatting, error handling, and response parsing.
"""
import httpx
from typing import Optional, Dict, Any


# API Configuration
API_BASE_URL = "http://localhost:8000"
API_V1_PREFIX = "/api/v1"
API_TIMEOUT = 30.0  # seconds


class APIClient:
    """HTTP client for making requests to the Intelligence API"""
    
    def __init__(self, base_url: str = API_BASE_URL, api_prefix: str = API_V1_PREFIX):
        self.base_url = base_url
        self.api_prefix = api_prefix
        self.timeout = API_TIMEOUT
    
    def _handle_response(self, response: httpx.Response) -> Dict[Any, Any]:
        """
        Handle API response and raise appropriate errors
        
        Args:
            response: HTTP response object
            
        Returns:
            Parsed JSON response
            
        Raises:
            Exception: If request failed
        """
        try:
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # Extract error detail from response if available
            try:
                error_data = e.response.json()
                error_msg = error_data.get("detail", str(e))
            except:
                error_msg = str(e)
            raise Exception(f"API Error: {error_msg}")
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def login(self, username: str, password: str) -> Dict[Any, Any]:
        """
        Login agent
        
        Args:
            username: Agent username
            password: Agent password
            
        Returns:
            Agent information
        """
        url = f"{self.base_url}{self.api_prefix}/agents/login"
        data = {"username": username, "password": password}
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=data)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def register(self, name: str, username: str, password: str) -> Dict[Any, Any]:
        """
        Register new agent
        
        Args:
            name: Full name
            username: Username
            password: Password
            
        Returns:
            Created agent information
        """
        url = f"{self.base_url}{self.api_prefix}/agents/register"
        data = {"name": name, "username": username, "password": password}
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=data)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def create_terrorist(
        self, 
        name: str, 
        affiliation: Optional[str] = None, 
        location: Optional[str] = None
    ) -> Dict[Any, Any]:
        """
        Create new terrorist record
        
        Args:
            name: Terrorist name
            affiliation: Organization
            location: Area of activity
            
        Returns:
            Created terrorist information
        """
        url = f"{self.base_url}{self.api_prefix}/terrorists/"
        data = {
            "name": name,
            "affiliation": affiliation,
            "location": location
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=data)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def create_report(
        self, 
        content: str, 
        agent_id: int, 
        terrorist_id: int
    ) -> Dict[Any, Any]:
        """
        Create new intelligence report
        
        Args:
            content: Report content
            agent_id: ID of agent creating report
            terrorist_id: ID of terrorist being reported on
            
        Returns:
            Created report information
        """
        url = f"{self.base_url}{self.api_prefix}/reports/"
        data = {
            "content": content,
            "agent_id": agent_id,
            "terrorist_id": terrorist_id
        }
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=data)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def delete_report(self, report_id: int, agent_id: Optional[int] = None) -> Dict[Any, Any]:
        """
        Delete a report
        
        Args:
            report_id: ID of report to delete
            agent_id: Optional - ID of agent requesting deletion
            
        Returns:
            Success message
        """
        url = f"{self.base_url}{self.api_prefix}/reports/{report_id}"
        params = {}
        if agent_id is not None:
            params["agent_id"] = agent_id
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.delete(url, params=params)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def search_reports_by_text(self, keyword: str) -> list:
        """
        Search reports by keyword
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching reports
        """
        url = f"{self.base_url}{self.api_prefix}/reports/search/text"
        params = {"keyword": keyword}
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, params=params)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def search_reports_by_terrorist(self, terrorist_id: int) -> Dict[Any, Any]:
        """
        Search reports by terrorist ID
        
        Args:
            terrorist_id: ID of terrorist
            
        Returns:
            Dictionary with total count and first 5 reports
        """
        url = f"{self.base_url}{self.api_prefix}/reports/search/terrorist/{terrorist_id}"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def get_dangerous_terrorists(self) -> list:
        """
        Get dangerous terrorists (>5 reports)
        
        Returns:
            List of dangerous terrorists with report counts
        """
        url = f"{self.base_url}{self.api_prefix}/reports/dangerous"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def get_super_dangerous_terrorists(self) -> list:
        """
        Get super dangerous terrorists (>10 reports with weapon keywords)
        
        Returns:
            List of super dangerous terrorists with report counts
        """
        url = f"{self.base_url}{self.api_prefix}/reports/super-dangerous"
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
    
    def execute_sql(self, query: str) -> Dict[Any, Any]:
        """
        Execute raw SQL query
        
        Args:
            query: SQL query to execute
            
        Returns:
            Query results
        """
        url = f"{self.base_url}{self.api_prefix}/sql/execute"
        data = {"query": query}
        
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=data)
                return self._handle_response(response)
        except httpx.ConnectError:
            raise Exception("Cannot connect to server. Is the server running?")
