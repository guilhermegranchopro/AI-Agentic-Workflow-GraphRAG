import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from .schemas.config import settings
from .schemas.messages import HealthResponse

# Create FastAPI app without lifespan
app = FastAPI(
    title="UAE Legal GraphRAG API",
    description="Production-ready GraphRAG API for UAE legal research",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "UAE Legal GraphRAG API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    dependencies = {
        "neo4j": "not_configured",
        "azure_openai": "not_configured", 
        "faiss": "not_configured"
    }
    
    return HealthResponse(
        status="healthy",
        dependencies=dependencies
    )

# Test endpoint
@app.get("/test")
async def test():
    """Test endpoint."""
    return {"message": "Backend is working!", "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_simple:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.app_env == "development"
    )
