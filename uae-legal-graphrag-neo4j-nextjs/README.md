# UAE Legal GraphRAG

[![Next.js](https://img.shields.io/badge/Next.js-15.5.0-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4.0-blue)](https://www.typescriptlang.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-green)](https://neo4j.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Advanced legal research platform powered by GraphRAG (Graph Retrieval-Augmented Generation) technology, specifically designed for UAE legal corpus analysis. This system combines knowledge graphs with AI agents to provide sophisticated legal research, contradiction detection, and harmonization suggestions.

## 🏗️ Architecture

### Frontend (Next.js)
- **Framework**: Next.js 15.5.0 with TypeScript
- **Styling**: Tailwind CSS with professional design system
- **Graph Visualization**: Vis.js Network for interactive knowledge graphs
- **State Management**: React hooks with context patterns
- **API Integration**: RESTful APIs with Server-Sent Events (SSE)

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

## 🚀 Quick Start

### Prerequisites
- **Node.js**: 18.0.0 or higher
- **Python**: 3.8 or higher
- **Neo4j**: 5.x database instance
- **Azure OpenAI**: API access and deployment

### Automated Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd uae-legal-graphrag-neo4j-nextjs
   ```

2. **Run the setup script**
   ```powershell
   # Windows PowerShell
   .\setup.ps1
   ```

   The setup script will:
   - Check Python and Node.js installations
   - Create Python virtual environment
   - Install all dependencies
   - Set up development environment

### Manual Setup

1. **Install Node.js dependencies**
   ```bash
   npm install
   ```

2. **Create Python virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Neo4j Configuration
NEO4J_URI=bolt+s://<host>:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=********
NEO4J_DATABASE=neo4j

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Optional: Advanced Settings
NEO4J_MAX_CONNECTIONS=50
AZURE_OPENAI_MAX_TOKENS=4000
```

### Neo4j Setup

1. **Install Neo4j Desktop** or use Neo4j AuraDB
2. **Create a new database** or connect to existing one
3. **Import legal documents** using the provided Cypher scripts
4. **Verify connection** using the health check endpoint

## 🏃‍♂️ Running the Application

### Development Mode

1. **Start the Next.js frontend**
   ```bash
   npm run dev
   ```
   Frontend will be available at: http://localhost:3000

2. **Start the Python backend**
   ```bash
   npm run py:dev
   ```
   Backend will be available at: http://localhost:8000

3. **Verify services are running**
   ```bash
   # Check frontend health
   curl http://localhost:3000/api/health
   
   # Check backend health
   curl http://localhost:8000/health
   ```

### Production Mode

1. **Build the frontend**
   ```bash
   npm run build
   npm start
   ```

2. **Deploy the backend**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## 📊 Available Scripts

### Frontend (Next.js)
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run lint:fix     # Fix linting issues
npm run format       # Format code with Prettier
npm run typecheck    # Run TypeScript type checking
npm run unused       # Find unused exports
```

### Backend (Python)
```bash
npm run py:venv      # Create Python virtual environment
npm run py:install   # Install Python dependencies
npm run py:dev       # Start Python development server
npm run py:test      # Run Python tests
npm run py:fmt       # Format Python code with Black
npm run py:lint      # Lint Python code with Ruff
npm run py:typecheck # Type check Python code with MyPy
```

## 🔍 API Endpoints

### Frontend APIs (Next.js)
- `GET /api/health` - Health check
- `GET /api/diagnostics/env` - Environment diagnostics
- `GET /api/graph` - Graph data retrieval
- `POST /api/assistant` - AI assistant queries
- `POST /api/analysis` - Legal analysis requests

### Backend APIs (Python FastAPI)
- `GET /health` - Health check
- `GET /env/present` - Environment presence check
- `POST /api/graphrag/query` - GraphRAG queries
- `POST /api/analysis/advanced` - Advanced legal analysis
- `POST /api/assistant/stream` - Streaming assistant responses

## 🧪 Testing

### Frontend Testing
```bash
npm run test         # Run frontend tests
npm run test:watch   # Run tests in watch mode
```

### Backend Testing
```bash
npm run py:test      # Run Python tests
pytest python_backend/tests/ -v  # Verbose test output
```

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   # Clear Next.js cache
   npm run clean
   rm -rf .next
   npm install
   ```

2. **Python import errors**
   ```bash
   # Ensure virtual environment is activated
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **Neo4j connection issues**
   ```bash
   # Check Neo4j is running
   curl http://localhost:7474
   
   # Verify credentials in .env file
   # Test connection with health endpoint
   curl http://localhost:3000/api/diagnostics/neo4j
   ```

4. **Azure OpenAI configuration**
   ```bash
   # Check environment variables
   curl http://localhost:3000/api/diagnostics/env
   
   # Verify API key and endpoint
   # Ensure deployment is active
   ```

### Performance Optimization

1. **Enable caching**
   ```bash
   # Redis for session storage
   npm install redis
   ```

2. **Optimize database queries**
   ```bash
   # Use Neo4j query optimization
   # Implement connection pooling
   ```

3. **Frontend optimization**
   ```bash
   # Enable Next.js optimizations
   # Use dynamic imports for large components
   ```

## 📁 Project Structure

```
uae-legal-graphrag-neo4j-nextjs/
├── components/           # React components
│   ├── Layout.tsx       # Main layout component
│   ├── Navigation.tsx   # Navigation bar
│   └── ui/              # UI components
├── lib/                 # Core libraries
│   ├── config.ts        # Environment configuration
│   ├── graph/           # Graph-related utilities
│   │   ├── neo4j.ts     # Neo4j driver
│   │   └── graphRag.ts  # GraphRAG implementation
│   └── ai/              # AI-related utilities
│       └── orchestrator.ts # Multi-agent orchestrator
├── pages/               # Next.js pages and API routes
│   ├── api/             # API endpoints
│   ├── assistant.tsx    # AI assistant page
│   ├── graph.tsx        # Graph visualization
│   └── index.tsx        # Home page
├── python_backend/      # Python FastAPI backend
│   ├── app/             # Application modules
│   │   ├── agents/      # Multi-agent system
│   │   ├── services/    # Business logic services
│   │   └── config.py    # Configuration management
│   ├── main.py          # FastAPI application entry
│   └── requirements.txt # Python dependencies
├── styles/              # CSS stylesheets
├── types/               # TypeScript type definitions
├── utils/               # Utility functions
├── .env.example         # Environment variables template
├── package.json         # Node.js dependencies
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Run tests**
   ```bash
   npm run test
   npm run py:test
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

For questions and support, please refer to the project documentation or open an issue in the repository.

## 🔄 Version History

- **v1.0.0** - Initial release with core GraphRAG functionality
- **v1.1.0** - Added multi-agent orchestration
- **v1.2.0** - Enhanced contradiction detection
- **v1.3.0** - Improved UI/UX and performance optimizations
