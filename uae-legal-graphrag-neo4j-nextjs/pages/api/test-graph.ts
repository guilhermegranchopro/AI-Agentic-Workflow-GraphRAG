import type { NextApiRequest, NextApiResponse } from 'next';

// Simple test data that should definitely work with vis-network
const testGraphData = {
  nodes: [
    { id: '1', label: 'Node 1', color: '#e74c3c' },
    { id: '2', label: 'Node 2', color: '#3498db' },
    { id: '3', label: 'Node 3', color: '#2ecc71' }
  ],
  edges: [
    { from: '1', to: '2', label: 'connects' },
    { from: '2', to: '3', label: 'links' }
  ]
};

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  console.log('Test graph data endpoint called');
  
  // Return simple test data
  res.status(200).json({
    nodes: testGraphData.nodes,
    edges: testGraphData.edges,
    stats: {
      nodeCount: testGraphData.nodes.length,
      edgeCount: testGraphData.edges.length,
      nodeTypes: { 'TestNode': testGraphData.nodes.length },
      edgeTypes: { 'TestEdge': testGraphData.edges.length }
    }
  });
}
