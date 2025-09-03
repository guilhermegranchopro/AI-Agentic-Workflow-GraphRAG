# UAE Legal GraphRAG

## Project Overview

This repository contains the implementation of a fully compliant A2A Protocol system for the UAE Legal GraphRAG project, developed as part of a summer internship at EY Portugal's AI & Data team in August 2025. The system provides AI-powered legal research and analysis using GraphRAG (Graph-based Retrieval Augmented Generation) and multi-agent workflows, designed for eventual deployment to the UAE.

### Core Functionality

The UAE Legal GraphRAG system is a comprehensive legal research platform that combines:

- **Graph Database Technology**: Neo4j-based knowledge graph representing UAE legal system entities and relationships
- **AI-Powered Analysis**: Azure OpenAI GPT-4o integration for intelligent legal research and analysis
- **Multi-Agent Workflows**: Orchestrated AI agents specializing in different aspects of legal research
- **Vector Search**: FAISS-based semantic search for legal document similarity and relevance
- **Real-Time Visualization**: Interactive graph exploration and legal relationship mapping
- **A2A Protocol Compliance**: Industry-standard agent interoperability for future integration

### Frontend Application Pages

#### Overview Dashboard
- **Purpose**: Central hub providing system status and quick access to all features
- **Features**: System health indicators, recent activities, quick navigation to core tools
- **Use Case**: Initial landing page for users to understand system capabilities

#### Graph Visualization
- **Purpose**: Interactive exploration of the UAE legal knowledge graph
- **Features**: 
  - Real-time Neo4j graph visualization with 83+ legal entities
  - 103+ legal relationships and connections
  - Interactive node filtering and relationship exploration
  - Zoom, pan, and search functionality
  - Legal domain categorization and color coding
- **Use Case**: Legal researchers exploring connections between laws, regulations, and legal entities

#### AI Assistant
- **Purpose**: Intelligent legal research assistant powered by GraphRAG technology
- **Features**:
  - Natural language legal queries with context-aware responses
  - Multiple retrieval strategies (local, global, hybrid)
  - Citation system with source legal documents
  - Conversation history and context preservation
  - Multi-agent coordination for comprehensive responses
- **Use Case**: Legal professionals seeking quick answers to complex legal questions

#### AI Analysis
- **Purpose**: Advanced legal analysis including contradiction detection and harmonization
- **Features**:
  - Legal contradiction identification across different regulations
  - Priority-based analysis and risk assessment
  - Harmonization recommendations for conflicting legal provisions
  - Compliance gap analysis
  - Detailed legal reasoning and explanations
- **Use Case**: Legal compliance officers and regulatory analysts

### Knowledge Graph Coverage

The system includes comprehensive coverage of UAE legal domains:
- **Corporate Tax Law**: 2022 and 2024 regulations with detailed provisions
- **Data Protection**: GDPR-compliant data handling requirements
- **Court System**: Judicial structure and procedural rules
- **Business Licensing**: Commercial registration and licensing requirements
- **Environmental Regulations**: Sustainability and compliance standards
- **Digital Innovation**: Technology and innovation laws
- **Labor Law**: Employment regulations and worker rights
- **Financial Services**: Banking and financial regulations

**Note: This project contains proprietary EY intellectual property and is intended for internal use only.**

## Multi-Agent AI System

The UAE Legal GraphRAG system implements a sophisticated multi-agent architecture that coordinates specialized AI agents for comprehensive legal research:

### Agent Architecture

#### Orchestrator Agent
- **Role**: Central coordinator managing workflow execution and agent coordination
- **Responsibilities**: 
  - Route user queries to appropriate specialized agents
  - Coordinate multi-agent workflows for complex legal analysis
  - Manage conversation context and history
  - Implement A2A Protocol message handling

#### Specialized GraphRAG Agents

**Local GraphRAG Agent**
- **Purpose**: Focused legal research using local graph neighborhood traversal
- **Strategy**: Explores immediate connections and relationships around specific legal entities
- **Use Case**: Detailed analysis of specific legal provisions and their direct implications

**Global GraphRAG Agent**
- **Purpose**: Comprehensive legal research using global graph analysis
- **Strategy**: Analyzes the entire knowledge graph for broad legal patterns and connections
- **Use Case**: Understanding legal system-wide implications and cross-domain relationships

**DRIFT GraphRAG Agent**
- **Purpose**: Dynamic relevance and importance tracking for legal analysis
- **Strategy**: Identifies time-sensitive legal changes and evolving regulatory priorities
- **Use Case**: Staying current with legal developments and regulatory updates

#### AI Analysis Agent
- **Purpose**: Advanced legal analysis including contradiction detection and harmonization
- **Capabilities**: 
  - Identify conflicting legal provisions across different regulations
  - Assess compliance risks and gaps
  - Provide harmonization recommendations
  - Generate detailed legal reasoning and explanations

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

