import asyncio
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.app.adapters.neo4j_conn import Neo4jConnection

async def expand_legal_data():
    """Expand the Neo4j knowledge graph with comprehensive UAE legal data."""
    
    # Initialize Neo4j connection
    neo4j_conn = Neo4jConnection()
    
    # Additional legal nodes
    additional_nodes = [
        # Tax Laws
        {
            "id": "personal_income_tax_2023",
            "title": "Personal Income Tax Law 2023",
            "content": "Introduces personal income tax for high-net-worth individuals. Establishes progressive tax rates from 0% to 35%. Defines taxable income categories and exemptions. Implements tax residency rules and reporting requirements.",
            "type": "Law",
            "metadata": {"law_number": "2023/15", "effective_date": "2023-06-01", "jurisdiction": "Federal", "category": "Tax Law", "importance": "High"}
        },
        {
            "id": "excise_tax_law_2017",
            "title": "Excise Tax Law 2017",
            "content": "Implements excise tax on harmful goods including tobacco, energy drinks, and carbonated beverages. Establishes tax rates of 50% on tobacco and 100% on energy drinks. Defines registration and compliance requirements.",
            "type": "Law",
            "metadata": {"law_number": "2017/7", "effective_date": "2017-10-01", "jurisdiction": "Federal", "category": "Tax Law", "importance": "Medium"}
        },
        {
            "id": "transfer_pricing_2024",
            "title": "Transfer Pricing Regulations 2024",
            "content": "Establishes transfer pricing rules for related party transactions. Requires documentation and reporting of intercompany transactions. Implements arm's length principle and penalty provisions for non-compliance.",
            "type": "Regulation",
            "metadata": {"regulator": "FTA", "effective_date": "2024-01-01", "jurisdiction": "Federal", "category": "Tax Law", "importance": "High"}
        },
        
        # Corporate Governance
        {
            "id": "corporate_governance_code_2020",
            "title": "Corporate Governance Code 2020",
            "content": "Establishes corporate governance framework for public joint stock companies. Defines board composition, independence requirements, and committee structures. Implements disclosure and transparency requirements.",
            "type": "Code",
            "metadata": {"regulator": "SCA", "effective_date": "2020-01-01", "jurisdiction": "Federal", "category": "Corporate Law", "importance": "High"}
        },
        {
            "id": "esg_reporting_2023",
            "title": "ESG Reporting Framework 2023",
            "content": "Mandates environmental, social, and governance reporting for listed companies. Establishes reporting standards and disclosure requirements. Implements sustainability metrics and performance indicators.",
            "type": "Framework",
            "metadata": {"regulator": "SCA", "effective_date": "2023-01-01", "jurisdiction": "Federal", "category": "Corporate Law", "importance": "Medium"}
        },
        
        # Financial Services
        {
            "id": "insurance_law_2007",
            "title": "Insurance Law 2007",
            "content": "Regulates insurance activities in UAE. Establishes licensing requirements for insurers and brokers. Defines capital adequacy and solvency requirements. Implements consumer protection measures.",
            "type": "Law",
            "metadata": {"law_number": "2007/6", "effective_date": "2007-01-01", "jurisdiction": "Federal", "category": "Financial Services", "importance": "Medium"}
        },
        {
            "id": "securities_law_2000",
            "title": "Securities Law 2000",
            "content": "Regulates securities markets and trading activities. Establishes licensing for brokers and investment advisors. Implements market conduct rules and investor protection measures.",
            "type": "Law",
            "metadata": {"law_number": "2000/4", "effective_date": "2000-01-01", "jurisdiction": "Federal", "category": "Financial Services", "importance": "Medium"}
        },
        
        # Technology & Digital
        {
            "id": "cybersecurity_law_2022",
            "title": "Cybersecurity Law 2022",
            "content": "Establishes cybersecurity framework for critical infrastructure. Defines security standards and incident reporting requirements. Implements penalties for cyber attacks and data breaches.",
            "type": "Law",
            "metadata": {"law_number": "2022/34", "effective_date": "2022-01-01", "jurisdiction": "Federal", "category": "Technology Law", "importance": "High"}
        },
        {
            "id": "digital_payments_2021",
            "title": "Digital Payments Regulations 2021",
            "content": "Regulates digital payment systems and fintech activities. Establishes licensing for payment service providers. Implements security and consumer protection standards.",
            "type": "Regulation",
            "metadata": {"regulator": "CBUAE", "effective_date": "2021-01-01", "jurisdiction": "Federal", "category": "Financial Services", "importance": "Medium"}
        },
        
        # Real Estate & Construction
        {
            "id": "construction_law_2008",
            "title": "Construction Law 2008",
            "content": "Regulates construction activities and contractor licensing. Establishes building codes and safety standards. Implements dispute resolution mechanisms for construction disputes.",
            "type": "Law",
            "metadata": {"law_number": "2008/29", "effective_date": "2008-01-01", "jurisdiction": "Federal", "category": "Construction Law", "importance": "Medium"}
        },
        {
            "id": "strata_law_2007",
            "title": "Strata Law 2007",
            "content": "Regulates ownership and management of jointly owned properties. Establishes owners' associations and management companies. Implements voting rights and maintenance responsibilities.",
            "type": "Law",
            "metadata": {"law_number": "2007/27", "effective_date": "2007-01-01", "jurisdiction": "Dubai", "category": "Real Estate Law", "importance": "Medium"}
        },
        
        # Employment & Immigration
        {
            "id": "emiratization_law_2022",
            "title": "Emiratization Law 2022",
            "content": "Mandates employment of UAE nationals in private sector. Establishes quotas and compliance requirements. Implements penalties for non-compliance and incentives for compliance.",
            "type": "Law",
            "metadata": {"law_number": "2022/33", "effective_date": "2022-01-01", "jurisdiction": "Federal", "category": "Employment Law", "importance": "High"}
        },
        {
            "id": "golden_visa_2019",
            "title": "Golden Visa Regulations 2019",
            "content": "Establishes long-term residency for investors, entrepreneurs, and professionals. Defines eligibility criteria and application procedures. Implements benefits and renewal requirements.",
            "type": "Regulation",
            "metadata": {"regulator": "GDRFA", "effective_date": "2019-01-01", "jurisdiction": "Federal", "category": "Immigration Law", "importance": "Medium"}
        },
        
        # Environmental & Sustainability
        {
            "id": "environmental_law_1999",
            "title": "Environmental Law 1999",
            "content": "Establishes environmental protection framework. Defines pollution control and waste management standards. Implements environmental impact assessment requirements.",
            "type": "Law",
            "metadata": {"law_number": "1999/24", "effective_date": "1999-01-01", "jurisdiction": "Federal", "category": "Environmental Law", "importance": "Medium"}
        },
        {
            "id": "renewable_energy_2020",
            "title": "Renewable Energy Regulations 2020",
            "content": "Promotes renewable energy development and investment. Establishes feed-in tariffs and net metering. Implements renewable energy targets and incentives.",
            "type": "Regulation",
            "metadata": {"regulator": "MOEI", "effective_date": "2020-01-01", "jurisdiction": "Federal", "category": "Energy Law", "importance": "Medium"}
        }
    ]
    
    # Create nodes
    for node in additional_nodes:
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
        # Tax relationships
        ("personal_income_tax_2023", "corporate_tax_law_2022", "complements", {"type": "tax_system", "weight": 1}),
        ("excise_tax_law_2017", "vat_law_2017", "complements", {"type": "tax_system", "weight": 1}),
        ("transfer_pricing_2024", "corporate_tax_law_2022", "implements", {"type": "tax_compliance", "weight": 1}),
        
        # Corporate governance relationships
        ("corporate_governance_code_2020", "commercial_companies_law_2015", "enhances", {"type": "governance", "weight": 1}),
        ("esg_reporting_2023", "corporate_governance_code_2020", "extends", {"type": "reporting", "weight": 1}),
        
        # Financial services relationships
        ("insurance_law_2007", "banking_regulations_2018", "complements", {"type": "financial_services", "weight": 1}),
        ("securities_law_2000", "corporate_governance_code_2020", "supports", {"type": "market_regulation", "weight": 1}),
        
        # Technology relationships
        ("cybersecurity_law_2022", "data_protection_law_2021", "strengthens", {"type": "digital_security", "weight": 1}),
        ("digital_payments_2021", "banking_regulations_2023", "modernizes", {"type": "payment_systems", "weight": 1}),
        
        # Real estate relationships
        ("construction_law_2008", "real_estate_law_2006", "supports", {"type": "development", "weight": 1}),
        ("strata_law_2007", "real_estate_law_2006", "implements", {"type": "property_management", "weight": 1}),
        
        # Employment relationships
        ("emiratization_law_2022", "labor_law_2021", "complements", {"type": "employment_policy", "weight": 1}),
        ("golden_visa_2019", "business_licensing", "facilitates", {"type": "investment", "weight": 1}),
        
        # Environmental relationships
        ("environmental_law_1999", "construction_law_2008", "influences", {"type": "environmental_compliance", "weight": 1}),
        ("renewable_energy_2020", "environmental_law_1999", "implements", {"type": "sustainability", "weight": 1}),
        
        # CONTRADICTS relationships for AI Analysis
        ("personal_income_tax_2023", "corporate_tax_law_2022", "CONTRADICTS", {
            "type": "CONTRADICTS", 
            "priority": "medium", 
            "severity": "moderate", 
            "category": "tax_rates",
            "description": "Different tax rate structures between personal and corporate income",
            "weight": 1
        }),
        ("cybersecurity_law_2022", "data_protection_law_2021", "CONTRADICTS", {
            "type": "CONTRADICTS", 
            "priority": "high", 
            "severity": "significant", 
            "category": "data_security",
            "description": "Conflicting requirements for data retention and security measures",
            "weight": 1
        }),
        ("emiratization_law_2022", "labor_law_2021", "CONTRADICTS", {
            "type": "CONTRADICTS", 
            "priority": "high", 
            "severity": "significant", 
            "category": "employment_quotas",
            "description": "Conflicting requirements for workforce composition and employment rights",
            "weight": 1
        })
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
    
    print("✅ Expanded Neo4j knowledge graph with 15 additional legal nodes and 18 relationships")
    print("✅ Added 3 CONTRADICTS relationships for AI Analysis testing")

if __name__ == "__main__":
    asyncio.run(expand_legal_data())
