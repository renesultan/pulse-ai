# Pulse AI: Data Model Documentation

This document describes the core data entities, their attributes, and relationships in the Pulse AI system. Understanding this data model is essential for contributing to the project effectively.

## Core Entities

### Organization

The top-level entity representing the company structure.

**Attributes:**
- `organization_id` (UUID): Primary key
- `name` (String): Organization name
- `description` (String): Organization description
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

### Node

Represents departments, teams, or individuals within the organization. This is a flexible entity that forms the building blocks of the organizational chart.

**Attributes:**
- `node_id` (UUID): Primary key
- `organization_id` (UUID): Foreign key to Organization
- `name` (String): Node name
- `type` (Enum): Type of node (DEPARTMENT, TEAM, INDIVIDUAL)
- `metadata` (JSON): Additional node-specific data
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- One Organization has many Nodes
- Nodes can have parent-child relationships (via NodeRelationship)

### NodeRelationship

Defines hierarchical connections between nodes, allowing for the creation of the organizational structure.

**Attributes:**
- `relationship_id` (UUID): Primary key
- `parent_node_id` (UUID): Foreign key to parent Node
- `child_node_id` (UUID): Foreign key to child Node
- `relationship_type` (Enum): Type of relationship (REPORTS_TO, COLLABORATES_WITH)
- `weight` (Float): Optional weight/strength of relationship
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Each relationship connects two Nodes (parent and child)

### ObjectiveKeyResult (OKR)

Tracks objectives at different levels (company, department, team) and their associated key results.

**Attributes:**
- `objective_id` (UUID): Primary key
- `parent_objective_id` (UUID): Optional foreign key to parent Objective
- `node_id` (UUID): Foreign key to the Node this objective belongs to
- `statement` (String): The objective statement
- `timeframe` (String): Time period for the objective (e.g., Q1 2025)
- `owner_id` (UUID): Foreign key to the employee responsible
- `status` (Enum): Current status (ON_TRACK, AT_RISK, BEHIND)
- `priority` (Enum): Priority level (HIGH, MEDIUM, LOW)
- `description` (String): Detailed description
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Objectives can have parent-child relationships
- Each Objective belongs to a Node
- Each Objective has an owner (Employee)
- Objectives have associated KeyResults

### KeyResult

Measurable outcomes that define success for an objective.

**Attributes:**
- `key_result_id` (UUID): Primary key
- `objective_id` (UUID): Foreign key to associated Objective
- `statement` (String): Description of the key result
- `current_value` (Float): Current progress value
- `target_value` (Float): Target value for completion
- `unit` (String): Unit of measurement
- `owner_id` (UUID): Foreign key to the employee responsible
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Each KeyResult belongs to an Objective
- Each KeyResult has an owner (Employee)

### Dependency

Tracks dependencies between teams or objectives, highlighting potential bottlenecks.

**Attributes:**
- `dependency_id` (UUID): Primary key
- `source_id` (UUID): Foreign key to source Node or Objective
- `target_id` (UUID): Foreign key to target Node or Objective
- `dependency_type` (Enum): Type of dependency (BLOCKER, ENABLER, INFORMATIONAL)
- `status` (Enum): Current status (NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED)
- `description` (String): Description of the dependency
- `due_date` (Date): Expected resolution date
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Each Dependency connects two entities (source and target)

### Employee

Represents individual employees within the organization.

**Attributes:**
- `employee_id` (UUID): Primary key
- `first_name` (String): First name
- `last_name` (String): Last name
- `email` (String): Email address
- `hire_date` (Date): Date of hiring
- `job_title` (String): Job title
- `department_id` (UUID): Foreign key to department Node
- `manager_id` (UUID): Foreign key to manager Employee
- `employment_status` (Enum): Status (ACTIVE, LEAVE, TERMINATED)
- `location` (String): Work location
- `salary` (Integer): Annual salary

**Relationships:**
- Each Employee belongs to a Department (Node)
- Employees can have manager-report relationships
- Employees can own Objectives and KeyResults

### ResourceAllocation

Tracks how resources are allocated across departments and objectives.

**Attributes:**
- `allocation_id` (UUID): Primary key
- `department_id` (UUID): Foreign key to department Node
- `objective_id` (UUID): Optional foreign key to Objective
- `resource_type` (Enum): Type of resource (BUDGET, HEADCOUNT, TIME)
- `amount` (Float): Amount allocated
- `timeframe` (String): Time period for allocation
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Relationships:**
- Each ResourceAllocation is associated with a Department
- ResourceAllocations can be linked to specific Objectives

### StatusUpdate

Provides regular updates on team and department progress.

**Attributes:**
- `update_id` (UUID): Primary key
- `node_id` (UUID): Foreign key to the Node this update is about
- `author_id` (UUID): Foreign key to the Employee who created the update
- `content` (String): Update content
- `update_type` (Enum): Type of update (PROGRESS, BLOCKER, MILESTONE)
- `sentiment` (Enum): Sentiment of update (POSITIVE, NEUTRAL, NEGATIVE)
- `created_at` (DateTime): Creation timestamp

