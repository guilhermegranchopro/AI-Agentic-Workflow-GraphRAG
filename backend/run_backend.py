#!/usr/bin/env python3
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting UAE Legal GraphRAG Backend...")
    print("Backend will be available at: http://127.0.0.1:8012")
    print("Health check: http://127.0.0.1:8012/health")
    print("API docs: http://127.0.0.1:8012/docs")
    print("Press Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=8012, 
        log_level="info",
        reload=False
    )
