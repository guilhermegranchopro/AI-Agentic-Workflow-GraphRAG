# GraphRAG Test Suite

This directory contains the comprehensive test suite for the GraphRAG application. The tests are designed to ensure the reliability, functionality, and performance of all components.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration and shared fixtures
├── test_api.py              # API endpoint tests
├── test_schemas.py          # Pydantic schema validation tests
├── test_rate_limiter.py     # Rate limiter utility tests
├── test_openai_service.py   # OpenAI service tests
├── test_neo4j_service.py    # Neo4j service tests
├── rag/
│   └── test_rag_service.py  # RAG service tests
└── README.md               # This file
```

## Test Categories

### Unit Tests (`@pytest.mark.unit`)
- Fast, isolated tests that don't require external services
- Test individual functions and classes
- Use mocks to isolate dependencies

### Integration Tests (`@pytest.mark.integration`)
- Tests that require external services (Neo4j, OpenAI)
- Test component interactions
- May be slower and require specific environment setup

### API Tests (`@pytest.mark.api`)
- Test FastAPI endpoints
- Validate request/response schemas
- Test error handling and edge cases

### Service Tests
- **RAG Service** (`@pytest.mark.rag`): Test RAG functionality
- **Neo4j Service** (`@pytest.mark.neo4j`): Test graph database operations
- **OpenAI Service** (`@pytest.mark.openai`): Test AI model interactions

## Running Tests

### Prerequisites

1. Install test dependencies:
```bash
pip install -r requirements-test.txt
```

2. Set up environment variables (or use the defaults in `conftest.py`):
```bash
export APP_ENV=test
export LOG_LEVEL=DEBUG
export AZURE_OPENAI_API_KEY=your-test-key
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your-password
```

### Basic Test Execution

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run specific test file:
```bash
pytest tests/test_api.py
```

Run specific test function:
```bash
pytest tests/test_api.py::test_root_endpoint
```

### Test Filtering

Run only unit tests:
```bash
pytest -m unit
```

Run only integration tests:
```bash
pytest -m integration
```

Run API tests only:
```bash
pytest -m api
```

Skip slow tests:
```bash
pytest -m "not slow"
```

### Coverage Reporting

Run tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

Generate HTML coverage report:
```bash
pytest --cov=app --cov-report=html
```

### Parallel Execution

Run tests in parallel (requires pytest-xdist):
```bash
pytest -n auto
```

### Test Output Formats

Generate HTML test report:
```bash
pytest --html=test-report.html
```

Generate JUnit XML report:
```bash
pytest --junitxml=test-results.xml
```

## Test Configuration

### Pytest Configuration (`pytest.ini`)

The `pytest.ini` file configures:
- Test discovery patterns
- Custom markers
- Default command-line options
- Environment variables
- Warning filters

### Shared Fixtures (`conftest.py`)

Common fixtures available to all tests:
- `test_app`: FastAPI application instance
- `client`: TestClient for API testing
- `mock_openai_client`: Mocked OpenAI client
- `mock_neo4j_service`: Mocked Neo4j service
- `rate_limiter`: Rate limiter instance
- Sample data fixtures for requests and responses

## Writing Tests

### Test Naming Conventions

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test Structure

```python
import pytest
from unittest.mock import Mock, patch

class TestExampleService:
    """Test example service functionality."""
    
    @pytest.mark.asyncio
    async def test_example_function(self, mock_dependency):
        """Test example function with mocked dependency."""
        # Arrange
        mock_dependency.return_value = "expected_result"
        
        # Act
        result = await example_function("test_input")
        
        # Assert
        assert result == "expected_result"
        mock_dependency.assert_called_once_with("test_input")
```

### Using Fixtures

```python
def test_with_fixture(client, sample_data):
    """Test using shared fixtures."""
    response = client.post("/api/endpoint", json=sample_data)
    assert response.status_code == 200
```

### Async Testing

For async functions, use the `@pytest.mark.asyncio` decorator:

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result is not None
```

### Mocking External Services

```python
@patch("app.services.external_service.ExternalClient")
def test_with_mock(mock_client):
    """Test with mocked external service."""
    mock_client.return_value.method.return_value = "mocked_result"
    # Test implementation
```

## Test Data

### Sample Data Fixtures

The `conftest.py` file provides sample data fixtures:
- `sample_chat_request`: Valid chat request data
- `sample_chat_response`: Valid chat response data
- `sample_rag_response`: Valid RAG response data
- `sample_graph_response`: Valid graph response data

### Using Sample Data

```python
def test_with_sample_data(sample_chat_request):
    """Test using sample data fixture."""
    request = ChatRequest(**sample_chat_request)
    assert request.message == "What is the UAE Civil Code?"
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v1
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure the app package is in the Python path
2. **Async Test Failures**: Use `@pytest.mark.asyncio` for async tests
3. **Mock Issues**: Check that mocks are applied to the correct import path
4. **Environment Variables**: Verify test environment variables are set

### Debug Mode

Run tests in debug mode:
```bash
pytest --pdb
```

Run specific test with debugger:
```bash
pytest tests/test_api.py::test_specific_function --pdb
```

### Verbose Output

Get detailed test output:
```bash
pytest -vvv
```

Show local variables on failure:
```bash
pytest -l
```

## Performance Testing

### Benchmark Tests

Run performance benchmarks:
```bash
pytest --benchmark-only
```

### Load Testing

For load testing, consider using tools like:
- `locust` for HTTP load testing
- `pytest-benchmark` for performance benchmarking
- Custom load testing scripts

## Contributing

### Adding New Tests

1. Follow the existing naming conventions
2. Use appropriate markers for test categorization
3. Add comprehensive docstrings
4. Include both positive and negative test cases
5. Mock external dependencies appropriately

### Test Quality Checklist

- [ ] Tests are isolated and don't depend on each other
- [ ] External services are properly mocked
- [ ] Edge cases and error conditions are covered
- [ ] Tests are fast and efficient
- [ ] Clear assertions and error messages
- [ ] Proper use of fixtures and setup/teardown

### Code Coverage

Maintain high code coverage:
- Aim for >90% line coverage
- Focus on critical business logic
- Test error handling paths
- Include integration tests for key workflows

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pydantic Testing](https://pydantic-docs.helpmanual.io/usage/testing/)
