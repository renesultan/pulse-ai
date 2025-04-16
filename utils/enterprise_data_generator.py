"""
Enterprise Matrix Organization Data Generator for F*ck Meetings app
This module generates sample enterprise data with matrix organization structure
"""

import random
import json
from datetime import datetime, timedelta
import os
import sys

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models import (
    Organization, Region, Location, Department, Project, 
    Employee, OrgChart, project_members, secondary_reports
)

# Enterprise organization configuration
ORG_CONFIG = {
    'name': 'TechNova Global',
    'description': 'A leading enterprise technology company specializing in cloud solutions, AI, and digital transformation.',
    'industry': 'Technology',
    'headquarters': 'San Francisco, CA',
    
    'regions': [
        {'name': 'Americas', 'code': 'AM'},
        {'name': 'EMEA', 'code': 'EMEA'},
        {'name': 'APAC', 'code': 'APAC'}
    ],
    
    'locations': {
        'Americas': [
            {'name': 'San Francisco HQ', 'city': 'San Francisco', 'country': 'USA', 'timezone': 'GMT-8', 'is_headquarters': True},
            {'name': 'New York Office', 'city': 'New York', 'country': 'USA', 'timezone': 'GMT-5', 'is_headquarters': False},
            {'name': 'Austin Office', 'city': 'Austin', 'country': 'USA', 'timezone': 'GMT-6', 'is_headquarters': False},
            {'name': 'Toronto Office', 'city': 'Toronto', 'country': 'Canada', 'timezone': 'GMT-5', 'is_headquarters': False},
            {'name': 'Remote - Americas', 'city': 'Various', 'country': 'Various', 'timezone': 'Various', 'is_headquarters': False}
        ],
        'EMEA': [
            {'name': 'London Office', 'city': 'London', 'country': 'UK', 'timezone': 'GMT', 'is_headquarters': False},
            {'name': 'Berlin Office', 'city': 'Berlin', 'country': 'Germany', 'timezone': 'GMT+1', 'is_headquarters': False},
            {'name': 'Tel Aviv Office', 'city': 'Tel Aviv', 'country': 'Israel', 'timezone': 'GMT+2', 'is_headquarters': False},
            {'name': 'Remote - EMEA', 'city': 'Various', 'country': 'Various', 'timezone': 'Various', 'is_headquarters': False}
        ],
        'APAC': [
            {'name': 'Singapore Office', 'city': 'Singapore', 'country': 'Singapore', 'timezone': 'GMT+8', 'is_headquarters': False},
            {'name': 'Sydney Office', 'city': 'Sydney', 'country': 'Australia', 'timezone': 'GMT+10', 'is_headquarters': False},
            {'name': 'Tokyo Office', 'city': 'Tokyo', 'country': 'Japan', 'timezone': 'GMT+9', 'is_headquarters': False},
            {'name': 'Bangalore Office', 'city': 'Bangalore', 'country': 'India', 'timezone': 'GMT+5:30', 'is_headquarters': False},
            {'name': 'Remote - APAC', 'city': 'Various', 'country': 'Various', 'timezone': 'Various', 'is_headquarters': False}
        ]
    },
    
    'departments': [
        {'name': 'Executive Leadership', 'code': 'EXE', 'cost_center': 'CC-100', 'parent': None},
        {'name': 'Engineering', 'code': 'ENG', 'cost_center': 'CC-200', 'parent': None},
        {'name': 'Product', 'code': 'PRD', 'cost_center': 'CC-300', 'parent': None},
        {'name': 'Marketing', 'code': 'MKT', 'cost_center': 'CC-400', 'parent': None},
        {'name': 'Sales', 'code': 'SLS', 'cost_center': 'CC-500', 'parent': None},
        {'name': 'People Operations', 'code': 'HR', 'cost_center': 'CC-600', 'parent': None},
        {'name': 'Finance', 'code': 'FIN', 'cost_center': 'CC-700', 'parent': None},
        {'name': 'Legal', 'code': 'LGL', 'cost_center': 'CC-800', 'parent': None},
        {'name': 'Customer Success', 'code': 'CS', 'cost_center': 'CC-900', 'parent': None},
        {'name': 'Information Technology', 'code': 'IT', 'cost_center': 'CC-1000', 'parent': None}
    ],
    
    'sub_departments': {
        'Engineering': [
            {'name': 'Frontend Engineering', 'code': 'ENG-FE', 'cost_center': 'CC-210'},
            {'name': 'Backend Engineering', 'code': 'ENG-BE', 'cost_center': 'CC-220'},
            {'name': 'Infrastructure', 'code': 'ENG-INF', 'cost_center': 'CC-230'},
            {'name': 'Security', 'code': 'ENG-SEC', 'cost_center': 'CC-240'},
            {'name': 'Data Engineering', 'code': 'ENG-DATA', 'cost_center': 'CC-250'},
            {'name': 'Quality Assurance', 'code': 'ENG-QA', 'cost_center': 'CC-260'}
        ],
        'Product': [
            {'name': 'Product Management', 'code': 'PRD-PM', 'cost_center': 'CC-310'},
            {'name': 'Product Design', 'code': 'PRD-DES', 'cost_center': 'CC-320'},
            {'name': 'User Research', 'code': 'PRD-UR', 'cost_center': 'CC-330'},
            {'name': 'Product Analytics', 'code': 'PRD-ANL', 'cost_center': 'CC-340'}
        ],
        'Marketing': [
            {'name': 'Brand Marketing', 'code': 'MKT-BRD', 'cost_center': 'CC-410'},
            {'name': 'Product Marketing', 'code': 'MKT-PRD', 'cost_center': 'CC-420'},
            {'name': 'Growth Marketing', 'code': 'MKT-GRW', 'cost_center': 'CC-430'},
            {'name': 'Marketing Operations', 'code': 'MKT-OPS', 'cost_center': 'CC-440'}
        ],
        'Sales': [
            {'name': 'Inside Sales', 'code': 'SLS-INS', 'cost_center': 'CC-510'},
            {'name': 'Field Sales', 'code': 'SLS-FLD', 'cost_center': 'CC-520'},
            {'name': 'Solutions Engineering', 'code': 'SLS-SOL', 'cost_center': 'CC-530'},
            {'name': 'Sales Operations', 'code': 'SLS-OPS', 'cost_center': 'CC-540'}
        ],
        'Customer Success': [
            {'name': 'Customer Support', 'code': 'CS-SUP', 'cost_center': 'CC-910'},
            {'name': 'Customer Education', 'code': 'CS-EDU', 'cost_center': 'CC-920'},
            {'name': 'Account Management', 'code': 'CS-ACC', 'cost_center': 'CC-930'}
        ]
    },
    
    'projects': [
        {
            'name': 'Project Phoenix',
            'code': 'PHX',
            'description': 'Next-generation cloud platform rewrite with enhanced performance and security features',
            'status': 'Active',
            'priority': 'High',
            'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
        },
        {
            'name': 'AI Assistant Integration',
            'code': 'AI-AST',
            'description': 'Add AI assistant capabilities across all product lines',
            'status': 'Active',
            'priority': 'High',
            'start_date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Global Expansion - APAC',
            'code': 'GE-APAC',
            'description': 'Expansion of operations and localization for APAC markets',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Enterprise Security Compliance',
            'code': 'ESC',
            'description': 'Ensure all systems comply with latest security regulations',
            'status': 'Active',
            'priority': 'High',
            'start_date': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Data Platform Modernization',
            'code': 'DPM',
            'description': 'Update data infrastructure to support real-time analytics',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=120)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Mobile Experience Revamp',
            'code': 'MXR',
            'description': 'Complete redesign of mobile applications',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Developer Platform API',
            'code': 'DEV-API',
            'description': 'Create public APIs and developer platform for ecosystem growth',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Sales Enablement',
            'code': 'SE',
            'description': 'Improve sales tools and processes for higher conversion',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=75)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Customer Feedback Loop',
            'code': 'CFL',
            'description': 'Create systematic process to incorporate customer feedback',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=100)).strftime('%Y-%m-%d')
        },
        {
            'name': 'HR Digital Transformation',
            'code': 'HR-DT',
            'description': 'Modernize all HR systems and employee experience',
            'status': 'Active',
            'priority': 'Low',
            'start_date': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Cost Optimization',
            'code': 'COST-OPT',
            'description': 'Review and optimize company-wide spending',
            'status': 'Active',
            'priority': 'Medium',
            'start_date': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Compliance Framework',
            'code': 'COMP',
            'description': 'Build regulatory compliance system for all regions',
            'status': 'Active',
            'priority': 'High',
            'start_date': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=120)).strftime('%Y-%m-%d')
        },
        {
            'name': 'Customer Knowledge Base',
            'code': 'CKB',
            'description': 'Develop comprehensive self-service knowledge base',
            'status': 'Active',
            'priority': 'Low',
            'start_date': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
        },
        {
            'name': 'IT Infrastructure Upgrade',
            'code': 'IT-INF',
            'description': 'Modernize internal IT systems and infrastructure',
            'status': 'Active',
            'priority': 'Low',
            'start_date': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')
        },
    ],
    
    # Executive team structure
    'executive_team': [
        {'name': 'Sarah Chen', 'title': 'Chief Executive Officer', 'department': 'Executive Leadership', 'reports_to': None},
        {'name': 'Alex Rodriguez', 'title': 'Chief Technology Officer', 'department': 'Engineering', 'reports_to': 'Sarah Chen'},
        {'name': 'Mira Patel', 'title': 'Chief Product Officer', 'department': 'Product', 'reports_to': 'Sarah Chen'},
        {'name': 'James Wilson', 'title': 'Chief Marketing Officer', 'department': 'Marketing', 'reports_to': 'Sarah Chen'},
        {'name': 'David Klein', 'title': 'Chief Revenue Officer', 'department': 'Sales', 'reports_to': 'Sarah Chen'},
        {'name': 'Emily Johnson', 'title': 'Chief People Officer', 'department': 'People Operations', 'reports_to': 'Sarah Chen'},
        {'name': 'Michael Chang', 'title': 'Chief Financial Officer', 'department': 'Finance', 'reports_to': 'Sarah Chen'},
        {'name': 'Lauren Gonzalez', 'title': 'General Counsel', 'department': 'Legal', 'reports_to': 'Sarah Chen'},
        {'name': 'Tom Watkins', 'title': 'Chief Customer Officer', 'department': 'Customer Success', 'reports_to': 'Sarah Chen'},
        {'name': 'Rajesh Kumar', 'title': 'Chief Information Officer', 'department': 'Information Technology', 'reports_to': 'Sarah Chen'}
    ],
    
    # SVP/VP level
    'vp_team': [
        # Engineering VPs
        {'name': 'Kevin Zhang', 'title': 'SVP, Engineering', 'department': 'Engineering', 'reports_to': 'Alex Rodriguez'},
        {'name': 'Lisa Wong', 'title': 'VP, Frontend Engineering', 'department': 'Frontend Engineering', 'reports_to': 'Kevin Zhang'},
        {'name': 'John Smith', 'title': 'VP, Backend Engineering', 'department': 'Backend Engineering', 'reports_to': 'Kevin Zhang'},
        {'name': 'Maria Santos', 'title': 'VP, Infrastructure', 'department': 'Infrastructure', 'reports_to': 'Kevin Zhang'},
        {'name': 'Omar Hassan', 'title': 'VP, Security', 'department': 'Security', 'reports_to': 'Kevin Zhang'},
        {'name': 'Priya Nair', 'title': 'VP, Data Engineering', 'department': 'Data Engineering', 'reports_to': 'Kevin Zhang'},
        {'name': 'Wei Chen', 'title': 'VP, Quality Assurance', 'department': 'Quality Assurance', 'reports_to': 'Kevin Zhang'},
        
        # Product VPs
        {'name': 'Samantha Lee', 'title': 'SVP, Product', 'department': 'Product', 'reports_to': 'Mira Patel'},
        {'name': 'Daniel Okafor', 'title': 'VP, Product Management', 'department': 'Product Management', 'reports_to': 'Samantha Lee'},
        {'name': 'Sophia Garcia', 'title': 'VP, Product Design', 'department': 'Product Design', 'reports_to': 'Samantha Lee'},
        {'name': 'Taro Yamamoto', 'title': 'VP, User Research', 'department': 'User Research', 'reports_to': 'Samantha Lee'},
        {'name': 'Andrew Kim', 'title': 'VP, Product Analytics', 'department': 'Product Analytics', 'reports_to': 'Samantha Lee'},
        
        # Marketing VPs
        {'name': 'Nicole Dubois', 'title': 'SVP, Marketing', 'department': 'Marketing', 'reports_to': 'James Wilson'},
        {'name': 'Carlos Rivera', 'title': 'VP, Brand Marketing', 'department': 'Brand Marketing', 'reports_to': 'Nicole Dubois'},
        {'name': 'Emma Thompson', 'title': 'VP, Product Marketing', 'department': 'Product Marketing', 'reports_to': 'Nicole Dubois'},
        {'name': 'Liam O\'Brien', 'title': 'VP, Growth Marketing', 'department': 'Growth Marketing', 'reports_to': 'Nicole Dubois'},
        {'name': 'Zara Ahmed', 'title': 'VP, Marketing Operations', 'department': 'Marketing Operations', 'reports_to': 'Nicole Dubois'},
        
        # Sales VPs
        {'name': 'Robert Jackson', 'title': 'SVP, Global Sales', 'department': 'Sales', 'reports_to': 'David Klein'},
        {'name': 'Sophie Martin', 'title': 'VP, Inside Sales', 'department': 'Inside Sales', 'reports_to': 'Robert Jackson'},
        {'name': 'Marcus Chen', 'title': 'VP, Field Sales', 'department': 'Field Sales', 'reports_to': 'Robert Jackson'},
        {'name': 'Ava Williams', 'title': 'VP, Solutions Engineering', 'department': 'Solutions Engineering', 'reports_to': 'Robert Jackson'},
        {'name': 'Raj Patel', 'title': 'VP, Sales Operations', 'department': 'Sales Operations', 'reports_to': 'Robert Jackson'},
        
        # Customer Success VPs
        {'name': 'Jennifer Murphy', 'title': 'SVP, Customer Success', 'department': 'Customer Success', 'reports_to': 'Tom Watkins'},
        {'name': 'Hiroshi Tanaka', 'title': 'VP, Customer Support', 'department': 'Customer Support', 'reports_to': 'Jennifer Murphy'},
        {'name': 'Olivia Bennett', 'title': 'VP, Customer Education', 'department': 'Customer Education', 'reports_to': 'Jennifer Murphy'},
        {'name': 'Ryan Campbell', 'title': 'VP, Account Management', 'department': 'Account Management', 'reports_to': 'Jennifer Murphy'},
        
        # Other department VPs
        {'name': 'Grace Park', 'title': 'VP, People Operations', 'department': 'People Operations', 'reports_to': 'Emily Johnson'},
        {'name': 'Thomas Weber', 'title': 'VP, Finance', 'department': 'Finance', 'reports_to': 'Michael Chang'},
        {'name': 'Aisha Johnson', 'title': 'VP, Legal Affairs', 'department': 'Legal', 'reports_to': 'Lauren Gonzalez'},
        {'name': 'Victor Nguyen', 'title': 'VP, Information Technology', 'department': 'Information Technology', 'reports_to': 'Rajesh Kumar'}
    ]
}

