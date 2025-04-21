#!/usr/bin/env python3
"""
Sample Database Queries for Organization Alignment Platform

This script runs several sample SQL queries against the database to demonstrate its capabilities.
"""

import os
import sys
import sqlite3
from tabulate import tabulate as tabulate_func

# Sample queries to demonstrate database capabilities
SAMPLE_QUERIES = [
    {
        "name": "Department Employee Counts",
        "query": """
            SELECT d.department_name, COUNT(e.employee_id) as employee_count
            FROM departments d
            LEFT JOIN employees e ON d.department_id = e.department_id
            WHERE d.parent_department_id IS NULL
            GROUP BY d.department_name
            ORDER BY employee_count DESC
        """
    },
    {
        "name": "OKR Status Summary",
        "query": """
            SELECT 'Company' as level, status, COUNT(*) as count
            FROM company_okrs
            GROUP BY status
            UNION ALL
            SELECT 'Department' as level, status, COUNT(*) as count
            FROM department_okrs
            GROUP BY status
            UNION ALL
            SELECT 'Team' as level, status, COUNT(*) as count
            FROM team_okrs
            GROUP BY status
            ORDER BY level, status
        """
    },
    {
        "name": "Team Dependencies",
        "query": """
            SELECT 
                t1.team_name as dependent_team,
                t2.team_name as dependency_team,
                td.description,
                td.status,
                td.criticality
            FROM cross_team_dependencies td
            JOIN teams t1 ON td.dependent_team_id = t1.team_id
            JOIN teams t2 ON td.dependency_team_id = t2.team_id
            ORDER BY td.criticality, td.status
            LIMIT 10
        """
    },
    {
        "name": "Objective Alignment Analysis",
        "query": """
            SELECT 
                co.objective_statement as company_objective,
                COUNT(do.department_objective_id) as aligned_dept_objectives,
                (
                    SELECT COUNT(*)
                    FROM team_okrs t_okr
                    JOIN department_okrs do2 ON t_okr.department_objective_id = do2.department_objective_id
                    WHERE do2.parent_objective_id = co.objective_id
                ) as aligned_team_objectives
            FROM company_okrs co
            LEFT JOIN department_okrs do ON do.parent_objective_id = co.objective_id
            GROUP BY co.objective_id
            ORDER BY aligned_dept_objectives DESC, aligned_team_objectives DESC
        """
    },
    {
        "name": "Key Result Progress",
        "query": """
            SELECT 
                co.objective_statement,
                kr.description,
                kr.target_value,
                kr.current_value,
                CASE 
                    WHEN kr.description LIKE '%Reduce%' OR kr.description LIKE '%Decrease%' 
                    THEN ROUND((kr.target_value / kr.current_value) * 100, 1)
                    ELSE ROUND((kr.current_value / kr.target_value) * 100, 1)
                END as progress_pct,
                kr.confidence_score
            FROM key_results kr
            JOIN company_okrs co ON kr.objective_id = co.objective_id
            ORDER BY progress_pct DESC
        """
    },
    {
        "name": "Resource Allocation by Priority",
        "query": """
            SELECT 
                do.priority,
                ra.resource_type,
                SUM(ra.allocated_amount) as total_allocated,
                SUM(ra.actual_usage) as total_used,
                ROUND((SUM(ra.actual_usage) - SUM(ra.allocated_amount)) / SUM(ra.allocated_amount) * 100, 1) as variance_pct
            FROM resource_allocation ra
            JOIN department_okrs do ON ra.objective_id = do.department_objective_id
            GROUP BY do.priority, ra.resource_type
            ORDER BY do.priority, ra.resource_type
        """
    }
]

def run_sample_queries():
    """Run sample queries against the database and display the results."""
    # Determine database path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))  # Two levels up from src/db
    db_path = os.path.join(project_root, "data", "organization.db")
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}")
        print("Please run import_data.py first to create the database.")
        return False
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Run each sample query
        for query_info in SAMPLE_QUERIES:
            print(f"\n=== {query_info['name']} ===")
            print("=" * (len(query_info['name']) + 8))
            
            # Execute the query
            cursor.execute(query_info['query'])
            rows = cursor.fetchall()
            
            if not rows:
                print("No results found.")
                continue
            
            # Get column names
            columns = [column[0] for column in cursor.description]
            
            # Convert to list of dicts
            results = [dict(zip(columns, row)) for row in rows]
            
            # Display results
            print(tabulate_func(results, headers="keys", tablefmt="pretty"))
        
        conn.close()
        return True
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

if __name__ == "__main__":
    try:
        # Check if tabulate is installed, if not, install it
        from tabulate import tabulate
    except ImportError:
        print("Installing required dependency: tabulate")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
        from tabulate import tabulate
    
    print("\nRunning sample queries against the organization database...\n")
    success = run_sample_queries()
    
    if success:
        print("\nAll sample queries executed successfully.")
    else:
        print("\nSome queries failed to execute. See error messages above.")