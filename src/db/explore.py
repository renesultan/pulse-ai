#!/usr/bin/env python3
"""
Interactive Database Exploration Script

This script provides a simple REPL to run SQL queries against the database.
"""

import os
import sys
import logging
import cmd
import sqlite3
from typing import List, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SQLiteExplorer(cmd.Cmd):
    """Interactive command-line SQL explorer for the database."""
    
    intro = '''
    =======================================================
    Database Explorer for Organization Alignment Platform
    =======================================================
    
    Type SQL queries to explore the database.
    
    Some example queries:
    - SELECT COUNT(*) FROM employees;
    - SELECT department_name, COUNT(*) FROM departments;
    - SELECT * FROM company_okrs LIMIT 5;
    
    Type 'tables' to see available tables.
    Type 'schema [table_name]' to see table schema.
    Type 'exit' or 'quit' to exit.
    '''
    prompt = 'sql> '
    
    def __init__(self, db_path: str = "organization.db"):
        """Initialize with path to the SQLite database."""
        super().__init__()
        self.db_path = db_path
        try:
            self.conn = sqlite3.connect(db_path)
            self.conn.row_factory = sqlite3.Row
            print(f"Connected to database: {db_path}")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            sys.exit(1)
    
    def _execute_query(self, query: str) -> Tuple[List[sqlite3.Row], List[str]]:
        """Execute SQL query and return results and column names."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description] if cursor.description else []
            return results, column_names
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return [], []
    
    def _format_results(self, results: List[sqlite3.Row], column_names: List[str], max_width: int = 20) -> str:
        """Format query results into a readable table format."""
        if not results or not column_names:
            return "No results returned."
        
        # Determine column widths (limited by max_width)
        col_widths = {}
        for col in column_names:
            col_widths[col] = min(max_width, len(str(col)))
        
        for row in results:
            for col in column_names:
                col_widths[col] = min(max_width, max(col_widths[col], len(str(row[col]))))
        
        # Create header
        header = " | ".join(col.ljust(col_widths[col]) for col in column_names)
        separator = "-+-".join("-" * col_widths[col] for col in column_names)
        
        # Create rows
        formatted_rows = []
        for row in results:
            formatted_row = " | ".join(
                str(row[col]).ljust(col_widths[col]) if len(str(row[col])) <= max_width 
                else str(row[col])[:max_width - 3] + "..."
                for col in column_names
            )
            formatted_rows.append(formatted_row)
        
        # Combine all parts
        output = [header, separator] + formatted_rows
        
        # Add row count
        output.append(f"\n{len(results)} rows returned")
        
        return "\n".join(output)
    
    def default(self, line: str) -> bool:
        """Handle SQL queries."""
        if line.lower() in ('exit', 'quit', 'q'):
            return self.do_exit(line)
        
        # Execute the query
        results, column_names = self._execute_query(line)
        if results:
            print(self._format_results(results, column_names))
        return False
    
    def do_tables(self, arg: str) -> bool:
        """List all tables in the database."""
        query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
        results, column_names = self._execute_query(query)
        if results:
            print("\nAvailable Tables:")
            print("----------------")
            for row in results:
                print(f"- {row['name']}")
        return False
    
    def do_schema(self, arg: str) -> bool:
        """Show schema for a specific table."""
        if not arg:
            print("Please specify a table name. Usage: schema table_name")
            return False
        
        # First check if the table exists
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{arg}';"
        results, _ = self._execute_query(query)
        if not results:
            print(f"Table '{arg}' does not exist.")
            return False
        
        # Get table schema
        query = f"PRAGMA table_info({arg});"
        results, column_names = self._execute_query(query)
        if results:
            print(f"\nSchema for table '{arg}':")
            print("-" * (19 + len(arg)))
            for row in results:
                not_null = "NOT NULL" if row['notnull'] else "NULL"
                pk = "PRIMARY KEY" if row['pk'] else ""
                print(f"{row['name']} ({row['type']}) {not_null} {pk}")
        return False
    
    def do_count(self, arg: str) -> bool:
        """Count records in all tables or a specific table."""
        if not arg:
            # Count records in all tables
            query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
            results, _ = self._execute_query(query)
            
            print("\nRecord Counts:")
            print("-------------")
            for row in results:
                table_name = row['name']
                count_query = f"SELECT COUNT(*) as count FROM {table_name};"
                count_results, _ = self._execute_query(count_query)
                if count_results:
                    print(f"{table_name}: {count_results[0]['count']} records")
        else:
            # Count records in specific table
            query = f"SELECT COUNT(*) as count FROM {arg};"
            results, _ = self._execute_query(query)
            if results:
                print(f"\n{arg}: {results[0]['count']} records")
        return False
    
    def do_exit(self, arg: str) -> bool:
        """Exit the explorer."""
        print("\nClosing database connection and exiting.")
        self.conn.close()
        return True
    
    # Aliases
    do_quit = do_exit
    do_q = do_exit


if __name__ == "__main__":
    # Default database path in project root
    db_path = "organization.db"
    
    # Make script executable from any location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    db_path = os.path.join(project_root, db_path)
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        print("Please run import_data.py first to create the database.")
        sys.exit(1)
    
    # Start the explorer
    explorer = SQLiteExplorer(db_path)
    explorer.cmdloop()