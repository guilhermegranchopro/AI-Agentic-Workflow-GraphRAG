import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk2_data():
    """Add second chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "arbitration_law_2018",
            "title": "Arbitration Law 2018",
            "content": "Establishes framework for domestic and international arbitration. Defines arbitration procedures and enforcement mechanisms. Implements UNCITRAL Model Law principles.",
            "type": "Law",
            "metadata": {"law_number": "2018/6", "effective_date": "2018-01-01", "jurisdiction": "Federal", "category": "Arbitration Law", "importance": "High"}
        },
        {
            "id": "evidence_law_1992",
            "title": "Evidence Law 1992",
            "content": "Regulates evidence rules for civil and commercial proceedings. Defines admissible evidence types and procedures. Establishes expert witness framework.",
            "type": "Law",
            "metadata": {"law_number": "1992/10", "effective_date": "1992-01-01", "jurisdiction": "Federal", "category": "Evidence Law", "importance": "Medium"}
        },
        {
            "id": "insurance_law_2007",
            "title": "Insurance Law 2007",
            "content": "Regulates insurance industry and policies. Establishes insurance company requirements and consumer protection. Defines mandatory insurance types.",
            "type": "Law",
            "metadata": {"law_number": "2007/6", "effective_date": "2007-01-01", "jurisdiction": "Federal", "category": "Insurance Law", "importance": "Medium"}
        },
        {
            "id": "securities_law_2000",
            "title": "Securities Law 2000",
            "content": "Regulates securities markets and trading. Establishes Securities and Commodities Authority. Defines disclosure requirements and market conduct.",
            "type": "Law",
            "metadata": {"law_number": "2000/4", "effective_date": "2000-01-01", "jurisdiction": "Federal", "category": "Securities Law", "importance": "High"}
        },
        {
            "id": "environmental_law_1999",
            "title": "Environmental Law 1999",
            "content": "Protects environment and natural resources. Establishes environmental standards and penalties. Implements sustainable development principles.",
            "type": "Law",
            "metadata": {"law_number": "1999/24", "effective_date": "1999-01-01", "jurisdiction": "Federal", "category": "Environmental Law", "importance": "Medium"}
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
        ("arbitration_law_2018", "court_system_2020", "alternative_to", {"type": "dispute_resolution", "weight": 1}),
        ("evidence_law_1992", "civil_code_1985", "supports", {"type": "legal_procedure", "weight": 1}),
        ("insurance_law_2007", "commercial_code_1993", "regulates", {"type": "financial_services", "weight": 1}),
        ("securities_law_2000", "commercial_companies_law_2015", "governs", {"type": "market_regulation", "weight": 1}),
        ("environmental_law_1999", "real_estate_law_2006", "influences", {"type": "compliance", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 2)")

if __name__ == "__main__":
    asyncio.run(add_chunk2_data())
