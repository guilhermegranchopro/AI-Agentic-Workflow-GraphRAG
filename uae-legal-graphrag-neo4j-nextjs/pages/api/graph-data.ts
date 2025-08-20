import { NextApiRequest, NextApiResponse } from 'next';
import { runQuery } from '../../lib/graph/neo4j';
import { getNeo4jConfig } from '../../lib/config';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, any>;
}

interface GraphEdge {
  id: string;
  from: string;
  to: string;
  label: string;
  type: string;
  properties?: Record<string, any>;
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

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Check Neo4j configuration
    try {
      const neo4jConfig = getNeo4jConfig();
      // Config is successful if we reach here
    } catch (configError) {
      return res.status(503).json({ 
        error: 'Neo4j not configured. Please check your .env file.',
        details: configError instanceof Error ? configError.message : 'Configuration error',
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

    // Get query parameters with defaults
    const maxNodes = parseInt(req.query.max_nodes as string) || 50;
    const includeRelationships = req.query.relationships 
      ? (req.query.relationships as string).split(',')
      : ["HAS_PROVISION", "CITES", "INTERPRETED_BY", "AMENDED_BY"];

    // Fetch graph data using the same logic as Streamlit
    const graphData = await fetchGraphData(maxNodes, includeRelationships);
    
    res.status(200).json(graphData);
  } catch (error) {
    console.error('Graph data error:', error);
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

async function fetchGraphData(maxNodes: number, includeRelationships: string[]): Promise<GraphData> {
  const relFilter = includeRelationships.map(rel => `'${rel}'`).join(', ');
  
  // Neo4j query using the same logic as Streamlit
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

  const result = await runQuery(query);
  const data = result.records[0];
  
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
  const allNodes = data.get('nodes') || [];
  const edges = data.get('edges') || [];

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
  const nodes: GraphNode[] = uniqueNodes.map((node: any) => {
    const nodeType = node.labels && node.labels.length > 0 ? node.labels[0] : 'Unknown';
    const label = node.properties?.id || node.properties?.title || String(node.id);
    
    return {
      id: String(node.id),
      label: label.length > 20 ? label.substring(0, 17) + '...' : label,
      type: nodeType,
      properties: node.properties
    };
  });

  const formattedEdges: GraphEdge[] = validEdges.map((edge: any, index: number) => ({
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
