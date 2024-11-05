import psycopg2

DB_NAME = "alumni"
DB_USER = "satvik"
DB_PASSWORD = "12345"
DB_HOST = "localhost"  
DB_PORT = "5432"

try:
    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS FaissMapping (
        FaissID SERIAL PRIMARY KEY,
        AlumniID INT REFERENCES AlumniProfiles(AlumniID) ON DELETE CASCADE,
        Vector BYTEA
    );
    '''


    cursor.execute(create_table_query)
    conn.commit() 

    print("Table 'FaissMapping' created successfully")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while creating table:", error)

finally:
    # Close the cursor and connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
