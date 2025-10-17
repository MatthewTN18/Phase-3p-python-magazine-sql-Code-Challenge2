import psycopg2
import os

def get_connection():
   
    try:
        
        conn = psycopg2.connect(
            dbname="magazine_db",
            user="tt", 
            password="mypassword",  
            host="172.22.135.239",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        raise

def create_tables():
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Create authors table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE
            )
        ''')
        
        # Create magazines table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS magazines (
                id SERIAL PRIMARY KEY,
                name VARCHAR NOT NULL,
                category VARCHAR NOT NULL
            )
        ''')
        
        # Create articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                title VARCHAR NOT NULL,
                author_id INTEGER NOT NULL,
                magazine_id INTEGER NOT NULL,
                FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE,
                FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        print("Tables created successfully!")
        
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

def drop_tables():
    #drop tables
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DROP TABLE IF EXISTS articles CASCADE")
        cursor.execute("DROP TABLE IF EXISTS authors CASCADE") 
        cursor.execute("DROP TABLE IF EXISTS magazines CASCADE")
        conn.commit()
        print("Tables dropped successfully!")
    except psycopg2.Error as e:
        print(f"Error dropping tables: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


create_tables()