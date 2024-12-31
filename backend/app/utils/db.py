# app/utils/db.py
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.server_api import ServerApi
import asyncio
from functools import lru_cache
import os
from urllib.parse import quote_plus
import certifi
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    _instance: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """
        Get MongoDB client using singleton pattern.
        Returns cached instance if exists, creates new one if needed.
        """
        if cls._instance is None:
            try:
                # Get configuration from environment variables with defaults
                mongodb_url = os.getenv('MONGODB_URL')
                
                if mongodb_url:
                    # Use complete URL if provided
                    uri = mongodb_url
                else:
                    # Construct URL from individual components
                    username = quote_plus(os.getenv('MONGODB_USERNAME', ''))
                    password = quote_plus(os.getenv('MONGODB_PASSWORD', ''))
                    host = os.getenv('MONGODB_HOST', 'localhost')
                    port = os.getenv('MONGODB_PORT', '27017')
                    database = os.getenv('MONGODB_DATABASE', 'alumni_search')

                    if username and password:
                        uri = f"mongodb://{username}:{password}@{host}:{port}/{database}"
                    else:
                        uri = f"mongodb://{host}:{port}/{database}"

                # Create client with optimized settings
                cls._instance = AsyncIOMotorClient(
                    uri,
                    server_api=ServerApi('1'),
                    maxPoolSize=50,
                    minPoolSize=10,
                    maxIdleTimeMS=50000,
                    connectTimeoutMS=20000,
                    retryWrites=True,
                    w='majority',
                    tlsCAFile=certifi.where()  # For secure connections
                )
                
                logger.info("MongoDB client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize MongoDB client: {str(e)}")
                raise

        return cls._instance

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Get database instance."""
        if cls._db is None:
            client = cls.get_client()
            cls._db = client[os.getenv('MONGODB_DATABASE', 'alumni_search')]
        return cls._db

async def init_db() -> None:
    """
    Initialize database connection and verify connectivity.
    Should be called during application startup.
    """
    try:
        client = DatabaseConnection.get_client()
        # Verify connection
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        
        # Initialize indexes
        await create_indexes()
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise

async def close_db() -> None:
    """
    Close database connection.
    Should be called during application shutdown.
    """
    if DatabaseConnection._instance:
        DatabaseConnection._instance.close()
        DatabaseConnection._instance = None
        DatabaseConnection._db = None
        logger.info("Closed MongoDB connection")

@lru_cache()
def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance with caching.
    This is the main function that should be imported and used by other modules.
    """
    return DatabaseConnection.get_database()

async def create_indexes() -> None:
    """
    Create necessary indexes for the application.
    Called during database initialization.
    """
    try:
        db = get_database()
        
        # Indexes for alumni_profiles collection
        await db.alumni_profiles.create_indexes([
            # Basic profile fields
            {'key': [('fullName', 1)], 'background': True},
            {'key': [('currentRole', 1)], 'background': True},
            {'key': [('company', 1)], 'background': True},
            {'key': [('university', 1)], 'background': True},
            {'key': [('highSchool', 1)], 'background': True},
            {'key': [('dateUpdated', -1)], 'background': True},
            
            # Compound indexes for common queries
            {'key': [('company', 1), ('currentRole', 1)], 'background': True},
            {'key': [('university', 1), ('currentRole', 1)], 'background': True}
        ])
        
        # Indexes for profile_vectors collection
        await db.profile_vectors.create_indexes([
            # Unique index on alumniId
            {'key': [('alumniId', 1)], 'unique': True, 'background': True}
        ])
        
        logger.info("Successfully created database indexes")
    except Exception as e:
        logger.error(f"Failed to create indexes: {str(e)}")
        raise

async def health_check() -> bool:
    """
    Perform a health check on the database.
    Returns True if database is healthy, False otherwise.
    """
    try:
        client = DatabaseConnection.get_client()
        await client.admin.command('ping')
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return False