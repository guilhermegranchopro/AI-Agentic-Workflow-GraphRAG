# UAE Legal GraphRAG - AI-Powered Legal System

> **EY Portugal Summer Internship Project**  
> **Developer:** Guilherme Grancho  
> **Client:** Government of the United Arab Emirates  
> **Objective:** First AI-powered legal system implementation worldwide

## 🎯 Project Overview

This project represents a groundbreaking initiative by the Government of the United Arab Emirates to become the first country in the world to implement AI in their legal system. Developed as part of an EY Portugal summer internship, this GraphRAG (Graph Retrieval-Augmented Generation) system provides intelligent legal analysis, contradiction detection, and harmonization recommendations.

### 🌟 Key Features

- **AI Assistant**: Intelligent legal query processing with context-aware responses
- **AI Analysis**: Automated contradiction detection and harmonization suggestions
- **Knowledge Graph Visualization**: Interactive exploration of UAE legal framework
- **Multi-Agent Workflow**: Local, Global, and DRIFT agents for comprehensive analysis
- **Real-time Processing**: Server-sent events for live analysis updates

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Knowledge     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Graph (Neo4j) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│  Azure OpenAI   │◄─────────────┘
                        └─────────────────┘
```

### Technology Stack

- **Frontend**: Next.js, TypeScript, Tailwind CSS, Vis.js
- **Backend**: FastAPI, Python, Pydantic, SQLModel
- **Database**: Neo4j (Knowledge Graph), SQLite (Event Store)
- **AI Services**: Azure OpenAI (GPT-4, Embeddings)
- **Deployment**: Docker, Docker Compose

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Docker and Docker Compose
- Azure OpenAI API access

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd internship_GraphRAG
   ```

2. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your configuration:
   ```env
   # Neo4j Configuration
   NEO4J_URI=bolt+s://<host>:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password
   
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
   AZURE_OPENAI_DEPLOYMENT=your_deployment_name
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Or start manually**
   ```bash
   # Backend
   cd backend
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn app.main_simple:app --reload --port 8001
   
   # Frontend (in new terminal)
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8001
   - API Documentation: http://localhost:8001/docs

## 📊 Features Overview

### 1. AI Assistant
- **Intelligent Query Processing**: Context-aware responses based on UAE legal framework
- **Multi-Source Citations**: References to relevant laws, regulations, and precedents
- **Confidence Scoring**: Transparent confidence levels for all responses
- **Strategy Tracking**: Shows which AI agents contributed to the response

### 2. AI Analysis
- **Contradiction Detection**: Automated identification of legal conflicts
- **Harmonization Suggestions**: AI-powered recommendations for legal alignment
- **Priority Classification**: High, medium, and low priority issues
- **Impact Assessment**: Detailed analysis of legal implications

### 3. Knowledge Graph
- **Interactive Visualization**: Explore 300+ legal entities and relationships
- **Dynamic Filtering**: Filter by node types and relationship categories
- **Real-time Statistics**: Live updates of graph metrics
- **Comprehensive Coverage**: UAE Constitution, Federal Laws, Regulations, and more

### 4. Overview Dashboard
- **System Statistics**: Real-time metrics and performance indicators
- **Database Health**: Connection status and data integrity checks
- **Recent Activity**: Latest queries and analysis results

## 🔧 Development

### Project Structure

```
internship_GraphRAG/
├── frontend/                 # Next.js application
│   ├── pages/               # React pages and API routes
│   ├── components/          # Reusable React components
│   ├── lib/                 # Utility libraries
│   ├── types/               # TypeScript type definitions
│   └── styles/              # CSS and styling
├── backend/                 # FastAPI application
│   ├── app/                 # Main application code
│   │   ├── api/            # API endpoints
│   │   ├── adapters/       # External service adapters
│   │   ├── rag/            # GraphRAG implementation
│   │   ├── schemas/        # Pydantic models
│   │   └── utils/          # Utility functions
│   ├── tests/              # Test suite
│   └── scripts/            # Utility scripts
├── docker-compose.yml       # Container orchestration
└── README.md               # This file
```

### Available Scripts

**Frontend:**
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run typecheck    # TypeScript type checking
```

**Backend:**
```bash
# Development
uvicorn app.main_simple:app --reload --port 8001

# Testing
pytest

# Formatting
ruff check --fix
black backend
```

## 🧪 Testing

### Frontend Testing
```bash
cd frontend
npm run test
```

### Backend Testing
```bash
cd backend
pytest
```

### API Testing
```bash
# Test AI Assistant
curl -X POST http://localhost:3000/api/assistant \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"What are the requirements for starting a business in UAE?"}]}'

# Test AI Analysis
curl -X POST http://localhost:3000/api/analysis \
  -H "Content-Type: application/json" \
  -d '{"query":"VAT rates and tax regulations"}'

# Test Graph API
curl http://localhost:3000/api/graph?max_nodes=50
```

## 📈 Performance

- **Response Time**: < 2 seconds for AI queries
- **Graph Rendering**: Supports up to 300 nodes with smooth interactions
- **Concurrent Users**: Designed for multiple simultaneous users
- **Scalability**: Microservices architecture for horizontal scaling

## 🔒 Security

- **Environment Variables**: Secure configuration management
- **API Rate Limiting**: Token-bucket algorithm per IP
- **Input Validation**: Comprehensive request validation
- **CORS Configuration**: Proper cross-origin resource sharing
- **Error Handling**: Graceful error responses without data leakage

## 🌍 Deployment

### Production Deployment

1. **Build Docker images**
   ```bash
   docker-compose build
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Environment-specific configuration**
   - Production: `docker-compose.prod.yml`
   - Development: `docker-compose.yml`
   - Testing: `docker-compose.test.yml`

### Cloud Deployment

The system is designed for deployment on:
- **Azure**: Native integration with Azure OpenAI
- **AWS**: Compatible with AWS services
- **Google Cloud**: Supports GCP infrastructure

## 📚 API Documentation

### Core Endpoints

- `GET /api/graph` - Retrieve knowledge graph data
- `POST /api/assistant` - AI legal assistant queries
- `POST /api/analysis` - Legal contradiction analysis
- `GET /api/health` - System health check
- `GET /api/stats-new` - System statistics

### Response Formats

All API responses follow consistent JSON schemas with:
- Success/error status indicators
- Structured data payloads
- Metadata and pagination information
- Error codes and messages

## 🤝 Contributing

This project was developed as part of an EY Portugal internship. For contributions:

1. Follow the existing code style and patterns
2. Add comprehensive tests for new features
3. Update documentation for API changes
4. Use conventional commit messages

## 📄 License

This project is proprietary software developed for the Government of the United Arab Emirates through EY Portugal.

## 👨‍💻 Author

**Guilherme Grancho**  
*EY Portugal Summer Intern*  
*AI Legal Systems Specialist*

## 🙏 Acknowledgments

- **EY Portugal**: Internship opportunity and mentorship
- **UAE Government**: Vision and requirements for AI-powered legal systems
- **Azure OpenAI**: Advanced AI capabilities and support
- **Neo4j**: Knowledge graph technology and expertise

## 📞 Contact

For questions about this project:
- **EY Portugal**: [Contact Information]
- **UAE Government**: [Official Channels]

---

*This project represents a significant milestone in the integration of artificial intelligence with legal systems, positioning the UAE as a global leader in legal technology innovation.*
