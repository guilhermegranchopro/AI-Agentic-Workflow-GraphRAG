import { NextApiRequest, NextApiResponse } from 'next';

export const config = {
  runtime: 'nodejs',
};

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8012';

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

// Function to check if backend is available
async function isBackendAvailable(): Promise<boolean> {
  try {
    const response = await fetch(`${BACKEND_URL}/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(3000)
    });
    return response.ok;
  } catch (error) {
    console.log('Backend not available, using mock data');
    return false;
  }
}

// Function to fetch real graph data from Neo4j backend
async function fetchRealGraphData(maxNodes: number, includeRelationships: string[]): Promise<GraphData | null> {
  try {
    console.log('Fetching real graph data from backend...');
    
    const response = await fetch(`${BACKEND_URL}/api/graph`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
      signal: AbortSignal.timeout(10000)
    });

    if (!response.ok) {
      console.log(`Backend responded with status: ${response.status}`);
      return null;
    }

    const data = await response.json();
    
    // Transform backend data to frontend format
    const nodes: GraphNode[] = data.nodes?.map((node: any) => ({
      id: node.id,
      label: node.title || node.content?.substring(0, 50) || node.id,
      type: node.type,
      properties: node.metadata || {}
    })) || [];

    const edges: GraphEdge[] = data.edges?.map((edge: any, index: number) => ({
      id: `edge_${index}`,
      from: edge.source,
      to: edge.target,
      label: edge.type,
      type: edge.type,
      properties: edge.metadata || {}
    })) || [];

    // Filter by max nodes if specified
    if (maxNodes < nodes.length) {
      const selectedNodes = nodes.slice(0, maxNodes);
      const selectedNodeIds = new Set(selectedNodes.map(n => n.id));
      
      const filteredEdges = edges.filter(edge => 
        selectedNodeIds.has(edge.from) && selectedNodeIds.has(edge.to) &&
        includeRelationships.includes(edge.type)
      );

      return {
        nodes: selectedNodes,
        edges: filteredEdges,
        stats: calculateStats(selectedNodes, filteredEdges)
      };
    }

    // Filter edges by relationship types
    const filteredEdges = edges.filter(edge => 
      includeRelationships.includes(edge.type)
    );

    return {
      nodes,
      edges: filteredEdges,
      stats: calculateStats(nodes, filteredEdges)
    };

  } catch (error) {
    console.error('Error fetching real graph data:', error);
    return null;
  }
}

// Function to calculate statistics
function calculateStats(nodes: GraphNode[], edges: GraphEdge[]) {
  const nodeTypes: Record<string, number> = {};
  const edgeTypes: Record<string, number> = {};

  nodes.forEach(node => {
    nodeTypes[node.type] = (nodeTypes[node.type] || 0) + 1;
  });

  edges.forEach(edge => {
    edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
  });

  return {
    nodeCount: nodes.length,
    edgeCount: edges.length,
    nodeTypes,
    edgeTypes
  };
}

// Comprehensive UAE Legal Knowledge Graph Data (Mock Data)
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
  addEdge(commercialCode, soleProprietorship, "DEFINES", "DEFINES");
  addEdge(commercialCode, branch, "DEFINES", "DEFINES");
  addEdge(commercialCode, representativeOffice, "DEFINES", "DEFINES");

  // 4. FREE ZONES
  const dubaiFreeZone = addNode("Dubai Free Zone", "FreeZone", { location: "dubai", type: "free_zone" });
  const abuDhabiFreeZone = addNode("Abu Dhabi Free Zone", "FreeZone", { location: "abu_dhabi", type: "free_zone" });
  const sharjahFreeZone = addNode("Sharjah Free Zone", "FreeZone", { location: "sharjah", type: "free_zone" });
  const ajmanFreeZone = addNode("Ajman Free Zone", "FreeZone", { location: "ajman", type: "free_zone" });
  const ummAlQuwainFreeZone = addNode("Umm Al Quwain Free Zone", "FreeZone", { location: "umm_al_quwain", type: "free_zone" });
  const rasAlKhaimahFreeZone = addNode("Ras Al Khaimah Free Zone", "FreeZone", { location: "ras_al_khaimah", type: "free_zone" });
  const fujairahFreeZone = addNode("Fujairah Free Zone", "FreeZone", { location: "fujairah", type: "free_zone" });

  addEdge(constitution, dubaiFreeZone, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, abuDhabiFreeZone, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, sharjahFreeZone, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, ajmanFreeZone, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, ummAlQuwainFreeZone, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, rasAlKhaimahFreeZone, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, fujairahFreeZone, "ESTABLISHES", "ESTABLISHES");

  // 5. JUDICIAL SYSTEM
  const federalSupremeCourt = addNode("Federal Supreme Court", "Court", { type: "supreme_court", level: "federal" });
  const federalCourtOfAppeal = addNode("Federal Court of Appeal", "Court", { type: "appellate_court", level: "federal" });
  const federalCourtOfFirstInstance = addNode("Federal Court of First Instance", "Court", { type: "trial_court", level: "federal" });
  const localCourts = addNode("Local Courts", "Court", { type: "local_courts", level: "local" });
  const shariaCourts = addNode("Sharia Courts", "Court", { type: "religious_courts", level: "local" });

  addEdge(constitution, federalSupremeCourt, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, federalCourtOfAppeal, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, federalCourtOfFirstInstance, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, localCourts, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, shariaCourts, "ESTABLISHES", "ESTABLISHES");

  // 6. REGULATORY BODIES
  const centralBank = addNode("Central Bank of UAE", "Regulator", { type: "financial_regulator" });
  const securitiesCommoditiesAuthority = addNode("Securities and Commodities Authority", "Regulator", { type: "securities_regulator" });
  const insuranceAuthority = addNode("Insurance Authority", "Regulator", { type: "insurance_regulator" });
  const telecomRegulator = addNode("Telecommunications Regulatory Authority", "Regulator", { type: "telecom_regulator" });
  const energyRegulator = addNode("Energy Regulatory Authority", "Regulator", { type: "energy_regulator" });

  addEdge(constitution, centralBank, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, securitiesCommoditiesAuthority, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, insuranceAuthority, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, telecomRegulator, "ESTABLISHES", "ESTABLISHES");
  addEdge(constitution, energyRegulator, "ESTABLISHES", "ESTABLISHES");

  // 7. TAX SYSTEM
  const corporateTax = addNode("Corporate Tax", "Tax", { type: "corporate_tax", rate: "9%" });
  const vat = addNode("Value Added Tax (VAT)", "Tax", { type: "consumption_tax", rate: "5%" });
  const exciseTax = addNode("Excise Tax", "Tax", { type: "excise_tax" });
  const customsDuty = addNode("Customs Duty", "Tax", { type: "import_tax" });

  addEdge(vatLaw, vat, "DEFINES", "DEFINES");
  addEdge(vatLaw, corporateTax, "RELATES_TO", "RELATES_TO");
  addEdge(vatLaw, exciseTax, "RELATES_TO", "RELATES_TO");
  addEdge(vatLaw, customsDuty, "RELATES_TO", "RELATES_TO");

  // 8. INTELLECTUAL PROPERTY
  const patents = addNode("Patents", "IP", { type: "patent_protection" });
  const trademarks = addNode("Trademarks", "IP", { type: "trademark_protection" });
  const copyrights = addNode("Copyrights", "IP", { type: "copyright_protection" });
  const industrialDesigns = addNode("Industrial Designs", "IP", { type: "design_protection" });

  addEdge(ipLaw, patents, "PROTECTS", "PROTECTS");
  addEdge(trademarkLaw, trademarks, "PROTECTS", "PROTECTS");
  addEdge(copyrightLaw, copyrights, "PROTECTS", "PROTECTS");
  addEdge(ipLaw, industrialDesigns, "PROTECTS", "PROTECTS");

  // 9. LABOR & EMPLOYMENT
  const employmentContract = addNode("Employment Contract", "Employment", { type: "contract_type" });
  const workPermit = addNode("Work Permit", "Employment", { type: "permit_type" });
  const laborCard = addNode("Labor Card", "Employment", { type: "identification" });
  const endOfService = addNode("End of Service Benefits", "Employment", { type: "benefit_type" });

  addEdge(laborLaw, employmentContract, "DEFINES", "DEFINES");
  addEdge(laborLaw, workPermit, "REQUIRES", "REQUIRES");
  addEdge(laborLaw, laborCard, "REQUIRES", "REQUIRES");
  addEdge(laborLaw, endOfService, "PROVIDES", "PROVIDES");

  // 10. ARBITRATION & DISPUTE RESOLUTION
  const arbitrationCenter = addNode("Arbitration Center", "DisputeResolution", { type: "arbitration_institution" });
  const mediationCenter = addNode("Mediation Center", "DisputeResolution", { type: "mediation_institution" });
  const conciliationCenter = addNode("Conciliation Center", "DisputeResolution", { type: "conciliation_institution" });

  addEdge(arbitrationLaw, arbitrationCenter, "ESTABLISHES", "ESTABLISHES");
  addEdge(arbitrationLaw, mediationCenter, "ESTABLISHES", "ESTABLISHES");
  addEdge(arbitrationLaw, conciliationCenter, "ESTABLISHES", "ESTABLISHES");

  // Calculate statistics
  return {
    nodes,
    edges,
    stats: calculateStats(nodes, edges)
  };
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    // Get query parameters with defaults
    const maxNodes = parseInt(req.query.max_nodes as string) || 1000;
    const includeRelationships = req.query.relationships 
      ? (req.query.relationships as string).split(',')
      : ["ESTABLISHES", "DEFINES", "REGULATES", "PROTECTS", "GOVERNED_BY", "REQUIRES", "HAS_PRINCIPLE", "ALIGNS_WITH", "CONTRADICTS", "RELATES_TO", "PROVIDES", "APPLIES_TO", "INCLUDES", "ENFORCED_BY", "AFFECTS", "ENFORCES", "HAS_SPECIAL"];

    // Check if backend is available
    const backendAvailable = await isBackendAvailable();
    
    if (backendAvailable) {
      console.log('Backend available, attempting to fetch real data...');
      const realData = await fetchRealGraphData(maxNodes, includeRelationships);
      
      if (realData) {
        console.log('Using real data from Neo4j backend');
        return res.status(200).json(realData);
      } else {
        console.log('Failed to fetch real data, falling back to mock data');
      }
    } else {
      console.log('Backend not available, using mock data');
    }

    // Fall back to mock data
    console.log('Generating comprehensive mock UAE knowledge graph...');
    const graphData = generateComprehensiveUAEKnowledgeGraph();

    // Filter by max nodes if specified
    if (maxNodes < graphData.nodes.length) {
      const selectedNodes = graphData.nodes.slice(0, maxNodes);
      const selectedNodeIds = new Set(selectedNodes.map(n => n.id));
      
      const filteredEdges = graphData.edges.filter(edge => 
        selectedNodeIds.has(edge.from) && selectedNodeIds.has(edge.to) &&
        includeRelationships.includes(edge.type)
      );

      return res.status(200).json({
        nodes: selectedNodes,
        edges: filteredEdges,
        stats: calculateStats(selectedNodes, filteredEdges)
      });
    }

    // Filter edges by relationship types
    const filteredEdges = graphData.edges.filter(edge => 
      includeRelationships.includes(edge.type)
    );

    res.status(200).json({
      nodes: graphData.nodes,
      edges: filteredEdges,
      stats: {
        nodeCount: graphData.nodes.length,
        edgeCount: filteredEdges.length,
        nodeTypes: graphData.stats.nodeTypes,
        edgeTypes: calculateStats(graphData.nodes, filteredEdges).edgeTypes
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
