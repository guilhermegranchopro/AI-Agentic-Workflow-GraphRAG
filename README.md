# UAE Legal GraphRAG Application

A comprehensive legal knowledge management system for UAE law, featuring GraphRAG (Graph Retrieval-Augmented Generation) capabilities.

## 🏗️ Architecture

- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **Backend**: Python FastAPI with GraphRAG implementation
- **Database**: Neo4j Knowledge Graph
- **AI Services**: Azure OpenAI integration
- **Vector Database**: FAISS for semantic search

## 🚀 Quick Start

1. **Setup Environment**:
   ```bash
   python setup.py
   ```

2. **Start Backend**:
   ```bash
   python start.py
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

## 📁 Project Structure

```
├── backend/                 # Python FastAPI backend
│   ├── app/                # Main application code
│   ├── data/               # Data storage
│   └── logs/               # Application logs
├── frontend/               # Next.js frontend
│   ├── pages/              # Next.js pages
│   ├── public/             # Static assets
│   └── styles/             # CSS styles
├── scripts/                # Utility scripts
├── docs/                   # Documentation
└── .env                    # Environment variables
```

## 🔧 Features

- **AI Assistant**: Interactive legal Q&A with GraphRAG
- **AI Analysis**: Legal contradiction detection and analysis
- **Knowledge Graph Visualization**: Interactive Neo4j graph display
- **Multi-Agent System**: Local, Global, and DRIFT GraphRAG strategies

## 📊 Health Status

- Backend: http://localhost:8012/health
- Frontend: http://localhost:3000

## 🤝 Contributing

1. Follow the existing code structure
2. Ensure all tests pass
3. Update documentation as needed

## 📄 License

This project is for educational and demonstration purposes.
