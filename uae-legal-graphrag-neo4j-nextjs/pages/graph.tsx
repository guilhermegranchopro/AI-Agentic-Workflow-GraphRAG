import React, { useState, useEffect, useRef } from 'react';
import Layout from '@/components/Layout';
import { Network, Share2, Search, Filter, ZoomIn, ZoomOut, RotateCcw, Download } from 'lucide-react';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, any>;
  group?: number;
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

const GraphVisualizationPage: React.FC = () => {
  const [query, setQuery] = useState('');
  const [nodeLimit, setNodeLimit] = useState(50);
  const [loading, setLoading] = useState(false);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<GraphEdge | null>(null);
  const [networkInstance, setNetworkInstance] = useState<any>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const fetchGraphData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/graph-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query.trim() || undefined,
          limit: nodeLimit,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch graph data');
      }

      setGraphData(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Load vis-network dynamically
    const loadVisNetwork = async () => {
      if (typeof window !== 'undefined' && graphData) {
        try {
          const vis = await import('vis-network');
          
          if (containerRef.current) {
            // Prepare nodes with vis-network format
            const nodes = new vis.DataSet(
              graphData.nodes.map(node => ({
                id: node.id,
                label: node.label,
                group: node.type,
                title: `Type: ${node.type}\nID: ${node.id}`,
                color: getNodeColor(node.type),
                font: { size: 12, color: '#333' },
                borderWidth: 2,
                borderWidthSelected: 3,
              }))
            );

            // Prepare edges with vis-network format
            const edges = new vis.DataSet(
              graphData.edges.map(edge => ({
                id: edge.id,
                from: edge.from,
                to: edge.to,
                label: edge.label,
                title: `Type: ${edge.type}\nFrom: ${edge.from}\nTo: ${edge.to}`,
                color: { color: '#666666', highlight: '#333333' },
                arrows: { to: { enabled: true, scaleFactor: 0.8 } },
                font: { size: 10, align: 'middle' },
                smooth: { enabled: true, type: 'curvedCW', roundness: 0.2 },
              }))
            );

            const data = { nodes, edges };

            const options = {
              layout: {
                improvedLayout: true,
                hierarchical: false,
              },
              physics: {
                enabled: true,
                stabilization: { iterations: 100 },
                barnesHut: {
                  gravitationalConstant: -2000,
                  centralGravity: 0.1,
                  springLength: 200,
                  springConstant: 0.05,
                  damping: 0.09,
                },
              },
              interaction: {
                hover: true,
                selectConnectedEdges: false,
                tooltipDelay: 300,
              },
              nodes: {
                shape: 'dot',
                size: 15,
                font: { size: 12, color: '#333333' },
                borderWidth: 2,
                shadow: true,
              },
              edges: {
                width: 2,
                shadow: true,
                smooth: {
                  enabled: true,
                  type: 'curvedCW',
                  roundness: 0.2,
                },
              },
              groups: {
                PERSON: { color: { background: '#FFB6C1', border: '#FF69B4' } },
                ORGANIZATION: { color: { background: '#87CEEB', border: '#4682B4' } },
                LOCATION: { color: { background: '#98FB98', border: '#32CD32' } },
                EVENT: { color: { background: '#DDA0DD', border: '#9370DB' } },
                DOCUMENT: { color: { background: '#F0E68C', border: '#DAA520' } },
                LAW: { color: { background: '#FFA07A', border: '#FF6347' } },
                CONCEPT: { color: { background: '#D3D3D3', border: '#A9A9A9' } },
              },
            };

            const network = new vis.Network(containerRef.current, data, options);

            // Event listeners
            network.on('selectNode', (params) => {
              if (params.nodes.length > 0) {
                const nodeId = params.nodes[0];
                const node = graphData.nodes.find(n => n.id === nodeId);
                setSelectedNode(node || null);
                setSelectedEdge(null);
              }
            });

            network.on('selectEdge', (params) => {
              if (params.edges.length > 0) {
                const edgeId = params.edges[0];
                const edge = graphData.edges.find(e => e.id === edgeId);
                setSelectedEdge(edge || null);
                setSelectedNode(null);
              }
            });

            network.on('deselectNode', () => {
              setSelectedNode(null);
            });

            network.on('deselectEdge', () => {
              setSelectedEdge(null);
            });

            setNetworkInstance(network);
          }
        } catch (error) {
          console.error('Failed to load vis-network:', error);
          setError('Failed to load graph visualization library');
        }
      }
    };

    loadVisNetwork();
  }, [graphData]);

  const getNodeColor = (type: string) => {
    const colors: Record<string, string> = {
      PERSON: '#FFB6C1',
      ORGANIZATION: '#87CEEB',
      LOCATION: '#98FB98',
      EVENT: '#DDA0DD',
      DOCUMENT: '#F0E68C',
      LAW: '#FFA07A',
      CONCEPT: '#D3D3D3',
    };
    return colors[type] || '#D3D3D3';
  };

  const handleZoomIn = () => {
    if (networkInstance) {
      const scale = networkInstance.getScale();
      networkInstance.moveTo({ scale: scale * 1.2 });
    }
  };

  const handleZoomOut = () => {
    if (networkInstance) {
      const scale = networkInstance.getScale();
      networkInstance.moveTo({ scale: scale * 0.8 });
    }
  };

  const handleFit = () => {
    if (networkInstance) {
      networkInstance.fit();
    }
  };

  const handleReset = () => {
    setQuery('');
    setNodeLimit(50);
    setGraphData(null);
    setSelectedNode(null);
    setSelectedEdge(null);
    setError(null);
  };

  return (
    <Layout title="Graph Visualization - UAE Legal GraphRAG">
      <div className="animate-fade-in">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-4">
            <Share2 className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">Graph Visualization</h1>
          </div>
          <p className="text-lg text-gray-600">
            Interactive exploration of the legal knowledge graph
          </p>
        </div>

        {/* Controls */}
        <div className="card mb-8">
          <div className="flex flex-col lg:flex-row lg:items-end lg:space-x-4 space-y-4 lg:space-y-0">
            <div className="flex-grow">
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
                Search Query (optional)
              </label>
              <input
                type="text"
                id="query"
                className="input-field"
                placeholder="Enter search terms to filter nodes..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
            
            <div className="w-full lg:w-48">
              <label htmlFor="nodeLimit" className="block text-sm font-medium text-gray-700 mb-2">
                <Filter className="inline h-4 w-4 mr-1" />
                Node Limit
              </label>
              <select
                id="nodeLimit"
                className="select-field"
                value={nodeLimit}
                onChange={(e) => setNodeLimit(parseInt(e.target.value))}
              >
                <option value={25}>25 nodes</option>
                <option value={50}>50 nodes</option>
                <option value={100}>100 nodes</option>
                <option value={200}>200 nodes</option>
              </select>
            </div>

            <div className="flex space-x-2">
              <button
                onClick={fetchGraphData}
                disabled={loading}
                className="btn-primary px-6 py-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Loading...</span>
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4" />
                    <span>Load Graph</span>
                  </>
                )}
              </button>

              <button
                onClick={handleReset}
                className="btn-secondary px-4 py-2 flex items-center space-x-2"
              >
                <RotateCcw className="h-4 w-4" />
                <span>Reset</span>
              </button>
            </div>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="card border-red-200 bg-red-50 mb-8">
            <div className="flex items-center space-x-2">
              <div className="h-4 w-4 bg-red-500 rounded-full"></div>
              <h3 className="text-lg font-semibold text-red-800">Error</h3>
            </div>
            <p className="mt-2 text-red-700">{error}</p>
          </div>
        )}

        {/* Graph Container */}
        {graphData && (
          <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
            {/* Main Graph */}
            <div className="xl:col-span-3">
              <div className="card p-0 overflow-hidden">
                <div className="flex items-center justify-between p-4 border-b border-gray-200">
                  <h3 className="text-lg font-semibold text-gray-900">
                    <Network className="inline h-5 w-5 mr-2" />
                    Knowledge Graph
                  </h3>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={handleZoomIn}
                      className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
                      title="Zoom In"
                    >
                      <ZoomIn className="h-4 w-4" />
                    </button>
                    <button
                      onClick={handleZoomOut}
                      className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
                      title="Zoom Out"
                    >
                      <ZoomOut className="h-4 w-4" />
                    </button>
                    <button
                      onClick={handleFit}
                      className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded"
                      title="Fit to View"
                    >
                      <RotateCcw className="h-4 w-4" />
                    </button>
                  </div>
                </div>
                <div
                  ref={containerRef}
                  className="w-full h-96 lg:h-[600px]"
                  style={{ background: '#fafafa' }}
                />
              </div>
            </div>

            {/* Sidebar */}
            <div className="xl:col-span-1 space-y-6">
              {/* Graph Statistics */}
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">📊 Graph Statistics</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Nodes:</span>
                    <span className="font-medium">{graphData.stats.nodeCount}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Edges:</span>
                    <span className="font-medium">{graphData.stats.edgeCount}</span>
                  </div>
                  
                  <div className="pt-3 border-t border-gray-200">
                    <h4 className="font-medium text-gray-900 mb-2">Node Types:</h4>
                    <div className="space-y-2">
                      {Object.entries(graphData.stats.nodeTypes).map(([type, count]) => (
                        <div key={type} className="flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <div
                              className="w-3 h-3 rounded-full border"
                              style={{ backgroundColor: getNodeColor(type) }}
                            />
                            <span className="text-xs text-gray-600">{type}</span>
                          </div>
                          <span className="text-xs font-medium">{count}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Selected Node */}
              {selectedNode && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">🎯 Selected Node</h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <span className="text-gray-600">ID:</span>
                      <p className="font-medium break-all">{selectedNode.id}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Label:</span>
                      <p className="font-medium">{selectedNode.label}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Type:</span>
                      <p className="font-medium">{selectedNode.type}</p>
                    </div>
                    {selectedNode.properties && Object.keys(selectedNode.properties).length > 0 && (
                      <div>
                        <span className="text-gray-600">Properties:</span>
                        <div className="mt-1 space-y-1">
                          {Object.entries(selectedNode.properties).map(([key, value]) => (
                            <div key={key} className="text-xs">
                              <span className="font-medium">{key}:</span> {String(value)}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Selected Edge */}
              {selectedEdge && (
                <div className="card">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">🔗 Selected Edge</h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <span className="text-gray-600">From:</span>
                      <p className="font-medium break-all">{selectedEdge.from}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">To:</span>
                      <p className="font-medium break-all">{selectedEdge.to}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Type:</span>
                      <p className="font-medium">{selectedEdge.type}</p>
                    </div>
                    <div>
                      <span className="text-gray-600">Label:</span>
                      <p className="font-medium">{selectedEdge.label}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default GraphVisualizationPage;
