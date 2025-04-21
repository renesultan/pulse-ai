#!/usr/bin/env python3
"""
Database Validation Script for Organization Alignment Data

This script validates the SQLite database structure and data integrity.
"""

import os
import sys
import logging
from sqlalchemy import inspect, func, text
from sqlalchemy.orm import sessionmaker
from typing import Dict, List, Tuple, Any

# Add parent directory to path to import models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.models import (
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
        logging.FileHandler('validate_database.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class DatabaseValidator:
    """Class to handle database validation."""
    
    def __init__(self, db_path="sqlite:///organization.db"):
        """Initialize the validator with database path."""
        self.db_path = db_path
        self.engine = get_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)
        self.inspector = inspect(self.engine)
        
        # Track validation results
        self.validation_results = {
            "schema": {},
            "relationships": {},
            "data_integrity": {},
            "consistency": {}
        }
        
        # Expected table counts based on CSV files
        self.expected_counts = {
            "organizations": 1,  # Just Horizon Technologies
            "departments": 16,
            "positions": 77,
            "employees": 521,
            "teams": 15,
            "team_members": 118,
            "company_okrs": 7,
            "department_okrs": 29,
            "team_okrs": 45,
            "key_results": 22,
            "okr_updates": 63,
            "cross_team_dependencies": 22,
            "status_updates": 76,
            "resource_allocation": 58
        }
    
    def validate_schema(self) -> bool:
        """Validate the database schema against expected tables and columns."""
        logger.info("Validating database schema...")
        
        # Get all table names from SQLAlchemy models
        model_tables = {table.__tablename__ for table in Base.__subclasses__()}
        
        # Get actual tables in database
        db_tables = set(self.inspector.get_table_names())
        
        # Check if all expected tables exist
        missing_tables = model_tables - db_tables
        if missing_tables:
            logger.error(f"Missing tables in database: {missing_tables}")
            self.validation_results["schema"]["missing_tables"] = list(missing_tables)
            return False
        
        # Check each table's columns
        all_columns_valid = True
        for table_name in model_tables:
            # Get columns from database
            db_columns = {col["name"] for col in self.inspector.get_columns(table_name)}
            
            # Get expected columns from model
            model_class = next((cls for cls in Base.__subclasses__() 
                             if cls.__tablename__ == table_name), None)
            if not model_class:
                logger.error(f"Could not find model class for table {table_name}")
                continue
                
            model_columns = set(model_class.__table__.columns.keys())
            
            # Check for missing columns
            missing_columns = model_columns - db_columns
            if missing_columns:
                logger.error(f"Table {table_name} is missing columns: {missing_columns}")
                self.validation_results["schema"][f"{table_name}_missing_columns"] = list(missing_columns)
                all_columns_valid = False
        
        if all_columns_valid:
            logger.info("✓ Schema validation passed")
            self.validation_results["schema"]["status"] = "passed"
            return True
        else:
            logger.error("✗ Schema validation failed")
            self.validation_results["schema"]["status"] = "failed"
            return False
    
    def validate_relationships(self) -> bool:
        """Validate foreign key relationships between tables."""
        logger.info("Validating table relationships...")
        session = self.Session()
        
        relationship_tests = [
            # Test that all departments with parent_department_id reference valid departments
            {
                "name": "department_parent_references",
                "query": session.query(Department).filter(
                    Department.parent_department_id.isnot(None)
                ).all(),
                "validation": lambda depts: all(
                    session.query(Department).filter_by(
                        department_id=dept.parent_department_id
                    ).first() is not None for dept in depts
                )
            },
            # Test that all employees with department_id reference valid departments
            {
                "name": "employee_department_references",
                "query": session.query(Employee).filter(
                    Employee.department_id.isnot(None)
                ).all(),
                "validation": lambda emps: all(
                    session.query(Department).filter_by(
                        department_id=emp.department_id
                    ).first() is not None for emp in emps
                )
            },
            # Test that all team members reference valid teams and employees
            {
                "name": "team_member_references",
                "query": session.query(TeamMember).all(),
                "validation": lambda members: all(
                    session.query(Team).filter_by(team_id=member.team_id).first() is not None and
                    session.query(Employee).filter_by(employee_id=member.employee_id).first() is not None
                    for member in members
                )
            },
            # Test that all department OKRs with parent_objective_id reference valid company OKRs
            {
                "name": "department_okr_parent_references",
                "query": session.query(DepartmentObjective).filter(
                    DepartmentObjective.parent_objective_id.isnot(None)
                ).all(),
                "validation": lambda objectives: all(
                    session.query(CompanyObjective).filter_by(
                        objective_id=obj.parent_objective_id
                    ).first() is not None for obj in objectives
                )
            },
            # Test that all team OKRs with department_objective_id reference valid department OKRs
            {
                "name": "team_okr_parent_references",
                "query": session.query(TeamObjective).filter(
                    TeamObjective.department_objective_id.isnot(None)
                ).all(),
                "validation": lambda objectives: all(
                    session.query(DepartmentObjective).filter_by(
                        department_objective_id=obj.department_objective_id
                    ).first() is not None for obj in objectives
                )
            },
            # Test that all key results reference valid company objectives
            {
                "name": "key_result_objective_references",
                "query": session.query(KeyResult).all(),
                "validation": lambda krs: all(
                    session.query(CompanyObjective).filter_by(
                        objective_id=kr.objective_id
                    ).first() is not None for kr in krs
                )
            },
            # Test that all OKR updates reference valid key results
            {
                "name": "okr_update_references",
                "query": session.query(OKRUpdate).all(),
                "validation": lambda updates: all(
                    session.query(KeyResult).filter_by(
                        key_result_id=update.key_result_id
                    ).first() is not None for update in updates
                )
            },
            # Test that all team dependencies reference valid teams
            {
                "name": "team_dependency_references",
                "query": session.query(TeamDependency).all(),
                "validation": lambda deps: all(
                    session.query(Team).filter_by(
                        team_id=dep.dependent_team_id
                    ).first() is not None and
                    session.query(Team).filter_by(
                        team_id=dep.dependency_team_id
                    ).first() is not None
                    for dep in deps
                )
            }
        ]
        
        all_valid = True
        for test in relationship_tests:
            try:
                items = test["query"]
                is_valid = test["validation"](items)
                
                if is_valid:
                    logger.info(f"✓ {test['name']} validation passed")
                    self.validation_results["relationships"][test["name"]] = "passed"
                else:
                    logger.error(f"✗ {test['name']} validation failed")
                    self.validation_results["relationships"][test["name"]] = "failed"
                    all_valid = False
            except Exception as e:
                logger.error(f"Error validating {test['name']}: {e}")
                self.validation_results["relationships"][test["name"]] = f"error: {str(e)}"
                all_valid = False
        
        session.close()
        
        if all_valid:
            logger.info("✓ Relationship validation passed")
            self.validation_results["relationships"]["status"] = "passed"
            return True
        else:
            logger.error("✗ Relationship validation failed")
            self.validation_results["relationships"]["status"] = "failed"
            return False
    
    def validate_data_integrity(self) -> bool:
        """Validate data integrity including completeness and constraints."""
        logger.info("Validating data integrity...")
        session = self.Session()
        
        # Check record counts against expected values
        all_counts_match = True
        for table_name, expected_count in self.expected_counts.items():
            try:
                # Get the model class for this table
                model_class = next((cls for cls in Base.__subclasses__() 
                                 if cls.__tablename__ == table_name), None)
                if not model_class:
                    logger.error(f"Could not find model class for table {table_name}")
                    continue
                
                # Count records
                actual_count = session.query(model_class).count()
                
                # Check if count matches expected
                if actual_count != expected_count:
                    logger.warning(f"Table {table_name} has {actual_count} records, expected {expected_count}")
                    self.validation_results["data_integrity"][f"{table_name}_count"] = {
                        "expected": expected_count,
                        "actual": actual_count,
                        "status": "warning"
                    }
                    all_counts_match = False
                else:
                    logger.info(f"✓ Table {table_name} has expected count of {expected_count} records")
                    self.validation_results["data_integrity"][f"{table_name}_count"] = {
                        "expected": expected_count,
                        "actual": actual_count,
                        "status": "passed"
                    }
            except Exception as e:
                logger.error(f"Error checking record count for {table_name}: {e}")
                self.validation_results["data_integrity"][f"{table_name}_count"] = {
                    "expected": expected_count,
                    "actual": "error",
                    "status": "error",
                    "message": str(e)
                }
                all_counts_match = False
        
        # Check for NULL values in non-nullable fields
        null_checks = [
            # Check required organization fields
            {
                "name": "organization_required_fields",
                "query": session.query(Organization).filter(
                    (Organization.name.is_(None)) |
                    (Organization.domain.is_(None))
                ).count(),
                "expected": 0
            },
            # Check required department fields
            {
                "name": "department_required_fields",
                "query": session.query(Department).filter(
                    (Department.department_name.is_(None)) |
                    (Department.organization_id.is_(None))
                ).count(),
                "expected": 0
            },
            # Check required employee fields
            {
                "name": "employee_required_fields",
                "query": session.query(Employee).filter(
                    (Employee.first_name.is_(None)) |
                    (Employee.last_name.is_(None)) |
                    (Employee.email.is_(None)) |
                    (Employee.organization_id.is_(None))
                ).count(),
                "expected": 0
            },
            # Check required team fields
            {
                "name": "team_required_fields",
                "query": session.query(Team).filter(
                    (Team.team_name.is_(None))
                ).count(),
                "expected": 0
            },
            # Check required OKR fields
            {
                "name": "objective_required_fields",
                "query": session.query(CompanyObjective).filter(
                    (CompanyObjective.objective_statement.is_(None))
                ).count(),
                "expected": 0
            },
            # Check required key result fields
            {
                "name": "key_result_required_fields",
                "query": session.query(KeyResult).filter(
                    (KeyResult.description.is_(None)) |
                    (KeyResult.target_value.is_(None)) |
                    (KeyResult.current_value.is_(None))
                ).count(),
                "expected": 0
            }
        ]
        
        all_null_checks_pass = True
        for check in null_checks:
            try:
                null_count = check["query"]
                if null_count != check["expected"]:
                    logger.error(f"✗ {check['name']} check failed: Found {null_count} records with NULL in required fields")
                    self.validation_results["data_integrity"][check["name"]] = {
                        "expected": check["expected"],
                        "actual": null_count,
                        "status": "failed"
                    }
                    all_null_checks_pass = False
                else:
                    logger.info(f"✓ {check['name']} check passed")
                    self.validation_results["data_integrity"][check["name"]] = {
                        "expected": check["expected"],
                        "actual": null_count,
                        "status": "passed"
                    }
            except Exception as e:
                logger.error(f"Error running NULL check {check['name']}: {e}")
                self.validation_results["data_integrity"][check["name"]] = {
                    "status": "error",
                    "message": str(e)
                }
                all_null_checks_pass = False
        
        # Check for duplicate primary keys
        duplicate_checks = [
            {
                "table": "departments",
                "field": "department_id",
                "model": Department
            },
            {
                "table": "employees",
                "field": "employee_id",
                "model": Employee
            },
            {
                "table": "teams",
                "field": "team_id",
                "model": Team
            },
            {
                "table": "company_okrs",
                "field": "objective_id",
                "model": CompanyObjective
            }
        ]
        
        all_duplicate_checks_pass = True
        for check in duplicate_checks:
            try:
                # Count occurrences of each ID
                duplicate_query = session.query(
                    getattr(check["model"], check["field"]),
                    func.count(getattr(check["model"], check["field"])).label('count')
                ).group_by(
                    getattr(check["model"], check["field"])
                ).having(
                    func.count(getattr(check["model"], check["field"])) > 1
                ).all()
                
                if duplicate_query:
                    logger.error(f"✗ Found duplicates in {check['table']}.{check['field']}: {duplicate_query}")
                    self.validation_results["data_integrity"][f"{check['table']}_duplicate_ids"] = {
                        "status": "failed",
                        "duplicates": [str(item) for item in duplicate_query]
                    }
                    all_duplicate_checks_pass = False
                else:
                    logger.info(f"✓ No duplicates found in {check['table']}.{check['field']}")
                    self.validation_results["data_integrity"][f"{check['table']}_duplicate_ids"] = {
                        "status": "passed"
                    }
            except Exception as e:
                logger.error(f"Error checking duplicates in {check['table']}.{check['field']}: {e}")
                self.validation_results["data_integrity"][f"{check['table']}_duplicate_ids"] = {
                    "status": "error",
                    "message": str(e)
                }
                all_duplicate_checks_pass = False
        
        session.close()
        
        data_integrity_passed = all_counts_match and all_null_checks_pass and all_duplicate_checks_pass
        if data_integrity_passed:
            logger.info("✓ Data integrity validation passed")
            self.validation_results["data_integrity"]["status"] = "passed"
        else:
            logger.error("✗ Data integrity validation failed")
            self.validation_results["data_integrity"]["status"] = "failed" if not all_null_checks_pass or not all_duplicate_checks_pass else "warning"
        
        return data_integrity_passed
    
    def validate_consistency(self) -> bool:
        """Validate cross-table data consistency."""
        logger.info("Validating data consistency...")
        session = self.Session()
        
        consistency_checks = [
            # Department head should exist in employees table
            {
                "name": "department_heads_exist",
                "query": """
                    SELECT COUNT(*) 
                    FROM departments d
                    WHERE d.department_head_id IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM employees e 
                        WHERE e.employee_id = d.department_head_id
                    )
                """,
                "expected": 0,
                "message": "Department heads should exist in employees table"
            },
            
            # Employee managers should exist in employees table
            {
                "name": "employee_managers_exist",
                "query": """
                    SELECT COUNT(*) 
                    FROM employees e
                    WHERE e.manager_id IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM employees m 
                        WHERE m.employee_id = e.manager_id
                    )
                """,
                "expected": 0,
                "message": "Employee managers should exist in employees table"
            },
            
            # Team leads should exist in employees table
            {
                "name": "team_leads_exist",
                "query": """
                    SELECT COUNT(*) 
                    FROM teams t
                    WHERE t.team_lead_id IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM employees e 
                        WHERE e.employee_id = t.team_lead_id
                    )
                """,
                "expected": 0,
                "message": "Team leads should exist in employees table"
            },
            
            # All employees should belong to the Horizon Technologies organization
            {
                "name": "employees_organization",
                "query": """
                    SELECT COUNT(*) 
                    FROM employees 
                    WHERE organization_id != 1
                """,
                "expected": 0,
                "message": "All employees should belong to the Horizon Technologies organization"
            },
            
            # All departments should belong to the Horizon Technologies organization
            {
                "name": "departments_organization",
                "query": """
                    SELECT COUNT(*) 
                    FROM departments 
                    WHERE organization_id != 1
                """,
                "expected": 0,
                "message": "All departments should belong to the Horizon Technologies organization"
            },
            
            # Department OKR owners should exist in employees table
            {
                "name": "department_okr_owners_exist",
                "query": """
                    SELECT COUNT(*) 
                    FROM department_okrs d
                    WHERE d.owner_id IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM employees e 
                        WHERE e.employee_id = d.owner_id
                    )
                """,
                "expected": 0,
                "message": "Department OKR owners should exist in employees table"
            },
            
            # Key result owners should exist in employees table
            {
                "name": "key_result_owners_exist",
                "query": """
                    SELECT COUNT(*) 
                    FROM key_results k
                    WHERE k.owner_id IS NOT NULL
                    AND NOT EXISTS (
                        SELECT 1 
                        FROM employees e 
                        WHERE e.employee_id = k.owner_id
                    )
                """,
                "expected": 0,
                "message": "Key result owners should exist in employees table"
            },
            
            # Check consistency between OKR updates and key results
            {
                "name": "okr_updates_consistency",
                "query": """
                    SELECT COUNT(*) 
                    FROM okr_updates u
                    JOIN key_results k ON u.key_result_id = k.key_result_id
                    WHERE u.new_value IS NOT NULL 
                    AND k.current_value != (
                        SELECT new_value
                        FROM okr_updates
                        WHERE key_result_id = k.key_result_id
                        ORDER BY update_date DESC
                        LIMIT 1
                    )
                """,
                "expected": 0,
                "message": "Key result current_value should match the latest update's new_value"
            }
        ]
        
        all_consistency_checks_pass = True
        for check in consistency_checks:
            try:
                result = session.execute(text(check["query"])).scalar()
                if result != check["expected"]:
                    logger.error(f"✗ {check['name']} check failed: {check['message']} - Found {result} inconsistencies")
                    self.validation_results["consistency"][check["name"]] = {
                        "expected": check["expected"],
                        "actual": result,
                        "message": check["message"],
                        "status": "failed"
                    }
                    all_consistency_checks_pass = False
                else:
                    logger.info(f"✓ {check['name']} check passed")
                    self.validation_results["consistency"][check["name"]] = {
                        "expected": check["expected"],
                        "actual": result,
                        "status": "passed"
                    }
            except Exception as e:
                logger.error(f"Error running consistency check {check['name']}: {e}")
                self.validation_results["consistency"][check["name"]] = {
                    "status": "error",
                    "message": str(e)
                }
                all_consistency_checks_pass = False
        
        session.close()
        
        if all_consistency_checks_pass:
            logger.info("✓ Data consistency validation passed")
            self.validation_results["consistency"]["status"] = "passed"
            return True
        else:
            logger.error("✗ Data consistency validation failed")
            self.validation_results["consistency"]["status"] = "failed"
            return False
    
    def validate_all(self) -> bool:
        """Run all validation checks and return overall result."""
        logger.info(f"Starting database validation for {self.db_path}")
        
        schema_valid = self.validate_schema()
        relationships_valid = self.validate_relationships()
        data_integrity_valid = self.validate_data_integrity()
        consistency_valid = self.validate_consistency()
        
        all_valid = schema_valid and relationships_valid and data_integrity_valid and consistency_valid
        
        if all_valid:
            logger.info("✅ All database validation checks passed!")
        else:
            logger.error("❌ Some database validation checks failed, see logs for details")
        
        # Print a summary report
        logger.info("\nValidation Summary:")
        logger.info(f"Schema: {'✅ Passed' if schema_valid else '❌ Failed'}")
        logger.info(f"Relationships: {'✅ Passed' if relationships_valid else '❌ Failed'}")
        logger.info(f"Data Integrity: {'✅ Passed' if data_integrity_valid else '❌ Failed'}")
        logger.info(f"Consistency: {'✅ Passed' if consistency_valid else '❌ Failed'}")
        
        return all_valid
    
    def get_results(self) -> Dict[str, Any]:
        """Return validation results."""
        return self.validation_results


if __name__ == "__main__":
    # Default database path
    db_path = "sqlite:///organization.db"
    
    # Create and run the validator
    validator = DatabaseValidator(db_path)
    validator.validate_all()