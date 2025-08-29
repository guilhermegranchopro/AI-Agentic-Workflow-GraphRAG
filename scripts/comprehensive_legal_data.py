#!/usr/bin/env python3
"""
Comprehensive UAE Legal Data Population Script
Populates Neo4j knowledge graph with extensive UAE legal information.
"""

import sys
import json
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.app.adapters.neo4j_conn import Neo4jConnection
from loguru import logger

async def create_comprehensive_legal_data():
    """Create comprehensive UAE legal data for Neo4j knowledge graph."""
    
    # Initialize Neo4j connection
    neo4j_conn = Neo4jConnection()
    
    # Clear existing data
    logger.info("Clearing existing legal data...")
    await neo4j_conn.run_cypher("MATCH (n:LegalNode) DETACH DELETE n")
    
    # Comprehensive legal data
    legal_nodes = [
        # UAE CONSTITUTION AND FOUNDATION
        {
            "id": "uae_constitution_1971",
            "title": "UAE Constitution",
            "content": "The UAE Constitution establishes the federal structure, fundamental rights, and governance framework. It defines the relationship between federal and local authorities, establishes the Federal Supreme Council, and guarantees fundamental freedoms including equality, education, and healthcare.",
            "type": "Constitution",
            "metadata": {
                "law_number": "1/1971",
                "effective_date": "1971-12-02",
                "jurisdiction": "Federal",
                "category": "Constitutional Law",
                "importance": "Foundational"
            }
        },
        
        # CORPORATE LAW
        {
            "id": "commercial_companies_law_2015",
            "title": "Federal Law No. 2 of 2015 on Commercial Companies",
            "content": "Governs the formation, management, and dissolution of commercial companies in the UAE. Establishes seven types of companies: general partnership, limited partnership, joint venture, public joint stock, private joint stock, limited liability, and partnership limited by shares. Defines corporate governance requirements, shareholder rights, and director responsibilities.",
            "type": "Law",
            "metadata": {
                "law_number": "2/2015",
                "effective_date": "2015-07-01",
                "jurisdiction": "Federal",
                "category": "Corporate Law",
                "importance": "High"
            }
        },
        
        {
            "id": "commercial_companies_amendment_2020",
            "title": "Federal Decree-Law No. 26 of 2020 Amending Commercial Companies Law",
            "content": "Amends the Commercial Companies Law to allow 100% foreign ownership in mainland companies, removes the requirement for UAE national majority ownership, and introduces new corporate governance standards. Establishes new requirements for board composition and shareholder rights.",
            "type": "Law",
            "metadata": {
                "law_number": "26/2020",
                "effective_date": "2020-06-01",
                "jurisdiction": "Federal",
                "category": "Corporate Law",
                "importance": "High"
            }
        },
        
        # CORPORATE TAX
        {
            "id": "corporate_tax_law_2022",
            "title": "Federal Decree-Law No. 47 of 2022 on Taxation of Corporations and Businesses",
            "content": "Introduces corporate tax at 9% for taxable income above AED 375,000, effective from June 2023. Applies to UAE companies and foreign companies with permanent establishments. Free zone companies may be exempt under certain conditions. Establishes transfer pricing rules and anti-avoidance measures.",
            "type": "Law",
            "metadata": {
                "law_number": "47/2022",
                "effective_date": "2023-06-01",
                "jurisdiction": "Federal",
                "category": "Tax Law",
                "importance": "High"
            }
        },
        
        {
            "id": "corporate_tax_amendment_2024",
            "title": "Federal Decree-Law No. 60 of 2024 Amending Corporate Tax Law",
            "content": "Amends corporate tax rates to progressive structure: 0% for income up to AED 375,000, 5% for income between AED 375,000 and AED 1,000,000, and 9% for income above AED 1,000,000. Introduces new exemptions for small businesses and enhanced transfer pricing documentation requirements.",
            "type": "Law",
            "metadata": {
                "law_number": "60/2024",
                "effective_date": "2024-01-01",
                "jurisdiction": "Federal",
                "category": "Tax Law",
                "importance": "High"
            }
        },
        
        # VAT LAW
        {
            "id": "vat_law_2017",
            "title": "Federal Decree-Law No. 8 of 2017 on Value Added Tax",
            "content": "Establishes 5% VAT on most goods and services. Exemptions include residential properties, local passenger transport, and certain financial services. Zero-rated supplies include exports, international transport, and certain healthcare and education services. Requires registration for businesses with annual turnover above AED 375,000.",
            "type": "Law",
            "metadata": {
                "law_number": "8/2017",
                "effective_date": "2018-01-01",
                "jurisdiction": "Federal",
                "category": "Tax Law",
                "importance": "High"
            }
        },
        
        # CIVIL CODE
        {
            "id": "civil_code_1985",
            "title": "Federal Law No. 5 of 1985 on Civil Transactions",
            "content": "Comprehensive civil code governing contracts, property rights, torts, and personal status matters. Establishes principles of good faith, freedom of contract, and compensation for damages. Covers sale, lease, agency, partnership, and other civil transactions. Influenced by Islamic law and modern civil law principles.",
            "type": "Law",
            "metadata": {
                "law_number": "5/1985",
                "effective_date": "1985-01-01",
                "jurisdiction": "Federal",
                "category": "Civil Law",
                "importance": "High"
            }
        },
        
        # COMMERCIAL CODE
        {
            "id": "commercial_code_1993",
            "title": "Federal Law No. 18 of 1993 on Commercial Transactions",
            "content": "Governs commercial transactions, banking operations, and negotiable instruments. Establishes rules for commercial contracts, agency, brokerage, and commercial pledges. Defines commercial activities and establishes commercial courts. Covers letters of credit, bills of exchange, and commercial arbitration.",
            "type": "Law",
            "metadata": {
                "law_number": "18/1993",
                "effective_date": "1993-01-01",
                "jurisdiction": "Federal",
                "category": "Commercial Law",
                "importance": "High"
            }
        },
        
        # LABOR LAW
        {
            "id": "labor_law_2021",
            "title": "Federal Decree-Law No. 33 of 2021 on Regulation of Labor Relations",
            "content": "Modernizes UAE labor law with enhanced worker protections, flexible work arrangements, and improved dispute resolution. Establishes minimum wage requirements, maximum working hours, and annual leave entitlements. Introduces new categories of work permits and enhanced termination protections.",
            "type": "Law",
            "metadata": {
                "law_number": "33/2021",
                "effective_date": "2022-02-02",
                "jurisdiction": "Federal",
                "category": "Labor Law",
                "importance": "High"
            }
        },
        
        # REAL ESTATE LAW
        {
            "id": "real_estate_law_2006",
            "title": "Federal Law No. 8 of 2006 on Real Estate Registration",
            "content": "Establishes real estate registration system and regulates property transactions. Defines ownership rights, mortgage procedures, and property development regulations. Establishes real estate courts and dispute resolution mechanisms. Regulates off-plan sales and escrow accounts.",
            "type": "Law",
            "metadata": {
                "law_number": "8/2006",
                "effective_date": "2006-01-01",
                "jurisdiction": "Federal",
                "category": "Real Estate Law",
                "importance": "Medium"
            }
        },
        
        {
            "id": "real_estate_amendment_2023",
            "title": "Federal Decree-Law No. 35 of 2023 Amending Real Estate Law",
            "content": "Introduces freehold ownership for foreigners in specific areas, extends beyond the previous 99-year leasehold system. Establishes new property registration requirements and enhanced developer obligations. Introduces real estate investment trusts (REITs) and crowdfunding regulations.",
            "type": "Law",
            "metadata": {
                "law_number": "35/2023",
                "effective_date": "2023-06-01",
                "jurisdiction": "Federal",
                "category": "Real Estate Law",
                "importance": "High"
            }
        },
        
        # INTELLECTUAL PROPERTY
        {
            "id": "intellectual_property_law_2006",
            "title": "Federal Law No. 31 of 2006 on Industrial Property Rights",
            "content": "Protects patents, industrial designs, and trade secrets. Establishes 20-year patent protection, 10-year design protection, and trade secret confidentiality. Defines patentability requirements and infringement remedies. Establishes patent office and registration procedures.",
            "type": "Law",
            "metadata": {
                "law_number": "31/2006",
                "effective_date": "2006-01-01",
                "jurisdiction": "Federal",
                "category": "Intellectual Property",
                "importance": "Medium"
            }
        },
        
        {
            "id": "copyright_law_2002",
            "title": "Federal Law No. 7 of 2002 on Copyrights and Related Rights",
            "content": "Protects literary, artistic, and scientific works. Establishes 50-year copyright protection for most works, 25 years for applied art. Covers software, databases, and digital content. Defines fair use exceptions and infringement penalties. Establishes copyright office and registration system.",
            "type": "Law",
            "metadata": {
                "law_number": "7/2002",
                "effective_date": "2002-01-01",
                "jurisdiction": "Federal",
                "category": "Intellectual Property",
                "importance": "Medium"
            }
        },
        
        {
            "id": "trademark_law_1992",
            "title": "Federal Law No. 37 of 1992 on Trademarks",
            "content": "Protects trademarks, service marks, and trade names. Establishes 10-year renewable protection. Defines distinctiveness requirements and opposition procedures. Covers well-known marks and international registration. Establishes trademark office and enforcement mechanisms.",
            "type": "Law",
            "metadata": {
                "law_number": "37/1992",
                "effective_date": "1992-01-01",
                "jurisdiction": "Federal",
                "category": "Intellectual Property",
                "importance": "Medium"
            }
        },
        
        # BANKING AND FINANCIAL REGULATIONS
        {
            "id": "banking_regulations_2018",
            "title": "Central Bank Regulations 2018",
            "content": "Establishes banking supervision framework, capital adequacy requirements, and risk management standards. Defines licensing requirements for banks and financial institutions. Establishes consumer protection measures and dispute resolution procedures. Regulates digital banking and fintech activities.",
            "type": "Regulation",
            "metadata": {
                "regulator": "Central Bank of UAE",
                "effective_date": "2018-01-01",
                "jurisdiction": "Federal",
                "category": "Banking Law",
                "importance": "High"
            }
        },
        
        {
            "id": "banking_regulations_2023",
            "title": "Central Bank Regulations 2023",
            "content": "Updates banking regulations with enhanced cybersecurity requirements, digital transformation standards, and sustainable finance guidelines. Introduces new capital buffers and liquidity requirements. Establishes framework for open banking and digital assets. Enhances anti-money laundering compliance.",
            "type": "Regulation",
            "metadata": {
                "regulator": "Central Bank of UAE",
                "effective_date": "2023-01-01",
                "jurisdiction": "Federal",
                "category": "Banking Law",
                "importance": "High"
            }
        },
        
        # ANTI-MONEY LAUNDERING
        {
            "id": "aml_cft_law_2018",
            "title": "Federal Decree-Law No. 20 of 2018 on Anti-Money Laundering and Combating the Financing of Terrorism",
            "content": "Establishes comprehensive AML/CFT framework. Requires customer due diligence, suspicious transaction reporting, and record keeping. Defines designated non-financial businesses and professions. Establishes Financial Intelligence Unit and enforcement mechanisms.",
            "type": "Law",
            "metadata": {
                "law_number": "20/2018",
                "effective_date": "2018-10-30",
                "jurisdiction": "Federal",
                "category": "Financial Crime",
                "importance": "High"
            }
        },
        
        {
            "id": "aml_cft_amendment_2023",
            "title": "Federal Decree-Law No. 26 of 2023 Amending AML/CFT Law",
            "content": "Strengthens AML/CFT framework with enhanced due diligence requirements, virtual asset regulations, and beneficial ownership transparency. Introduces new reporting obligations and enhanced penalties. Establishes framework for international cooperation and information sharing.",
            "type": "Law",
            "metadata": {
                "law_number": "26/2023",
                "effective_date": "2023-01-01",
                "jurisdiction": "Federal",
                "category": "Financial Crime",
                "importance": "High"
            }
        },
        
        # DATA PROTECTION
        {
            "id": "data_protection_law_2021",
            "title": "Federal Decree-Law No. 45 of 2021 on the Protection of Personal Data",
            "content": "Establishes comprehensive data protection framework. Defines personal data, processing principles, and individual rights. Requires data protection impact assessments and breach notification. Establishes Data Office and enforcement mechanisms. Aligns with international data protection standards.",
            "type": "Law",
            "metadata": {
                "law_number": "45/2021",
                "effective_date": "2022-01-02",
                "jurisdiction": "Federal",
                "category": "Data Protection",
                "importance": "High"
            }
        },
        
        {
            "id": "data_protection_amendment_2024",
            "title": "Federal Decree-Law No. 15 of 2024 Amending Data Protection Law",
            "content": "Enhances data protection with new requirements for AI systems, cross-border data transfers, and children's data protection. Introduces data portability rights and enhanced consent mechanisms. Establishes framework for data protection certification and codes of conduct.",
            "type": "Law",
            "metadata": {
                "law_number": "15/2024",
                "effective_date": "2024-03-01",
                "jurisdiction": "Federal",
                "category": "Data Protection",
                "importance": "High"
            }
        },
        
        # FREE ZONE REGULATIONS
        {
            "id": "dubai_free_zones_2020",
            "title": "Dubai Free Zone Regulations 2020",
            "content": "Establishes regulatory framework for Dubai free zones including DMCC, DIFC, and Dubai Internet City. Defines licensing requirements, tax benefits, and operational restrictions. Establishes dispute resolution mechanisms and regulatory oversight. Covers digital economy and fintech activities.",
            "type": "Regulation",
            "metadata": {
                "regulator": "Dubai Free Zone Authority",
                "effective_date": "2020-01-01",
                "jurisdiction": "Dubai",
                "category": "Free Zone Law",
                "importance": "Medium"
            }
        },
        
        {
            "id": "dubai_free_zones_2024",
            "title": "Dubai Free Zone Regulations 2024",
            "content": "Updates free zone regulations with enhanced digital transformation requirements, sustainability standards, and innovation incentives. Introduces new categories for AI, blockchain, and green technology companies. Establishes framework for virtual free zone licenses and remote work regulations.",
            "type": "Regulation",
            "metadata": {
                "regulator": "Dubai Free Zone Authority",
                "effective_date": "2024-01-01",
                "jurisdiction": "Dubai",
                "category": "Free Zone Law",
                "importance": "Medium"
            }
        },
        
        {
            "id": "abu_dhabi_free_zones",
            "title": "Abu Dhabi Free Zone Regulations",
            "content": "Establishes regulatory framework for Abu Dhabi free zones including ADGM, Masdar City, and twofour54. Defines licensing requirements, tax benefits, and operational restrictions. Establishes dispute resolution mechanisms and regulatory oversight. Covers financial services and media activities.",
            "type": "Regulation",
            "metadata": {
                "regulator": "Abu Dhabi Free Zone Authority",
                "effective_date": "2018-01-01",
                "jurisdiction": "Abu Dhabi",
                "category": "Free Zone Law",
                "importance": "Medium"
            }
        },
        
        # COURT SYSTEM
        {
            "id": "court_system_2020",
            "title": "UAE Court System 2020",
            "content": "Establishes three-tier court system: Courts of First Instance, Courts of Appeal, and Federal Supreme Court. Defines jurisdiction for civil, commercial, criminal, and administrative cases. Establishes specialized courts for labor, real estate, and family matters. Defines appeal procedures and enforcement mechanisms.",
            "type": "System",
            "metadata": {
                "effective_date": "2020-01-01",
                "jurisdiction": "Federal",
                "category": "Judicial System",
                "importance": "High"
            }
        },
        
        {
            "id": "court_system_2024",
            "title": "UAE Court System 2024",
            "content": "Updates court system with enhanced digital transformation, specialized commercial courts, and alternative dispute resolution mechanisms. Introduces online dispute resolution and electronic filing systems. Establishes framework for international commercial courts and arbitration centers.",
            "type": "System",
            "metadata": {
                "effective_date": "2024-01-01",
                "jurisdiction": "Federal",
                "category": "Judicial System",
                "importance": "High"
            }
        },
        
        # BUSINESS LICENSING
        {
            "id": "business_licensing",
            "title": "Business Licensing Regulations",
            "content": "Establishes framework for business licensing across UAE. Defines license categories, application procedures, and renewal requirements. Establishes requirements for trade names, office premises, and local sponsorship. Covers mainland, free zone, and offshore licensing options.",
            "type": "Regulation",
            "metadata": {
                "regulator": "Various Authorities",
                "effective_date": "2015-01-01",
                "jurisdiction": "Federal/Local",
                "category": "Business Law",
                "importance": "Medium"
            }
        },
        
        # UAE LEGAL SYSTEM OVERVIEW
        {
            "id": "uae_legal_system",
            "title": "UAE Legal System Overview",
            "content": "The UAE legal system combines civil law principles with Islamic law (Sharia) influences. The federal structure allows for both federal and local legislation. The judiciary is independent with specialized courts for different matters. The system emphasizes commercial law, corporate governance, and international business standards.",
            "type": "System",
            "metadata": {
                "jurisdiction": "Federal",
                "category": "Legal System",
                "importance": "High"
            }
        }
    ]
    
    # Create nodes
    logger.info("Creating legal nodes...")
    for node in legal_nodes:
        cypher_query = """
        CREATE (n:LegalNode {
            id: $id,
            title: $title,
            content: $content,
            type: $type,
            metadata: $metadata
        })
        """
        await neo4j_conn.run_cypher(cypher_query, {
            "id": node["id"],
            "title": node["title"],
            "content": node["content"],
            "type": node["type"],
            "metadata": json.dumps(node["metadata"])
        })
    
    # Create relationships
    relationships = [
        # Constitutional relationships
        ("uae_constitution_1971", "uae_legal_system", "ESTABLISHES", {"type": "foundational"}),
        ("uae_constitution_1971", "court_system_2020", "ESTABLISHES", {"type": "judicial"}),
        ("uae_constitution_1971", "court_system_2024", "ESTABLISHES", {"type": "judicial"}),
        
        # Corporate law relationships
        ("commercial_companies_law_2015", "commercial_companies_amendment_2020", "AMENDED_BY", {"type": "legislative"}),
        ("commercial_companies_law_2015", "business_licensing", "GOVERNED_BY", {"type": "regulatory"}),
        ("commercial_companies_amendment_2020", "business_licensing", "IMPACTS", {"type": "regulatory"}),
        
        # Tax relationships
        ("corporate_tax_law_2022", "corporate_tax_amendment_2024", "AMENDED_BY", {"type": "legislative"}),
        ("corporate_tax_law_2022", "commercial_companies_law_2015", "APPLIES_TO", {"type": "regulatory"}),
        ("vat_law_2017", "business_licensing", "REQUIRES", {"type": "compliance"}),
        
        # Civil and commercial relationships
        ("civil_code_1985", "commercial_code_1993", "SUPPLEMENTS", {"type": "legal"}),
        ("civil_code_1985", "real_estate_law_2006", "GOVERNED_BY", {"type": "legal"}),
        ("commercial_code_1993", "banking_regulations_2018", "REGULATED_BY", {"type": "regulatory"}),
        
        # Labor relationships
        ("labor_law_2021", "commercial_companies_law_2015", "APPLIES_TO", {"type": "regulatory"}),
        ("labor_law_2021", "business_licensing", "REQUIRES", {"type": "compliance"}),
        
        # Real estate relationships
        ("real_estate_law_2006", "real_estate_amendment_2023", "AMENDED_BY", {"type": "legislative"}),
        ("real_estate_law_2006", "civil_code_1985", "BASED_ON", {"type": "legal"}),
        
        # Intellectual property relationships
        ("intellectual_property_law_2006", "copyright_law_2002", "COMPLEMENTS", {"type": "legal"}),
        ("trademark_law_1992", "intellectual_property_law_2006", "COMPLEMENTS", {"type": "legal"}),
        ("intellectual_property_law_2006", "commercial_companies_law_2015", "PROTECTS", {"type": "legal"}),
        
        # Banking relationships
        ("banking_regulations_2018", "banking_regulations_2023", "UPDATED_BY", {"type": "regulatory"}),
        ("banking_regulations_2023", "aml_cft_law_2018", "ENFORCES", {"type": "compliance"}),
        ("aml_cft_law_2018", "aml_cft_amendment_2023", "AMENDED_BY", {"type": "legislative"}),
        
        # Data protection relationships
        ("data_protection_law_2021", "data_protection_amendment_2024", "AMENDED_BY", {"type": "legislative"}),
        ("data_protection_law_2021", "commercial_companies_law_2015", "APPLIES_TO", {"type": "regulatory"}),
        ("data_protection_law_2021", "banking_regulations_2023", "REQUIRED_BY", {"type": "compliance"}),
        
        # Free zone relationships
        ("dubai_free_zones_2020", "dubai_free_zones_2024", "UPDATED_BY", {"type": "regulatory"}),
        ("dubai_free_zones_2020", "business_licensing", "PROVIDES", {"type": "regulatory"}),
        ("abu_dhabi_free_zones", "business_licensing", "PROVIDES", {"type": "regulatory"}),
        
        # Court system relationships
        ("court_system_2020", "court_system_2024", "UPDATED_BY", {"type": "system"}),
        ("court_system_2020", "commercial_code_1993", "ENFORCES", {"type": "judicial"}),
        ("court_system_2020", "labor_law_2021", "ENFORCES", {"type": "judicial"}),
        
        # Contradictions (for AI Analysis testing)
        ("corporate_tax_law_2022", "corporate_tax_amendment_2024", "CONTRADICTS", {
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "significant",
            "category": "tax_rates",
            "description": "Tax rates changed from flat 9% to progressive structure"
        }),
        
        ("banking_regulations_2018", "banking_regulations_2023", "CONTRADICTS", {
            "type": "CONTRADICTS",
            "priority": "medium",
            "severity": "moderate",
            "category": "capital_requirements",
            "description": "Capital adequacy requirements increased"
        }),
        
        ("dubai_free_zones_2020", "dubai_free_zones_2024", "CONTRADICTS", {
            "type": "CONTRADICTS",
            "priority": "low",
            "severity": "minor",
            "category": "digital_requirements",
            "description": "Digital transformation requirements enhanced"
        }),
        
        ("real_estate_law_2006", "real_estate_amendment_2023", "CONTRADICTS", {
            "type": "CONTRADICTS",
            "priority": "high",
            "severity": "significant",
            "category": "ownership_rights",
            "description": "Foreign ownership rights expanded from leasehold to freehold"
        }),
        
        ("data_protection_law_2021", "data_protection_amendment_2024", "CONTRADICTS", {
            "type": "CONTRADICTS",
            "priority": "medium",
            "severity": "moderate",
            "category": "ai_regulations",
            "description": "New AI-specific data protection requirements added"
        }),
        
        ("court_system_2020", "court_system_2024", "CONTRADICTS", {
            "type": "CONTRADICTS",
            "priority": "low",
            "severity": "minor",
            "category": "digital_courts",
            "description": "Enhanced digital court procedures introduced"
        })
    ]
    
    # Create relationships
    logger.info("Creating relationships...")
    for rel in relationships:
        source, target, rel_type, properties = rel
        cypher_query = """
        MATCH (a:LegalNode {id: $source})
        MATCH (b:LegalNode {id: $target})
        CREATE (a)-[r:RELATES_TO {
            type: $rel_type,
            priority: $priority,
            severity: $severity,
            category: $category,
            description: $description
        }]->(b)
        """
        await neo4j_conn.run_cypher(cypher_query, {
            "source": source,
            "target": target,
            "rel_type": properties.get("type", rel_type),
            "priority": properties.get("priority", "medium"),
            "severity": properties.get("severity", "moderate"),
            "category": properties.get("category", "general"),
            "description": properties.get("description", f"{rel_type} relationship")
        })
    
    # Verify data
    logger.info("Verifying data...")
    node_count_result = await neo4j_conn.run_cypher("MATCH (n:LegalNode) RETURN count(n) as count")
    node_count = node_count_result[0]["count"]
    rel_count_result = await neo4j_conn.run_cypher("MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count")
    rel_count = rel_count_result[0]["count"]
    
    logger.info(f"✅ Successfully created {node_count} legal nodes and {rel_count} relationships")
    
    # Test queries
    logger.info("Testing GraphRAG queries...")
    
    # Test corporate tax query
    test_query = """
    MATCH (n:LegalNode)
    WHERE toLower(n.content) CONTAINS 'corporate tax'
    RETURN n.title, n.type, n.metadata
    LIMIT 5
    """
    results = await neo4j_conn.run_cypher(test_query)
    logger.info(f"Found {len(results)} corporate tax related nodes")
    
    # Test contradictions query
    contradictions_query = """
    MATCH (a:LegalNode)-[r:RELATES_TO]->(b:LegalNode)
    WHERE r.type = 'CONTRADICTS'
    RETURN a.title, b.title, r.priority, r.severity, r.category
    """
    contradictions = await neo4j_conn.run_cypher(contradictions_query)
    logger.info(f"Found {len(contradictions)} contradiction relationships")
    
    logger.info("🎉 Comprehensive UAE legal data population completed successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(create_comprehensive_legal_data())
    except Exception as e:
        logger.error(f"Error populating legal data: {e}")
        sys.exit(1)
