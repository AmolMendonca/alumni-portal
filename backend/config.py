# config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration"""
    
    # Application Settings
    APP_NAME = "Alumni Search"
    API_PREFIX = "/api/v1"
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Server Settings
    SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVER_PORT = int(os.getenv('SERVER_PORT', 8000))
    
    # CORS Settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    CORS_ALLOWED_HEADERS = ['Content-Type', 'Authorization']
    
    # MongoDB Settings
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'alum_ni')
    MONGO_MIN_POOL_SIZE = int(os.getenv('MONGO_MIN_POOL_SIZE', 10))
    MONGO_MAX_POOL_SIZE = int(os.getenv('MONGO_MAX_POOL_SIZE', 50))
    
    # Cohere settings
    COHERE_KEY = os.getenv('COHERE_KEY')
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    @classmethod
    def verify_env_variables(cls) -> None:
        """Verify that all required environment variables are set"""
        required_vars = [
            ('MONGO_URI', cls.MONGO_URI),
        ]
        
        missing_vars = [var[0] for var in required_vars if not var[1]]
        
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )