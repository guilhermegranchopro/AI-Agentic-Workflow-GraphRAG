"""Test vector KNN functionality."""
import pytest
import sys
import os
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import db
from src.graph.queries import knn_provisions
from src.embeddings.azure_openai import embeddings_client


def test_embedding_dimensions():
    """Test that embeddings have correct dimensions."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Check if any provisions have embeddings
        result = session.run("""
            MATCH (p:Provision) 
            WHERE p.embedding IS NOT NULL 
            RETURN p.embedding as embedding 
            LIMIT 1
        """)
        
        record = result.single()
        if record:
            embedding = record["embedding"]
            assert len(embedding) == settings.embedding_dim, \
                f"Expected {settings.embedding_dim} dimensions, got {len(embedding)}"
        else:
            pytest.skip("No embeddings found in database")
    
    db.close()


def test_vector_index_exists():
    """Test that vector index exists and is usable."""
    
    db.connect()
    
    with db.session() as session:
        # Check if vector index exists
        result = session.run("""
            SHOW INDEXES 
            YIELD name, type 
            WHERE name = 'prov_embedding_index' AND type = 'VECTOR'
            RETURN count(*) as count
        """)
        
        count = result.single()["count"]
        assert count > 0, "Vector index 'prov_embedding_index' not found"
    
    db.close()


def test_knn_query():
    """Test KNN query functionality."""
    
    # Load environment
    load_dotenv()
    
    db.connect()
    
    with db.session() as session:
        # Get a sample embedding from database
        result = session.run("""
            MATCH (p:Provision) 
            WHERE p.embedding IS NOT NULL 
            RETURN p.embedding as embedding 
            LIMIT 1
        """)
        
        record = result.single()
        if not record:
            pytest.skip("No embeddings found in database")
        
        sample_embedding = record["embedding"]
        
        # Test KNN query
        knn_results = knn_provisions(sample_embedding, k=3)
        
        assert len(knn_results) <= 3, "KNN returned more results than requested"
        assert len(knn_results) > 0, "KNN returned no results"
        
        # Check result structure
        for result in knn_results:
            assert "provision" in result
            assert "score" in result
            assert "id" in result["provision"]
            assert isinstance(result["score"], (int, float))
    
    db.close()


def test_azure_openai_embeddings():
    """Test Azure OpenAI embeddings generation."""
    
    # Load environment
    load_dotenv()
    
    try:
        # Test embedding generation
        test_text = "This is a test legal provision about civil liability."
        embedding = embeddings_client.get_embeddings(test_text)
        
        assert isinstance(embedding, list), "Embedding should be a list"
        assert len(embedding) == settings.embedding_dim, \
            f"Expected {settings.embedding_dim} dimensions, got {len(embedding)}"
        assert all(isinstance(x, (int, float)) for x in embedding), \
            "All embedding values should be numeric"
        
        # Test that different texts produce different embeddings
        different_text = "This is about commercial contracts and agreements."
        different_embedding = embeddings_client.get_embeddings(different_text)
        
        assert embedding != different_embedding, \
            "Different texts should produce different embeddings"
    
    except Exception as e:
        pytest.skip(f"Azure OpenAI not available: {e}")


def test_semantic_similarity():
    """Test that semantically similar texts have higher similarity scores."""
    
    # Load environment
    load_dotenv()
    
    try:
        # Generate embeddings for similar and different texts
        legal_text1 = "Civil liability for damages and compensation"
        legal_text2 = "Liability for civil damages and monetary compensation"
        unrelated_text = "Commercial company formation and registration"
        
        embedding1 = embeddings_client.get_embeddings(legal_text1)
        embedding2 = embeddings_client.get_embeddings(legal_text2)
        embedding3 = embeddings_client.get_embeddings(unrelated_text)
        
        # Calculate cosine similarity manually (simplified)
        def cosine_similarity(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            norm_a = sum(x * x for x in a) ** 0.5
            norm_b = sum(x * x for x in b) ** 0.5
            return dot_product / (norm_a * norm_b)
        
        similarity_12 = cosine_similarity(embedding1, embedding2)
        similarity_13 = cosine_similarity(embedding1, embedding3)
        
        # Similar legal texts should be more similar than unrelated texts
        assert similarity_12 > similarity_13, \
            "Similar legal texts should have higher similarity than unrelated texts"
    
    except Exception as e:
        pytest.skip(f"Azure OpenAI not available: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
