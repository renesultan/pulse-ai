# Data Directory

This directory contains database files and other data assets for the Pulse AI project.

## Contents

- `organization.db` - SQLite database containing the organizational data
- Other data assets used by the application

## Usage

The SQLite database can be accessed directly using SQL tools, or through SQLAlchemy 
models defined in the `src/db/models.py` file.

For development purposes, this database is included in version control to provide 
a consistent starting point. In production, this would be replaced with a PostgreSQL 
database or other enterprise-grade solution.