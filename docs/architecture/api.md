# API Design Documentation

This document outlines the API design for the Pulse AI platform, providing a comprehensive guide for backend developers to implement consistent, well-structured, and performant API endpoints.

## API Design Principles

The Pulse AI API follows these core principles:

1. **RESTful Design**: Resources are represented as URLs, with HTTP methods defining actions
2. **Consistent Structure**: Endpoints follow a consistent naming and response pattern
3. **Versioning**: All endpoints include version information to allow for future evolution
4. **Authentication**: JWT-based authentication for secure access
5. **Comprehensive Documentation**: All endpoints are fully documented with OpenAPI/Swagger
6. **Appropriate Status Codes**: HTTP status codes accurately reflect the result of operations

## Base URL Structure

```
https://api.example.com/api/v1/[resource]
```

- `api` prefix to distinguish API endpoints
- `v1` version identifier
- `resource` represents the entity being accessed

## Authentication

All API endpoints (except authentication endpoints) require a valid JWT token.

### Authentication Endpoints

#### Login

```
POST /api/v1/auth/login
```

Request:
```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Refresh Token

```
POST /api/v1/auth/refresh
```

Request:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

## Core Resources

### Organization

#### Get Organization

```
GET /api/v1/organizations/{organization_id}
```

Response:
```json
{
  "organization_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Horizon Technologies",
  "description": "A technology company focused on cloud solutions",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

### Nodes (Departments, Teams, Individuals)

#### List Nodes

```
GET /api/v1/organizations/{organization_id}/nodes
```

Query Parameters:
- `type`: Filter by node type (DEPARTMENT, TEAM, INDIVIDUAL)
- `parent_id`: Filter by parent node
- `page`: Page number for pagination
- `limit`: Number of items per page

Response:
```json
{
  "items": [
    {
      "node_id": "123e4567-e89b-12d3-a456-426614174001",
      "organization_id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Engineering",
      "type": "DEPARTMENT",
      "metadata": {
        "location": "San Francisco",
        "budget": 1000000
      },
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    // More nodes...
  ],
  "total": 50,
  "page": 1,
  "limit": 20
}
```

#### Get Node

```
GET /api/v1/nodes/{node_id}
```

Response:
```json
{
  "node_id": "123e4567-e89b-12d3-a456-426614174001",
  "organization_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Engineering",
  "type": "DEPARTMENT",
  "metadata": {
    "location": "San Francisco",
    "budget": 1000000
  },
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### Create Node

```
POST /api/v1/organizations/{organization_id}/nodes
```

Request:
```json
{
  "name": "Product Development",
  "type": "DEPARTMENT",
  "metadata": {
    "location": "New York",
    "budget": 800000
  }
}
```

Response:
```json
{
  "node_id": "123e4567-e89b-12d3-a456-426614174002",
  "organization_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Product Development",
  "type": "DEPARTMENT",
  "metadata": {
    "location": "New York",
    "budget": 800000
  },
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### Update Node

```
PUT /api/v1/nodes/{node_id}
```

Request:
```json
{
  "name": "Product Development",
  "metadata": {
    "location": "Boston",
    "budget": 900000
  }
}
```

Response:
```json
{
  "node_id": "123e4567-e89b-12d3-a456-426614174002",
  "organization_id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Product Development",
  "type": "DEPARTMENT",
  "metadata": {
    "location": "Boston",
    "budget": 900000
  },
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-02T00:00:00Z"
}
```

#### Delete Node

```
DELETE /api/v1/nodes/{node_id}
```

Response:
```
204 No Content
```

### Node Relationships

#### List Node Relationships

```
GET /api/v1/nodes/{node_id}/relationships
```

Query Parameters:
- `type`: Filter by relationship type (REPORTS_TO, COLLABORATES_WITH)
- `direction`: "incoming" or "outgoing"
- `page`: Page number for pagination
- `limit`: Number of items per page

Response:
```json
{
  "items": [
    {
      "relationship_id": "123e4567-e89b-12d3-a456-426614174003",
      "parent_node_id": "123e4567-e89b-12d3-a456-426614174001",
      "child_node_id": "123e4567-e89b-12d3-a456-426614174002",
      "relationship_type": "REPORTS_TO",
      "weight": 1.0,
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    // More relationships...
  ],
  "total": 15,
  "page": 1,
  "limit": 20
}
```

#### Create Relationship

```
POST /api/v1/nodes/relationships
```

Request:
```json
{
  "parent_node_id": "123e4567-e89b-12d3-a456-426614174001",
  "child_node_id": "123e4567-e89b-12d3-a456-426614174002",
  "relationship_type": "REPORTS_TO",
  "weight": 1.0
}
```

Response:
```json
{
  "relationship_id": "123e4567-e89b-12d3-a456-426614174003",
  "parent_node_id": "123e4567-e89b-12d3-a456-426614174001",
  "child_node_id": "123e4567-e89b-12d3-a456-426614174002",
  "relationship_type": "REPORTS_TO",
  "weight": 1.0,
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### Delete Relationship

```
DELETE /api/v1/nodes/relationships/{relationship_id}
```

Response:
```
204 No Content
```

### Objectives and Key Results (OKRs)

#### List Objectives

```
GET /api/v1/organizations/{organization_id}/objectives
```

Query Parameters:
- `timeframe`: Filter by timeframe (e.g., "Q1 2025")
- `node_id`: Filter by node
- `status`: Filter by status (ON_TRACK, AT_RISK, BEHIND)
- `priority`: Filter by priority (HIGH, MEDIUM, LOW)
- `page`: Page number for pagination
- `limit`: Number of items per page

Response:
```json
{
  "items": [
    {
      "objective_id": "123e4567-e89b-12d3-a456-426614174004",
      "parent_objective_id": null,
      "node_id": "123e4567-e89b-12d3-a456-426614174000",
      "statement": "Achieve market leadership in cloud solutions",
      "timeframe": "FY 2025",
      "owner_id": "123e4567-e89b-12d3-a456-426614174010",
      "status": "ON_TRACK",
      "priority": "HIGH",
      "description": "Establish our company as the go-to provider for cloud solutions",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    // More objectives...
  ],
  "total": 25,
  "page": 1,
  "limit": 20
}
```

#### Get Objective

```
GET /api/v1/objectives/{objective_id}
```

Response:
```json
{
  "objective_id": "123e4567-e89b-12d3-a456-426614174004",
  "parent_objective_id": null,
  "node_id": "123e4567-e89b-12d3-a456-426614174000",
  "statement": "Achieve market leadership in cloud solutions",
  "timeframe": "FY 2025",
  "owner_id": "123e4567-e89b-12d3-a456-426614174010",
  "status": "ON_TRACK",
  "priority": "HIGH",
  "description": "Establish our company as the go-to provider for cloud solutions",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z",
  "key_results": [
    {
      "key_result_id": "123e4567-e89b-12d3-a456-426614174005",
      "objective_id": "123e4567-e89b-12d3-a456-426614174004",
      "statement": "Increase market share to 25%",
      "current_value": 18,
      "target_value": 25,
      "unit": "percentage",
      "owner_id": "123e4567-e89b-12d3-a456-426614174011",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    // More key results...
  ]
}
```

#### Create Objective

```
POST /api/v1/nodes/{node_id}/objectives
```

Request:
```json
{
  "parent_objective_id": null,
  "statement": "Improve customer satisfaction",
  "timeframe": "Q2 2025",
  "owner_id": "123e4567-e89b-12d3-a456-426614174010",
  "status": "ON_TRACK",
  "priority": "HIGH",
  "description": "Enhance customer experience to improve retention"
}
```

Response:
```json
{
  "objective_id": "123e4567-e89b-12d3-a456-426614174006",
  "parent_objective_id": null,
  "node_id": "123e4567-e89b-12d3-a456-426614174001",
  "statement": "Improve customer satisfaction",
  "timeframe": "Q2 2025",
  "owner_id": "123e4567-e89b-12d3-a456-426614174010",
  "status": "ON_TRACK",
  "priority": "HIGH",
  "description": "Enhance customer experience to improve retention",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### Update Objective

```
PUT /api/v1/objectives/{objective_id}
```

Request:
```json
{
  "status": "AT_RISK",
  "description": "Enhance customer experience to improve retention and reduce churn"
}
```

Response:
```json
{
  "objective_id": "123e4567-e89b-12d3-a456-426614174006",
  "parent_objective_id": null,
  "node_id": "123e4567-e89b-12d3-a456-426614174001",
  "statement": "Improve customer satisfaction",
  "timeframe": "Q2 2025",
  "owner_id": "123e4567-e89b-12d3-a456-426614174010",
  "status": "AT_RISK",
  "priority": "HIGH",
  "description": "Enhance customer experience to improve retention and reduce churn",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-02T00:00:00Z"
}
```

#### Delete Objective

```
DELETE /api/v1/objectives/{objective_id}
```

Response:
```
204 No Content
```

### Key Results

#### List Key Results for an Objective

```
GET /api/v1/objectives/{objective_id}/key-results
```

Response:
```json
{
  "items": [
    {
      "key_result_id": "123e4567-e89b-12d3-a456-426614174005",
      "objective_id": "123e4567-e89b-12d3-a456-426614174004",
      "statement": "Increase market share to 25%",
      "current_value": 18,
      "target_value": 25,
      "unit": "percentage",
      "owner_id": "123e4567-e89b-12d3-a456-426614174011",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    // More key results...
  ],
  "total": 3,
  "page": 1,
  "limit": 20
}
```

#### Create Key Result

```
POST /api/v1/objectives/{objective_id}/key-results
```

Request:
```json
{
  "statement": "Achieve NPS score of 50",
  "current_value": 35,
  "target_value": 50,
  "unit": "score",
  "owner_id": "123e4567-e89b-12d3-a456-426614174011"
}
```

Response:
```json
{
  "key_result_id": "123e4567-e89b-12d3-a456-426614174007",
  "objective_id": "123e4567-e89b-12d3-a456-426614174006",
  "statement": "Achieve NPS score of 50",
  "current_value": 35,
  "target_value": 50,
  "unit": "score",
  "owner_id": "123e4567-e89b-12d3-a456-426614174011",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### Update Key Result

```
PUT /api/v1/key-results/{key_result_id}
```

Request:
```json
{
  "current_value": 42
}
```

Response:
```json
{
  "key_result_id": "123e4567-e89b-12d3-a456-426614174007",
  "objective_id": "123e4567-e89b-12d3-a456-426614174006",
  "statement": "Achieve NPS score of 50",
  "current_value": 42,
  "target_value": 50,
  "unit": "score",
  "owner_id": "123e4567-e89b-12d3-a456-426614174011",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-02T00:00:00Z"
}
```

#### Delete Key Result

```
DELETE /api/v1/key-results/{key_result_id}
```

Response:
```
204 No Content
```

### Dependencies

#### List Dependencies

```
GET /api/v1/organizations/{organization_id}/dependencies
```

Query Parameters:
- `source_id`: Filter by source node/objective
- `target_id`: Filter by target node/objective
- `status`: Filter by status
- `page`: Page number for pagination
- `limit`: Number of items per page

Response:
```json
{
  "items": [
    {
      "dependency_id": "123e4567-e89b-12d3-a456-426614174008",
      "source_id": "123e4567-e89b-12d3-a456-426614174001",
      "target_id": "123e4567-e89b-12d3-a456-426614174002",
      "dependency_type": "BLOCKER",
      "status": "IN_PROGRESS",
      "description": "Engineering needs to complete API before Product can proceed",
      "due_date": "2025-03-15",
      "created_at": "2025-01-01T00:00:00Z",
      "updated_at": "2025-01-01T00:00:00Z"
    },
    // More dependencies...
  ],
  "total": 12,
  "page": 1,
  "limit": 20
}
```

#### Create Dependency

```
POST /api/v1/dependencies
```

Request:
```json
{
  "source_id": "123e4567-e89b-12d3-a456-426614174001",
  "target_id": "123e4567-e89b-12d3-a456-426614174002",
  "dependency_type": "BLOCKER",
  "status": "IN_PROGRESS",
  "description": "Engineering needs to complete API before Product can proceed",
  "due_date": "2025-03-15"
}
```

Response:
```json
{
  "dependency_id": "123e4567-e89b-12d3-a456-426614174008",
  "source_id": "123e4567-e89b-12d3-a456-426614174001",
  "target_id": "123e4567-e89b-12d3-a456-426614174002",
  "dependency_type": "BLOCKER",
  "status": "IN_PROGRESS",
  "description": "Engineering needs to complete API before Product can proceed",
  "due_date": "2025-03-15",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:00:00Z"
}
```

#### Update Dependency

```
PUT /api/v1/dependencies/{dependency_id}
```

Request:
```json
{
  "status": "COMPLETED",
  "description": "Engineering completed API ahead of schedule"
}
```

Response:
```json
{
  "dependency_id": "123e4567-e89b-12d3-a456-426614174008",
  "source_id": "123e4567-e89b-12d3-a456-426614174001",
  "target_id": "123e4567-e89b-12d3-a456-426614174002",
  "dependency_type": "BLOCKER",
  "status": "COMPLETED",
  "description": "Engineering completed API ahead of schedule",
  "due_date": "2025-03-15",
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-02T00:00:00Z"
}
```

### Status Updates

#### List Status Updates

```
GET /api/v1/nodes/{node_id}/status-updates
```

Query Parameters:
- `update_type`: Filter by update type
- `start_date`: Filter by date range start
- `end_date`: Filter by date range end
- `page`: Page number for pagination
- `limit`: Number of items per page

Response:
```json
{
  "items": [
    {
      "update_id": "123e4567-e89b-12d3-a456-426614174009",
      "node_id": "123e4567-e89b-12d3-a456-426614174001",
      "author_id": "123e4567-e89b-12d3-a456-426614174010",
      "content": "API development is progressing well, on track to meet deadline",
      "update_type": "PROGRESS",
      "sentiment": "POSITIVE",
      "created_at": "2025-01-01T00:00:00Z"
    },
    // More updates...
  ],
  "total": 35,
  "page": 1,
  "limit": 20
}
```

#### Create Status Update

```
POST /api/v1/nodes/{node_id}/status-updates
```

Request:
```json
{
  "content": "Encountered issues with third-party integration, may impact timeline",
  "update_type": "BLOCKER",
  "sentiment": "NEGATIVE"
}
```

Response:
```json
{
  "update_id": "123e4567-e89b-12d3-a456-426614174010",
  "node_id": "123e4567-e89b-12d3-a456-426614174001",
  "author_id": "123e4567-e89b-12d3-a456-426614174010",
  "content": "Encountered issues with third-party integration, may impact timeline",
  "update_type": "BLOCKER",
  "sentiment": "NEGATIVE",
  "created_at": "2025-01-02T00:00:00Z"
}
```

## Analysis Endpoints

### Alignment Analysis

```
GET /api/v1/analysis/alignment
```

Query Parameters:
- `organization_id`: Organization to analyze
- `timeframe`: Filter by timeframe
- `department_id`: Optional filter by department

Response:
```json
{
  "overall_alignment_score": 0.85,
  "department_scores": [
    {
      "department_id": "123e4567-e89b-12d3-a456-426614174001",
      "name": "Engineering",
      "alignment_score": 0.92,
      "misalignments": []
    },
    {
      "department_id": "123e4567-e89b-12d3-a456-426614174002",
      "name": "Product",
      "alignment_score": 0.78,
      "misalignments": [
        {
          "objective_id": "123e4567-e89b-12d3-a456-426614174006",
          "statement": "Improve customer satisfaction",
          "company_objective_id": "123e4567-e89b-12d3-a456-426614174004",
          "alignment_score": 0.65,
          "recommendation": "Refocus objective to better support company goal of market leadership"
        }
      ]
    }
  ]
}
```

### Resource Allocation Analysis

```
GET /api/v1/analysis/resources
```

Query Parameters:
- `organization_id`: Organization to analyze
- `timeframe`: Filter by timeframe
- `resource_type`: Optional filter by resource type

Response:
```json
{
  "total_resources": {
    "BUDGET": 5000000,
    "HEADCOUNT": 500
  },
  "allocation_by_priority": {
    "HIGH": {
      "BUDGET": 3000000,
      "HEADCOUNT": 300
    },
    "MEDIUM": {
      "BUDGET": 1500000,
      "HEADCOUNT": 150
    },
    "LOW": {
      "BUDGET": 500000,
      "HEADCOUNT": 50
    }
  },
  "allocation_by_department": [
    {
      "department_id": "123e4567-e89b-12d3-a456-426614174001",
      "name": "Engineering",
      "resources": {
        "BUDGET": 2000000,
        "HEADCOUNT": 200
      },
      "objectives": [
        {
          "objective_id": "123e4567-e89b-12d3-a456-426614174005",
          "statement": "Deliver next-gen platform",
          "priority": "HIGH",
          "resources": {
            "BUDGET": 1500000,
            "HEADCOUNT": 150
          }
        }
      ]
    }
  ],
  "recommendations": [
    {
      "type": "REALLOCATION",
      "description": "Consider shifting 10% of budget from low-priority objectives to high-priority objective 'Expand into European market'",
      "impact_score": 0.75
    }
  ]
}
```

### Bottleneck Analysis

```
GET /api/v1/analysis/bottlenecks
```

Query Parameters:
- `organization_id`: Organization to analyze

Response:
```json
{
  "critical_dependencies": [
    {
      "dependency_id": "123e4567-e89b-12d3-a456-426614174008",
      "source": {
        "id": "123e4567-e89b-12d3-a456-426614174001",
        "name": "Engineering"
      },
      "target": {
        "id": "123e4567-e89b-12d3-a456-426614174002",
        "name": "Product"
      },
      "status": "BLOCKED",
      "impact_score": 0.85,
      "affected_objectives": [
        {
          "objective_id": "123e4567-e89b-12d3-a456-426614174006",
          "statement": "Improve customer satisfaction"
        }
      ]
    }
  ],
  "resource_bottlenecks": [
    {
      "department_id": "123e4567-e89b-12d3-a456-426614174003",
      "name": "Design",
      "bottleneck_score": 0.78,
      "description": "Design team is assigned to 12 high-priority objectives across 5 departments",
      "recommendation": "Consider hiring additional designers or reprioritizing objectives"
    }
  ]
}
```

## Error Handling

All API endpoints use standard HTTP status codes and return consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "statement",
        "message": "Field cannot be empty"
      }
    ]
  }
}
```

Common error codes:
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource conflict
- `500 Internal Server Error`: Server-side error

## Pagination

All list endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

Response format for paginated endpoints:
```json
{
  "items": [...],
  "total": 50,
  "page": 1,
  "limit": 20
}
```

## Filtering

Most list endpoints support filtering via query parameters. Common filters include:
- `timeframe`: Filter by time period
- `status`: Filter by status
- `priority`: Filter by priority
- Date ranges with `start_date` and `end_date`

## Implementation Guidelines

When implementing these API endpoints:

1. **Use FastAPI's dependency injection**
   - Inject services and repositories
   - Reuse common dependencies

2. **Implement proper validation**
   - Use Pydantic models for request/response validation
   - Add custom validators for business rules

3. **Optimize database queries**
   - Use SQLAlchemy efficiently
   - Implement pagination at the database level
   - Use appropriate indexes

4. **Document with OpenAPI**
   - Add detailed descriptions to all endpoints
   - Include example requests and responses
   - Document all possible error responses

5. **Implement proper error handling**
   - Use custom exception handlers
   - Return appropriate status codes
   - Provide detailed error messages

6. **Add authentication and authorization**
   - Implement JWT validation
   - Check permissions for each endpoint
   - Log authentication failures
