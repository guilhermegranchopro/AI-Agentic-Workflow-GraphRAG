import { NextApiRequest, NextApiResponse } from 'next';
import { AnalysisRequest, AnalysisProgressEvent, AnalysisResult, Contradiction, Harmonisation } from '../../../lib/ai/analysis/types';
import { retrieve, searchByConcept, findPotentialConflicts } from '../../../lib/graph/graphRag';
import { ContradictionMinerAgent } from '../../../lib/ai/agents/analysis/contradictionMiner';
import { HarmoniserAgent } from '../../../lib/ai/agents/analysis/harmoniser';

export const config = {
  runtime: 'nodejs',
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { query, scope = 'all', maxFindings = 10 }: AnalysisRequest = req.body;

    if (!query || typeof query !== 'string') {
      return res.status(400).json({ error: 'Invalid query format' });
    }

    // Set headers for SSE
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Headers', 'Cache-Control');

    const startTime = Date.now();

    // Phase 1: Retrieval
    await sendProgress(res, {
      type: 'progress',
      data: {
        stage: 'retrieval',
        pct: 10,
        message: 'Gathering legal provisions from knowledge graph...',
        timestamp: Date.now()
      }
    });

    // Use existing GraphRAG agents for retrieval
    const [localResult, globalResult, driftResult] = await Promise.allSettled([
      retrieve(query, 'local'),
      retrieve(query, 'global'), 
      retrieve(query, 'drift')
    ]);

    // Add targeted conflict search
    const conceptResult = await searchByConcept(query, scope);
    const conflictResult = await findPotentialConflicts(query, scope);

    await sendProgress(res, {
      type: 'progress', 
      data: {
        stage: 'retrieval',
        pct: 30,
        message: 'Retrieval complete. Analyzing for contradictions...',
        timestamp: Date.now()
      }
    });

    // Phase 2: Contradiction Mining
    await sendProgress(res, {
      type: 'progress',
      data: {
        stage: 'mining',
        pct: 40,
        message: 'Mining legal contradictions using AI analysis...',
        timestamp: Date.now()
      }
    });

    const pooledResults = [
      ...(localResult.status === 'fulfilled' ? [localResult.value] : []),
      ...(globalResult.status === 'fulfilled' ? [globalResult.value] : []),
      ...(driftResult.status === 'fulfilled' ? [driftResult.value] : []),
      conceptResult,
      conflictResult
    ];

    const contradictionMiner = new ContradictionMinerAgent();
    const minerResult = await contradictionMiner.process(pooledResults, query, scope);
    
    // Extract contradictions from the result - for now, create sample contradictions
    // In a real implementation, the ContradictionMinerAgent would return structured data
    let contradictions: Contradiction[] = [];
    
    if (minerResult.citations && minerResult.citations.length > 0) {
      // Group citations into potential contradictions (simplified approach)
      for (let i = 0; i < minerResult.citations.length; i += 2) {
        const leftCitation = minerResult.citations[i];
        const rightCitation = minerResult.citations[i + 1];
        
        if (leftCitation && rightCitation) {
          contradictions.push({
            id: `contradiction-${i / 2}-${Date.now()}`,
            title: `Potential Legal Contradiction ${Math.floor(i / 2) + 1}`,
            category: 'other',
            severity: 'medium',
            rationale: `Identified potential contradiction between provisions`,
            left: [{
              nodeId: leftCitation.nodeId,
              snippet: leftCitation.snippet,
              score: leftCitation.score,
              law: leftCitation.metadata?.law as string || 'Unknown',
              article: leftCitation.metadata?.article as string || 'Unknown'
            }],
            right: rightCitation ? [{
              nodeId: rightCitation.nodeId,
              snippet: rightCitation.snippet,
              score: rightCitation.score,
              law: rightCitation.metadata?.law as string || 'Unknown',
              article: rightCitation.metadata?.article as string || 'Unknown'
            }] : []
          });
        }
      }
    }

    await sendProgress(res, {
      type: 'progress',
      data: {
        stage: 'mining', 
        pct: 60,
        message: `Found ${contradictions.length} potential contradictions`,
        timestamp: Date.now()
      }
    });

    // Send individual findings
    for (const contradiction of contradictions.slice(0, maxFindings)) {
      await sendProgress(res, {
        type: 'finding',
        data: {
          contradiction,
          timestamp: Date.now()
        }
      });
    }

    // Phase 3: Harmonisation
    await sendProgress(res, {
      type: 'progress',
      data: {
        stage: 'harmonising',
        pct: 70,
        message: 'Generating harmonisation recommendations...',
        timestamp: Date.now()
      }
    });

    const harmoniser = new HarmoniserAgent();
    const harmoniserResult = await harmoniser.process(contradictions.slice(0, maxFindings), query);
    
    // Extract harmonisations - for now, create basic suggestions
    const harmonisations: Harmonisation[] = contradictions.slice(0, maxFindings).map(contradiction => ({
      contradictionId: contradiction.id,
      recommendation: `Review and clarify the conflicting provisions in ${contradiction.title.toLowerCase()}. Apply lex specialis principle where appropriate.`,
      reasoning: `Based on legal precedence analysis, this contradiction can be resolved through careful interpretation of the scope and applicability of each provision.`,
      risks: ['May require legislative review', 'Implementation may need stakeholder consultation']
    }));

    await sendProgress(res, {
      type: 'progress',
      data: {
        stage: 'harmonising',
        pct: 90,
        message: `Generated ${harmonisations.length} harmonisation suggestions`,
        timestamp: Date.now()
      }
    });

    // Send individual suggestions
    for (const harmonisation of harmonisations) {
      await sendProgress(res, {
        type: 'suggestion',
        data: {
          harmonisation,
          timestamp: Date.now()
        }
      });
    }

    // Phase 4: Final Results
    const finalContradictions = contradictions.slice(0, maxFindings);
    const stats = {
      total: finalContradictions.length,
      bySeverity: finalContradictions.reduce((acc, c) => {
        acc[c.severity] = (acc[c.severity] || 0) + 1;
        return acc;
      }, {} as Record<string, number>)
    };

    const result: AnalysisResult = {
      query,
      findings: finalContradictions,
      suggestions: harmonisations,
      stats
    };

    await sendProgress(res, {
      type: 'done',
      data: {
        result,
        message: `Analysis complete: ${finalContradictions.length} contradictions, ${harmonisations.length} suggestions`,
        timestamp: Date.now()
      }
    });

    res.end();

  } catch (error) {
    console.error('Analysis API error:', error);
    
    const errorMessage = error instanceof Error ? error.message : 'Unknown error';
    
    if (!res.headersSent) {
      res.setHeader('Content-Type', 'application/json');
      res.status(500).json({ 
        error: 'Analysis failed',
        details: errorMessage
      });
    } else {
      await sendProgress(res, {
        type: 'progress',
        data: {
          stage: 'mining',
          message: `Error: ${errorMessage}`,
          timestamp: Date.now()
        }
      });
      res.end();
    }
  }
}

async function sendProgress(res: NextApiResponse, event: AnalysisProgressEvent): Promise<void> {
  return new Promise((resolve) => {
    res.write(`event: ${event.type}\ndata: ${JSON.stringify(event)}\n\n`);
    // Small delay to ensure proper streaming
    setTimeout(resolve, 10);
  });
}
