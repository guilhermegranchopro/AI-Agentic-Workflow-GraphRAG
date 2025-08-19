# UAE Legal GraphRAG - Next.js Application

A modern, scalable legal research platform combining Next.js frontend with GraphRAG (Graph Retrieval-Augmented Generation) backend for comprehensive UAE legal analysis.

## 🏗️ Architecture

- **Frontend**: Next.js 14 with React 18 and TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Backend**: Python GraphRAG engine with Neo4j graph database
- **AI**: Azure OpenAI integration for legal analysis
- **Graph**: Neo4j with Graph Data Science (GDS) for community detection

## 🚀 Features

### Core RAG Capabilities
- **Local RAG**: Entity-centric legal search with temporal filtering
- **Global RAG**: Community-based analysis using Graph Data Science
- **DRIFT RAG**: Dynamic temporal analysis for tracking legal evolution

### User Interface
- **Dashboard**: System overview with health monitoring and statistics
- **Graph Visualization**: Interactive knowledge graph exploration
- **Legal Assistant**: AI-powered chat with multi-agent reasoning
- **Responsive Design**: Mobile-first, accessible interface

### Technical Features
- **Real-time Updates**: Live system status and query processing
- **Type Safety**: Full TypeScript integration
- **Component Architecture**: Reusable, maintainable UI components
- **API Integration**: RESTful endpoints for Python backend communication

## � Prerequisites

- **Node.js**: v18+ (v20+ recommended)
- **Python**: 3.11+
- **Neo4j**: Desktop or Aura instance
- **Azure OpenAI**: Active subscription with GPT-4 and embeddings

## 🛠️ Installation

### 1. Clone and Setup

```bash
git clone <repository-url>
cd uae-legal-graphrag-neo4j-nextjs
```

### 2. Node.js Dependencies

```bash
npm install
```

### 3. Python Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

```bash
# Copy environment template
cp .env .env.local

# Edit .env.local with your credentials
```

Required environment variables:

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://your-instance.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o
EMBEDDING_DIM=3072

# Application Settings
ENABLE_GDS=true
APP_DEFAULT_ASOF=2025-08-19
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=development
```

## 🚀 Running the Application

### Development Mode

```bash
# Start the Next.js development server
npm run dev
```

The application will be available at **http://localhost:3000**

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Automated Setup (Windows)

For automated environment setup on Windows:

```powershell
# Run the setup script
.\setup.ps1
```

This script will:
- Check Python and Node.js installations
- Create and activate virtual environment
- Install all dependencies
- Set up environment configuration

## 🏃‍♂️ Quick Start

1. **Clone the repository**
2. **Run the setup script**: `.\setup.ps1` (Windows) or follow manual installation steps
3. **Configure environment**: Edit `.env.local` with your credentials
4. **Start development**: `npm run dev`
5. **Open browser**: Navigate to `http://localhost:3000`

## 📖 Usage Guide

### Dashboard
- **System Health**: Monitor Neo4j connectivity and service status
- **Database Statistics**: View document, entity, and relationship counts
- **Performance Metrics**: Track query response times and system load

### RAG Operations
- **Local RAG**: Search within specific entity neighborhoods
- **Global RAG**: Query across community-detected clusters
- **DRIFT RAG**: Temporal analysis with dynamic community exploration

### Graph Visualization
- **Interactive Network**: Explore entity relationships and communities
- **Temporal Filtering**: View graph state at specific time points
- **Community Detection**: Visualize Louvain algorithm results

### AI Assistant
- **Multi-Agent System**: Orchestrated responses using specialized agents
- **Legal Context**: UAE-specific legal knowledge and interpretation
- **Citation Support**: Source attribution for all generated responses

## 🛠️ Development

### Project Structure

```
├── components/          # Reusable React components
│   ├── Layout.tsx      # Main application layout
│   ├── Navigation.tsx  # Top navigation bar
│   └── Sidebar.tsx     # Side navigation menu
├── pages/              # Next.js pages and API routes
│   ├── index.tsx       # Dashboard homepage
│   ├── local.tsx       # Local RAG interface
│   ├── global.tsx      # Global RAG interface
│   ├── drift.tsx       # DRIFT RAG interface
│   ├── graph.tsx       # Graph visualization
│   ├── assistant.tsx   # AI assistant chat
│   └── api/           # API endpoints
├── python-backend/     # Python GraphRAG engine
│   ├── agents/        # AI agent implementations
│   ├── graph/         # Graph operations and queries
│   ├── embeddings/    # Azure OpenAI integration
│   └── utils/         # Utility functions
├── styles/            # Global CSS and Tailwind config
└── types/             # TypeScript type definitions
```

### Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm start           # Start production server

# Code Quality
npm run lint        # Run ESLint
npm run type-check  # Run TypeScript compiler

# Python Environment
.\.venv\Scripts\Activate.ps1  # Activate virtual environment (Windows)
source .venv/bin/activate     # Activate virtual environment (macOS/Linux)
pip install -r requirements.txt  # Install Python dependencies
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEO4J_URI` | Neo4j database connection string | ✅ |
| `NEO4J_USER` | Neo4j username | ✅ |
| `NEO4J_PASSWORD` | Neo4j password | ✅ |
| `NEO4J_DATABASE` | Neo4j database name | ✅ |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI service endpoint | ✅ |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | ✅ |
| `AZURE_OPENAI_CHAT_DEPLOYMENT` | GPT model deployment name | ✅ |
| `AZURE_OPENAI_EMBEDDING_DEPLOYMENT` | Embedding model deployment name | ✅ |
| `EMBEDDING_DIM` | Embedding dimension (3072 for text-embedding-3-large) | ✅ |
| `ENABLE_GDS` | Enable Neo4j Graph Data Science | Optional |
| `APP_DEFAULT_ASOF` | Default temporal filter date | Optional |
| `LOG_LEVEL` | Application logging level | Optional |

## 🧪 Testing

### Running Tests

```bash
# Activate Python environment
.\.venv\Scripts\Activate.ps1

# Run Python tests
pytest tests/

# Run specific test files
pytest tests/test_db_connect.py
pytest tests/test_vector_knn.py
```

### Health Checks

The application provides several health check endpoints:

- `GET /api/health` - Overall system health
- `GET /api/stats` - Database statistics
- `GET /api/graph-data` - Graph connectivity test

## 🔧 Troubleshooting

### Common Issues

1. **Python not found**
   - Ensure Python 3.11+ is installed and in PATH
   - Use `py` command on Windows instead of `python`

2. **Neo4j connection failed**
   - Verify Neo4j is running and accessible
   - Check credentials in `.env.local`
   - Ensure firewall allows connections on port 7687

3. **Azure OpenAI errors**
   - Verify API key and endpoint in `.env.local`
   - Check deployment names match your Azure configuration
   - Ensure sufficient quota for API calls

4. **Module import errors**
   - Activate Python virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

### Debug Mode

Enable debug logging by setting:

```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit with descriptive messages
5. Push to your fork and create a pull request

### Code Style

- **TypeScript**: Follow ESLint configuration
- **Python**: Use Black formatter and follow PEP 8
- **React**: Use functional components with hooks
- **CSS**: Use Tailwind utility classes

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🆘 Support

For support and questions:
- Check this README and troubleshooting section
- Review the [original Streamlit documentation](../uae-legal-graphrag-neo4j-streamlit/README.md)
- Open an issue in the repository
- **Database**: Neo4j with GraphRAG capabilities
- **AI Services**: Azure OpenAI for embeddings and chat

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.8+ with existing GraphRAG backend
- Neo4j database with UAE legal data
- Azure OpenAI API access

## ⚡ Quick Start

