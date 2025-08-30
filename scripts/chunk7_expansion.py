import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk7_data():
    """Add seventh chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "pharmaceutical_law_2007",
            "title": "Pharmaceutical Law 2007",
            "content": "Regulates pharmaceutical industry and drug manufacturing. Establishes drug authority and licensing requirements. Defines drug safety and quality standards.",
            "type": "Law",
            "metadata": {"law_number": "2007/8", "effective_date": "2007-01-01", "jurisdiction": "Federal", "category": "Pharmaceutical Law", "importance": "High"}
        },
        {
            "id": "medical_device_law_2008",
            "title": "Medical Device Law 2008",
            "content": "Regulates medical devices and equipment. Establishes device authority and registration framework. Defines safety and performance standards.",
            "type": "Law",
            "metadata": {"law_number": "2008/9", "effective_date": "2008-01-01", "jurisdiction": "Federal", "category": "Medical Device Law", "importance": "Medium"}
        },
        {
            "id": "clinical_trials_law_2019",
            "title": "Clinical Trials Law 2019",
            "content": "Regulates clinical trials and medical research. Establishes research authority and ethical framework. Defines trial protocols and participant protection.",
            "type": "Law",
            "metadata": {"law_number": "2019/12", "effective_date": "2019-01-01", "jurisdiction": "Federal", "category": "Clinical Trials Law", "importance": "Medium"}
        },
        {
            "id": "genetic_research_law_2020",
            "title": "Genetic Research Law 2020",
            "content": "Regulates genetic research and biotechnology. Establishes bioethics authority and research framework. Defines genetic privacy and consent requirements.",
            "type": "Law",
            "metadata": {"law_number": "2020/15", "effective_date": "2020-01-01", "jurisdiction": "Federal", "category": "Genetic Research Law", "importance": "Medium"}
        },
        {
            "id": "stem_cell_law_2021",
            "title": "Stem Cell Law 2021",
            "content": "Regulates stem cell research and therapy. Establishes stem cell authority and research standards. Defines ethical guidelines and safety protocols.",
            "type": "Law",
            "metadata": {"law_number": "2021/7", "effective_date": "2021-01-01", "jurisdiction": "Federal", "category": "Stem Cell Law", "importance": "Medium"}
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
        ("pharmaceutical_law_2007", "healthcare_law_2008", "supports", {"type": "healthcare_regulation", "weight": 1}),
        ("medical_device_law_2008", "healthcare_law_2008", "complements", {"type": "medical_standards", "weight": 1}),
        ("clinical_trials_law_2019", "pharmaceutical_law_2007", "regulates", {"type": "research_regulation", "weight": 1}),
        ("genetic_research_law_2020", "data_protection_law_2021", "requires", {"type": "genetic_privacy", "weight": 1}),
        ("stem_cell_law_2021", "genetic_research_law_2020", "extends", {"type": "biotechnology_regulation", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 7)")

if __name__ == "__main__":
    asyncio.run(add_chunk7_data())
