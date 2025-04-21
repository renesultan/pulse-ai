#!/bin/bash
# Project Reorganization Script for Pulse AI
#
# This script reorganizes the project structure to be more modular and organized.
# It moves files to appropriate directories while maintaining project integrity.

set -e  # Exit on error

# Create required directories if they don't exist
mkdir -p src/api
mkdir -p src/db
mkdir -p src/utils
mkdir -p src/scripts
mkdir -p src/migrations
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/api
mkdir -p tests/db
mkdir -p docs/specifications

echo "Created directory structure"

# Move database files
echo "Moving database files..."
cp -r db/* src/db/

# Move migration files
echo "Moving migration files..."
cp -r migrations/* src/migrations/

# Move scripts
echo "Moving scripts..."
cp generate_org_data.py src/scripts/
cp test_migration.py src/scripts/

# Move specifications
echo "Moving specification files..."
cp design_specification.md docs/specifications/
cp organization_report.md docs/specifications/
cp ALEMBIC_INTEGRATION.md docs/specifications/

# Copy notebooks to appropriate locations
echo "Moving notebooks..."
mkdir -p src/notebooks
cp analyze_org_data.ipynb src/notebooks/
cp validate_database.ipynb src/notebooks/

# Update the main README
echo "Updating README..."
mv README.md.new README.md

echo "Project reorganization completed successfully!"
echo 
echo "Next steps:"
echo "1. Update import paths in Python files"
echo "2. Test the reorganized structure"
echo "3. Commit the changes"