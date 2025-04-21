"""
SQLAlchemy models for organization alignment data.

This module defines the database schema for the organizational alignment data,
mirroring the structure of the CSV files.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Organization(Base):
    """Organization model representing a company entity."""
    
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    domain = Column(String(255), nullable=False)
    
    # Relationships
    departments = relationship("Department", back_populates="organization")
    employees = relationship("Employee", back_populates="organization")


class Department(Base):
    """Department model representing company departments."""
    
    __tablename__ = "departments"
    
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(255), nullable=False)
    department_head_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    parent_department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    cost_center_code = Column(String(50))
    location = Column(String(255))
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="departments")
    parent_department = relationship("Department", remote_side=[department_id])
    employees = relationship("Employee", foreign_keys="Employee.department_id", back_populates="department")
    department_head = relationship("Employee", foreign_keys=[department_head_id])
    department_objectives = relationship("DepartmentObjective", back_populates="department")


class Position(Base):
    """Position model representing job positions within the company."""
    
    __tablename__ = "positions"
    
    position_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    level = Column(String(50))
    salary_band_minimum = Column(Integer)
    salary_band_maximum = Column(Integer)
    
    # Relationships
    department = relationship("Department")
    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    """Employee model representing individuals within the company."""
    
    __tablename__ = "employees"
    
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hire_date = Column(Date)
    job_title = Column(String(255))
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.position_id"), nullable=True)
    manager_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=True)
    employment_status = Column(String(50))
    location = Column(String(255))
    salary = Column(Integer)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Relationships
    organization = relationship("Organization", back_populates="employees")
    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    position = relationship("Position", back_populates="employees")
    manager = relationship("Employee", remote_side=[employee_id])
    team_memberships = relationship("TeamMember", back_populates="employee")
    owned_company_objectives = relationship("CompanyObjective", foreign_keys="CompanyObjective.owner_id", back_populates="owner")
    owned_department_objectives = relationship("DepartmentObjective", foreign_keys="DepartmentObjective.owner_id", back_populates="owner")
    owned_team_objectives = relationship("TeamObjective", foreign_keys="TeamObjective.owner_id", back_populates="owner")
    owned_key_results = relationship("KeyResult", foreign_keys="KeyResult.owner_id", back_populates="owner")


class Team(Base):
    """Team model representing project teams within the company."""
    
    __tablename__ = "teams"
    
    team_id = Column(Integer, primary_key=True)
    team_name = Column(String(255), nullable=False)
    team_lead_id = Column(Integer, ForeignKey("employees.employee_id"))
    project_name = Column(String(255))
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    
    # Relationships
    team_lead = relationship("Employee")
    members = relationship("TeamMember", back_populates="team")
    team_objectives = relationship("TeamObjective", back_populates="team")
    dependent_teams = relationship(
        "TeamDependency",
        foreign_keys="TeamDependency.dependent_team_id",
        back_populates="dependent_team"
    )
    dependency_for_teams = relationship(
        "TeamDependency",
        foreign_keys="TeamDependency.dependency_team_id",
        back_populates="dependency_team"
    )


class TeamMember(Base):
    """TeamMember model representing the relationship between teams and employees."""
    
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.employee_id"), nullable=False)
    role_in_team = Column(String(255))
    allocation_percentage = Column(Integer)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    employee = relationship("Employee", back_populates="team_memberships")


class CompanyObjective(Base):
    """CompanyObjective model representing company-level OKRs."""
    
    __tablename__ = "company_okrs"
    
    objective_id = Column(Integer, primary_key=True)
    objective_statement = Column(String(255), nullable=False)
    timeframe = Column(String(50))
    owner_id = Column(Integer, ForeignKey("employees.employee_id"))
    status = Column(String(50))
    priority = Column(String(50))
    description = Column(Text)
    
    # Relationships
    owner = relationship("Employee", foreign_keys=[owner_id], back_populates="owned_company_objectives")
    key_results = relationship("KeyResult", back_populates="objective")
    department_objectives = relationship("DepartmentObjective", back_populates="parent_objective")


class DepartmentObjective(Base):
    """DepartmentObjective model representing department-level OKRs."""
    
    __tablename__ = "department_okrs"
    
    department_objective_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    objective_statement = Column(String(255), nullable=False)
    parent_objective_id = Column(Integer, ForeignKey("company_okrs.objective_id"), nullable=True)
    timeframe = Column(String(50))
    owner_id = Column(Integer, ForeignKey("employees.employee_id"))
    status = Column(String(50))
    priority = Column(String(50))
    
    # Relationships
    department = relationship("Department", back_populates="department_objectives")
    parent_objective = relationship("CompanyObjective", back_populates="department_objectives")
    owner = relationship("Employee", foreign_keys=[owner_id], back_populates="owned_department_objectives")
    team_objectives = relationship("TeamObjective", back_populates="department_objective")
    resource_allocations = relationship("ResourceAllocation", back_populates="objective")


class TeamObjective(Base):
    """TeamObjective model representing team-level OKRs."""
    
    __tablename__ = "team_okrs"
    
    team_objective_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    objective_statement = Column(String(255), nullable=False)
    department_objective_id = Column(Integer, ForeignKey("department_okrs.department_objective_id"), nullable=True)
    timeframe = Column(String(50))
    owner_id = Column(Integer, ForeignKey("employees.employee_id"))
    status = Column(String(50))
    priority = Column(String(50))
    
    # Relationships
    team = relationship("Team", back_populates="team_objectives")
    department_objective = relationship("DepartmentObjective", back_populates="team_objectives")
    owner = relationship("Employee", foreign_keys=[owner_id], back_populates="owned_team_objectives")


class KeyResult(Base):
    """KeyResult model representing measurable key results for objectives."""
    
    __tablename__ = "key_results"
    
    key_result_id = Column(Integer, primary_key=True)
    objective_id = Column(Integer, ForeignKey("company_okrs.objective_id"), nullable=False)
    description = Column(String(255), nullable=False)
    target_value = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    unit_of_measurement = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    owner_id = Column(Integer, ForeignKey("employees.employee_id"))
    last_updated = Column(Date)
    confidence_score = Column(Integer)
    
    # Relationships
    objective = relationship("CompanyObjective", back_populates="key_results")
    owner = relationship("Employee", foreign_keys=[owner_id], back_populates="owned_key_results")
    updates = relationship("OKRUpdate", back_populates="key_result")


class OKRUpdate(Base):
    """OKRUpdate model tracking historical updates to key results."""
    
    __tablename__ = "okr_updates"
    
    update_id = Column(Integer, primary_key=True)
    key_result_id = Column(Integer, ForeignKey("key_results.key_result_id"), nullable=False)
    previous_value = Column(Float)
    new_value = Column(Float)
    update_date = Column(Date)
    confidence_score = Column(Integer)
    notes = Column(Text)
    updater_id = Column(Integer, ForeignKey("employees.employee_id"))
    
    # Relationships
    key_result = relationship("KeyResult", back_populates="updates")
    updater = relationship("Employee")


class TeamDependency(Base):
    """TeamDependency model representing dependencies between teams."""
    
    __tablename__ = "cross_team_dependencies"
    
    dependency_id = Column(Integer, primary_key=True)
    dependent_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    dependency_team_id = Column(Integer, ForeignKey("teams.team_id"), nullable=False)
    description = Column(Text)
    due_date = Column(Date)
    status = Column(String(50))
    criticality = Column(String(50))
    impact_description = Column(Text)
    
    # Relationships
    dependent_team = relationship("Team", foreign_keys=[dependent_team_id], back_populates="dependent_teams")
    dependency_team = relationship("Team", foreign_keys=[dependency_team_id], back_populates="dependency_for_teams")


class StatusUpdate(Base):
    """StatusUpdate model for team and department status reports."""
    
    __tablename__ = "status_updates"
    
    update_id = Column(Integer, primary_key=True)
    entity_id = Column(Integer, nullable=False)
    entity_type = Column(String(50), nullable=False)
    report_date = Column(Date)
    status = Column(String(50))
    summary = Column(Text)
    blockers = Column(Text)
    next_steps = Column(Text)
    author_id = Column(Integer, ForeignKey("employees.employee_id"))
    
    # Relationships
    author = relationship("Employee")


class ResourceAllocation(Base):
    """ResourceAllocation model for tracking resources assigned to objectives."""
    
    __tablename__ = "resource_allocation"
    
    allocation_id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"), nullable=False)
    objective_id = Column(Integer, ForeignKey("department_okrs.department_objective_id"), nullable=False)
    resource_type = Column(String(50), nullable=False)
    allocated_amount = Column(Integer, nullable=False)
    timeframe = Column(String(50))
    actual_usage = Column(Integer)
    variance_explanation = Column(Text)
    
    # Relationships
    department = relationship("Department")
    objective = relationship("DepartmentObjective", back_populates="resource_allocations")


def get_engine(db_path="sqlite:///data/organization.db"):
    """Create and return a SQLAlchemy engine instance."""
    return create_engine(db_path)


def create_tables(engine):
    """Create all database tables."""
    Base.metadata.create_all(engine)