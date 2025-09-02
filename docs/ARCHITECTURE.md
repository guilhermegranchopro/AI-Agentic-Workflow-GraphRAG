# System Architecture

This document describes the architecture of the UAE Legal GraphRAG system, including the technology stack, component interactions, and data flow.

## 🏗️ High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Mock Data     │    │   Neo4j Graph   │    │  Azure OpenAI   │
│   (Fallback)    │    │   Database      │    │     (LLM)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🎯 Core Components

### 1. Frontend (Next.js)

**Technology Stack:**
- **Framework**: Next.js 15.5.0
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Graph Visualization**: Vis.js
- **State Management**: React Hooks

**Key Features:**
- **Responsive Design**: Mobile-first approach
- **Real-time Updates**: Live data synchronization
- **Graceful Degradation**: Automatic fallback to mock data
- **Interactive Graphs**: 3D graph visualization with filtering

**Pages:**
- `/` - Overview dashboard
- `/graph` - Knowledge graph visualization
- `/ai-analysis` - Legal analysis interface
- `/assistant` - AI chat interface

### 2. Backend (FastAPI)

**Technology Stack:**
- **Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: Neo4j (Graph), SQLite (Events)
- **AI Services**: Azure OpenAI
- **Vector Search**: FAISS (optional)

**Key Features:**
- **GraphRAG Implementation**: Multi-agent system
- **Real-time Processing**: Async/await throughout
- **Health Monitoring**: Comprehensive health checks
- **Error Handling**: Graceful error recovery

**API Endpoints:**
- `GET /health` - System health check
- `GET /api/graph` - Graph data retrieval
- `POST /api/chat` - AI assistant chat
- `POST /api/analysis` - Legal analysis

### 3. Data Layer

#### Neo4j Knowledge Graph
- **Purpose**: Store legal knowledge as a graph
- **Schema**: Nodes (legal entities) + Relationships (legal connections)
- **Query Language**: Cypher
- **Features**: Complex graph queries, relationship traversal

#### SQLite Event Store
- **Purpose**: Store A2A (Agent-to-Agent) communication events
- **Schema**: Event logs with timestamps and metadata
- **Features**: Lightweight, embedded, ACID compliance

#### FAISS Vector Database (Optional)
- **Purpose**: Semantic search and similarity matching
- **Features**: High-performance vector operations
- **Fallback**: System works without FAISS

### 4. AI Services

#### Azure OpenAI Integration
- **Model**: GPT-4o
- **Purpose**: Natural language processing and generation
- **Features**: Context-aware responses, citation support
- **Fallback**: Mock responses when unavailable

#### GraphRAG Agents
- **LocalGraphRAG**: Local neighborhood analysis
- **GlobalGraphRAG**: Global graph traversal
- **DRIFTGraphRAG**: Dynamic relevance and importance tracking

## 🔄 Data Flow

### 1. Frontend Request Flow

```
User Action → Frontend API Route → Backend Health Check → 
Backend API Call → Response Processing → UI Update
```

### 2. Backend Processing Flow

```
API Request → Authentication → Service Validation → 
GraphRAG Processing → Neo4j Query → AI Enhancement → 
Response Formatting → API Response
```

### 3. Fallback Mechanism

```
Backend Unavailable → Health Check Failure → 
Mock Data Activation → Frontend Fallback → 
User Experience Maintained
```

## 🛡️ Security & Reliability

### Security Features
- **Environment Variables**: Sensitive data protection
- **CORS Configuration**: Cross-origin request handling
- **Input Validation**: Pydantic model validation
- **Error Handling**: No information leakage

### Reliability Features
- **Health Checks**: Continuous service monitoring
- **Graceful Degradation**: Fallback mechanisms
- **Connection Pooling**: Database connection management
- **Timeout Handling**: Request timeout management

## 📊 Performance Considerations

### Frontend Optimization
- **Code Splitting**: Lazy loading of components
- **Static Generation**: Pre-rendered pages where possible
- **Caching**: Browser and CDN caching strategies
- **Bundle Optimization**: Tree shaking and minification

### Backend Optimization
- **Async Processing**: Non-blocking operations
- **Connection Pooling**: Database connection reuse
- **Caching**: Response caching where appropriate
- **Query Optimization**: Efficient Neo4j queries

## 🔧 Configuration Management

### Environment Variables
```env
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# AI Services
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
NEXT_PUBLIC_BACKEND_URL=http://localhost:8012
```

### Configuration Hierarchy
1. **Environment Variables** (highest priority)
2. **Configuration Files** (default values)
3. **Hard-coded Defaults** (fallback)

## 🚀 Deployment Architecture

### Development Environment
```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (localhost:3000) │    │   (localhost:8012) │
└─────────────────┘    └─────────────────┘
```

### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   Application   │    │   Database      │
│   (Nginx)       │◄──►│   Servers       │◄──►│   Cluster       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔍 Monitoring & Observability

### Health Checks
- **Backend Health**: `/health` endpoint
- **Database Connectivity**: Neo4j connection status
- **AI Service Status**: Azure OpenAI availability
- **Frontend Status**: Frontend API health checks

### Logging
- **Structured Logging**: JSON-formatted logs
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Request Tracking**: Unique request IDs
- **Performance Metrics**: Response times and throughput

### Metrics
- **API Response Times**: Endpoint performance
- **Error Rates**: Failure tracking
- **Resource Usage**: CPU, memory, database connections
- **User Activity**: Page views and interactions

## 🔄 Development Workflow

### Local Development
1. **Setup**: `python setup.py`
2. **Start Services**: `python start.py`
3. **Development**: Hot reload enabled
4. **Testing**: Automated tests and manual testing

### Code Organization
```
internship_GraphRAG/
├── frontend/           # Next.js frontend
├── backend/            # FastAPI backend
├── scripts/            # Utility scripts
├── docs/               # Documentation
├── start.py           # Unified startup script
├── setup.py           # Setup script
└── cleanup_repo.py    # Repository cleanup script
```

## 🔮 Future Enhancements

### Planned Features
- **Multi-tenant Support**: Multiple legal jurisdictions
- **Advanced Analytics**: Legal trend analysis
- **Mobile Application**: Native mobile app
- **API Rate Limiting**: Request throttling
- **Advanced Caching**: Redis integration

### Scalability Considerations
- **Horizontal Scaling**: Multiple backend instances
- **Database Sharding**: Neo4j cluster deployment
- **CDN Integration**: Global content delivery
- **Microservices**: Service decomposition

---

This architecture provides a robust, scalable, and maintainable foundation for the UAE Legal GraphRAG system, with clear separation of concerns and comprehensive fallback mechanisms.
