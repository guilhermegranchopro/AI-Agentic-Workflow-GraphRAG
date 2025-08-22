"""
Simple test version of the Python backend to verify setup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="UAE Legal GraphRAG Backend",
    description="Advanced legal research backend",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    mode: Optional[str] = "basic"

@app.get("/health")
async def health_check():
    return {"status": "healthy", "backend": "python_fastapi"}

@app.post("/api/test")
async def test_endpoint(request: QueryRequest):
    return {
        "success": True,
        "message": f"Python backend received query: {request.query}",
        "mode": request.mode
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("test_main:app", host="127.0.0.1", port=8000, reload=True)
