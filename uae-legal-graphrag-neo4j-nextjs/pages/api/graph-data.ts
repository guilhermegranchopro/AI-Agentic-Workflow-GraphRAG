import { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

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

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { query, limit = 50 } = req.body;

  // Path to the Python backend
  const pythonBackendPath = path.join(process.cwd(), 'python-backend');
  const scriptPath = path.join(pythonBackendPath, 'graph', 'queries.py');

  const pythonProcess = spawn('python', [
    '-c',
    `
import sys
import os
import json
sys.path.append('${pythonBackendPath.replace(/\\/g, '\\\\')}')

try:
    from graph.tools import get_graph_data
    
    # Get graph data
    result = get_graph_data(
        query="${query || ''}",
        limit=${limit}
    )
    
    print(json.dumps(result, default=str))
except Exception as e:
    error_result = {
        "error": str(e),
        "nodes": [],
        "edges": [],
        "stats": {
            "nodeCount": 0,
            "edgeCount": 0,
            "nodeTypes": {},
            "edgeTypes": {}
        }
    }
    print(json.dumps(error_result))
    `
  ], {
    cwd: pythonBackendPath,
    env: { ...process.env, PYTHONPATH: pythonBackendPath }
  });

  let output = '';
  let errorOutput = '';

  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  pythonProcess.on('close', (code) => {
    try {
      if (code === 0 && output.trim()) {
        const result = JSON.parse(output.trim());
        
        if (result.error) {
          console.error('Python script error:', result.error);
          return res.status(500).json({ 
            error: result.error,
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
        
        // Ensure we have the required structure
        const graphData: GraphData = {
          nodes: result.nodes || [],
          edges: result.edges || [],
          stats: {
            nodeCount: result.stats?.nodeCount || (result.nodes?.length || 0),
            edgeCount: result.stats?.edgeCount || (result.edges?.length || 0),
            nodeTypes: result.stats?.nodeTypes || {},
            edgeTypes: result.stats?.edgeTypes || {}
          }
        };
        
        res.status(200).json(graphData);
      } else {
        console.error('Python process failed:', errorOutput);
        res.status(500).json({ 
          error: errorOutput || 'Failed to fetch graph data',
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
    } catch (parseError) {
      console.error('Failed to parse Python output:', parseError);
      console.error('Raw output:', output);
      console.error('Error output:', errorOutput);
      res.status(500).json({ 
        error: 'Failed to parse graph data response',
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
  });

  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python process:', error);
    res.status(500).json({ 
      error: 'Failed to start graph data process',
      nodes: [],
      edges: [],
      stats: {
        nodeCount: 0,
        edgeCount: 0,
        nodeTypes: {},
        edgeTypes: {}
      }
    });
  });
}
