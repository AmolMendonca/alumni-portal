import numpy as np
import datetime
import certifi
from pymongo import MongoClient
from bson import Binary, ObjectId
from sentence_transformers import SentenceTransformer

uri = "mongodb+srv://ksatvik:S9050756696k@cluster0.z3sbo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['alum_ni']  
alumni_profiles = db['alumniProfiles']
faiss_mapping = db['faissMapping']


def insert_alumni_profile(full_name, current_role, company, university, high_school, linkedin_url):
    """Insert an alumni profile into MongoDB and return the inserted ID."""
    try:
        new_profile = {
            "fullName": full_name,
            "currentRole": current_role,
            "company": company,
            "university": university,
            "highSchool": high_school,
            "linkedInURL": linkedin_url,
            "dateUpdated": datetime.datetime.now()
        }
        result = alumni_profiles.insert_one(new_profile)
        return {"status": "success", "alumni_id": str(result.inserted_id)}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    
def insert_vector(alumni_id, profile_text):
    """Generate a vector embedding and insert it into the faissMapping collection."""
    model = SentenceTransformer('all-MiniLM-L6-v2')
    try:
        # Generate the vector embedding
        vector = model.encode(profile_text).astype('float32')
        
        # Insert the vector into the faissMapping collection
        new_vector_entry = {
            "alumniId": alumni_id,
            "vector": Binary(vector.tobytes())
        }
        faiss_mapping.insert_one(new_vector_entry)
        return {"status": "success", "message": "Vector inserted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def get_profiles_from_indices(result_ids):
    """Fetch detailed alumni information based on result IDs in the order of input IDs."""
    if not result_ids:
        return []
    try:
        # Convert result_ids to ObjectId instances
        object_ids = [ObjectId(id) if ObjectId.is_valid(id) else id for id in result_ids]

        # Query the alumniProfiles collection using _id
        results = alumni_profiles.find({"_id": {"$in": object_ids}})
        
        # Convert cursor to a list and create a dictionary for ordering
        result_list = list(results)
        print("Fetched Profiles:", result_list)  # Debug print
        
        if not result_list:
            print("No profiles found for the given IDs.")

        result_dict = {str(item['_id']): item for item in result_list}

        # Order the results based on the input result_ids
        ordered_results = [result_dict[str(alumni_id)] for alumni_id in result_ids if str(alumni_id) in result_dict]
        return ordered_results
    except Exception as e:
        print("Error fetching profiles:", e)
        return []