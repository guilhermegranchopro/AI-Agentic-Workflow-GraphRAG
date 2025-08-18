import type { NextApiRequest, NextApiResponse } from 'next';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy';
  database: boolean;
  embeddings: boolean;
  ai_service: boolean;
  message?: string;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<HealthCheckResponse>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({
      status: 'unhealthy',
      database: false,
      embeddings: false,
      ai_service: false,
      message: 'Method not allowed'
    });
  }

  try {
    // Path to Python backend
    const pythonBackendPath = path.join(process.cwd(), 'python-backend');
    
    // Test database connectivity using existing Python backend
    const dbTestCommand = `cd "${pythonBackendPath}" && python -c "
import sys
import os
sys.path.append('.')
from db import db
try:
    result = db.health_check()
    print('DB_OK' if result.get('status') == 'connected' else 'DB_ERROR')
except Exception as e:
    print('DB_ERROR')
"`;

    // Test AI service using existing Python backend
    const aiTestCommand = `cd "${pythonBackendPath}" && python -c "
import sys
import os
sys.path.append('.')
try:
    from embeddings.azure_openai import AzureOpenAIEmbeddings
    embeddings = AzureOpenAIEmbeddings()
    test_embed = embeddings.embed_query('test')
    print('AI_OK' if test_embed and len(test_embed) > 0 else 'AI_ERROR')
except Exception as e:
    print('AI_ERROR')
"`;

    const [dbResult, aiResult] = await Promise.allSettled([
      execAsync(dbTestCommand),
      execAsync(aiTestCommand)
    ]);

    const database = dbResult.status === 'fulfilled' && 
                    dbResult.value.stdout.trim() === 'DB_OK';
    
    const ai_service = aiResult.status === 'fulfilled' && 
                      aiResult.value.stdout.trim() === 'AI_OK';
    
    // Embeddings service is same as AI service in our case
    const embeddings = ai_service;

    const allHealthy = database && embeddings && ai_service;

    res.status(200).json({
      status: allHealthy ? 'healthy' : 'unhealthy',
      database,
      embeddings,
      ai_service,
      message: allHealthy ? 'All systems operational' : 'Some services unavailable'
    });

  } catch (error) {
    console.error('Health check error:', error);
    res.status(500).json({
      status: 'unhealthy',
      database: false,
      embeddings: false,
      ai_service: false,
      message: 'Health check failed'
    });
  }
}
