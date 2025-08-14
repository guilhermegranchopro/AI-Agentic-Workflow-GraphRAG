#!/usr/bin/env python3
"""Verify database seeding and display statistics."""

import os
import ssl
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from dotenv import load_dotenv
from neo4j import GraphDatabase

def verify_seeding():
    """Verify the database seeding was successful."""
    load_dotenv()
    
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    database = os.getenv("NEO4J_DATABASE", "neo4j")
    
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
            print("=== Database Verification ===")
            
            # Check constraints
            result = session.run("SHOW CONSTRAINTS")
            constraints = list(result)
            print(f"✅ Constraints: {len(constraints)} created")
            
            # Check node counts
            result = session.run("MATCH (n) RETURN labels(n) AS lbl, count(*) AS cnt ORDER BY cnt DESC")
            node_counts = list(result)
            print("✅ Node counts:")
            for record in node_counts:
                labels = record['lbl']
                count = record['cnt']
                if labels:  # Skip empty labels
                    print(f"   {labels[0]}: {count}")
            
            # Check relationships
            result = session.run("MATCH ()-[r]->() RETURN type(r) AS rel_type, count(*) AS cnt ORDER BY cnt DESC")
            rel_counts = list(result)
            print("✅ Relationship counts:")
            for record in rel_counts:
                print(f"   {record['rel_type']}: {record['cnt']}")
                
            # Sample queries
            print("\n=== Sample Queries ===")
            result = session.run("MATCH (p:Provision) RETURN p.id AS id, p.title AS title LIMIT 3")
            provisions = list(result)
            print("✅ Sample provisions:")
            for prov in provisions:
                print(f"   {prov['id']}: {prov['title'][:50]}...")
        
        driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

if __name__ == "__main__":
    success = verify_seeding()
    sys.exit(0 if success else 1)
