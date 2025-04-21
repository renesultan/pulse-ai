"""Initial database schema

Revision ID: 1e9e89fe38af
Revises: 
Create Date: 2025-04-20 17:44:14.099955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e9e89fe38af'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tables in the correct order to avoid circular dependencies
    
    # Create organizations table
    op.create_table('organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('domain', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create departments table first without the department_head_id foreign key
    op.create_table('departments',
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('department_name', sa.String(length=255), nullable=False),
        sa.Column('parent_department_id', sa.Integer(), nullable=True),
        sa.Column('cost_center_code', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['parent_department_id'], ['departments.department_id'], ),
        sa.PrimaryKeyConstraint('department_id')
    )
    
    # Create positions table
    op.create_table('positions',
        sa.Column('position_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('level', sa.String(length=50), nullable=True),
        sa.Column('salary_band_minimum', sa.Integer(), nullable=True),
        sa.Column('salary_band_maximum', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
        sa.PrimaryKeyConstraint('position_id')
    )
    
    # Create employees table
    op.create_table('employees',
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=255), nullable=False),
        sa.Column('last_name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hire_date', sa.Date(), nullable=True),
        sa.Column('job_title', sa.String(length=255), nullable=True),
        sa.Column('department_id', sa.Integer(), nullable=True),
        sa.Column('position_id', sa.Integer(), nullable=True),
        sa.Column('manager_id', sa.Integer(), nullable=True),
        sa.Column('employment_status', sa.String(length=50), nullable=True),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('salary', sa.Integer(), nullable=True),
        sa.Column('organization_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
        sa.ForeignKeyConstraint(['manager_id'], ['employees.employee_id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['position_id'], ['positions.position_id'], ),
        sa.PrimaryKeyConstraint('employee_id'),
        sa.UniqueConstraint('email')
    )
    
    # Add department_head_id to departments table
    op.add_column('departments', sa.Column('department_head_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'departments', 'employees', ['department_head_id'], ['employee_id'])
    
    # Create company_okrs table
    op.create_table('company_okrs',
        sa.Column('objective_id', sa.Integer(), nullable=False),
        sa.Column('objective_statement', sa.String(length=255), nullable=False),
        sa.Column('timeframe', sa.String(length=50), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['employees.employee_id'], ),
        sa.PrimaryKeyConstraint('objective_id')
    )
    
    # Create teams table
    op.create_table('teams',
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('team_name', sa.String(length=255), nullable=False),
        sa.Column('team_lead_id', sa.Integer(), nullable=True),
        sa.Column('project_name', sa.String(length=255), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['team_lead_id'], ['employees.employee_id'], ),
        sa.PrimaryKeyConstraint('team_id')
    )
    
    # Create department_okrs table
    op.create_table('department_okrs',
        sa.Column('department_objective_id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('objective_statement', sa.String(length=255), nullable=False),
        sa.Column('parent_objective_id', sa.Integer(), nullable=True),
        sa.Column('timeframe', sa.String(length=50), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['employees.employee_id'], ),
        sa.ForeignKeyConstraint(['parent_objective_id'], ['company_okrs.objective_id'], ),
        sa.PrimaryKeyConstraint('department_objective_id')
    )
    
    # Create cross_team_dependencies table
    op.create_table('cross_team_dependencies',
        sa.Column('dependency_id', sa.Integer(), nullable=False),
        sa.Column('dependent_team_id', sa.Integer(), nullable=False),
        sa.Column('dependency_team_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('criticality', sa.String(length=50), nullable=True),
        sa.Column('impact_description', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['dependency_team_id'], ['teams.team_id'], ),
        sa.ForeignKeyConstraint(['dependent_team_id'], ['teams.team_id'], ),
        sa.PrimaryKeyConstraint('dependency_id')
    )
    
    # Create key_results table
    op.create_table('key_results',
        sa.Column('key_result_id', sa.Integer(), nullable=False),
        sa.Column('objective_id', sa.Integer(), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('target_value', sa.Float(), nullable=False),
        sa.Column('current_value', sa.Float(), nullable=False),
        sa.Column('unit_of_measurement', sa.String(length=50), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=True),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('last_updated', sa.Date(), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['objective_id'], ['company_okrs.objective_id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['employees.employee_id'], ),
        sa.PrimaryKeyConstraint('key_result_id')
    )
    
    # Create resource_allocation table
    op.create_table('resource_allocation',
        sa.Column('allocation_id', sa.Integer(), nullable=False),
        sa.Column('department_id', sa.Integer(), nullable=False),
        sa.Column('objective_id', sa.Integer(), nullable=False),
        sa.Column('resource_type', sa.String(length=50), nullable=False),
        sa.Column('allocated_amount', sa.Integer(), nullable=False),
        sa.Column('timeframe', sa.String(length=50), nullable=True),
        sa.Column('actual_usage', sa.Integer(), nullable=True),
        sa.Column('variance_explanation', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['department_id'], ['departments.department_id'], ),
        sa.ForeignKeyConstraint(['objective_id'], ['department_okrs.department_objective_id'], ),
        sa.PrimaryKeyConstraint('allocation_id')
    )
    
    # Create team_members table
    op.create_table('team_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.Column('role_in_team', sa.String(length=255), nullable=True),
        sa.Column('allocation_percentage', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.employee_id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create team_okrs table
    op.create_table('team_okrs',
        sa.Column('team_objective_id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('objective_statement', sa.String(length=255), nullable=False),
        sa.Column('department_objective_id', sa.Integer(), nullable=True),
        sa.Column('timeframe', sa.String(length=50), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('priority', sa.String(length=50), nullable=True),
        sa.ForeignKeyConstraint(['department_objective_id'], ['department_okrs.department_objective_id'], ),
        sa.ForeignKeyConstraint(['owner_id'], ['employees.employee_id'], ),
        sa.ForeignKeyConstraint(['team_id'], ['teams.team_id'], ),
        sa.PrimaryKeyConstraint('team_objective_id')
    )
    
    # Create okr_updates table
    op.create_table('okr_updates',
        sa.Column('update_id', sa.Integer(), nullable=False),
        sa.Column('key_result_id', sa.Integer(), nullable=False),
        sa.Column('previous_value', sa.Float(), nullable=True),
        sa.Column('new_value', sa.Float(), nullable=True),
        sa.Column('update_date', sa.Date(), nullable=True),
        sa.Column('confidence_score', sa.Integer(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('updater_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['key_result_id'], ['key_results.key_result_id'], ),
        sa.ForeignKeyConstraint(['updater_id'], ['employees.employee_id'], ),
        sa.PrimaryKeyConstraint('update_id')
    )
    
    # Create status_updates table
    op.create_table('status_updates',
        sa.Column('update_id', sa.Integer(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('report_date', sa.Date(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('blockers', sa.Text(), nullable=True),
        sa.Column('next_steps', sa.Text(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['employees.employee_id'], ),
        sa.PrimaryKeyConstraint('update_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order of creation to handle dependencies
    op.drop_table('status_updates')
    op.drop_table('okr_updates')
    op.drop_table('team_okrs')
    op.drop_table('team_members')
    op.drop_table('resource_allocation')
    op.drop_table('key_results')
    op.drop_table('cross_team_dependencies')
    op.drop_table('department_okrs')
    op.drop_table('teams')
    op.drop_table('company_okrs')
    
    # Remove department_head_id foreign key first
    op.drop_constraint(None, 'departments', type_='foreignkey')
    op.drop_column('departments', 'department_head_id')
    
    op.drop_table('employees')
    op.drop_table('positions')
    op.drop_table('departments')
    op.drop_table('organizations')
