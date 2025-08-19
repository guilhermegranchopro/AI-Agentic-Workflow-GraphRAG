import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

interface DatabaseStats {
  total_documents: number;
  total_entities: number;
  total_relationships: number;
  communities: number;
  last_updated: string;
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<DatabaseStats | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const pythonBackendPath = path.join(process.cwd(), 'python-backend');

  const pythonProcess = spawn('python', [
    '-c',
    `
import sys
import os
import json
sys.path.append('${pythonBackendPath.replace(/\\/g, '\\\\')}')

try:
    # Mock database statistics
    stats = {
        "total_documents": 1247,
        "total_entities": 8934,
        "total_relationships": 15627,
        "communities": 42,
        "last_updated": "2025-08-19T10:30:00Z"
    }
    
    print(json.dumps(stats))
except Exception as e:
    error_result = {
        "error": str(e)
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
          return res.status(500).json({ error: result.error });
        }
        
        const formattedStats: DatabaseStats = {
          total_documents: result.total_documents || 0,
          total_entities: result.total_entities || 0,
          total_relationships: result.total_relationships || 0,
          communities: result.communities || 0,
          last_updated: result.last_updated || new Date().toISOString()
        };
        
        res.status(200).json(formattedStats);
      } else {
        console.error('Python process failed:', errorOutput);
        res.status(500).json({ 
          error: errorOutput || 'Failed to fetch database statistics'
        });
      }
    } catch (parseError) {
      console.error('Failed to parse Python output:', parseError);
      res.status(500).json({ 
        error: 'Failed to parse database statistics'
      });
    }
  });

  pythonProcess.on('error', (error) => {
    console.error('Failed to start Python process:', error);
    res.status(500).json({ 
      error: 'Failed to start statistics process'
    });
  });
}
      total_documents: stats.total_documents || 0,
      total_entities: stats.total_entities || 0,
      total_relationships: stats.total_relationships || 0,
      communities: stats.communities || 0,
      last_updated: stats.last_updated || new Date().toISOString()
    };

    res.status(200).json(formattedStats);

  } catch (error) {
    console.error('Database stats error:', error);
    res.status(500).json({ 
      error: 'Failed to fetch database statistics' 
    });
  }
}
