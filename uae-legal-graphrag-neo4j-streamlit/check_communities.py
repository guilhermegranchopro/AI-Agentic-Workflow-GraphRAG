#!/usr/bin/env python3
"""Quick script to check community detection results."""

from src.db import db

def check_communities():
    """Check what communities were created by Louvain algorithm."""
    try:
        with db.session() as session:
            # Check communities
            result = session.run("""
                MATCH (n) 
                WHERE n.communityId IS NOT NULL 
                RETURN DISTINCT n.communityId as communityId, 
                       count(n) as size,
                       collect(DISTINCT labels(n)[0]) as node_types
                ORDER BY size DESC
            """)
            
            communities = [dict(record) for record in result]
            
            print(f"🎪 Found {len(communities)} communities:")
            for i, community in enumerate(communities, 1):
                print(f"  Community {community['communityId']}: {community['size']} nodes ({', '.join(community['node_types'])})")
            
            # Check specific provisions with communities
            result2 = session.run("""
                MATCH (p:Provision) 
                WHERE p.communityId IS NOT NULL 
                RETURN p.id, p.communityId, p.number
                ORDER BY p.communityId
            """)
            
            provisions = [dict(record) for record in result2]
            print(f"\n📄 Provisions with community assignments:")
            for prov in provisions:
                print(f"  {prov['p.id']} (Art. {prov['p.number']}) → Community {prov['p.communityId']}")
                
    except Exception as e:
        print(f"Error checking communities: {e}")

if __name__ == "__main__":
    check_communities()
