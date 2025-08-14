#!/usr/bin/env python3
"""Create vector index with proper dimension from environment."""

import os
import ssl
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def create_vector_index():
    """Create the vector index for provisions."""
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    embedding_dim = int(os.getenv("EMBEDDING_DIM", "3072"))
    
    print(f"Creating vector index with dimension: {embedding_dim}")
    
    try:
        # Handle AuraDB SSL issues (demo mode)
        if "bolt+s://" in uri:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            plain_uri = uri.replace("bolt+s://", "bolt://")
            driver = GraphDatabase.driver(
                plain_uri, 
                auth=(user, password),
                encrypted=True,
                ssl_context=ssl_context
            )
        else:
            driver = GraphDatabase.driver(uri, auth=(user, password))
        
        with driver.session(database=database) as session:
            # Create vector index
            vector_index_query = f"""
            CREATE VECTOR INDEX prov_embedding_index IF NOT EXISTS
            FOR (p:Provision) ON (p.embedding)
            OPTIONS {{ indexConfig: {{ `vector.dimensions`: {embedding_dim}, `vector.similarity_function`: 'cosine' }} }}
            """
            
            print("⚡ Creating vector index...")
            def create_index(tx):
                result = tx.run(vector_index_query)
                summary = result.consume()
                return summary
            
            summary = session.execute_write(create_index)
            print(f"✅ Vector index created: {summary.counters}")
            
            # Verify index exists
            result = session.run("SHOW INDEXES YIELD name, type WHERE type='VECTOR' RETURN name, type")
            indexes = list(result)
            print("✅ Vector indexes:")
            for idx in indexes:
                print(f"   {idx['name']}: {idx['type']}")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Vector index creation failed: {e}")
        return False

if __name__ == "__main__":
    success = create_vector_index()
    sys.exit(0 if success else 1)
