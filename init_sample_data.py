"""
Initialize the database with sample enterprise matrix organization data.
This script will reset the database and create a pre-defined sample organization.
"""
import sys
import os
import json
from datetime import datetime, timedelta
import random

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import app, db
from models import (
    Organization, Region, Location, Department, Project, 
    Employee, OrgChart, project_members, secondary_reports
)

def reset_database():
    """Reset the database by dropping and recreating all tables"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Database reset complete")
        return True

def initialize_sample_data():
    """Create a sample enterprise organization with matrix structure"""
    with app.app_context():
        # Create the organization
        org = Organization(
            name="TechNova Global",
            description="A leading enterprise technology company specializing in cloud solutions, AI, and digital transformation.",
            industry="Technology",
            headquarters="San Francisco, CA"
        )
        db.session.add(org)
        db.session.flush()
        print(f"Created organization: {org.name}")
        
        # Create regions
        americas = Region(name="Americas", code="AM", organization_id=org.id)
        emea = Region(name="EMEA", code="EMEA", organization_id=org.id)
        apac = Region(name="APAC", code="APAC", organization_id=org.id)
        db.session.add_all([americas, emea, apac])
        db.session.flush()
        print("Created regions: Americas, EMEA, APAC")
        
        # Create some locations
        locations = [
            Location(name="San Francisco HQ", city="San Francisco", country="USA", 
                    timezone="GMT-8", is_headquarters=True, region_id=americas.id),
            Location(name="New York Office", city="New York", country="USA",
                    timezone="GMT-5", is_headquarters=False, region_id=americas.id),
            Location(name="London Office", city="London", country="UK",
                    timezone="GMT", is_headquarters=False, region_id=emea.id),
            Location(name="Singapore Office", city="Singapore", country="Singapore",
                    timezone="GMT+8", is_headquarters=False, region_id=apac.id)
        ]
        db.session.add_all(locations)
        db.session.flush()
        print("Created 4 office locations")
        
        # Create departments
        eng_dept = Department(name="Engineering", code="ENG", cost_center="CC-001", organization_id=org.id)
        product_dept = Department(name="Product", code="PROD", cost_center="CC-002", organization_id=org.id)
        marketing_dept = Department(name="Marketing", code="MKT", cost_center="CC-003", organization_id=org.id)
        sales_dept = Department(name="Sales", code="SALES", cost_center="CC-004", organization_id=org.id)
        exec_dept = Department(name="Executive Leadership", code="EXEC", cost_center="CC-000", organization_id=org.id)
        
        departments = [eng_dept, product_dept, marketing_dept, sales_dept, exec_dept]
        db.session.add_all(departments)
        db.session.flush()
        print("Created 5 departments")
        
        # Create sub-departments
        fe_dept = Department(name="Frontend Engineering", code="FE", cost_center="CC-001-1", 
                           organization_id=org.id, parent_id=eng_dept.id)
        be_dept = Department(name="Backend Engineering", code="BE", cost_center="CC-001-2", 
                           organization_id=org.id, parent_id=eng_dept.id)
        qa_dept = Department(name="Quality Assurance", code="QA", cost_center="CC-001-3", 
                           organization_id=org.id, parent_id=eng_dept.id)
        
        pm_dept = Department(name="Product Management", code="PM", cost_center="CC-002-1", 
                           organization_id=org.id, parent_id=product_dept.id)
        design_dept = Department(name="Product Design", code="PD", cost_center="CC-002-2", 
                               organization_id=org.id, parent_id=product_dept.id)
        
        sub_departments = [fe_dept, be_dept, qa_dept, pm_dept, design_dept]
        db.session.add_all(sub_departments)
        db.session.flush()
        print("Created 5 sub-departments")
        
        # Create projects for matrix organization
        project1 = Project(
            name="Cloud Platform Redesign",
            code="CPR-2025",
            description="Redesign our flagship cloud platform with improved UX and performance",
            status="Active",
            priority="High",
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=180)).date(),
            organization_id=org.id
        )
        
        project2 = Project(
            name="Mobile App Relaunch",
            code="MAR-2025",
            description="Rebuild our mobile app with cross-platform technology",
            status="Active",
            priority="High",
            start_date=datetime.now().date(),
            end_date=(datetime.now() + timedelta(days=90)).date(),
            organization_id=org.id
        )
        
        projects = [project1, project2]
        db.session.add_all(projects)
        db.session.flush()
        print("Created 2 cross-functional projects")
        
        # Create executives
        ceo = Employee(
            employee_id="E10001",
            name="Sarah Chen",
            title="Chief Executive Officer",
            email="schen@technova.example",
            level="Executive",
            organization_id=org.id,
            department_id=exec_dept.id,
            location_id=locations[0].id,
            cost_center=exec_dept.cost_center
        )
        db.session.add(ceo)
        db.session.flush()
        
        cto = Employee(
            employee_id="E10002",
            name="Alex Rodriguez",
            title="Chief Technology Officer",
            email="arodriguez@technova.example",
            level="Executive",
            organization_id=org.id,
            department_id=exec_dept.id,
            location_id=locations[0].id,
            cost_center=exec_dept.cost_center,
            primary_manager_id=ceo.id,
            reports_to_id=ceo.id
        )
        
        cpo = Employee(
            employee_id="E10003",
            name="Mira Patel",
            title="Chief Product Officer",
            email="mpatel@technova.example",
            level="Executive",
            organization_id=org.id,
            department_id=exec_dept.id,
            location_id=locations[0].id,
            cost_center=exec_dept.cost_center,
            primary_manager_id=ceo.id,
            reports_to_id=ceo.id
        )
        
        executives = [ceo, cto, cpo]
        db.session.add_all([cto, cpo])
        db.session.flush()
        print("Created executive team")
        
        # Create VPs
        vp_eng = Employee(
            employee_id="E20001",
            name="Kevin Zhang",
            title="VP Engineering",
            email="kzhang@technova.example",
            level="VP",
            organization_id=org.id,
            department_id=eng_dept.id,
            location_id=locations[0].id,
            cost_center=eng_dept.cost_center,
            primary_manager_id=cto.id,
            reports_to_id=cto.id
        )
        
        vp_product = Employee(
            employee_id="E20002",
            name="Samantha Lee",
            title="VP Product",
            email="slee@technova.example",
            level="VP",
            organization_id=org.id,
            department_id=product_dept.id,
            location_id=locations[0].id,
            cost_center=product_dept.cost_center,
            primary_manager_id=cpo.id,
            reports_to_id=cpo.id
        )
        
        vps = [vp_eng, vp_product]
        db.session.add_all(vps)
        db.session.flush()
        print("Created VP team")
        
        # Create directors and managers
        dir_fe = Employee(
            employee_id="E30001",
            name="Lisa Wong",
            title="Director, Frontend Engineering",
            level="Director",
            organization_id=org.id,
            department_id=fe_dept.id,
            location_id=locations[0].id,
            cost_center=fe_dept.cost_center,
            primary_manager_id=vp_eng.id,
            reports_to_id=vp_eng.id
        )
        
        dir_be = Employee(
            employee_id="E30002",
            name="John Smith",
            title="Director, Backend Engineering",
            level="Director",
            organization_id=org.id,
            department_id=be_dept.id,
            location_id=locations[0].id,
            cost_center=be_dept.cost_center,
            primary_manager_id=vp_eng.id,
            reports_to_id=vp_eng.id
        )
        
        dir_pm = Employee(
            employee_id="E30003",
            name="Daniel Okafor",
            title="Director, Product Management",
            level="Director",
            organization_id=org.id,
            department_id=pm_dept.id,
            location_id=locations[0].id,
            cost_center=pm_dept.cost_center,
            primary_manager_id=vp_product.id,
            reports_to_id=vp_product.id
        )
        
        directors = [dir_fe, dir_be, dir_pm]
        db.session.add_all(directors)
        db.session.flush()
        print("Created directors")
        
        # Create managers
        mgr_fe1 = Employee(
            employee_id="E40001",
            name="James Johnson",
            title="Engineering Manager, Frontend",
            level="Manager",
            organization_id=org.id,
            department_id=fe_dept.id,
            location_id=locations[0].id,
            cost_center=fe_dept.cost_center,
            primary_manager_id=dir_fe.id,
            reports_to_id=dir_fe.id
        )
        
        mgr_be1 = Employee(
            employee_id="E40002",
            name="Maria Garcia",
            title="Engineering Manager, Backend",
            level="Manager",
            organization_id=org.id,
            department_id=be_dept.id,
            location_id=locations[0].id,
            cost_center=be_dept.cost_center,
            primary_manager_id=dir_be.id,
            reports_to_id=dir_be.id
        )
        
        mgr_pm1 = Employee(
            employee_id="E40003",
            name="Priya Sharma",
            title="Product Manager",
            level="Manager",
            organization_id=org.id,
            department_id=pm_dept.id,
            location_id=locations[0].id,
            cost_center=pm_dept.cost_center,
            primary_manager_id=dir_pm.id,
            reports_to_id=dir_pm.id
        )
        
        managers = [mgr_fe1, mgr_be1, mgr_pm1]
        db.session.add_all(managers)
        db.session.flush()
        print("Created managers")
        
        # Create some employees
        fe_emp1 = Employee(
            employee_id="E50001",
            name="Michael Brown",
            title="Senior Frontend Engineer",
            level="Senior",
            organization_id=org.id,
            department_id=fe_dept.id,
            location_id=locations[0].id,
            cost_center=fe_dept.cost_center,
            primary_manager_id=mgr_fe1.id,
            reports_to_id=mgr_fe1.id
        )
        
        fe_emp2 = Employee(
            employee_id="E50002",
            name="Emma Wilson",
            title="Frontend Engineer",
            level="Individual Contributor",
            organization_id=org.id,
            department_id=fe_dept.id,
            location_id=locations[0].id,
            cost_center=fe_dept.cost_center,
            primary_manager_id=mgr_fe1.id,
            reports_to_id=mgr_fe1.id
        )
        
        be_emp1 = Employee(
            employee_id="E50003",
            name="David Kim",
            title="Senior Backend Engineer",
            level="Senior",
            organization_id=org.id,
            department_id=be_dept.id,
            location_id=locations[0].id,
            cost_center=be_dept.cost_center,
            primary_manager_id=mgr_be1.id,
            reports_to_id=mgr_be1.id
        )
        
        be_emp2 = Employee(
            employee_id="E50004",
            name="Fatima Zahra",
            title="Backend Engineer",
            level="Individual Contributor",
            organization_id=org.id,
            department_id=be_dept.id,
            location_id=locations[1].id,
            cost_center=be_dept.cost_center,
            primary_manager_id=mgr_be1.id,
            reports_to_id=mgr_be1.id
        )
        
        pm_emp1 = Employee(
            employee_id="E50005",
            name="Carlos Diaz",
            title="Associate Product Manager",
            level="Individual Contributor",
            organization_id=org.id,
            department_id=pm_dept.id,
            location_id=locations[0].id,
            cost_center=pm_dept.cost_center,
            primary_manager_id=mgr_pm1.id,
            reports_to_id=mgr_pm1.id
        )
        
        employees = [fe_emp1, fe_emp2, be_emp1, be_emp2, pm_emp1]
        db.session.add_all(employees)
        db.session.flush()
        print("Created individual contributors")
        
        # Create matrix relationships through projects
        # Project 1: Cloud Platform Redesign
        project1.sponsor_id = cto.id
        project1.members.append(mgr_pm1)  # Product Manager as project manager
        project1.members.append(fe_emp1)  # Frontend engineer
        project1.members.append(be_emp1)  # Backend engineer
        
        # Secondary reporting for project 1 (matrix structure)
        fe_emp1.secondary_managers.append(mgr_pm1)  # Frontend reports to PM in matrix
        be_emp1.secondary_managers.append(mgr_pm1)  # Backend reports to PM in matrix
        
        # Project 2: Mobile App Relaunch
        project2.sponsor_id = cpo.id
        project2.members.append(pm_emp1)  # Associate PM as project manager
        project2.members.append(fe_emp2)  # Frontend engineer
        project2.members.append(be_emp2)  # Backend engineer
        
        # Secondary reporting for project 2 (matrix structure)
        fe_emp2.secondary_managers.append(pm_emp1)  # Frontend reports to APM in matrix
        be_emp2.secondary_managers.append(pm_emp1)  # Backend reports to APM in matrix
        
        db.session.commit()
        print("Created matrix reporting relationships")
        
        # Create org charts
        # Hierarchical chart
        hierarchical_chart_data = {
            "name": ceo.name,
            "title": ceo.title,
            "children": [
                {
                    "name": cto.name,
                    "title": cto.title,
                    "children": [
                        {
                            "name": vp_eng.name,
                            "title": vp_eng.title,
                            "children": [
                                {
                                    "name": dir_fe.name,
                                    "title": dir_fe.title,
                                    "children": [
                                        {
                                            "name": mgr_fe1.name,
                                            "title": mgr_fe1.title,
                                            "children": [
                                                {
                                                    "name": fe_emp1.name,
                                                    "title": fe_emp1.title,
                                                    "children": []
                                                },
                                                {
                                                    "name": fe_emp2.name,
                                                    "title": fe_emp2.title,
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "name": dir_be.name,
                                    "title": dir_be.title,
                                    "children": [
                                        {
                                            "name": mgr_be1.name,
                                            "title": mgr_be1.title,
                                            "children": [
                                                {
                                                    "name": be_emp1.name,
                                                    "title": be_emp1.title,
                                                    "children": []
                                                },
                                                {
                                                    "name": be_emp2.name,
                                                    "title": be_emp2.title,
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    "name": cpo.name,
                    "title": cpo.title,
                    "children": [
                        {
                            "name": vp_product.name,
                            "title": vp_product.title,
                            "children": [
                                {
                                    "name": dir_pm.name,
                                    "title": dir_pm.title,
                                    "children": [
                                        {
                                            "name": mgr_pm1.name,
                                            "title": mgr_pm1.title,
                                            "children": [
                                                {
                                                    "name": pm_emp1.name,
                                                    "title": pm_emp1.title,
                                                    "children": []
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        # Matrix org chart (includes dotted line/secondary reporting)
        matrix_chart_data = {
            "name": ceo.name,
            "title": ceo.title,
            "children": hierarchical_chart_data["children"],
            "dotted_line_reports": []
        }
        
        # Project chart
        project_chart_data = {
            "name": project1.name,
            "description": project1.description,
            "sponsor": {
                "name": cto.name,
                "title": cto.title
            },
            "departments": [
                {
                    "name": "Product Management",
                    "members": [
                        {
                            "name": mgr_pm1.name,
                            "title": mgr_pm1.title,
                            "role": "Project Manager"
                        }
                    ]
                },
                {
                    "name": "Frontend Engineering",
                    "members": [
                        {
                            "name": fe_emp1.name,
                            "title": fe_emp1.title
                        }
                    ]
                },
                {
                    "name": "Backend Engineering",
                    "members": [
                        {
                            "name": be_emp1.name,
                            "title": be_emp1.title
                        }
                    ]
                }
            ]
        }
        
        hierarchy_chart = OrgChart(
            name="TechNova Hierarchical Structure",
            description="Traditional reporting structure by department",
            organization_id=org.id,
            view_type="hierarchical",
            chart_data=json.dumps(hierarchical_chart_data)
        )
        
        matrix_chart = OrgChart(
            name="TechNova Matrix Structure",
            description="Cross-functional project teams with dual reporting lines",
            organization_id=org.id,
            view_type="matrix",
            chart_data=json.dumps(matrix_chart_data)
        )
        
        project_chart = OrgChart(
            name="Cloud Platform Redesign Team",
            description="Cross-functional team for Cloud Platform Redesign",
            organization_id=org.id,
            project_id=project1.id,
            view_type="project",
            chart_data=json.dumps(project_chart_data)
        )
        
        db.session.add_all([hierarchy_chart, matrix_chart, project_chart])
        db.session.commit()
        print("Created org charts (hierarchical, matrix, and project)")
        
        print("\nSample data initialization complete!")
        print("Organization: TechNova Global")
        print("Employees: 15 (CEO, CxOs, VPs, Directors, Managers, and ICs)")
        print("Departments: 5 main departments with 5 sub-departments")
        print("Projects: 2 cross-functional projects with matrix reporting")
        print("Charts: 3 different visualization types (hierarchical, matrix, project)")
        return True

if __name__ == "__main__":
    print("Resetting database and initializing sample data...")
    reset_database()
    initialize_sample_data()
    print("Done!")