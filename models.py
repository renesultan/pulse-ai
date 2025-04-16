from app import db
from datetime import datetime

class Organization(db.Model):
    """Model representing an organization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    departments = db.relationship('Department', backref='organization', lazy=True, cascade="all, delete-orphan")
    employees = db.relationship('Employee', backref='organization', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Organization {self.name}>'

class Department(db.Model):
    """Model representing a department within an organization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    employees = db.relationship('Employee', backref='department', lazy=True)
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Employee(db.Model):
    """Model representing an employee within an organization"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    reports_to_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    direct_reports = db.relationship('Employee', backref=db.backref('manager', remote_side=[id]), lazy=True)
    
    def __repr__(self):
        return f'<Employee {self.name} - {self.title}>'

class OrgChart(db.Model):
    """Model representing a saved organization chart"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    reporting_structure = db.Column(db.Text, nullable=True)  # JSON representation of the hierarchy
    reporting_line_type = db.Column(db.String(50), nullable=True)  # hierarchical, matrix, flat
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = db.relationship('Organization', backref='org_charts', lazy=True)
    department = db.relationship('Department', backref='org_charts', lazy=True)
    
    def __repr__(self):
        return f'<OrgChart {self.name}>'