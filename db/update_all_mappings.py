import psycopg2
import numpy as np
from sentence_transformers import SentenceTransformer

# Database connection details
DB_NAME = "alumni"
DB_USER = "satvik"
DB_PASSWORD = "12345"
DB_HOST = "localhost"
DB_PORT = "5432"

# Initialize the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Establish database connection
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

# Fetch all profiles from the AlumniProfiles table
cursor.execute("SELECT AlumniID, FullName, CurrentRole, Company, University, HighSchool FROM AlumniProfiles;")
profiles = cursor.fetchall()

# Iterate over each profile and generate new vectors
for profile in profiles:
    alumni_id = profile[0]
    profile_text = f"{profile[1]} at {profile[3]}, graduated from {profile[4]}"
    
    # Generate the vector embedding
    new_vector = model.encode(profile_text).astype('float32').tobytes()
    
    # Update or insert the new vector in the FaissMapping table
    cursor.execute("""
        INSERT INTO FaissMapping (AlumniID, Vector)
        VALUES (%s, %s)
        ON CONFLICT (AlumniID)
        DO UPDATE SET Vector = EXCLUDED.Vector;
    """, (alumni_id, new_vector))
    conn.commit()
    print(f"Updated vector for AlumniID {alumni_id}")

# Close the connection
cursor.close()
conn.close()

print("All vectors have been updated in the FaissMapping table.")