### 1. Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Or with yarn
yarn install
```

### 2. Environment Configuration

Copy the environment variables from your existing Streamlit setup:

```bash
# The .env.local file should already be copied from the Streamlit version
# Verify it contains:
# NEO4J_URI=your_neo4j_uri
# NEO4J_USERNAME=your_username
# NEO4J_PASSWORD=your_password
# AZURE_OPENAI_API_KEY=your_api_key
# AZURE_OPENAI_ENDPOINT=your_endpoint
# AZURE_OPENAI_CHAT_DEPLOYMENT=your_chat_deployment
# AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment
```

### 3. Start Development Server

```bash
npm run dev
# Or
yarn dev
```

Visit [http://localhost:3000](http://localhost:3000) to see the application.

## 📁 Project Structure

```
uae-legal-graphrag-neo4j-nextjs/
├── components/                 # Reusable React components
│   ├── Layout.tsx             # Main application layout
│   ├── Navigation.tsx         # Top navigation bar
│   └── Sidebar.tsx            # Left sidebar navigation
├── pages/                     # Next.js pages (file-based routing)
│   ├── api/                   # API routes
│   │   ├── health.ts          # System health check
│   │   ├── stats.ts           # Database statistics
│   │   ├── local-rag.ts       # Local RAG search
│   │   ├── global-rag.ts      # Global RAG search
│   │   ├── drift-rag.ts       # DRIFT RAG search
│   │   └── agents/            # AI Agents API endpoints
│   ├── index.tsx              # Home page
│   ├── local.tsx              # Local RAG interface
│   ├── global.tsx             # Global RAG interface
│   ├── drift.tsx              # DRIFT RAG interface
│   ├── graph.tsx              # Graph visualization
│   └── assistant.tsx          # AI Legal Assistant
├── lib/                       # Utility libraries
├── types/                     # TypeScript type definitions
│   └── index.ts               # Main type definitions
├── styles/                    # Global styles
│   └── globals.css            # Tailwind CSS + custom styles
├── python-backend/            # Copied Python backend for API integration
└── public/                    # Static assets
```

## 🔧 Architecture

### Frontend Architecture
- **Next.js Pages Router**: File-based routing for all application pages
- **API Routes**: Server-side API endpoints that interface with Python backend
- **Component-Based**: Modular React components with TypeScript
- **Responsive Design**: Mobile-first design with Tailwind CSS

### Backend Integration
- **Python Bridge**: API routes execute Python scripts from the existing backend
- **Process Isolation**: Each API call spawns isolated Python processes
- **Error Handling**: Comprehensive error handling and logging
- **Type Safety**: Full TypeScript interfaces for all data exchanges

### State Management
- **React Hooks**: useState and useEffect for local component state
- **No Global State**: Simple architecture without Redux/Zustand complexity
- **API-First**: All data fetched via API calls to maintain consistency

## 🎨 UI/UX Features

### Design System
- **Consistent Styling**: Custom Tailwind component classes
- **Professional Theme**: Blue primary color scheme suitable for legal applications
- **Responsive Layout**: Adaptive design for desktop, tablet, and mobile
- **Loading States**: Smooth loading animations and progress indicators

### User Experience
- **Search Interfaces**: Intuitive search forms with advanced filtering
- **Real-time Feedback**: Immediate visual feedback for user actions
- **Error Handling**: User-friendly error messages and recovery suggestions
- **Performance**: Optimized rendering and efficient API calls

## 🚀 Available Scripts

```bash
# Development
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server

# Code Quality
npm run lint         # Run ESLint
npm run type-check   # TypeScript type checking

# Maintenance
npm install          # Install dependencies
npm update           # Update dependencies
```

## 📊 API Endpoints

### System APIs
- `GET /api/health` - System health check
- `GET /api/stats` - Database statistics

### Search APIs
- `POST /api/local-rag` - Local RAG search
- `POST /api/global-rag` - Global RAG search
- `POST /api/drift-rag` - DRIFT RAG search

### AI Agent APIs
- `POST /api/agents/query` - AI agent system query
- `GET /api/agents/status` - Agent system status

### Graph APIs
- `POST /api/graph/search` - Graph search and visualization
- `GET /api/graph/stats` - Graph statistics

## 🔐 Security

- **Environment Variables**: Sensitive data stored in .env.local
- **API Validation**: Input validation on all API endpoints
- **Error Sanitization**: No sensitive information in error messages
- **CORS Protection**: Appropriate CORS headers for API routes

## 🚧 Development Notes

### Code Style
- **TypeScript**: Strict type checking enabled
- **ESLint**: Configured with Next.js recommended rules
- **Prettier**: Code formatting with Tailwind CSS plugin

### Performance Optimization
- **Next.js Optimization**: Automatic code splitting and optimization
- **Image Optimization**: Next.js Image component for optimized images
- **Bundle Analysis**: Use `npm run build` to analyze bundle size

## 📈 Monitoring

- **Health Checks**: Automatic system health monitoring
- **Error Logging**: Comprehensive error logging in API routes
- **Performance Metrics**: Built-in Next.js analytics support

## 🔄 Migration from Streamlit

This Next.js application maintains **100% feature parity** with the original Streamlit application:

### Migrated Features
✅ **Home Dashboard** - Overview, health checks, database stats  
✅ **Local RAG** - Entity-centric search with temporal filtering  
✅ **Global RAG** - Community-based analysis  
✅ **DRIFT RAG** - Community-guided local search  
✅ **Graph Visualization** - Interactive graph exploration  
✅ **Legal Assistant AI** - Multi-agent system integration  

### Improvements Over Streamlit
- **Better Performance**: Faster page loads and interactions
- **Mobile Responsive**: Works perfectly on all devices
- **Professional UI**: Modern, polished interface design
- **Better UX**: Improved user experience and workflows
- **Extensibility**: Easier to add new features and customize

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of the UAE Legal GraphRAG system for legal research and analysis.

---

**🎯 Ready to scale!** This Next.js application is designed to handle thousands of documents efficiently while providing a superior user experience for legal professionals.
