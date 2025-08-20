import type { NextApiRequest, NextApiResponse } from 'next';
import { getAzureOpenAIConfig } from '../../lib/config';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    console.log('Testing Azure OpenAI configuration...');
    
    // This will throw if the configuration is missing
    const config = getAzureOpenAIConfig();
    
    console.log('Azure OpenAI Config test passed!');
    console.log('Available config keys:', Object.keys(config));
    
    res.status(200).json({
      success: true,
      message: 'Azure OpenAI configuration is valid',
      configKeys: Object.keys(config),
      endpoint: config.AZURE_OPENAI_ENDPOINT,
      deployment: config.AZURE_OPENAI_DEPLOYMENT,
      apiVersion: config.AZURE_OPENAI_API_VERSION
    });
  } catch (error) {
    console.error('Azure OpenAI Config test failed:', error);
    
    res.status(500).json({
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      // @ts-ignore
      present: error?.present || {}
    });
  }
}
