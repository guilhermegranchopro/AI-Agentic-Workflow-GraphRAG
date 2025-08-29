# Project Structure Documentation

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
