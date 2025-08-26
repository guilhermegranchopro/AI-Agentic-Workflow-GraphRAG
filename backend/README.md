# GraphRAG Backend

This is the Python FastAPI backend for the UAE Legal GraphRAG application. It provides a comprehensive API for legal document retrieval, analysis, and graph-based knowledge extraction.

## Features

- **RAG (Retrieval Augmented Generation)**: Hybrid search combining vector and graph-based retrieval
- **Neo4j Integration**: Graph database for knowledge representation
- **OpenAI Integration**: Azure OpenAI for text generation and analysis
- **Rate Limiting**: Built-in request rate limiting
- **Comprehensive Testing**: Full test suite with pytest
- **Docker Support**: Containerized deployment

## Architecture

```
backend/
├── app/                    # Main application code
│   ├── api/               # API routes and endpoints
│   ├── rag/               # RAG service implementation
│   ├── services/          # External service integrations
│   ├── schemas/           # Pydantic data models
│   ├── utils/             # Utility functions
│   └── main.py           # FastAPI application entry point
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── requirements.txt       # Python dependencies
├── requirements-test.txt  # Test dependencies
├── pytest.ini           # Test configuration
├── Dockerfile            # Docker configuration
└── README.md            # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- Neo4j Database
- Azure OpenAI API access

### Installation

1. **Clone the repository and navigate to backend:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

Create a `.env` file in the backend directory:

```env
# Application
APP_ENV=development
LOG_LEVEL=INFO
DEBUG=true

# Azure OpenAI
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password

# Rate Limiting
RATE_LIMIT_MAX_REQUESTS=100
RATE_LIMIT_TIME_WINDOW=60

# Security
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## API Endpoints

### Core Endpoints

- `GET /` - Health check and API information
- `GET /health` - Detailed health status
- `GET /config` - Configuration information
- `GET /rate-limit-info` - Rate limiting status

### Chat Endpoints

- `POST /api/chat` - Main chat endpoint for legal queries
- `POST /api/analysis` - Legal document analysis
- `GET /api/debug/stats` - Debug statistics

### Request Examples

**Chat Request:**
```json
{
  "message": "What are the requirements for business registration in UAE?",
  "strategy": "hybrid",
  "max_results": 10
}
```

**Analysis Request:**
```json
{
  "query": "Analyze the UAE Civil Code",
  "analysis_type": "comprehensive",
  "include_graph": true,
  "max_depth": 3
}
```

## Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m api           # API tests only
```

### Test Structure

- **Unit Tests**: Fast, isolated tests with mocked dependencies
- **Integration Tests**: Tests requiring external services
- **API Tests**: Endpoint testing with FastAPI TestClient

## Development

### Code Style

The project uses:
- **Black** for code formatting
- **Flake8** for linting
- **MyPy** for type checking
- **isort** for import sorting

### Running Development Tools

```bash
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/

# Sort imports
isort app/ tests/
```

## Docker

### Build and Run

```bash
# Build the image
docker build -t graphrag-backend .

# Run the container
docker run -p 8000:8000 graphrag-backend
```

### Docker Compose

Use the main `docker-compose.yml` in the project root to run the full stack:

```bash
docker-compose up backend
```

## Scripts

### Available Scripts

- `scripts/build_faiss.py` - Build FAISS vector index
- `scripts/seed_graph.py` - Seed Neo4j with initial data

### Running Scripts

```bash
# Build vector index
python scripts/build_faiss.py

# Seed graph database
python scripts/seed_graph.py
```

## Monitoring and Logging

The application uses structured logging with the following features:

- **Request/Response Logging**: All API requests and responses
- **Performance Metrics**: Response times and throughput
- **Error Tracking**: Detailed error logging with stack traces
- **Health Monitoring**: System health and dependency status

## Security

- **Rate Limiting**: Prevents abuse with configurable limits
- **Input Validation**: All inputs validated with Pydantic
- **CORS**: Configurable Cross-Origin Resource Sharing
- **Authentication**: JWT-based authentication (if enabled)

## Performance

- **Async Operations**: All I/O operations are asynchronous
- **Connection Pooling**: Database connection pooling
- **Caching**: Response caching for frequently accessed data
- **Optimized Queries**: Efficient Neo4j and vector search queries

## Troubleshooting

### Common Issues

1. **Neo4j Connection Issues**
   - Verify Neo4j is running and accessible
   - Check connection credentials in `.env`

2. **OpenAI API Errors**
   - Verify API key and endpoint configuration
   - Check API quota and rate limits

3. **Import Errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

### Debug Mode

Enable debug mode for detailed logging:

```bash
export LOG_LEVEL=DEBUG
export DEBUG=true
uvicorn app.main:app --reload --log-level debug
```

## Contributing

1. Follow the existing code style and patterns
2. Add tests for new functionality
3. Update documentation for API changes
4. Ensure all tests pass before submitting

## License

This project is part of the UAE Legal GraphRAG application.
