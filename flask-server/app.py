import sys
import os
import traceback  # Add this import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import certifi
import faiss
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import Binary
from sentence_transformers import SentenceTransformer
from db.db_utils import insert_alumni_profile, insert_vector, get_profiles_from_indices

app = Flask(__name__)

MONGO_URI = "mongodb+srv://ksatvik:S9050756696k@cluster0.z3sbo.mongodb.net/myDatabase?retryWrites=true&w=majority"

# Configure CORS properly
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept"],
        "expose_headers": ["Content-Type", "Accept"]
    }
})

print("Initializing model and index...")
model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384
faiss_index = faiss.IndexFlatL2(dimension)
profile_ids = []  # Will be populated by load_vectors()

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/search', methods=['POST'])
def search_profiles():
    try:
        print("\n=== Starting Search ===")
        data = request.get_json()
        print("Received request data:", data)
        
        query = data.get('query')
        k = min(data.get('k', 5), len(profile_ids))  # Don't request more than we have

        if not query:
            return jsonify({"status": "error", "message": "Missing query"}), 400

        print(f"Processing query: '{query}' for k={k}")
        print(f"Current profile_ids count: {len(profile_ids)}")

        # Generate query embedding
        query_embedding = model.encode(query).astype("float32").reshape(1, -1)
        print("Generated query embedding with shape:", query_embedding.shape)

        # Perform FAISS search
        distances, indices = faiss_index.search(query_embedding, k)
        print("FAISS search results:")
        print("- Indices:", indices)
        print("- Distances:", distances)

        # Get result IDs
        result_ids = []
        for idx in indices[0]:
            if idx >= 0 and idx < len(profile_ids):
                result_id = profile_ids[idx]
                result_ids.append(result_id)
                print(f"Added result ID: {result_id}")

        print(f"Found {len(result_ids)} valid results")

        if not result_ids:
            print("No valid results found")
            return jsonify({
                "status": "success",
                "results": [],
                "message": "No matching profiles found"
            })

        # Get detailed results from MongoDB
        print("Fetching detailed results from MongoDB")
        detailed_results = get_profiles_from_indices(result_ids)
        print(f"Retrieved {len(detailed_results)} detailed results")

        # Build response
        response = []
        for idx, result_id in enumerate(result_ids):
            matching_result = next(
                (r for r in detailed_results if str(r['_id']) == str(result_id)),
                None
            )
            if matching_result:
                profile = {
                    "AlumniID": str(matching_result['_id']),
                    "FullName": matching_result.get('fullName', 'N/A'),
                    "CurrentRole": matching_result.get('currentRole', 'N/A'),
                    "Company": matching_result.get('company', 'N/A'),
                    "University": matching_result.get('university', 'N/A'),
                    "HighSchool": matching_result.get('highSchool', 'N/A'),
                    "LinkedInURL": matching_result.get('linkedInURL', 'N/A'),
                    "Distance": float(distances[0][idx])
                }
                response.append(profile)
                print(f"Added profile to response: {profile['FullName']}")

        print(f"Final response has {len(response)} profiles")
        return jsonify({
            "status": "success",
            "results": response,
            "count": len(response)
        })

    except Exception as e:
        print("\nError in search:")
        print(traceback.format_exc())
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
# Make sure these are at the module level
print("Initializing model and index...")
model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384
faiss_index = faiss.IndexFlatL2(dimension)

@app.route('/add-profile', methods=['POST'])
def add_profile():
    try:
        data = request.get_json()
        required_fields = ['FullName', 'CurrentRole', 'Company', 'University', 'HighSchool', 'LinkedInURL']
        
        if not all(field in data for field in required_fields):
            return jsonify({"status": "error", "message": "Missing required fields"}), 400

        # Insert the profile
        profile_result = insert_alumni_profile(
            data['FullName'],
            data['CurrentRole'],
            data['Company'],
            data['University'],
            data['HighSchool'],
            data['LinkedInURL']
        )

        if profile_result['status'] == 'success':
            alumni_id = profile_result['alumni_id']
            
            # Generate embedding text
            profile_text = (
                f"{data['FullName']} works as {data['CurrentRole']} at {data['Company']}, "
                f"graduated from {data['University']} and attended {data['HighSchool']}"
            )
            
            # Generate vector embedding
            vector = model.encode(profile_text).astype('float32')
            
            # Store vector as bytes in MongoDB
            vector_bytes = vector.tobytes()
            
            # Connect to MongoDB
            client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
            db = client['alum_ni']
            faiss_mapping = db['faissMapping']
            
            # Insert vector mapping
            faiss_mapping.insert_one({
                'alumniId': str(alumni_id),
                'vector': vector_bytes  # Store as bytes
            })
            
            # Add to FAISS index
            faiss_index.add(vector.reshape(1, -1))
            profile_ids.append(str(alumni_id))
            
            return jsonify({
                "status": "success",
                "message": "Profile added successfully"
            }), 201
        else:
            return jsonify(profile_result), 500
            
    except Exception as e:
        print("Error adding profile:", str(e))
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

def load_vectors():
    try:
        print("\n=== Loading Vectors ===")
        client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
        db = client['alum_ni']
        faiss_mapping = db['faissMapping']
        
        print("Connected to MongoDB, fetching vectors...")
        data = list(faiss_mapping.find({}, {'alumniId': 1, 'vector': 1}))
        print(f"Found {len(data)} vector records in MongoDB")

        profile_ids = []
        vectors = []

        for record in data:
            try:
                # Skip if vector is a string
                if isinstance(record['vector'], str):
                    print(f"Skipping invalid vector for profile {record['alumniId']}")
                    continue
                    
                vector = np.frombuffer(record['vector'], dtype='float32')
                if vector.shape[0] != dimension:
                    print(f"Skipping vector with wrong dimension for profile {record['alumniId']}")
                    continue
                    
                profile_ids.append(record['alumniId'])
                vectors.append(vector)
                print(f"Processed vector for profile: {record['alumniId']}")
                
            except Exception as e:
                print(f"Error processing vector for profile {record['alumniId']}: {str(e)}")
                continue

        print(f"Successfully processed {len(vectors)} vectors")

        if vectors:
            try:
                vectors_array = np.array(vectors)
                print("Vector array shape:", vectors_array.shape)
                faiss_index.add(vectors_array)
                print("Successfully added vectors to FAISS index")
            except ValueError as e:
                print("Error adding vectors to FAISS index:", e)

        return profile_ids
    except Exception as e:
        print("\nError in load_vectors:")
        print(traceback.format_exc())
        return []

# Also let's add a utility function to rebuild the index if needed
@app.route('/rebuild-index', methods=['POST'])
def rebuild_index():
    try:
        global faiss_index
        global profile_ids
        
        # Reset the index
        faiss_index = faiss.IndexFlatL2(dimension)
        profile_ids = load_vectors()
        
        return jsonify({
            "status": "success",
            "message": f"Index rebuilt with {len(profile_ids)} profiles"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 
        
if __name__ == '__main__':
    print("Starting server...")
    print("Initializing search components...")
    
    # Clear and reinitialize FAISS index
    faiss_index = faiss.IndexFlatL2(dimension)
    
    # Load vectors
    profile_ids = load_vectors()
    
    print(f"\nServer initialized with {len(profile_ids)} profiles")
    app.run(debug=True, host='0.0.0.0', port=8000)
