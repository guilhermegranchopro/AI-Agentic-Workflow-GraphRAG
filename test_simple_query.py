#!/usr/bin/env python3
"""
Simple test to see Neo4j query results structure
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def test_simple_query():
    """Test a simple Neo4j query to see the result structure."""
    print("🔍 Testing Simple Neo4j Query")
    print("=" * 40)
    
    try:
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        neo4j_conn = Neo4jConnection()
        
        # Test the exact query that GraphRAG uses
        query = """
        MATCH (n:LegalNode)
        WHERE n.content CONTAINS $query OR n.title CONTAINS $query
        WITH n, size([(n)-[]-() | 1]) as degree
        ORDER BY degree DESC, n.score DESC
        LIMIT $max_results
        OPTIONAL MATCH (n)-[r]-(related)
        RETURN DISTINCT n, r, related
        """
        
        params = {"query": "business", "max_results": 5}
        
        print("🔍 Running GraphRAG-style query...")
        results = await neo4j_conn.run_cypher(query, params)
        
        print(f"📊 Found {len(results)} results")
        
        for i, record in enumerate(results):
            print(f"\n📋 Record {i+1}:")
            print(f"   Keys: {list(record.keys())}")
            
            if 'n' in record:
                node = record['n']
                print(f"   Node type: {type(node)}")
                if hasattr(node, 'keys'):
                    print(f"   Node keys: {list(node.keys())}")
                    print(f"   Node title: {node.get('title', 'N/A')}")
                    print(f"   Node content: {node.get('content', 'N/A')[:50]}...")
                else:
                    print(f"   Node: {node}")
            
            if 'r' in record:
                rel = record['r']
                print(f"   Relationship type: {type(rel)}")
                if hasattr(rel, 'keys'):
                    print(f"   Relationship keys: {list(rel.keys())}")
                else:
                    print(f"   Relationship: {rel}")
            
            if 'related' in record:
                related = record['related']
                print(f"   Related type: {type(related)}")
                if hasattr(related, 'keys'):
                    print(f"   Related keys: {list(related.keys())}")
                else:
                    print(f"   Related: {related}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simple_query())
    sys.exit(0 if success else 1)
