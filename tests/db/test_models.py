"""
Tests for database models and connections.
"""

import unittest
import os
import sys
from sqlalchemy.orm import sessionmaker
from src.db.models import get_engine, Base, Organization, Department


class TestDatabaseConnection(unittest.TestCase):
    """Test basic database connectivity and models."""

    def setUp(self):
        """Set up test database session."""
        self.engine = get_engine()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        """Close session after tests."""
        self.session.close()

    def test_database_connection(self):
        """Test that we can connect to the database."""
        # Simple check to see if we can execute a query
        from sqlalchemy import text
        result = self.session.execute(text("SELECT 1")).scalar()
        self.assertEqual(result, 1)

    def test_organization_table(self):
        """Test that the organization table exists and has data."""
        orgs = self.session.query(Organization).all()
        self.assertTrue(len(orgs) > 0, "No organizations found in database")
        
        # Check a specific organization property exists
        org = orgs[0]
        self.assertTrue(hasattr(org, 'name'), "Organization missing 'name' attribute")
        self.assertTrue(hasattr(org, 'domain'), "Organization missing 'domain' attribute")

    def test_department_relationship(self):
        """Test that relationships between models work."""
        # Get the first organization
        org = self.session.query(Organization).first()
        
        # Check that we can access departments
        self.assertIsNotNone(org.departments, "Organization-Department relationship failed")
        
        # If there are departments, check the relationship back to organization
        if org.departments:
            dept = org.departments[0]
            self.assertEqual(dept.organization.id, org.id, 
                             "Department-Organization relationship failed")


if __name__ == '__main__':
    unittest.main()