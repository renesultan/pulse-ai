"""
Reset and reinitialize the database with the current schema.
This module provides functions to drop and recreate all database tables
to ensure the schema matches the current models.
"""
import traceback
import time
import logging
from app import app, db

def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    WARNING: This will result in data loss.
    
    Returns:
        bool: True if successful, False otherwise
    """
    max_attempts = 3
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        try:
            with app.app_context():
                logging.info(f"Attempt {attempt}/{max_attempts}: Dropping all tables...")
                # First, drop all tables
                db.session.close()  # Close any existing sessions
                db.session.remove()  # Remove all sessions
                db.drop_all()
                
                logging.info("Creating all tables with updated schema...")
                # Then create all tables
                db.create_all()
                
                logging.info("Database reset complete. All tables have been recreated.")
                return True
        except Exception as e:
            error_msg = str(e)
            tb = traceback.format_exc()
            logging.error(f"Error resetting database (attempt {attempt}/{max_attempts}): {error_msg}")
            logging.error(f"Traceback: {tb}")
            
            if attempt < max_attempts:
                logging.info(f"Retrying in 2 seconds...")
                time.sleep(2)  # Wait before retrying
            else:
                logging.error("Maximum retry attempts reached. Database reset failed.")
                return False

if __name__ == "__main__":
    reset_database()