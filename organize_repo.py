#!/usr/bin/env python3
"""
Repository Organization and Cleanup Script
Organizes the UAE Legal GraphRAG repository structure and removes unnecessary files.
"""

import os
import shutil
import sys
from pathlib import Path

def organize_repository():
    """Organize the repository structure and clean up unnecessary files."""
    
    # Get the project root directory
    project_root = Path(__file__).parent
    
    print("🏗️  Starting repository organization...")
    
    # 1. Remove unnecessary files and directories
    cleanup_items = [
        # Python cache files
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        
        # Log files
        "**/*.log",
        "logs",
        
        # Temporary files
        "**/*.tmp",
        "**/*.temp",
        "**/.DS_Store",
        "**/Thumbs.db",
        
        # Build artifacts
        "**/dist",
        "**/build",
        "**/.pytest_cache",
        "**/.coverage",
        "**/.mypy_cache",
        "**/.ruff_cache",
        
        # Node.js artifacts (will be reinstalled)
        "frontend/node_modules",
        "frontend/.next",
        "frontend/.nuxt",
        "frontend/dist",
        
        # IDE files
        "**/.vscode",
        "**/.idea",
        "**/*.swp",
        "**/*.swo",
        
        # OS files
        "**/.DS_Store",
        "**/Thumbs.db",
        "**/desktop.ini",
    ]
    
    print("🧹 Cleaning up unnecessary files...")
    for pattern in cleanup_items:
        for item in project_root.glob(pattern):
            if item.is_file():
                try:
                    item.unlink()
                    print(f"  ✅ Removed file: {item}")
                except Exception as e:
                    print(f"  ⚠️  Could not remove file {item}: {e}")
            elif item.is_dir():
                try:
                    shutil.rmtree(item)
                    print(f"  ✅ Removed directory: {item}")
                except Exception as e:
                    print(f"  ⚠️  Could not remove directory {item}: {e}")
    
    # 2. Create proper directory structure
    directories = [
        "docs",
        "scripts",
        "backend/data",
        "backend/logs",
        "frontend/public",
        "frontend/styles",
    ]
    
    print("📁 Creating directory structure...")
    for dir_path in directories:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created directory: {dir_path}")
    
    # 3. Create/update important files
    print("📝 Creating/updating important files...")
    
    # Create a comprehensive README
    readme_content = """# UAE Legal GraphRAG Application

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
"""
    
    with open(project_root / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  ✅ Updated README.md")
    
    # Create .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
*.log
logs/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
.next/
out/
.nuxt/
dist/

# Build
build/
dist/

# Environment
.env.local
.env.development.local
.env.test.local
.env.production.local

# Database
*.db
*.sqlite
*.sqlite3

# Cache
.cache/
.parcel-cache/
"""
    
    with open(project_root / ".gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    print("  ✅ Updated .gitignore")
    
    # Create project structure documentation
    structure_content = """# Project Structure Documentation

## Overview
This document describes the organization and purpose of each directory and file in the UAE Legal GraphRAG application.

## Root Directory

### Core Files
- `setup.py` - Initial project setup and dependency installation
- `start.py` - Application startup script
- `organize_repo.py` - Repository organization script
- `cleanup_repo.py` - Repository cleanup script
- `requirements.txt` - Python dependencies
- `docker-compose.yml` - Docker configuration for services
- `.env` - Environment variables (not in git)

### Directories
- `backend/` - Python FastAPI backend application
- `frontend/` - Next.js frontend application
- `scripts/` - Utility and maintenance scripts
- `docs/` - Project documentation
- `logs/` - Application logs (not in git)

## Backend Structure (`backend/`)

### Core Application (`backend/app/`)
- `main.py` - FastAPI application entry point
- `config.py` - Configuration management
- `api/` - API routes and endpoints
- `rag/` - GraphRAG implementation
- `adapters/` - External service adapters
- `store/` - Data storage layer
- `schemas/` - Pydantic models
- `utils/` - Utility functions

### Data (`backend/data/`)
- Database files and indexes
- FAISS vector database files
- SQLite event store

### Logs (`backend/logs/`)
- Application logs (not in git)

## Frontend Structure (`frontend/`)

### Pages (`frontend/pages/`)
- `index.tsx` - Home page
- `assistant.tsx` - AI Assistant page
- `ai-analysis.tsx` - AI Analysis page
- `graph.tsx` - Knowledge Graph visualization
- `api/` - Next.js API routes

### Components (`frontend/components/`)
- Reusable React components
- UI components
- Graph visualization components

### Styles (`frontend/styles/`)
- CSS and styling files
- Tailwind CSS configuration

### Public (`frontend/public/`)
- Static assets
- Images and icons

## Scripts (`scripts/`)

### Data Management
- `load_mock_data.py` - Load mock data into Neo4j
- `enhanced_mock_data.py` - Enhanced data loading with contradictions
- `test_graphrag_with_data.py` - Test GraphRAG functionality

### Testing
- `test_ai_assistant.py` - Test AI Assistant functionality
- `test_backend_endpoints.py` - Test backend API endpoints

### Maintenance
- `check_contradictions.py` - Check for contradictions in Neo4j
- `cleanup_repo.py` - Repository cleanup
- `organize_repo.py` - Repository organization

## Documentation (`docs/`)

- API documentation
- User guides
- Technical specifications
- Deployment guides

## Environment Configuration

### Required Environment Variables
- `NEO4J_URI` - Neo4j database connection string
- `NEO4J_USER` - Neo4j username
- `NEO4J_PASSWORD` - Neo4j password
- `AZURE_OPENAI_ENDPOINT` - Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY` - Azure OpenAI API key
- `AZURE_OPENAI_DEPLOYMENT_NAME` - Azure OpenAI deployment name

### Development Environment
- `BACKEND_URL` - Backend API URL (default: http://localhost:8012)
- `FRONTEND_URL` - Frontend URL (default: http://localhost:3000)

## Deployment

### Local Development
1. Run `python setup.py` to set up the environment
2. Run `python start.py` to start the backend
3. Run `cd frontend && npm run dev` to start the frontend

### Production
1. Use Docker Compose: `docker-compose up -d`
2. Or deploy backend and frontend separately

## Health Checks

- Backend Health: `GET /health`
- Frontend Health: Check if Next.js is running
- Neo4j Connection: Verified through backend health check
- Azure OpenAI: Verified through backend health check
- FAISS: Vector database status (optional)

## Monitoring

- Application logs in `backend/logs/`
- Health check endpoints
- Telemetry and request tracking
- Error monitoring and reporting
"""
    
    with open(project_root / "docs" / "PROJECT_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write(structure_content)
    print("  ✅ Created PROJECT_STRUCTURE.md")
    
    print("\n🎉 Repository organization completed successfully!")
    print("\n📋 Summary of changes:")
    print("  ✅ Removed unnecessary cache and build files")
    print("  ✅ Created proper directory structure")
    print("  ✅ Updated README.md with comprehensive documentation")
    print("  ✅ Updated .gitignore with proper exclusions")
    print("  ✅ Created project structure documentation")
    print("\n🚀 Next steps:")
    print("  1. Run 'python setup.py' to ensure all dependencies are installed")
    print("  2. Run 'python start.py' to start the backend")
    print("  3. Run 'cd frontend && npm run dev' to start the frontend")
    print("  4. Test the application at http://localhost:3000")

if __name__ == "__main__":
    organize_repository()
