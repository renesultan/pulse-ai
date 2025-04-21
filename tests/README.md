# Tests Directory

This directory contains all tests for the Pulse AI application.

## Test Structure

Tests are organized to mirror the application structure:

- `/unit` - Unit tests for individual components
- `/integration` - Integration tests for component interactions
- `/api` - API endpoint tests
- `/db` - Database tests

## Running Tests

To run tests, use the following command from the project root:

```bash
pytest tests/
```

For specific test categories:

```bash
pytest tests/unit/
pytest tests/api/
```