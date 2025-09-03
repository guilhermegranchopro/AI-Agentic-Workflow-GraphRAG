# UAE Legal GraphRAG - A2A Protocol Implementation

## Project Overview

This repository contains the implementation of a **fully compliant A2A Protocol** system for the UAE Legal GraphRAG project, developed as part of a summer internship at EY Portugal's AI & Data team in August 2025. The system provides AI-powered legal research and analysis using GraphRAG (Graph-based Retrieval Augmented Generation) and multi-agent workflows, designed for eventual deployment to the UAE.

**Note: This project contains proprietary EY intellectual property and is intended for internal use only.**

## A2A Protocol Compliance

**YES, we have properly implemented the A2A Protocol** following the exact guidelines:

### What We Implemented:
1. **Discovery: publish an Agent Card** ✓
   - `/.well-known/agent.json` - Public agent card for discovery
   - `/.well-known/agent` - Alternative discovery endpoint
   - `/.well-known/health` - Well-known health check

2. **Choose a transport and implement the core methods** ✓
   - `POST /a2a/v1/message:send` - Send messages to agents
   - `POST /a2a/v1/message:stream` - Stream task updates (SSE)
   - `GET /a2a/v1/tasks/{task_id}` - Get task status

3. **Auth & security** ✓
   - Bearer token authentication
   - API key authentication
   - Security schemes defined in agent card

4. **Streaming & long-running tasks** ✓
   - Server-Sent Events (SSE) for real-time updates
   - Task status polling for long-running operations

5. **Compliance testing** ✓
   - Comprehensive test suite
   - A2A Protocol validation

## Technical Overview

### Architecture
The UAE Legal GraphRAG system is built as a multi-agent AI platform that leverages advanced graph database technology and large language models to provide comprehensive legal research capabilities. The system architecture follows modern microservices principles with clear separation of concerns.

### Technology Stack Justification

#### Backend Framework: FastAPI
- **Performance**: FastAPI is built on Starlette and Pydantic, providing near-native performance with async support
- **Type Safety**: Built-in Pydantic validation ensures data integrity and reduces runtime errors
- **API Documentation**: Automatic OpenAPI/Swagger documentation generation
- **Modern Python**: Full support for Python 3.11+ features including type hints and async/await
- **Production Ready**: Used by major companies for high-traffic applications

#### Database: Neo4j
- **Graph-Native**: Purpose-built for graph data, essential for legal knowledge representation
- **Cypher Query Language**: Intuitive graph querying that mirrors natural language
- **ACID Compliance**: Ensures data consistency and reliability
- **Scalability**: Handles complex relationships and large datasets efficiently
- **Legal Domain Fit**: Perfect for representing legal entities, relationships, and precedents

#### Vector Database: FAISS
- **Performance**: Optimized for similarity search with sub-linear time complexity
- **Memory Efficiency**: Effective memory usage for large-scale vector operations
- **Integration**: Seamless integration with Python ecosystem
- **Legal Text Search**: Excellent for semantic search across legal documents

#### AI Services: Azure OpenAI
- **Enterprise Grade**: Meets EY's security and compliance requirements
- **GPT-4o Model**: State-of-the-art language model for legal analysis
- **Azure Integration**: Native integration with Microsoft cloud services
- **Compliance**: Meets enterprise security and privacy standards

#### Frontend: Next.js
- **React Ecosystem**: Leverages mature React component library
- **Server-Side Rendering**: Improved performance and SEO
- **TypeScript Support**: Type safety for frontend development
- **Modern Development**: Hot reloading and modern build tools

#### A2A Protocol Implementation
- **Industry Standard**: Follows open protocol for agent interoperability
- **Future-Proof**: Enables integration with other AI agents and systems
- **Compliance**: Meets all specification requirements for production use

## Project Structure

```
├── backend/                 # FastAPI backend with A2A Protocol
│   ├── app/
│   │   ├── api/            # API endpoints including A2A Protocol
│   │   ├── agents/         # AI agents (Local/Global/DRIFT GraphRAG)
│   │   ├── schemas/        # Pydantic schemas including A2A Protocol
│   │   └── main.py         # Main FastAPI application
│   ├── tests/              # Test suite including A2A Protocol tests
│   ├── data/               # Data storage
│   └── .env                # Backend environment variables
├── frontend/               # Next.js frontend application
├── docs/                   # Project documentation
├── .env                    # Root environment variables
├── .env.template           # Environment configuration template
├── requirements.txt        # Python dependencies (root level)
└── neo4j_knowledge_graph.dump # Neo4j database dump with mock UAE legal data
```

## Prerequisites

### Required Software
- **Python 3.11+** with pip
- **Node.js 18+** and npm (Next.js with TypeScript and Tailwind CSS)
- **Neo4j Desktop** application
- **Git** for version control

