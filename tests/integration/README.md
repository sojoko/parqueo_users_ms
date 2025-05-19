# Integration Tests

This directory contains integration tests for the parqueo_users_ms application. Unlike unit tests that use mocks, these integration tests interact with real database connections and services.

## Purpose

Integration tests verify that different components of the application work together correctly. They test the interaction between:

- Service layer
- Repository layer
- Database
- Other external services (if applicable)

## Structure

The integration tests follow the same structure as the unit tests:

```
integration/
├── __init__.py
├── services/
│   ├── __init__.py
│   ├── test_tickets_service.py
│   └── ... (other service tests)
└── ... (other test categories)
```

## Running Integration Tests

To run the integration tests, use the following command from the project root:

```bash
pytest tests/integration
```

To run a specific test file:

```bash
pytest tests/integration/services/test_tickets_service.py
```

## Best Practices

1. **Database Setup/Teardown**: Each test should set up its own test data and clean up after itself.
2. **Isolation**: Tests should be isolated and not depend on the state left by other tests.
3. **Real Connections**: Use real database connections instead of mocks.
4. **Comprehensive Testing**: Test all aspects of the service, including edge cases and error conditions.
5. **Descriptive Names**: Use descriptive test names that explain what is being tested.

## Differences from Unit Tests

- Integration tests use real database connections instead of mocks
- They test the interaction between multiple components
- They may be slower to run than unit tests
- They may require more setup and teardown code