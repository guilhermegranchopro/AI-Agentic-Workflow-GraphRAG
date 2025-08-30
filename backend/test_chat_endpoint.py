import asyncio
import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.api.routes import chat_endpoint
from app.schemas.messages import ChatRequest
from app.adapters.neo4j_conn import Neo4jConnection
from app.adapters.azure_openai import AzureLLM
from app.adapters.a2a import A2AAdapter
from app.adapters.vectordb_faiss import FAISSVectorDB
from fastapi import Request
from unittest.mock import Mock

async def test_chat_endpoint():
    print("=== Testing Chat Endpoint ===")
    
    # Initialize services
    neo4j_conn = Neo4jConnection()
    azure_llm = AzureLLM()
    a2a_adapter = A2AAdapter()
    faiss_db = FAISSVectorDB()
    
    # Create services dict
    services = {
        "azure_llm": azure_llm,
        "neo4j_conn": neo4j_conn,
        "a2a_adapter": a2a_adapter,
        "faiss_db": faiss_db
    }
    
    # Create mock request
    mock_request = Mock()
    mock_request.headers = {"X-Request-ID": "test_123"}
    
    # Create chat request
    chat_request = ChatRequest(
        message="Corporate Tax",
        conversation_id="test_conv",
        strategy="auto",
        max_results=10
    )
    
    try:
        # Call the chat endpoint
        response = await chat_endpoint(
            request=chat_request,
            req=mock_request,
            services=services
        )
        
        print(f"Response:")
        print(f"  Response text: {response.response[:200]}...")
        print(f"  Citations: {len(response.citations)}")
        print(f"  Nodes: {len(response.nodes)}")
        print(f"  Edges: {len(response.edges)}")
        print(f"  Metadata: {response.metadata}")
        
        if response.citations:
            print(f"\nFirst citation:")
            citation = response.citations[0]
            print(f"  Node ID: {citation.node_id}")
            print(f"  Content: {citation.content[:100]}...")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    print("=== End Test ===")

if __name__ == "__main__":
    asyncio.run(test_chat_endpoint())
