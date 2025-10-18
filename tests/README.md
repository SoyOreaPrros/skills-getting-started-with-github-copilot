# Tests

This directory contains the test suite for the Mergington High School Activities API.

## Running Tests

### Quick Start
```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=src --cov-report=term-missing

# Run tests with HTML coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Using the Test Script
```bash
# Make executable (if not already)
chmod +x run_tests.sh

# Run comprehensive tests with coverage
./run_tests.sh
```

## Test Structure

### `test_api.py`
Main test file containing:

- **TestRootEndpoint**: Tests for the root `/` endpoint
- **TestActivitiesEndpoint**: Tests for `/activities` endpoint
- **TestSignupEndpoint**: Tests for `/activities/{name}/signup` endpoint
- **TestUnregisterEndpoint**: Tests for `/activities/{name}/unregister` endpoint
- **TestIntegrationScenarios**: End-to-end workflow tests
- **TestErrorHandling**: Edge cases and error conditions

### `conftest.py`
Shared test configuration and fixtures.

### `__init__.py`
Makes the tests directory a Python package.

## Test Coverage

The test suite achieves 100% code coverage of the main application code.

## Test Features

- **Fixtures**: Automatic test data reset between tests
- **Integration Tests**: Complete user workflow testing
- **Error Handling**: Tests for all error conditions
- **URL Encoding**: Tests for special characters in URLs
- **Edge Cases**: Empty parameters, case sensitivity, etc.

## Dependencies

Required packages (in `requirements.txt`):
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing support
- `pytest-cov` - Coverage reporting
- `httpx` - HTTP client for FastAPI testing

## Test Data

Each test uses a fresh copy of the initial activities data:
- Chess Club (2 participants)
- Programming Class (2 participants)  
- Gym Class (2 participants)

Tests verify that additional activities are properly added during signup operations.