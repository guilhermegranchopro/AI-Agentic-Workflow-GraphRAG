import { useEffect, useRef, useState } from 'react';
import Layout from '../components/Layout';

interface GraphNode {
  id: string;
  label: string;
  type: string;
  properties?: Record<string, unknown>;
}

interface GraphEdge {
  id: string;
  from: string;
  to: string;
  label: string;
  type: string;
  properties?: Record<string, unknown>;
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

export default function GraphSimple() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const networkRef = useRef<HTMLDivElement>(null);
  const networkInstance = useRef<any>(null);

  // Fetch graph data
  const fetchGraphData = async () => {
    try {
      console.log('Fetching graph data...');
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/graph-data');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Graph data received:', data);
      setGraphData(data);
    } catch (err) {
      console.error('Error fetching graph data:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Initialize vis-network (simplified version)
  const initializeNetwork = async () => {
    if (!networkRef.current || !graphData) {
      console.log('Cannot initialize network:', { 
        container: !!networkRef.current, 
        data: !!graphData 
      });
      return;
    }

    try {
      console.log('Initializing network with data:', graphData);

      // Dynamic import of vis-network
      const { Network } = await import('vis-network/standalone/umd/vis-network.min');

      // Simple node colors
      const getNodeColor = (type: string) => {
        const colors: Record<string, string> = {
          'Instrument': '#e74c3c',
          'Provision': '#3498db',
          'GazetteIssue': '#2ecc71',
          'Court': '#f39c12',
          'Judgment': '#9b59b6',
          'Event': '#1abc9c'
        };
        return colors[type] || '#95a5a6';
      };

      // Simple data format (no DataSet)
      const data = {
        nodes: graphData.nodes.map(node => ({
          id: node.id,
          label: node.label,
          color: getNodeColor(node.type),
          title: `${node.type}: ${node.label}`
        })),
        edges: graphData.edges.map(edge => ({
          from: edge.from,
          to: edge.to,
          label: edge.type
        }))
      };

      console.log('Network data:', data);

      const options = {
        nodes: {
          shape: 'dot',
          size: 30,
          font: {
            size: 12,
            color: '#ffffff'
          },
          borderWidth: 2,
          shadow: true
        },
        edges: {
          width: 2,
          color: '#848484',
          arrows: {
            to: { enabled: true, scaleFactor: 1, type: 'arrow' }
          },
          smooth: {
            enabled: true,
            type: 'continuous',
            roundness: 0.5
          }
        },
        physics: {
          enabled: true,
          stabilization: { iterations: 200 }
        },
        interaction: {
          dragNodes: true,
          dragView: true,
          zoomView: true
        }
      };

      console.log('Creating network...');

      // Clear container first
      if (networkRef.current) {
        networkRef.current.innerHTML = '';
      }

      // Create network
      const network = new Network(networkRef.current, data, options);
      networkInstance.current = network;

      // Add event listeners
      network.on('click', (params: any) => {
        console.log('Network clicked:', params);
      });

      network.on('stabilizationIterationsDone', () => {
        console.log('Network stabilization complete');
      });

      console.log('✅ Network initialized successfully');

    } catch (err) {
      console.error('❌ Failed to initialize network:', err);
      setError(`Failed to initialize visualization: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  useEffect(() => {
    fetchGraphData();
  }, []);

  useEffect(() => {
    if (graphData && !loading && !error) {
      console.log('Data available, initializing network...');
      initializeNetwork();
    }
  }, [graphData, loading, error]);

  if (loading) {
    return (
      <Layout title="Simple Graph - UAE Legal GraphRAG">
        <div className="text-center py-12">
          <div className="text-blue-400 mb-4">📊 Loading simple graph...</div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Simple Graph - UAE Legal GraphRAG">
        <div className="text-center py-12 max-w-2xl mx-auto">
          <div className="text-red-400 mb-4">❌ Error in simple graph</div>
          <div className="text-gray-400 mb-6 whitespace-pre-line">{error}</div>
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
    <Layout title="Simple Graph - UAE Legal GraphRAG">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">🔗 Simple Graph</h1>
            <p className="text-gray-400">Legal Knowledge Graph (Simple Version)</p>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={fetchGraphData}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              🔄 Refresh
            </button>
            <button
              onClick={initializeNetwork}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              🔧 Force Init
            </button>
          </div>
        </div>

        {/* Stats */}
        {graphData?.stats && (
          <div className="bg-gray-800/50 border border-gray-700 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-white mb-3">📈 Graph Stats</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <div className="text-gray-400">Nodes</div>
                <div className="text-white font-semibold">{graphData.stats.nodeCount}</div>
              </div>
              <div>
                <div className="text-gray-400">Edges</div>
                <div className="text-white font-semibold">{graphData.stats.edgeCount}</div>
              </div>
              <div>
                <div className="text-gray-400">Node Types</div>
                <div className="text-white font-semibold">{Object.keys(graphData.stats.nodeTypes).length}</div>
              </div>
              <div>
                <div className="text-gray-400">Edge Types</div>
                <div className="text-white font-semibold">{Object.keys(graphData.stats.edgeTypes).length}</div>
              </div>
            </div>
          </div>
        )}

        {/* Graph Canvas */}
        <div className="bg-gray-900/50 rounded-xl border border-gray-700/50 overflow-hidden">
          <div
            ref={networkRef}
            className="w-full h-[600px] bg-gray-900"
            style={{ cursor: 'default' }}
          />
        </div>
      </div>
    </Layout>
  );
}
