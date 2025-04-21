# Database Component for Pulse AI

This directory contains database models and utilities for the Pulse AI organization alignment platform.

## Overview

The database component provides:

1. SQLAlchemy models that define the schema for the organization alignment data
2. Import utilities to load the synthetic CSV data into the SQLite database
3. Query examples for accessing and analyzing the organizational data

## Files

- `models.py` - SQLAlchemy models defining the database schema
- `import_data.py` - Script to import CSV data into the database
- `query_data.py` - Examples of database queries

## Database Schema

The database includes tables for:

- Organizations
- Departments
- Positions
- Employees
- Teams
- Team Members
- Company OKRs
- Department OKRs
- Team OKRs
- Key Results
- OKR Updates
- Cross-Team Dependencies
- Status Updates
- Resource Allocations

## Usage

### Setting Up the Database

1. Make sure you have activated the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Import data from CSV files:
   ```
   python db/import_data.py
   ```
   This will create a SQLite database file `organization.db` in the project root.

### Running Query Examples

To see examples of database queries:
```
python db/query_data.py
```

### Using the Database in Your Code

```python
from db.models import get_engine, Employee, Department
from sqlalchemy.orm import sessionmaker

# Create a database session
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# Query example
employees = session.query(Employee).filter_by(department_id=1).all()
for employee in employees:
    print(f"{employee.first_name} {employee.last_name}")

# Close the session
session.close()
```