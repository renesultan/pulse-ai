from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB

# Association tables for many-to-many relationships
project_members = db.Table('project_members',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

secondary_reports = db.Table('secondary_reports',
    db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True),
    db.Column('manager_id', db.Integer, db.ForeignKey('employee.id'), primary_key=True)
)

class Organization(db.Model):
    """Model representing an organization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    headquarters = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    departments = db.relationship('Department', backref='organization', lazy=True, cascade="all, delete-orphan")
    regions = db.relationship('Region', backref='organization', lazy=True, cascade="all, delete-orphan")
    employees = db.relationship('Employee', backref='organization', lazy=True, cascade="all, delete-orphan")
    projects = db.relationship('Project', backref='organization', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Organization {self.name}>'

class Region(db.Model):
    """Model representing geographic regions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Americas, EMEA, APAC, etc.
    code = db.Column(db.String(20), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    locations = db.relationship('Location', backref='region', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Region {self.name}>'

class Location(db.Model):
    """Model representing office locations"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # HQ, Remote, Regional Office
    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    timezone = db.Column(db.String(50), nullable=True)
    is_headquarters = db.Column(db.Boolean, default=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    employees = db.relationship('Employee', backref='location', lazy=True)
    
    def __repr__(self):
        return f'<Location {self.name}>'

class Department(db.Model):
    """Model representing a department within an organization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(20), nullable=True)  # Department code (ENG, MKT, etc.)
    description = db.Column(db.Text, nullable=True)
    cost_center = db.Column(db.String(50), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)  # For nested departments
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    employees = db.relationship('Employee', backref='department', lazy=True)
    sub_departments = db.relationship('Department', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Project(db.Model):
    """Model representing cross-functional projects"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    code = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=True)  # Active, Completed, On Hold
    priority = db.Column(db.String(20), nullable=True)  # High, Medium, Low
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)  # Executive sponsor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('Employee', secondary=project_members, lazy='subquery',
                              backref=db.backref('projects', lazy=True))
    
    def __repr__(self):
        return f'<Project {self.name}>'

class Employee(db.Model):
    """Model representing an employee within an organization"""
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), nullable=True)  # Internal employee ID
    name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    level = db.Column(db.String(50), nullable=True)  # Seniority level
    cost_center = db.Column(db.String(50), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=True)
    primary_manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    direct_reports = db.relationship('Employee', 
                                    backref=db.backref('primary_manager', remote_side=[id]),
                                    foreign_keys=[primary_manager_id],
                                    lazy=True)
    secondary_managers = db.relationship('Employee',
                                       secondary=secondary_reports,
                                       primaryjoin=(id == secondary_reports.c.employee_id),
                                       secondaryjoin=(id == secondary_reports.c.manager_id),
                                       backref=db.backref('dotted_line_reports', lazy=True),
                                       lazy=True)
    # Project sponsorships
    sponsored_projects = db.relationship('Project', backref='sponsor', lazy=True, foreign_keys=[Project.sponsor_id])
    
    def __repr__(self):
        return f'<Employee {self.name} - {self.title}>'

class OrgChart(db.Model):
    """Model representing a saved organization chart"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)  # For project-specific charts
    view_type = db.Column(db.String(50), nullable=False, default='hierarchical')  # hierarchical, matrix, project
    chart_data = db.Column(JSONB, nullable=True)  # JSON representation of the hierarchy
    display_options = db.Column(JSONB, nullable=True)  # JSON for display settings
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    organization = db.relationship('Organization', backref='org_charts', lazy=True)
    department = db.relationship('Department', backref='org_charts', lazy=True)
    project = db.relationship('Project', backref='org_charts', lazy=True)
    
    def __repr__(self):
        return f'<OrgChart {self.name}>'