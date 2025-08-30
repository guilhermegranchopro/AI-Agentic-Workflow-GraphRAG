import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def add_chunk6_contradictions():
    """Add sixth chunk with additional contradictions for AI Analysis."""
    
    neo4j_conn = Neo4jConnection()
    
    # Create additional contradictions with different priority levels
    contradictions = [
        {
            "source": "criminal_law_1987",
            "target": "cybersecurity_law_2022",
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "major",
            "category": "digital_crimes",
            "description": "Criminal Law 1987 lacks specific provisions for cyber crimes, while Cybersecurity Law 2022 introduces new digital offense categories"
        },
        {
            "source": "family_law_2005",
            "target": "data_protection_law_2021",
            "type": "CONTRADICTS",
            "priority": "medium",
            "severity": "moderate",
            "category": "privacy_rights",
            "description": "Family Law 2005 allows broader information sharing in family matters, while Data Protection Law 2021 imposes strict privacy restrictions"
        },
        {
            "source": "commercial_agency_law_1981",
            "target": "antitrust_law_2012",
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "major",
            "category": "competition_policy",
            "description": "Commercial Agency Law 1981 grants exclusive agency rights, while Antitrust Law 2012 prohibits anti-competitive practices"
        },
        {
            "source": "consumer_protection_law_2006",
            "target": "insurance_law_2007",
            "type": "CONTRADICTS",
            "priority": "medium",
            "severity": "moderate",
            "category": "consumer_rights",
            "description": "Consumer Protection Law 2006 provides broad consumer rights, while Insurance Law 2007 has specific limitations on insurance claims"
        },
        {
            "source": "securities_law_2000",
            "target": "banking_regulations_2023",
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "major",
            "category": "financial_regulation",
            "description": "Securities Law 2000 has different disclosure requirements compared to Banking Regulations 2023 for financial institutions"
        }
    ]
    
    # Create contradiction relationships
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
    
    print("✅ Added 5 new contradictions with varying priority levels (Chunk 6)")

if __name__ == "__main__":
    asyncio.run(add_chunk6_contradictions())
