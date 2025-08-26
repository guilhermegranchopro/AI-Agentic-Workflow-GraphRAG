import { NextApiRequest, NextApiResponse } from 'next';

export const config = {
  runtime: 'nodejs',
};

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties: Record<string, any>;
}

interface GraphEdge {
  id: string;
  from: string;
  to: string;
  label: string;
  type: string;
  properties: Record<string, any>;
}

interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    nodeCount: number;
    edgeCount: number;
    nodeTypes: Record<string, number>;
    edgeTypes: Record<string, number>;
  };
}

// Comprehensive UAE Legal Knowledge Graph Data
function generateComprehensiveUAEKnowledgeGraph(): GraphData {
  const nodes: GraphNode[] = [];
  const edges: GraphEdge[] = [];
  let nodeId = 1;
  let edgeId = 1;

  // Helper function to add node
  const addNode = (label: string, type: string, properties: Record<string, any> = {}) => {
    const id = String(nodeId++);
    nodes.push({ id, label, type, properties });
    return id;
  };

  // Helper function to add edge
  const addEdge = (from: string, to: string, label: string, type: string, properties: Record<string, any> = {}) => {
    edges.push({
      id: `edge_${edgeId++}`,
      from,
      to,
      label,
      type,
      properties
    });
  };

  // 1. CONSTITUTIONAL FRAMEWORK
  const constitution = addNode("UAE Constitution", "Constitutional", { year: 1971, type: "supreme_law" });
  const federalSupremeCouncil = addNode("Federal Supreme Council", "Constitutional", { type: "highest_authority" });
  const president = addNode("President of UAE", "Constitutional", { type: "head_of_state" });
  const vicePresident = addNode("Vice President of UAE", "Constitutional", { type: "deputy_head" });
  const cabinet = addNode("Federal Cabinet", "Constitutional", { type: "executive_body" });
  const nationalAssembly = addNode("Federal National Council", "Constitutional", { type: "legislative_body" });

  addEdge(constitution, federalSupremeCouncil, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, president, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, vicePresident, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, cabinet, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, nationalAssembly, "ESTABLISHES", "ESTABLISHES");

  // 2. CORE FEDERAL LAWS
  const civilCode = addNode("Federal Law No. 5 of 1985 - Civil Code", "Law", { year: 1985, type: "civil_law" });
  const commercialCode = addNode("Federal Law No. 18 of 1993 - Commercial Code", "Law", { year: 1993, type: "commercial_law" });
  const criminalCode = addNode("Federal Law No. 3 of 1987 - Criminal Code", "Law", { year: 1987, type: "criminal_law" });
  const laborLaw = addNode("Federal Law No. 8 of 1980 - Labor Law", "Law", { year: 1980, type: "labor_law" });
  const companiesLaw = addNode("Federal Law No. 2 of 2015 - Commercial Companies Law", "Law", { year: 2015, type: "corporate_law" });
  const arbitrationLaw = addNode("Federal Law No. 6 of 2018 - Arbitration Law", "Law", { year: 2018, type: "arbitration_law" });
  const vatLaw = addNode("Federal Law No. 8 of 2017 - VAT Law", "Law", { year: 2017, type: "tax_law" });
  const ipLaw = addNode("Federal Law No. 31 of 2006 - Industrial Property Law", "Law", { year: 2006, type: "ip_law" });
  const copyrightLaw = addNode("Federal Law No. 7 of 2002 - Copyright Law", "Law", { year: 2002, type: "copyright_law" });
  const trademarkLaw = addNode("Federal Law No. 37 of 1992 - Trademark Law", "Law", { year: 1992, type: "trademark_law" });

  addEdge(constitution, civilCode, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, commercialCode, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, criminalCode, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, laborLaw, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, companiesLaw, "ESTABLISHES", "ESTABLISHES");

  // 3. COMMERCIAL & CORPORATE ENTITIES
  const llc = addNode("Limited Liability Company (LLC)", "EntityType", { type: "commercial_entity" });
  const pjsc = addNode("Public Joint Stock Company (PJSC)", "EntityType", { type: "public_company" });
  const psc = addNode("Private Joint Stock Company (PSC)", "EntityType", { type: "private_company" });
  const partnership = addNode("Partnership", "EntityType", { type: "partnership" });
  const soleProprietorship = addNode("Sole Proprietorship", "EntityType", { type: "individual_business" });
  const branch = addNode("Branch Office", "EntityType", { type: "foreign_branch" });
  const representativeOffice = addNode("Representative Office", "EntityType", { type: "foreign_office" });

  addEdge(companiesLaw, llc, "DEFINES", "DEFINES");
  addEdge(companiesLaw, pjsc, "DEFINES", "DEFINES");
  addEdge(companiesLaw, psc, "DEFINES", "DEFINES");
  addEdge(companiesLaw, partnership, "DEFINES", "DEFINES");

  // 4. FREE ZONES
  const dmcc = addNode("Dubai Multi Commodities Centre (DMCC)", "FreeZone", { emirate: "Dubai", type: "commodities" });
  const difc = addNode("Dubai International Financial Centre (DIFC)", "FreeZone", { emirate: "Dubai", type: "financial" });
  const adgm = addNode("Abu Dhabi Global Market (ADGM)", "FreeZone", { emirate: "Abu Dhabi", type: "financial" });
  const jafza = addNode("Jebel Ali Free Zone (JAFZA)", "FreeZone", { emirate: "Dubai", type: "industrial" });
  const saifZone = addNode("Sharjah Airport International Free Zone (SAIF Zone)", "FreeZone", { emirate: "Sharjah", type: "aviation" });
  const rakez = addNode("Ras Al Khaimah Economic Zone (RAKEZ)", "FreeZone", { emirate: "Ras Al Khaimah", type: "mixed" });

  // 5. REGULATORY BODIES
  const sca = addNode("Securities and Commodities Authority (SCA)", "Regulator", { type: "securities_regulator" });
  const uaeCentralBank = addNode("UAE Central Bank", "Regulator", { type: "banking_regulator" });
  const ded = addNode("Department of Economic Development (DED)", "Regulator", { type: "business_regulator" });
  const tra = addNode("Telecommunications Regulatory Authority (TRA)", "Regulator", { type: "telecom_regulator" });
  const fta = addNode("Federal Tax Authority (FTA)", "Regulator", { type: "tax_regulator" });
  const mof = addNode("Ministry of Finance (MoF)", "Regulator", { type: "finance_regulator" });

  addEdge(sca, pjsc, "REGULATES", "REGULATES");
  addEdge(uaeCentralBank, branch, "REGULATES", "REGULATES");
  addEdge(ded, llc, "REGULATES", "REGULATES");
  addEdge(fta, vatLaw, "ENFORCES", "ENFORCES");

  // 6. COURT SYSTEM
  const federalSupremeCourt = addNode("Federal Supreme Court", "Court", { level: "federal_supreme", type: "constitutional" });
  const federalAppealCourt = addNode("Federal Court of Appeal", "Court", { level: "federal_appeal", type: "appellate" });
  const federalFirstInstance = addNode("Federal Court of First Instance", "Court", { level: "federal_first", type: "trial" });
  const difcCourt = addNode("DIFC Courts", "Court", { level: "free_zone", type: "commercial" });
  const adgmCourt = addNode("ADGM Courts", "Court", { level: "free_zone", type: "commercial" });
  const localCourts = addNode("Local Courts", "Court", { level: "local", type: "general" });

  addEdge(constitution, federalSupremeCourt, "ESTABLISHES", "ESTABLISHES");
  addEdge(federalSupremeCourt, federalAppealCourt, "OVERSEES", "OVERSEES");
  addEdge(federalAppealCourt, federalFirstInstance, "OVERSEES", "OVERSEES");

  // 7. LEGAL CONCEPTS & PRINCIPLES
  const limitedLiability = addNode("Limited Liability", "LegalConcept", { type: "corporate_principle" });
  const piercingVeil = addNode("Piercing Corporate Veil", "LegalConcept", { type: "corporate_principle" });
  const fiduciaryDuty = addNode("Fiduciary Duty", "LegalConcept", { type: "director_obligation" });
  const goodFaith = addNode("Good Faith", "LegalConcept", { type: "contract_principle" });
  const forceMajeure = addNode("Force Majeure", "LegalConcept", { type: "contract_principle" });
  const specificPerformance = addNode("Specific Performance", "LegalConcept", { type: "remedy" });
  const damages = addNode("Damages", "LegalConcept", { type: "remedy" });
  const injunction = addNode("Injunction", "LegalConcept", { type: "remedy" });

  addEdge(companiesLaw, limitedLiability, "ESTABLISHES", "ESTABLISHES");
  addEdge(companiesLaw, piercingVeil, "ESTABLISHES", "ESTABLISHES");
  addEdge(companiesLaw, fiduciaryDuty, "ESTABLISHES", "ESTABLISHES");
  addEdge(civilCode, goodFaith, "ESTABLISHES", "ESTABLISHES");
  addEdge(civilCode, forceMajeure, "ESTABLISHES", "ESTABLISHES");

  // 8. CONTRACT TYPES
  const salesContract = addNode("Sales Contract", "ContractType", { type: "commercial" });
  const serviceContract = addNode("Service Contract", "ContractType", { type: "commercial" });
  const employmentContract = addNode("Employment Contract", "ContractType", { type: "labor" });
  const leaseContract = addNode("Lease Contract", "ContractType", { type: "property" });
  const agencyContract = addNode("Agency Contract", "ContractType", { type: "commercial" });
  const partnershipContract = addNode("Partnership Contract", "ContractType", { type: "commercial" });

  addEdge(commercialCode, salesContract, "DEFINES", "DEFINES");
  addEdge(commercialCode, serviceContract, "DEFINES", "DEFINES");
  addEdge(laborLaw, employmentContract, "DEFINES", "DEFINES");
  addEdge(civilCode, leaseContract, "DEFINES", "DEFINES");

  // 9. INTELLECTUAL PROPERTY TYPES
  const patent = addNode("Patent", "IPType", { protection: "20_years", type: "invention" });
  const trademark = addNode("Trademark", "IPType", { protection: "10_years", type: "brand" });
  const copyright = addNode("Copyright", "IPType", { protection: "50_years", type: "creative_work" });
  const tradeSecret = addNode("Trade Secret", "IPType", { protection: "unlimited", type: "confidential" });
  const industrialDesign = addNode("Industrial Design", "IPType", { protection: "10_years", type: "design" });

  addEdge(ipLaw, patent, "PROTECTS", "PROTECTS");
  addEdge(trademarkLaw, trademark, "PROTECTS", "PROTECTS");
  addEdge(copyrightLaw, copyright, "PROTECTS", "PROTECTS");

  // 10. LABOR & EMPLOYMENT
  const permanentEmployee = addNode("Permanent Employee", "EmployeeType", { type: "full_time" });
  const temporaryEmployee = addNode("Temporary Employee", "EmployeeType", { type: "part_time" });
  const probationaryEmployee = addNode("Probationary Employee", "EmployeeType", { type: "trial" });
  const termination = addNode("Termination", "EmploymentAction", { type: "separation" });
  const resignation = addNode("Resignation", "EmploymentAction", { type: "voluntary" });
  const redundancy = addNode("Redundancy", "EmploymentAction", { type: "involuntary" });

  addEdge(laborLaw, permanentEmployee, "DEFINES", "DEFINES");
  addEdge(laborLaw, temporaryEmployee, "DEFINES", "DEFINES");
  addEdge(laborLaw, termination, "REGULATES", "REGULATES");

  // 11. TAX SYSTEM
  const corporateTax = addNode("Corporate Tax", "TaxType", { rate: "9%", type: "business_tax" });
  const vat = addNode("Value Added Tax (VAT)", "TaxType", { rate: "5%", type: "consumption_tax" });
  const exciseTax = addNode("Excise Tax", "TaxType", { type: "sin_tax" });
  const customsDuty = addNode("Customs Duty", "TaxType", { type: "import_tax" });

  addEdge(vatLaw, vat, "ESTABLISHES", "ESTABLISHES");
  addEdge(mof, corporateTax, "ADMINISTERS", "ADMINISTERS");

  // 12. REAL ESTATE & PROPERTY
  const freehold = addNode("Freehold Property", "PropertyType", { type: "ownership" });
  const leasehold = addNode("Leasehold Property", "PropertyType", { type: "tenure" });
  const usufruct = addNode("Usufruct", "PropertyType", { type: "right" });
  const mortgage = addNode("Mortgage", "PropertyType", { type: "security" });

  addEdge(civilCode, freehold, "DEFINES", "DEFINES");
  addEdge(civilCode, leasehold, "DEFINES", "DEFINES");
  addEdge(civilCode, usufruct, "DEFINES", "DEFINES");

  // 13. INTERNATIONAL TREATIES & AGREEMENTS
  const wto = addNode("World Trade Organization (WTO)", "InternationalBody", { type: "trade" });
  const wipo = addNode("World Intellectual Property Organization (WIPO)", "InternationalBody", { type: "ip" });
  const gcc = addNode("Gulf Cooperation Council (GCC)", "InternationalBody", { type: "regional" });
  const un = addNode("United Nations (UN)", "InternationalBody", { type: "global" });

  addEdge(ipLaw, wipo, "ALIGNS_WITH", "ALIGNS_WITH");
  addEdge(commercialCode, wto, "ALIGNS_WITH", "ALIGNS_WITH");

  // 14. LEGAL PROCEDURES
  const litigation = addNode("Litigation", "LegalProcedure", { type: "court_proceeding" });
  const arbitration = addNode("Arbitration", "LegalProcedure", { type: "alternative_dispute" });
  const mediation = addNode("Mediation", "LegalProcedure", { type: "alternative_dispute" });
  const conciliation = addNode("Conciliation", "LegalProcedure", { type: "alternative_dispute" });

  addEdge(arbitrationLaw, arbitration, "ESTABLISHES", "ESTABLISHES");
  addEdge(civilCode, litigation, "ESTABLISHES", "ESTABLISHES");

  // 15. CRIMINAL OFFENSES
  const fraud = addNode("Fraud", "CriminalOffense", { type: "financial_crime" });
  const corruption = addNode("Corruption", "CriminalOffense", { type: "public_crime" });
  const moneyLaundering = addNode("Money Laundering", "CriminalOffense", { type: "financial_crime" });
  const cybercrime = addNode("Cybercrime", "CriminalOffense", { type: "digital_crime" });

  addEdge(criminalCode, fraud, "DEFINES", "DEFINES");
  addEdge(criminalCode, corruption, "DEFINES", "DEFINES");
  addEdge(criminalCode, moneyLaundering, "DEFINES", "DEFINES");

  // 16. LEGAL REMEDIES
  const compensation = addNode("Compensation", "LegalRemedy", { type: "monetary" });
  const restitution = addNode("Restitution", "LegalRemedy", { type: "restoration" });
  const declaratoryJudgment = addNode("Declaratory Judgment", "LegalRemedy", { type: "clarification" });

  addEdge(civilCode, compensation, "PROVIDES", "PROVIDES");
  addEdge(civilCode, restitution, "PROVIDES", "PROVIDES");

  // 17. BUSINESS ACTIVITIES
  const trading = addNode("Trading", "BusinessActivity", { type: "commercial" });
  const manufacturing = addNode("Manufacturing", "BusinessActivity", { type: "industrial" });
  const services = addNode("Services", "BusinessActivity", { type: "service" });
  const consulting = addNode("Consulting", "BusinessActivity", { type: "professional" });

  addEdge(commercialCode, trading, "REGULATES", "REGULATES");
  addEdge(commercialCode, manufacturing, "REGULATES", "REGULATES");

  // 18. LEGAL DOCUMENTS
  const memorandum = addNode("Memorandum of Association", "LegalDocument", { type: "corporate" });
  const articles = addNode("Articles of Association", "LegalDocument", { type: "corporate" });
  const bylaws = addNode("Bylaws", "LegalDocument", { type: "corporate" });
  const prospectus = addNode("Prospectus", "LegalDocument", { type: "securities" });

  addEdge(companiesLaw, memorandum, "REQUIRES", "REQUIRES");
  addEdge(companiesLaw, articles, "REQUIRES", "REQUIRES");
  addEdge(sca, prospectus, "REQUIRES", "REQUIRES");

  // 19. COMPLIANCE REQUIREMENTS
  const audit = addNode("Audit", "ComplianceRequirement", { type: "financial" });
  const reporting = addNode("Financial Reporting", "ComplianceRequirement", { type: "disclosure" });
  const licensing = addNode("Licensing", "ComplianceRequirement", { type: "authorization" });
  const registration = addNode("Registration", "ComplianceRequirement", { type: "formalization" });

  addEdge(companiesLaw, audit, "REQUIRES", "REQUIRES");
  addEdge(companiesLaw, reporting, "REQUIRES", "REQUIRES");
  addEdge(ded, licensing, "REQUIRES", "REQUIRES");

  // 20. LEGAL PROFESSIONS
  const lawyer = addNode("Lawyer", "LegalProfession", { type: "legal_practitioner" });
  const notary = addNode("Notary Public", "LegalProfession", { type: "legal_officer" });
  const judge = addNode("Judge", "LegalProfession", { type: "judicial_officer" });
  const prosecutor = addNode("Prosecutor", "LegalProfession", { type: "legal_officer" });

  addEdge(constitution, judge, "ESTABLISHES", "ESTABLISHES");
  addEdge(civilCode, notary, "RECOGNIZES", "RECOGNIZES");

  // Add relationships between different categories
  addEdge(llc, limitedLiability, "HAS_PRINCIPLE", "HAS_PRINCIPLE");
  addEdge(pjsc, sca, "REGULATED_BY", "REGULATED_BY");
  addEdge(difc, difcCourt, "HAS_COURT", "HAS_COURT");
  addEdge(adgm, adgmCourt, "HAS_COURT", "HAS_COURT");
  addEdge(salesContract, goodFaith, "REQUIRES", "REQUIRES");
  addEdge(employmentContract, laborLaw, "GOVERNED_BY", "GOVERNED_BY");
  addEdge(patent, wipo, "PROTECTED_BY", "PROTECTED_BY");
  addEdge(trademark, wipo, "PROTECTED_BY", "PROTECTED_BY");
  addEdge(copyright, wipo, "PROTECTED_BY", "PROTECTED_BY");
  addEdge(fraud, criminalCode, "DEFINED_BY", "DEFINED_BY");
  addEdge(arbitration, arbitrationLaw, "GOVERNED_BY", "GOVERNED_BY");
  addEdge(vat, fta, "ADMINISTERED_BY", "ADMINISTERED_BY");
  addEdge(corporateTax, mof, "ADMINISTERED_BY", "ADMINISTERED_BY");

  // 21. ADDITIONAL LEGAL CASES & PRECEDENTS
  const case1 = addNode("Case: Emirates Airlines v. Contractor (2022)", "LegalCase", { year: 2022, type: "contract_dispute" });
  const case2 = addNode("Case: Dubai Properties v. Developer (2021)", "LegalCase", { year: 2021, type: "real_estate" });
  const case3 = addNode("Case: Abu Dhabi Bank v. Borrower (2023)", "LegalCase", { year: 2023, type: "banking" });
  const case4 = addNode("Case: Sharjah Free Zone v. Company (2022)", "LegalCase", { year: 2022, type: "free_zone" });
  const case5 = addNode("Case: DIFC Courts v. International Bank (2023)", "LegalCase", { year: 2023, type: "financial" });

  addEdge(case1, civilCode, "INTERPRETED_BY", "INTERPRETED_BY");
  addEdge(case2, civilCode, "INTERPRETED_BY", "INTERPRETED_BY");
  addEdge(case3, commercialCode, "INTERPRETED_BY", "INTERPRETED_BY");
  addEdge(case4, companiesLaw, "INTERPRETED_BY", "INTERPRETED_BY");
  addEdge(case5, difcCourt, "HEARD_BY", "HEARD_BY");

  // 22. SPECIFIC REGULATIONS & DECREES
  const decree1 = addNode("Dubai Decree No. 20 of 2020 - Virtual Companies", "Regulation", { year: 2020, type: "virtual_business" });
  const decree2 = addNode("Abu Dhabi Law No. 4 of 2021 - Data Protection", "Regulation", { year: 2021, type: "data_protection" });
  const decree3 = addNode("Federal Decree No. 15 of 2022 - E-commerce", "Regulation", { year: 2022, type: "ecommerce" });
  const decree4 = addNode("Sharjah Law No. 8 of 2021 - Tourism", "Regulation", { year: 2021, type: "tourism" });

  addEdge(decree1, companiesLaw, "AMENDS", "AMENDS");
  addEdge(decree2, civilCode, "SUPPLEMENTS", "SUPPLEMENTS");
  addEdge(decree3, commercialCode, "AMENDS", "AMENDS");
  addEdge(decree4, ded, "ENFORCED_BY", "ENFORCED_BY");

  // 23. LEGAL PRACTICE AREAS
  const corporateLawPractice = addNode("Corporate Law Practice", "PracticeArea", { type: "business_law" });
  const commercialLawPractice = addNode("Commercial Law Practice", "PracticeArea", { type: "trade_law" });
  const employmentLawPractice = addNode("Employment Law Practice", "PracticeArea", { type: "labor_law" });
  const intellectualPropertyLawPractice = addNode("Intellectual Property Law Practice", "PracticeArea", { type: "ip_law" });
  const realEstateLawPractice = addNode("Real Estate Law Practice", "PracticeArea", { type: "property_law" });
  const criminalLawPractice = addNode("Criminal Law Practice", "PracticeArea", { type: "criminal_law" });

  addEdge(corporateLawPractice, companiesLaw, "SPECIALIZES_IN", "SPECIALIZES_IN");
  addEdge(commercialLawPractice, commercialCode, "SPECIALIZES_IN", "SPECIALIZES_IN");
  addEdge(employmentLawPractice, laborLaw, "SPECIALIZES_IN", "SPECIALIZES_IN");
  addEdge(intellectualPropertyLawPractice, patent, "SPECIALIZES_IN", "SPECIALIZES_IN");
  addEdge(realEstateLawPractice, freehold, "SPECIALIZES_IN", "SPECIALIZES_IN");
  addEdge(criminalLawPractice, criminalCode, "SPECIALIZES_IN", "SPECIALIZES_IN");

  // 24. LEGAL DOCUMENTS & FORMS
  const powerOfAttorney = addNode("Power of Attorney", "LegalDocument", { type: "authorization" });
  const nonDisclosureAgreement = addNode("Non-Disclosure Agreement", "LegalDocument", { type: "confidentiality" });
  const employmentAgreement = addNode("Employment Agreement", "LegalDocument", { type: "employment" });
  const serviceAgreement = addNode("Service Agreement", "LegalDocument", { type: "service" });
  const leaseAgreement = addNode("Lease Agreement", "LegalDocument", { type: "property" });

  addEdge(powerOfAttorney, civilCode, "GOVERNED_BY", "GOVERNED_BY");
  addEdge(nonDisclosureAgreement, tradeSecret, "PROTECTS", "PROTECTS");
  addEdge(employmentAgreement, laborLaw, "GOVERNED_BY", "GOVERNED_BY");
  addEdge(serviceAgreement, commercialCode, "GOVERNED_BY", "GOVERNED_BY");
  addEdge(leaseAgreement, civilCode, "GOVERNED_BY", "GOVERNED_BY");

  // 25. COMPLIANCE & REGULATORY REQUIREMENTS
  const antiMoneyLaundering = addNode("Anti-Money Laundering (AML)", "ComplianceRequirement", { type: "financial_crime" });
  const knowYourCustomer = addNode("Know Your Customer (KYC)", "ComplianceRequirement", { type: "customer_due_diligence" });
  const dataProtection = addNode("Data Protection Compliance", "ComplianceRequirement", { type: "privacy" });
  const corporateGovernance = addNode("Corporate Governance", "ComplianceRequirement", { type: "management" });

  addEdge(antiMoneyLaundering, moneyLaundering, "PREVENTS", "PREVENTS");
  addEdge(knowYourCustomer, fraud, "PREVENTS", "PREVENTS");
  addEdge(dataProtection, decree2, "REQUIRED_BY", "REQUIRED_BY");
  addEdge(corporateGovernance, companiesLaw, "REQUIRED_BY", "REQUIRED_BY");

  // 26. DISPUTE RESOLUTION MECHANISMS
  const expertDetermination = addNode("Expert Determination", "DisputeResolution", { type: "technical_dispute" });
  const negotiation = addNode("Negotiation", "DisputeResolution", { type: "direct_resolution" });
  const conciliationProcess = addNode("Conciliation", "DisputeResolution", { type: "assisted_resolution" });
  const adjudication = addNode("Adjudication", "DisputeResolution", { type: "binding_resolution" });

  addEdge(expertDetermination, arbitration, "ALTERNATIVE_TO", "ALTERNATIVE_TO");
  addEdge(negotiation, mediation, "PRECEDES", "PRECEDES");
  addEdge(conciliationProcess, mediation, "SIMILAR_TO", "SIMILAR_TO");
  addEdge(adjudication, litigation, "ALTERNATIVE_TO", "ALTERNATIVE_TO");

  // 27. LEGAL LIABILITIES & OBLIGATIONS
  const contractualLiability = addNode("Contractual Liability", "LiabilityType", { type: "contract_based" });
  const tortiousLiability = addNode("Tortious Liability", "LiabilityType", { type: "civil_wrong" });
  const statutoryLiability = addNode("Statutory Liability", "LiabilityType", { type: "law_based" });
  const vicariousLiability = addNode("Vicarious Liability", "LiabilityType", { type: "employer_responsibility" });

  addEdge(contractualLiability, civilCode, "DEFINED_BY", "DEFINED_BY");
  addEdge(tortiousLiability, civilCode, "DEFINED_BY", "DEFINED_BY");
  addEdge(statutoryLiability, companiesLaw, "DEFINED_BY", "DEFINED_BY");
  addEdge(vicariousLiability, laborLaw, "DEFINED_BY", "DEFINED_BY");

  // 28. LEGAL RIGHTS & ENTITLEMENTS
  const rightToInformation = addNode("Right to Information", "LegalRight", { type: "access_right" });
  const rightToPrivacy = addNode("Right to Privacy", "LegalRight", { type: "personal_right" });
  const rightToFairTrial = addNode("Right to Fair Trial", "LegalRight", { type: "procedural_right" });
  const rightToProperty = addNode("Right to Property", "LegalRight", { type: "property_right" });

  addEdge(rightToInformation, constitution, "GUARANTEED_BY", "GUARANTEED_BY");
  addEdge(rightToPrivacy, constitution, "GUARANTEED_BY", "GUARANTEED_BY");
  addEdge(rightToFairTrial, constitution, "GUARANTEED_BY", "GUARANTEED_BY");
  addEdge(rightToProperty, constitution, "GUARANTEED_BY", "GUARANTEED_BY");

  // 29. LEGAL SANCTIONS & PENALTIES
  const fine = addNode("Fine", "LegalSanction", { type: "monetary_penalty" });
  const imprisonment = addNode("Imprisonment", "LegalSanction", { type: "custodial_sentence" });
  const suspension = addNode("Suspension", "LegalSanction", { type: "temporary_ban" });
  const revocation = addNode("Revocation", "LegalSanction", { type: "permanent_ban" });

  addEdge(fine, criminalCode, "IMPOSED_BY", "IMPOSED_BY");
  addEdge(imprisonment, criminalCode, "IMPOSED_BY", "IMPOSED_BY");
  addEdge(suspension, ded, "IMPOSED_BY", "IMPOSED_BY");
  addEdge(revocation, ded, "IMPOSED_BY", "IMPOSED_BY");

  // 30. LEGAL PROCEDURES & PROCESSES
  const registrationProcess = addNode("Company Registration Process", "LegalProcess", { type: "formation" });
  const licensingProcess = addNode("Business Licensing Process", "LegalProcess", { type: "authorization" });
  const disputeProcess = addNode("Dispute Resolution Process", "LegalProcess", { type: "conflict_resolution" });
  const complianceProcess = addNode("Compliance Monitoring Process", "LegalProcess", { type: "oversight" });

  addEdge(registrationProcess, companiesLaw, "GOVERNED_BY", "GOVERNED_BY");
  addEdge(licensingProcess, ded, "ADMINISTERED_BY", "ADMINISTERED_BY");
  addEdge(disputeProcess, arbitration, "INCLUDES", "INCLUDES");
  addEdge(complianceProcess, audit, "INCLUDES", "INCLUDES");

  // Add contradictory data for AI Analysis demonstration
  const contradictoryNodes = [
    // Contradictory Tax Regulations
    { id: 'vat_old', label: 'VAT Rate 5% (2018-2023)', type: 'TaxType', properties: { rate: 5, effective_date: '2018-01-01', end_date: '2023-01-01', source: 'Federal Tax Authority 2018' }},
    { id: 'vat_new', label: 'VAT Rate 7% (2023-Present)', type: 'TaxType', properties: { rate: 7, effective_date: '2023-01-01', source: 'Federal Tax Authority 2023' }},
    { id: 'vat_amendment', label: 'VAT Rate 6% (Proposed)', type: 'TaxType', properties: { rate: 6, effective_date: '2024-01-01', source: 'Cabinet Resolution 2024', status: 'proposed' }},
    
    // Contradictory Employment Laws
    { id: 'notice_old', label: '30 Days Notice (Pre-2020)', type: 'LegalConcept', properties: { notice_period: 30, effective_date: '2015-01-01', end_date: '2020-01-01', source: 'Labor Law 2015' }},
    { id: 'notice_new', label: '60 Days Notice (Post-2020)', type: 'LegalConcept', properties: { notice_period: 60, effective_date: '2020-01-01', source: 'Labor Law Amendment 2020' }},
    { id: 'notice_court', label: '45 Days Notice (Court Interpretation)', type: 'LegalConcept', properties: { notice_period: 45, effective_date: '2021-06-15', source: 'Federal Court Decision 2021', interpretation: 'reasonable period' }},
    
    // Contradictory Free Zone Regulations
    { id: 'dubai_tech_license', label: 'Dubai Tech License (No Office Required)', type: 'LegalDocument', properties: { office_requirement: false, source: 'Dubai Free Zone 2022', jurisdiction: 'Dubai' }},
    { id: 'abu_dhabi_tech_license', label: 'Abu Dhabi Tech License (Office Required)', type: 'LegalDocument', properties: { office_requirement: true, source: 'Abu Dhabi Free Zone 2022', jurisdiction: 'Abu Dhabi' }},
    { id: 'federal_tech_regulation', label: 'Federal Tech Regulation (Mixed Requirements)', type: 'Regulation', properties: { office_requirement: 'conditional', source: 'Federal Cabinet 2022', applies_to: 'all_emirates' }},
    
    // Contradictory IP Laws
    { id: 'copyright_old', label: 'Copyright 50 Years (Pre-2021)', type: 'IPType', properties: { duration: 50, effective_date: '1992-01-01', end_date: '2021-01-01', source: 'IP Law 1992' }},
    { id: 'copyright_new', label: 'Copyright 70 Years (Post-2021)', type: 'IPType', properties: { duration: 70, effective_date: '2021-01-01', source: 'IP Law Amendment 2021' }},
    { id: 'copyright_wto', label: 'Copyright 75 Years (WTO Standard)', type: 'IPType', properties: { duration: 75, source: 'WTO TRIPS Agreement', international: true }},
    
    // Contradictory Corporate Governance
    { id: 'board_size_old', label: 'Minimum 3 Directors (Pre-2022)', type: 'ComplianceRequirement', properties: { min_directors: 3, effective_date: '2015-01-01', end_date: '2022-01-01', source: 'Companies Law 2015' }},
    { id: 'board_size_new', label: 'Minimum 5 Directors (Post-2022)', type: 'ComplianceRequirement', properties: { min_directors: 5, effective_date: '2022-01-01', source: 'Companies Law Amendment 2022' }},
    { id: 'board_size_exception', label: 'Minimum 2 Directors (Small Companies)', type: 'ComplianceRequirement', properties: { min_directors: 2, effective_date: '2022-01-01', source: 'Companies Law Amendment 2022', exception: 'small_companies' }},
    
    // Contradictory Data Protection
    { id: 'data_retention_old', label: 'Data Retention 3 Years (Pre-2023)', type: 'ComplianceRequirement', properties: { retention_period: 3, effective_date: '2020-01-01', end_date: '2023-01-01', source: 'Data Protection Law 2020' }},
    { id: 'data_retention_new', label: 'Data Retention 7 Years (Post-2023)', type: 'ComplianceRequirement', properties: { retention_period: 7, effective_date: '2023-01-01', source: 'Data Protection Law Amendment 2023' }},
    { id: 'data_retention_gdpr', label: 'Data Retention 5 Years (GDPR Alignment)', type: 'ComplianceRequirement', properties: { retention_period: 5, source: 'GDPR Compliance Guidelines', international: true }}
  ];

  const contradictoryEdges = [
    // Tax contradictions
    { from: 'vat_old', to: 'vat_new', type: 'CONTRADICTS' },
    { from: 'vat_new', to: 'vat_amendment', type: 'CONTRADICTS' },
    { from: 'vat_old', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' },
    { from: 'vat_new', to: 'federal_tax_authority', type: 'ADMINISTERED_BY' },
    { from: 'vat_amendment', to: 'federal_tax_authority', type: 'PROPOSED_BY' },
    
    // Employment contradictions
    { from: 'notice_old', to: 'notice_new', type: 'CONTRADICTS' },
    { from: 'notice_new', to: 'notice_court', type: 'CONTRADICTS' },
    { from: 'notice_old', to: 'labor_law', type: 'DEFINED_BY' },
    { from: 'notice_new', to: 'labor_law', type: 'AMENDS' },
    { from: 'notice_court', to: 'federal_court', type: 'INTERPRETED_BY' },
    
    // Free zone contradictions
    { from: 'dubai_tech_license', to: 'abu_dhabi_tech_license', type: 'CONTRADICTS' },
    { from: 'abu_dhabi_tech_license', to: 'federal_tech_regulation', type: 'CONTRADICTS' },
    { from: 'dubai_tech_license', to: 'dubai_free_zone', type: 'ISSUED_BY' },
    { from: 'abu_dhabi_tech_license', to: 'abu_dhabi_free_zone', type: 'ISSUED_BY' },
    { from: 'federal_tech_regulation', to: 'federal_law_1', type: 'DEFINED_BY' },
    
    // IP contradictions
    { from: 'copyright_old', to: 'copyright_new', type: 'CONTRADICTS' },
    { from: 'copyright_new', to: 'copyright_wto', type: 'CONTRADICTS' },
    { from: 'copyright_old', to: 'intellectual_property', type: 'PROTECTED_BY' },
    { from: 'copyright_new', to: 'intellectual_property', type: 'AMENDS' },
    { from: 'copyright_wto', to: 'wto', type: 'ALIGNS_WITH' },
    
    // Corporate governance contradictions
    { from: 'board_size_old', to: 'board_size_new', type: 'CONTRADICTS' },
    { from: 'board_size_new', to: 'board_size_exception', type: 'CONTRADICTS' },
    { from: 'board_size_old', to: 'corporate_governance', type: 'REQUIRES' },
    { from: 'board_size_new', to: 'corporate_governance', type: 'AMENDS' },
    { from: 'board_size_exception', to: 'corporate_governance', type: 'EXCEPTION_TO' },
    
    // Data protection contradictions
    { from: 'data_retention_old', to: 'data_retention_new', type: 'CONTRADICTS' },
    { from: 'data_retention_new', to: 'data_retention_gdpr', type: 'CONTRADICTS' },
    { from: 'data_retention_old', to: 'data_protection', type: 'REQUIRES' },
    { from: 'data_retention_new', to: 'data_protection', type: 'AMENDS' },
    { from: 'data_retention_gdpr', to: 'un', type: 'ALIGNS_WITH' }
  ];

  // Add contradictory nodes and edges to the main arrays
  nodes.push(...contradictoryNodes);
  edges.push(...contradictoryEdges);

  // Calculate statistics
  const nodeTypes: Record<string, number> = {};
  const edgeTypes: Record<string, number> = {};

  nodes.forEach(node => {
    nodeTypes[node.type] = (nodeTypes[node.type] || 0) + 1;
  });

  edges.forEach(edge => {
    edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
  });

  return {
    nodes,
    edges,
    stats: {
      nodeCount: nodes.length,
      edgeCount: edges.length,
      nodeTypes,
      edgeTypes
    }
  };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Get query parameters with defaults
    const maxNodes = parseInt(req.query.max_nodes as string) || 1000;
    const includeRelationships = req.query.relationships 
      ? (req.query.relationships as string).split(',')
      : ["ESTABLISHES", "DEFINES", "REGULATES", "PROTECTS", "GOVERNED_BY", "REQUIRES", "HAS_PRINCIPLE", "ALIGNS_WITH"];

    // Generate comprehensive knowledge graph
    const graphData = generateComprehensiveUAEKnowledgeGraph();

    // Filter by max nodes if specified
    if (maxNodes < graphData.nodes.length) {
      const selectedNodes = graphData.nodes.slice(0, maxNodes);
      const selectedNodeIds = new Set(selectedNodes.map(n => n.id));
      
      const filteredEdges = graphData.edges.filter(edge => 
        selectedNodeIds.has(edge.from) && selectedNodeIds.has(edge.to) &&
        includeRelationships.includes(edge.type)
      );

      // Recalculate stats
      const nodeTypes: Record<string, number> = {};
      const edgeTypes: Record<string, number> = {};

      selectedNodes.forEach(node => {
        nodeTypes[node.type] = (nodeTypes[node.type] || 0) + 1;
      });

      filteredEdges.forEach(edge => {
        edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
      });

      return res.status(200).json({
        nodes: selectedNodes,
        edges: filteredEdges,
        stats: {
          nodeCount: selectedNodes.length,
          edgeCount: filteredEdges.length,
          nodeTypes,
          edgeTypes
        }
      });
    }

    // Filter edges by relationship types
    const filteredEdges = graphData.edges.filter(edge => 
      includeRelationships.includes(edge.type)
    );

    // Recalculate stats for filtered edges
    const edgeTypes: Record<string, number> = {};
    filteredEdges.forEach(edge => {
      edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
    });

    res.status(200).json({
      nodes: graphData.nodes,
      edges: filteredEdges,
      stats: {
        nodeCount: graphData.nodes.length,
        edgeCount: filteredEdges.length,
        nodeTypes: graphData.stats.nodeTypes,
        edgeTypes
      }
    });

  } catch (error) {
    console.error('Graph data error:', error);
    res.status(500).json({ 
      error: 'Failed to generate graph data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
