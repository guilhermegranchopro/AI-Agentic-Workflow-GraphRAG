# Quick Start Guide

This guide will help you get the UAE Legal GraphRAG system up and running in minutes.

## 🚀 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Neo4j Database** (optional - system works with mock data)
- **Azure OpenAI API access** (optional - system has fallbacks)

## ⚡ Quick Setup

### 1. Clone and Setup (One Command)

```bash
# Clone the repository
git clone <repository-url>
cd internship_GraphRAG

# Run the setup script (automatically handles everything)
python setup.py
```

### 2. Configure Environment

Edit the `.env` file with your configuration:

```env
# Neo4j Configuration (optional)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Azure OpenAI Configuration (optional)
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Frontend Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:8012
```

### 3. Start the Application

```bash
# Start both backend and frontend
python start.py
```

That's it! 🎉

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8012
- **API Documentation**: http://localhost:8012/docs

## 📊 What You'll See

### Overview Page (`/`)
- Database statistics
- System health status
- Quick navigation

### Graph Page (`/graph`)
- Interactive knowledge graph visualization
- Real UAE legal data (or mock data if backend unavailable)
- Node filtering and relationship exploration

### AI Analysis Page (`/ai-analysis`)
- Legal contradiction detection
- Harmonization recommendations
- Intelligent legal insights

### AI Assistant Page (`/assistant`)
- Conversational AI with legal knowledge
- Context-aware responses
- Citation support

## 🔧 Advanced Usage

### Start Only Backend
```bash
python start.py --backend-only
```

### Start Only Frontend (with mock data)
```bash
python start.py --frontend-only
```

### Load Mock Data
```bash
# Note: Mock data loading is now handled automatically by the application
```

## 🛠️ Troubleshooting

### Backend Won't Start
- Check Neo4j connection (if using real data)
- Verify Azure OpenAI credentials (if using AI features)
- Ensure virtual environment is activated

### Frontend Shows Mock Data
- Backend is not running or not accessible
- Check backend health at http://localhost:8012/health
- This is normal behavior - system gracefully falls back to mock data

### Port Already in Use
- Backend: Change port in `.env` file
- Frontend: Change port in `frontend/package.json`

## 📚 Next Steps

1. **Explore the Graph**: Navigate to the Graph page to see the knowledge visualization
2. **Try AI Analysis**: Use the AI Analysis page to detect legal contradictions
3. **Chat with AI**: Test the AI Assistant with legal questions
4. **Load Real Data**: Connect to Neo4j and load your own legal data
5. **Customize**: Modify the system for your specific legal domain

## 🆘 Need Help?

- Check the main [README.md](../README.md) for detailed documentation
- Review the [API Documentation](../docs/API.md) for technical details
- Open an issue on GitHub for support

---

**Note**: The system is designed to work with or without external dependencies. Mock data and fallback mechanisms ensure the application is always functional for demonstrations and testing.
