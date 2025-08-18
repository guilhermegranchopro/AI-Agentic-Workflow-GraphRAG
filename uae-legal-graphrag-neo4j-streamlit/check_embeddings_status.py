#!/usr/bin/env python3
"""Check embeddings status in the database."""

from src.db import db

def check_embeddings():
    """Check if provisions have embeddings."""
    try:
        with db.session() as session:
            # Check embedding status
            result = session.run("""
                MATCH (p:Provision) 
                RETURN count(p) as total, 
                       sum(CASE WHEN p.embedding IS NOT NULL THEN 1 ELSE 0 END) as with_embeddings
            """)
            
            data = result.single()
            total = data["total"]
            with_embeddings = data["with_embeddings"]
            
            print(f"📊 Embeddings Status:")
            print(f"  Total provisions: {total}")
            print(f"  With embeddings: {with_embeddings}")
            print(f"  Missing embeddings: {total - with_embeddings}")
            
            if with_embeddings == 0:
                print("\n❌ No embeddings found! DRIFT RAG requires embeddings.")
                print("   Run: python scripts/load_embeddings.py")
            elif with_embeddings < total:
                print(f"\n⚠️  Only {with_embeddings}/{total} provisions have embeddings.")
            else:
                print("\n✅ All provisions have embeddings!")
                
    except Exception as e:
        print(f"Error checking embeddings: {e}")

if __name__ == "__main__":
    check_embeddings()
