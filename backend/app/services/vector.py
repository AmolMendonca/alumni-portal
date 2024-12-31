from typing import List, Tuple, Optional
from config import Config
import numpy as np
from bson import ObjectId
from bson.binary import Binary, BinaryVectorDtype
import logging
import cohere
from flask import current_app
from app.models.profile import AlumniProfile

logger = logging.getLogger(__name__)

class VectorService:
    """Service for handling vector operations"""
    
    def __init__(self, model_name: str = 'embed-english-v3.0'):
        """Initialize the vector service"""
        self.co = cohere.Client(Config.COHERE_KEY)
        self.model_name = model_name

    def generate_profile_vector(self, profile: AlumniProfile) -> Binary:
        """
        Generate vector embedding for a profile
        
        Args:
            profile: AlumniProfile instance
            
        Returns:
            binary vector embedding
        """
        # Create text representation of profile
        profile_text = (
            f"{profile.fullName} works as {profile.currentRole} at {profile.company}. "
            f"Graduated from {profile.university} and attended {profile.highSchool}."
        )
        
        gen = self.co.embed(
            texts=[profile_text],
            model=self.model_name,
            input_type="search_document",
            embedding_types=["int8"]).embeddings
        
        vector = gen.int8[0]
        
        varray = np.array(vector, dtype=np.int8)
        
        return Binary.from_vector(varray, BinaryVectorDtype.INT8)

    async def store_vector(self, profile_id: str, vector: Binary) -> bool:
        """
        Store vector embedding in database
        
        Args:
            profile_id: ID of the alumni profile
            vector: Vector embedding
            
        Returns:
            Success status
        """
        try:
            db = current_app.database
            
            # Create or update vector document
            db.alumniProfiles.update_one(
                {"id": profile_id},
                {
                    "$set": {
                        "alumniEmb": vector,
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error storing vector: {str(e)}")
            return False

    async def get_profile_vector(self, profile_id: str) -> Optional[np.ndarray]:
        """Get vector for a specific profile"""
        try:
            db = current_app.database
            vector_doc = db.alumniProfiles.find_one({"alumniId": profile_id})
            
            if vector_doc:
                vector_bytes = vector_doc["vector"]
                return np.frombuffer(vector_bytes, dtype=np.float32)
            return None
        except Exception as e:
            print(f"Error retrieving vector: {str(e)}")
            return None

    async def update_profile_vector(self, profile_id: str) -> bool:
        """
        Update vector for a profile (e.g., after profile updates)
        
        Args:
            profile_id: ID of the profile to update
            
        Returns:
            Success status
        """
        try:
            db = current_app.database
            
            # Get profile
            profile_data = db.alumniProfiles.find_one({"_id": ObjectId(profile_id)})
            if not profile_data:
                return False
                
            profile = AlumniProfile(**profile_data)
            
            # Generate new vector
            new_vector = self.generate_profile_vector(profile)
            
            # Store updated vector
            return await self.store_vector(profile_id, new_vector)
            
        except Exception as e:
            print(f"Error updating vector: {str(e)}")
            return False
