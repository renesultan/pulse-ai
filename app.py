import os
import logging
from flask import Flask, render_template, request, jsonify

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/org-chart')
def org_chart():
    # Get parameters from the query string
    company_name = request.args.get('company_name', '')
    department_name = request.args.get('department_name', '')
    org_structure = request.args.get('org_structure', '')
    reporting_line = request.args.get('reporting_line', '')
    
    return render_template(
        'org_chart.html',
        company_name=company_name,
        department_name=department_name,
        org_structure=org_structure,
        reporting_line=reporting_line
    )

@app.route('/api/parse-org-data', methods=['POST'])
def parse_org_data():
    data = request.json
    org_structure = data.get('org_structure', '')
    
    # Process the org structure and convert it to a hierarchical format
    hierarchy = parse_org_structure(org_structure)
    
    return jsonify(hierarchy)

def parse_org_structure(org_structure_text):
    """Parse the org structure text into a hierarchical JSON format for D3.js"""
    if not org_structure_text:
        return {}
    
    # Split the input text into lines
    lines = org_structure_text.strip().split('\n')
    
    # Dictionary to store all employees by name for quick lookup
    employees = {}
    
    # First pass: Create all employee nodes
    for line in lines:
        parts = [part.strip() for part in line.split(',')]
        if len(parts) >= 2:  # At least name and title
            name = parts[0]
            title = parts[1]
            
            employees[name] = {
                'name': name,
                'title': title,
                'children': []
            }
    
    # Second pass: Establish reporting relationships
    root_nodes = []
    for line in lines:
        parts = [part.strip() for part in line.split(',')]
        if len(parts) >= 2:  # At least name and title
            name = parts[0]
            
            # Check if reports to someone
            if len(parts) >= 3 and parts[2] in employees:
                reports_to = parts[2]
                employees[reports_to]['children'].append(employees[name])
            else:
                # This is a root node (no manager specified)
                root_nodes.append(employees[name])
    
    # Create the final hierarchy
    if len(root_nodes) == 1:
        # Single root node (CEO or similar)
        return root_nodes[0]
    else:
        # Multiple root nodes, create a virtual root
        return {
            'name': 'Organization',
            'title': '',
            'children': root_nodes
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
