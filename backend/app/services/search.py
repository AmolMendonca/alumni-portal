from datetime import datetime
from typing import List, Dict, Any
import cohere
from flask import current_app
from app.models.profile import AlumniProfile
from bson.binary import Binary, BinaryVectorDtype

class SearchService:
    """Service for handling alumni search operations using Atlas Search"""
    
    def __init__(self, database: None, cohere_api_key: str, model_name: str = "embed-english-v3.0"):
        """Initialize the search service with Cohere client"""
        self.co = cohere.Client(cohere_api_key)
        self.model_name = model_name
        self.db = database

    def generate_bson_vector(self, vector, vector_dtype):
        """Convert vector to BSON Binary format"""
        return Binary.from_vector(vector, vector_dtype)
    
    def generate_embedding(self, text: str) -> Binary:
        """Generate int8 embeddings using Cohere and convert to BSON Binary"""
        try:
            response = self.co.embed(
                texts=[text],
                model=self.model_name,
                input_type='search_query',
                embedding_types=["int8"]
            )
            # Get int8 embeddings
            int8_embedding = response.embeddings.int8[0]
            # Convert to BSON Binary format
            bson_vector = self.generate_bson_vector(int8_embedding, BinaryVectorDtype.INT8)
            return bson_vector
        except Exception as e:
            current_app.logger.error(f"Cohere embedding error: {str(e)}")
            raise

    def search_by_text(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        """
        Search alumni profiles using text query with Atlas Search vector search
        
        Args:
            query: Search query text
            k: Number of results to return
            
        Returns:
            List of alumni profiles with similarity scores
        """
        try:
            # Generate query embedding using Cohere
            query_vector = self.generate_embedding(query)
            
            
            # Construct Atlas Search aggregation pipeline
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "alumni_vector_index",
                        "path": "alumniEmb",
                        "queryVector": query_vector,
                        "numCandidates": k * 2,  # Consider more candidates than final results
                        "limit": k
                    }
                },
                {
                    "$project": {
                        "score": {
                            "$meta": "vectorSearchScore"
                        },
                        "fullName": 1,
                        "currentRole": 1,
                        "company": 1,
                        "university": 1,
                        "highSchool": 1,
                        "linkedInURL": 1,
                        "dateUpdated": 1,
                        "_id": 1
                    }
                }
            ]
            
            # Execute search using the alumniProfiles collection
            search_results = list(self.db.alumniProfiles.aggregate(pipeline))
            
            results = []
            for result in search_results:
                results.append({
                    "profile": {
                        "_id": str(result["_id"]),  # Convert ObjectId to string
                        "fullName": result.get("fullName"),
                        "currentRole": result.get("currentRole"),
                        "company": result.get("company"),
                        "university": result.get("university"),
                        "highSchool": result.get("highSchool"),
                        "linkedInURL": result.get("linkedInURL"),
                        "dateUpdated": result.get("dateUpdated").isoformat() if result.get("dateUpdated") else None
                    },
                    "similarity_score": result["score"]
                })
            
            
            
            return results
            
        except Exception as e:
            current_app.logger.error(f"Search error: {str(e)}")
            return []