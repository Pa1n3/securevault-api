import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    """Get a raw database connection."""
    return psycopg2.connect(DATABASE_URL)


def execute_query(query: str, params: tuple = None, fetch: str = None):
    """
    Universal query executor.
    fetch = 'one' | 'all' | None (for INSERT/UPDATE/DELETE)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(query, params)
        
        if fetch == 'one':
            result = cur.fetchone()
        elif fetch == 'all':
            result = cur.fetchall()
        else:
            result = None
        
        conn.commit()
        return result
    
    except Exception as e:
        conn.rollback()
        raise e
    
    finally:
        cur.close()
        conn.close()