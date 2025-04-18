import os
import logging
import json
import traceback
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the database base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///fmeetings.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Import models after db is defined
with app.app_context():
    from models import (
        Organization, Department, Employee, OrgChart,
        Region, Location, Project, project_members, secondary_reports
    )
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-enterprise-example')
def get_enterprise_example():
    """Get enterprise example data for populating the form"""
    try:
        # Get the first organization (TechNova Global from our sample data)
        org = Organization.query.first()
        
        if not org:
            return jsonify({"error": "No sample organization found"}), 404
        
        # Get the CEO (first executive)
        ceo = Employee.query.filter_by(organization_id=org.id, primary_manager_id=None).first()
        
        if not ceo:
            return jsonify({"error": "No CEO found in sample data"}), 404
            
        # Fetch all employees to build the org structure text
        employees = Employee.query.filter_by(organization_id=org.id).all()
        
        # Build organization structure text in the format: Name, Title, Reports To
        org_structure_lines = []
        for emp in employees:
            # The CEO doesn't report to anyone
            if emp.id == ceo.id:
                org_structure_lines.append(f"{emp.name}, {emp.title}")
            else:
                # Get the primary manager's name
                manager = None
                if emp.primary_manager_id:
                    manager = Employee.query.get(emp.primary_manager_id)
                elif emp.reports_to_id:  # Fallback to reports_to for backward compatibility
                    manager = Employee.query.get(emp.reports_to_id)
                    
                if manager:
                    org_structure_lines.append(f"{emp.name}, {emp.title}, {manager.name}")
                else:
                    org_structure_lines.append(f"{emp.name}, {emp.title}")
        
        # Create the response data
        response_data = {
            "companyName": org.name,
            "departmentName": "Executive Leadership",  # Default to executive department for the overview
            "orgStructure": "\n".join(org_structure_lines),
            "reportingLine": "matrix"  # Using matrix as our example showcases matrix organization
        }
        
        return jsonify(response_data)
    except Exception as e:
        logging.error(f"Error fetching enterprise example data: {str(e)}")
        return jsonify({"error": "Failed to fetch enterprise example data"}), 500

@app.route('/org-chart', methods=['GET', 'POST'])
def org_chart():
    # Check if we're viewing an existing chart by ID (GET request)
    if request.method == 'GET':
        chart_id = request.args.get('id')
        
        if chart_id:
            try:
                # Get the org chart from the database
                chart = OrgChart.query.get(chart_id)
                
                if not chart:
                    # If chart not found, redirect to home
                    logging.error(f"Org chart with ID {chart_id} not found")
                    return redirect('/')
                
                # Get the chart data
                chart_data = None
                if chart.chart_data:
                    chart_data = json.loads(chart.chart_data)
                elif chart.reporting_structure:
                    # For backward compatibility
                    chart_data = json.loads(chart.reporting_structure)
                    
                # Set up template variables
                return render_template(
                    'org_chart.html',
                    company_name=chart.organization.name,
                    department_name=chart.department.name if chart.department else '',
                    chart_data=json.dumps(chart_data),
                    reporting_line=chart.reporting_line_type or chart.view_type or 'hierarchical',
                    chart_id=chart.id,
                    chart_title=chart.name,
                    view_type=chart.view_type
                )
            except Exception as e:
                logging.error(f"Error loading org chart: {e}")
                return redirect('/')
        
        # Regular GET parameters for new charts (backward compatibility)
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
    
    # Handle POST request from the form submission
    elif request.method == 'POST':
        # Get form data
        company_name = request.form.get('company_name', '')
        department_name = request.form.get('department_name', '')
        org_structure = request.form.get('org_structure', '')
        reporting_line = request.form.get('reporting_line', '')
        
        logging.info(f"POST to /org-chart received with company={company_name}, dept={department_name}")
        logging.info(f"Organization structure length: {len(org_structure or '')}")
        
        # Validate required fields
        if not company_name or not org_structure:
            logging.error("Missing required fields in POST data")
            # If validation fails, redirect back to the form
            return redirect('/')
        
        try:
            # Process the org structure and convert it to a hierarchical format
            logging.info("Processing organization structure...")
            hierarchy = parse_org_structure(org_structure)
            
            logging.info(f"Successfully created hierarchy with {len(hierarchy.get('children', []))} top-level nodes")
            
            # Render the direct chart template with the processed data
            # This template has the D3 code directly embedded to avoid JSON parsing issues
            logging.info("Rendering direct_chart.html template with processed data")
            
            # Debug the hierarchy data
            logging.info(f"Chart data type: {type(hierarchy)}")
            logging.info(f"Chart data structure: {hierarchy.keys() if isinstance(hierarchy, dict) else 'Not a dict'}")
            logging.info(f"Children count: {len(hierarchy.get('children', [])) if isinstance(hierarchy, dict) else 'No children'}")
            
            # Enhanced debugging of first level
            if isinstance(hierarchy, dict) and 'children' in hierarchy:
                for i, child in enumerate(hierarchy.get('children', [])[:5]):  # Show first 5 children
                    logging.info(f"Child {i}: {child.get('name', 'No name')} - {child.get('title', 'No title')}")
            
            # Dump the JSON with indentation for easier debugging
            chart_data_json = json.dumps(hierarchy, indent=2)
            logging.info(f"First 500 chars of JSON data: {chart_data_json[:500]}...")
            
            return render_template(
                'direct_chart.html',
                company_name=company_name,
                department_name=department_name,
                reporting_line=reporting_line,
                chart_data=chart_data_json  # Pass the processed hierarchical data with nice formatting
            )
        except Exception as e:
            logging.error(f"Error processing org chart data: {e}")
            import traceback
            logging.error(traceback.format_exc())
            
            # If processing fails, redirect back to the form with error indication
            return redirect('/?error=chart_creation_failed')