# Names and titles for generating more employees
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven", "Paul", "Andrew", "Joshua",
    "Michelle", "Laura", "Sarah", "Kimberly", "Deborah", "Jessica", "Shirley", "Cynthia", "Angela", "Melissa",
    "Jason", "Brian", "Kevin", "Edward", "Ronald", "Timothy", "Jeffrey", "Gary", "Ryan", "Nicholas",
    "Catherine", "Christine", "Samantha", "Rebecca", "Virginia", "Martha", "Debra", "Amanda", "Stephanie", "Carolyn",
    "Jacob", "Jose", "Gregory", "Joshua", "Frank", "Benjamin", "Peter", "Samuel", "Raymond", "Patrick",
    "Margaret", "Ashley", "Judith", "Helen", "Olivia", "Sandra", "Tara", "Sophia", "Isabella", "Emily",
    "Jack", "Dennis", "Jerry", "Alexander", "Tyler", "Harold", "Douglas", "Henry", "Carl", "Arthur",
    "Emma", "Chloe", "Abigail", "Madison", "Ella", "Lily", "Natalie", "Hannah", "Addison", "Victoria",
    "Wei", "Li", "Ming", "Yong", "Jie", "Hui", "Yan", "Xin", "Yu", "Hao",
    "Mei", "Na", "Ying", "Xia", "Juan", "Yan", "Zhen", "Fang", "Lin", "Hong",
    "Raj", "Amit", "Sanjay", "Vijay", "Rahul", "Arjun", "Nikhil", "Anil", "Sunil", "Vikram",
    "Priya", "Neha", "Anjali", "Pooja", "Divya", "Ananya", "Manisha", "Swati", "Nisha", "Kavita",
    "Mohammed", "Ali", "Omar", "Ahmed", "Hassan", "Khalid", "Tariq", "Abdul", "Samir", "Jamal",
    "Fatima", "Aisha", "Layla", "Maryam", "Zahra", "Huda", "Amina", "Zainab", "Leila", "Yasmin",
    "Dmitri", "Ivan", "Sergei", "Andrei", "Vladimir", "Mikhail", "Nikita", "Alexei", "Igor", "Boris",
    "Olga", "Natasha", "Svetlana", "Tatiana", "Ekaterina", "Anna", "Elena", "Irina", "Yulia", "Anastasia"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
    "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King",
    "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins",
    "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey",
    "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez",
    "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross",
    "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington",
    "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes",
    "Wang", "Li", "Zhang", "Chen", "Liu", "Yang", "Huang", "Zhao", "Wu", "Zhou",
    "Patel", "Kumar", "Singh", "Shah", "Sharma", "Gupta", "Desai", "Mehta", "Joshi", "Verma",
    "Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Cho", "Yoon", "Jang", "Kwon",
    "Ahmed", "Mohamed", "Ali", "Ibrahim", "Hassan", "Khan", "Rahman", "Mahmoud", "Abdi", "Hussein",
    "Ivanov", "Smirnov", "Kuznetsov", "Popov", "Sokolov", "Lebedev", "Kozlov", "Novikov", "Morozov", "Petrov",
    "Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Almeida", "Costa", "Carvalho", "Gomes",
    "Müller", "Schmidt", "Schneider", "Fischer", "Meyer", "Weber", "Schulz", "Wagner", "Becker", "Hoffmann",
    "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau", "Simon"
]

