#!/usr/bin/env python3
"""
Synthetic Data Generator for Organizational Alignment Platform

This script generates a comprehensive synthetic dataset for Horizon Technologies,
a fictional mid-sized technology company with ~500 employees. The dataset includes
organizational structure, OKRs, and alignment data.

The data is written to CSV files in the 'synthetic_data' directory.
"""

import os
import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import uuid
import csv
from typing import Dict, List, Tuple, Any, Optional

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Initialize Faker
fake = Faker()
Faker.seed(42)

# Constants
COMPANY_NAME = "Horizon Technologies"
COMPANY_DOMAIN = "horizontech.com"
CURRENT_DATE = datetime(2025, 4, 19)  # Using the current date from the metadata
OUTPUT_DIR = "synthetic_data"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Configuration
NUM_EMPLOYEES = 500
TIMEFRAMES = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "FY 2025"]
CURRENT_TIMEFRAME = "Q2 2025"
STATUS_OPTIONS = ["On Track", "At Risk", "Behind"]
PRIORITY_OPTIONS = ["High", "Medium", "Low"]
DEPENDENCY_STATUS = ["Not Started", "In Progress", "Completed", "Blocked"]
EMPLOYMENT_STATUS = ["Active", "Leave", "Terminated"]
CONFIDENCE_SCORES = list(range(1, 11))  # 1-10

# Department distribution (percentage of employees)
DEPARTMENT_DISTRIBUTION = {
    "Engineering": 0.33,
    "Product Management": 0.09,
    "Sales & Marketing": 0.18,
    "Customer Success": 0.14,
    "Finance & Accounting": 0.06,
    "Human Resources": 0.05,
    "Operations": 0.09,
    "Research & Development": 0.11
}

# Location distribution
LOCATIONS = ["San Francisco, CA", "New York, NY", "Austin, TX", "Remote", "Boston, MA", "Seattle, WA"]
LOCATION_WEIGHTS = [0.3, 0.2, 0.15, 0.2, 0.1, 0.05]

# Hierarchy levels with salary ranges (in thousands)
HIERARCHY_LEVELS = {
    "C-Suite": {"min": 250, "max": 500},
    "VP": {"min": 180, "max": 300},
    "Senior Director": {"min": 150, "max": 250},
    "Director": {"min": 130, "max": 200},
    "Senior Manager": {"min": 110, "max": 170},
    "Manager": {"min": 90, "max": 140},
    "Team Lead": {"min": 80, "max": 120},
    "Senior": {"min": 70, "max": 110},
    "Mid-level": {"min": 55, "max": 85},
    "Junior": {"min": 40, "max": 65}
}

