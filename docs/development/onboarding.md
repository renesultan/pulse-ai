# Developer Onboarding Guide

Welcome to the Pulse AI project! This guide will help you get set up and become familiar with the codebase, development practices, and current project status.

## Project Overview

Pulse AI is an organizational visibility platform designed to help leaders identify misalignment across their company. The platform visualizes organizational structure, tracks objectives alignment, identifies dependencies, and highlights potential bottlenecks.

Our primary goal is to build a graph-based visualization of company structure that allows users to:
- View high-level organizational components (C-Suite, departments)
- Drill down into details via cards showing objectives and responsibilities
- Expand/collapse nodes to show sub-departments
- View a clean, sleek, and intuitive interface

## Getting Started

### 1. Environment Setup

First, clone the repository and set up your development environment:

```bash
# Clone the repository
git clone [repository-url]
cd pulse-ai

# Set up the Python virtual environment
chmod +x setup_env.sh
./setup_env.sh

# Activate the virtual environment
source venv/bin/activate
```

### 2. Project Structure

Familiarize yourself with the project's directory structure:

```
pulse-ai/
├── ALEMBIC_INTEGRATION.md   # Overview of database migration implementation
├── CLAUDE.md                # AI assistant project instructions
├── CONTRIBUTING.md          # Contribution guidelines
├── README.md                # Project overview and setup instructions
├── alembic.ini              # Database migration configuration
├── analyze_org_data.ipynb   # Jupyter notebook for data analysis
├── db/                      # Database models, import, and query scripts
├── docs/                    # Project documentation
│   ├── architecture/        # Architecture decisions and designs
│   ├── development/         # Development guides and practices
│   └── tutorials/           # Step-by-step tutorials
├── generate_org_data.py     # Script to generate synthetic data
├── migrations/              # Database migration scripts
├── organization_report.md   # Generated organizational report
├── requirements.txt         # Python dependencies
├── setup_env.sh             # Environment setup script
├── synthetic_data/          # CSV files containing synthetic data
└── test_migration.py        # Example script for database migrations
```

### 3. Database Setup

The project uses SQLAlchemy ORM with SQLite for development and PostgreSQL for production. Alembic is used for database migrations.

```bash
# Check the current database migration status
alembic current

# If you need to create a new migration after changing models
alembic revision --autogenerate -m "Description of changes"

# Apply any pending migrations
alembic upgrade head
```

For a comprehensive guide to database migrations, see [Database Migrations with Alembic](database-migrations.md).

### 4. Exploring the Data Model

The core data model is defined in `db/models.py` and includes:

- Organization
- Department
- Position
- Employee
- Team
- TeamMember
- Various OKR-related models (Company, Department, Team objectives)
- Dependencies between teams
- Status updates and resource allocations

To explore the data model:

```bash
# Import synthetic data into the database
python3 db/import_data.py

# Run sample queries to explore the data
python3 db/query_data.py

# Open the Jupyter notebook for interactive analysis
jupyter notebook analyze_org_data.ipynb
```

### 5. Current Project Status

We are in Phase 1 (Foundation) of our development roadmap. Here's what has been completed and what's next:

**Completed:**
- Initial project structure
- Basic data generation
- SQLAlchemy models for core entities
- Database migration system (Alembic)
- CSV import script

**Next Steps:**
- FastAPI application structure
- Core API endpoints
- Building the graph visualization frontend

## Development Workflow

### Making Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following the [code style guidelines](../../CONTRIBUTING.md)

3. If you've made database model changes:
   ```bash
   # Generate a migration
   alembic revision --autogenerate -m "Description of your changes"
   
   # Review the generated migration file in migrations/versions/
   
   # Apply the migration
   alembic upgrade head
   ```

4. Run tests and lint your code

5. Commit your changes with a descriptive message

6. Push your branch and create a pull request

### Documentation

We maintain extensive documentation for all aspects of the project. When making changes, please update the relevant documentation:

- For API changes, update `docs/architecture/api.md`
- For data model changes, update `docs/architecture/data-model.md`
- For new features, add usage examples to the relevant documentation

## Visualization Development Guide

Our current focus is on developing a graph-based visualization of the company structure. The key components we're working on:

1. **Backend API**:
   - Endpoints for retrieving hierarchical organizational data
   - Transformation of relational data to graph structure
   - Filtering and query capabilities

2. **Frontend Visualization**:
   - Hierarchical display of organizational structure
   - Interactive expansion/collapse of nodes
   - Side panel for detailed information
   - Clean, uncluttered interface

For more details on the design approach, see the [design_specification.md](../../design_specification.md) document.

## Getting Help

If you have questions or need assistance:

1. Check the documentation in the `docs/` directory
2. Review the project roadmap in the `README.md`
3. Reach out to the project maintainers

## Development Best Practices

1. **Follow the established patterns**: Look at existing code before implementing new features
2. **Document as you go**: Update documentation alongside code changes
3. **Write tests**: Ensure your changes are covered by tests
4. **Review your migrations**: Always review autogenerated migration scripts
5. **Commit often**: Make small, focused commits with clear messages

Welcome to the team, and happy coding!