# Engineering roles
ENG_ROLES = {
    'Frontend Engineering': [
        "Frontend Engineer", "Senior Frontend Engineer", "Staff Frontend Engineer", "Frontend Engineering Manager", 
        "Frontend Architect", "UI Developer", "React Specialist", "Angular Developer", "Web Performance Engineer"
    ],
    'Backend Engineering': [
        "Backend Engineer", "Senior Backend Engineer", "Staff Backend Engineer", "Backend Engineering Manager",
        "Systems Architect", "API Developer", "Service Infrastructure Engineer", "Database Specialist"
    ],
    'Infrastructure': [
        "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer", "Infrastructure Engineer",
        "Platform Engineer", "Systems Administrator", "Kubernetes Specialist", "Infrastructure Architect"
    ],
    'Security': [
        "Security Engineer", "Application Security Engineer", "Security Analyst", "Security Operations Engineer",
        "Penetration Tester", "Security Architect", "Compliance Specialist", "Security Manager"
    ],
    'Data Engineering': [
        "Data Engineer", "Data Scientist", "Machine Learning Engineer", "Data Architect",
        "ETL Developer", "Analytics Engineer", "Big Data Specialist", "Data Engineering Manager"
    ],
    'Quality Assurance': [
        "QA Engineer", "Test Automation Engineer", "QA Analyst", "Quality Assurance Manager",
        "Performance Test Engineer", "SDET", "QA Architect", "Test Lead"
    ]
}

