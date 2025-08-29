#!/usr/bin/env python3
"""
Script to load comprehensive UAE legal data with realistic contradictions into Neo4j knowledge graph
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.adapters.neo4j_conn import Neo4jConnection
from backend.app.schemas.config import settings

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

async def load_contradictory_uae_legal_data(neo4j_conn):
    """Load comprehensive UAE legal data with realistic contradictions."""
    print("📚 Loading comprehensive UAE legal data with contradictions...")
    
    # Comprehensive UAE Legal System Data with Contradictions
    legal_data = [
        # UAE Legal System Overview
        {
            "type": "LegalSystem",
            "id": "uae_legal_system",
            "title": "UAE Legal System",
            "content": "The UAE legal system is based on civil law principles with Islamic Sharia as a primary source. The system includes federal and local laws, with the Federal Supreme Court as the highest judicial authority. The UAE follows a dual legal system with both federal and emirate-level jurisdictions.",
            "metadata": {"jurisdiction": "federal", "legal_family": "civil_law", "sharia_influence": True}
        },
        
        # UAE Constitution
        {
            "type": "Constitution",
            "id": "uae_constitution",
            "title": "UAE Constitution",
            "content": "The UAE Constitution establishes the federation of seven emirates, defines the powers of federal and local authorities, and guarantees fundamental rights and freedoms. It establishes the Federal Supreme Council as the highest authority and outlines the structure of federal institutions.",
            "metadata": {"year": 1971, "amended": 2004, "emirates": 7}
        },
        
        # Business and Commercial Law
        {
            "type": "Law",
            "id": "commercial_companies_law",
            "title": "Commercial Companies Law",
            "content": "Federal Law No. 2 of 2015 regulates the formation, management, and dissolution of commercial companies in the UAE, including LLCs, joint stock companies, and partnerships. It establishes corporate governance requirements, shareholder rights, and regulatory compliance obligations.",
            "metadata": {"law_number": "2/2015", "category": "commercial", "foreign_ownership": "allowed"}
        },
        
        {
            "type": "Law",
            "id": "commercial_transactions_law",
            "title": "Commercial Transactions Law",
            "content": "Federal Law No. 18 of 1993 governs commercial transactions, contracts, banking operations, and commercial instruments in the UAE. It covers agency relationships, commercial contracts, banking operations, and negotiable instruments.",
            "metadata": {"law_number": "18/1993", "category": "commercial", "scope": "transactions"}
        },
        
        {
            "type": "Regulation",
            "id": "business_licensing",
            "title": "Business Licensing Requirements",
            "content": "Businesses in the UAE require appropriate licenses from relevant authorities. Mainland companies need trade licenses from DED, while free zone companies have specific licensing requirements. Different license types include commercial, professional, industrial, and tourism licenses.",
            "metadata": {"category": "licensing", "applicable_to": "all_businesses", "authority": "DED"}
        },
        
        # Labor Law - CONTRADICTION 1: Different notice periods
        {
            "type": "Law",
            "id": "labor_law_2021",
            "title": "UAE Labor Law 2021",
            "content": "Federal Law No. 33 of 2021 regulates employment relationships, working conditions, wages, termination, and employee rights in the UAE. It establishes minimum wage requirements, working hours, leave entitlements, and dispute resolution mechanisms. Notice period for termination is 30 days.",
            "metadata": {"law_number": "33/2021", "category": "employment", "effective_date": "2022", "notice_period": "30_days"}
        },
        
        {
            "type": "Regulation",
            "id": "labor_law_1980",
            "title": "UAE Labor Law 1980 (Amended)",
            "content": "Federal Law No. 8 of 1980 (as amended) regulates employment relationships in the UAE. This law establishes different notice periods: 14 days for workers with less than 5 years of service, and 30 days for workers with 5 or more years of service.",
            "metadata": {"law_number": "8/1980", "category": "employment", "notice_period": "14_30_days", "amended": True}
        },
        
        {
            "type": "Regulation",
            "id": "work_visa_requirements",
            "title": "Work Visa Requirements",
            "content": "Foreign workers require work permits and residence visas. Employers must sponsor employees and comply with quota systems and labor card requirements. The process involves obtaining labor card, entry permit, medical fitness test, and residence visa.",
            "metadata": {"category": "immigration", "applicable_to": "foreign_workers", "sponsorship": "required"}
        },
        
        # Corporate Tax - CONTRADICTION 2: Different tax rates
        {
            "type": "Law",
            "id": "corporate_tax_2022",
            "title": "Corporate Tax Law 2022",
            "content": "Federal Decree-Law No. 47 of 2022 introduces corporate tax at 9% for taxable income above AED 375,000, effective from June 2023. It applies to UAE companies and foreign companies with permanent establishments in the UAE. Free zone companies may be exempt under certain conditions.",
            "metadata": {"law_number": "47/2022", "rate": "9%", "threshold": "AED 375,000", "effective": "2023"}
        },
        
        {
            "type": "Law",
            "id": "corporate_tax_amendment_2024",
            "title": "Corporate Tax Amendment 2024",
            "content": "Amendment to Federal Decree-Law No. 47 of 2022 introduces progressive corporate tax rates: 0% for income up to AED 375,000, 5% for income between AED 375,000 and AED 1,000,000, and 9% for income above AED 1,000,000. This creates a more progressive tax system.",
            "metadata": {"law_number": "47/2022_amended", "rate": "0_5_9%", "threshold": "progressive", "effective": "2024", "amendment": True}
        },
        
        {
            "type": "Law",
            "id": "vat_law",
            "title": "Value Added Tax Law",
            "content": "Federal Decree-Law No. 8 of 2017 establishes VAT at 5% on most goods and services, with specific exemptions and zero-rated supplies. It requires businesses with annual turnover above AED 375,000 to register for VAT and file regular returns.",
            "metadata": {"law_number": "8/2017", "rate": "5%", "effective": "2018", "threshold": "AED 375,000"}
        },
        
        # Intellectual Property - CONTRADICTION 3: Different protection periods
        {
            "type": "Law",
            "id": "intellectual_property_2016",
            "title": "Intellectual Property Protection 2016",
            "content": "UAE provides comprehensive IP protection including patents, trademarks, copyrights, and industrial designs through federal laws and international treaties. The UAE is a member of WIPO and various international IP conventions. Protection is available for 20 years for patents and 10 years for trademarks.",
            "metadata": {"category": "intellectual_property", "protection_type": "comprehensive", "wipo_member": True, "patent_period": "20_years", "trademark_period": "10_years"}
        },
        
        {
            "type": "Law",
            "id": "intellectual_property_2023",
            "title": "Intellectual Property Protection 2023",
            "content": "Updated UAE IP protection laws extend protection periods: patents are protected for 25 years, trademarks for 15 years, and copyrights for 70 years after the author's death. This aligns with international standards and provides stronger protection for innovators.",
            "metadata": {"category": "intellectual_property", "protection_type": "enhanced", "patent_period": "25_years", "trademark_period": "15_years", "copyright_period": "70_years", "effective": "2023"}
        },
        
        # Banking and Financial - CONTRADICTION 4: Different capital requirements
        {
            "type": "Law",
            "id": "banking_regulations_2018",
            "title": "Banking and Financial Regulations 2018",
            "content": "The Central Bank of UAE regulates banking activities, financial institutions, and monetary policy. Islamic banking principles are also recognized. The regulatory framework includes capital adequacy requirements of 12.5% for conventional banks and 10% for Islamic banks.",
            "metadata": {"regulator": "central_bank", "category": "financial_services", "islamic_banking": True, "capital_adequacy": "12.5%_conventional", "islamic_capital": "10%"}
        },
        
        {
            "type": "Law",
            "id": "banking_regulations_2023",
            "title": "Banking and Financial Regulations 2023",
            "content": "Updated banking regulations increase capital adequacy requirements: 15% for conventional banks and 12% for Islamic banks. This strengthens the financial system and aligns with Basel III standards. Additional liquidity requirements are also introduced.",
            "metadata": {"regulator": "central_bank", "category": "financial_services", "capital_adequacy": "15%_conventional", "islamic_capital": "12%", "effective": "2023", "basel_iii": True}
        },
        
        # Free Zones - CONTRADICTION 5: Different ownership rules
        {
            "type": "Zone",
            "id": "dubai_free_zones_2020",
            "title": "Dubai Free Zones 2020",
            "content": "Dubai offers multiple free zones including DIFC, DMCC, and Dubai Internet City, providing 100% foreign ownership, tax benefits, and streamlined business setup. Each free zone has specific regulations and benefits. DIFC operates under English common law and has its own judicial system.",
            "metadata": {"location": "dubai", "ownership": "100%_foreign", "tax_benefits": True, "count": "multiple", "year": "2020"}
        },
        
        {
            "type": "Zone",
            "id": "dubai_free_zones_2024",
            "title": "Dubai Free Zones 2024",
            "content": "Updated Dubai free zone regulations introduce sector-specific ownership restrictions: 100% foreign ownership for technology and innovation companies, 70% for manufacturing companies, and 51% for retail and trading companies. This creates a more nuanced approach to foreign investment.",
            "metadata": {"location": "dubai", "ownership": "sector_specific", "tech_ownership": "100%", "manufacturing_ownership": "70%", "retail_ownership": "51%", "year": "2024"}
        },
        
        {
            "type": "Zone",
            "id": "abu_dhabi_free_zones",
            "title": "Abu Dhabi Free Zones",
            "content": "Abu Dhabi offers free zones like ADGM and twofour54, providing 100% foreign ownership and tax benefits. ADGM operates under English common law and has its own regulatory framework for financial services and commercial activities.",
            "metadata": {"location": "abu_dhabi", "ownership": "100%_foreign", "tax_benefits": True, "common_law": True}
        },
        
        # Court System - CONTRADICTION 6: Different jurisdiction rules
        {
            "type": "System",
            "id": "court_system_2020",
            "title": "UAE Court System 2020",
            "content": "The UAE has a three-tier court system: Courts of First Instance, Courts of Appeal, and Federal Supreme Court. Specialized courts handle commercial and labor disputes. DIFC and ADGM have their own independent court systems operating under English common law.",
            "metadata": {"tiers": 3, "specialized_courts": True, "difc_courts": True, "year": "2020"}
        },
        
        {
            "type": "System",
            "id": "court_system_2024",
            "title": "UAE Court System 2024",
            "content": "Updated court system introduces new specialized courts for technology disputes, intellectual property cases, and international commercial disputes. The jurisdiction of DIFC courts is expanded to cover all technology-related disputes across the UAE, creating potential conflicts with federal courts.",
            "metadata": {"tiers": 3, "specialized_courts": True, "tech_courts": True, "ip_courts": True, "difc_expansion": True, "year": "2024"}
        },
        
        {
            "type": "System",
            "id": "arbitration",
            "title": "Arbitration Framework",
            "content": "UAE supports both domestic and international arbitration. DIFC and ADGM have their own arbitration centers with international recognition. The UAE is a signatory to the New York Convention on the Recognition and Enforcement of Foreign Arbitral Awards.",
            "metadata": {"type": "domestic_international", "centers": ["DIFC", "ADGM"], "new_york_convention": True}
        },
        
        # Compliance and AML - CONTRADICTION 7: Different reporting requirements
        {
            "type": "Law",
            "id": "aml_cft_2018",
            "title": "Anti-Money Laundering and Counter-Terrorism Financing 2018",
            "content": "Federal Law No. 20 of 2018 establishes AML/CFT framework requiring customer due diligence, suspicious transaction reporting, and compliance programs. Financial institutions must implement risk-based approaches and maintain comprehensive records. Reporting threshold is AED 50,000.",
            "metadata": {"law_number": "20/2018", "category": "compliance", "fatf_compliant": True, "reporting_threshold": "AED 50,000"}
        },
        
        {
            "type": "Law",
            "id": "aml_cft_2023",
            "title": "Anti-Money Laundering and Counter-Terrorism Financing 2023",
            "content": "Updated AML/CFT regulations lower the reporting threshold to AED 25,000 and introduce real-time transaction monitoring requirements. Virtual asset service providers are now included in the regulatory framework, creating additional compliance obligations.",
            "metadata": {"law_number": "20/2018_amended", "category": "compliance", "reporting_threshold": "AED 25,000", "real_time_monitoring": True, "vasp_regulation": True, "effective": "2023"}
        },
        
        # Real Estate - CONTRADICTION 8: Different ownership restrictions
        {
            "type": "Law",
            "id": "real_estate_law_2020",
            "title": "Real Estate Law 2020",
            "content": "UAE real estate law governs property ownership, development, and transactions. Foreign ownership is allowed in designated areas and free zones. The law covers property registration, development regulations, and dispute resolution mechanisms. Foreign ownership is limited to 99-year leasehold in designated areas.",
            "metadata": {"category": "real_estate", "foreign_ownership": "leasehold_99_years", "designated_areas": True, "year": "2020"}
        },
        
        {
            "type": "Law",
            "id": "real_estate_law_2024",
            "title": "Real Estate Law 2024",
            "content": "Updated real estate law introduces freehold ownership for foreigners in specific areas, extending beyond the previous 99-year leasehold restrictions. This creates a dual system where some areas allow freehold ownership while others maintain leasehold restrictions.",
            "metadata": {"category": "real_estate", "foreign_ownership": "freehold_available", "leasehold_99_years": True, "dual_system": True, "year": "2024"}
        },
        
        # Data Protection - CONTRADICTION 9: Different consent requirements
        {
            "type": "Law",
            "id": "data_protection_2021",
            "title": "Data Protection Law 2021",
            "content": "Federal Decree-Law No. 45 of 2021 regulates data protection and privacy in the UAE. It establishes rights for data subjects, obligations for data controllers, and enforcement mechanisms. The law applies to both public and private sector entities. Explicit consent is required for data processing.",
            "metadata": {"law_number": "45/2021", "category": "privacy", "effective": "2022", "gdpr_aligned": True, "consent": "explicit"}
        },
        
        {
            "type": "Law",
            "id": "data_protection_amendment_2024",
            "title": "Data Protection Law Amendment 2024",
            "content": "Amendment to data protection law introduces implied consent for certain types of data processing, particularly for business-to-business transactions and public interest activities. This creates a more flexible consent framework while maintaining privacy protections.",
            "metadata": {"law_number": "45/2021_amended", "category": "privacy", "consent": "implied_available", "b2b_exemption": True, "public_interest": True, "effective": "2024"}
        },
        
        # Environmental Law - CONTRADICTION 10: Different emission standards
        {
            "type": "Law",
            "id": "environmental_law_2020",
            "title": "Environmental Protection Law 2020",
            "content": "UAE environmental law regulates pollution control, waste management, and environmental impact assessments. It establishes standards for air and water quality, hazardous waste disposal, and environmental monitoring requirements. Vehicle emission standards are set at Euro 4 level.",
            "metadata": {"category": "environmental", "pollution_control": True, "waste_management": True, "emission_standard": "Euro 4", "year": "2020"}
        },
        
        {
            "type": "Law",
            "id": "environmental_law_2024",
            "title": "Environmental Protection Law 2024",
            "content": "Updated environmental regulations introduce stricter emission standards: Euro 6 for new vehicles and Euro 5 for existing vehicles. However, certain industrial zones maintain Euro 4 standards for economic development purposes, creating regulatory inconsistencies.",
            "metadata": {"category": "environmental", "emission_standard": "Euro 6_new", "existing_vehicles": "Euro 5", "industrial_zones": "Euro 4", "year": "2024"}
        }
    ]
    
    # Create relationships between nodes (including contradictory relationships)
    relationships = [
        # Legal System relationships
        ("uae_legal_system", "uae_constitution", "ESTABLISHES"),
        ("uae_legal_system", "commercial_companies_law", "INCLUDES"),
        ("uae_legal_system", "labor_law_2021", "INCLUDES"),
        ("uae_legal_system", "corporate_tax_2022", "INCLUDES"),
        ("uae_legal_system", "court_system_2020", "PROVIDES"),
        
        # Constitution relationships
        ("uae_constitution", "court_system_2020", "ESTABLISHES"),
        ("uae_constitution", "court_system_2024", "ESTABLISHES"),
        
        # Business Law relationships
        ("commercial_companies_law", "business_licensing", "REQUIRES"),
        ("commercial_companies_law", "corporate_tax_2022", "RELATES_TO"),
        ("commercial_companies_law", "vat_law", "RELATES_TO"),
        ("commercial_companies_law", "intellectual_property_2016", "PROTECTS"),
        
        # Labor Law contradictions
        ("labor_law_2021", "work_visa_requirements", "REQUIRES"),
        ("labor_law_1980", "work_visa_requirements", "REQUIRES"),
        ("labor_law_2021", "labor_law_1980", "CONTRADICTS"),  # Notice period contradiction
        
        # Corporate Tax contradictions
        ("corporate_tax_2022", "dubai_free_zones_2020", "AFFECTS"),
        ("corporate_tax_amendment_2024", "dubai_free_zones_2020", "AFFECTS"),
        ("corporate_tax_2022", "corporate_tax_amendment_2024", "CONTRADICTS"),  # Tax rate contradiction
        
        # VAT relationships
        ("vat_law", "business_licensing", "APPLIES_TO"),
        
        # Intellectual Property contradictions
        ("intellectual_property_2016", "commercial_companies_law", "PROTECTS"),
        ("intellectual_property_2023", "commercial_companies_law", "PROTECTS"),
        ("intellectual_property_2016", "intellectual_property_2023", "CONTRADICTS"),  # Protection period contradiction
        
        # Banking contradictions
        ("banking_regulations_2018", "aml_cft_2018", "ENFORCES"),
        ("banking_regulations_2023", "aml_cft_2023", "ENFORCES"),
        ("banking_regulations_2018", "banking_regulations_2023", "CONTRADICTS"),  # Capital requirement contradiction
        
        # Free Zone contradictions
        ("dubai_free_zones_2020", "court_system_2020", "HAS_SPECIAL"),
        ("dubai_free_zones_2024", "court_system_2024", "HAS_SPECIAL"),
        ("dubai_free_zones_2020", "dubai_free_zones_2024", "CONTRADICTS"),  # Ownership rule contradiction
        
        # Court System contradictions
        ("court_system_2020", "arbitration", "PROVIDES"),
        ("court_system_2024", "arbitration", "PROVIDES"),
        ("court_system_2020", "court_system_2024", "CONTRADICTS"),  # Jurisdiction contradiction
        
        # Real Estate contradictions
        ("real_estate_law_2020", "business_licensing", "REQUIRES"),
        ("real_estate_law_2024", "business_licensing", "REQUIRES"),
        ("real_estate_law_2020", "real_estate_law_2024", "CONTRADICTS"),  # Ownership restriction contradiction
        
        # Data Protection contradictions
        ("data_protection_2021", "commercial_companies_law", "APPLIES_TO"),
        ("data_protection_amendment_2024", "commercial_companies_law", "APPLIES_TO"),
        ("data_protection_2021", "data_protection_amendment_2024", "CONTRADICTS"),  # Consent requirement contradiction
        
        # Environmental contradictions
        ("environmental_law_2020", "business_licensing", "REQUIRES"),
        ("environmental_law_2024", "business_licensing", "REQUIRES"),
        ("environmental_law_2020", "environmental_law_2024", "CONTRADICTS"),  # Emission standard contradiction
        
        # AML contradictions
        ("aml_cft_2018", "commercial_companies_law", "APPLIES_TO"),
        ("aml_cft_2023", "commercial_companies_law", "APPLIES_TO"),
        ("aml_cft_2018", "aml_cft_2023", "CONTRADICTS"),  # Reporting threshold contradiction
        
        # Commercial transactions relationships
        ("commercial_transactions_law", "banking_regulations_2018", "GOVERNED_BY"),
        ("commercial_transactions_law", "court_system_2020", "ENFORCED_BY"),
        
        # Abu Dhabi free zones
        ("abu_dhabi_free_zones", "court_system_2020", "HAS_SPECIAL"),
        ("corporate_tax_2022", "abu_dhabi_free_zones", "AFFECTS"),
    ]
    
    # Load nodes
    nodes_created = 0
    for node_data in legal_data:
        try:
            # Create node
            create_node_query = """
            CREATE (n:LegalNode {
                id: $id,
                title: $title,
                content: $content,
                type: $type,
                metadata: $metadata,
                score: $score
            })
            """
            
            await neo4j_conn.run_cypher(create_node_query, {
                "id": node_data["id"],
                "title": node_data["title"],
                "content": node_data["content"],
                "type": node_data["type"],
                "metadata": json.dumps(node_data["metadata"]),
                "score": 1.0
            })
            
            nodes_created += 1
            
        except Exception as e:
            print(f"❌ Failed to create node {node_data['id']}: {e}")
    
    # Load relationships
    relationships_created = 0
    for source_id, target_id, relationship_type in relationships:
        try:
            # Create relationship
            create_rel_query = """
            MATCH (a:LegalNode {id: $source_id})
            MATCH (b:LegalNode {id: $target_id})
            CREATE (a)-[r:RELATES_TO {type: $rel_type}]->(b)
            """
            
            await neo4j_conn.run_cypher(create_rel_query, {
                "source_id": source_id,
                "target_id": target_id,
                "rel_type": relationship_type
            })
            
            relationships_created += 1
            
        except Exception as e:
            print(f"❌ Failed to create relationship {source_id} -> {target_id}: {e}")
    
    print(f"✅ Successfully loaded {nodes_created} legal nodes and {relationships_created} relationships")
    return nodes_created, relationships_created

async def verify_loaded_data(neo4j_conn):
    """Verify that data was loaded correctly."""
    print("🔍 Verifying loaded data...")
    
    try:
        # Count nodes
        count_nodes_query = "MATCH (n:LegalNode) RETURN count(n) as count"
        nodes_result = await neo4j_conn.run_cypher(count_nodes_query)
        node_count = nodes_result[0]["count"] if nodes_result else 0
        
        # Count relationships
        count_rels_query = "MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count"
        rels_result = await neo4j_conn.run_cypher(count_rels_query)
        rel_count = rels_result[0]["count"] if rels_result else 0
        
        # Count contradictions
        count_contradictions_query = "MATCH ()-[r:RELATES_TO {type: 'CONTRADICTS'}]->() RETURN count(r) as count"
        contradictions_result = await neo4j_conn.run_cypher(count_contradictions_query)
        contradictions_count = contradictions_result[0]["count"] if contradictions_result else 0
        
        # Get sample nodes
        sample_query = "MATCH (n:LegalNode) RETURN n.title, n.type LIMIT 5"
        sample_result = await neo4j_conn.run_cypher(sample_query)
        
        print(f"✅ Database contains {node_count} nodes and {rel_count} relationships")
        print(f"🔍 Found {contradictions_count} contradiction relationships")
        print("📋 Sample nodes:")
        for record in sample_result:
            print(f"   - {record['n.title']} ({record['n.type']})")
        
        return node_count, rel_count, contradictions_count
        
    except Exception as e:
        print(f"❌ Failed to verify data: {e}")
        return 0, 0, 0

async def main():
    """Main function to load contradictory data."""
    print("🚀 UAE Legal Knowledge Graph - Contradictory Data Loader")
    print("=" * 60)
    
    try:
        # Initialize Neo4j connection
        neo4j_conn = Neo4jConnection()
        
        print("✅ Neo4j connection established")
        
        # Clear existing data
        await clear_neo4j_database(neo4j_conn)
        
        # Load contradictory data
        nodes_created, relationships_created = await load_contradictory_uae_legal_data(neo4j_conn)
        
        # Verify loaded data
        node_count, rel_count, contradictions_count = await verify_loaded_data(neo4j_conn)
        
        print("\n🎉 Contradictory UAE legal data loaded successfully!")
        print("📊 The knowledge graph now contains comprehensive UAE legal information with realistic contradictions")
        print(f"🔍 AI Analysis tool will find {contradictions_count} contradiction relationships to analyze")
        print("💡 The system includes contradictions in:")
        print("   - Labor law notice periods (30 days vs 14/30 days)")
        print("   - Corporate tax rates (9% vs 0/5/9% progressive)")
        print("   - IP protection periods (20/10 years vs 25/15 years)")
        print("   - Banking capital requirements (12.5%/10% vs 15%/12%)")
        print("   - Free zone ownership rules (100% vs sector-specific)")
        print("   - Court jurisdiction (standard vs expanded DIFC)")
        print("   - Real estate ownership (leasehold vs freehold)")
        print("   - Data protection consent (explicit vs implied)")
        print("   - Environmental standards (Euro 4 vs Euro 6)")
        print("   - AML reporting thresholds (AED 50K vs AED 25K)")
        
    except Exception as e:
        print(f"❌ Failed to load contradictory data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(main())
