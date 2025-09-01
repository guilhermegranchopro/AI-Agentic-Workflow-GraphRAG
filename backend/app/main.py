import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
import time

from .schemas.config import settings
from .schemas.messages import HealthResponse
from .api.routes import api_router
from .utils.telemetry import log_request_start, log_request_end, cleanup_telemetry_context
from .utils.rate_limit import rate_limiter, check_rate_limit
from .utils.errors import handle_exception
from .adapters.azure_openai import AzureLLM
from .adapters.neo4j_conn import Neo4jConnection
from .adapters.a2a import A2AAdapter
from .adapters.vectordb_faiss import FAISSVectorDB
from .agents.orchestrator_agent import OrchestratorAgent
from .agents.local_graphrag_agent import LocalGraphRAGAgent
from .agents.global_graphrag_agent import GlobalGraphRAGAgent
from .agents.drift_graphrag_agent import DRIFTGraphRAGAgent


# Global service instances
azure_llm = None
neo4j_conn = None
a2a_adapter = None
faiss_db = None

# Agent instances
orchestrator_agent = None
local_graphrag_agent = None
global_graphrag_agent = None
drift_graphrag_agent = None

# Import routes module to update its global variables
from .api import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global azure_llm, neo4j_conn, a2a_adapter, faiss_db
    
    # Startup
    logger.info("Starting GraphRAG API server...")
    
    # Initialize services
    try:
        azure_llm = AzureLLM()
        neo4j_conn = Neo4jConnection()
        a2a_adapter = A2AAdapter()
        faiss_db = FAISSVectorDB()
        
        # Set global variables in routes module
        routes.azure_llm = azure_llm
        routes.neo4j_conn = neo4j_conn
        routes.a2a_adapter = a2a_adapter
        routes.faiss_db = faiss_db
        
        # Initialize AI Agents
        logger.info("Initializing AI Agents...")
        
        # Initialize GraphRAG agents
        local_graphrag_agent = LocalGraphRAGAgent(neo4j_conn, azure_llm)
        global_graphrag_agent = GlobalGraphRAGAgent(neo4j_conn, azure_llm)
        drift_graphrag_agent = DRIFTGraphRAGAgent(neo4j_conn, azure_llm)
        
        # Initialize orchestrator agent
        orchestrator_agent = OrchestratorAgent(neo4j_conn, azure_llm, a2a_adapter)
        
        # Register agents with A2A adapter
        a2a_adapter.register_router("local_graphrag_agent", local_graphrag_agent.handle_message)
        a2a_adapter.register_router("global_graphrag_agent", global_graphrag_agent.handle_message)
        a2a_adapter.register_router("drift_graphrag_agent", drift_graphrag_agent.handle_message)
        a2a_adapter.register_router("orchestrator_agent", orchestrator_agent.handle_message)
        
        # Set agent instances in routes
        routes.local_graphrag_agent = local_graphrag_agent
        routes.global_graphrag_agent = global_graphrag_agent
        routes.drift_graphrag_agent = drift_graphrag_agent
        routes.orchestrator_agent = orchestrator_agent
        
        logger.info("AI Agents initialized successfully")
        
        # Load FAISS index if exists
        if faiss_db.load():
            logger.info("FAISS index loaded successfully")
        else:
            logger.info("No existing FAISS index found")
            
        # Start rate limiter cleanup
        rate_limiter.start_cleanup()
        
        # Health checks
        await perform_health_checks()
        
        logger.info("GraphRAG API server started successfully")
        
    except Exception as e:
        logger.error(f"Failed to start GraphRAG API server: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down GraphRAG API server...")
    
    try:
        # Stop rate limiter cleanup
        rate_limiter.stop_cleanup()
        
        # Close connections
        if neo4j_conn:
            await neo4j_conn.close()
        if a2a_adapter:
            await a2a_adapter.close()
            
        logger.info("GraphRAG API server shutdown complete")
        
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


async def perform_health_checks():
    """Perform initial health checks."""
    logger.info("Performing health checks...")
    
    # Check Neo4j
    if neo4j_conn:
        health = await neo4j_conn.health_check()
        if health.get("status") == "healthy":
            logger.info("Neo4j connection: OK")
        else:
            logger.warning(f"Neo4j connection: {health.get('status', 'unknown')}")
    
    # Check Azure OpenAI
    if azure_llm:
        health = await azure_llm.health_check()
        if health.get("status") == "healthy":
            logger.info("Azure OpenAI connection: OK")
        else:
            logger.warning(f"Azure OpenAI connection: {health.get('status', 'unknown')}")


# Create FastAPI app
app = FastAPI(
    title="UAE Legal GraphRAG API",
    description="Production-ready GraphRAG API for UAE legal research",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def telemetry_middleware(request: Request, call_next):
    """Telemetry middleware for request tracing."""
    request_id = str(time.time())
    start_time = time.time()
    
    # Log request start
    log_request_start(request_id, request.method, str(request.url.path))
    
    try:
        response = await call_next(request)
        
        # Log request end
        log_request_end(request_id, response.status_code)
        
        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        
        return response
        
    except Exception as e:
        # Log error
        log_request_end(request_id, 500, {"error": str(e)})
        raise
    finally:
        # Cleanup telemetry context
        cleanup_telemetry_context(request_id)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    # Skip rate limiting for health checks
    if request.url.path in ["/", "/health", "/docs", "/openapi.json"]:
        return await call_next(request)
    
    # Check rate limit
    if not await check_rate_limit(request):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": "Too many requests. Please try again later."
            }
        )
    
    return await call_next(request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.exception(f"Unhandled exception: {exc}")
    
    # Handle GraphRAG exceptions
    http_exception = await handle_exception(exc)
    
    return JSONResponse(
        status_code=http_exception.status_code,
        content=http_exception.detail
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
    dependencies = {}
    
    # Check Neo4j using global variable from routes
    if routes.neo4j_conn:
        neo4j_health = await routes.neo4j_conn.health_check()
        dependencies["neo4j"] = neo4j_health.get("status", "unknown")
    else:
        dependencies["neo4j"] = "not_configured"
    
    # Check Azure OpenAI using global variable from routes
    if routes.azure_llm:
        azure_health = await routes.azure_llm.health_check()
        dependencies["azure_openai"] = azure_health.get("status", "unknown")
    else:
        dependencies["azure_openai"] = "not_configured"
    
    # Check FAISS using global variable from routes
    if routes.faiss_db:
        faiss_stats = routes.faiss_db.get_stats()
        dependencies["faiss"] = "healthy" if "error" not in faiss_stats else "unhealthy"
    else:
        dependencies["faiss"] = "not_configured"
    
    return HealthResponse(
        status="healthy" if all(v in ["healthy", "not_configured"] for v in dependencies.values()) else "degraded",
        dependencies=dependencies
    )


# Include API routes
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.app_env == "development"
    )