# Product roles
PRODUCT_ROLES = {
    'Product Management': [
        "Product Manager", "Senior Product Manager", "Principal Product Manager", "Group Product Manager",
        "Technical Product Manager", "Product Owner", "Product Operations Manager"
    ],
    'Product Design': [
        "Product Designer", "UX Designer", "UI Designer", "Senior Product Designer",
        "Design Manager", "Design Systems Engineer", "Visual Designer", "Interaction Designer"
    ],
    'User Research': [
        "User Researcher", "UX Researcher", "Research Analyst", "Senior User Researcher",
        "Research Operations Manager", "Quantitative Researcher", "Research Manager"
    ],
    'Product Analytics': [
        "Product Analyst", "Data Analyst", "Analytics Manager", "Growth Analyst",
        "Senior Product Analyst", "Business Intelligence Analyst", "Insights Manager"
    ]
}

# Marketing roles
MARKETING_ROLES = {
    'Brand Marketing': [
        "Brand Manager", "Brand Strategist", "Brand Marketing Specialist", "Creative Director",
        "Brand Designer", "Content Strategist", "Corporate Communications Manager"
    ],
    'Product Marketing': [
        "Product Marketing Manager", "Senior PMM", "Product Marketing Director",
        "Solutions Marketing Manager", "Technical Marketing Manager", "Marketing Content Manager"
    ],
    'Growth Marketing': [
        "Growth Marketing Manager", "Acquisition Marketing Manager", "Demand Generation Specialist",
        "Digital Marketing Manager", "SEO Specialist", "Performance Marketing Manager", "Email Marketing Specialist"
    ],
    'Marketing Operations': [
        "Marketing Operations Manager", "Marketing Technology Specialist", "Campaign Manager",
        "Marketing Analytics Manager", "Marketing Automation Specialist", "Marketing Systems Administrator"
    ]
}

# Sales roles
SALES_ROLES = {
    'Inside Sales': [
        "Sales Development Representative", "Account Executive", "Senior Account Executive",
        "Sales Manager", "Business Development Representative", "Inside Sales Manager"
    ],
    'Field Sales': [
        "Field Sales Representative", "Territory Manager", "Regional Sales Manager",
        "Enterprise Account Executive", "Senior Account Manager", "Sales Director"
    ],
    'Solutions Engineering': [
        "Solutions Engineer", "Sales Engineer", "Technical Sales Specialist",
        "Pre-Sales Consultant", "Solutions Architect", "Technical Account Manager"
    ],
    'Sales Operations': [
        "Sales Operations Analyst", "Sales Operations Manager", "Revenue Operations Specialist",
        "Deal Desk Analyst", "Sales Enablement Manager", "CRM Administrator"
    ]
}

