#!/usr/bin/env python3
"""Debug DRIFT RAG issues."""

from datetime import date
from src.db import db
from src.graph.tools import semantic_search_provisions, drift_rag_query
from src.graph.queries import communities_top, provision_by_community

def debug_drift_rag():
    """Debug DRIFT RAG step by step."""
    
    query_text = "civil liability compensation damage"
    as_of_date = date(2024, 10, 1)
    
    print(f"🎪 Debugging DRIFT RAG for query: '{query_text}'")
    print("=" * 60)
    
    # Step 1: Test semantic search
    print("\n1️⃣ Testing semantic search...")
    try:
        semantic_results = semantic_search_provisions(query_text, 5)
        print(f"   Found {len(semantic_results)} semantic results")
        for i, result in enumerate(semantic_results[:3]):
            provision = result.get("provision", {})
            score = result.get("score", "unknown")
            print(f"   {i+1}. {provision.get('id', 'unknown')} (score: {score})")
    except Exception as e:
        print(f"   ❌ Semantic search failed: {e}")
        return
    
    # Step 2: Test communities
    print("\n2️⃣ Testing community detection...")
    try:
        communities_df = communities_top(3)
        print(f"   Found {len(communities_df)} communities")
        for _, row in communities_df.iterrows():
            print(f"   Community {row['community_id']}: {row['size']} nodes")
    except Exception as e:
        print(f"   ❌ Communities failed: {e}")
        return
    
    # Step 3: Test provision by community
    print("\n3️⃣ Testing provisions by community...")
    try:
        community_ids = communities_df['community_id'].tolist()
        community_provisions = provision_by_community(community_ids, 2)
        print(f"   Found {len(community_provisions)} community groups")
        for cp in community_provisions:
            cid = cp["community_id"]
            provisions = cp["provisions"]
            print(f"   Community {cid}: {len(provisions)} provisions")
            for prov in provisions:
                print(f"     - {prov['id']}")
    except Exception as e:
        print(f"   ❌ Provision by community failed: {e}")
        return
    
    # Step 4: Test full DRIFT
    print("\n4️⃣ Testing full DRIFT RAG...")
    try:
        drift_result = drift_rag_query(query_text, as_of_date, 2)
        if "error" in drift_result:
            print(f"   ❌ DRIFT failed: {drift_result['error']}")
        else:
            seeds = drift_result.get("semantic_seeds", [])
            communities = drift_result.get("community_results", [])
            print(f"   ✅ DRIFT succeeded:")
            print(f"     Semantic seeds: {len(seeds)}")
            print(f"     Community results: {len(communities)}")
            for cr in communities:
                cid = cr["community_id"]
                paths = cr["paths"]
                print(f"       Community {cid}: {len(paths)} paths")
    except Exception as e:
        print(f"   ❌ Full DRIFT failed: {e}")

if __name__ == "__main__":
    debug_drift_rag()
