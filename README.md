# UAE Legal GraphRAG

[![Next.js](https://img.shields.io/badge/Next.js-15.5.0-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-green)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4.0-blue)](https://www.typescriptlang.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-green)](https://neo4j.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Advanced legal research platform powered by GraphRAG (Graph Retrieval-Augmented Generation) technology, specifically designed for UAE legal corpus analysis. This system combines knowledge graphs with AI agents to provide sophisticated legal research, contradiction detection, and harmonization suggestions.

## 🏗️ Architecture

### Frontend (Next.js)
- **Framework**: Next.js 15.5.0 with TypeScript
- **Styling**: Tailwind CSS with professional design system
- **Graph Visualization**: Interactive knowledge graphs
- **State Management**: React hooks with context patterns
- **API Integration**: RESTful APIs with real-time updates

### Backend (Python FastAPI)
- **Framework**: FastAPI with async/await support
- **Graph Database**: Neo4j with advanced Cypher queries
- **AI Integration**: Azure OpenAI with multi-agent orchestration
- **Embeddings**: Sentence Transformers for semantic search
- **Analysis**: Advanced legal pattern recognition and contradiction detection

### Key Features
- **Multi-Agent System**: Local, Global, and DRIFT GraphRAG agents
- **Real-time Analysis**: Live contradiction detection and harmonization
- **Interactive Graphs**: Dynamic knowledge graph visualization
- **Advanced Search**: Semantic and concept-based legal document retrieval
- **Professional UI**: Modern, responsive interface optimized for legal professionals

## 📁 Project Structure

```
uae-legal-graphrag/
├── backend/                    # Python FastAPI backend
│   ├── app/                   # Main application code
│   │   ├── api/              # API routes and endpoints
│   │   ├── rag/              # RAG service implementation
│   │   ├── services/         # External service integrations
│   │   ├── schemas/          # Pydantic data models
│   │   ├── utils/            # Utility functions
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/                # Comprehensive test suite
│   ├── scripts/              # Utility scripts
│   ├── requirements.txt      # Python dependencies
│   ├── requirements-test.txt # Test dependencies
│   ├── pytest.ini          # Test configuration
│   ├── Dockerfile           # Docker configuration
│   └── README.md           # Backend documentation
├── frontend/                  # Next.js frontend
│   ├── components/           # React components
│   ├── pages/               # Next.js pages
│   ├── styles/              # CSS styles
│   ├── utils/               # Frontend utilities
│   ├── types/               # TypeScript types
│   ├── lib/                 # Library code
│   ├── package.json         # Frontend dependencies
│   ├── tsconfig.json        # TypeScript config
│   ├── next.config.js       # Next.js config
│   ├── tailwind.config.js   # Tailwind config
│   └── README.md            # Frontend documentation
├── docker-compose.yml        # Docker orchestration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## 🚀 Quick Start

### Prerequisites
- **Node.js**: 18.0.0 or higher
- **Python**: 3.9 or higher
- **Neo4j**: 5.x database instance
- **Azure OpenAI**: API access and deployment

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd uae-legal-graphrag
   ```

2. **Set up the Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   
   # Set up environment variables
   cp .env.example .env
   # Edit .env with your configuration
   
   # Run the backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Set up the Frontend**
   ```bash
   cd ../frontend
   npm install
   
   # Set up environment variables
   cp .env.example .env.local
   # Edit .env.local with your configuration
   
   # Run the frontend
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Docker Setup

For a complete setup with Docker:

```bash
# Run the entire stack
docker-compose up

# Or run individual services
docker-compose up backend
docker-compose up frontend
docker-compose up neo4j
```

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
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
```

#### Frontend (.env.local)
```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_API_VERSION=v1

# Feature Flags
NEXT_PUBLIC_ENABLE_GRAPH_VISUALIZATION=true
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

## 🔍 API Endpoints

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

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest                    # Run all tests
pytest --cov=app         # Run with coverage
pytest -m unit           # Unit tests only
pytest -m integration    # Integration tests only
```

### Frontend Testing
```bash
cd frontend
npm test                 # Run all tests
npm run test:watch       # Run tests in watch mode
npm run test:coverage    # Run tests with coverage
```

## 📊 Available Scripts

### Backend Scripts
```bash
cd backend
# Development
uvicorn app.main:app --reload    # Start development server
pytest                           # Run tests
black app/ tests/                # Format code
flake8 app/ tests/               # Lint code

# Scripts
python scripts/build_faiss.py    # Build vector index
python scripts/seed_graph.py     # Seed Neo4j database
```

### Frontend Scripts
```bash
cd frontend
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript type checking
npm run format       # Format code with Prettier

# Testing
npm test             # Run tests
npm run test:watch   # Run tests in watch mode
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend Connection Issues**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Check Neo4j connection
   curl http://localhost:8000/config
   ```

2. **Frontend Build Issues**
   ```bash
   # Clear Next.js cache
   rm -rf .next
   npm install
   npm run dev
   ```

3. **Environment Variables**
   - Ensure all required environment variables are set
   - Check file permissions for .env files
   - Verify API endpoints are accessible

### Performance Optimization

1. **Backend Optimization**
   - Enable connection pooling for Neo4j
   - Implement response caching
   - Optimize database queries

2. **Frontend Optimization**
   - Enable Next.js optimizations
   - Use dynamic imports for large components
   - Implement proper error boundaries

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   # Backend tests
   cd backend && pytest
   
   # Frontend tests
   cd frontend && npm test
   ```
5. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
6. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request**

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions and support:
- Check the [Backend Documentation](backend/README.md)
- Check the [Frontend Documentation](frontend/README.md)
- Open an issue in the repository

## 🔄 Version History

- **v1.0.0** - Initial release with core GraphRAG functionality
- **v1.1.0** - Added multi-agent orchestration
- **v1.2.0** - Enhanced contradiction detection
- **v1.3.0** - Improved UI/UX and performance optimizations
- **v1.4.0** - Reorganized project structure for better maintainability
