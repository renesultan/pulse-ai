#!/usr/bin/env python3
"""
CSV Import Script for Organization Alignment Data

This script imports the synthetic CSV data into the SQLite database.
"""

import os
import sys
import csv
import logging
import pandas as pd
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models from the src package
from src.db.models import (
    Base, Organization, Department, Position, Employee, Team, TeamMember,
    CompanyObjective, DepartmentObjective, TeamObjective, KeyResult,
    OKRUpdate, TeamDependency, StatusUpdate, ResourceAllocation,
    get_engine, create_tables
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('import_data.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DataImporter:
    """Class to handle importing CSV data into the database."""
    
    def __init__(self, data_dir, db_path="sqlite:///organization.db"):
        """Initialize the importer with data directory and database path."""
        self.data_dir = Path(data_dir)
        self.db_path = db_path
        self.engine = get_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        
        # Ensure database tables exist
        create_tables(self.engine)
        
        # Dictionary to track imported data
        self.imported_counts = {}
    
    def _parse_date(self, date_str):
        """Parse date string to Python date object."""
        if not date_str or pd.isna(date_str):
            return None
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            logger.warning(f"Invalid date format: {date_str}")
            return None
    
    def _get_csv_files(self):
        """Get a list of all CSV files in the data directory."""
        return list(self.data_dir.glob('*.csv'))
    
    def import_organization(self):
        """Import organization data."""
        session = self.Session()
        try:
            # Check if organization already exists
            if session.query(Organization).count() == 0:
                # Create Horizon Technologies organization
                org = Organization(
                    id=1,
                    name="Horizon Technologies",
                    domain="horizontech.com"
                )
                session.add(org)
                session.commit()
                logger.info("Created organization: Horizon Technologies")
            else:
                logger.info("Organization already exists, skipping creation")
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing organization: {e}")
        finally:
            session.close()
    
    def import_departments(self):
        """Import department data from CSV."""
        file_path = self.data_dir / 'departments.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if department already exists
                existing = session.query(Department).filter_by(
                    department_id=row['department_id']).first()
                
                if existing:
                    logger.debug(f"Department already exists: {row['department_name']}")
                    continue
                
                # Create new department
                department = Department(
                    department_id=row['department_id'],
                    department_name=row['department_name'],
                    department_head_id=row['department_head_id'] if not pd.isna(row['department_head_id']) else None,
                    parent_department_id=row['parent_department_id'] if not pd.isna(row['parent_department_id']) else None,
                    cost_center_code=row['cost_center_code'],
                    location=row['location'],
                    organization_id=1  # Assign to Horizon Technologies
                )
                session.add(department)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} departments")
            self.imported_counts['departments'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing departments: {e}")
        finally:
            session.close()
    
    def import_positions(self):
        """Import position data from CSV."""
        file_path = self.data_dir / 'positions.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if position already exists
                existing = session.query(Position).filter_by(
                    position_id=row['position_id']).first()
                
                if existing:
                    logger.debug(f"Position already exists: {row['title']}")
                    continue
                
                # Create new position
                position = Position(
                    position_id=row['position_id'],
                    title=row['title'],
                    department_id=row['department_id'] if not pd.isna(row['department_id']) else None,
                    level=row['level'],
                    salary_band_minimum=row['salary_band_minimum'],
                    salary_band_maximum=row['salary_band_maximum']
                )
                session.add(position)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} positions")
            self.imported_counts['positions'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing positions: {e}")
        finally:
            session.close()
    
    def import_employees(self):
        """Import employee data from CSV."""
        file_path = self.data_dir / 'employees.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if employee already exists
                existing = session.query(Employee).filter_by(
                    employee_id=row['employee_id']).first()
                
                if existing:
                    logger.debug(f"Employee already exists: {row['first_name']} {row['last_name']}")
                    continue
                
                # Create new employee
                employee = Employee(
                    employee_id=row['employee_id'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    hire_date=self._parse_date(row['hire_date']),
                    job_title=row['job_title'],
                    department_id=row['department_id'] if not pd.isna(row['department_id']) else None,
                    manager_id=row['manager_id'] if not pd.isna(row['manager_id']) else None,
                    employment_status=row['employment_status'],
                    location=row['location'],
                    salary=row['salary'],
                    organization_id=1  # Assign to Horizon Technologies
                )
                session.add(employee)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} employees")
            self.imported_counts['employees'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing employees: {e}")
        finally:
            session.close()
    
    def import_teams(self):
        """Import team data from CSV."""
        file_path = self.data_dir / 'teams.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if team already exists
                existing = session.query(Team).filter_by(
                    team_id=row['team_id']).first()
                
                if existing:
                    logger.debug(f"Team already exists: {row['team_name']}")
                    continue
                
                # Create new team
                team = Team(
                    team_id=row['team_id'],
                    team_name=row['team_name'],
                    team_lead_id=row['team_lead_id'],
                    project_name=row['project_name'],
                    start_date=self._parse_date(row['start_date']),
                    end_date=self._parse_date(row['end_date']) if 'end_date' in row and not pd.isna(row['end_date']) else None
                )
                session.add(team)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} teams")
            self.imported_counts['teams'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing teams: {e}")
        finally:
            session.close()
    
    def import_team_members(self):
        """Import team member data from CSV."""
        file_path = self.data_dir / 'team_members.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for i, row in df.iterrows():
                # Create a unique ID for the team member
                member_id = i + 1
                
                # Check if team member already exists (using team_id and employee_id)
                existing = session.query(TeamMember).filter_by(
                    team_id=row['team_id'],
                    employee_id=row['employee_id']
                ).first()
                
                if existing:
                    logger.debug(f"Team member already exists: Team {row['team_id']}, Employee {row['employee_id']}")
                    continue
                
                # Create new team member
                team_member = TeamMember(
                    id=member_id,
                    team_id=row['team_id'],
                    employee_id=row['employee_id'],
                    role_in_team=row['role_in_team'],
                    allocation_percentage=row['allocation_percentage']
                )
                session.add(team_member)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} team members")
            self.imported_counts['team_members'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing team members: {e}")
        finally:
            session.close()
    
    def import_company_okrs(self):
        """Import company OKR data from CSV."""
        file_path = self.data_dir / 'company_okrs.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if objective already exists
                existing = session.query(CompanyObjective).filter_by(
                    objective_id=row['objective_id']).first()
                
                if existing:
                    logger.debug(f"Company objective already exists: {row['objective_statement']}")
                    continue
                
                # Create new company objective
                objective = CompanyObjective(
                    objective_id=row['objective_id'],
                    objective_statement=row['objective_statement'],
                    timeframe=row['timeframe'],
                    owner_id=row['owner_id'],
                    status=row['status'],
                    priority=row['priority'],
                    description=row['description'] if 'description' in row else None
                )
                session.add(objective)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} company OKRs")
            self.imported_counts['company_okrs'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing company OKRs: {e}")
        finally:
            session.close()
    
    def import_department_okrs(self):
        """Import department OKR data from CSV."""
        file_path = self.data_dir / 'department_okrs.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if objective already exists
                existing = session.query(DepartmentObjective).filter_by(
                    department_objective_id=row['department_objective_id']).first()
                
                if existing:
                    logger.debug(f"Department objective already exists: {row['objective_statement']}")
                    continue
                
                # Create new department objective
                objective = DepartmentObjective(
                    department_objective_id=row['department_objective_id'],
                    department_id=row['department_id'],
                    objective_statement=row['objective_statement'],
                    parent_objective_id=row['parent_objective_id'] if not pd.isna(row['parent_objective_id']) else None,
                    timeframe=row['timeframe'],
                    owner_id=row['owner_id'],
                    status=row['status'],
                    priority=row['priority']
                )
                session.add(objective)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} department OKRs")
            self.imported_counts['department_okrs'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing department OKRs: {e}")
        finally:
            session.close()
    
    def import_team_okrs(self):
        """Import team OKR data from CSV."""
        file_path = self.data_dir / 'team_okrs.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if objective already exists
                existing = session.query(TeamObjective).filter_by(
                    team_objective_id=row['team_objective_id']).first()
                
                if existing:
                    logger.debug(f"Team objective already exists: {row['objective_statement']}")
                    continue
                
                # Create new team objective
                objective = TeamObjective(
                    team_objective_id=row['team_objective_id'],
                    team_id=row['team_id'],
                    objective_statement=row['objective_statement'],
                    department_objective_id=row['department_objective_id'] if not pd.isna(row['department_objective_id']) else None,
                    timeframe=row['timeframe'],
                    owner_id=row['owner_id'],
                    status=row['status'],
                    priority=row['priority']
                )
                session.add(objective)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} team OKRs")
            self.imported_counts['team_okrs'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing team OKRs: {e}")
        finally:
            session.close()
    
    def import_key_results(self):
        """Import key result data from CSV."""
        file_path = self.data_dir / 'key_results.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if key result already exists
                existing = session.query(KeyResult).filter_by(
                    key_result_id=row['key_result_id']).first()
                
                if existing:
                    logger.debug(f"Key result already exists: {row['description']}")
                    continue
                
                # Create new key result
                key_result = KeyResult(
                    key_result_id=row['key_result_id'],
                    objective_id=row['objective_id'],
                    description=row['description'],
                    target_value=row['target_value'],
                    current_value=row['current_value'],
                    unit_of_measurement=row['unit_of_measurement'],
                    start_date=self._parse_date(row['start_date']),
                    end_date=self._parse_date(row['end_date']),
                    owner_id=row['owner_id'],
                    last_updated=self._parse_date(row['last_updated']),
                    confidence_score=row['confidence_score']
                )
                session.add(key_result)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} key results")
            self.imported_counts['key_results'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing key results: {e}")
        finally:
            session.close()
    
    def import_okr_updates(self):
        """Import OKR update data from CSV."""
        file_path = self.data_dir / 'okr_updates.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if update already exists
                existing = session.query(OKRUpdate).filter_by(
                    update_id=row['update_id']).first()
                
                if existing:
                    logger.debug(f"OKR update already exists: {row['update_id']}")
                    continue
                
                # Create new OKR update
                update = OKRUpdate(
                    update_id=row['update_id'],
                    key_result_id=row['key_result_id'],
                    previous_value=row['previous_value'],
                    new_value=row['new_value'],
                    update_date=self._parse_date(row['update_date']),
                    confidence_score=row['confidence_score'],
                    notes=row['notes'],
                    updater_id=row['updater_id']
                )
                session.add(update)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} OKR updates")
            self.imported_counts['okr_updates'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing OKR updates: {e}")
        finally:
            session.close()
    
    def import_team_dependencies(self):
        """Import team dependency data from CSV."""
        file_path = self.data_dir / 'cross_team_dependencies.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if dependency already exists
                existing = session.query(TeamDependency).filter_by(
                    dependency_id=row['dependency_id']).first()
                
                if existing:
                    logger.debug(f"Team dependency already exists: {row['dependency_id']}")
                    continue
                
                # Create new team dependency
                dependency = TeamDependency(
                    dependency_id=row['dependency_id'],
                    dependent_team_id=row['dependent_team_id'],
                    dependency_team_id=row['dependency_team_id'],
                    description=row['description'],
                    due_date=self._parse_date(row['due_date']),
                    status=row['status'],
                    criticality=row['criticality'],
                    impact_description=row['impact_description']
                )
                session.add(dependency)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} team dependencies")
            self.imported_counts['team_dependencies'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing team dependencies: {e}")
        finally:
            session.close()
    
    def import_status_updates(self):
        """Import status update data from CSV."""
        file_path = self.data_dir / 'status_updates.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if status update already exists
                existing = session.query(StatusUpdate).filter_by(
                    update_id=row['update_id']).first()
                
                if existing:
                    logger.debug(f"Status update already exists: {row['update_id']}")
                    continue
                
                # Create new status update
                update = StatusUpdate(
                    update_id=row['update_id'],
                    entity_id=row['entity_id'],
                    entity_type=row['entity_type'],
                    report_date=self._parse_date(row['report_date']),
                    status=row['status'],
                    summary=row['summary'],
                    blockers=row['blockers'],
                    next_steps=row['next_steps'],
                    author_id=row['author_id']
                )
                session.add(update)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} status updates")
            self.imported_counts['status_updates'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing status updates: {e}")
        finally:
            session.close()
    
    def import_resource_allocations(self):
        """Import resource allocation data from CSV."""
        file_path = self.data_dir / 'resource_allocation.csv'
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return
        
        session = self.Session()
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            count = 0
            
            for _, row in df.iterrows():
                # Check if resource allocation already exists
                existing = session.query(ResourceAllocation).filter_by(
                    allocation_id=row['allocation_id']).first()
                
                if existing:
                    logger.debug(f"Resource allocation already exists: {row['allocation_id']}")
                    continue
                
                # Create new resource allocation
                allocation = ResourceAllocation(
                    allocation_id=row['allocation_id'],
                    department_id=row['department_id'],
                    objective_id=row['objective_id'],
                    resource_type=row['resource_type'],
                    allocated_amount=row['allocated_amount'],
                    timeframe=row['timeframe'],
                    actual_usage=row['actual_usage'],
                    variance_explanation=row['variance_explanation']
                )
                session.add(allocation)
                count += 1
            
            session.commit()
            logger.info(f"Imported {count} resource allocations")
            self.imported_counts['resource_allocations'] = count
            
        except Exception as e:
            session.rollback()
            logger.error(f"Error importing resource allocations: {e}")
        finally:
            session.close()
    
    def import_all_data(self):
        """Import all data from CSVs to database."""
        logger.info(f"Starting import from {self.data_dir} to {self.db_path}")
        
        # Import organization first (as it's a dependency for many tables)
        self.import_organization()
        
        # Import in order of dependencies
        self.import_departments()
        self.import_positions()
        self.import_employees()
        self.import_teams()
        self.import_team_members()
        self.import_company_okrs()
        self.import_department_okrs()
        self.import_team_okrs()
        self.import_key_results()
        self.import_okr_updates()
        self.import_team_dependencies()
        self.import_status_updates()
        self.import_resource_allocations()
        
        # Log summary
        logger.info("Import completed. Summary:")
        for table, count in self.imported_counts.items():
            logger.info(f"  {table}: {count} records")


if __name__ == "__main__":
    # Default data directory
    script_dir = Path(__file__).parent.parent.parent  # Get project root
    data_dir = script_dir / "synthetic_data"
    
    # Create the database in the data directory
    db_path = "sqlite:///data/organization.db"
    
    # Create and run the importer
    importer = DataImporter(data_dir, db_path)
    importer.import_all_data()