#!/usr/bin/env python3
"""
Migration script to add the 'resolved' column to the Conversations table.
This script should be run once to update the existing database schema.
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def migrate_add_resolved_column():
    """Add the resolved column to the Conversations table"""
    password = os.getenv("DB_PASSWORD")
    
    if not password:
        print("Error: DB_PASSWORD environment variable not set")
        return
    
    engine = create_engine(
        f"postgresql+psycopg2://postgres:{password}@127.0.0.1:5432/testing_tutor"
    )
    
    try:
        with engine.connect() as connection:
            # Check if the column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'Conversations' 
                AND column_name = 'resolved'
            """)
            
            result = connection.execute(check_query)
            if result.fetchone():
                print("Column 'resolved' already exists in Conversations table")
                return
            
            # Add the resolved column
            alter_query = text("""
                ALTER TABLE "Conversations" 
                ADD COLUMN resolved BOOLEAN NOT NULL DEFAULT FALSE
            """)
            
            connection.execute(alter_query)
            connection.commit()
            print("Successfully added 'resolved' column to Conversations table")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        raise

if __name__ == "__main__":
    migrate_add_resolved_column() 