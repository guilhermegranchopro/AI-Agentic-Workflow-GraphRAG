import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk8_data():
    """Add eighth chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "space_law_2019",
            "title": "Space Law 2019",
            "content": "Regulates space activities and satellite operations. Establishes space authority and licensing framework. Defines space safety and orbital debris management.",
            "type": "Law",
            "metadata": {"law_number": "2019/12", "effective_date": "2019-01-01", "jurisdiction": "Federal", "category": "Space Law", "importance": "Medium"}
        },
        {
            "id": "quantum_computing_law_2022",
            "title": "Quantum Computing Law 2022",
            "content": "Regulates quantum computing research and applications. Establishes quantum authority and security framework. Defines quantum encryption and cybersecurity standards.",
            "type": "Law",
            "metadata": {"law_number": "2022/25", "effective_date": "2022-01-01", "jurisdiction": "Federal", "category": "Quantum Computing Law", "importance": "High"}
        },
        {
            "id": "artificial_intelligence_law_2023",
            "title": "Artificial Intelligence Law 2023",
            "content": "Regulates AI development and deployment. Establishes AI authority and ethical framework. Defines AI safety and accountability standards.",
            "type": "Law",
            "metadata": {"law_number": "2023/8", "effective_date": "2023-01-01", "jurisdiction": "Federal", "category": "Artificial Intelligence Law", "importance": "High"}
        },
        {
            "id": "blockchain_law_2021",
            "title": "Blockchain Law 2021",
            "content": "Regulates blockchain technology and cryptocurrency. Establishes blockchain authority and regulatory framework. Defines digital asset and smart contract standards.",
            "type": "Law",
            "metadata": {"law_number": "2021/18", "effective_date": "2021-01-01", "jurisdiction": "Federal", "category": "Blockchain Law", "importance": "Medium"}
        },
        {
            "id": "metaverse_law_2024",
            "title": "Metaverse Law 2024",
            "content": "Regulates virtual reality and metaverse platforms. Establishes metaverse authority and governance framework. Defines virtual property and digital identity standards.",
            "type": "Law",
            "metadata": {"law_number": "2024/3", "effective_date": "2024-01-01", "jurisdiction": "Federal", "category": "Metaverse Law", "importance": "Medium"}
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
        ("space_law_2019", "aviation_law_1991", "extends", {"type": "aerospace_regulation", "weight": 1}),
        ("quantum_computing_law_2022", "cybersecurity_law_2022", "enhances", {"type": "quantum_security", "weight": 1}),
        ("artificial_intelligence_law_2023", "data_protection_law_2021", "requires", {"type": "ai_privacy", "weight": 1}),
        ("blockchain_law_2021", "securities_law_2000", "regulates", {"type": "digital_assets", "weight": 1}),
        ("metaverse_law_2024", "artificial_intelligence_law_2023", "supports", {"type": "virtual_reality", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 8)")

if __name__ == "__main__":
    asyncio.run(add_chunk8_data())
