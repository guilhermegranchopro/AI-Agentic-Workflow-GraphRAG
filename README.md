# UAE Legal GraphRAG - Complete Legal Knowledge Graph System

A comprehensive legal knowledge graph system for UAE law, featuring a Next.js frontend and Python FastAPI backend with Neo4j graph database integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Neo4j Database
- Azure OpenAI API access

### 1. Clone and Setup
```bash
git clone <repository-url>
cd internship_GraphRAG
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Frontend Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8012
```

### 4. Load Mock Data (Optional)
```bash
python load_mock_data.py
```

### 5. Start the Application
```bash
# Start both backend and frontend
python start.py

# Or start only backend
python start.py --backend-only

# Or start only frontend
python start.py --frontend-only
```

## 📁 Repository Structure

```
internship_GraphRAG/
├── start.py                 # 🚀 Unified startup script
├── .env                     # Environment configuration
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── load_mock_data.py      # Load mock UAE legal data
├── 
├── backend/               # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py       # FastAPI application
│   │   ├── api/
│   │   │   └── routes.py # API endpoints
│   │   ├── adapters/     # External service adapters
│   │   ├── rag/          # GraphRAG implementations
│   │   ├── schemas/      # Pydantic models
│   │   └── store/        # Data storage
│   ├── requirements.txt  # Python dependencies
│   └── Dockerfile        # Backend container
│
├── frontend/             # Next.js Frontend
│   ├── pages/
│   │   ├── index.tsx     # Overview page
│   │   ├── graph.tsx     # Graph visualization
│   │   ├── ai-analysis.tsx # AI analysis
│   │   ├── assistant.tsx # AI assistant
│   │   └── api/          # Frontend API routes
│   ├── components/       # React components
│   ├── package.json      # Node.js dependencies
│   └── next.config.js    # Next.js configuration
│
└── docs/                 # Documentation
    ├── setup.md          # Detailed setup guide
    ├── api.md            # API documentation
    └── architecture.md   # System architecture
```

## 🌟 Key Features

### 🔗 Smart Backend Integration
- **Automatic Fallback**: Frontend automatically uses mock data when backend is unavailable
- **Health Checks**: Continuous monitoring of backend availability
- **Real-time Switching**: Seamless transition between real and mock data

### 📊 Graph Visualization
- **Interactive Neo4j Graph**: Real-time visualization of legal knowledge graph
- **Node Filtering**: Filter by legal document types, entities, and relationships
- **Relationship Analysis**: Explore connections between legal concepts

### 🤖 AI-Powered Analysis
- **Legal Contradiction Detection**: Identify conflicting legal provisions
- **Harmonization Suggestions**: Propose legal harmonization opportunities
- **Intelligent Recommendations**: AI-driven legal insights

### 💬 AI Assistant
- **Context-Aware Responses**: Leverages Neo4j knowledge graph for accurate answers
- **Multiple Strategies**: Local, Global, and DRIFT GraphRAG implementations
- **Citation Support**: Provides source references for all responses

## 🛠️ Usage

### Starting the Application

#### Option 1: Unified Startup (Recommended)
```bash
python start.py
```
This starts both backend and frontend with automatic health monitoring.

#### Option 2: Individual Services
```bash
# Backend only
python start.py --backend-only

# Frontend only (with mock data fallback)
python start.py --frontend-only
```

### Accessing the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8012
- **Health Check**: http://localhost:8012/health
- **API Documentation**: http://localhost:8012/docs

### Pages Overview

1. **Overview** (`/`): Database statistics and system status
2. **Graph** (`/graph`): Interactive knowledge graph visualization
3. **AI Analysis** (`/ai-analysis`): Legal contradiction and harmonization analysis
4. **AI Assistant** (`/assistant`): Conversational AI with legal knowledge

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEO4J_URI` | Neo4j database URI | `bolt://localhost:7687` |
| `NEO4J_USER` | Neo4j username | `neo4j` |
| `NEO4J_PASSWORD` | Neo4j password | - |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | - |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | - |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | `gpt-4o` |
| `NEXT_PUBLIC_BACKEND_URL` | Backend URL for frontend | `http://localhost:8012` |

### Backend Configuration

The backend automatically:
- Connects to Neo4j database
- Initializes Azure OpenAI client
- Sets up FAISS vector database (optional)
- Performs health checks on startup

### Frontend Configuration

The frontend automatically:
- Detects backend availability
- Falls back to mock data when backend is unavailable
- Provides real-time status updates
- Maintains responsive UI regardless of backend state

## 🧪 Testing

### Backend Health Check
```bash
curl http://localhost:8012/health
```

### Frontend Health Check
```bash
curl http://localhost:3000/api/health
```

### Load Mock Data
```bash
python load_mock_data.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Backend Won't Start**
   - Check Neo4j connection
   - Verify Azure OpenAI credentials
   - Ensure virtual environment is activated

2. **Frontend Shows Mock Data**
   - Backend is not running or not accessible
   - Check backend health at http://localhost:8012/health
   - Verify network connectivity

3. **Neo4j Connection Issues**
   - Ensure Neo4j is running
   - Check credentials in `.env` file
   - Verify Neo4j URI format

### Logs

- **Backend Logs**: Visible in terminal when running `python start.py`
- **Frontend Logs**: Check browser console and terminal output
- **Neo4j Logs**: Check Neo4j database logs

## 📚 API Documentation

### Backend Endpoints

- `GET /health` - Health check
- `GET /api/graph` - Get graph data
- `POST /api/chat` - AI assistant chat
- `POST /api/analysis` - Legal analysis

### Frontend API Routes

- `GET /api/health` - Frontend health check
- `GET /api/graph` - Graph data (with fallback)
- `GET /api/stats-new` - Database statistics (with fallback)
- `POST /api/assistant` - AI assistant (with fallback)
- `POST /api/analysis` - Analysis (with fallback)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation
- Open an issue on GitHub

---

**Note**: This system is designed for demonstration and educational purposes. For production use, ensure proper security measures and compliance with relevant regulations.
