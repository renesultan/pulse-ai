"""
Reset and reinitialize the database with the current schema.
This module provides functions to drop and recreate all database tables
to ensure the schema matches the current models.
"""
from app import app, db

def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    WARNING: This will result in data loss.
    """
    try:
        with app.app_context():
            print("Dropping all tables...")
            db.drop_all()
            
            print("Creating all tables with updated schema...")
            db.create_all()
            
            print("Database reset complete. All tables have been recreated.")
            return True
    except Exception as e:
        print(f"Error resetting database: {e}")
        return False

if __name__ == "__main__":
    reset_database()