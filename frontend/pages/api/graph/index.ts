import { NextApiRequest, NextApiResponse } from 'next';
import { executeQuery } from '../../../lib/graph/neo4j';
import { hasNeo4jConfig } from '../../../lib/config';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Check Neo4j configuration
    if (!hasNeo4jConfig()) {
      return res.status(503).json({
        error: 'Neo4j not configured',
        message: 'Please configure Neo4j environment variables',
        details: {
          neo4j_configured: false,
          required_vars: ['NEO4J_URI', 'NEO4J_USERNAME', 'NEO4J_PASSWORD']
        }
      });
    }

    const maxNodes = parseInt(req.query.max_nodes as string) || 50;
    const includeRelationships = req.query.relationships 
      ? (req.query.relationships as string).split(',')
      : ["HAS_PROVISION", "CITES", "INTERPRETED_BY", "AMENDED_BY"];

    // Fetch graph data
    const graphData = await fetchGraphData(maxNodes, includeRelationships);
    
    res.status(200).json(graphData);
  } catch (error) {
    console.error('Graph API error:', error);
    res.status(500).json({ 
      error: error instanceof Error ? error.message : 'Failed to fetch graph data',
      nodes: [],
      edges: [],
      stats: {
        nodeCount: 0,
        edgeCount: 0,
        nodeTypes: {},
        edgeTypes: {}
      }
    });
  }
}

async function fetchGraphData(maxNodes: number, includeRelationships: string[]) {
  const relFilter = includeRelationships.map(rel => `'${rel}'`).join(', ');
  
  const query = `
    MATCH (n)
    WITH n LIMIT ${maxNodes}
    OPTIONAL MATCH (n)-[r]->(m)
    WHERE type(r) IN [${relFilter}]
    RETURN 
        collect(DISTINCT {
            id: elementId(n),
            labels: labels(n),
            properties: properties(n)
        }) + collect(DISTINCT {
            id: elementId(m),
            labels: labels(m),
            properties: properties(m)
        }) as nodes,
        collect(DISTINCT {
            source: elementId(n),
            target: elementId(m),
            type: type(r),
            properties: properties(r)
        }) as edges
  `;

  const result = await executeQuery(query);
  const data = result[0];
  
  if (!data) {
    return {
      nodes: [],
      edges: [],
      stats: {
        nodeCount: 0,
        edgeCount: 0,
        nodeTypes: {},
        edgeTypes: {}
      }
    };
  }

  // Process nodes - filter out nulls and deduplicate
  const allNodes = data.nodes || [];
  const edges = data.edges || [];

  const filteredNodes = allNodes.filter((node: any) => node.id !== null);
  
  // Deduplicate nodes by ID
  const seenIds = new Set();
  const uniqueNodes = filteredNodes.filter((node: any) => {
    if (seenIds.has(node.id)) {
      return false;
    }
    seenIds.add(node.id);
    return true;
  });

  // Filter edges to only include those with valid source and target
  const validEdges = edges.filter((edge: any) => 
    edge.source !== null && edge.target !== null
  );

  // Transform to vis-network format
  const nodes = uniqueNodes.map((node: any) => {
    const nodeType = node.labels && node.labels.length > 0 ? node.labels[0] : 'Unknown';
    const label = node.properties?.id || node.properties?.title || String(node.id);
    
    return {
      id: String(node.id),
      label: label.length > 20 ? label.substring(0, 17) + '...' : label,
      type: nodeType,
      properties: node.properties
    };
  });

  const formattedEdges = validEdges.map((edge: any, index: number) => ({
    id: `edge_${index}`,
    from: String(edge.source),
    to: String(edge.target),
    label: edge.type,
    type: edge.type,
    properties: edge.properties
  }));

  // Calculate statistics
  const nodeTypes: Record<string, number> = {};
  const edgeTypes: Record<string, number> = {};

  nodes.forEach(node => {
    nodeTypes[node.type] = (nodeTypes[node.type] || 0) + 1;
  });

  formattedEdges.forEach(edge => {
    edgeTypes[edge.type] = (edgeTypes[edge.type] || 0) + 1;
  });

  return {
    nodes,
    edges: formattedEdges,
    stats: {
      nodeCount: nodes.length,
      edgeCount: formattedEdges.length,
      nodeTypes,
      edgeTypes
    }
  };
}
