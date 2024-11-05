import psycopg2

DB_NAME = "alumni"
DB_USER = "satvik"
DB_PASSWORD = "12345"
DB_HOST = "localhost"  
DB_PORT = "5432"

try:
    
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS AlumniProfiles (
        AlumniID SERIAL PRIMARY KEY,
        FullName VARCHAR(100) NOT NULL,
        CurrentRole VARCHAR(100),
        Company VARCHAR(100),
        University VARCHAR(100),
        HighSchool VARCHAR(100),
        LinkedInURL VARCHAR(255),
        DateUpdated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    '''

    cursor.execute(create_table_query)
    conn.commit() 

    print("Table 'alumni_table' created successfully")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while creating table:", error)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