**Relationships:**
- Each StatusUpdate is associated with a Node
- Each StatusUpdate has an author (Employee)

## Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│              │       │              │       │              │
│ Organization │───1:N─▶     Node     ◀───N:1─│   Employee   │
│              │       │              │       │              │
└──────────────┘       └──────┬───────┘       └──────┬───────┘
                              │ 1                    │ 1
                              │                      │
                              │ N                    │ N
                       ┌──────▼───────┐       ┌──────▼───────┐
                       │              │       │              │
                       │NodeRelation- │       │ObjectiveKey- │
                       │    ship      │       │    Result    │
                       │              │       │              │
                       └──────────────┘       └──────┬───────┘
                                                     │ 1
                                                     │
                                                     │ N
                                              ┌──────▼───────┐
                                              │              │
                                              │  KeyResult   │
                                              │              │
                                              └──────────────┘
                                                     ▲
                                                     │
                       ┌──────────────┐              │
                       │              │              │
                       │  Dependency  │──────────────┘
                       │              │
                       └──────────────┘
                              ▲
                              │
                       ┌──────┴───────┐
                       │              │
                       │StatusUpdate  │
                       │              │
                       └──────────────┘
```

## Database Schema

The following SQL represents the core tables in our PostgreSQL database:

```sql
-- Organization table
CREATE TABLE organizations (
    organization_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Node table
CREATE TABLE nodes (
    node_id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(organization_id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Node Relationship table
CREATE TABLE node_relationships (
    relationship_id UUID PRIMARY KEY,
    parent_node_id UUID REFERENCES nodes(node_id),
    child_node_id UUID REFERENCES nodes(node_id),
    relationship_type VARCHAR(50) NOT NULL,
    weight FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Employee table
CREATE TABLE employees (
    employee_id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hire_date DATE NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    department_id UUID REFERENCES nodes(node_id),
    manager_id UUID REFERENCES employees(employee_id),
    employment_status VARCHAR(50) NOT NULL,
    location VARCHAR(255),
    salary INTEGER
);

-- Objective table
CREATE TABLE objectives (
    objective_id UUID PRIMARY KEY,
    parent_objective_id UUID REFERENCES objectives(objective_id),
    node_id UUID REFERENCES nodes(node_id),
    statement VARCHAR(255) NOT NULL,
    timeframe VARCHAR(50) NOT NULL,
    owner_id UUID REFERENCES employees(employee_id),
    status VARCHAR(50) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Key Result table
CREATE TABLE key_results (
    key_result_id UUID PRIMARY KEY,
    objective_id UUID REFERENCES objectives(objective_id),
    statement VARCHAR(255) NOT NULL,
    current_value FLOAT NOT NULL,
    target_value FLOAT NOT NULL,
    unit VARCHAR(50),
    owner_id UUID REFERENCES employees(employee_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Dependency table
CREATE TABLE dependencies (
    dependency_id UUID PRIMARY KEY,
    source_id UUID NOT NULL,
    target_id UUID NOT NULL,
    dependency_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    description TEXT,
    due_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Resource Allocation table
CREATE TABLE resource_allocations (
    allocation_id UUID PRIMARY KEY,
    department_id UUID REFERENCES nodes(node_id),
    objective_id UUID REFERENCES objectives(objective_id),
    resource_type VARCHAR(50) NOT NULL,
    amount FLOAT NOT NULL,
    timeframe VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Status Update table
CREATE TABLE status_updates (
    update_id UUID PRIMARY KEY,
    node_id UUID REFERENCES nodes(node_id),
    author_id UUID REFERENCES employees(employee_id),
    content TEXT NOT NULL,
    update_type VARCHAR(50) NOT NULL,
    sentiment VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Data Flow and Relationships

1. **Organization Structure**
   - Organization contains multiple Nodes (departments, teams)
   - Nodes are connected via NodeRelationships
   - Employees belong to Nodes (departments)

2. **OKR Hierarchy**
   - Company-level Objectives
   - Department-level Objectives (aligned to company objectives)
   - Team-level Objectives (aligned to department objectives)
   - Key Results measure progress on Objectives

3. **Dependencies and Status**
   - Dependencies track relationships between teams/objectives
   - StatusUpdates provide regular progress information
   - ResourceAllocations show how resources are distributed

## Data Validation Rules

1. **Objective Alignment**
   - Department objectives must link to company objectives
   - Team objectives must link to department objectives

2. **Node Relationships**
   - No circular dependencies in the reporting structure
   - Each node (except the root) must have a parent

3. **Key Results**
   - Current value must be within range [0, target_value]
   - Each objective should have 2-5 key results

4. **Resource Allocation**
   - Total allocated resources should not exceed available resources
   - Resources must be allocated to valid departments/objectives
