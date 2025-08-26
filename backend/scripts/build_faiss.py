#!/usr/bin/env python3
"""
Build FAISS index from Neo4j data for vector similarity search.
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.neo4j_conn import Neo4jConnection
from app.adapters.vectordb_faiss import FAISSVectorDB
from app.adapters.azure_openai import AzureLLM
from app.schemas.config import settings
from loguru import logger


async def extract_text_content(neo4j_conn: Neo4jConnection) -> list[dict]:
    """Extract text content from Neo4j for embedding."""
    query = """
    MATCH (n)
    WHERE n.content IS NOT NULL OR n.title IS NOT NULL
    RETURN 
        id(n) as node_id,
        labels(n)[0] as node_type,
        COALESCE(n.title, '') + ' ' + COALESCE(n.content, '') as text,
        n.id as original_id,
        n.title as title
    """
    
    results = await neo4j_conn.run_cypher(query)
    
    # Filter out empty or very short texts
    filtered_results = []
    for record in results:
        text = record.get("text", "").strip()
        if len(text) > 10:  # Minimum text length
            filtered_results.append({
                "node_id": record["node_id"],
                "node_type": record["node_type"],
                "text": text,
                "original_id": record["original_id"],
                "title": record["title"]
            })
    
    logger.info(f"Extracted {len(filtered_results)} text entries from Neo4j")
    return filtered_results


async def build_faiss_index():
    """Build FAISS index from Neo4j data."""
    logger.info("Starting FAISS index build...")
    
    # Initialize connections
    neo4j_conn = Neo4jConnection()
    azure_llm = AzureLLM()
    faiss_db = FAISSVectorDB()
    
    try:
        # Verify Neo4j connectivity
        is_connected = await neo4j_conn.verify_connectivity()
        if not is_connected:
            logger.error("Failed to connect to Neo4j")
            return
        
        # Check Azure OpenAI availability
        azure_health = await azure_llm.health_check()
        if azure_health.get("status") != "healthy":
            logger.warning("Azure OpenAI not available, using mock embeddings")
            azure_llm = None
        
        # Extract text content from Neo4j
        text_data = await extract_text_content(neo4j_conn)
        
        if not text_data:
            logger.warning("No text content found in Neo4j")
            return
        
        # Create FAISS index
        if not faiss_db.create_index():
            logger.error("Failed to create FAISS index")
            return
        
        # Generate embeddings and add to index
        texts = [item["text"] for item in text_data]
        metadata = [
            {
                "node_id": item["node_id"],
                "node_type": item["node_type"],
                "original_id": item["original_id"],
                "title": item["title"]
            }
            for item in text_data
        ]
        
        if azure_llm:
            # Use Azure OpenAI for embeddings
            logger.info("Generating embeddings with Azure OpenAI...")
            embeddings = await azure_llm.embed(texts)
            
            if embeddings:
                success = faiss_db.add_vectors(embeddings, texts, metadata)
                if success:
                    logger.info(f"Added {len(embeddings)} vectors to FAISS index")
                else:
                    logger.error("Failed to add vectors to FAISS index")
                    return
            else:
                logger.error("Failed to generate embeddings")
                return
        else:
            # Use mock embeddings for testing
            logger.info("Using mock embeddings for testing...")
            import numpy as np
            
            # Generate random embeddings (for testing only)
            dimension = 1536  # OpenAI embedding dimension
            mock_embeddings = [np.random.rand(dimension).tolist() for _ in texts]
            
            success = faiss_db.add_vectors(mock_embeddings, texts, metadata)
            if success:
                logger.info(f"Added {len(mock_embeddings)} mock vectors to FAISS index")
            else:
                logger.error("Failed to add mock vectors to FAISS index")
                return
        
        # Save the index
        if faiss_db.save():
            logger.info("FAISS index saved successfully")
            
            # Get index statistics
            stats = faiss_db.get_stats()
            logger.info(f"FAISS index statistics: {stats}")
        else:
            logger.error("Failed to save FAISS index")
        
    except Exception as e:
        logger.error(f"Error during FAISS index build: {e}")
        raise
    finally:
        await neo4j_conn.close()


async def main():
    """Main function."""
    await build_faiss_index()


if __name__ == "__main__":
    asyncio.run(main())
