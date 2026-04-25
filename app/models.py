from app.database import execute_query


def create_tables():
    """Create all tables if they don't exist."""
    
    # Users table
    execute_query("""
        CREATE TABLE IF NOT EXISTS users (
            id          SERIAL PRIMARY KEY,
            username    VARCHAR(50) UNIQUE NOT NULL,
            email       VARCHAR(100) UNIQUE NOT NULL,
            password    VARCHAR(255) NOT NULL,
            role        VARCHAR(20) DEFAULT 'user',  -- 'user' | 'admin'
            api_key     VARCHAR(64) UNIQUE,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Notes table
    execute_query("""
        CREATE TABLE IF NOT EXISTS notes (
            id          SERIAL PRIMARY KEY,
            user_id     INTEGER REFERENCES users(id) ON DELETE CASCADE,
            title       VARCHAR(200) NOT NULL,
            content     TEXT,
            is_private  BOOLEAN DEFAULT TRUE,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    # Files table
    execute_query("""
        CREATE TABLE IF NOT EXISTS files (
            id          SERIAL PRIMARY KEY,
            user_id     INTEGER REFERENCES users(id) ON DELETE CASCADE,
            filename    VARCHAR(255) NOT NULL,
            filepath    VARCHAR(500) NOT NULL,
            filesize    INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    execute_query("""
        CREATE TABLE IF NOT EXISTS password_resets (
            id           SERIAL PRIMARY KEY,
            user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            token        VARCHAR(128) NOT NULL,
            expires_at   TIMESTAMP WITH TIME ZONE NOT NULL,
            used         BOOLEAN DEFAULT FALSE,
            created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    """)
    
    print("✅ Tables created successfully")