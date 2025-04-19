#!/bin/bash
# Script to set up a virtual environment for the organizational alignment data analysis project

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Create a Jupyter kernel for this environment
python -m ipykernel install --user --name=org-alignment-env --display-name="Python (Org Alignment)"

echo "Virtual environment setup complete!"
echo "To activate the environment, run: source venv/bin/activate"
echo "To start Jupyter Notebook, run: jupyter notebook"
echo "Make sure to select the 'Python (Org Alignment)' kernel when working with notebooks."
