import sys
import os

# Add the current directory to the path
sys.path.append('.')

from app.adapters.neo4j_conn import Neo4jConnection
from app.adapters.azure_openai import AzureLLM
from app.adapters.a2a import A2AAdapter
from app.adapters.vectordb_faiss import FAISSVectorDB

# Import routes module
from app.api import routes

def test_global_vars():
    print("=== Testing Global Variable Initialization ===")
    
    # Check initial state
    print(f"Initial neo4j_conn: {routes.neo4j_conn}")
    print(f"Initial azure_llm: {routes.azure_llm}")
    
    # Create instances
    neo4j_conn = Neo4jConnection()
    azure_llm = AzureLLM()
    a2a_adapter = A2AAdapter()
    faiss_db = FAISSVectorDB()
    
    print(f"Created neo4j_conn: {neo4j_conn}")
    print(f"Created azure_llm: {azure_llm}")
    
    # Set global variables
    routes.neo4j_conn = neo4j_conn
    routes.azure_llm = azure_llm
    routes.a2a_adapter = a2a_adapter
    routes.faiss_db = faiss_db
    
    print(f"After setting - neo4j_conn: {routes.neo4j_conn}")
    print(f"After setting - azure_llm: {routes.azure_llm}")
    
    # Test get_services
    services = routes.get_services()
    print(f"Services: {services}")
    
    print("=== End Test ===")

if __name__ == "__main__":
    test_global_vars()
