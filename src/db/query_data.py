#!/usr/bin/env python3
"""
Database Query Examples for Organization Alignment Data

This script provides simple examples of querying the organization database.
"""

import os
import sys
import logging
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker, joinedload, aliased

# Import models from the src package
from src.db.models import (
    Base, Organization, Department, Position, Employee, Team, TeamMember,
    CompanyObjective, DepartmentObjective, TeamObjective, KeyResult,
    OKRUpdate, TeamDependency, StatusUpdate, ResourceAllocation,
    get_engine
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class OrganizationDatabase:
    """Class to handle database queries for the organization data."""
    
    def __init__(self, db_path=None):
        """Initialize the database connection."""
        self.engine = get_engine(db_path) if db_path else get_engine()
        self.Session = sessionmaker(bind=self.engine)
    
    def employee_count_by_department(self):
        """Get employee count by department."""
        session = self.Session()
        try:
            # Join departments with employees and group by department
            results = session.query(
                Department.department_name,
                func.count(Employee.employee_id).label('employee_count')
            ).join(
                Employee, Department.department_id == Employee.department_id
            ).group_by(
                Department.department_name
            ).order_by(
                desc('employee_count')
            ).all()
            
            print("\nEmployee Count by Department:")
            print("-----------------------------")
            for dept_name, count in results:
                print(f"{dept_name}: {count} employees")
            
            return results
        finally:
            session.close()
    
    def okr_status_by_level(self):
        """Get OKR status counts by level (company, department, team)."""
        session = self.Session()
        try:
            # Company OKR status
            company_status = session.query(
                CompanyObjective.status,
                func.count(CompanyObjective.objective_id).label('count')
            ).group_by(
                CompanyObjective.status
            ).all()
            
            # Department OKR status
            dept_status = session.query(
                DepartmentObjective.status,
                func.count(DepartmentObjective.department_objective_id).label('count')
            ).group_by(
                DepartmentObjective.status
            ).all()
            
            # Team OKR status
            team_status = session.query(
                TeamObjective.status,
                func.count(TeamObjective.team_objective_id).label('count')
            ).group_by(
                TeamObjective.status
            ).all()
            
            print("\nOKR Status by Level:")
            print("-------------------")
            
            print("Company Level:")
            for status, count in company_status:
                print(f"  {status}: {count}")
            
            print("\nDepartment Level:")
            for status, count in dept_status:
                print(f"  {status}: {count}")
            
            print("\nTeam Level:")
            for status, count in team_status:
                print(f"  {status}: {count}")
            
            return {
                'company': company_status,
                'department': dept_status,
                'team': team_status
            }
        finally:
            session.close()
    
    def key_result_progress(self):
        """Get progress of key results for company objectives."""
        session = self.Session()
        try:
            # Get key results with objective information
            results = session.query(
                CompanyObjective.objective_statement,
                CompanyObjective.priority,
                func.avg(KeyResult.current_value / KeyResult.target_value * 100).label('avg_progress')
            ).join(
                KeyResult, CompanyObjective.objective_id == KeyResult.objective_id
            ).group_by(
                CompanyObjective.objective_id
            ).order_by(
                CompanyObjective.priority
            ).all()
            
            print("\nKey Result Progress by Company Objective:")
            print("---------------------------------------")
            for objective, priority, progress in results:
                print(f"{objective} (Priority: {priority}): {progress:.1f}% complete")
            
            return results
        finally:
            session.close()
    
    def resource_allocation_by_priority(self):
        """Get resource allocation by priority level."""
        session = self.Session()
        try:
            # Get resource allocation grouped by priority
            results = session.query(
                DepartmentObjective.priority,
                ResourceAllocation.resource_type,
                func.sum(ResourceAllocation.allocated_amount).label('total_allocated')
            ).join(
                ResourceAllocation, 
                DepartmentObjective.department_objective_id == ResourceAllocation.objective_id
            ).group_by(
                DepartmentObjective.priority,
                ResourceAllocation.resource_type
            ).order_by(
                DepartmentObjective.priority,
                ResourceAllocation.resource_type
            ).all()
            
            print("\nResource Allocation by Priority:")
            print("------------------------------")
            for priority, resource_type, total in results:
                if resource_type == 'Budget':
                    print(f"{priority} Priority - {resource_type}: ${total:,}")
                else:
                    print(f"{priority} Priority - {resource_type}: {total}")
            
            return results
        finally:
            session.close()
    
    def team_dependencies(self):
        """Get team dependencies information."""
        session = self.Session()
        try:
            # Create an alias for the dependency team
            DependencyTeam = aliased(Team)
            
            # Get dependencies with team information
            results = session.query(
                Team.team_name.label('dependent_team'),
                Team.project_name.label('dependent_project'),
                TeamDependency.description,
                TeamDependency.criticality,
                TeamDependency.status
            ).join(
                TeamDependency, Team.team_id == TeamDependency.dependent_team_id
            ).join(
                DependencyTeam, TeamDependency.dependency_team_id == DependencyTeam.team_id
            ).order_by(
                TeamDependency.criticality
            ).limit(5).all()
            
            print("\nSample Team Dependencies:")
            print("-----------------------")
            for dep_team, dep_project, desc, criticality, status in results:
                print(f"{dep_team} ({dep_project}): {desc}")
                print(f"  Criticality: {criticality}, Status: {status}\n")
            
            return results
        finally:
            session.close()
    
    def run_all_queries(self):
        """Run all sample queries."""
        logger.info("Running sample queries on the organization database")
        
        self.employee_count_by_department()
        self.okr_status_by_level()
        self.key_result_progress()
        self.resource_allocation_by_priority()
        self.team_dependencies()
        
        logger.info("Query examples completed")


if __name__ == "__main__":
    # Use the default path from models
    db = OrganizationDatabase()
    db.run_all_queries()