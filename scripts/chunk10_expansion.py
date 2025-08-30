import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk10_data():
    """Add tenth chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "digital_identity_law_2022",
            "title": "Digital Identity Law 2022",
            "content": "Regulates digital identity and authentication systems. Establishes identity authority and verification framework. Defines digital identity standards and privacy protection.",
            "type": "Law",
            "metadata": {"law_number": "2022/16", "effective_date": "2022-01-01", "jurisdiction": "Federal", "category": "Digital Identity Law", "importance": "High"}
        },
        {
            "id": "digital_currency_law_2023",
            "title": "Digital Currency Law 2023",
            "content": "Regulates digital currencies and central bank digital currency. Establishes digital currency authority and regulatory framework. Defines CBDC standards and monetary policy.",
            "type": "Law",
            "metadata": {"law_number": "2023/11", "effective_date": "2023-01-01", "jurisdiction": "Federal", "category": "Digital Currency Law", "importance": "High"}
        },
        {
            "id": "digital_payment_law_2021",
            "title": "Digital Payment Law 2021",
            "content": "Regulates digital payment systems and fintech services. Establishes payment authority and licensing framework. Defines payment standards and consumer protection.",
            "type": "Law",
            "metadata": {"law_number": "2021/14", "effective_date": "2021-01-01", "jurisdiction": "Federal", "category": "Digital Payment Law", "importance": "Medium"}
        },
        {
            "id": "digital_asset_law_2024",
            "title": "Digital Asset Law 2024",
            "content": "Regulates digital assets and tokenization. Establishes digital asset authority and trading framework. Defines asset tokenization and custody standards.",
            "type": "Law",
            "metadata": {"law_number": "2024/5", "effective_date": "2024-01-01", "jurisdiction": "Federal", "category": "Digital Asset Law", "importance": "Medium"}
        },
        {
            "id": "digital_sovereignty_law_2023",
            "title": "Digital Sovereignty Law 2023",
            "content": "Regulates digital sovereignty and data localization. Establishes sovereignty authority and governance framework. Defines data sovereignty and national security standards.",
            "type": "Law",
            "metadata": {"law_number": "2023/19", "effective_date": "2023-01-01", "jurisdiction": "Federal", "category": "Digital Sovereignty Law", "importance": "High"}
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
        ("digital_identity_law_2022", "data_protection_law_2021", "requires", {"type": "identity_privacy", "weight": 1}),
        ("digital_currency_law_2023", "banking_regulations_2023", "regulates", {"type": "monetary_policy", "weight": 1}),
        ("digital_payment_law_2021", "banking_regulations_2023", "complements", {"type": "payment_systems", "weight": 1}),
        ("digital_asset_law_2024", "securities_law_2000", "extends", {"type": "asset_regulation", "weight": 1}),
        ("digital_sovereignty_law_2023", "cybersecurity_law_2022", "strengthens", {"type": "national_security", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 10)")

if __name__ == "__main__":
    asyncio.run(add_chunk10_data())
