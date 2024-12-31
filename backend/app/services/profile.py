import base64
from flask import current_app
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from bson import ObjectId
from app.models.profile import AlumniProfile
from bson.binary import Binary



class ProfileService:
    def __init__(self, database: None):
        self.db = database
        
    async def create_profile(self, profile_data: Dict[str, Any]) -> Optional[AlumniProfile]:
        """Create a new alumni profile with vector embedding."""
        try:
            
            profile_data['dateUpdated'] = datetime.now(timezone.utc)
    
            result = self.db.alumniProfiles.insert_one(profile_data)
            
            created_profile = self.db.alumniProfiles.find_one(
                {'_id': result.inserted_id}
            )
            
            if created_profile:
                # Convert ObjectId to string for JSON serialization
                created_profile['_id'] = str(created_profile['_id'])
                if 'alumniEmb' in created_profile:
                    created_profile['alumniEmb'] = base64.b64encode(created_profile['alumniEmb']).decode('utf-8')
                return created_profile
                
            return None
            
        except Exception as e:
            print(f"Error creating profile: {str(e)}")
            return None 
        
    def get_profile(self, profile_id: str) -> Optional[AlumniProfile]:
        """Retrieve a profile by ID."""
        try:
            object_id = ObjectId(profile_id)
            profile_data = self.db.alumniProfiles.find_one(
                {'_id': object_id}
            )
            
            if not profile_data:
                return None
            
            return AlumniProfile.parse_obj(profile_data) 
        
        except Exception as e:
            print(f"Error retrieving profile: {str(e)}")
            return None
        
    async def update_profile(
        self,
        profile_id: str,
        update_data: Dict[str, Any]
    ) -> Optional[AlumniProfile]:
        """Update an existing profile and its vector embedding."""
        try:
            update_data['dateUpdated'] = datetime.now(timezone.utc)

            result = await self.db.alumniProfiles.find_one_and_update(
                {'_id': ObjectId(profile_id)},
                {'$set': update_data},
                return_document=True
            )
            
            if not result:
                return None
            
            profile = AlumniProfile(**result)
            
            return profile
        except Exception as e:
            print(f"Error updating profile: {str(e)}")
            return None
        
    async def delete_profile(self, profile_id: str) -> bool:
        """Delete a profile and its associated vector."""
        try:
            # Delete profile
            result = await self.db.alumniProfiles.delete_one(
                {'_id': ObjectId(profile_id)}
            )
            
            if result.deleted_count == 0:
                return False
            
            return True
        except Exception as e:
            print(f"Error deleting profile: {str(e)}")
            return False

    async def create_many_profiles(
        self,
        profiles_data: List[Dict[str, Any]]
    ) -> List[AlumniProfile]:
        """Batch create multiple profiles with vector embeddings."""
        created_profiles = []
        
        for profile_data in profiles_data:
            try:
                profile = await self.create_profile(profile_data)
                if profile:
                    created_profiles.append(profile)
            except Exception as e:
                print(f"Error in batch profile creation: {str(e)}")
                continue
        
        return created_profiles