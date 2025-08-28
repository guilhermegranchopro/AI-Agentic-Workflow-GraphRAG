#!/usr/bin/env python3
"""
Script to load mock UAE legal data into Neo4j knowledge graph
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def clear_neo4j_database(neo4j_conn):
    """Clear all data from Neo4j database."""
    print("🗑️  Clearing Neo4j database...")
    
    try:
        # Delete all nodes and relationships
        clear_query = "MATCH (n) DETACH DELETE n"
        await neo4j_conn.run_cypher(clear_query)
        print("✅ Database cleared successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to clear database: {e}")
        return False

async def load_mock_uae_legal_data(neo4j_conn):
    """Load comprehensive mock UAE legal data into Neo4j."""
    print("📚 Loading mock UAE legal data...")
    
    # UAE Legal System Overview
    legal_system_data = [
        {
            "type": "LegalSystem",
            "id": "uae_legal_system",
            "title": "UAE Legal System",
            "content": "The UAE legal system is based on civil law principles with Islamic Sharia as a primary source. The system includes federal and local laws, with the Federal Supreme Court as the highest judicial authority.",
            "metadata": {"jurisdiction": "federal", "legal_family": "civil_law"}
        }
    ]
    
    # UAE Constitution
    constitution_data = [
        {
            "type": "Constitution",
            "id": "uae_constitution",
            "title": "UAE Constitution",
            "content": "The UAE Constitution establishes the federation of seven emirates, defines the powers of federal and local authorities, and guarantees fundamental rights and freedoms.",
            "metadata": {"year": 1971, "amended": 2004}
        }
    ]
    
    # Business and Commercial Law
    business_law_data = [
        {
            "type": "Law",
            "id": "commercial_companies_law",
            "title": "Commercial Companies Law",
            "content": "Federal Law No. 2 of 2015 regulates the formation, management, and dissolution of commercial companies in the UAE, including LLCs, joint stock companies, and partnerships.",
            "metadata": {"law_number": "2/2015", "category": "commercial"}
        },
        {
            "type": "Law",
            "id": "commercial_transactions_law",
            "title": "Commercial Transactions Law",
            "content": "Federal Law No. 18 of 1993 governs commercial transactions, contracts, banking operations, and commercial instruments in the UAE.",
            "metadata": {"law_number": "18/1993", "category": "commercial"}
        },
        {
            "type": "Regulation",
            "id": "business_licensing",
            "title": "Business Licensing Requirements",
            "content": "Businesses in the UAE require appropriate licenses from relevant authorities. Mainland companies need trade licenses, while free zone companies have specific licensing requirements.",
            "metadata": {"category": "licensing", "applicable_to": "all_businesses"}
        }
    ]
    
    # Labor Law
    labor_law_data = [
        {
            "type": "Law",
            "id": "labor_law",
            "title": "UAE Labor Law",
            "content": "Federal Law No. 33 of 2021 regulates employment relationships, working conditions, wages, termination, and employee rights in the UAE.",
            "metadata": {"law_number": "33/2021", "category": "employment"}
        },
        {
            "type": "Regulation",
            "id": "work_visa_requirements",
            "title": "Work Visa Requirements",
            "content": "Foreign workers require work permits and residence visas. Employers must sponsor employees and comply with quota systems and labor card requirements.",
            "metadata": {"category": "immigration", "applicable_to": "foreign_workers"}
        }
    ]
    
    # Corporate Law
    corporate_law_data = [
        {
            "type": "Law",
            "id": "corporate_governance",
            "title": "Corporate Governance Regulations",
            "content": "UAE companies must comply with corporate governance standards including board composition, audit requirements, and shareholder rights protection.",
            "metadata": {"category": "governance", "applicable_to": "public_companies"}
        },
        {
            "type": "Regulation",
            "id": "foreign_ownership",
            "title": "Foreign Ownership Regulations",
            "content": "Foreign ownership restrictions apply in certain sectors. Free zones allow 100% foreign ownership, while mainland companies may require UAE national partners.",
            "metadata": {"category": "ownership", "applicable_to": "foreign_investors"}
        }
    ]
    
    # Tax Law
    tax_law_data = [
        {
            "type": "Law",
            "id": "corporate_tax",
            "title": "Corporate Tax Law",
            "content": "Federal Decree-Law No. 47 of 2022 introduces corporate tax at 9% for taxable income above AED 375,000, effective from June 2023.",
            "metadata": {"law_number": "47/2022", "rate": "9%", "threshold": "AED 375,000"}
        },
        {
            "type": "Law",
            "id": "vat_law",
            "title": "Value Added Tax Law",
            "content": "Federal Decree-Law No. 8 of 2017 establishes VAT at 5% on most goods and services, with specific exemptions and zero-rated supplies.",
            "metadata": {"law_number": "8/2017", "rate": "5%", "effective": "2018"}
        }
    ]
    
    # Intellectual Property
    ip_law_data = [
        {
            "type": "Law",
            "id": "intellectual_property",
            "title": "Intellectual Property Protection",
            "content": "UAE provides comprehensive IP protection including patents, trademarks, copyrights, and industrial designs through federal laws and international treaties.",
            "metadata": {"category": "intellectual_property", "protection_type": "comprehensive"}
        }
    ]
    
    # Banking and Finance
    banking_law_data = [
        {
            "type": "Law",
            "id": "banking_regulations",
            "title": "Banking and Financial Regulations",
            "content": "The Central Bank of UAE regulates banking activities, financial institutions, and monetary policy. Islamic banking principles are also recognized.",
            "metadata": {"regulator": "central_bank", "category": "financial_services"}
        }
    ]
    
    # Free Zones
    free_zone_data = [
        {
            "type": "Zone",
            "id": "dubai_free_zones",
            "title": "Dubai Free Zones",
            "content": "Dubai offers multiple free zones including DIFC, DMCC, and Dubai Internet City, providing 100% foreign ownership, tax benefits, and streamlined business setup.",
            "metadata": {"location": "dubai", "ownership": "100%_foreign", "tax_benefits": True}
        },
        {
            "type": "Zone",
            "id": "abu_dhabi_free_zones",
            "title": "Abu Dhabi Free Zones",
            "content": "Abu Dhabi free zones like ADGM and twofour54 offer international business environment with common law framework and tax advantages.",
            "metadata": {"location": "abu_dhabi", "legal_framework": "common_law"}
        }
    ]
    
    # Dispute Resolution
    dispute_resolution_data = [
        {
            "type": "System",
            "id": "court_system",
            "title": "UAE Court System",
            "content": "The UAE has a three-tier court system: Courts of First Instance, Courts of Appeal, and Federal Supreme Court. Specialized courts handle commercial and labor disputes.",
            "metadata": {"tiers": 3, "specialized_courts": True}
        },
        {
            "type": "System",
            "id": "arbitration",
            "title": "Arbitration Framework",
            "content": "UAE supports both domestic and international arbitration. DIFC and ADGM have their own arbitration centers with international recognition.",
            "metadata": {"type": "domestic_international", "centers": ["DIFC", "ADGM"]}
        }
    ]
    
    # Compliance and Anti-Money Laundering
    compliance_data = [
        {
            "type": "Law",
            "id": "aml_cft",
            "title": "Anti-Money Laundering and Counter-Terrorism Financing",
            "content": "Federal Law No. 20 of 2018 establishes AML/CFT framework requiring customer due diligence, suspicious transaction reporting, and compliance programs.",
            "metadata": {"law_number": "20/2018", "category": "compliance"}
        }
    ]
    
    # Combine all data
    all_data = (
        legal_system_data + constitution_data + business_law_data + 
        labor_law_data + corporate_law_data + tax_law_data + 
        ip_law_data + banking_law_data + free_zone_data + 
        dispute_resolution_data + compliance_data
    )
    
    try:
        # Create nodes
        for item in all_data:
            create_node_query = """
            CREATE (n:LegalNode {
                id: $id,
                type: $type,
                title: $title,
                content: $content,
                metadata: $metadata,
                score: $score,
                timestamp: datetime()
            })
            """
            await neo4j_conn.run_cypher(create_node_query, {
                "id": item["id"],
                "type": item["type"],
                "title": item["title"],
                "content": item["content"],
                "metadata": json.dumps(item["metadata"]),
                "score": 1.0
            })
        
        # Create relationships
        relationships = [
            # Legal System relationships
            ("uae_legal_system", "uae_constitution", "CONTAINS"),
            ("uae_legal_system", "commercial_companies_law", "GOVERNED_BY"),
            ("uae_legal_system", "labor_law", "GOVERNED_BY"),
            ("uae_legal_system", "corporate_tax", "GOVERNED_BY"),
            
            # Business Law relationships
            ("commercial_companies_law", "business_licensing", "REQUIRES"),
            ("commercial_companies_law", "corporate_governance", "INCLUDES"),
            ("commercial_companies_law", "foreign_ownership", "REGULATES"),
            
            # Tax relationships
            ("corporate_tax", "vat_law", "COMPLEMENTS"),
            ("corporate_tax", "business_licensing", "AFFECTS"),
            
            # Free Zone relationships
            ("dubai_free_zones", "foreign_ownership", "ALLOWS"),
            ("abu_dhabi_free_zones", "foreign_ownership", "ALLOWS"),
            ("dubai_free_zones", "corporate_tax", "EXEMPT_FROM"),
            ("abu_dhabi_free_zones", "corporate_tax", "EXEMPT_FROM"),
            
            # Dispute Resolution relationships
            ("court_system", "arbitration", "ALTERNATIVE_TO"),
            ("commercial_companies_law", "court_system", "ENFORCED_BY"),
            ("labor_law", "court_system", "ENFORCED_BY"),
            
            # Compliance relationships
            ("aml_cft", "banking_regulations", "APPLIES_TO"),
            ("aml_cft", "commercial_companies_law", "APPLIES_TO"),
            
            # IP relationships
            ("intellectual_property", "commercial_companies_law", "PROTECTS"),
            ("intellectual_property", "business_licensing", "REQUIRED_FOR"),
            
            # Labor relationships
            ("labor_law", "work_visa_requirements", "INCLUDES"),
            ("labor_law", "business_licensing", "REQUIRES"),
        ]
        
        for source_id, target_id, relationship_type in relationships:
            create_rel_query = """
            MATCH (a:LegalNode {id: $source_id})
            MATCH (b:LegalNode {id: $target_id})
            CREATE (a)-[r:RELATES_TO {type: $rel_type, weight: 1.0}]->(b)
            """
            await neo4j_conn.run_cypher(create_rel_query, {
                "source_id": source_id,
                "target_id": target_id,
                "rel_type": relationship_type
            })
        
        print(f"✅ Successfully loaded {len(all_data)} legal nodes and {len(relationships)} relationships")
        return True
        
    except Exception as e:
        print(f"❌ Failed to load mock data: {e}")
        return False

async def verify_data_loaded(neo4j_conn):
    """Verify that the data was loaded correctly."""
    print("🔍 Verifying loaded data...")
    
    try:
        # Count nodes
        node_count_query = "MATCH (n:LegalNode) RETURN count(n) as count"
        node_result = await neo4j_conn.run_cypher(node_count_query)
        node_count = node_result[0]["count"] if node_result else 0
        
        # Count relationships
        rel_count_query = "MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count"
        rel_result = await neo4j_conn.run_cypher(rel_count_query)
        rel_count = rel_result[0]["count"] if rel_result else 0
        
        # Get sample nodes
        sample_query = "MATCH (n:LegalNode) RETURN n.title, n.type LIMIT 5"
        sample_result = await neo4j_conn.run_cypher(sample_query)
        
        print(f"✅ Database contains {node_count} nodes and {rel_count} relationships")
        print("📋 Sample nodes:")
        for record in sample_result:
            print(f"   - {record['n.title']} ({record['n.type']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to verify data: {e}")
        return False

async def main():
    """Main function to load mock data."""
    print("🚀 UAE Legal Knowledge Graph - Mock Data Loader")
    print("=" * 50)
    
    try:
        # Initialize Neo4j connection
        from backend.app.adapters.neo4j_conn import Neo4jConnection
        neo4j_conn = Neo4jConnection()
        
        # Test connection
        health = await neo4j_conn.health_check()
        if health.get("status") != "healthy":
            print("❌ Neo4j connection failed")
            return False
        
        print("✅ Neo4j connection established")
        
        # Clear existing data
        if not await clear_neo4j_database(neo4j_conn):
            return False
        
        # Load mock data
        if not await load_mock_uae_legal_data(neo4j_conn):
            return False
        
        # Verify data
        if not await verify_data_loaded(neo4j_conn):
            return False
        
        print("\n🎉 Mock UAE legal data loaded successfully!")
        print("📊 The knowledge graph now contains comprehensive UAE legal information")
        print("🔍 You can now test the GraphRAG functionality with real legal data")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to load mock data: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