# Customer Success roles
CS_ROLES = {
    'Customer Support': [
        "Support Engineer", "Customer Support Specialist", "Technical Support Manager",
        "Support Operations Manager", "Customer Support Team Lead", "Technical Support Engineer"
    ],
    'Customer Education': [
        "Customer Education Specialist", "Training Manager", "Instructional Designer",
        "Education Content Developer", "Customer Training Specialist", "Learning Experience Designer"
    ],
    'Account Management': [
        "Customer Success Manager", "Account Manager", "Strategic Account Manager",
        "Customer Success Team Lead", "Implementation Specialist", "Onboarding Manager"
    ]
}

# Other departments
OTHER_ROLES = {
    'People Operations': [
        "HR Business Partner", "Recruiter", "Talent Acquisition Specialist", "People Operations Specialist",
        "Benefits Administrator", "Learning & Development Manager", "HR Coordinator", "Culture Manager"
    ],
    'Finance': [
        "Financial Analyst", "Accountant", "FP&A Manager", "Controller", "Treasury Analyst",
        "Payroll Manager", "Procurement Specialist", "Revenue Accountant"
    ],
    'Legal': [
        "Corporate Counsel", "Legal Counsel", "Compliance Manager", "Contract Specialist",
        "IP Attorney", "Privacy Counsel", "Legal Operations Manager"
    ],
    'Information Technology': [
        "IT Support Specialist", "Systems Administrator", "Network Engineer", "IT Project Manager",
        "Service Desk Manager", "IT Operations Manager", "Enterprise Applications Administrator"
    ],
    'Executive Leadership': [
        "Chief of Staff", "Executive Assistant", "Business Operations Manager"
    ]
}

# Create a dictionary mapping department names to roles for easier access
DEPARTMENT_ROLES = {}
DEPARTMENT_ROLES.update(ENG_ROLES)
DEPARTMENT_ROLES.update(PRODUCT_ROLES)
DEPARTMENT_ROLES.update(MARKETING_ROLES)
DEPARTMENT_ROLES.update(SALES_ROLES)
DEPARTMENT_ROLES.update(CS_ROLES)
DEPARTMENT_ROLES.update(OTHER_ROLES)

# Matrix project assignment probability by department (how likely someone from this dept is on a project)
PROJECT_ASSIGNMENT_PROBABILITY = {
    'Frontend Engineering': 0.6,
    'Backend Engineering': 0.7,
    'Infrastructure': 0.5,
    'Security': 0.4,
    'Data Engineering': 0.5,
    'Quality Assurance': 0.5,
    'Product Management': 0.8,
    'Product Design': 0.6,
    'User Research': 0.3,
    'Product Analytics': 0.4,
    'Brand Marketing': 0.3,
    'Product Marketing': 0.5,
    'Growth Marketing': 0.4,
    'Marketing Operations': 0.2,
    'Inside Sales': 0.3,
    'Field Sales': 0.3,
    'Solutions Engineering': 0.4,
    'Sales Operations': 0.2,
    'Customer Support': 0.3,
    'Customer Education': 0.3,
    'Account Management': 0.5,
    'People Operations': 0.2,
    'Finance': 0.2,
    'Legal': 0.2,
    'Information Technology': 0.3,
    'Executive Leadership': 0.7
}

# Default department team sizes (approximate number of employees per department)
DEPARTMENT_SIZES = {
    'Frontend Engineering': 25,
    'Backend Engineering': 30,
    'Infrastructure': 20,
    'Security': 15,
    'Data Engineering': 20,
    'Quality Assurance': 15,
    'Product Management': 15,
    'Product Design': 12,
    'User Research': 8,
    'Product Analytics': 10,
    'Brand Marketing': 8,
    'Product Marketing': 10,
    'Growth Marketing': 12,
    'Marketing Operations': 8,
    'Inside Sales': 20,
    'Field Sales': 25,
    'Solutions Engineering': 15,
    'Sales Operations': 10,
    'Customer Support': 20,
    'Customer Education': 8,
    'Account Management': 15,
    'People Operations': 12,
    'Finance': 10,
    'Legal': 8,
    'Information Technology': 15,
    'Executive Leadership': 5
}

