import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk3_data():
    """Add third chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "telecom_law_2003",
            "title": "Telecommunications Law 2003",
            "content": "Regulates telecommunications sector and services. Establishes TRA as regulatory authority. Defines licensing requirements and consumer protection.",
            "type": "Law",
            "metadata": {"law_number": "2003/3", "effective_date": "2003-01-01", "jurisdiction": "Federal", "category": "Telecommunications Law", "importance": "High"}
        },
        {
            "id": "energy_law_1998",
            "title": "Energy Law 1998",
            "content": "Regulates energy sector including oil, gas, and electricity. Establishes energy authority and licensing framework. Implements energy efficiency standards.",
            "type": "Law",
            "metadata": {"law_number": "1998/15", "effective_date": "1998-01-01", "jurisdiction": "Federal", "category": "Energy Law", "importance": "High"}
        },
        {
            "id": "aviation_law_1991",
            "title": "Aviation Law 1991",
            "content": "Regulates civil aviation and air transport. Establishes GCAA as aviation authority. Defines safety standards and licensing requirements.",
            "type": "Law",
            "metadata": {"law_number": "1991/20", "effective_date": "1991-01-01", "jurisdiction": "Federal", "category": "Aviation Law", "importance": "Medium"}
        },
        {
            "id": "maritime_law_1981",
            "title": "Maritime Law 1981",
            "content": "Regulates maritime transport and shipping. Establishes port authorities and vessel registration. Defines maritime safety and environmental standards.",
            "type": "Law",
            "metadata": {"law_number": "1981/11", "effective_date": "1981-01-01", "jurisdiction": "Federal", "category": "Maritime Law", "importance": "Medium"}
        },
        {
            "id": "media_law_1980",
            "title": "Media Law 1980",
            "content": "Regulates media and broadcasting sector. Establishes media authority and content standards. Defines licensing requirements and censorship rules.",
            "type": "Law",
            "metadata": {"law_number": "1980/15", "effective_date": "1980-01-01", "jurisdiction": "Federal", "category": "Media Law", "importance": "Medium"}
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
        ("telecom_law_2003", "cybersecurity_law_2022", "supports", {"type": "digital_infrastructure", "weight": 1}),
        ("energy_law_1998", "environmental_law_1999", "complements", {"type": "sustainability", "weight": 1}),
        ("aviation_law_1991", "commercial_code_1993", "regulates", {"type": "transport_regulation", "weight": 1}),
        ("maritime_law_1981", "commercial_code_1993", "governs", {"type": "trade_regulation", "weight": 1}),
        ("media_law_1980", "data_protection_law_2021", "influences", {"type": "content_regulation", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 3)")

if __name__ == "__main__":
    asyncio.run(add_chunk3_data())