#### Development Tools
- **TypeScript**: Type-safe development for frontend components
- **Tailwind CSS**: Utility-first CSS framework for modern UI design
- **Vis.js**: Interactive graph visualization library
- **React Hooks**: Modern React patterns for state management
- **FastAPI**: High-performance Python web framework
- **Pydantic**: Data validation and settings management
- **SQLAlchemy**: Database ORM and connection management
- **Loguru**: Advanced logging and monitoring

## Data and Knowledge Representation

### Knowledge Graph Structure
The system maintains a comprehensive knowledge graph representing the UAE legal system:

- **Legal Entities**: Laws, regulations, court decisions, government bodies, and legal concepts
- **Relationships**: Hierarchical structures, cross-references, amendments, and legal dependencies
- **Metadata**: Effective dates, jurisdiction, legal status, and regulatory authority
- **Content**: Full text of legal provisions, explanatory notes, and implementation guidelines

### Data Sources and Coverage
- **Primary Legislation**: Federal laws, decrees, and ministerial decisions
- **Regulatory Framework**: Administrative regulations and implementation guidelines
- **Judicial Precedents**: Court decisions and legal interpretations
- **International Standards**: Alignment with international legal frameworks
- **Industry-Specific Regulations**: Sector-specific legal requirements and compliance standards

### Data Quality and Maintenance
- **Regular Updates**: Continuous monitoring of legal changes and regulatory updates
- **Validation**: Multi-source verification of legal accuracy and currency
- **Version Control**: Tracking of legal document versions and amendment history
- **Compliance Monitoring**: Regular assessment of regulatory compliance status

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
│   ├── extra/              # Research documentation and findings
│   │   ├── A2A Protocol Guide.docx
│   │   ├── Technology Stack Analysis.docx
│   │   ├── GraphRAG Research.docx
│   │   ├── Cost Analysis.docx
│   │   ├── Future Ideas.docx
│   │   └── UAE Legal AI GraphRAG Presentation.pdf
│   ├── A2A_PROTOCOL_IMPLEMENTATION.md
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT_GUIDE.md
│   └── USER_GUIDE.md
├── .env                    # Root environment variables
├── .env.template           # Environment configuration template
├── requirements.txt        # Python dependencies (root level)
├── neo4j_knowledge_graph.dump # Neo4j database dump with mock UAE legal data
├── UAE Legal AI GraphRAG Presentation.pptm # Final project presentation
└── Recording of the Demo.mp4 # Full-stack application demonstration
```

## Prerequisites

### Required Software
- **Python 3.11+** with pip
- **Node.js 18+** and npm
- **Next.js 15+** with Turbopack enabled
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

### Core Documentation
- **[A2A Protocol Implementation](docs/A2A_PROTOCOL_IMPLEMENTATION.md)** - Complete A2A Protocol documentation
- **[Architecture](docs/ARCHITECTURE.md)** - System architecture details
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Production deployment instructions
- **[API Reference](docs/API_REFERENCE.md)** - Complete API documentation
- **[User Guide](docs/USER_GUIDE.md)** - End-user documentation and tutorials

### Research Documentation & Presentations
- **[Research Documentation](docs/extra/)** - Comprehensive research findings and analysis
  - A2A Protocol research and implementation guide
  - Technology stack analysis and comparisons
  - GraphRAG methodology research
  - Cost analysis and projections
  - Future development ideas and roadmap
- **[Final Presentation](UAE Legal AI GraphRAG Presentation.pptm)** - PowerPoint presentation of the complete project
- **[Demo Recording](Recording of the Demo.mp4)** - Full demonstration of the working Next.js application

## Project Status

**FULL A2A PROTOCOL COMPLIANCE ACHIEVED**

Your UAE Legal GraphRAG system is now a **fully compliant A2A Protocol agent** that can interoperate with other A2A-compliant agents and follows industry standards for agent-to-agent communication.

## Deployment and Production

### Development Environment
- **Local Development**: Python virtual environment with hot reload
- **Frontend Development**: Next.js development server with Turbopack
- **Database**: Local Neo4j instance for development and testing
- **Environment Configuration**: .env files for local configuration management

### Production Considerations
- **Containerization**: Docker support for consistent deployment environments
- **Environment Management**: Secure configuration management for production
- **Monitoring**: Health checks, logging, and performance monitoring
- **Scaling**: Horizontal scaling support for high-traffic deployments
- **Security**: Production-grade authentication and authorization

### Cloud Deployment
- **Azure Integration**: Native integration with Microsoft Azure services
- **Container Registry**: Support for Azure Container Registry deployment
- **Managed Services**: Integration with Azure OpenAI and other managed services
- **Monitoring**: Azure Monitor integration for production monitoring

## Support and Maintenance

For questions about the A2A Protocol implementation, please refer to the [A2A Protocol documentation](docs/A2A_PROTOCOL_IMPLEMENTATION.md) or check the [A2A Protocol specification](https://a2a-protocol.org/dev/specification/).

## License and Proprietary Information

This project contains proprietary EY intellectual property and is intended for internal use only. All rights reserved by EY.

---

**Developed by [Guilherme Grancho](https://www.linkedin.com/in/guilhermegrancho/) for EY Portugal AI & Data Team - August Internship 2025**