def generate_enterprise_data():
    """Generate and store enterprise organization data in the database"""
    with app.app_context():
        try:
            # Clean existing data
            db.session.query(secondary_reports).delete()
            db.session.query(project_members).delete()
            db.session.query(OrgChart).delete()
            db.session.query(Employee).delete()
            db.session.query(Project).delete()
            db.session.query(Department).delete()
            db.session.query(Location).delete()
            db.session.query(Region).delete()
            db.session.query(Organization).delete()
            db.session.commit()
            
            print("Creating organization...")
            # Create organization
            org = Organization(
                name=ORG_CONFIG['name'],
                description=ORG_CONFIG['description'],
                industry=ORG_CONFIG['industry'],
                headquarters=ORG_CONFIG['headquarters']
            )
            db.session.add(org)
            db.session.commit()
            
            print("Creating regions and locations...")
            # Create regions
            regions = {}
            for region_data in ORG_CONFIG['regions']:
                region = Region(
                    name=region_data['name'],
                    code=region_data['code'],
                    organization_id=org.id
                )
                db.session.add(region)
                db.session.flush()
                regions[region_data['name']] = region
            
            # Create locations
            locations = {}
            for region_name, location_list in ORG_CONFIG['locations'].items():
                region = regions[region_name]
                for loc_data in location_list:
                    location = Location(
                        name=loc_data['name'],
                        city=loc_data['city'],
                        country=loc_data['country'],
                        timezone=loc_data['timezone'],
                        is_headquarters=loc_data['is_headquarters'],
                        region_id=region.id
                    )
                    db.session.add(location)
                    db.session.flush()
                    locations[loc_data['name']] = location
            
            db.session.commit()
            
            print("Creating departments...")
            # Create departments
            departments = {}
            for dept_data in ORG_CONFIG['departments']:
                department = Department(
                    name=dept_data['name'],
                    code=dept_data['code'],
                    cost_center=dept_data['cost_center'],
                    organization_id=org.id
                )
                db.session.add(department)
                db.session.flush()
                departments[dept_data['name']] = department
            
            # Create sub-departments
            for parent_name, sub_dept_list in ORG_CONFIG['sub_departments'].items():
                parent_dept = departments[parent_name]
                for sub_dept_data in sub_dept_list:
                    sub_dept = Department(
                        name=sub_dept_data['name'],
                        code=sub_dept_data['code'],
                        cost_center=sub_dept_data['cost_center'],
                        organization_id=org.id,
                        parent_id=parent_dept.id
                    )
                    db.session.add(sub_dept)
                    db.session.flush()
                    departments[sub_dept_data['name']] = sub_dept
            
            db.session.commit()
            
            print("Creating projects...")
            # Create projects
            projects = {}
            for project_data in ORG_CONFIG['projects']:
                project = Project(
                    name=project_data['name'],
                    code=project_data['code'],
                    description=project_data['description'],
                    status=project_data['status'],
                    priority=project_data['priority'],
                    start_date=datetime.strptime(project_data['start_date'], '%Y-%m-%d').date(),
                    end_date=datetime.strptime(project_data['end_date'], '%Y-%m-%d').date(),
                    organization_id=org.id
                )
                db.session.add(project)
                db.session.flush()
                projects[project_data['name']] = project
            
            db.session.commit()
            
            print("Creating executive team...")
            # Create executives
            employees = {}
            for exec_data in ORG_CONFIG['executive_team']:
                dept = departments[exec_data['department']]
                # Random location assignment for executives
                exec_location = random.choice(list(locations.values()))
                
                employee = Employee(
                    employee_id=f"E{random.randint(10000, 99999)}",
                    name=exec_data['name'],
                    title=exec_data['title'],
                    level="Executive",
                    organization_id=org.id,
                    department_id=dept.id,
                    location_id=exec_location.id,
                    cost_center=dept.cost_center
                )
                db.session.add(employee)
                db.session.flush()
                
                employees[exec_data['name']] = employee
            
            # Set reporting relationships for executives
            for exec_data in ORG_CONFIG['executive_team']:
                if exec_data['reports_to']:
                    employees[exec_data['name']].primary_manager_id = employees[exec_data['reports_to']].id
                    employees[exec_data['name']].reports_to_id = employees[exec_data['reports_to']].id
            
            db.session.commit()
            
            print("Creating VP team...")
            # Create VP level
            for vp_data in ORG_CONFIG['vp_team']:
                dept = departments[vp_data['department']]
                # Random location assignment for VPs
                vp_location = random.choice(list(locations.values()))
                
                employee = Employee(
                    employee_id=f"E{random.randint(10000, 99999)}",
                    name=vp_data['name'],
                    title=vp_data['title'],
                    level="VP",
                    organization_id=org.id,
                    department_id=dept.id,
                    location_id=vp_location.id,
                    cost_center=dept.cost_center
                )
                db.session.add(employee)
                db.session.flush()
                
                employees[vp_data['name']] = employee
            
            # Set reporting relationships for VPs
            for vp_data in ORG_CONFIG['vp_team']:
                if vp_data['reports_to']:
                    employees[vp_data['name']].primary_manager_id = employees[vp_data['reports_to']].id
                    employees[vp_data['name']].reports_to_id = employees[vp_data['reports_to']].id
            
            db.session.commit()
            
            print("Creating directors and managers...")
            # Create directors and managers
            dept_managers = {}
            for dept_name, dept in departments.items():
                if dept_name in DEPARTMENT_ROLES:  # Skip parent departments without direct roles
                    dept_managers[dept_name] = []
                    
                    # Create directors (2-3 per department)
                    num_directors = random.randint(2, 3) if dept_name != 'Executive Leadership' else 0
                    directors = []
                    
                    for _ in range(num_directors):
                        director_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                        director_location = random.choice(list(locations.values()))
                        
                        director = Employee(
                            employee_id=f"E{random.randint(10000, 99999)}",
                            name=director_name,
                            title=f"Director, {dept_name}",
                            level="Director",
                            organization_id=org.id,
                            department_id=dept.id,
                            location_id=director_location.id,
                            cost_center=dept.cost_center
                        )
                        db.session.add(director)
                        db.session.flush()
                        directors.append(director)
                        employees[director_name] = director
                        
                        # Find VP to report to
                        vp_name = None
                        for vp_data in ORG_CONFIG['vp_team']:
                            if vp_data['department'] == dept_name:
                                vp_name = vp_data['name']
                                break
                        
                        if vp_name:
                            director.primary_manager_id = employees[vp_name].id
                            director.reports_to_id = employees[vp_name].id
                    
                    # Create managers (2-3 per director)
                    for director in directors:
                        num_managers = random.randint(2, 3)
                        for _ in range(num_managers):
                            manager_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                            manager_location = random.choice(list(locations.values()))
                            
                            manager = Employee(
                                employee_id=f"E{random.randint(10000, 99999)}",
                                name=manager_name,
                                title=f"Manager, {dept_name}",
                                level="Manager",
                                organization_id=org.id,
                                department_id=dept.id,
                                location_id=manager_location.id,
                                primary_manager_id=director.id,
                                reports_to_id=director.id,
                                cost_center=dept.cost_center
                            )
                            db.session.add(manager)
                            db.session.flush()
                            dept_managers[dept_name].append(manager)
                            employees[manager_name] = manager
            
            db.session.commit()
            
            print("Creating employees...")
            # Create regular employees for each department
            for dept_name, dept_obj in departments.items():
                if dept_name in DEPARTMENT_ROLES and dept_name in DEPARTMENT_SIZES:
                    dept_size = DEPARTMENT_SIZES[dept_name]
                    roles = DEPARTMENT_ROLES[dept_name]
                    managers = dept_managers.get(dept_name, [])
                    
                    if not managers:
                        # Find any manager from a parent department
                        if dept_obj.parent_id:
                            parent_dept = Department.query.get(dept_obj.parent_id)
                            if parent_dept.name in dept_managers:
                                managers = dept_managers[parent_dept.name]
                    
                    # Create employees
                    num_employees = max(0, dept_size - len(managers))
                    for _ in range(num_employees):
                        emp_name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
                        emp_title = random.choice(roles)
                        emp_location = random.choice(list(locations.values()))
                        
                        # Determine level
                        if "Senior" in emp_title or "Lead" in emp_title:
                            emp_level = "Senior"
                        elif "Staff" in emp_title or "Principal" in emp_title:
                            emp_level = "Staff"
                        else:
                            emp_level = "Individual Contributor"
                        
                        employee = Employee(
                            employee_id=f"E{random.randint(10000, 99999)}",
                            name=emp_name,
                            title=emp_title,
                            level=emp_level,
                            organization_id=org.id,
                            department_id=dept_obj.id,
                            location_id=emp_location.id,
                            cost_center=dept_obj.cost_center
                        )
                        
                        # Assign to a manager if available
                        if managers:
                            manager = random.choice(managers)
                            employee.primary_manager_id = manager.id
                            employee.reports_to_id = manager.id
                        
                        db.session.add(employee)
                        db.session.flush()
                        employees[emp_name] = employee
                    
                    # Commit in batches to avoid memory issues
                    db.session.commit()
            
            print("Assigning project relationships...")
            # Assign employees to projects (matrix organization structure)
            all_employees = list(employees.values())
            for project in projects.values():
                # Assign executive sponsor
                exec_team = [emp for emp in all_employees if emp.level == "Executive"]
                if exec_team:
                    sponsor = random.choice(exec_team)
                    project.sponsor_id = sponsor.id
                
                # Assign project manager from Product Management
                pm_dept = departments.get('Product Management')
                if pm_dept:
                    pm_candidates = [emp for emp in all_employees if emp.department_id == pm_dept.id]
                    if pm_candidates:
                        pm = random.choice(pm_candidates)
                        project.members.append(pm)
                
                # For each department, decide if and how many people join the project
                for dept_name, prob in PROJECT_ASSIGNMENT_PROBABILITY.items():
                    if dept_name in departments:
                        dept = departments[dept_name]
                        dept_employees = [emp for emp in all_employees if emp.department_id == dept.id]
                        
                        # How many to assign from this department
                        team_size = min(len(dept_employees), random.randint(1, 3))
                        
                        # Only assign based on probability
                        if random.random() < prob and dept_employees:
                            # Take a random sample of employees from this department
                            project_team = random.sample(dept_employees, team_size)
                            
                            for emp in project_team:
                                project.members.append(emp)
            
            db.session.commit()
            
            print("Creating secondary reporting lines...")
            # Create matrix/secondary reporting relationships
            for project in projects.values():
                # For each project, establish secondary reporting lines
                # 1. Find the project manager (from Product Management)
                pm_dept = departments.get('Product Management')
                project_managers = [member for member in project.members 
                                    if member.department_id == pm_dept.id] if pm_dept else []
                
                if project_managers:
                    project_manager = project_managers[0]  # Take the first one as PM
                    
                    # 2. Have other project members report to the PM as a secondary manager
                    for member in project.members:
                        # Skip if this is the PM or already reporting to the PM
                        if member.id != project_manager.id and member.primary_manager_id != project_manager.id:
                            # Add dotted line reporting relationship
                            member.secondary_managers.append(project_manager)
            
            db.session.commit()
            
            print("Creating org chart visualizations...")
            # Create a hierarchical org chart
            hierarchical_chart = OrgChart(
                name=f"{org.name} Hierarchical Structure",
                description="Traditional reporting structure by department",
                organization_id=org.id,
                view_type="hierarchical",
                chart_data=json.dumps(generate_hierarchical_chart_data(org))
            )
            db.session.add(hierarchical_chart)
            
            # Create a matrix org chart
            matrix_chart = OrgChart(
                name=f"{org.name} Matrix Structure",
                description="Cross-functional project teams with dual reporting lines",
                organization_id=org.id,
                view_type="matrix",
                chart_data=json.dumps(generate_matrix_chart_data(org))
            )
            db.session.add(matrix_chart)
            
            # Create a project-based org chart for each major project
            for project_name, project in projects.items():
                if project.priority == "High":
                    project_chart = OrgChart(
                        name=f"{project_name} Team Structure",
                        description=f"Cross-functional team for {project_name}",
                        organization_id=org.id,
                        project_id=project.id,
                        view_type="project",
                        chart_data=json.dumps(generate_project_chart_data(project))
                    )
                    db.session.add(project_chart)
            
            db.session.commit()
            
            print("Enterprise organization data generation complete!")
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error generating enterprise data: {e}")
            return False

