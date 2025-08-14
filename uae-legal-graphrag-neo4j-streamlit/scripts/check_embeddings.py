#!/usr/bin/env python3
"""Quick embedding verification."""

import os
import ssl
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def check_embeddings():
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    embedding_dim = int(os.getenv("EMBEDDING_DIM", "3072"))
    
    try:
        # Handle AuraDB SSL
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        plain_uri = uri.replace("bolt+s://", "bolt://")
        
        driver = GraphDatabase.driver(plain_uri, auth=(user, password), encrypted=True, ssl_context=ssl_context)
        
        with driver.session(database=database) as session:
            # Count provisions with embeddings
            result = session.run("MATCH (p:Provision) WHERE p.embedding IS NOT NULL RETURN count(p) AS c")
            count = result.single()["c"]
            print(f"✅ Provisions with embeddings: {count}")
            
            # Test KNN query
            if count > 0:
                qvec = [0.0] * embedding_dim
                qvec[0] = 1.0  # Simple test vector
                result = session.run(
                    "CALL db.index.vector.queryNodes('prov_embedding_index', 3, $qvec) YIELD node, score RETURN node.id AS id, score ORDER BY score DESC",
                    qvec=qvec
                )
                results = list(result)
                print(f"✅ Vector search returned {len(results)} results")
                if results:
                    print(f"   Top result: {results[0]['id']} (score: {results[0]['score']:.4f})")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    success = check_embeddings()
    sys.exit(0 if success else 1)
