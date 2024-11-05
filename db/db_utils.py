import traceback
from pymongo import MongoClient
from bson import ObjectId  # Add this import
import certifi

MONGO_URI = "mongodb+srv://ksatvik:S9050756696k@cluster0.z3sbo.mongodb.net/myDatabase?retryWrites=true&w=majority"

def get_db_connection():
    return MongoClient(MONGO_URI, tlsCAFile=certifi.where())

def get_profiles_from_indices(result_ids):
    try:
        print("Getting profiles for IDs:", result_ids)
        client = get_db_connection()
        db = client['alum_ni']
        alumni_profiles = db['alumniProfiles']
        
        # Convert string IDs to ObjectId
        object_ids = [ObjectId(id_) for id_ in result_ids]
        
        # Find the profiles
        results = list(alumni_profiles.find({'_id': {'$in': object_ids}}))
        print(f"Found {len(results)} profiles")
        
        # Debug output
        for result in results:
            print(f"Found profile: {result.get('fullName', 'N/A')}")
            
        return results
    except Exception as e:
        print("Error in get_profiles_from_indices:")
        print(traceback.format_exc())
        return []
    finally:
        if 'client' in locals():
            client.close()

def insert_alumni_profile(full_name, current_role, company, university, high_school, linkedin_url):
    try:
        client = get_db_connection()
        db = client['alum_ni']
        alumni_profiles = db['alumniProfiles']
        
        result = alumni_profiles.insert_one({
            'fullName': full_name,
            'currentRole': current_role,
            'company': company,
            'university': university,
            'highSchool': high_school,
            'linkedInURL': linkedin_url
        })
        
        return {"status": "success", "alumni_id": result.inserted_id}
    except Exception as e:
        print("Error in insert_alumni_profile:")
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}
    finally:
        if 'client' in locals():
            client.close()

def insert_vector(alumni_id, profile_text):
    try:
        client = get_db_connection()
        db = client['alum_ni']
        faiss_mapping = db['faissMapping']
        
        result = faiss_mapping.insert_one({
            'alumniId': alumni_id,
            'vector': profile_text
        })
        
        return {"status": "success"}
    except Exception as e:
        print("Error in insert_vector:")
        print(traceback.format_exc())
        return {"status": "error", "message": str(e)}
    finally:
        if 'client' in locals():
            client.close()