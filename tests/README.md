# Unit Tests for Parqueo Users Microservice

This directory contains unit tests for the Parqueo Users Microservice. The tests are organized by component type:

- `routes/`: Tests for API route handlers
- `services/`: Tests for service layer implementations

## Test Structure

The tests follow a standard structure:

- Route tests use FastAPI's TestClient to simulate HTTP requests and mock the service layer
- Service tests mock the database session and test the business logic in isolation
- All tests follow the Arrange-Act-Assert pattern

## Running the Tests

To run all tests, execute the following command from the project root:

```bash
pytest tests/
```

To run tests for a specific component:

```bash
# Run all route tests
pytest tests/routes/

# Run all service tests
pytest tests/services/

# Run tests for a specific file
pytest tests/routes/test_aprendices_route.py
pytest tests/services/test_aprendices_service.py
```

## Test Coverage

To run tests with coverage reporting:

```bash
# Install pytest-cov if not already installed
pip install pytest-cov

# Run tests with coverage
pytest --cov=routes --cov=services tests/

# Generate HTML coverage report
pytest --cov=routes --cov=services tests/ --cov-report=html
```

## Dependencies

The tests require the following packages:

- pytest
- pytest-cov (for coverage reporting)
- fastapi
- httpx (used by TestClient)

Install them with:

```bash
pip install pytest pytest-cov fastapi httpx
```

## Adding New Tests

When adding new tests:

1. Follow the existing pattern for route and service tests
2. Use descriptive test names that indicate what is being tested
3. Include both success and failure test cases
4. Mock external dependencies to isolate the component being tested