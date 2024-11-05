import psycopg2
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm



DB_NAME = "alumni"
DB_USER = "satvik"
DB_PASSWORD = "12345"
DB_HOST = "localhost"  
DB_PORT = "5432"

model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384
faiss_index = faiss.IndexFlatL2(dimension)

try:
    
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


    cursor = conn.cursor()


    def get_all_profiles():
        cursor.execute("SELECT * FROM AlumniProfiles;")
        return cursor.fetchall()

    def insert_alumni_profile(full_name, current_role, company, university, high_school, linkedin_url):
        cursor.execute(""" INSERT INTO AlumniProfiles (FullName, CurrentRole, Company, University, HighSchool, LinkedInURL)
                       VALUES (%s, %s, %s, %s, %s, %s);
                       """, (full_name, current_role, company, university, high_school, linkedin_url))

    # Adding five new profiles
    insert_alumni_profile("Alice Johnson", "Data Scientist", "DataWorks", "Stanford University", "Greenfield High School", "https://www.linkedin.com/in/alicejohnson")
    insert_alumni_profile("Bob Lee", "Product Manager", "Innovatech", "Harvard University", "Springfield High School", "https://www.linkedin.com/in/boblee")
    insert_alumni_profile("Catherine Park", "UX Designer", "Creative Solutions", "University of Michigan", "Cathedral and John Connon School", "https://www.linkedin.com/in/catherinepark")
    insert_alumni_profile("David Kim", "Software Engineer", "TechCorp", "MIT", "Horizon High School", "https://www.linkedin.com/in/davidkim")
    insert_alumni_profile("Emma Watson", "Financial Analyst", "Finwise Group", "Yale University", "Sunset High School", "https://www.linkedin.com/in/emmawatson")

    profiles = get_all_profiles()
    print(f"Number of profiles: {len(profiles)}")   
    for profile in profiles:
        print(profile)

    profile_ids = []
    for profile in tqdm(profiles, desc="Embedding profiles"):
        alumni_id = profile[0]
        profile_text = f"{profile[2]} at {profile[3]}, graduated from {profile[4]}"
        embedding = model.encode(profile_text).astype("float32")
        faiss_index.add(np.array([embedding]))
        profile_ids.append(alumni_id)
        
    def search_profiles(query, k=5):
        query_embedding = model.encode(query).astype("float32").reshape(1, -1)
        distances, indices = faiss_index.search(query_embedding, k)
        result_ids = [profile_ids[i] for i in indices[0]]
        return result_ids, distances
    
    def get_profiles_from_indices(result_ids):
        cursor.execute(
            "SELECT AlumniID, FullName, CurrentRole, Company, University, HighSchool, LinkedInURL FROM AlumniProfiles WHERE AlumniID IN %s;", 
            (tuple(result_ids),)
        )
        return cursor.fetchall()
    query = "find someone who studied at cathedral"
    result_ids, distances = search_profiles(query)
    print(result_ids)
    detailed_results = get_profiles_from_indices(result_ids)

    # Display results
    for result in detailed_results:
        print(result)

except (Exception, psycopg2.DatabaseError) as error:
    print("Error:", error)

finally:

    if cursor:
        cursor.close()
    if conn:
        conn.close()

