# UAE Legal GraphRAG - AI-Powered Legal System

> **EY Portugal Summer Internship Project**  
> **Developer:** Guilherme Grancho  
> **Client:** Government of the United Arab Emirates  
> **Objective:** First AI-powered legal system implementation worldwide

## 🎯 Project Overview

This project represents a groundbreaking initiative by the Government of the United Arab Emirates to become the first country in the world to implement AI in their legal system. Developed as part of an EY Portugal summer internship, this GraphRAG (Graph Retrieval-Augmented Generation) system provides intelligent legal analysis, contradiction detection, and harmonization recommendations.

### 🏗️ Architecture

- **Frontend**: Next.js 15.5.0 with TypeScript, Tailwind CSS, and Vis.js
- **Backend**: FastAPI with Python 3.11+
- **Database**: Neo4j (Knowledge Graph) + SQLite (Event Store)
- **AI Services**: Azure OpenAI (GPT-4o) with graceful fallback
- **Vector Database**: FAISS for semantic search
- **GraphRAG**: Multi-agent system (Local, Global, DRIFT, Hybrid)

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Node.js 18 or higher
- Neo4j Database (optional - system works with mock data)

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd internship_GraphRAG

# Create unified virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Key settings:
# - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
# - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint
# - AZURE_OPENAI_DEPLOYMENT: Your deployment name (e.g., gpt-4o)
# - NEO4J_URI: Your Neo4j connection string (optional)
```

### 3. Start the Application

#### Option A: Using Startup Scripts (Recommended)

```bash
# Terminal 1: Start Backend
python start_backend.py

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

#### Option B: Manual Startup

```bash
# Terminal 1: Start Complex Backend
uvicorn backend.app.main:app --host 0.0.0.0 --port 8012 --reload

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8012
- **Health Check**: http://localhost:8012/health
- **API Documentation**: http://localhost:8012/docs

## 🎯 Features

### 1. **AI Assistant**
- Intelligent legal Q&A with UAE legal framework
- Multi-agent GraphRAG system
- Context-aware responses with citations
- Graceful fallback to mock responses

### 2. **Knowledge Graph Visualization**
- Interactive 3D graph visualization
- 29+ entity types and 30+ relationship types
- Real-time filtering and search
- Comprehensive UAE legal knowledge base

### 3. **AI Analysis**
- Contradiction detection in legal documents
- Harmonization recommendations
- Automated legal analysis
- Suggested queries for common scenarios

### 4. **Dashboard**
- Real-time system health monitoring
- Database statistics
- Service status indicators
- Performance metrics

## 🔧 Backend Services

### Complex Mode (Default)
- **Azure OpenAI Integration**: GPT-4o with graceful fallback
- **Neo4j Knowledge Graph**: Real-time legal data queries
- **FAISS Vector Database**: Semantic search capabilities
- **A2A Protocol**: Agent-to-agent communication
- **Event Store**: SQLite-based message tracking
- **Rate Limiting**: Request throttling and monitoring
- **Telemetry**: Comprehensive logging and metrics

### Fallback Mode
- Automatic fallback to mock responses
- No external dependencies required
- Perfect for demonstrations and testing

## 📊 API Endpoints

### Core Endpoints
- `GET /health` - System health check
- `GET /docs` - Interactive API documentation
- `GET /openapi.json` - OpenAPI specification

### GraphRAG Endpoints
- `POST /api/v1/chat` - AI Assistant chat
- `POST /api/v1/analyze` - Legal analysis
- `GET /api/v1/graph` - Knowledge graph data
- `GET /api/v1/stats` - System statistics

## 🛠️ Development

### Project Structure
```
internship_GraphRAG/
├── .venv/                 # Unified virtual environment
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── adapters/      # External service adapters
│   │   ├── api/           # API routes
│   │   ├── rag/           # GraphRAG implementation
│   │   ├── schemas/       # Pydantic models
│   │   ├── store/         # Data storage
│   │   └── utils/         # Utilities
│   ├── data/              # Data files
│   └── requirements.txt   # Python dependencies
├── frontend/              # Next.js frontend
│   ├── pages/             # Next.js pages
│   ├── components/        # React components
│   ├── lib/               # Utilities and types
│   └── package.json       # Node.js dependencies
├── .env                   # Unified environment configuration
├── start_backend.py       # Backend startup script
└── README.md              # This file
```

### Environment Variables
```env
# Application Settings
APP_ENV=development
PORT=8000

# Backend Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8012

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-10-21

# Neo4j (Optional)
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password
```

## 🧪 Testing

### Backend Testing
```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Run tests
cd backend
pytest

# Test specific components
python test_azure_openai.py
```

### Frontend Testing
```bash
cd frontend
npm test
npm run build
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build individually
docker build -t uae-legal-graphrag-backend ./backend
docker build -t uae-legal-graphrag-frontend ./frontend
```

### Production Configuration
- Set `APP_ENV=production`
- Configure proper CORS settings
- Set up SSL/TLS certificates
- Configure production database
- Set up monitoring and logging

## 🔒 Security

- Environment variable protection
- CORS configuration
- Rate limiting
- Input validation
- Error handling without information leakage

## 📈 Performance

- Async/await throughout the stack
- Connection pooling for databases
- Caching strategies
- Optimized vector search
- Efficient graph queries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is proprietary software developed for the Government of the United Arab Emirates through EY Portugal.

## 👨‍💻 Author

**Guilherme Grancho**  
EY Portugal Summer Intern  
*UAE Legal GraphRAG Project*

## 🙏 Acknowledgments

- EY Portugal for the internship opportunity
- Government of the United Arab Emirates for the project
- Azure OpenAI for AI services
- Neo4j for graph database technology
- The open-source community for various libraries and tools

---

**Status**: ✅ Production Ready  
**Last Updated**: August 2025  
**Version**: 1.0.0
