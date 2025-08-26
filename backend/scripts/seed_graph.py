#!/usr/bin/env python3
"""
Seed script for Neo4j database with UAE legal data.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.adapters.neo4j_conn import Neo4jConnection
from app.schemas.config import settings
from loguru import logger


async def create_constraints(neo4j_conn: Neo4jConnection):
    """Create database constraints."""
    constraints = [
        "CREATE CONSTRAINT law_id IF NOT EXISTS FOR (l:Law) REQUIRE l.id IS UNIQUE",
        "CREATE CONSTRAINT article_id IF NOT EXISTS FOR (a:Article) REQUIRE a.id IS UNIQUE",
        "CREATE CONSTRAINT case_id IF NOT EXISTS FOR (c:Case) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
    ]
    
    for constraint in constraints:
        try:
            await neo4j_conn.run_cypher(constraint)
            logger.info(f"Created constraint: {constraint}")
        except Exception as e:
            logger.warning(f"Constraint may already exist: {e}")


async def create_laws(neo4j_conn: Neo4jConnection):
    """Create sample UAE laws."""
    laws = [
        {
            "id": "law_001",
            "title": "UAE Civil Code",
            "content": "Federal Law No. 5 of 1985 on Civil Transactions",
            "type": "Federal Law",
            "year": 1985,
            "status": "active"
        },
        {
            "id": "law_002", 
            "title": "UAE Commercial Code",
            "content": "Federal Law No. 18 of 1993 on Commercial Transactions",
            "type": "Federal Law",
            "year": 1993,
            "status": "active"
        },
        {
            "id": "law_003",
            "title": "UAE Labor Law",
            "content": "Federal Law No. 8 of 1980 on Labor Relations",
            "type": "Federal Law", 
            "year": 1980,
            "status": "active"
        }
    ]
    
    for law in laws:
        query = """
        MERGE (l:Law {id: $id})
        SET l.title = $title, l.content = $content, l.type = $type, 
            l.year = $year, l.status = $status
        """
        await neo4j_conn.run_cypher(query, law)
        logger.info(f"Created law: {law['title']}")


async def create_articles(neo4j_conn: Neo4jConnection):
    """Create sample legal articles."""
    articles = [
        {
            "id": "art_001",
            "law_id": "law_001",
            "number": 1,
            "title": "Scope of Application",
            "content": "This law shall apply to all civil transactions in the UAE.",
            "type": "Article"
        },
        {
            "id": "art_002",
            "law_id": "law_001", 
            "number": 2,
            "title": "Good Faith",
            "content": "All parties must act in good faith in civil transactions.",
            "type": "Article"
        },
        {
            "id": "art_003",
            "law_id": "law_002",
            "number": 1,
            "title": "Commercial Transactions",
            "content": "Commercial transactions are those conducted by merchants.",
            "type": "Article"
        },
        {
            "id": "art_004",
            "law_id": "law_003",
            "number": 1,
            "title": "Employment Contracts",
            "content": "Employment contracts must be in writing and specify terms.",
            "type": "Article"
        }
    ]
    
    for article in articles:
        query = """
        MERGE (a:Article {id: $id})
        SET a.number = $number, a.title = $title, a.content = $content, a.type = $type
        WITH a
        MATCH (l:Law {id: $law_id})
        MERGE (a)-[:BELONGS_TO]->(l)
        """
        await neo4j_conn.run_cypher(query, article)
        logger.info(f"Created article: {article['title']}")


async def create_cases(neo4j_conn: Neo4jConnection):
    """Create sample legal cases."""
    cases = [
        {
            "id": "case_001",
            "title": "Commercial Contract Dispute",
            "content": "Case involving interpretation of commercial contract terms.",
            "year": 2020,
            "court": "Dubai Court of Cassation",
            "outcome": "Contract upheld"
        },
        {
            "id": "case_002",
            "title": "Labor Rights Case",
            "content": "Case regarding employee termination and compensation.",
            "year": 2021,
            "court": "Abu Dhabi Labor Court",
            "outcome": "Employee compensation awarded"
        }
    ]
    
    for case in cases:
        query = """
        MERGE (c:Case {id: $id})
        SET c.title = $title, c.content = $content, c.year = $year,
            c.court = $court, c.outcome = $outcome
        """
        await neo4j_conn.run_cypher(query, case)
        logger.info(f"Created case: {case['title']}")


async def create_entities(neo4j_conn: Neo4jConnection):
    """Create sample legal entities."""
    entities = [
        {
            "id": "ent_001",
            "name": "Ministry of Justice",
            "type": "Government Entity",
            "role": "Legal Authority"
        },
        {
            "id": "ent_002",
            "name": "Dubai Courts",
            "type": "Judicial Entity", 
            "role": "Court System"
        },
        {
            "id": "ent_003",
            "name": "UAE Central Bank",
            "type": "Regulatory Entity",
            "role": "Financial Regulation"
        }
    ]
    
    for entity in entities:
        query = """
        MERGE (e:Entity {id: $id})
        SET e.name = $name, e.type = $type, e.role = $role
        """
        await neo4j_conn.run_cypher(query, entity)
        logger.info(f"Created entity: {entity['name']}")


async def create_relationships(neo4j_conn: Neo4jConnection):
    """Create relationships between legal elements."""
    relationships = [
        # Article references
        {
            "from_id": "art_001",
            "to_id": "art_002", 
            "type": "REFERENCES",
            "description": "Article 1 references good faith principle"
        },
        # Case interpretations
        {
            "from_id": "case_001",
            "to_id": "art_003",
            "type": "INTERPRETS",
            "description": "Case interprets commercial transaction definition"
        },
        {
            "from_id": "case_002", 
            "to_id": "art_004",
            "type": "INTERPRETS",
            "description": "Case interprets employment contract requirements"
        },
        # Entity relationships
        {
            "from_id": "ent_001",
            "to_id": "law_001",
            "type": "ADMINISTERS",
            "description": "Ministry administers civil code"
        },
        {
            "from_id": "ent_002",
            "to_id": "case_001",
            "type": "DECIDES",
            "description": "Dubai Courts decided the case"
        },
        # Deliberate contradictions for testing
        {
            "from_id": "art_001",
            "to_id": "art_003",
            "type": "CONTRADICTS",
            "description": "Civil code scope contradicts commercial code scope"
        }
    ]
    
    for rel in relationships:
        query = """
        MATCH (from {id: $from_id}), (to {id: $to_id})
        MERGE (from)-[r:RELATES_TO {type: $type}]->(to)
        SET r.description = $description
        """
        await neo4j_conn.run_cypher(query, rel)
        logger.info(f"Created relationship: {rel['from_id']} -> {rel['to_id']}")


async def create_indexes(neo4j_conn: Neo4jConnection):
    """Create database indexes for performance."""
    indexes = [
        "CREATE INDEX law_title IF NOT EXISTS FOR (l:Law) ON (l.title)",
        "CREATE INDEX article_number IF NOT EXISTS FOR (a:Article) ON (a.number)",
        "CREATE INDEX case_year IF NOT EXISTS FOR (c:Case) ON (c.year)",
        "CREATE INDEX entity_name IF NOT EXISTS FOR (e:Entity) ON (e.name)",
    ]
    
    for index in indexes:
        try:
            await neo4j_conn.run_cypher(index)
            logger.info(f"Created index: {index}")
        except Exception as e:
            logger.warning(f"Index may already exist: {e}")


async def main():
    """Main seeding function."""
    logger.info("Starting Neo4j database seeding...")
    
    # Initialize Neo4j connection
    neo4j_conn = Neo4jConnection()
    
    try:
        # Verify connectivity
        is_connected = await neo4j_conn.verify_connectivity()
        if not is_connected:
            logger.error("Failed to connect to Neo4j")
            return
        
        logger.info("Connected to Neo4j successfully")
        
        # Create database structure
        await create_constraints(neo4j_conn)
        await create_laws(neo4j_conn)
        await create_articles(neo4j_conn)
        await create_cases(neo4j_conn)
        await create_entities(neo4j_conn)
        await create_relationships(neo4j_conn)
        await create_indexes(neo4j_conn)
        
        # Get final statistics
        stats = await neo4j_conn.get_graph_stats()
        logger.info(f"Database seeding completed. Stats: {stats}")
        
    except Exception as e:
        logger.error(f"Error during seeding: {e}")
        raise
    finally:
        await neo4j_conn.close()


if __name__ == "__main__":
    asyncio.run(main())