# Helper functions
def save_to_csv(data: List[Dict], filename: str) -> None:
    """Save data to a CSV file in the output directory."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if data and len(data) > 0:
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False)
        print(f"Saved {len(data)} records to {filepath}")
    else:
        print(f"Warning: No data to save to {filepath}")

def generate_random_date(start_date: datetime, end_date: datetime) -> datetime:
    """Generate a random date between start_date and end_date."""
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

def weighted_choice(options: List[Any], weights: Optional[List[float]] = None) -> Any:
    """Make a weighted random choice from a list of options."""
    if weights is None:
        return random.choice(options)
    return random.choices(options, weights=weights, k=1)[0]

def generate_email(first_name: str, last_name: str, domain: str = COMPANY_DOMAIN) -> str:
    """Generate an email address from first and last name."""
    return f"{first_name.lower()}.{last_name.lower()}@{domain}"

def generate_salary(level: str) -> int:
    """Generate a realistic salary based on hierarchy level."""
    level_data = HIERARCHY_LEVELS.get(level, HIERARCHY_LEVELS["Mid-level"])
    min_salary = level_data["min"] * 1000
    max_salary = level_data["max"] * 1000
    # Add some randomness but keep within range
    return int(np.random.normal((min_salary + max_salary) / 2, (max_salary - min_salary) / 6))

# Department generation
def generate_departments() -> List[Dict]:
    """Generate department data."""
    departments = []
    
    # Define the main departments
    main_dept_names = list(DEPARTMENT_DISTRIBUTION.keys())
    
    # Create department IDs and basic info
    for i, dept_name in enumerate(main_dept_names, 1):
        cost_center = f"CC-{i:03d}"
        location = weighted_choice(LOCATIONS, LOCATION_WEIGHTS)
        
        departments.append({
            "department_id": i,
            "department_name": dept_name,
            "department_head_id": None,  # Will be filled later
            "parent_department_id": None,  # Top-level departments
            "cost_center_code": cost_center,
            "location": location
        })
    
    # Add sub-departments
    sub_dept_id = len(departments) + 1
    
    # Engineering sub-departments
    eng_dept_id = 1  # Engineering is the first department
    eng_subdepts = ["Frontend", "Backend", "DevOps", "QA", "Mobile"]
    
    for sub_name in eng_subdepts:
        departments.append({
            "department_id": sub_dept_id,
            "department_name": f"{sub_name} Engineering",
            "department_head_id": None,  # Will be filled later
            "parent_department_id": eng_dept_id,
            "cost_center_code": f"CC-{eng_dept_id:03d}-{sub_dept_id-len(departments):02d}",
            "location": departments[eng_dept_id-1]["location"]  # Same as parent
        })
        sub_dept_id += 1
    
    # Sales & Marketing sub-departments
    sales_dept_id = 3  # Sales & Marketing is the third department
    sales_subdepts = ["Sales", "Marketing", "Business Development"]
    
    for sub_name in sales_subdepts:
        departments.append({
            "department_id": sub_dept_id,
            "department_name": sub_name,
            "department_head_id": None,  # Will be filled later
            "parent_department_id": sales_dept_id,
            "cost_center_code": f"CC-{sales_dept_id:03d}-{sub_dept_id-len(departments):02d}",
            "location": departments[sales_dept_id-1]["location"]  # Same as parent
        })
        sub_dept_id += 1
    
    return departments

# Position generation
def generate_positions(departments: List[Dict]) -> List[Dict]:
    """Generate job positions data."""
    positions = []
    position_id = 1
    
    # C-Suite positions
    c_suite_titles = ["CEO", "CTO", "CFO", "COO", "CHRO", "CMO"]
    for title in c_suite_titles:
        positions.append({
            "position_id": position_id,
            "title": title,
            "department_id": None,  # C-Suite spans all departments
            "level": "C-Suite",
            "salary_band_minimum": HIERARCHY_LEVELS["C-Suite"]["min"] * 1000,
            "salary_band_maximum": HIERARCHY_LEVELS["C-Suite"]["max"] * 1000
        })
        position_id += 1
    
    # Department-specific positions
    for dept in departments:
        dept_id = dept["department_id"]
        dept_name = dept["department_name"]
        
        # Skip adding specific positions for sub-departments
        if dept["parent_department_id"] is not None:
            continue
        
        # VP level
        positions.append({
            "position_id": position_id,
            "title": f"VP of {dept_name}",
            "department_id": dept_id,
            "level": "VP",
            "salary_band_minimum": HIERARCHY_LEVELS["VP"]["min"] * 1000,
            "salary_band_maximum": HIERARCHY_LEVELS["VP"]["max"] * 1000
        })
        position_id += 1
        
        # Director level
        positions.append({
            "position_id": position_id,
            "title": f"Director of {dept_name}",
            "department_id": dept_id,
            "level": "Director",
            "salary_band_minimum": HIERARCHY_LEVELS["Director"]["min"] * 1000,
            "salary_band_maximum": HIERARCHY_LEVELS["Director"]["max"] * 1000
        })
        position_id += 1
        
        # Manager level
        positions.append({
            "position_id": position_id,
            "title": f"{dept_name} Manager",
            "department_id": dept_id,
            "level": "Manager",
            "salary_band_minimum": HIERARCHY_LEVELS["Manager"]["min"] * 1000,
            "salary_band_maximum": HIERARCHY_LEVELS["Manager"]["max"] * 1000
        })
        position_id += 1
        
        # Team Lead
        positions.append({
            "position_id": position_id,
            "title": f"{dept_name} Team Lead",
            "department_id": dept_id,
            "level": "Team Lead",
            "salary_band_minimum": HIERARCHY_LEVELS["Team Lead"]["min"] * 1000,
            "salary_band_maximum": HIERARCHY_LEVELS["Team Lead"]["max"] * 1000
        })
        position_id += 1
        
        # Individual Contributors
        for level in ["Senior", "Mid-level", "Junior"]:
            positions.append({
                "position_id": position_id,
                "title": f"{level} {dept_name} Specialist",
                "department_id": dept_id,
                "level": level,
                "salary_band_minimum": HIERARCHY_LEVELS[level]["min"] * 1000,
                "salary_band_maximum": HIERARCHY_LEVELS[level]["max"] * 1000
            })
            position_id += 1
    
    # Add specific roles for Engineering
    eng_roles = ["Software Engineer", "QA Engineer", "DevOps Engineer", "Frontend Developer", "Backend Developer"]
    eng_dept_id = 1  # Engineering department ID
    
    for role in eng_roles:
        for level in ["Senior", "Mid-level", "Junior"]:
            positions.append({
                "position_id": position_id,
                "title": f"{level} {role}",
                "department_id": eng_dept_id,
                "level": level,
                "salary_band_minimum": HIERARCHY_LEVELS[level]["min"] * 1000,
                "salary_band_maximum": HIERARCHY_LEVELS[level]["max"] * 1000
            })
            position_id += 1
    
    return positions

# Employee generation
# Team generation functions
def generate_teams(employees: List[Dict]) -> List[Dict]:
    """Generate cross-functional project teams."""
    teams = []
    team_id = 1
    
    # Define some realistic project names
    project_names = [
        "Atlas Platform Migration",
        "Customer Portal Redesign",
        "Mobile App 2.0",
        "Cloud Infrastructure Upgrade",
        "Data Analytics Platform",
        "Security Compliance Initiative",
        "API Gateway Implementation",
        "DevOps Automation",
        "ML Recommendation Engine",
        "Customer Retention Program",
        "Horizon 2026 Strategic Planning",
        "Enterprise CRM Integration",
        "Marketplace Expansion",
        "Internal Knowledge Base",
        "Performance Optimization"
    ]
    
    # Create teams with realistic start/end dates
    for i, project_name in enumerate(project_names):
        # Find a suitable team lead (manager or team lead level)
        potential_leads = [e for e in employees if e["employment_status"] == "Active" and 
                         ("Manager" in e["job_title"] or "Lead" in e["job_title"] or "Director" in e["job_title"])]
        
        if potential_leads:
            team_lead = random.choice(potential_leads)
            
            # Determine if project is ongoing or completed
            is_ongoing = random.random() < 0.7  # 70% of projects are ongoing
            
            # Generate start date (within last 2 years)
            start_date = generate_random_date(CURRENT_DATE - timedelta(days=365*2), 
                                             CURRENT_DATE - timedelta(days=30)).strftime("%Y-%m-%d")
            
            # For completed projects, generate end date
            end_date = None
            if not is_ongoing:
                # End date is between start date and current date
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = generate_random_date(start_date_obj + timedelta(days=30), 
                                               CURRENT_DATE).strftime("%Y-%m-%d")
            
            teams.append({
                "team_id": team_id,
                "team_name": project_name.replace(" ", "_").lower() + "_team",
                "team_lead_id": team_lead["employee_id"],
                "project_name": project_name,
                "start_date": start_date,
                "end_date": end_date
            })
            
            team_id += 1
    
    return teams

# OKR generation functions
def generate_company_okrs(employees: List[Dict]) -> List[Dict]:
    """Generate company-level objectives and key results."""
    company_okrs = []
    objective_id = 1
    
    # Find executives for ownership
    executives = [e for e in employees if e["job_title"] in ["CEO", "CTO", "CFO", "COO", "CHRO", "CMO"]]
    
    # Define company objectives
    objectives = [
        {
            "statement": "Achieve market leadership in cloud-based enterprise solutions",
            "description": "Establish Horizon Technologies as the go-to provider for cloud-based enterprise solutions in our target markets",
            "owner_role": "CEO",
            "timeframe": "FY 2025",
            "priority": "High"
        },
        {
            "statement": "Increase annual recurring revenue by 30%",
            "description": "Drive substantial growth in ARR through new customer acquisition and expansion of existing accounts",
            "owner_role": "CFO",
            "timeframe": "FY 2025",
            "priority": "High"
        },
        {
            "statement": "Launch next-generation platform with AI capabilities",
            "description": "Develop and release our next-gen platform with integrated AI features that differentiate us from competitors",
            "owner_role": "CTO",
            "timeframe": "Q3 2025",
            "priority": "High"
        },
        {
            "statement": "Improve customer satisfaction and reduce churn",
            "description": "Enhance customer experience to improve NPS scores and reduce customer churn rate",
            "owner_role": "COO",
            "timeframe": "Q2 2025",
            "priority": "Medium"
        },
        {
            "statement": "Expand into European market",
            "description": "Establish operations and customer base in key European markets",
            "owner_role": "CEO",
            "timeframe": "Q4 2025",
            "priority": "Medium"
        },
        {
            "statement": "Build world-class engineering organization",
            "description": "Attract, develop and retain top engineering talent to drive innovation",
            "owner_role": "CHRO",
            "timeframe": "FY 2025",
            "priority": "Medium"
        },
        {
            "statement": "Achieve SOC 2 Type II compliance",
            "description": "Implement security controls and processes to achieve SOC 2 Type II compliance",
            "owner_role": "CTO",
            "timeframe": "Q2 2025",
            "priority": "Low"
        }
    ]
    
    # Create company OKRs
    for obj in objectives:
        # Find the appropriate owner
        owner = next((e for e in executives if e["job_title"] == obj["owner_role"]), random.choice(executives))
        
        # Determine status with some randomness
        if obj["timeframe"] == CURRENT_TIMEFRAME:
            status_weights = [0.6, 0.3, 0.1]  # Mostly on track
        elif obj["timeframe"] > CURRENT_TIMEFRAME:  # Future timeframe
            status_weights = [0.3, 0.5, 0.2]  # More likely at risk
        else:  # Past timeframe
            status_weights = [0.7, 0.2, 0.1]  # Mostly completed
        
        status = weighted_choice(STATUS_OPTIONS, status_weights)
        
        company_okrs.append({
            "objective_id": objective_id,
            "objective_statement": obj["statement"],
            "timeframe": obj["timeframe"],
            "owner_id": owner["employee_id"],
            "status": status,
            "priority": obj["priority"],
            "description": obj["description"]
        })
        
        objective_id += 1
    
    return company_okrs

def generate_department_okrs(company_okrs: List[Dict], departments: List[Dict], employees: List[Dict]) -> List[Dict]:
    """Generate department-level objectives that support company objectives."""
    department_okrs = []
    dept_objective_id = 1
    
    # For each top-level department
    for dept in departments:
        if dept["parent_department_id"] is not None:
            continue  # Skip sub-departments for simplicity
        
        dept_id = dept["department_id"]
        dept_name = dept["department_name"]
        dept_head_id = dept["department_head_id"]
        
        # Determine how many objectives this department should have (3-5)
        num_objectives = random.randint(3, 5)
        
        # Randomly select company objectives to support
        # Some departments might have misaligned objectives (not supporting company goals)
        include_misaligned = random.random() < 0.3  # 30% chance of including misaligned objectives
        
        # Create department objectives
        for i in range(num_objectives):
            # Determine if this objective is aligned with company objectives
            is_aligned = not include_misaligned or (i < num_objectives - 1)
            
            if is_aligned:
                # Select a random company objective to support
                parent_objective = random.choice(company_okrs)
                parent_id = parent_objective["objective_id"]
                timeframe = parent_objective["timeframe"]
                
                # Create an aligned objective
                if dept_name == "Engineering":
                    statements = [
                        f"Deliver technical capabilities for {parent_objective['objective_statement'].lower()}",
                        f"Build infrastructure to support {parent_objective['objective_statement'].lower()}",
                        f"Develop technical solutions for {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Product Management":
                    statements = [
                        f"Define product roadmap to achieve {parent_objective['objective_statement'].lower()}",
                        f"Prioritize features that enable {parent_objective['objective_statement'].lower()}",
                        f"Create product specifications for {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Sales & Marketing":
                    statements = [
                        f"Drive market awareness to support {parent_objective['objective_statement'].lower()}",
                        f"Generate qualified leads to achieve {parent_objective['objective_statement'].lower()}",
                        f"Develop go-to-market strategy for {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Customer Success":
                    statements = [
                        f"Ensure customer adoption to support {parent_objective['objective_statement'].lower()}",
                        f"Improve customer experience to enable {parent_objective['objective_statement'].lower()}",
                        f"Reduce churn to achieve {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Finance & Accounting":
                    statements = [
                        f"Optimize financial operations to support {parent_objective['objective_statement'].lower()}",
                        f"Ensure funding for initiatives related to {parent_objective['objective_statement'].lower()}",
                        f"Develop financial models for {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Human Resources":
                    statements = [
                        f"Recruit talent needed to achieve {parent_objective['objective_statement'].lower()}",
                        f"Develop training programs to support {parent_objective['objective_statement'].lower()}",
                        f"Create compensation structures aligned with {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Operations":
                    statements = [
                        f"Streamline processes to enable {parent_objective['objective_statement'].lower()}",
                        f"Implement operational improvements for {parent_objective['objective_statement'].lower()}",
                        f"Optimize resource allocation to support {parent_objective['objective_statement'].lower()}"
                    ]
                elif dept_name == "Research & Development":
                    statements = [
                        f"Research new technologies to enable {parent_objective['objective_statement'].lower()}",
                        f"Develop innovative solutions for {parent_objective['objective_statement'].lower()}",
                        f"Create prototypes to support {parent_objective['objective_statement'].lower()}"
                    ]
                else:
                    statements = [
                        f"Support company initiative to {parent_objective['objective_statement'].lower()}",
                        f"Contribute departmental resources to {parent_objective['objective_statement'].lower()}",
                        f"Align department activities with {parent_objective['objective_statement'].lower()}"
                    ]
            else:
                # Create a misaligned objective (not supporting any company objective)
                parent_id = None
                timeframe = random.choice(TIMEFRAMES)
                
                # Department-specific misaligned objectives
                if dept_name == "Engineering":
                    statements = [
                        "Rewrite legacy codebase using latest framework",
                        "Achieve 100% unit test coverage",
                        "Migrate all services to microservices architecture"
                    ]
                elif dept_name == "Product Management":
                    statements = [
                        "Redesign product interface",
                        "Add 20 new features to the platform",
                        "Create comprehensive product documentation"
                    ]
                elif dept_name == "Sales & Marketing":
                    statements = [
                        "Increase social media followers by 50%",
                        "Redesign company website",
                        "Attend 15 industry conferences"
                    ]
                elif dept_name == "Customer Success":
                    statements = [
                        "Implement new ticketing system",
                        "Create customer feedback program",
                        "Develop new customer onboarding process"
                    ]
                else:
                    statements = [
                        "Improve internal department processes",
                        "Implement new department-specific tools",
                        "Reorganize department structure"
                    ]
            
            # Select a random statement
            objective_statement = random.choice(statements)
            
            # Determine status with some randomness
            if timeframe == CURRENT_TIMEFRAME:
                status_weights = [0.5, 0.3, 0.2]  # Mix of statuses
            elif timeframe > CURRENT_TIMEFRAME:  # Future timeframe
                status_weights = [0.3, 0.5, 0.2]  # More likely at risk
            else:  # Past timeframe
                status_weights = [0.7, 0.2, 0.1]  # Mostly completed
            
            status = weighted_choice(STATUS_OPTIONS, status_weights)
            
            # Determine priority
            if is_aligned and parent_objective["priority"] == "High":
                priority_weights = [0.7, 0.2, 0.1]  # Mostly high priority
            elif is_aligned and parent_objective["priority"] == "Medium":
                priority_weights = [0.3, 0.6, 0.1]  # Mostly medium priority
            elif is_aligned and parent_objective["priority"] == "Low":
                priority_weights = [0.1, 0.3, 0.6]  # Mostly low priority
            else:
                priority_weights = [0.2, 0.5, 0.3]  # Mix of priorities
            
            priority = weighted_choice(PRIORITY_OPTIONS, priority_weights)
            
            department_okrs.append({
                "department_objective_id": dept_objective_id,
                "department_id": dept_id,
                "objective_statement": objective_statement,
                "parent_objective_id": parent_id,
                "timeframe": timeframe,
                "owner_id": dept_head_id,
                "status": status,
                "priority": priority
            })
            
            dept_objective_id += 1
    
    return department_okrs

def generate_team_okrs(department_okrs: List[Dict], teams: List[Dict], employees: List[Dict]) -> List[Dict]:
    """Generate team-level objectives that support department objectives."""
    team_okrs = []
    team_objective_id = 1
    
    # For each team
    for team in teams:
        team_id = team["team_id"]
        team_lead_id = team["team_lead_id"]
        
        # Find team lead to determine their department
        team_lead = next((e for e in employees if e["employee_id"] == team_lead_id), None)
        if not team_lead:
            continue
        
        team_dept_id = team_lead["department_id"]
        
        # Find department objectives for this team's department
        dept_objectives = [obj for obj in department_okrs if obj["department_id"] == team_dept_id]
        
        # If no department objectives found, try to find any department objective
        if not dept_objectives:
            dept_objectives = department_okrs
        
        # Determine how many objectives this team should have (2-4)
        num_objectives = random.randint(2, 4)
        
        # Some teams might have misaligned objectives (not supporting department goals)
        include_misaligned = random.random() < 0.2  # 20% chance of including misaligned objectives
        
        # Create team objectives
        for i in range(num_objectives):
            # Determine if this objective is aligned with department objectives
            is_aligned = not include_misaligned or (i < num_objectives - 1)
            
            if is_aligned and dept_objectives:
                # Select a random department objective to support
                parent_objective = random.choice(dept_objectives)
                parent_id = parent_objective["department_objective_id"]
                timeframe = parent_objective["timeframe"]
                
                # Create an aligned objective based on team's project
                project_name = team["project_name"]
                statements = [
                    f"Deliver {project_name} components that support {parent_objective['objective_statement'].lower()}",
                    f"Complete {project_name} milestones aligned with {parent_objective['objective_statement'].lower()}",
                    f"Implement {project_name} features for {parent_objective['objective_statement'].lower()}"
                ]
            else:
                # Create a misaligned objective (not supporting any department objective)
                parent_id = None
                timeframe = random.choice(TIMEFRAMES)
                
                # Project-specific misaligned objectives
                project_name = team["project_name"]
                statements = [
                    f"Complete all planned {project_name} features",
                    f"Improve {project_name} performance metrics",
                    f"Reduce {project_name} technical debt",
                    f"Document {project_name} architecture and processes",
                    f"Conduct user research for {project_name}"
                ]
            
            # Select a random statement
            objective_statement = random.choice(statements)
            
            # Determine status with some randomness
            if timeframe == CURRENT_TIMEFRAME:
                status_weights = [0.4, 0.4, 0.2]  # Mix of statuses
            elif timeframe > CURRENT_TIMEFRAME:  # Future timeframe
                status_weights = [0.2, 0.5, 0.3]  # More likely at risk or behind
            else:  # Past timeframe
                status_weights = [0.6, 0.3, 0.1]  # Mostly completed
            
            status = weighted_choice(STATUS_OPTIONS, status_weights)
            
            # Determine priority (if aligned, inherit from parent)
            if is_aligned and dept_objectives:
                priority = parent_objective["priority"]
            else:
                priority = weighted_choice(PRIORITY_OPTIONS, [0.3, 0.5, 0.2])
            
            team_okrs.append({
                "team_objective_id": team_objective_id,
                "team_id": team_id,
                "objective_statement": objective_statement,
                "department_objective_id": parent_id,
                "timeframe": timeframe,
                "owner_id": team_lead_id,
                "status": status,
                "priority": priority
            })
            
            team_objective_id += 1
    
    return team_okrs

def generate_key_results(company_okrs: List[Dict], employees: List[Dict]) -> List[Dict]:
    """Generate measurable key results for company objectives."""
    key_results = []
    key_result_id = 1
    
    # Define key results for each company objective
    key_result_templates = {
        "Achieve market leadership in cloud-based enterprise solutions": [
            {
                "description": "Increase market share to 15% in target verticals",
                "target_value": 15,
                "unit": "percentage",
                "progress_range": (8, 13)  # Current progress range
            },
            {
                "description": "Achieve #1 or #2 position in industry analyst reports",
                "target_value": 2,
                "unit": "rank",
                "progress_range": (3, 5)  # Current progress range
            },
            {
                "description": "Secure 25 reference customers from Fortune 500",
                "target_value": 25,
                "unit": "customers",
                "progress_range": (15, 22)  # Current progress range
            }
        ],
        "Increase annual recurring revenue by 30%": [
            {
                "description": "Close $15M in new business",
                "target_value": 15000000,
                "unit": "USD",
                "progress_range": (8000000, 12000000)  # Current progress range
            },
            {
                "description": "Increase average deal size to $100K",
                "target_value": 100000,
                "unit": "USD",
                "progress_range": (75000, 95000)  # Current progress range
            },
            {
                "description": "Achieve 120% net revenue retention",
                "target_value": 120,
                "unit": "percentage",
                "progress_range": (105, 115)  # Current progress range
            }
        ],
        "Launch next-generation platform with AI capabilities": [
            {
                "description": "Complete development of 5 key AI features",
                "target_value": 5,
                "unit": "features",
                "progress_range": (2, 4)  # Current progress range
            },
            {
                "description": "Achieve 99.99% platform availability",
                "target_value": 99.99,
                "unit": "percentage",
                "progress_range": (99.9, 99.98)  # Current progress range
            },
            {
                "description": "Reduce average API response time to 100ms",
                "target_value": 100,
                "unit": "milliseconds",
                "progress_range": (150, 200)  # Current progress range
            },
            {
                "description": "Onboard 50 beta customers to new platform",
                "target_value": 50,
                "unit": "customers",
                "progress_range": (20, 40)  # Current progress range
            }
        ],
        "Improve customer satisfaction and reduce churn": [
            {
                "description": "Increase NPS score to 50",
                "target_value": 50,
                "unit": "score",
                "progress_range": (35, 45)  # Current progress range
            },
            {
                "description": "Reduce annual customer churn to 5%",
                "target_value": 5,
                "unit": "percentage",
                "progress_range": (7, 10)  # Current progress range
            },
            {
                "description": "Decrease average support ticket resolution time to 4 hours",
                "target_value": 4,
                "unit": "hours",
                "progress_range": (6, 8)  # Current progress range
            }
        ],
        "Expand into European market": [
            {
                "description": "Establish legal entities in 3 European countries",
                "target_value": 3,
                "unit": "entities",
                "progress_range": (1, 2)  # Current progress range
            },
            {
                "description": "Hire 20 employees for European operations",
                "target_value": 20,
                "unit": "employees",
                "progress_range": (5, 15)  # Current progress range
            },
            {
                "description": "Generate €5M in European revenue",
                "target_value": 5000000,
                "unit": "EUR",
                "progress_range": (1000000, 3000000)  # Current progress range
            }
        ],
        "Build world-class engineering organization": [
            {
                "description": "Reduce engineering turnover to less than 10%",
                "target_value": 10,
                "unit": "percentage",
                "progress_range": (15, 20)  # Current progress range
            },
            {
                "description": "Hire 50 new engineers",
                "target_value": 50,
                "unit": "engineers",
                "progress_range": (20, 40)  # Current progress range
            },
            {
                "description": "Implement career development plans for 100% of engineering staff",
                "target_value": 100,
                "unit": "percentage",
                "progress_range": (60, 80)  # Current progress range
            }
        ],
        "Achieve SOC 2 Type II compliance": [
            {
                "description": "Complete 100% of required security controls",
                "target_value": 100,
                "unit": "percentage",
                "progress_range": (60, 90)  # Current progress range
            },
            {
                "description": "Pass all pre-audit assessments",
                "target_value": 1,
                "unit": "binary",
                "progress_range": (0, 1)  # Current progress range
            },
            {
                "description": "Train 100% of employees on security procedures",
                "target_value": 100,
                "unit": "percentage",
                "progress_range": (70, 90)  # Current progress range
            }
        ]
    }
    
    # Generate key results for each company objective
    for objective in company_okrs:
        objective_statement = objective["objective_statement"]
        objective_id = objective["objective_id"]
        
        # Get key results for this objective
        if objective_statement in key_result_templates:
            templates = key_result_templates[objective_statement]
            
            for template in templates:
                # Find a suitable owner (not the same as objective owner)
                potential_owners = [e for e in employees if e["employment_status"] == "Active" 
                                  and e["employee_id"] != objective["owner_id"]]
                owner = random.choice(potential_owners)
                
                # Generate current progress value within the specified range
                min_progress, max_progress = template["progress_range"]
                if template["unit"] == "binary":
                    current_value = random.randint(min_progress, max_progress)
                else:
                    current_value = round(random.uniform(min_progress, max_progress), 2)
                
                # Calculate confidence score based on progress vs target
                progress_ratio = current_value / template["target_value"]
                if template["description"].startswith("Reduce") or template["description"].startswith("Decrease"):
                    # For metrics where lower is better, invert the ratio
                    if current_value > 0:  # Avoid division by zero
                        progress_ratio = template["target_value"] / current_value
                
                confidence_score = min(10, max(1, int(progress_ratio * 10)))
                
                # Generate last updated date (within last month)
                last_updated = generate_random_date(CURRENT_DATE - timedelta(days=30), 
                                                 CURRENT_DATE).strftime("%Y-%m-%d")
                
                # Generate start and end dates
                timeframe = objective["timeframe"]
                if timeframe.startswith("Q"):
                    quarter = int(timeframe[1])
                    year = int(timeframe[-4:])
                    start_date = datetime(year, (quarter-1)*3+1, 1).strftime("%Y-%m-%d")
                    end_month = quarter * 3
                    end_date = datetime(year, end_month, 28).strftime("%Y-%m-%d")
                else:  # FY
                    year = int(timeframe[-4:])
                    start_date = datetime(year, 1, 1).strftime("%Y-%m-%d")
                    end_date = datetime(year, 12, 31).strftime("%Y-%m-%d")
                
                key_results.append({
                    "key_result_id": key_result_id,
                    "objective_id": objective_id,
                    "description": template["description"],
                    "target_value": template["target_value"],
                    "current_value": current_value,
                    "unit_of_measurement": template["unit"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "owner_id": owner["employee_id"],
                    "last_updated": last_updated,
                    "confidence_score": confidence_score
                })
                
                key_result_id += 1
    
    return key_results

# Dependency and alignment data generation functions
def generate_dependencies(teams: List[Dict]) -> List[Dict]:
    """Generate cross-team dependencies."""
    dependencies = []
    dependency_id = 1
    
    # Create dependencies between teams
    # About 70% of teams will have dependencies
    dependent_teams = random.sample(teams, int(len(teams) * 0.7))
    
    for dependent_team in dependent_teams:
        # Each dependent team will have 1-3 dependencies
        num_dependencies = random.randint(1, 3)
        
        # Find teams that this team depends on (excluding itself)
        potential_dependency_teams = [t for t in teams if t["team_id"] != dependent_team["team_id"]]
        
        if potential_dependency_teams:
            # Select random teams to depend on
            dependency_count = min(num_dependencies, len(potential_dependency_teams))
            dependency_teams = random.sample(potential_dependency_teams, dependency_count)
            
            for dependency_team in dependency_teams:
                # Generate a dependency description
                descriptions = [
                    f"Need API specifications from {dependency_team['project_name']} team",
                    f"Waiting for component delivery from {dependency_team['project_name']} team",
                    f"Require technical documentation from {dependency_team['project_name']} team",
                    f"Blocked on integration testing with {dependency_team['project_name']} team",
                    f"Need design assets from {dependency_team['project_name']} team",
                    f"Waiting for security review from {dependency_team['project_name']} team",
                    f"Dependent on infrastructure changes from {dependency_team['project_name']} team"
                ]
                
                description = random.choice(descriptions)
                
                # Generate due date (within next 90 days)
                due_date = generate_random_date(CURRENT_DATE, 
                                              CURRENT_DATE + timedelta(days=90)).strftime("%Y-%m-%d")
                
                # Determine status
                status_weights = [0.2, 0.5, 0.2, 0.1]  # Not Started, In Progress, Completed, Blocked
                status = weighted_choice(DEPENDENCY_STATUS, status_weights)
                
                # Determine criticality
                criticality = weighted_choice(PRIORITY_OPTIONS, [0.3, 0.5, 0.2])  # High, Medium, Low
                
                # Generate impact description
                if criticality == "High":
                    impact = f"Critical path item that will delay {dependent_team['project_name']} delivery if not completed on time"
                elif criticality == "Medium":
                    impact = f"Important dependency that affects multiple features in {dependent_team['project_name']}"
                else:
                    impact = f"Minor dependency that can be worked around if needed"
                
                dependencies.append({
                    "dependency_id": dependency_id,
                    "dependent_team_id": dependent_team["team_id"],
                    "dependency_team_id": dependency_team["team_id"],
                    "description": description,
                    "due_date": due_date,
                    "status": status,
                    "criticality": criticality,
                    "impact_description": impact
                })
                
                dependency_id += 1
    
    return dependencies

def generate_status_updates(teams: List[Dict], departments: List[Dict], employees: List[Dict]) -> List[Dict]:
    """Generate status updates for teams and departments."""
    status_updates = []
    update_id = 1
    
    # Generate team status updates
    for team in teams:
        # Generate 2-5 status updates per team over the last 90 days
        num_updates = random.randint(2, 5)
        
        # Generate update dates (sorted from oldest to newest)
        update_dates = sorted([
            generate_random_date(CURRENT_DATE - timedelta(days=90), CURRENT_DATE)
            for _ in range(num_updates)
        ])
        
        # Find team members who could author updates
        team_lead_id = team["team_id"]
        
        for i, update_date in enumerate(update_dates):
            # Determine status (trend from good to bad or bad to good)
            if random.random() < 0.5:  # Trend from good to bad
                status_weights = [0.8 - (i * 0.15), 0.1 + (i * 0.1), 0.1 + (i * 0.05)]
            else:  # Trend from bad to good
                status_weights = [0.2 + (i * 0.15), 0.4 - (i * 0.05), 0.4 - (i * 0.1)]
            
            status = weighted_choice(STATUS_OPTIONS, status_weights)
            
            # Generate summary based on status
            if status == "On Track":
                summaries = [
                    f"{team['project_name']} progressing as planned",
                    f"All {team['project_name']} milestones on schedule",
                    f"Good progress on {team['project_name']} deliverables"
                ]
                blockers = "No significant blockers at this time"
                next_steps = [
                    "Continue with planned development activities",
                    "Proceed to next phase of the project",
                    "Begin planning for upcoming milestones"
                ]
            elif status == "At Risk":
                summaries = [
                    f"Some {team['project_name']} milestones at risk",
                    f"Resource constraints affecting {team['project_name']} timeline",
                    f"Technical challenges emerging in {team['project_name']}"
                ]
                blockers = [
                    "Resource allocation issues",
                    "Technical complexity higher than estimated",
                    "Dependencies from other teams delayed",
                    "Scope creep affecting timeline"
                ]
                next_steps = [
                    "Escalate resource needs to management",
                    "Reprioritize features to meet critical deadlines",
                    "Schedule technical review to address challenges"
                ]
            else:  # Behind
                summaries = [
                    f"{team['project_name']} behind schedule",
                    f"Critical {team['project_name']} milestones missed",
                    f"Significant delays in {team['project_name']} delivery"
                ]
                blockers = [
                    "Critical dependencies not met",
                    "Major technical issues discovered",
                    "Team capacity severely constrained",
                    "Requirements changed significantly"
                ]
                next_steps = [
                    "Develop recovery plan with revised timeline",
                    "Request additional resources to address gaps",
                    "Reduce scope to focus on critical deliverables"
                ]
            
            summary = random.choice(summaries)
            blockers = random.choice(blockers) if isinstance(blockers, list) else blockers
            next_steps = random.choice(next_steps)
            
            status_updates.append({
                "update_id": update_id,
                "entity_id": team["team_id"],
                "entity_type": "Team",
                "report_date": update_date.strftime("%Y-%m-%d"),
                "status": status,
                "summary": summary,
                "blockers": blockers,
                "next_steps": next_steps,
                "author_id": team_lead_id
            })
            
            update_id += 1
    
    # Generate department status updates (less frequent)
    for dept in departments:
        if dept["parent_department_id"] is not None:
            continue  # Skip sub-departments
        
        # Generate 1-3 status updates per department over the last 90 days
        num_updates = random.randint(1, 3)
        
        # Generate update dates (sorted from oldest to newest)
        update_dates = sorted([
            generate_random_date(CURRENT_DATE - timedelta(days=90), CURRENT_DATE)
            for _ in range(num_updates)
        ])
        
        dept_head_id = dept["department_head_id"]
        
        for update_date in update_dates:
            # Determine status (mostly positive for department reports)
            status = weighted_choice(STATUS_OPTIONS, [0.7, 0.2, 0.1])
            
            # Generate summary based on status and department
            dept_name = dept["department_name"]
            
            if status == "On Track":
                summary = f"{dept_name} objectives progressing well across all initiatives"
                blockers = "No significant blockers at the department level"
                next_steps = "Continue executing on department strategy and supporting team initiatives"
            elif status == "At Risk":
                summary = f"Some {dept_name} objectives at risk due to resource constraints"
                blockers = "Budget limitations and competing priorities affecting progress"
                next_steps = "Reprioritizing department initiatives and reallocating resources"
            else:  # Behind
                summary = f"{dept_name} facing significant challenges in meeting objectives"
                blockers = "Critical resource gaps and external factors impacting multiple initiatives"
                next_steps = "Developing department recovery plan and requesting additional support"
            
            status_updates.append({
                "update_id": update_id,
                "entity_id": dept["department_id"],
                "entity_type": "Department",
                "report_date": update_date.strftime("%Y-%m-%d"),
                "status": status,
                "summary": summary,
                "blockers": blockers,
                "next_steps": next_steps,
                "author_id": dept_head_id
            })
            
            update_id += 1
    
    return status_updates

def generate_resource_allocation(departments: List[Dict], company_okrs: List[Dict], department_okrs: List[Dict]) -> List[Dict]:
    """Generate resource allocation data."""
    resource_allocations = []
    allocation_id = 1
    
    # For each department
    for dept in departments:
        if dept["parent_department_id"] is not None:
            continue  # Skip sub-departments
        
        dept_id = dept["department_id"]
        
        # Find department objectives
        dept_objectives = [obj for obj in department_okrs if obj["department_id"] == dept_id]
        
        # If no department objectives, skip
        if not dept_objectives:
            continue
        
        # Allocate headcount resources
        total_headcount = random.randint(20, 50)  # Total headcount for department
        remaining_headcount = total_headcount
        
        # Allocate budget resources
        total_budget = random.randint(500000, 5000000)  # Total budget for department
        remaining_budget = total_budget
        
        # First, allocate to aligned objectives
        aligned_objectives = [obj for obj in dept_objectives if obj["parent_objective_id"] is not None]
        
        for obj in aligned_objectives:
            # Determine priority-based allocation percentage
            if obj["priority"] == "High":
                headcount_pct = random.uniform(0.2, 0.4)  # 20-40% of resources
                budget_pct = random.uniform(0.2, 0.4)
            elif obj["priority"] == "Medium":
                headcount_pct = random.uniform(0.1, 0.2)  # 10-20% of resources
                budget_pct = random.uniform(0.1, 0.2)
            else:  # Low priority
                headcount_pct = random.uniform(0.05, 0.1)  # 5-10% of resources
                budget_pct = random.uniform(0.05, 0.1)
            
            # Calculate allocations
            headcount_allocation = int(total_headcount * headcount_pct)
            budget_allocation = int(total_budget * budget_pct)
            
            # Ensure we don't exceed remaining resources
            headcount_allocation = min(headcount_allocation, remaining_headcount)
            budget_allocation = min(budget_allocation, remaining_budget)
            
            remaining_headcount -= headcount_allocation
            remaining_budget -= budget_allocation
            
            # Determine timeframe from the objective
            timeframe = obj["timeframe"]
            
            # Add headcount allocation
            resource_allocations.append({
                "allocation_id": allocation_id,
                "department_id": dept_id,
                "objective_id": obj["department_objective_id"],
                "resource_type": "Headcount",
                "allocated_amount": headcount_allocation,
                "timeframe": timeframe,
                "actual_usage": int(headcount_allocation * random.uniform(0.8, 1.2)),  # Actual usage varies
                "variance_explanation": "" if 0.9 <= (headcount_allocation / total_headcount) <= 1.1 else 
                                       "Resource reallocation due to changing priorities"
            })
            allocation_id += 1
            
            # Add budget allocation
            resource_allocations.append({
                "allocation_id": allocation_id,
                "department_id": dept_id,
                "objective_id": obj["department_objective_id"],
                "resource_type": "Budget",
                "allocated_amount": budget_allocation,
                "timeframe": timeframe,
                "actual_usage": int(budget_allocation * random.uniform(0.8, 1.2)),  # Actual usage varies
                "variance_explanation": "" if 0.9 <= (budget_allocation / total_budget) <= 1.1 else 
                                       "Budget adjustment based on actual expenditure patterns"
            })
            allocation_id += 1
        
        # Then, allocate to misaligned objectives (if any resources left)
        misaligned_objectives = [obj for obj in dept_objectives if obj["parent_objective_id"] is None]
        
        if misaligned_objectives and (remaining_headcount > 0 or remaining_budget > 0):
            # Distribute remaining resources among misaligned objectives
            for obj in misaligned_objectives:
                # Allocate a portion of remaining resources
                headcount_allocation = int(remaining_headcount / len(misaligned_objectives))
                budget_allocation = int(remaining_budget / len(misaligned_objectives))
                
                timeframe = obj["timeframe"]
                
                # Add headcount allocation if any
                if headcount_allocation > 0:
                    resource_allocations.append({
                        "allocation_id": allocation_id,
                        "department_id": dept_id,
                        "objective_id": obj["department_objective_id"],
                        "resource_type": "Headcount",
                        "allocated_amount": headcount_allocation,
                        "timeframe": timeframe,
                        "actual_usage": int(headcount_allocation * random.uniform(0.8, 1.2)),
                        "variance_explanation": "Resources allocated to department-specific initiative"
                    })
                    allocation_id += 1
                
                # Add budget allocation if any
                if budget_allocation > 0:
                    resource_allocations.append({
                        "allocation_id": allocation_id,
                        "department_id": dept_id,
                        "objective_id": obj["department_objective_id"],
                        "resource_type": "Budget",
                        "allocated_amount": budget_allocation,
                        "timeframe": timeframe,
                        "actual_usage": int(budget_allocation * random.uniform(0.8, 1.2)),
                        "variance_explanation": "Budget allocated to department-specific initiative"
                    })
                    allocation_id += 1
    
    return resource_allocations

def generate_okr_updates(key_results: List[Dict], employees: List[Dict]) -> List[Dict]:
    """Generate historical updates to OKR progress."""
    okr_updates = []
    update_id = 1
    
    # For each key result, generate 1-5 updates over time
    for kr in key_results:
        # Determine number of updates
        num_updates = random.randint(1, 5)
        
        # Get current value and target value
        current_value = kr["current_value"]
        target_value = kr["target_value"]
        
        # Generate a progression of values from 0 to current value
        is_decreasing = "Reduce" in kr["description"] or "Decrease" in kr["description"]
        
        if is_decreasing:
            # For metrics where lower is better, start high and decrease
            start_value = target_value * random.uniform(1.5, 2.0)
            values = [start_value]
            
            # Generate intermediate values that decrease over time
            for i in range(1, num_updates):
                progress_pct = i / num_updates
                value = start_value - (start_value - current_value) * progress_pct
                values.append(value)
        else:
            # For metrics where higher is better, start low and increase
            values = [0]  # Start at 0
            
            # Generate intermediate values that increase over time
            for i in range(1, num_updates):
                progress_pct = i / num_updates
                value = current_value * progress_pct
                values.append(value)
        
        # Sort values appropriately
        if is_decreasing:
            values.sort(reverse=True)  # Highest to lowest
        else:
            values.sort()  # Lowest to highest
        
        # Generate update dates (from oldest to newest)
        start_date = datetime.strptime(kr["start_date"], "%Y-%m-%d")
        last_updated = datetime.strptime(kr["last_updated"], "%Y-%m-%d")
        
        date_range = (last_updated - start_date).days
        update_dates = []
        
        for i in range(num_updates):
            days_offset = int(date_range * (i / num_updates))
            update_date = start_date + timedelta(days=days_offset)
            update_dates.append(update_date)
        
        # Generate updates
        for i in range(num_updates):
            # For the last update, use the current value
            if i == num_updates - 1:
                new_value = current_value
            else:
                new_value = values[i]
            
            # Determine previous value
            previous_value = 0 if i == 0 else values[i-1]
            
            # Calculate confidence score based on progress vs target and time elapsed
            progress_ratio = new_value / target_value if not is_decreasing else target_value / new_value
            time_elapsed_ratio = (update_dates[i] - start_date).days / date_range
            
            # If progress ratio is better than time elapsed ratio, confidence is higher
            confidence_factor = progress_ratio / time_elapsed_ratio if time_elapsed_ratio > 0 else 1
            confidence_score = min(10, max(1, int(confidence_factor * 5)))
            
            # Generate notes based on progress
            if new_value > previous_value and not is_decreasing:
                notes = [
                    "Good progress made this period",
                    "Team efforts showing positive results",
                    "On track to meet target",
                    "Steady improvement in metrics"
                ]
            elif new_value < previous_value and is_decreasing:
                notes = [
                    "Successfully reduced metric this period",
                    "Improvement efforts showing results",
                    "Continuing to make progress toward target",
                    "Optimization initiatives working well"
                ]
            elif new_value == previous_value:
                notes = [
                    "No change in metric this period",
                    "Progress temporarily plateaued",
                    "Working on strategies to resume progress",
                    "Maintaining current level while addressing challenges"
                ]
            else:
                notes = [
                    "Metric moved in wrong direction",
                    "Facing challenges in making progress",
                    "Implementing recovery plan",
                    "Reassessing approach to meet target"
                ]
            
            # Find a random employee to be the updater (preferably the owner)
            updater_id = kr["owner_id"]
            if random.random() < 0.3:  # 30% chance of someone else updating
                active_employees = [e for e in employees if e["employment_status"] == "Active"]
                if active_employees:
                    updater = random.choice(active_employees)
                    updater_id = updater["employee_id"]
            
            okr_updates.append({
                "update_id": update_id,
                "key_result_id": kr["key_result_id"],
                "previous_value": round(previous_value, 2),
                "new_value": round(new_value, 2),
                "update_date": update_dates[i].strftime("%Y-%m-%d"),
                "confidence_score": confidence_score,
                "notes": random.choice(notes),
                "updater_id": updater_id
            })
            
            update_id += 1
    
    return okr_updates

def generate_team_members(teams: List[Dict], employees: List[Dict]) -> List[Dict]:
    """Generate team membership data."""
    team_members = []
    
    # Define possible roles in teams
    roles = [
        "Project Manager", "Technical Lead", "Developer", "Designer", "QA Engineer",
        "Business Analyst", "Product Owner", "DevOps Engineer", "Data Scientist",
        "UX Researcher", "Content Strategist", "Marketing Specialist"
    ]
    
    # For each team, assign members
    for team in teams:
        # Team lead is automatically a member
        team_lead_id = team["team_lead_id"]
        team_lead = next((e for e in employees if e["employee_id"] == team_lead_id), None)
        
        if team_lead:
            team_members.append({
                "team_id": team["team_id"],
                "employee_id": team_lead_id,
                "role_in_team": "Team Lead",
                "allocation_percentage": random.randint(30, 70)  # Team leads split time
            })
        
        # Determine team size (between 5 and 15 members including lead)
        team_size = random.randint(5, 15)
        
        # Get active employees excluding the team lead
        active_employees = [e for e in employees if e["employment_status"] == "Active" and e["employee_id"] != team_lead_id]
        
        # Select random team members
        team_member_count = min(team_size - 1, len(active_employees))
        selected_members = random.sample(active_employees, team_member_count)
        
        for member in selected_members:
            # Assign a role
            role = random.choice(roles)
            
            # Determine allocation percentage (some fully dedicated, others part-time)
            allocation = random.choices([100, random.randint(10, 90)], weights=[0.3, 0.7], k=1)[0]
            
            team_members.append({
                "team_id": team["team_id"],
                "employee_id": member["employee_id"],
                "role_in_team": role,
                "allocation_percentage": allocation
            })
    
    return team_members

def generate_employees(departments: List[Dict], positions: List[Dict]) -> List[Dict]:
    """Generate employee data with appropriate distribution across departments."""
    employees = []
    employee_id = 1
    
    # First, create the C-Suite
    c_suite_positions = [p for p in positions if p["level"] == "C-Suite"]
    
    for position in c_suite_positions:
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        employees.append({
            "employee_id": employee_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": generate_email(first_name, last_name),
            "hire_date": generate_random_date(CURRENT_DATE - timedelta(days=365*10), CURRENT_DATE - timedelta(days=365*5)).strftime("%Y-%m-%d"),
            "job_title": position["title"],
            "department_id": None,  # C-Suite spans all departments
            "manager_id": None if position["title"] == "CEO" else 1,  # CEO is employee_id 1, reports to no one
            "employment_status": "Active",
            "location": "San Francisco, CA",  # C-Suite is at HQ
            "salary": generate_salary("C-Suite")
        })
        employee_id += 1
    
    # Assign department heads (VPs)
    for dept in departments:
        if dept["parent_department_id"] is None:  # Only for top-level departments
            dept_name = dept["department_name"]
            vp_position = next((p for p in positions if p["title"] == f"VP of {dept_name}"), None)
            
            if vp_position:
                first_name = fake.first_name()
                last_name = fake.last_name()
                
                employees.append({
                    "employee_id": employee_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": generate_email(first_name, last_name),
                    "hire_date": generate_random_date(CURRENT_DATE - timedelta(days=365*8), CURRENT_DATE - timedelta(days=365*3)).strftime("%Y-%m-%d"),
                    "job_title": vp_position["title"],
                    "department_id": dept["department_id"],
                    "manager_id": 1,  # Reports to CEO
                    "employment_status": "Active",
                    "location": dept["location"],
                    "salary": generate_salary("VP")
                })
                
                # Update department head
                dept["department_head_id"] = employee_id
                employee_id += 1
    
    # Now distribute the rest of employees according to department distribution
    remaining_employees = NUM_EMPLOYEES - employee_id + 1
    
    for dept in departments:
        dept_id = dept["department_id"]
        dept_name = dept["department_name"]
        
        # Skip sub-departments for now
        if dept["parent_department_id"] is not None:
            continue
        
        # Calculate number of employees for this department
        if dept_name in DEPARTMENT_DISTRIBUTION:
            dept_percentage = DEPARTMENT_DISTRIBUTION[dept_name]
            dept_employees = int(remaining_employees * dept_percentage)
            
            # Get positions for this department
            dept_positions = [p for p in positions if p["department_id"] == dept_id]
            
            # Create employees for this department
            for _ in range(dept_employees):
                # Select a random position appropriate for this department
                position = random.choice(dept_positions)
                
                first_name = fake.first_name()
                last_name = fake.last_name()
                
                # Determine manager based on position level
                if position["level"] == "Director":
                    manager_id = dept["department_head_id"]  # Reports to VP
                elif position["level"] == "Manager":
                    # Find a director in this department
                    directors = [e for e in employees if e["department_id"] == dept_id and "Director" in e["job_title"]]
                    manager_id = directors[0]["employee_id"] if directors else dept["department_head_id"]
                elif position["level"] == "Team Lead":
                    # Find a manager in this department
                    managers = [e for e in employees if e["department_id"] == dept_id and "Manager" in e["job_title"]]
                    manager_id = managers[0]["employee_id"] if managers else dept["department_head_id"]
                else:
                    # Find a team lead or manager in this department
                    leads = [e for e in employees if e["department_id"] == dept_id and ("Lead" in e["job_title"] or "Manager" in e["job_title"])]
                    manager_id = leads[0]["employee_id"] if leads else dept["department_head_id"]
                
                employees.append({
                    "employee_id": employee_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": generate_email(first_name, last_name),
                    "hire_date": generate_random_date(CURRENT_DATE - timedelta(days=365*7), CURRENT_DATE).strftime("%Y-%m-%d"),
                    "job_title": position["title"],
                    "department_id": dept_id,
                    "manager_id": manager_id,
                    "employment_status": weighted_choice(EMPLOYMENT_STATUS, [0.95, 0.04, 0.01]),  # Mostly active
                    "location": weighted_choice([dept["location"]] + LOCATIONS, [0.7] + [0.3/len(LOCATIONS)]*len(LOCATIONS)),
                    "salary": generate_salary(position["level"])
                })
                employee_id += 1
    
    return employees

# Main execution function
def main():
    """Main function to orchestrate the data generation process."""
    print(f"Generating synthetic data for {COMPANY_NAME}...")
    
    # Generate organizational structure data
    departments = generate_departments()
    positions = generate_positions(departments)
    employees = generate_employees(departments, positions)
    
    # Save organizational structure data
    save_to_csv(departments, "departments.csv")
    save_to_csv(positions, "positions.csv")
    save_to_csv(employees, "employees.csv")
    
    # Generate team data
    teams = generate_teams(employees)
    team_members = generate_team_members(teams, employees)
    save_to_csv(teams, "teams.csv")
    save_to_csv(team_members, "team_members.csv")
    
    # Generate OKR data
    company_okrs = generate_company_okrs(employees)
    key_results = generate_key_results(company_okrs, employees)
    department_okrs = generate_department_okrs(company_okrs, departments, employees)
    team_okrs = generate_team_okrs(department_okrs, teams, employees)
    save_to_csv(company_okrs, "company_okrs.csv")
    save_to_csv(key_results, "key_results.csv")
    save_to_csv(department_okrs, "department_okrs.csv")
    save_to_csv(team_okrs, "team_okrs.csv")
    
    # Generate alignment and dependency data
    dependencies = generate_dependencies(teams)
    status_updates = generate_status_updates(teams, departments, employees)
    resource_allocation = generate_resource_allocation(departments, company_okrs, department_okrs)
    okr_updates = generate_okr_updates(key_results, employees)
    save_to_csv(dependencies, "cross_team_dependencies.csv")
    save_to_csv(status_updates, "status_updates.csv")
    save_to_csv(resource_allocation, "resource_allocation.csv")
    save_to_csv(okr_updates, "okr_updates.csv")
    
    print(f"Data generation complete. Files saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
