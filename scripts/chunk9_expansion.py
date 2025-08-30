import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk9_data():
    """Add ninth chunk of additional legal data."""
    
    neo4j_conn = Neo4jConnection()
    
    # 5 new legal nodes
    new_nodes = [
        {
            "id": "renewable_energy_law_2015",
            "title": "Renewable Energy Law 2015",
            "content": "Regulates renewable energy sector and clean technology. Establishes energy authority and licensing framework. Defines renewable energy standards and incentives.",
            "type": "Law",
            "metadata": {"law_number": "2015/12", "effective_date": "2015-01-01", "jurisdiction": "Federal", "category": "Renewable Energy Law", "importance": "High"}
        },
        {
            "id": "carbon_trading_law_2020",
            "title": "Carbon Trading Law 2020",
            "content": "Regulates carbon trading and emissions reduction. Establishes carbon authority and trading framework. Defines carbon credits and offset mechanisms.",
            "type": "Law",
            "metadata": {"law_number": "2020/18", "effective_date": "2020-01-01", "jurisdiction": "Federal", "category": "Carbon Trading Law", "importance": "Medium"}
        },
        {
            "id": "circular_economy_law_2022",
            "title": "Circular Economy Law 2022",
            "content": "Regulates circular economy and waste management. Establishes circular economy authority and framework. Defines recycling and resource efficiency standards.",
            "type": "Law",
            "metadata": {"law_number": "2022/9", "effective_date": "2022-01-01", "jurisdiction": "Federal", "category": "Circular Economy Law", "importance": "Medium"}
        },
        {
            "id": "green_building_law_2018",
            "title": "Green Building Law 2018",
            "content": "Regulates green building standards and sustainability. Establishes building authority and certification framework. Defines energy efficiency and environmental standards.",
            "type": "Law",
            "metadata": {"law_number": "2018/15", "effective_date": "2018-01-01", "jurisdiction": "Federal", "category": "Green Building Law", "importance": "Medium"}
        },
        {
            "id": "climate_adaptation_law_2023",
            "title": "Climate Adaptation Law 2023",
            "content": "Regulates climate adaptation and resilience measures. Establishes climate authority and adaptation framework. Defines climate risk and adaptation strategies.",
            "type": "Law",
            "metadata": {"law_number": "2023/22", "effective_date": "2023-01-01", "jurisdiction": "Federal", "category": "Climate Adaptation Law", "importance": "High"}
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
        ("renewable_energy_law_2015", "environmental_law_1999", "supports", {"type": "clean_energy", "weight": 1}),
        ("carbon_trading_law_2020", "renewable_energy_law_2015", "complements", {"type": "emissions_reduction", "weight": 1}),
        ("circular_economy_law_2022", "environmental_law_1999", "extends", {"type": "sustainable_development", "weight": 1}),
        ("green_building_law_2018", "construction_law_2008", "enhances", {"type": "sustainable_construction", "weight": 1}),
        ("climate_adaptation_law_2023", "environmental_law_1999", "strengthens", {"type": "climate_resilience", "weight": 1})
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
    
    print("✅ Added 5 new legal nodes and 5 relationships (Chunk 9)")

if __name__ == "__main__":
    asyncio.run(add_chunk9_data())
