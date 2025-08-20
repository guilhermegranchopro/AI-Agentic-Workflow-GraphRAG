import { useState, useEffect, useRef } from 'react';
import { Network } from 'vis-network/standalone';
import Layout from '../components/Layout';

interface GraphNode {
  id: string;
  label: string;
  group: string;
  properties?: Record<string, unknown>;
}

interface GraphEdge {
  source: string;
  target: string;
  type: string;
  properties?: Record<string, unknown>;
}

interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  stats: {
    nodeCount: number;
    edgeCount: number;
    timestamp: string;
  };
}

export default function Graph() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const networkRef = useRef<HTMLDivElement>(null);
  const networkInstance = useRef<Network | null>(null);

  useEffect(() => {
    fetchGraphData();
  }, []);

  useEffect(() => {
    if (graphData && networkRef.current && !networkInstance.current) {
      initializeNetwork();
    }
  }, [graphData]);

  const fetchGraphData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/graph');
      
      if (!response.ok) {
        throw new Error('Failed to fetch graph data');
      }
      
      const data = await response.json();
      setGraphData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const initializeNetwork = () => {
    if (!graphData || !networkRef.current) return;

    // Transform data for vis-network
    const nodes = graphData.nodes.map(node => ({
      id: node.id,
      label: node.label,
      group: node.group,
      title: `${node.group}: ${node.label}`, // Tooltip
      color: getNodeColor(node.group),
      font: { color: '#ffffff', size: 12 },
    }));

    const edges = graphData.edges.map(edge => ({
      from: edge.source,
      to: edge.target,
      label: edge.type,
      arrows: 'to',
      color: { color: '#6366f1', opacity: 0.6 },
      font: { color: '#9ca3af', size: 10 },
    }));

    const data = { nodes, edges };

    const options = {
      nodes: {
        shape: 'dot',
        size: 20,
        font: {
          size: 12,
          color: '#ffffff'
        },
        borderWidth: 2,
        shadow: true,
      },
      edges: {
        width: 2,
        shadow: true,
        smooth: {
          type: 'continuous',
          roundness: 0.2,
        },
      },
      physics: {
        enabled: true,
        stabilization: { iterations: 100 },
        barnesHut: {
          gravitationalConstant: -2000,
          centralGravity: 0.3,
          springLength: 95,
          springConstant: 0.04,
          damping: 0.09,
        },
      },
      interaction: {
        hover: true,
        selectConnectedEdges: false,
      },
      layout: {
        improvedLayout: false,
      },
    };

    networkInstance.current = new Network(networkRef.current, data, options);

    // Add event listeners
    networkInstance.current.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = graphData.nodes.find(n => n.id === nodeId);
        setSelectedNode(node || null);
      } else {
        setSelectedNode(null);
      }
    });

    networkInstance.current.on('hoverNode', () => {
      networkRef.current!.style.cursor = 'pointer';
    });

    networkInstance.current.on('blurNode', () => {
      networkRef.current!.style.cursor = 'default';
    });
  };

  const getNodeColor = (group: string): string => {
    const colors: Record<string, string> = {
      Document: '#ef4444',
      Entity: '#10b981',
      Concept: '#f59e0b',
      Relationship: '#8b5cf6',
      default: '#6b7280',
    };
    return colors[group] || colors.default;
  };

  const focusNode = () => {
    if (!networkInstance.current || !searchTerm) return;
    
    const node = graphData?.nodes.find(n => 
      n.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      n.label.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (node) {
      networkInstance.current.focus(node.id, {
        scale: 1.5,
        animation: { duration: 1000, easingFunction: 'easeInOutQuad' }
      });
      setSelectedNode(node);
    }
  };

  const resetView = () => {
    if (!networkInstance.current) return;
    networkInstance.current.fit({
      animation: { duration: 1000, easingFunction: 'easeInOutQuad' }
    });
    setSelectedNode(null);
  };

  if (loading) {
    return (
      <Layout title="Graph Visualization - UAE Legal GraphRAG">
        <div className="flex items-center justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
          <span className="ml-4 text-gray-300">Loading knowledge graph...</span>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Graph Visualization - UAE Legal GraphRAG">
        <div className="text-center py-12">
          <div className="text-red-400 mb-4">❌ Error loading graph</div>
          <p className="text-gray-400 mb-4">{error}</p>
          <button
            onClick={fetchGraphData}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Graph Visualization - UAE Legal GraphRAG">
      <div className="space-y-6">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-3xl font-bold text-white mb-2">
            🔗 Knowledge Graph
          </h1>
          <p className="text-gray-300">
            Interactive exploration of the legal knowledge graph
          </p>
          {graphData && (
            <div className="flex justify-center space-x-6 mt-4 text-sm text-gray-400">
              <span>📊 {graphData.stats.nodeCount} nodes</span>
              <span>🔗 {graphData.stats.edgeCount} edges</span>
              <span>🕒 {new Date(graphData.stats.timestamp).toLocaleTimeString()}</span>
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="bg-gray-800/60 backdrop-blur-sm rounded-xl p-4 border border-gray-700/50">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex-1 min-w-64">
              <div className="flex">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search nodes by ID or label..."
                  className="flex-1 bg-gray-900/50 border border-gray-600/50 rounded-l-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50"
                  onKeyPress={(e) => e.key === 'Enter' && focusNode()}
                />
                <button
                  onClick={focusNode}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-r-lg transition-colors"
                >
                  🔍
                </button>
              </div>
            </div>
            <button
              onClick={resetView}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
            >
              🎯 Reset View
            </button>
            <button
              onClick={fetchGraphData}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              🔄 Refresh
            </button>
          </div>
        </div>

        {/* Main Graph Area */}
        <div className="bg-gray-900/50 rounded-xl border border-gray-700/50 overflow-hidden">
          <div className="flex">
            {/* Graph Canvas */}
            <div className="flex-1">
              <div
                ref={networkRef}
                className="w-full h-[600px] bg-gray-900"
                style={{ cursor: 'default' }}
              />
            </div>

            {/* Node Details Panel */}
            {selectedNode && (
              <div className="w-80 bg-gray-800/90 backdrop-blur-sm border-l border-gray-700/50 p-4 overflow-y-auto">
                <h3 className="text-lg font-semibold text-white mb-3">
                  📋 Node Details
                </h3>
                
                <div className="space-y-3">
                  <div>
                    <label className="text-xs text-gray-400 uppercase tracking-wider">ID</label>
                    <div className="text-white font-mono text-sm bg-gray-900/50 p-2 rounded">
                      {selectedNode.id}
                    </div>
                  </div>
                  
                  <div>
                    <label className="text-xs text-gray-400 uppercase tracking-wider">Label</label>
                    <div className="text-white text-sm">{selectedNode.label}</div>
                  </div>
                  
                  <div>
                    <label className="text-xs text-gray-400 uppercase tracking-wider">Type</label>
                    <div className="text-white text-sm">
                      <span 
                        className="inline-block px-2 py-1 rounded text-xs font-medium"
                        style={{ backgroundColor: getNodeColor(selectedNode.group) + '40', color: getNodeColor(selectedNode.group) }}
                      >
                        {selectedNode.group}
                      </span>
                    </div>
                  </div>

                  {selectedNode.properties && Object.keys(selectedNode.properties).length > 0 && (
                    <div>
                      <label className="text-xs text-gray-400 uppercase tracking-wider">Properties</label>
                      <div className="bg-gray-900/50 p-2 rounded text-xs text-gray-300 font-mono max-h-32 overflow-y-auto">
                        <pre>{JSON.stringify(selectedNode.properties, null, 2)}</pre>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Legend */}
        <div className="bg-gray-800/60 backdrop-blur-sm rounded-xl p-4 border border-gray-700/50">
          <h4 className="text-white font-semibold mb-3">🎨 Node Types</h4>
          <div className="flex flex-wrap gap-4">
            {['Document', 'Entity', 'Concept', 'Relationship'].map(type => (
              <div key={type} className="flex items-center space-x-2">
                <div 
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: getNodeColor(type) }}
                />
                <span className="text-gray-300 text-sm">{type}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
