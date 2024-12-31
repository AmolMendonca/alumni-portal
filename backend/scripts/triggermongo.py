import logging
from typing import Dict, Any, Optional
from datetime import datetime
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
import cohere
import numpy as np
from bson import ObjectId
from bson.binary import Binary, BinaryVectorDtype
import certifi

class AlumniVectorGenerator:
    def __init__(
        self,
        mongo_uri: str,
        database_name: str,
        collection_name: str,
        cohere_api_key: str,
        model_name: str = "embed-english-v3.0"
    ):
        """
        Initialize the AlumniVectorGenerator with necessary configurations.
        
        Args:
            mongo_uri: MongoDB connection string
            database_name: Name of the database
            collection_name: Name of the collection containing alumni profiles
            cohere_api_key: API key for Cohere
            model_name: Name of the embedding model to use
        """
        # Set up logging
        self.logger = logging.getLogger("AlumniVectorGenerator")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        
        self.client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
        self.db: Database = self.client[database_name]
        self.collection: Collection = self.db[collection_name]
        
        
        self.cohere_client = cohere.Client(cohere_api_key)
        self.model_name = model_name

    def create_profile_text(self, profile: Dict[str, Any]) -> str:
        """
        Create a text representation of the alumni profile for embedding generation.
        
        Args:
            profile: Dictionary containing alumni profile data
            
        Returns:
            Formatted string containing relevant profile information
        """
        # Build a comprehensive text representation of the profile
        text_components = []
        
        # Add basic information
        if profile.get('fullName'):
            text_components.append(f"Name: {profile['fullName']}")
        
        if profile.get('currentRole'):
            text_components.append(f"Current Role: {profile['currentRole']}")
        
        if profile.get('company'):
            text_components.append(f"Company: {profile['company']}")
            
        # Add education information
        if profile.get('university'):
            text_components.append(f"University: {profile['university']}")
            
        if profile.get('highSchool'):
            text_components.append(f"High School: {profile['highSchool']}")
        
            
        return ' '.join(text_components)

    # def generate_vector(self, profile: Dict[str, Any]) -> Optional[list]:
    #     """
    #     Generate a vector embedding for a single profile.
    #     Returns the raw vector instead of Binary type for compatibility.
    #     """
    #     try:
    #         profile_text = self.create_profile_text(profile)
            
    #         # Generate embedding using Cohere
    #         response = self.cohere_client.embed(
    #             texts=[profile_text],
    #             model=self.model_name,
    #             input_type="search_document"
    #         )
            
    #         # Access embeddings correctly from response
    #         # The embeddings property returns a list of embeddings
    #         embeddings = response.embeddings
            
    #         # Since we only passed one text, get the first embedding
    #         if embeddings and len(embeddings) > 0:
    #             return embeddings[0]
    #         else:
    #             self.logger.warning(f"No embeddings generated for profile {profile.get('_id')}")
    #             return None
            
    #     except Exception as e:
    #         self.logger.error(f"Error generating vector for profile {profile.get('_id')}: {str(e)}")
    #         return None
        
    
    def generate_vector_int8(self, profile: Dict[str, Any]) -> Optional[Binary]:
        """
        Generate an int8 vector embedding for a single profile and convert to BSON Binary format.
        """
        try:
            profile_text = self.create_profile_text(profile)
            
            # Generate embedding using Cohere with int8 type
            response = self.cohere_client.embed(
                texts=[profile_text],
                model=self.model_name,
                input_type="search_document",
                embedding_types=["int8"]
            )
            
            # Get the int8 embeddings
            embeddings = response.embeddings.int8
            
            if embeddings and len(embeddings) > 0:
                # Convert to BSON Binary format with int8 dtype
                bson_vector = Binary.from_vector(embeddings[0], BinaryVectorDtype.INT8)
                return bson_vector
            else:
                self.logger.warning(f"No embeddings generated for profile {profile.get('_id')}")
                return None
            
        except Exception as e:
            self.logger.error(f"Error generating vector for profile {profile.get('_id')}: {str(e)}")
            return None
        
    def process_profiles(self, batch_size: int = 100) -> None:
            """
            Process all profiles in the database, generating and storing embeddings.
            Processes all profiles regardless of existing embeddings.
            """
            try:
                # Get total count of all profiles
                total_profiles = self.collection.count_documents({})
                self.logger.info(f"Found {total_profiles} total profiles to process")
                
                processed_count = 0
                failed_count = 0
                
                # Process all profiles
                for profile in self.collection.find({}):
                    try:
                        profile_id = profile['_id']
                        self.logger.info(f"Processing profile {profile_id}")
                        
                        vector = self.generate_vector_int8(profile)
                        
                        if vector is not None:
                            self.collection.update_one(
                                {"_id": profile_id},
                                {
                                    "$set": {
                                        "alumniEmb": vector,
                                        "embeddingGeneratedAt": datetime.utcnow()
                                    }
                                }
                            )
                            processed_count += 1
                            self.logger.info(f"Successfully processed profile {profile_id} ({processed_count}/{total_profiles})")
                        else:
                            failed_count += 1
                            self.logger.warning(f"Failed to generate vector for profile {profile_id}")
                            
                    except Exception as e:
                        failed_count += 1
                        self.logger.error(f"Error processing profile {profile_id}: {str(e)}")
                        continue
                        
                self.logger.info(f"Processing completed. Successful: {processed_count}, Failed: {failed_count}")
                
            except Exception as e:
                self.logger.error(f"Error in batch processing: {str(e)}")

def main():
    # Configuration
    MONGO_URI = "mongodb+srv://ksatvik:S9050756696k@cluster0.z3sbo.mongodb.net/myDatabase?retryWrites=true&w=majority"
    DB_NAME = "alum_ni"
    COLLECTION_NAME = "alumniProfiles"
    COHERE_API_KEY = "vaqsyNNL5LBRH1ZQ9BhWb4Zw3Ef0insOnRwNTeT3"
    
    # Initialize and run the vector generator
    generator = AlumniVectorGenerator(
        mongo_uri=MONGO_URI,
        database_name=DB_NAME,
        collection_name=COLLECTION_NAME,
        cohere_api_key=COHERE_API_KEY
    )
    
    generator.process_profiles()

if __name__ == "__main__":
    main()