# UAE Legal GraphRAG - Next.js Application

A sophisticated legal research platform powered by GraphRAG (Graph Retrieval-Augmented Generation) with multi-agent orchestration, built on Next.js, Neo4j, and Azure OpenAI.

## 🌟 Features

- **Multi-Agent AI System**: Orchestrated AI agents using Local, Global, and DRIFT strategies
- **GraphRAG Implementation**: Advanced retrieval from Neo4j knowledge graphs
- **Interactive Graph Visualization**: Real-time exploration of legal knowledge networks
- **Streaming AI Responses**: Server-sent events for real-time AI conversations
- **Markdown Rendering**: Beautiful formatting of AI responses with syntax highlighting
- **Dark Theme UI**: Modern, professional interface with purple accents

## 🏗️ Architecture

### Core Components

1. **AI Orchestrator** (`lib/ai/orchestrator.ts`)
   - Coordinates multiple retrieval strategies
   - Implements Reciprocal Rank Fusion (RRF) for result merging
   - Streams responses via Server-Sent Events

2. **GraphRAG Agents** (`lib/ai/agents/`)
   - **Local Agent**: Context-specific retrieval
   - **Global Agent**: Community-based search
   - **DRIFT Agent**: Temporal relationship analysis

3. **Neo4j Integration** (`lib/graph/`)
   - Singleton driver pattern
   - Optimized Cypher queries
   - Health monitoring

4. **Azure OpenAI** (`lib/ai/llm/azure.ts`)
   - GPT-4o integration
   - Streaming completions
   - Environment-based configuration

## 📁 Project Structure

```
├── components/
│   ├── Layout.tsx          # Main layout wrapper
│   └── Navigation.tsx      # Site navigation
├── lib/
│   ├── ai/
│   │   ├── agents/         # Local, Global, DRIFT agents
│   │   ├── llm/           # Azure OpenAI client
│   │   ├── orchestrator.ts # Multi-agent coordinator
│   │   ├── merge.ts       # RRF result merging
│   │   └── types.ts       # Type definitions
│   ├── graph/
│   │   ├── neo4j.ts       # Neo4j singleton driver
│   │   └── graphRag.ts    # GraphRAG implementations
│   └── config.ts          # Environment configuration
├── pages/
│   ├── api/
│   │   ├── assistant/     # AI assistant endpoints
│   │   ├── diagnostics/   # Health & debug endpoints
│   │   ├── graph/         # Graph data endpoints
│   │   ├── graph-data.ts  # Graph visualization data
│   │   ├── health.ts      # System health check
│   │   └── stats-new.ts   # Database statistics
│   ├── assistant.tsx      # AI chat interface
│   ├── graph.tsx          # Graph visualization
│   └── index.tsx          # Dashboard
├── styles/
│   └── globals.css        # Global styles
└── types/
    └── index.ts           # Shared type definitions
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Neo4j database with legal knowledge graph
- Azure OpenAI API access

### Installation

1. **Clone and install dependencies:**
   ```bash
   git clone <repository-url>
   cd uae-legal-graphrag-neo4j-nextjs
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

3. **Set environment variables in `.env`:**
   ```env
   # Neo4j Configuration
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your_password

   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_api_key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT=gpt-4o
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Access the application:**
   - Dashboard: http://localhost:3000
   - AI Assistant: http://localhost:3000/assistant
   - Graph Visualization: http://localhost:3000/graph

## 🔧 API Endpoints

### Core Endpoints

- `POST /api/assistant` - Multi-agent AI chat with streaming
- `GET /api/graph-data` - Graph visualization data
- `GET /api/health` - System health check
- `GET /api/stats-new` - Database statistics

### Diagnostic Endpoints

- `GET /api/diagnostics/debug` - Configuration validation
- `GET /api/diagnostics/env` - Environment status
- `GET /api/diagnostics/neo4j` - Neo4j connectivity

## 🎯 Usage

### AI Assistant

The AI Assistant provides intelligent legal research through:

1. **Natural Language Queries**: Ask complex legal questions
2. **Multi-Strategy Retrieval**: Automatically selects optimal retrieval approach
3. **Structured Responses**: Markdown-formatted answers with citations
4. **Real-time Streaming**: Progressive response generation

Example queries:
- "What are the liability rules for companies in UAE?"
- "Explain contract law with examples"
- "Business establishment requirements in Dubai"

### Graph Visualization

Interactive exploration of the legal knowledge graph:

- **Node Types**: Legal instruments, provisions, courts, entities
- **Relationship Types**: APPLIES_TO, REFERENCES, GOVERNS
- **Interactive Features**: Zoom, pan, node selection
- **Real-time Data**: Live updates from Neo4j

## 🛠️ Configuration

### Environment Groups

The system uses grouped environment validation:

1. **Neo4j Group**: Database connectivity
2. **Azure OpenAI Group**: AI model access

### Health Monitoring

Built-in health checks for:
- Neo4j connectivity
- Azure OpenAI API status
- Environment configuration
- System dependencies

## 📊 Performance

- **Streaming Responses**: Real-time AI output
- **Connection Pooling**: Optimized Neo4j connections
- **Result Caching**: Efficient query processing
- **Error Handling**: Graceful failure recovery

## 🔒 Security

- Environment variable validation
- API rate limiting
- Input sanitization
- Secure Neo4j connections

## 🚧 Development

### Scripts

```bash
npm run dev          # Development server
npm run build        # Production build
npm run start        # Production server
npm run lint         # Code linting
npm run type-check   # TypeScript validation
npm run clean        # Clean build files
```

### Code Quality

- TypeScript for type safety
- ESLint for code quality
- Prettier for formatting
- Modular architecture

## 📝 License

This project is proprietary software developed for UAE legal research applications.

## 🤝 Contributing

This is an internal project. For questions or support, contact the development team.
