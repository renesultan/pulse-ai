# Development Environment Setup

This guide provides step-by-step instructions for setting up your development environment for the Pulse AI project.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.8+**
- **Node.js 16+**
- **PostgreSQL 13+**
- **Git**
- **Docker** and **Docker Compose** (for deployment)

## Initial Setup

### 1. Clone the Repository

```bash
git clone git@github.com:renesultan/pulse-ai.git
cd pulse-ai
```

### 2. Set Up Python Environment

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup_env.sh
```

This script will:
- Create a Python virtual environment in the `venv` directory
- Install required Python packages from `requirements.txt`
- Set up a Jupyter kernel for data analysis

Activate the virtual environment:

```bash
source venv/bin/activate
```

### 3. Generate Synthetic Data

The project includes a synthetic data generator for development and testing:

```bash
python generate_org_data.py
```

This will create CSV files in the `synthetic_data` directory containing:
- Organizational structure (departments, positions, employees)
- Teams and team memberships
- OKRs at company, department, and team levels
- Cross-team dependencies
- Resource allocation
- Status updates and OKR progress tracking

### 4. Database Setup

#### Local PostgreSQL Setup

1. Create a new PostgreSQL database:

```bash
createdb pulse_ai
```

2. Set up environment variables for database connection:

```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/pulse_ai"
```

Replace `username` and `password` with your PostgreSQL credentials.

3. Run database migrations (once implemented):

```bash
# This will be implemented in Phase 1
# alembic upgrade head
```

#### Using Docker for Database (Alternative)

If you prefer using Docker for PostgreSQL:

```bash
docker run --name pulse-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=pulse -e POSTGRES_DB=pulse_ai -p 5432:5432 -d postgres:13
```

### 5. Frontend Setup (Future)

Once the frontend is implemented:

```bash
cd frontend
npm install
npm start
```

## Development Tools

### Recommended IDE Setup

- **VS Code** with the following extensions:
  - Python
  - ESLint
  - Prettier
  - GitLens
  - Docker

### Useful Commands

#### Backend

- Run tests: `pytest`
- Generate synthetic data: `python generate_org_data.py`
- Analyze data: `jupyter notebook analyze_org_data.ipynb`

#### Database

- Connect to PostgreSQL: `psql -U username -d pulse_ai`
- Backup database: `pg_dump -U username pulse_ai > backup.sql`
- Restore database: `psql -U username -d pulse_ai < backup.sql`

#### Git

- Create a feature branch: `git checkout -b feature/your-feature-name`
- Update from main: `git pull origin main`
- Push changes: `git push -u origin feature/your-feature-name`

## Troubleshooting

### Common Issues

1. **Virtual Environment Issues**

If you encounter problems with the virtual environment:

```bash
# Remove existing venv
rm -rf venv

# Create a new one manually
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Database Connection Issues**

If you can't connect to the database:

- Verify PostgreSQL is running: `pg_isready`
- Check your connection string
- Ensure you have the correct permissions

3. **Synthetic Data Generation Issues**

If data generation fails:

- Ensure all dependencies are installed
- Check for any error messages
- Verify the output directory exists and is writable

## Next Steps

After setting up your environment:

1. Review the [project architecture](../architecture/overview.md)
2. Understand the [data model](../architecture/data-model.md)
3. Familiarize yourself with the [development workflow](workflow.md)
4. Check the [README.md](../../README.md) for current project status and roadmap
5. Pick an issue to work on from the project board

## Getting Help

If you encounter any issues not covered in this guide:

1. Check existing documentation in the `docs` directory
2. Review open and closed issues on GitHub
3. Reach out to the team for assistance
