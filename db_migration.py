import os
import sys
from app import app, db

def migrate_database():
    """
    Migrate the database to match the current models.
    WARNING: This will drop and recreate all tables. All data will be lost.
    """
    print("WARNING: This will drop and recreate all database tables.")
    print("All existing data will be lost.")
    
    confirmation = input("Type 'YES' to confirm: ")
    if confirmation != "YES":
        print("Migration cancelled.")
        return
    
    print("Dropping all tables...")
    with app.app_context():
        db.drop_all()
    
    print("Creating all tables with updated schema...")
    with app.app_context():
        db.create_all()
    
    print("Database migration complete. All tables have been recreated with the updated schema.")

if __name__ == "__main__":
    migrate_database()