@app.route('/api/parse-org-data', methods=['POST'])
def parse_org_data():
    data = request.json
    org_structure = data.get('org_structure', '')
    
    # Process the org structure and convert it to a hierarchical format
    hierarchy = parse_org_structure(org_structure)
    
    # Save the org chart data to the database (optional based on form submission)
    company_name = data.get('company_name')
    department_name = data.get('department_name')
    reporting_line = data.get('reporting_line')
    
    if company_name and 'save_to_db' in data and data['save_to_db']:
        save_org_chart_to_db(company_name, department_name, org_structure, reporting_line, hierarchy)
    
    return jsonify(hierarchy)

def save_org_chart_to_db(company_name, department_name, org_structure, reporting_line, hierarchy):
    """Save the organization chart data to the database"""
    try:
        # Check if the organization already exists
        organization = Organization.query.filter_by(name=company_name).first()
        
        if not organization:
            # Create a new organization
            organization = Organization(name=company_name)
            db.session.add(organization)
            db.session.flush()  # Get the ID without committing
        
        # Handle department if provided
        department = None
        if department_name:
            department = Department.query.filter_by(
                name=department_name, 
                organization_id=organization.id
            ).first()
            
            if not department:
                department = Department(
                    name=department_name,
                    organization_id=organization.id
                )
                db.session.add(department)
                db.session.flush()
        
        # Create the org chart entry
        org_chart = OrgChart(
            name=f"{company_name} Org Chart",
            organization_id=organization.id,
            department_id=department.id if department else None,
            reporting_structure=json.dumps(hierarchy),
            reporting_line_type=reporting_line
        )
        db.session.add(org_chart)
        
        # Parse and save employees
        save_employees(org_structure, organization.id, department.id if department else None)
        
        # Commit all changes
        db.session.commit()
        return True
    except Exception as e:
        logging.error(f"Error saving org chart: {e}")
        db.session.rollback()
        return False

def save_employees(org_structure_text, organization_id, department_id=None):
    """Parse and save employees from the org structure text"""
    if not org_structure_text:
        return
    
    # Split the input text into lines
    lines = org_structure_text.strip().split('\n')
    
    # Dictionary to store employees by name for quick lookup
    employee_map = {}
    
    # First pass: Create all employee records
    for line in lines:
        parts = [part.strip() for part in line.split(',')]
        if len(parts) >= 2:  # At least name and title
            name = parts[0]
            title = parts[1]
            
            # Check if employee already exists
            employee = Employee.query.filter_by(
                name=name, 
                organization_id=organization_id
            ).first()
            
            if not employee:
                employee = Employee(
                    name=name,
                    title=title,
                    organization_id=organization_id,
                    department_id=department_id
                )
                db.session.add(employee)
                db.session.flush()  # Get the ID without committing
            
            employee_map[name] = employee
    
    # Second pass: Establish reporting relationships
    for line in lines:
        parts = [part.strip() for part in line.split(',')]
        if len(parts) >= 3 and parts[2] in employee_map:  # Has a manager
            employee = employee_map[parts[0]]
            manager = employee_map[parts[2]]
            
            # Set the reports_to relationship
            employee.reports_to_id = manager.id

