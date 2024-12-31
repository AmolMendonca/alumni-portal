import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.operations import SearchIndexModel
import time
import certifi  

# Connect to your Atlas deployment
uri = "mongodb+srv://ksatvik:S9050756696k@cluster0.z3sbo.mongodb.net/myDatabase?retryWrites=true&w=majority"
client = MongoClient(uri, tlsCAFile=certifi.where())

# Access your database and collection
database = client["alum_ni"]  # Using your actual database name
collection = database["alumniProfiles"]  # Using your actual collection name

# Create your index model for the alumniEmbInt8 field
search_index_model = SearchIndexModel(
    definition={
        "fields": [
            {
                "type": "vector",
                "numDimensions": 1024, 
                "path": "alumniEmb",  # Updated to match the int8 field name
                "similarity": "cosine" # Using cosine similarity
            }
        ]
    },
    name="alumni_vector_index",
    type="vectorSearch"
)

# Create the search index
try:
    result = collection.create_search_index(model=search_index_model)
    print(f"New search index named '{result}' is building.")

    # Wait for initial sync to complete
    print("Polling to check if the index is ready. This may take up to a minute.")
    predicate = lambda index: index.get("queryable") is True
    
    while True:
        indices = list(collection.list_search_indexes(result))
        if len(indices) and predicate(indices[0]):
            print(f"Index '{result}' is ready for querying.")
            break
        print("Still building... checking again in 5 seconds")
        time.sleep(5)

except Exception as e:
    print(f"Error creating search index: {str(e)}")
finally:
    client.close()