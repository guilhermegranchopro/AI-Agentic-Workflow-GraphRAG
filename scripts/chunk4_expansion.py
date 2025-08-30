import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk4_data():
    """Add fourth chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "healthcare_law_2008",
            "title": "Healthcare Law 2008",
            "content": "Regulates healthcare sector and medical services. Establishes health authority and licensing requirements. Defines patient rights and medical standards.",
            "type": "Law",
            "metadata": {"law_number": "2008/2", "effective_date": "2008-01-01", "jurisdiction": "Federal", "category": "Healthcare Law", "importance": "High"}
        },
        {
            "id": "education_law_1972",
            "title": "Education Law 1972",
            "content": "Establishes education system and standards. Defines curriculum requirements and teacher qualifications. Implements compulsory education framework.",
            "type": "Law",
            "metadata": {"law_number": "1972/11", "effective_date": "1972-01-01", "jurisdiction": "Federal", "category": "Education Law", "importance": "High"}
        },
        {
            "id": "tourism_law_2011",
            "title": "Tourism Law 2011",
            "content": "Regulates tourism sector and hospitality services. Establishes tourism authority and licensing framework. Defines tourism standards and visitor protection.",
            "type": "Law",
            "metadata": {"law_number": "2011/3", "effective_date": "2011-01-01", "jurisdiction": "Federal", "category": "Tourism Law", "importance": "Medium"}
        },
        {
            "id": "sports_law_2014",
            "title": "Sports Law 2014",
            "content": "Regulates sports activities and organizations. Establishes sports authority and anti-doping framework. Defines sports licensing and event management.",
            "type": "Law",
            "metadata": {"law_number": "2014/7", "effective_date": "2014-01-01", "jurisdiction": "Federal", "category": "Sports Law", "importance": "Medium"}
        },
        {
            "id": "charity_law_2014",
            "title": "Charity Law 2014",
            "content": "Regulates charitable organizations and donations. Establishes charity authority and fundraising standards. Defines transparency and accountability requirements.",
            "type": "Law",
            "metadata": {"law_number": "2014/4", "effective_date": "2014-01-01", "jurisdiction": "Federal", "category": "Charity Law", "importance": "Medium"}
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
        ("healthcare_law_2008", "data_protection_law_2021", "requires", {"type": "privacy_compliance", "weight": 1}),
        ("education_law_1972", "labor_law_2021", "supports", {"type": "employment_standards", "weight": 1}),
        ("tourism_law_2011", "commercial_code_1993", "regulates", {"type": "service_regulation", "weight": 1}),
        ("sports_law_2014", "commercial_companies_law_2015", "governs", {"type": "organization_regulation", "weight": 1}),
        ("charity_law_2014", "commercial_companies_law_2015", "regulates", {"type": "ngo_regulation", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 4)")

if __name__ == "__main__":
    asyncio.run(add_chunk4_data())
