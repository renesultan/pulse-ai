#!/bin/bash
# Script to complete the project reorganization by removing original files
# This script should be run after reorganize_project.sh

set -e  # Exit on error

echo "Completing project reorganization by removing original files..."

# Function to safely remove a file or directory
# Only removes if it exists in the new location
safe_remove() {
  local original_path=$1
  local new_path=$2
  
  if [ -e "$new_path" ]; then
    echo "Removing original: $original_path"
    rm -rf "$original_path"
  else
    echo "WARNING: Not removing $original_path because $new_path doesn't exist"
  fi
}

# Remove original Python files that have been moved
safe_remove "./generate_org_data.py" "./src/scripts/generate_org_data.py"
safe_remove "./test_migration.py" "./src/scripts/test_migration.py"
safe_remove "./analyze_org_data.ipynb" "./src/notebooks/analyze_org_data.ipynb"
safe_remove "./validate_database.ipynb" "./src/notebooks/validate_database.ipynb"

# Remove original directories that have been moved
safe_remove "./db" "./src/db"
safe_remove "./migrations" "./src/migrations"

# Move specifications to docs folder if not already there
if [ -f "./design_specification.md" ] && [ -f "./docs/specifications/design_specification.md" ]; then
  rm "./design_specification.md"
fi

if [ -f "./organization_report.md" ] && [ -f "./docs/specifications/organization_report.md" ]; then
  rm "./organization_report.md"
fi

if [ -f "./ALEMBIC_INTEGRATION.md" ] && [ -f "./docs/specifications/ALEMBIC_INTEGRATION.md" ]; then
  rm "./ALEMBIC_INTEGRATION.md"
fi

echo "Project reorganization completed!"
echo 
echo "Next steps:"
echo "1. Run 'git status' to verify changes"
echo "2. Commit the reorganized project structure"