import type { NextApiRequest, NextApiResponse } from 'next';

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8012';

interface DatabaseStats {
  total_documents: number;
  total_entities: number;
  total_relationships: number;
  communities: number;
  last_updated: string;
}

// Import the same data generation function used in the Graph API
function generateComprehensiveUAEKnowledgeGraph() {
  // This is the same function from the Graph API that generates our comprehensive knowledge graph
  const nodes = [
    // Constitutional & Legal Framework
    { id: 'constitution', label: 'UAE Constitution', type: 'Constitutional' },
    { id: 'federal_law_1', label: 'Federal Law No. 1', type: 'Law' },
    { id: 'federal_law_2', label: 'Federal Law No. 2', type: 'Law' },
    { id: 'federal_law_3', label: 'Federal Law No. 3', type: 'Law' },
    { id: 'federal_law_4', label: 'Federal Law No. 4', type: 'Law' },
    { id: 'federal_law_5', label: 'Federal Law No. 5', type: 'Law' },
    { id: 'federal_law_6', label: 'Federal Law No. 6', type: 'Law' },
    { id: 'federal_law_7', label: 'Federal Law No. 7', type: 'Law' },
    { id: 'federal_law_8', label: 'Federal Law No. 8', type: 'Law' },
    { id: 'federal_law_9', label: 'Federal Law No. 9', type: 'Law' },
    { id: 'federal_law_10', label: 'Federal Law No. 10', type: 'Law' },
    { id: 'regulation_1', label: 'Cabinet Resolution No. 1', type: 'Regulation' },
    { id: 'regulation_2', label: 'Cabinet Resolution No. 2', type: 'Regulation' },
    { id: 'regulation_3', label: 'Cabinet Resolution No. 3', type: 'Regulation' },
    { id: 'regulation_4', label: 'Cabinet Resolution No. 4', type: 'Regulation' },
    
    // Entities & Organizations
    { id: 'llc', label: 'Limited Liability Company', type: 'EntityType' },
    { id: 'pjsc', label: 'Public Joint Stock Company', type: 'EntityType' },
    { id: 'branch', label: 'Branch Office', type: 'EntityType' },
    { id: 'representative', label: 'Representative Office', type: 'EntityType' },
    { id: 'partnership', label: 'Partnership', type: 'EntityType' },
    { id: 'sole_proprietorship', label: 'Sole Proprietorship', type: 'EntityType' },
    { id: 'free_zone_company', label: 'Free Zone Company', type: 'EntityType' },
    { id: 'dubai_free_zone', label: 'Dubai Free Zone', type: 'FreeZone' },
    { id: 'abu_dhabi_free_zone', label: 'Abu Dhabi Free Zone', type: 'FreeZone' },
    { id: 'sharjah_free_zone', label: 'Sharjah Free Zone', type: 'FreeZone' },
    { id: 'ajman_free_zone', label: 'Ajman Free Zone', type: 'FreeZone' },
    { id: 'ras_al_khaimah_free_zone', label: 'Ras Al Khaimah Free Zone', type: 'FreeZone' },
    { id: 'umm_al_quwain_free_zone', label: 'Umm Al Quwain Free Zone', type: 'FreeZone' },
    { id: 'dubai_economic_development', label: 'Dubai Economic Development', type: 'Regulator' },
    { id: 'abu_dhabi_department', label: 'Abu Dhabi Department of Economic Development', type: 'Regulator' },
    { id: 'federal_tax_authority', label: 'Federal Tax Authority', type: 'Regulator' },
    { id: 'central_bank', label: 'Central Bank of UAE', type: 'Regulator' },
    { id: 'securities_authority', label: 'Securities and Commodities Authority', type: 'Regulator' },
    { id: 'insurance_authority', label: 'Insurance Authority', type: 'Regulator' },
    { id: 'federal_court', label: 'Federal Supreme Court', type: 'Court' },
    { id: 'appeals_court', label: 'Federal Court of Appeal', type: 'Court' },
    { id: 'first_instance_court', label: 'Federal Court of First Instance', type: 'Court' },
    { id: 'dubai_court', label: 'Dubai Courts', type: 'Court' },
    { id: 'abu_dhabi_court', label: 'Abu Dhabi Courts', type: 'Court' },
    { id: 'sharjah_court', label: 'Sharjah Courts', type: 'Court' },
    { id: 'un', label: 'United Nations', type: 'InternationalBody' },
    { id: 'wto', label: 'World Trade Organization', type: 'InternationalBody' },
    { id: 'gcc', label: 'Gulf Cooperation Council', type: 'InternationalBody' },
    { id: 'arab_league', label: 'Arab League', type: 'InternationalBody' },
    
    // Legal Concepts & Types
    { id: 'corporate_governance', label: 'Corporate Governance', type: 'LegalConcept' },
    { id: 'intellectual_property', label: 'Intellectual Property Rights', type: 'LegalConcept' },
    { id: 'labor_law', label: 'Labor Law Principles', type: 'LegalConcept' },
    { id: 'tax_law', label: 'Tax Law Principles', type: 'LegalConcept' },
    { id: 'property_law', label: 'Property Law Principles', type: 'LegalConcept' },
    { id: 'contract_law', label: 'Contract Law Principles', type: 'LegalConcept' },
    { id: 'criminal_law', label: 'Criminal Law Principles', type: 'LegalConcept' },
    { id: 'civil_law', label: 'Civil Law Principles', type: 'LegalConcept' },
    { id: 'employment_contract', label: 'Employment Contract', type: 'ContractType' },
    { id: 'commercial_contract', label: 'Commercial Contract', type: 'ContractType' },
    { id: 'service_contract', label: 'Service Contract', type: 'ContractType' },
    { id: 'lease_contract', label: 'Lease Contract', type: 'ContractType' },
    { id: 'partnership_contract', label: 'Partnership Contract', type: 'ContractType' },
    { id: 'agency_contract', label: 'Agency Contract', type: 'ContractType' },
    { id: 'trademark', label: 'Trademark', type: 'IPType' },
    { id: 'patent', label: 'Patent', type: 'IPType' },
    { id: 'copyright', label: 'Copyright', type: 'IPType' },
    { id: 'industrial_design', label: 'Industrial Design', type: 'IPType' },
    { id: 'trade_secret', label: 'Trade Secret', type: 'IPType' },
    { id: 'full_time_employee', label: 'Full-time Employee', type: 'EmployeeType' },
    { id: 'part_time_employee', label: 'Part-time Employee', type: 'EmployeeType' },
    { id: 'contractor', label: 'Contractor', type: 'EmployeeType' },
    { id: 'hiring', label: 'Hiring', type: 'EmploymentAction' },
    { id: 'termination', label: 'Termination', type: 'EmploymentAction' },
    { id: 'promotion', label: 'Promotion', type: 'EmploymentAction' },
    { id: 'vat', label: 'Value Added Tax', type: 'TaxType' },
    { id: 'corporate_tax', label: 'Corporate Tax', type: 'TaxType' },
    { id: 'excise_tax', label: 'Excise Tax', type: 'TaxType' },
    { id: 'customs_duty', label: 'Customs Duty', type: 'TaxType' },
    { id: 'residential_property', label: 'Residential Property', type: 'PropertyType' },
    { id: 'commercial_property', label: 'Commercial Property', type: 'PropertyType' },
    { id: 'industrial_property', label: 'Industrial Property', type: 'PropertyType' },
    { id: 'land_property', label: 'Land Property', type: 'PropertyType' },
    { id: 'litigation', label: 'Litigation', type: 'LegalProcedure' },
    { id: 'arbitration', label: 'Arbitration', type: 'LegalProcedure' },
    { id: 'mediation', label: 'Mediation', type: 'LegalProcedure' },
    { id: 'appeal', label: 'Appeal', type: 'LegalProcedure' },
    { id: 'fraud', label: 'Fraud', type: 'CriminalOffense' },
    { id: 'embezzlement', label: 'Embezzlement', type: 'CriminalOffense' },
    { id: 'money_laundering', label: 'Money Laundering', type: 'CriminalOffense' },
    { id: 'corruption', label: 'Corruption', type: 'CriminalOffense' },
    { id: 'damages', label: 'Damages', type: 'LegalRemedy' },
    { id: 'injunction', label: 'Injunction', type: 'LegalRemedy' },
    { id: 'specific_performance', label: 'Specific Performance', type: 'LegalRemedy' },
    { id: 'trading', label: 'Trading', type: 'BusinessActivity' },
    { id: 'manufacturing', label: 'Manufacturing', type: 'BusinessActivity' },
    { id: 'services', label: 'Services', type: 'BusinessActivity' },
    { id: 'consulting', label: 'Consulting', type: 'BusinessActivity' },
    { id: 'contract_agreement', label: 'Contract Agreement', type: 'LegalDocument' },
    { id: 'memorandum', label: 'Memorandum of Association', type: 'LegalDocument' },
    { id: 'articles', label: 'Articles of Association', type: 'LegalDocument' },
    { id: 'license', label: 'Business License', type: 'LegalDocument' },
    { id: 'permit', label: 'Business Permit', type: 'LegalDocument' },
    { id: 'certificate', label: 'Certificate', type: 'LegalDocument' },
    { id: 'resolution', label: 'Board Resolution', type: 'LegalDocument' },
    { id: 'policy', label: 'Corporate Policy', type: 'LegalDocument' },
    { id: 'procedure', label: 'Standard Procedure', type: 'LegalDocument' },
    { id: 'financial_reporting', label: 'Financial Reporting', type: 'ComplianceRequirement' },
    { id: 'audit', label: 'Audit Requirements', type: 'ComplianceRequirement' },
    { id: 'disclosure', label: 'Disclosure Requirements', type: 'ComplianceRequirement' },
    { id: 'record_keeping', label: 'Record Keeping', type: 'ComplianceRequirement' },
    { id: 'data_protection', label: 'Data Protection', type: 'ComplianceRequirement' },
    { id: 'anti_money_laundering', label: 'Anti-Money Laundering', type: 'ComplianceRequirement' },
    { id: 'kyc', label: 'Know Your Customer', type: 'ComplianceRequirement' },
    { id: 'corporate_social_responsibility', label: 'Corporate Social Responsibility', type: 'ComplianceRequirement' },
    { id: 'lawyer', label: 'Lawyer', type: 'LegalProfession' },
    { id: 'legal_advisor', label: 'Legal Advisor', type: 'LegalProfession' },
    { id: 'notary', label: 'Notary Public', type: 'LegalProfession' },
    { id: 'judge', label: 'Judge', type: 'LegalProfession' },
    { id: 'case_1', label: 'Case No. 1/2023', type: 'LegalCase' },
    { id: 'case_2', label: 'Case No. 2/2023', type: 'LegalCase' },
    { id: 'case_3', label: 'Case No. 3/2023', type: 'LegalCase' },
    { id: 'case_4', label: 'Case No. 4/2023', type: 'LegalCase' },
    { id: 'case_5', label: 'Case No. 5/2023', type: 'LegalCase' },
    { id: 'corporate_law', label: 'Corporate Law', type: 'PracticeArea' },
    { id: 'commercial_law', label: 'Commercial Law', type: 'PracticeArea' },
    { id: 'labor_law_practice', label: 'Labor Law', type: 'PracticeArea' },
    { id: 'tax_law_practice', label: 'Tax Law', type: 'PracticeArea' },
    { id: 'intellectual_property_law', label: 'Intellectual Property Law', type: 'PracticeArea' },
    { id: 'real_estate_law', label: 'Real Estate Law', type: 'PracticeArea' },
    { id: 'conciliation', label: 'Conciliation', type: 'DisputeResolution' },
    { id: 'arbitration_process', label: 'Arbitration Process', type: 'DisputeResolution' },
    { id: 'mediation_process', label: 'Mediation Process', type: 'DisputeResolution' },
    { id: 'expert_determination', label: 'Expert Determination', type: 'DisputeResolution' },
    { id: 'direct_liability', label: 'Direct Liability', type: 'LiabilityType' },
    { id: 'vicarious_liability', label: 'Vicarious Liability', type: 'LiabilityType' },
    { id: 'strict_liability', label: 'Strict Liability', type: 'LiabilityType' },
    { id: 'joint_liability', label: 'Joint Liability', type: 'LiabilityType' },
    { id: 'property_rights', label: 'Property Rights', type: 'LegalRight' },
    { id: 'contractual_rights', label: 'Contractual Rights', type: 'LegalRight' },
    { id: 'employment_rights', label: 'Employment Rights', type: 'LegalRight' },
    { id: 'constitutional_rights', label: 'Constitutional Rights', type: 'LegalRight' },
    { id: 'fine', label: 'Fine', type: 'LegalSanction' },
    { id: 'imprisonment', label: 'Imprisonment', type: 'LegalSanction' },
    { id: 'suspension', label: 'Suspension', type: 'LegalSanction' },
    { id: 'revocation', label: 'Revocation', type: 'LegalSanction' },
    { id: 'legislative_process', label: 'Legislative Process', type: 'LegalProcess' },
    { id: 'judicial_process', label: 'Judicial Process', type: 'LegalProcess' },
    { id: 'administrative_process', label: 'Administrative Process', type: 'LegalProcess' },
    { id: 'regulatory_process', label: 'Regulatory Process', type: 'LegalProcess' }
  ];

  const edges = [
    // Constitutional relationships
    { from: 'constitution', to: 'federal_law_1', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_2', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_3', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_4', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_5', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_6', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_7', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_8', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_9', type: 'ESTABLISHES' },
    { from: 'constitution', to: 'federal_law_10', type: 'ESTABLISHES' },
    
    // Law relationships
    { from: 'federal_law_1', to: 'regulation_1', type: 'DEFINES' },
    { from: 'federal_law_2', to: 'regulation_2', type: 'DEFINES' },
    { from: 'federal_law_3', to: 'regulation_3', type: 'DEFINES' },
    { from: 'federal_law_4', to: 'regulation_4', type: 'DEFINES' },
    { from: 'federal_law_1', to: 'llc', type: 'REGULATES' },
    { from: 'federal_law_2', to: 'pjsc', type: 'REGULATES' },
    { from: 'federal_law_3', to: 'branch', type: 'REGULATES' },
    { from: 'federal_law_4', to: 'representative', type: 'REGULATES' },
    { from: 'federal_law_5', to: 'partnership', type: 'REGULATES' },
    { from: 'federal_law_6', to: 'sole_proprietorship', type: 'REGULATES' },
    { from: 'federal_law_7', to: 'free_zone_company', type: 'REGULATES' },
    
    // Entity relationships
    { from: 'llc', to: 'dubai_free_zone', type: 'GOVERNED_BY' },
    { from: 'pjsc', to: 'abu_dhabi_free_zone', type: 'GOVERNED_BY' },
    { from: 'branch', to: 'sharjah_free_zone', type: 'GOVERNED_BY' },
    { from: 'representative', to: 'ajman_free_zone', type: 'GOVERNED_BY' },
    { from: 'partnership', to: 'ras_al_khaimah_free_zone', type: 'GOVERNED_BY' },
    { from: 'sole_proprietorship', to: 'umm_al_quwain_free_zone', type: 'GOVERNED_BY' },
    
    // Regulatory relationships
    { from: 'dubai_economic_development', to: 'dubai_free_zone', type: 'OVERSEES' },
    { from: 'abu_dhabi_department', to: 'abu_dhabi_free_zone', type: 'OVERSEES' },
    { from: 'federal_tax_authority', to: 'vat', type: 'ADMINISTERS' },
    { from: 'central_bank', to: 'banking_regulation', type: 'ENFORCES' },
    { from: 'securities_authority', to: 'securities_regulation', type: 'ENFORCES' },
    { from: 'insurance_authority', to: 'insurance_regulation', type: 'ENFORCES' },
    
    // Court relationships
    { from: 'federal_court', to: 'appeals_court', type: 'HAS_COURT' },
    { from: 'appeals_court', to: 'first_instance_court', type: 'HAS_COURT' },
    { from: 'dubai_court', to: 'dubai_free_zone', type: 'HEARD_BY' },
    { from: 'abu_dhabi_court', to: 'abu_dhabi_free_zone', type: 'HEARD_BY' },
    { from: 'sharjah_court', to: 'sharjah_free_zone', type: 'HEARD_BY' },
    
    // International relationships
    { from: 'un', to: 'constitution', type: 'RECOGNIZES' },
    { from: 'wto', to: 'federal_law_1', type: 'ALIGNS_WITH' },
    { from: 'gcc', to: 'federal_law_2', type: 'ALIGNS_WITH' },
    { from: 'arab_league', to: 'federal_law_3', type: 'ALIGNS_WITH' },
    
    // Legal concept relationships
    { from: 'corporate_governance', to: 'llc', type: 'REQUIRES' },
    { from: 'intellectual_property', to: 'trademark', type: 'PROTECTS' },
    { from: 'labor_law', to: 'employment_contract', type: 'GOVERNED_BY' },
    { from: 'tax_law', to: 'vat', type: 'IMPOSED_BY' },
    { from: 'property_law', to: 'residential_property', type: 'PROTECTS' },
    { from: 'contract_law', to: 'commercial_contract', type: 'DEFINES' },
    { from: 'criminal_law', to: 'fraud', type: 'PREVENTS' },
    { from: 'civil_law', to: 'damages', type: 'PROVIDES' },
    
    // Contract relationships
    { from: 'employment_contract', to: 'full_time_employee', type: 'DEFINES' },
    { from: 'commercial_contract', to: 'trading', type: 'GOVERNED_BY' },
    { from: 'service_contract', to: 'services', type: 'GOVERNED_BY' },
    { from: 'lease_contract', to: 'residential_property', type: 'GOVERNED_BY' },
    { from: 'partnership_contract', to: 'partnership', type: 'DEFINES' },
    { from: 'agency_contract', to: 'representative', type: 'DEFINES' },
    
    // IP relationships
    { from: 'trademark', to: 'intellectual_property', type: 'PROTECTED_BY' },
    { from: 'patent', to: 'intellectual_property', type: 'PROTECTED_BY' },
    { from: 'copyright', to: 'intellectual_property', type: 'PROTECTED_BY' },
    { from: 'industrial_design', to: 'intellectual_property', type: 'PROTECTED_BY' },
    { from: 'trade_secret', to: 'intellectual_property', type: 'PROTECTED_BY' },
    
    // Employment relationships
    { from: 'full_time_employee', to: 'hiring', type: 'PRECEDES' },
    { from: 'part_time_employee', to: 'hiring', type: 'PRECEDES' },
    { from: 'contractor', to: 'hiring', type: 'PRECEDES' },
    { from: 'hiring', to: 'promotion', type: 'ALTERNATIVE_TO' },
    { from: 'promotion', to: 'termination', type: 'ALTERNATIVE_TO' },
    
    // Tax relationships
    { from: 'vat', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' },
    { from: 'corporate_tax', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' },
    { from: 'excise_tax', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' },
    { from: 'customs_duty', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' },
    
    // Property relationships
    { from: 'residential_property', to: 'property_law', type: 'GOVERNED_BY' },
    { from: 'commercial_property', to: 'property_law', type: 'GOVERNED_BY' },
    { from: 'industrial_property', to: 'property_law', type: 'GOVERNED_BY' },
    { from: 'land_property', to: 'property_law', type: 'GOVERNED_BY' },
    
    // Legal procedure relationships
    { from: 'litigation', to: 'federal_court', type: 'HEARD_BY' },
    { from: 'arbitration', to: 'arbitration_process', type: 'ALTERNATIVE_TO' },
    { from: 'mediation', to: 'mediation_process', type: 'ALTERNATIVE_TO' },
    { from: 'appeal', to: 'appeals_court', type: 'HEARD_BY' },
    
    // Criminal relationships
    { from: 'fraud', to: 'criminal_law', type: 'GOVERNED_BY' },
    { from: 'embezzlement', to: 'criminal_law', type: 'GOVERNED_BY' },
    { from: 'money_laundering', to: 'criminal_law', type: 'GOVERNED_BY' },
    { from: 'corruption', to: 'criminal_law', type: 'GOVERNED_BY' },
    
    // Remedy relationships
    { from: 'damages', to: 'civil_law', type: 'PROVIDES' },
    { from: 'injunction', to: 'civil_law', type: 'PROVIDES' },
    { from: 'specific_performance', to: 'civil_law', type: 'PROVIDES' },
    
    // Business activity relationships
    { from: 'trading', to: 'commercial_contract', type: 'GOVERNED_BY' },
    { from: 'manufacturing', to: 'industrial_property', type: 'REQUIRES' },
    { from: 'services', to: 'service_contract', type: 'GOVERNED_BY' },
    { from: 'consulting', to: 'service_contract', type: 'GOVERNED_BY' },
    
    // Document relationships
    { from: 'contract_agreement', to: 'commercial_contract', type: 'DEFINES' },
    { from: 'memorandum', to: 'llc', type: 'REQUIRES' },
    { from: 'articles', to: 'pjsc', type: 'REQUIRES' },
    { from: 'license', to: 'dubai_economic_development', type: 'ISSUED_BY' },
    { from: 'permit', to: 'abu_dhabi_department', type: 'ISSUED_BY' },
    { from: 'certificate', to: 'federal_tax_authority', type: 'ISSUED_BY' },
    { from: 'resolution', to: 'corporate_governance', type: 'REQUIRES' },
    { from: 'policy', to: 'corporate_governance', type: 'REQUIRES' },
    { from: 'procedure', to: 'corporate_governance', type: 'REQUIRES' },
    
    // Compliance relationships
    { from: 'financial_reporting', to: 'audit', type: 'REQUIRES' },
    { from: 'audit', to: 'disclosure', type: 'REQUIRES' },
    { from: 'disclosure', to: 'record_keeping', type: 'REQUIRES' },
    { from: 'record_keeping', to: 'data_protection', type: 'REQUIRES' },
    { from: 'data_protection', to: 'anti_money_laundering', type: 'ALIGNS_WITH' },
    { from: 'anti_money_laundering', to: 'kyc', type: 'REQUIRES' },
    { from: 'kyc', to: 'corporate_social_responsibility', type: 'ALIGNS_WITH' },
    
    // Profession relationships
    { from: 'lawyer', to: 'corporate_law', type: 'SPECIALIZES_IN' },
    { from: 'legal_advisor', to: 'commercial_law', type: 'SPECIALIZES_IN' },
    { from: 'notary', to: 'contract_law', type: 'SPECIALIZES_IN' },
    { from: 'judge', to: 'judicial_process', type: 'ADMINISTERS' },
    
    // Case relationships
    { from: 'case_1', to: 'federal_court', type: 'HEARD_BY' },
    { from: 'case_2', to: 'dubai_court', type: 'HEARD_BY' },
    { from: 'case_3', to: 'abu_dhabi_court', type: 'HEARD_BY' },
    { from: 'case_4', to: 'sharjah_court', type: 'HEARD_BY' },
    { from: 'case_5', to: 'appeals_court', type: 'HEARD_BY' },
    
    // Practice area relationships
    { from: 'corporate_law', to: 'llc', type: 'GOVERNED_BY' },
    { from: 'commercial_law', to: 'commercial_contract', type: 'GOVERNED_BY' },
    { from: 'labor_law_practice', to: 'employment_contract', type: 'GOVERNED_BY' },
    { from: 'tax_law_practice', to: 'vat', type: 'GOVERNED_BY' },
    { from: 'intellectual_property_law', to: 'trademark', type: 'PROTECTS' },
    { from: 'real_estate_law', to: 'residential_property', type: 'GOVERNED_BY' },
    
    // Dispute resolution relationships
    { from: 'conciliation', to: 'mediation', type: 'SIMILAR_TO' },
    { from: 'arbitration_process', to: 'arbitration', type: 'DEFINES' },
    { from: 'mediation_process', to: 'mediation', type: 'DEFINES' },
    { from: 'expert_determination', to: 'arbitration', type: 'ALTERNATIVE_TO' },
    
    // Liability relationships
    { from: 'direct_liability', to: 'llc', type: 'IMPOSED_BY' },
    { from: 'vicarious_liability', to: 'partnership', type: 'IMPOSED_BY' },
    { from: 'strict_liability', to: 'manufacturing', type: 'IMPOSED_BY' },
    { from: 'joint_liability', to: 'partnership', type: 'IMPOSED_BY' },
    
    // Rights relationships
    { from: 'property_rights', to: 'residential_property', type: 'GUARANTEED_BY' },
    { from: 'contractual_rights', to: 'commercial_contract', type: 'GUARANTEED_BY' },
    { from: 'employment_rights', to: 'employment_contract', type: 'GUARANTEED_BY' },
    { from: 'constitutional_rights', to: 'constitution', type: 'GUARANTEED_BY' },
    
    // Sanction relationships
    { from: 'fine', to: 'fraud', type: 'IMPOSED_BY' },
    { from: 'imprisonment', to: 'embezzlement', type: 'IMPOSED_BY' },
    { from: 'suspension', to: 'license', type: 'IMPOSED_BY' },
    { from: 'revocation', to: 'permit', type: 'IMPOSED_BY' },
    
    // Process relationships
    { from: 'legislative_process', to: 'federal_law_1', type: 'PRECEDES' },
    { from: 'judicial_process', to: 'federal_court', type: 'ADMINISTERED_BY' },
    { from: 'administrative_process', to: 'dubai_economic_development', type: 'ADMINISTERED_BY' },
    { from: 'regulatory_process', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' }
  ];

  return { nodes, edges };
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<DatabaseStats | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    console.log(`Calling complex backend at: ${BACKEND_URL}/api/graph`);
    
    // Try to get real data from backend first
    const backendResponse = await fetch(`${BACKEND_URL}/api/graph`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: AbortSignal.timeout(10000) // 10 second timeout
    });

    if (backendResponse.ok) {
      const backendData = await backendResponse.json();
      console.log('Backend stats response received:', backendData);
      
      // Calculate statistics from real Neo4j data
      const nodes = backendData.nodes || [];
      const edges = backendData.edges || [];
      
      // Count different types of nodes to estimate communities
      const nodeTypes = new Set(nodes.map((node: any) => node.type || 'unknown'));
      
      const stats: DatabaseStats = {
        total_documents: nodes.filter((node: any) => 
          ['Law', 'Regulation', 'LegalDocument', 'LegalNode'].includes(node.type)
        ).length,
        total_entities: nodes.length,
        total_relationships: edges.length,
        communities: nodeTypes.size,
        last_updated: new Date().toISOString()
      };
      
      console.log('Serving real Neo4j statistics:', stats);
      return res.status(200).json(stats);
    } else {
      console.log('Backend not available, falling back to mock data');
    }
  } catch (error) {
    console.error('Backend stats error:', error);
    console.log('Falling back to mock data');
  }

  // Fallback to mock data if backend is not available
  try {
    // Generate comprehensive knowledge graph data
    const { nodes, edges } = generateComprehensiveUAEKnowledgeGraph();
    
    // Calculate accurate statistics
    const stats: DatabaseStats = {
      total_documents: nodes.filter(node => 
        ['Law', 'Regulation', 'LegalDocument'].includes(node.type)
      ).length,
      total_entities: nodes.length,
      total_relationships: edges.length,
      communities: 29, // Number of unique node types
      last_updated: new Date().toISOString()
    };
    
    console.log('Serving mock statistics:', stats);
    res.status(200).json(stats);
  } catch (error) {
    console.error('Stats API error:', error);
    res.status(500).json({ 
      error: 'Failed to fetch database statistics'
    });
  }
}
