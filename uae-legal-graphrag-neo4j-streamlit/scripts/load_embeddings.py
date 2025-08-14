"""Load embeddings for provisions using Azure OpenAI."""
import os
import sys
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config import settings
from src.db import db
from src.embeddings.azure_openai import embeddings_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_embeddings():
    """Load embeddings for all provisions in the database."""
    
    logger.info("🚀 Starting embedding generation process...")
    
    try:
        # Connect to database
        db.connect()
        logger.info("✅ Connected to Neo4j database")
        
        # Get all provisions without embeddings
        provisions_to_process = get_provisions_without_embeddings()
        
        if not provisions_to_process:
            logger.info("✅ All provisions already have embeddings")
            return
        
        logger.info(f"📝 Found {len(provisions_to_process)} provisions to process")
        
        # Process provisions in batches
        batch_size = 10
        total_processed = 0
        
        for i in range(0, len(provisions_to_process), batch_size):
            batch = provisions_to_process[i:i + batch_size]
            
            logger.info(f"🔄 Processing batch {i//batch_size + 1}/{(len(provisions_to_process) + batch_size - 1)//batch_size}")
            
            # Generate embeddings for batch
            batch_embeddings = generate_batch_embeddings(batch)
            
            # Update database with embeddings
            update_provision_embeddings(batch, batch_embeddings)
            
            total_processed += len(batch)
            logger.info(f"✅ Processed {total_processed}/{len(provisions_to_process)} provisions")
        
        logger.info("🎉 Embedding generation completed successfully!")
        
        # Verify embeddings
        verify_embeddings()
        
    except Exception as e:
        logger.error(f"❌ Error in embedding generation: {e}")
        raise
    
    finally:
        db.close()


def get_provisions_without_embeddings() -> List[Dict[str, Any]]:
    """Get all provisions that don't have embeddings."""
    
    query = """
    MATCH (p:Provision)
    WHERE p.embedding IS NULL AND p.text IS NOT NULL
    RETURN p.id as id, p.text as text, p.number as number
    ORDER BY p.id
    """
    
    provisions = []
    
    with db.session() as session:
        result = session.run(query)
        for record in result:
            provisions.append({
                "id": record["id"],
                "text": record["text"],
                "number": record["number"]
            })
    
    return provisions


def generate_batch_embeddings(provisions: List[Dict[str, Any]]) -> List[List[float]]:
    """Generate embeddings for a batch of provisions."""
    
    texts = [provision["text"] for provision in provisions]
    embeddings = []
    
    for i, text in enumerate(texts):
        try:
            provision_id = provisions[i]["id"]
            logger.info(f"  📝 Generating embedding for {provision_id}...")
            
            embedding = embeddings_client.get_embeddings(text)
            embeddings.append(embedding)
            
            # Validate embedding dimension
            if len(embedding) != settings.embedding_dim:
                raise ValueError(f"Expected {settings.embedding_dim} dimensions, got {len(embedding)}")
            
        except Exception as e:
            logger.error(f"  ❌ Failed to generate embedding for {provisions[i]['id']}: {e}")
            # Add zero vector as fallback
            embeddings.append([0.0] * settings.embedding_dim)
    
    return embeddings


def update_provision_embeddings(provisions: List[Dict[str, Any]], embeddings: List[List[float]]):
    """Update provisions with their embeddings."""
    
    query = """
    MATCH (p:Provision {id: $provision_id})
    SET p.embedding = $embedding
    """
    
    with db.session() as session:
        for provision, embedding in zip(provisions, embeddings):
            session.run(query, provision_id=provision["id"], embedding=embedding)
            logger.debug(f"  ✅ Updated embedding for {provision['id']}")


def verify_embeddings():
    """Verify that embeddings were loaded correctly."""
    
    logger.info("🔍 Verifying embeddings...")
    
    verification_queries = [
        ("Total provisions", "MATCH (p:Provision) RETURN count(p) as count"),
        ("Provisions with embeddings", "MATCH (p:Provision) WHERE p.embedding IS NOT NULL RETURN count(p) as count"),
        ("Embedding dimensions", "MATCH (p:Provision) WHERE p.embedding IS NOT NULL RETURN size(p.embedding) as dim LIMIT 1"),
    ]
    
    with db.session() as session:
        for description, query in verification_queries:
            result = session.run(query)
            record = result.single()
            if record:
                value = record.get("count") or record.get("dim")
                logger.info(f"  📊 {description}: {value}")
    
    # Test vector search
    logger.info("🎯 Testing vector search...")
    
    test_query = """
    MATCH (p:Provision) WHERE p.embedding IS NOT NULL
    WITH p LIMIT 1
    CALL db.index.vector.queryNodes('prov_embedding_index', 3, p.embedding)
    YIELD node, score
    RETURN count(node) as results
    """
    
    try:
        with db.session() as session:
            result = session.run(test_query)
            record = result.single()
            if record and record["results"] > 0:
                logger.info("  ✅ Vector search test passed")
            else:
                logger.warning("  ⚠️ Vector search test failed - check vector index")
    
    except Exception as e:
        logger.warning(f"  ⚠️ Vector search test failed: {e}")
        logger.info("  💡 Make sure vector index is created with: python scripts/seed_local.sh")


def check_azure_openai_config():
    """Check Azure OpenAI configuration."""
    
    logger.info("🔧 Checking Azure OpenAI configuration...")
    
    required_settings = [
        ("Azure OpenAI Endpoint", settings.azure_openai_endpoint),
        ("Deployment Name", settings.azure_openai_embedding_deployment),
        ("Embedding Dimension", settings.embedding_dim),
    ]
    
    for name, value in required_settings:
        logger.info(f"  📋 {name}: {value}")
    
    # Test API connectivity
    logger.info("🌐 Testing Azure OpenAI connectivity...")
    
    try:
        test_embedding = embeddings_client.get_embeddings("test")
        logger.info(f"  ✅ API test successful - received {len(test_embedding)} dimensions")
        
        if len(test_embedding) != settings.embedding_dim:
            logger.warning(f"  ⚠️ Dimension mismatch: expected {settings.embedding_dim}, got {len(test_embedding)}")
    
    except Exception as e:
        logger.error(f"  ❌ API test failed: {e}")
        raise


def main():
    """Main function."""
    
    # Load environment variables
    load_dotenv()
    
    logger.info("🔧 UAE Legal GraphRAG - Embedding Loader")
    logger.info("=" * 50)
    
    # Check configuration
    check_azure_openai_config()
    
    # Load embeddings
    load_embeddings()
    
    logger.info("=" * 50)
    logger.info("✨ Embedding loading process completed!")
    logger.info("🚀 You can now run the Streamlit app with vector search enabled.")


if __name__ == "__main__":
    main()
