"""
Core configuration module
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Intelligence Reporting System"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = """
    HTTP API for the Intelligence Reporting System.
    
    This API provides endpoints for:
    - **Agent Management**: Register and authenticate agents
    - **Terrorist Management**: Create and retrieve terrorist records
    - **Intelligence Reports**: Create, search, and delete intelligence reports
    - **Analytics**: Find dangerous and super dangerous terrorists
    - **SQL Execution**: Execute raw SQL queries (admin only)
    """
    
    # Database Settings
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "SQLnov8ING"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: str = "3306"
    MYSQL_DATABASE: str = "intelligence"
    
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list = ["*"]
    
    @property
    def DATABASE_URI(self) -> str:
        """Generate database connection URI"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    class Config:
        case_sensitive = True


settings = Settings()