### System Requirements
- **Memory**: Minimum 8GB RAM (16GB recommended)
- **Storage**: 10GB+ available disk space
- **Network**: Outbound access to Azure OpenAI and Neo4j

## Installation and Setup

### Step 1: Neo4j Database Setup

1. **Install Neo4j Desktop**
   - Download from [neo4j.com/download](https://neo4j.com/download/)
   - Install and launch Neo4j Desktop

2. **Create Neo4j Instance**
   - Click "New" → "Create a Local Graph"
   - Choose Neo4j 5.15+ version
   - Set password (remember this for .env file)
   - Start the instance

3. **Import Knowledge Graph Data**
   - In Neo4j Desktop, click on your instance
   - Go to "Manage" → "Import"
   - Upload the `neo4j_knowledge_graph.dump` file
   - This populates the database with mock UAE legal system data

### Step 2: Environment Configuration

1. **Create .env Template**
   ```bash
   cp .env.template .env
   ```

2. **Configure .env File**
   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   AZURE_OPENAI_API_VERSION=2024-02-15-preview

   # Neo4j Configuration
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_neo4j_password_here

   # Application Configuration
   APP_ENV=development
   PORT=8000
   ```

### Step 3: Python Environment Setup

1. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

2. **Activate Virtual Environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Frontend Dependencies

1. **Navigate to Frontend Directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js Dependencies**
   ```bash
   npm install
   ```

## Running the Project

### Start Backend Server

1. **Activate Virtual Environment**
   ```bash
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

2. **Start FastAPI Server**
   ```bash
   cd backend
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Verify Backend**
   - Health check: http://localhost:8000/health
   - A2A Protocol: http://localhost:8000/.well-known/agent.json
   - API docs: http://localhost:8000/docs

### Start Frontend Application

1. **New Terminal Window**
   ```bash
   cd frontend
   npm run dev
   ```

2. **Access Frontend**
   - Application: http://localhost:3000
   - Graph visualization: http://localhost:3000/graph
   - AI Assistant: http://localhost:3000/assistant
   - Legal Analysis: http://localhost:3000/ai-analysis

## Testing A2A Protocol

### Run Compliance Tests
```bash
cd backend
python tests/test_a2a_protocol.py
```

### Manual Testing
```bash
# Test agent discovery
curl http://localhost:8000/.well-known/agent.json

# Test A2A health
curl http://localhost:8000/a2a/health

# Test message sending
curl -X POST http://localhost:8000/a2a/v1/message:send \
  -H "Content-Type: application/json" \
  -d '{"message": {"role": "user", "parts": [{"kind": "text", "text": "Test"}], "metadata": {"skill_id": "ai_assistant"}}}'
```

## Available Skills

- **`local_graphrag`** - Local graph neighborhood traversal
- **`global_graphrag`** - Global graph analysis
- **`drift_graphrag`** - Dynamic relevance tracking
- **`legal_analysis`** - Contradiction detection & harmonization
- **`ai_assistant`** - AI-powered legal research assistant

## A2A Protocol Endpoints

### Agent Discovery (Public)
- `GET /.well-known/agent.json` - Public agent card (REQUIRED)
- `GET /.well-known/agent` - Alternative discovery endpoint
- `GET /.well-known/health` - Well-known health check

### Core A2A Protocol
- `POST /a2a/v1/message:send` - Send messages to agents (REQUIRED)
- `POST /a2a/v1/message:stream` - Stream task updates (SSE) (REQUIRED)
- `GET /a2a/v1/tasks/{task_id}` - Get task status (REQUIRED)
- `GET /a2a/v1/card` - Authenticated agent card
- `GET /a2a/health` - A2A Protocol health check

## Security

- Bearer token authentication
- API key authentication
- Rate limiting
- CORS protection
- Environment variable security

## Documentation

- **[A2A Protocol Implementation](README_A2A_PROTOCOL.md)** - Complete A2A Protocol documentation
- **[Startup Guide](STARTUP_GUIDE.md)** - How to get started
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture details

## Project Status

**FULL A2A PROTOCOL COMPLIANCE ACHIEVED**

Your UAE Legal GraphRAG system is now a **fully compliant A2A Protocol agent** that can interoperate with other A2A-compliant agents and follows industry standards for agent-to-agent communication.

## Support and Maintenance

For questions about the A2A Protocol implementation, please refer to the [A2A Protocol documentation](README_A2A_PROTOCOL.md) or check the [A2A Protocol specification](https://a2a-protocol.org/dev/specification/).

## License and Proprietary Information

This project contains proprietary EY intellectual property and is intended for internal use only. All rights reserved by EY.

---

**Developed by EY Portugal AI & Data Team - Summer Internship 2025**