def generate_hierarchical_chart_data(organization):
    """Generate hierarchical chart data for visualization"""
    # Find the CEO
    ceo = Employee.query.filter_by(
        organization_id=organization.id, 
        primary_manager_id=None
    ).first()
    
    if not ceo:
        return {}
    
    # Build the hierarchical structure recursively
    def build_hierarchy(employee):
        children = []
        direct_reports = Employee.query.filter_by(primary_manager_id=employee.id).all()
        
        for report in direct_reports:
            children.append(build_hierarchy(report))
        
        return {
            "id": employee.id,
            "name": employee.name,
            "title": employee.title,
            "department": employee.department.name if employee.department else "",
            "level": employee.level,
            "children": children
        }
    
    # Start with the CEO
    hierarchy = build_hierarchy(ceo)
    
    return hierarchy

def generate_matrix_chart_data(organization):
    """Generate matrix chart data showing both primary and secondary reporting"""
    # Find the CEO
    ceo = Employee.query.filter_by(
        organization_id=organization.id, 
        primary_manager_id=None
    ).first()
    
    if not ceo:
        return {}
    
    # Build the matrix structure
    def build_matrix_hierarchy(employee):
        # Get primary direct reports
        direct_reports = Employee.query.filter_by(primary_manager_id=employee.id).all()
        children = []
        
        for report in direct_reports:
            children.append(build_matrix_hierarchy(report))
        
        # Get secondary/dotted-line reports
        dotted_reports = employee.dotted_line_reports
        dotted_relationships = []
        
        for report in dotted_reports:
            dotted_relationships.append({
                "id": report.id,
                "name": report.name,
                "title": report.title,
                "department": report.department.name if report.department else "",
                "primary_manager": report.primary_manager.name if report.primary_manager else ""
            })
        
        return {
            "id": employee.id,
            "name": employee.name,
            "title": employee.title,
            "department": employee.department.name if employee.department else "",
            "level": employee.level,
            "children": children,  # Primary reporting relationships
            "dotted_line_reports": dotted_relationships  # Secondary/matrix relationships
        }
    
    # Start with the CEO
    matrix_hierarchy = build_matrix_hierarchy(ceo)
    
    return matrix_hierarchy

