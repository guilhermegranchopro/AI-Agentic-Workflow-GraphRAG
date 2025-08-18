# UAE Legal GraphRAG - Next.js Frontend

A modern React/Next.js frontend for the UAE Legal GraphRAG system, providing an intuitive interface for legal research using GraphRAG retrieval methods.

## 🚀 Features

- **🎯 Local RAG**: Entity-centric search with temporal filtering
- **🌐 Global RAG**: Community-based analysis using Graph Data Science
- **🎪 DRIFT RAG**: Community-guided local search for comprehensive coverage
- **📊 Graph Visualization**: Interactive exploration of legal knowledge graphs
- **🤖 Legal Assistant AI**: Multi-agent system for complex legal queries
- **📈 Analytics Dashboard**: System health monitoring and database statistics

## 🛠️ Technology Stack

- **Frontend**: Next.js 14, React 18, TypeScript
- **Styling**: Tailwind CSS with custom component library
- **Icons**: Lucide React
- **Charts**: Recharts
- **Backend Integration**: Python backend via API routes
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
