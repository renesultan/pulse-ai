# Contributing to Pulse AI

Thank you for your interest in contributing to Pulse AI! This document provides guidelines and instructions to help you contribute effectively.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Docker and Docker Compose (for deployment)

### Setting Up Your Development Environment

1. **Fork the repository**

   Start by forking the repository to your GitHub account.

2. **Clone your fork**

   ```bash
   git clone git@github.com:YOUR_USERNAME/pulse-ai.git
   cd pulse-ai
   ```

3. **Add the upstream remote**

   ```bash
   git remote add upstream git@github.com:renesultan/pulse-ai.git
   ```

4. **Set up the development environment**

   ```bash
   ./setup_env.sh
   source venv/bin/activate
   ```

5. **Verify the setup**

   ```bash
   python generate_org_data.py  # Should generate synthetic data
   ```

## Development Workflow

We follow a feature branch workflow:

1. **Create a new branch for your feature or bugfix**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-you-are-fixing
   ```

   Branch naming conventions:
   - `feature/` - For new features
   - `fix/` - For bug fixes
   - `docs/` - For documentation changes
   - `refactor/` - For code refactoring
   - `test/` - For adding or modifying tests

2. **Make your changes**

   - Write code that follows our [coding standards](#coding-standards)
   - Add tests for new functionality
   - Update documentation as needed

3. **Commit your changes**

   We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

   ```bash
   git commit -m "feat: add new visualization component"
   git commit -m "fix: resolve issue with data loading"
   git commit -m "docs: update API documentation"
   ```

4. **Keep your branch updated**

   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

5. **Push your changes**

   ```bash
   git push origin feature/your-feature-name
   ```

## Pull Request Process

1. **Create a Pull Request (PR)**

   - Go to the GitHub repository
   - Click "New Pull Request"
   - Select your branch
   - Fill out the PR template

2. **PR Requirements**

   - Provide a clear description of the changes
   - Link to any related issues
   - Include screenshots for UI changes
   - Ensure all tests pass
   - Maintain or improve code coverage

3. **Code Review**

   - Address reviewer comments
   - Make requested changes
   - Request re-review when ready

4. **Merge**

   Once approved, a maintainer will merge your PR.

## Coding Standards

### Python

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints
- Document functions and classes with docstrings
- Maximum line length of 88 characters (Black default)
- Use f-strings for string formatting

### TypeScript/React

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use functional components with hooks
- Use TypeScript interfaces for props
- Implement proper error handling
- Use CSS modules or styled-components for styling

### General

- Write self-documenting code with clear variable and function names
- Keep functions small and focused on a single responsibility
- Add comments for complex logic
- Use consistent indentation and formatting

## Testing

### Backend (Python)

- Write unit tests with pytest
- Create integration tests for API endpoints
- Use test fixtures for database operations
- Aim for 80%+ test coverage

### Frontend (React/TypeScript)

- Write component tests with React Testing Library
- Create end-to-end tests with Cypress
- Use snapshot testing for UI components
- Test error states and edge cases

### Running Tests

```bash
# Backend tests
pytest

# Frontend tests
cd frontend
npm test
```

## Documentation

Good documentation is crucial for this project. Please:

- Update README.md if you change setup requirements
- Document all functions, classes, and modules
- Update API documentation for endpoint changes
- Add JSDoc comments for TypeScript/JavaScript functions
- Create or update tutorials for new features

## Issue Reporting

When reporting issues, please use the issue templates and include:

- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details

## Feature Requests

For feature requests, please:

- Check existing issues first to avoid duplicates
- Use the feature request template
- Be specific about the problem the feature solves
- Consider implementation details if possible

Thank you for contributing to Pulse AI!