def parse_org_structure(org_structure_text):
    """Parse the org structure text into a hierarchical JSON format for D3.js"""
    if not org_structure_text:
        logging.warning("Empty org structure text provided")
        return {}
    
    # Split the input text into lines
    lines = org_structure_text.strip().split('\n')
    logging.info(f"Processing {len(lines)} lines of org structure")
    
    # Dictionary to store all employees by name for quick lookup
    employees = {}
    
    # First pass: Create all employee nodes
    for i, line in enumerate(lines[:5]):  # Debug first 5 lines
        logging.debug(f"Processing line {i}: {line}")
    
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
    
    logging.info(f"Created {len(employees)} employee nodes")
    
    # Second pass: Establish reporting relationships
    root_nodes = []
    child_count = 0
    
    for line in lines:
        parts = [part.strip() for part in line.split(',')]
        if len(parts) >= 2:  # At least name and title
            name = parts[0]
            
            # Check if reports to someone
            if len(parts) >= 3 and parts[2] in employees:
                reports_to = parts[2]
                employees[reports_to]['children'].append(employees[name])
                child_count += 1
            else:
                # This is a root node (no manager specified)
                root_nodes.append(employees[name])
    
    logging.info(f"Found {len(root_nodes)} root nodes and {child_count} reporting relationships")
    
    # Create the final hierarchy
    result = None
    if len(root_nodes) == 1:
        # Single root node (CEO or similar)
        logging.info(f"Using single root node: {root_nodes[0]['name']}")
        result = root_nodes[0]
    else:
        # Multiple root nodes, create a virtual root
        logging.info(f"Creating virtual root node for {len(root_nodes)} root nodes")
        result = {
            'name': 'Organization',
            'title': '',
            'children': root_nodes
        }
    
    # Debug the result
    if result and isinstance(result, dict):
        child_count = len(result.get('children', []))
        logging.info(f"Final hierarchy has {child_count} top-level children")
        
        if child_count > 0:
            first_child = result['children'][0]
            logging.info(f"First child: {first_child.get('name', 'No name')} - {first_child.get('title', 'No title')}")
            
            grandchild_count = len(first_child.get('children', []))
            logging.info(f"First child has {grandchild_count} children of its own")
    
    return result

@app.route('/api/charts', methods=['GET'])
def get_org_charts():
    """Get a list of saved organization charts"""
    try:
        org_charts = OrgChart.query.order_by(OrgChart.created_at.desc()).all()
        result = []
        
        for chart in org_charts:
            result.append({
                'id': chart.id,
                'name': chart.name,
                'organization': chart.organization.name,
                'department': chart.department.name if chart.department else None,
                'reporting_line_type': chart.reporting_line_type,
                'created_at': chart.created_at.isoformat()
            })
        
        return jsonify(result)
    except Exception as e:
        logging.error(f"Error retrieving org charts: {e}")
        return jsonify({'error': 'Failed to retrieve organization charts'}), 500

@app.route('/api/charts/<int:chart_id>', methods=['GET'])
def get_org_chart(chart_id):
    """Get a specific organization chart by ID"""
    try:
        chart = OrgChart.query.get(chart_id)
        
        if not chart:
            return jsonify({'error': 'Organization chart not found'}), 404
        
        return jsonify({
            'id': chart.id,
            'name': chart.name,
            'organization': chart.organization.name,
            'department': chart.department.name if chart.department else None,
            'reporting_line_type': chart.reporting_line_type,
            'hierarchy': json.loads(chart.reporting_structure),
            'created_at': chart.created_at.isoformat()
        })
    except Exception as e:
        logging.error(f"Error retrieving org chart {chart_id}: {e}")
        return jsonify({'error': 'Failed to retrieve organization chart'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
