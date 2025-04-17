# F*ck Meetings - Organization Chart Visualization Tool

A minimalist productivity application designed to challenge traditional meeting culture by providing an intuitive, visually engaging interface for visualizing organizational structures and reporting lines.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Database Models](#database-models)
- [Core Components](#core-components)
- [Setup and Installation](#setup-and-installation)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Development Guidelines](#development-guidelines)
- [Troubleshooting](#troubleshooting)

## Overview

The F*ck Meetings app provides an interactive organization chart visualization tool capable of handling both simple hierarchies and complex enterprise-scale matrix organizations. The app emphasizes clarity in organizational structure to reduce unnecessary meetings by making reporting lines and responsibilities explicit.

### Key Technologies

- **Backend**: Python with Flask and SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Visualization**: D3.js
- **Deployment**: Gunicorn

## Features

- Interactive organization chart visualization with D3.js
- Support for enterprise-scale matrix organizations
- Multiple visualization options:
  - Hierarchical (traditional org chart)
  - Matrix (showing dual reporting lines)
  - Project-based views
- Save and load organization charts
- Export charts as PNG
- Dynamic node details panel
- Mini-map for navigating large charts
- Zoom and pan controls
- Sample data generation for demo purposes

## Architecture

The application follows an MVC (Model-View-Controller) pattern:

- **Models**: SQLAlchemy ORM models in `models.py` define the database schema
- **Views**: Flask templates in the `templates/` directory for rendering UI
- **Controllers**: Route handlers in `app.py` that process requests and return responses

### Directory Structure

```
├── app.py                # Main application with route handlers
├── models.py             # Database models with SQLAlchemy
├── main.py               # Entry point for the application
├── db_migration.py       # Database migration utilities
├── init_sample_data.py   # Sample data initialization script
├── static/               # Static assets
│   ├── css/              # CSS stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Image assets
├── templates/            # HTML templates
│   ├── index.html          # Landing page with form
│   ├── org_chart.html      # Organization chart visualization
│   └── direct_chart.html   # Chart with direct data rendering
├── utils/                # Utility modules
│   ├── enterprise_data_generator.py  # Sample data generation
│   └── reset_database.py             # Database reset utilities
└── README.md             # This documentation file
```

## Database Models

The application uses a comprehensive set of models to represent organizational structures:

### Core Models

- **Organization**: Top-level entity representing a company or organization
- **Department**: Divisions or departments within an organization
- **Employee**: Individual employees with titles and reporting relationships
- **Region**: Geographic regions for distributed organizations
- **Location**: Physical office locations
- **Project**: Cross-functional projects for matrix organizations
- **OrgChart**: Saved organization chart visualizations

### Key Relationships

- Organizations have many Departments, Employees, Regions, and Projects
- Employees can have primary managers (solid line) and secondary managers (dotted line)
- Departments can be nested (parent-child)
- Projects can include members from different departments

For complete schema details, see the `models.py` file.

## Core Components

### Backend Components

#### `app.py`

Contains the main Flask application, route definitions, and request handlers. Key endpoints include:

- `/`: Landing page with the organization chart form
- `/org-chart`: Processes form submission and renders the chart
- `/api/charts`: REST endpoints for retrieving saved charts

#### `models.py`

Defines SQLAlchemy ORM models that map to database tables. Includes model relationships and metadata.

#### `init_sample_data.py`

Script for initializing the database with sample enterprise organization data for demonstration purposes.

### Frontend Components

#### `static/js/org_chart.js`

Core D3.js visualization logic for rendering the organization chart, including:
- Tree layout calculation
- Node and link rendering
- Zoom and pan functionality
- Mini-map navigation
- Node detail interaction

#### `static/js/script.js`

Handles form submission, UI interactions, and client-side validation.

#### `templates/direct_chart.html`

Specialized template for rendering large organizational charts directly from server-processed data to avoid JSON parsing issues.

## Setup and Installation

### Prerequisites

- Python 3.11+
- PostgreSQL
- Node.js (for some dependencies)

### Installation Steps

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/dbname
   FLASK_SECRET_KEY=your_secret_key
   ```
4. Initialize the database:
   ```bash
   python init_sample_data.py
   ```
5. Start the application:
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Usage Guide

### Creating an Organization Chart

1. Navigate to the landing page
2. Fill out the organization structure form or click "Try an example"
3. Follow the format: `Name, Title, Reports To (optional)`
4. Click "Generate Organization Chart" to visualize

### Reading the Chart

- **Boxes**: Represent individual employees
- **Lines**: Indicate reporting relationships
- **Click on any node**: View details about the employee
- **Use the mini-map**: Navigate large organizations
- **Zoom controls**: Scale the chart for better visibility

### Exporting Charts

1. Click the "Export" button in the chart view
2. Select the desired format (currently PNG)
3. The chart will be downloaded to your device

## API Documentation

### Chart Creation API

**Endpoint**: `/org-chart`
**Method**: POST
**Parameters**:
- `company-name`: Organization name
- `department-name`: Department (optional)
- `org-structure`: Text representation of the org structure
- `reporting-line`: Style of reporting (hierarchical, matrix)

**Response**: Rendered chart or error message

### Chart Retrieval API

**Endpoint**: `/api/charts`
**Method**: GET
**Response**: JSON list of saved charts

```json
[
  {
    "id": 1,
    "name": "Executive Team",
    "organization": "TechNova Global",
    "created_at": "2025-04-15T20:45:12.235"
  }
]
```

## Development Guidelines

### Adding New Features

1. Database changes:
   - Add models in `models.py`
   - Update relationships
   - Run migrations

2. Backend changes:
   - Add routes in `app.py`
   - Add logic to process/transform data

3. Frontend changes:
   - Update templates in `templates/`
   - Add visualization code to `static/js/org_chart.js`
   - Add styles to `static/css/styles.css`

### Code Style

- Python: Follow PEP 8
- JavaScript: Use ES6+ features
- CSS: Follow BEM naming convention
- HTML: Use semantic elements

## Troubleshooting

### Common Issues

#### Chart Not Rendering

- Check browser console for JavaScript errors
- Verify the organization structure format
- Check if the data includes circular references
- For large organizations, try reducing the complexity

#### Database Connection Issues

- Verify environment variables are set correctly
- Check PostgreSQL service is running
- Verify database user permissions

#### Slow Chart Performance

- Large organizations may require optimization
- Consider limiting the depth of the hierarchy
- Use the matrix view for complex relationships

---

For additional assistance, please open an issue in the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.