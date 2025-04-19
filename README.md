# Pulse AI: Organizational Visibility Platform

## Project Overview

Pulse AI is an organizational visibility platform designed to help leaders identify misalignment across their company. The platform visualizes organizational structure, tracks objectives alignment, identifies dependencies, and highlights potential bottlenecks or misalignments.

By providing real-time insights into organizational health, Pulse AI enables leaders to:
- Visualize complex organizational structures and relationships
- Track alignment of objectives across departments and teams
- Identify critical dependencies between teams and projects
- Detect potential bottlenecks before they impact performance
- Make data-driven decisions about resource allocation

## Current Status

This project is in the early development phase. We have completed:
- Initial project structure setup
- Synthetic data generation for testing and development
- Environment setup scripts

## Technical Architecture

- **Frontend**: React with TypeScript
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Development Approach**: Iterative with small, incremental steps
- **Deployment**: Docker containers

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Docker and Docker Compose (for deployment)

### Development Environment Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd pulse-ai
   ```

2. Set up the Python virtual environment:
   ```bash
   ./setup_env.sh
   ```
   This script will:
   - Create a virtual environment
   - Install required dependencies
   - Set up a Jupyter kernel for data analysis

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

### Synthetic Data

The project includes a comprehensive synthetic data generator that creates realistic organizational data for development and testing. The data represents "Horizon Technologies," a fictional mid-sized technology company with ~500 employees.

To generate fresh synthetic data:
```bash
python generate_org_data.py
```

Generated data includes:
- Organizational structure (departments, positions, employees)
- Teams and team memberships
- OKRs at company, department, and team levels
- Cross-team dependencies
- Resource allocation
- Status updates and OKR progress tracking

## Project Roadmap

The development is organized into four phases:

### Phase 1: Foundation (Current Phase)

1. **Database Setup & Data Import**
   - [x] Initial project structure
   - [x] Basic data generation
   - [ ] SQLAlchemy models for core entities
   - [ ] Database migration system (Alembic)
   - [ ] CSV import script

2. **Basic API & Authentication**
   - [ ] FastAPI application structure
   - [ ] Core API endpoints
   - [ ] JWT authentication
   - [ ] Role-based permissions

3. **Frontend Foundation**
   - [ ] React application with TypeScript
   - [ ] Authentication UI
   - [ ] Basic dashboard

### Phase 2: Core Visualization

4. **Organizational Chart**
   - [ ] Data transformation service
   - [ ] Basic org chart visualization
   - [ ] Node detail views

5. **OKR Visualization**
   - [ ] OKR data service
   - [ ] OKR component
   - [ ] Alignment visualization

6. **Dependency Tracking**
   - [ ] Dependency data service
   - [ ] Dependency visualization
   - [ ] Status updates & notifications

### Phase 3: Advanced Features

7. **Alignment Analysis**
   - [ ] Advanced alignment detection
   - [ ] Alignment reports

8. **Resource Allocation Analysis**
   - [ ] Resource tracking
   - [ ] What-if analysis

9. **User Customization**
   - [ ] Custom views
   - [ ] Alerts & monitors

### Phase 4: Refinement & Integration

10. **Performance Optimization**
    - [ ] Backend optimization
    - [ ] Frontend optimization

11. **Integration Capabilities**
    - [ ] Import/export system
    - [ ] Third-party integrations

12. **Final Polishing**
    - [ ] User experience refinement
    - [ ] Deployment preparation

## Technical Design

### Data Model

The core entities in our system include:

1. **Organization**
   - Represents the company structure
   - Contains metadata about the organization

2. **Node**
   - Represents departments, teams, or individuals
   - Forms the building blocks of the organizational chart
   - Contains attributes like name, type, and metadata

3. **NodeRelationship**
   - Defines hierarchical connections between nodes
   - Supports different relationship types (reports to, collaborates with)

4. **ObjectiveKeyResult (OKR)**
   - Tracks objectives at different levels (company, department, team)
   - Contains key results that measure progress
   - Includes metadata like timeframe, owner, status, and priority

5. **Dependency**
   - Tracks dependencies between teams or objectives
   - Includes status, criticality, and impact assessment

### API Design

The API will follow RESTful principles with the following main endpoints:

1. **Authentication**
   - `/auth/login`
   - `/auth/register`
   - `/auth/refresh`

2. **Organization Structure**
   - `/api/organization`
   - `/api/departments`
   - `/api/teams`
   - `/api/employees`

3. **OKRs and Alignment**
   - `/api/objectives`
   - `/api/key-results`
   - `/api/alignment`

4. **Dependencies**
   - `/api/dependencies`
   - `/api/status-updates`

5. **Analysis**
   - `/api/analysis/alignment`
   - `/api/analysis/resources`
   - `/api/analysis/bottlenecks`

### Frontend Architecture

The frontend will be built with React and TypeScript, following these principles:

1. **Component Structure**
   - Atomic design methodology
   - Reusable UI components
   - Container/presentation component pattern

2. **State Management**
   - React Context for global state
   - React Query for server state
   - Local component state where appropriate

3. **Visualization Libraries**
   - D3.js for custom visualizations
   - React Flow for organizational charts
   - Recharts for standard charts and graphs

## Contribution Guidelines

### Getting Started

1. Check the project roadmap to understand current priorities
2. Pick an unassigned task from the current phase
3. Create a feature branch from `develop`

### Development Workflow

1. **Branch Naming**
   - Feature branches: `feature/short-description`
   - Bug fixes: `fix/issue-description`
   - Refactoring: `refactor/component-name`

2. **Commit Messages**
   - Follow conventional commits format
   - Include issue number if applicable
   - Be descriptive but concise

3. **Pull Requests**
   - Create PR against `develop` branch
   - Include description of changes
   - Link to related issues
   - Ensure all tests pass
   - Request review from at least one team member

### Coding Standards

1. **Python**
   - Follow PEP 8 style guide
   - Use type hints
   - Document functions and classes with docstrings
   - Maintain 80%+ test coverage

2. **TypeScript/React**
   - Follow Airbnb JavaScript Style Guide
   - Use functional components with hooks
   - Implement proper error handling
   - Write unit tests for components

### Testing

1. **Backend**
   - Unit tests with pytest
   - Integration tests for API endpoints
   - Use test fixtures for database operations

2. **Frontend**
   - Component tests with React Testing Library
   - End-to-end tests with Cypress
   - Snapshot testing for UI components

## Deployment

The application is designed to be deployed as Docker containers:

1. **Development**
   - Local Docker Compose setup
   - Hot-reloading for both frontend and backend

2. **Staging**
   - Automated deployment from `develop` branch
   - Integration testing environment

3. **Production**
   - Deployment from `main` branch
   - Scalable infrastructure with load balancing

## License

[MIT License](LICENSE)

## Contact

For questions or clarification about the project, please contact the project maintainers.
