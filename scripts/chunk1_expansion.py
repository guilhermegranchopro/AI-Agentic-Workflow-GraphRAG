import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk1_data():
    """Add first chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "criminal_law_1987",
            "title": "Criminal Law 1987",
            "content": "Establishes criminal offenses and penalties in UAE. Defines crimes against persons, property, and state security. Implements criminal procedure and evidence rules.",
            "type": "Law",
            "metadata": {"law_number": "1987/3", "effective_date": "1987-01-01", "jurisdiction": "Federal", "category": "Criminal Law", "importance": "High"}
        },
        {
            "id": "family_law_2005",
            "title": "Family Law 2005",
            "content": "Regulates family matters including marriage, divorce, custody, and inheritance. Implements Islamic law principles for family relationships.",
            "type": "Law",
            "metadata": {"law_number": "2005/28", "effective_date": "2005-01-01", "jurisdiction": "Federal", "category": "Family Law", "importance": "High"}
        },
        {
            "id": "commercial_agency_law_1981",
            "title": "Commercial Agency Law 1981",
            "content": "Regulates commercial agency relationships and distribution agreements. Establishes rights and obligations of agents and principals.",
            "type": "Law",
            "metadata": {"law_number": "1981/18", "effective_date": "1981-01-01", "jurisdiction": "Federal", "category": "Commercial Law", "importance": "Medium"}
        },
        {
            "id": "consumer_protection_law_2006",
            "title": "Consumer Protection Law 2006",
            "content": "Protects consumer rights and regulates commercial transactions. Establishes standards for goods and services quality.",
            "type": "Law",
            "metadata": {"law_number": "2006/24", "effective_date": "2006-01-01", "jurisdiction": "Federal", "category": "Consumer Law", "importance": "Medium"}
        },
        {
            "id": "antitrust_law_2012",
            "title": "Antitrust Law 2012",
            "content": "Prevents anti-competitive practices and monopolies. Regulates mergers and acquisitions. Establishes competition authority.",
            "type": "Law",
            "metadata": {"law_number": "2012/4", "effective_date": "2012-01-01", "jurisdiction": "Federal", "category": "Competition Law", "importance": "Medium"}
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
        ("criminal_law_1987", "court_system_2020", "enforced_by", {"type": "enforcement", "weight": 1}),
        ("family_law_2005", "civil_code_1985", "supplements", {"type": "legal_system", "weight": 1}),
        ("commercial_agency_law_1981", "commercial_code_1993", "implements", {"type": "commercial_regulation", "weight": 1}),
        ("consumer_protection_law_2006", "commercial_code_1993", "protects", {"type": "consumer_rights", "weight": 1}),
        ("antitrust_law_2012", "commercial_companies_law_2015", "regulates", {"type": "competition", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 1)")

if __name__ == "__main__":
    asyncio.run(add_chunk1_data())