def generate_project_chart_data(project):
    """Generate project-specific chart data"""
    sponsor = project.sponsor
    members = project.members
    
    # Group members by department
    members_by_dept = {}
    for member in members:
        dept_name = member.department.name if member.department else "No Department"
        if dept_name not in members_by_dept:
            members_by_dept[dept_name] = []
        
        members_by_dept[dept_name].append({
            "id": member.id,
            "name": member.name,
            "title": member.title,
            "level": member.level,
            "primary_manager": member.primary_manager.name if member.primary_manager else ""
        })
    
    # Build project hierarchy
    project_data = {
        "name": project.name,
        "code": project.code,
        "description": project.description,
        "status": project.status,
        "priority": project.priority,
        "start_date": project.start_date.strftime('%Y-%m-%d') if project.start_date else "",
        "end_date": project.end_date.strftime('%Y-%m-%d') if project.end_date else "",
        "sponsor": {
            "id": sponsor.id,
            "name": sponsor.name,
            "title": sponsor.title,
            "department": sponsor.department.name if sponsor.department else ""
        } if sponsor else None,
        "departments": []
    }
    
    # Add departments and their members
    for dept_name, dept_members in members_by_dept.items():
        project_data["departments"].append({
            "name": dept_name,
            "members": dept_members
        })
    
    return project_data

def get_enterprise_example_text():
    """Generate a text representation of the enterprise data for the UI"""
    CEO_NAME = "Sarah Chen"
    
    example_text = f"""
{CEO_NAME}, Chief Executive Officer

# C-Suite
Alex Rodriguez, Chief Technology Officer, {CEO_NAME}
Mira Patel, Chief Product Officer, {CEO_NAME}
James Wilson, Chief Marketing Officer, {CEO_NAME}
David Klein, Chief Revenue Officer, {CEO_NAME}
Emily Johnson, Chief People Officer, {CEO_NAME}
Michael Chang, Chief Financial Officer, {CEO_NAME}
Lauren Gonzalez, General Counsel, {CEO_NAME}
Tom Watkins, Chief Customer Officer, {CEO_NAME}
Rajesh Kumar, Chief Information Officer, {CEO_NAME}

# Engineering Leadership
Kevin Zhang, SVP Engineering, Alex Rodriguez
Lisa Wong, VP Frontend Engineering, Kevin Zhang
John Smith, VP Backend Engineering, Kevin Zhang
Maria Santos, VP Infrastructure, Kevin Zhang
Omar Hassan, VP Security, Kevin Zhang
Priya Nair, VP Data Engineering, Kevin Zhang
Wei Chen, VP Quality Assurance, Kevin Zhang

# Product Leadership
Samantha Lee, SVP Product, Mira Patel
Daniel Okafor, VP Product Management, Samantha Lee
Sophia Garcia, VP Product Design, Samantha Lee
Taro Yamamoto, VP User Research, Samantha Lee
Andrew Kim, VP Product Analytics, Samantha Lee

# Marketing Leadership
Nicole Dubois, SVP Marketing, James Wilson
Carlos Rivera, VP Brand Marketing, Nicole Dubois
Emma Thompson, VP Product Marketing, Nicole Dubois
Liam O'Brien, VP Growth Marketing, Nicole Dubois
Zara Ahmed, VP Marketing Operations, Nicole Dubois

# Sales Leadership
Robert Jackson, SVP Global Sales, David Klein
Sophie Martin, VP Inside Sales, Robert Jackson
Marcus Chen, VP Field Sales, Robert Jackson
Ava Williams, VP Solutions Engineering, Robert Jackson
Raj Patel, VP Sales Operations, Robert Jackson

# Customer Success Leadership
Jennifer Murphy, SVP Customer Success, Tom Watkins
Hiroshi Tanaka, VP Customer Support, Jennifer Murphy
Olivia Bennett, VP Customer Education, Jennifer Murphy
Ryan Campbell, VP Account Management, Jennifer Murphy
"""
    return example_text.strip()

if __name__ == "__main__":
    generate_enterprise_data()