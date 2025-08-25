# UAE Legal GraphRAG

[![Next.js](https://img.shields.io/badge/Next.js-15.5.0-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4.0-blue)](https://www.typescriptlang.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-green)](https://neo4j.com/)
[![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-orange)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Advanced legal research platform powered by GraphRAG (Graph Retrieval-Augmented Generation) technology, specifically designed for UAE legal corpus analysis. This system combines knowledge graphs with AI agents to provide sophisticated legal research, contradiction analysis, and harmonisation capabilities.

## Overview

UAE Legal GraphRAG is a comprehensive legal research platform that leverages:

- **Graph-based Knowledge Representation**: Legal documents stored in Neo4j for complex relationship modeling
- **Multi-Agent AI System**: Specialized agents for different types of legal analysis
- **Professional Government-Ready UI**: Clean, accessible interface suitable for official presentations
- **Real-time Analysis**: Live contradiction mining and legal harmonisation

## Architecture

### Frontend (Next.js + Tailwind CSS)

- **Framework**: Next.js 15.5 with Pages Router
- **Styling**: Tailwind CSS with professional dark theme
- **Layout Pattern**: `#app-scroll` container prevents white gaps and ensures proper scrolling
- **Components**: Responsive grid system with `Container` component for consistent width
- **Accessibility**: Professional contrast ratios and keyboard navigation

### API Routes (Pages API)

#### `/api/graph`
Returns nodes and edges from Neo4j for the Graph visualization page.
- **Dependencies**: Neo4j only
- **Authentication**: Environment-based
- **Response**: JSON graph data structure

#### `/api/assistant`
Orchestrator + agents (Local/Global/Drift GraphRAG) using Azure OpenAI.
- **Dependencies**: Azure OpenAI + Neo4j
- **Agents**: LocalGraphRagAgent, GlobalGraphRagAgent, DriftGraphRagAgent
- **Protocol**: Agent-to-Agent (A2A) envelope system

#### `/api/analysis`
Contradiction mining + harmonisation using the same retrieval patterns.
- **Dependencies**: Azure OpenAI + Neo4j
- **Agents**: ContradictionMiner, Harmoniser
- **Features**: Real-time progress updates, severity classification

#### `/api/health`
System diagnostics and health checks.
- **Checks**: Neo4j connectivity, Azure OpenAI availability
- **Response**: Comprehensive system status

### AI Agents

- **Orchestrator**: A2A envelope system for agent coordination
- **LocalGraphRagAgent**: Entity-focused retrieval and reasoning
- **GlobalGraphRagAgent**: Community-based analysis across legal domains
- **DriftGraphRagAgent**: Temporal analysis of legal evolution
- **ContradictionMiner**: Identifies conflicting legal provisions
- **Harmoniser**: Suggests resolution strategies for legal conflicts

### Data Layer

- **Neo4j Driver**: Singleton connection with connection pooling
- **GraphRAG Patterns**: Implemented in `lib/graph/graphRag.ts`
- **Retrieval Functions**: 
  - `retrieve()`: Basic concept retrieval
  - `searchByConcept()`: Enhanced semantic search
  - `findPotentialConflicts()`: Contradiction detection

### Environment Management

Grouped configuration getters prevent environment variable leakage:

- **`getNeo4jConfig()`**: Only NEO4J_* variables
- **`getAzureOpenAIConfig()`**: Only Azure OpenAI variables
- **Validation**: Strict validation with helpful error messages
- **Diagnostics**: Environment debugging endpoints

## Getting Started

### Prerequisites

- **Node.js**: 18.0 or higher
- **npm**: 8.0 or higher  
- **Neo4j**: 5.x database instance
- **Azure OpenAI**: API access with deployment

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd uae-legal-graphrag-neo4j-nextjs
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment setup**
   ```bash
   cp .env.example .env.local
   ```
   
   Fill in your actual values in `.env.local`:
   ```bash
   NEO4J_URI=bolt+s://your-neo4j-instance:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your-password
   NEO4J_DATABASE=neo4j
   
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
   AZURE_OPENAI_DEPLOYMENT=your-deployment-name
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open in browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Python Backend (Optional)

The project includes an advanced Python backend with FastAPI for enhanced AI capabilities:

1. **Create Python virtual environment**
   ```bash
   npm run py:venv
   ```

2. **Install Python dependencies**
   ```bash
   npm run py:install
   ```

3. **Start Python backend**
   ```bash
   npm run py:dev
   ```

The Python backend runs on port 8000 and provides advanced GraphRAG capabilities with sentence transformers and multi-agent systems.

## Scripts

- **`npm run dev`**: Start development server with Turbopack
- **`npm run build`**: Build production application
- **`npm run start`**: Start production server
- **`npm run lint`**: Run ESLint checks
- **`npm run lint:fix`**: Fix ESLint issues automatically
- **`npm run format`**: Format code with Prettier
- **`npm run format:check`**: Check code formatting
- **`npm run typecheck`**: Run TypeScript type checking
- **`npm run unused`**: Find unused exports with ts-prune
- **`npm run clean`**: Clean Next.js build cache
- **`npm run health`**: Quick health check endpoint test

### Python Backend Scripts

- **`npm run py:venv`**: Create Python virtual environment
- **`npm run py:install`**: Install Python dependencies
- **`npm run py:dev`**: Start Python FastAPI server
- **`npm run py:test`**: Run Python tests
- **`npm run py:fmt`**: Format Python code with black
- **`npm run py:lint`**: Lint Python code with flake8

## Pages & Endpoints

### Frontend Pages

- **`/`**: Overview dashboard with system statistics and health status
- **`/graph`**: Interactive graph visualization of legal relationships
- **`/assistant`**: AI-powered legal research assistant
- **`/ai-analysis`**: Legal contradiction analysis and harmonisation

### API Endpoints

- **`GET /api/health`**: System health and diagnostics
- **`GET /api/graph`**: Graph visualization data
- **`POST /api/assistant`**: AI assistant chat interface
- **`POST /api/analysis`**: Legal analysis processing
- **`GET /api/diagnostics/*`**: Various diagnostic endpoints

### Python Backend Endpoints

- **`GET /health`**: Python backend health check
- **`GET /env/present`**: Environment variables presence check
- **`POST /api/graphrag/query`**: Advanced GraphRAG queries
- **`POST /api/assistant/stream`**: Streaming multi-agent assistant
- **`POST /api/analysis/advanced`**: Advanced legal analysis

## Development Notes

### Scroll Container Pattern

The application uses a robust scroll container pattern:

```tsx
// _app.tsx
<div id="app-scroll" className="h-screen overflow-auto overscroll-contain">
  <Component {...pageProps} />
</div>
```

- **Prevents white gaps**: `overscroll-contain` prevents bouncing
- **Consistent scrolling**: Single scroll container for entire app
- **Mobile optimized**: Works with touch devices

### Layout Guidelines

- **Never use `100vw`**: Use `w-full` for full-width containers
- **Sticky headers**: Use `top-0` with proper `scroll-margin-top`
- **No `overflow-hidden`**: On page-level containers (only for true clipping)
- **Container component**: Use `<Container>` for consistent max-width

### Common Pitfalls

1. **Missing environment variables**: Check `.env.local` against `.env.example`
2. **Neo4j connectivity**: Ensure database is accessible and credentials are correct
3. **Scrolling issues**: Don't add `overflow-hidden` to page containers
4. **White gaps**: Verify `#app-scroll` container is properly configured

## Troubleshooting

### "Missing AZURE_OPENAI_DEPLOYMENT"
```bash
# Ensure deployment name is set in .env.local
AZURE_OPENAI_DEPLOYMENT=gpt-4
```

### "Neo4j not reachable"
1. Check Neo4j instance is running
2. Verify URI format: `bolt+s://host:7687` or `neo4j+s://host:7687`
3. Confirm credentials and network access

### "No scrolling"
1. Check `#app-scroll` container exists in `_app.tsx`
2. Remove `overflow-hidden` from page-level containers
3. Ensure no `height: 100vh` constraints on content

### "White gaps on mobile"
1. Verify `overscroll-contain` is applied to `#app-scroll`
2. Check for `100vw` usage (replace with `w-full`)
3. Ensure proper viewport meta tag in `_document.tsx`

### "Python backend not working"
1. Ensure Python 3.8+ is installed
2. Check virtual environment is activated
3. Verify all dependencies are installed: `npm run py:install`
4. Check port 8000 is available

### Environment Diagnostics

Use the diagnostic endpoints to troubleshoot configuration issues:

- **`/api/diagnostics/env`**: Check environment variable presence
- **`/api/diagnostics/debug`**: Detailed configuration status
- **`/api/diagnostics/neo4j`**: Neo4j connection test
- **`/health`**: Overall system health

## Project Structure

```
├── components/
│   ├── Layout.tsx           # Main layout wrapper
│   ├── Navigation.tsx       # Navigation header
│   ├── Sidebar.tsx         # Sidebar component
│   └── ui/
│       └── Container.tsx    # Width-constrained container
├── lib/
│   ├── config.ts           # Environment configuration
│   ├── ai/
│   │   └── orchestrator.ts # Agent coordination
│   └── graph/
│       ├── neo4j.ts       # Neo4j driver
│       └── graphRag.ts    # GraphRAG retrieval
├── pages/
│   ├── api/               # API routes
│   │   ├── analysis/      # Legal analysis endpoints
│   │   ├── assistant/     # AI assistant endpoints
│   │   ├── diagnostics/   # Debug endpoints
│   │   ├── graph/         # Graph data endpoints
│   │   ├── graph-data.ts  # Legacy graph endpoint
│   │   ├── health.ts      # Health check
│   │   └── stats-new.ts   # Statistics
│   ├── ai-analysis.tsx    # Analysis interface
│   ├── assistant.tsx      # AI assistant interface
│   ├── graph.tsx         # Graph visualization
│   ├── index.tsx         # Homepage
│   ├── _app.tsx          # App wrapper with scroll container
│   └── _document.tsx     # Document structure
├── python_backend/        # Python FastAPI backend
│   ├── app/
│   │   ├── agents/        # AI agents
│   │   ├── services/      # Business logic
│   │   └── config.py      # Python configuration
│   ├── main.py           # FastAPI entry point
│   └── requirements.txt  # Python dependencies
├── styles/
│   ├── globals.css       # Global styles with scroll support
│   └── globals-professional.css # Professional theme
├── types/
│   └── index.ts          # Shared type definitions
└── utils/
    ├── constants.ts      # Application constants
    └── helpers.ts        # Utility functions
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For questions and support, please refer to the project documentation or open an issue in the repository.
