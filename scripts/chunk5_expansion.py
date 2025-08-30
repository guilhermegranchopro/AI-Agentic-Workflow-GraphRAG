import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk5_data():
    """Add fifth chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "construction_law_2008",
            "title": "Construction Law 2008",
            "content": "Regulates construction industry and building standards. Establishes construction authority and licensing requirements. Defines safety standards and quality control.",
            "type": "Law",
            "metadata": {"law_number": "2008/13", "effective_date": "2008-01-01", "jurisdiction": "Federal", "category": "Construction Law", "importance": "Medium"}
        },
        {
            "id": "agriculture_law_1993",
            "title": "Agriculture Law 1993",
            "content": "Regulates agricultural sector and food production. Establishes agricultural authority and farming standards. Defines food safety and quality requirements.",
            "type": "Law",
            "metadata": {"law_number": "1993/5", "effective_date": "1993-01-01", "jurisdiction": "Federal", "category": "Agriculture Law", "importance": "Medium"}
        },
        {
            "id": "fisheries_law_1999",
            "title": "Fisheries Law 1999",
            "content": "Regulates fishing industry and marine resources. Establishes fisheries authority and licensing framework. Defines sustainable fishing practices.",
            "type": "Law",
            "metadata": {"law_number": "1999/23", "effective_date": "1999-01-01", "jurisdiction": "Federal", "category": "Fisheries Law", "importance": "Medium"}
        },
        {
            "id": "mining_law_2009",
            "title": "Mining Law 2009",
            "content": "Regulates mining sector and mineral resources. Establishes mining authority and licensing requirements. Defines environmental protection standards.",
            "type": "Law",
            "metadata": {"law_number": "2009/8", "effective_date": "2009-01-01", "jurisdiction": "Federal", "category": "Mining Law", "importance": "Medium"}
        },
        {
            "id": "water_law_1999",
            "title": "Water Law 1999",
            "content": "Regulates water resources and distribution. Establishes water authority and conservation framework. Defines water quality and usage standards.",
            "type": "Law",
            "metadata": {"law_number": "1999/22", "effective_date": "1999-01-01", "jurisdiction": "Federal", "category": "Water Law", "importance": "Medium"}
        }
    ]
    
    # Create nodes
    for node in new_nodes:
        await neo4j_conn.run_cypher("""
            MERGE (n:LegalNode {id: $id})
            SET n.title = $title,
                n.content = $content,
                n.type = $type,
                n.metadata = $metadata,
                n.score = 1
        """, {
            "id": node["id"],
            "title": node["title"],
            "content": node["content"],
            "type": node["type"],
            "metadata": json.dumps(node["metadata"])
        })
    
    # Create relationships
    relationships = [
        ("construction_law_2008", "real_estate_law_2006", "supports", {"type": "development_regulation", "weight": 1}),
        ("agriculture_law_1993", "environmental_law_1999", "complements", {"type": "sustainable_development", "weight": 1}),
        ("fisheries_law_1999", "maritime_law_1981", "regulates", {"type": "marine_resources", "weight": 1}),
        ("mining_law_2009", "environmental_law_1999", "requires", {"type": "environmental_compliance", "weight": 1}),
        ("water_law_1999", "environmental_law_1999", "protects", {"type": "resource_management", "weight": 1})
    ]
    
    # Create relationships
    for source, target, rel_type, props in relationships:
        await neo4j_conn.run_cypher("""
            MATCH (a:LegalNode {id: $source})
            MATCH (b:LegalNode {id: $target})
            MERGE (a)-[r:RELATES_TO]->(b)
            SET r.type = $rel_type,
                r.priority = $priority,
                r.severity = $severity,
                r.category = $category,
                r.description = $description,
                r.weight = $weight
        """, {
            "source": source,
            "target": target,
            "rel_type": props.get("type", rel_type),
            "priority": props.get("priority", "low"),
            "severity": props.get("severity", "minor"),
            "category": props.get("category", "general"),
            "description": props.get("description", f"Relationship between {source} and {target}"),
            "weight": props.get("weight", 1)
        })
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 5)")

if __name__ == "__main__":
    asyncio.run(add_chunk5_data())
