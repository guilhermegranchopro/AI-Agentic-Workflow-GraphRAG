import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk11_contradictions():
    """Add eleventh chunk with additional contradictions for AI Analysis."""
    
    neo4j_conn = Neo4jConnection()
    
    # Create additional contradictions with different priority levels
    contradictions = [
        {
            "source": "digital_currency_law_2023",
            "target": "blockchain_law_2021",
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "major",
            "category": "digital_regulation",
            "description": "Digital Currency Law 2023 establishes centralized CBDC framework while Blockchain Law 2021 promotes decentralized cryptocurrency, creating regulatory conflicts."
        },
        {
            "source": "artificial_intelligence_law_2023",
            "target": "data_protection_law_2021",
            "type": "CONTRADICTS",
            "priority": "medium",
            "severity": "moderate",
            "category": "ai_privacy",
            "description": "AI Law 2023 allows extensive data processing for AI training while Data Protection Law 2021 restricts personal data usage, creating privacy conflicts."
        },
        {
            "source": "renewable_energy_law_2015",
            "target": "oil_gas_law_1993",
            "type": "CONTRADICTS",
            "priority": "low",
            "severity": "minor",
            "category": "energy_policy",
            "description": "Renewable Energy Law 2023 promotes clean energy transition while Oil & Gas Law 1993 supports traditional energy sector, creating policy tensions."
        },
        {
            "source": "digital_sovereignty_law_2023",
            "target": "international_trade_law_1994",
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "major",
            "category": "trade_regulation",
            "description": "Digital Sovereignty Law 2023 requires data localization while International Trade Law 1994 promotes cross-border data flows, creating trade conflicts."
        },
        {
            "source": "climate_adaptation_law_2023",
            "target": "real_estate_law_2006",
            "type": "CONTRADICTS",
            "priority": "medium",
            "severity": "moderate",
            "category": "environmental_compliance",
            "description": "Climate Adaptation Law 2023 requires climate-resilient development while Real Estate Law 2006 allows traditional construction, creating compliance conflicts."
        }
    ]
    
    # Create contradictions
    for contradiction in contradictions:
        await neo4j_conn.run_cypher("""
            MATCH (a:LegalNode {id: $source})
            MATCH (b:LegalNode {id: $target})
            MERGE (a)-[r:RELATES_TO]->(b)
            SET r.type = $type,
                r.priority = $priority,
                r.severity = $severity,
                r.category = $category,
                r.description = $description,
                r.weight = 1
        """, {
            "source": contradiction["source"],
            "target": contradiction["target"],
            "type": contradiction["type"],
            "priority": contradiction["priority"],
            "severity": contradiction["severity"],
            "category": contradiction["category"],
            "description": contradiction["description"]
        })
    
    print("✅ Added 5 new contradictions with varying priority levels (Chunk 11)")

if __name__ == "__main__":
    asyncio.run(add_chunk11_contradictions())
