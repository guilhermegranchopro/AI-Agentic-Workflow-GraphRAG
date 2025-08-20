import { useEffect, useRef, useState } from 'react';
import Layout from '../components/Layout';

interface GraphNode {
  id: string;
  label: string;
  color?: string;
}

interface GraphEdge {
  from: string;
  to: string;
  label?: string;
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

export default function GraphTest() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const networkRef = useRef<HTMLDivElement>(null);
  const networkInstance = useRef<any>(null);

  // Fetch test graph data
  const fetchTestData = async () => {
    try {
      console.log('Fetching test graph data...');
      setLoading(true);
      setError(null);
      
      const response = await fetch('/api/test-graph');
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      console.log('Test data received:', data);
      setGraphData(data);
    } catch (err) {
      console.error('Error fetching test data:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // Initialize vis-network
  const initializeNetwork = async () => {
    if (!networkRef.current || !graphData) {
      console.log('Cannot initialize network:', { 
        container: !!networkRef.current, 
        data: !!graphData 
      });
      return;
    }

    try {
      console.log('Initializing test network with data:', graphData);

      // Dynamic import of vis-network
      const { Network } = await import('vis-network/standalone/umd/vis-network.min');

      // Simple data format (no DataSet for now)
      const data = {
        nodes: graphData.nodes,
        edges: graphData.edges
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

      console.log('Creating network with options:', options);

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

      console.log('✅ Test network initialized successfully');

    } catch (err) {
      console.error('❌ Failed to initialize test network:', err);
      setError(`Failed to initialize test visualization: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  useEffect(() => {
    fetchTestData();
  }, []);

  useEffect(() => {
    if (graphData && !loading && !error) {
      console.log('Data available, initializing network...');
      initializeNetwork();
    }
  }, [graphData, loading, error]);

  if (loading) {
    return (
      <Layout title="Graph Test - UAE Legal GraphRAG">
        <div className="text-center py-12">
          <div className="text-blue-400 mb-4">📊 Loading test graph...</div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Graph Test - UAE Legal GraphRAG">
        <div className="text-center py-12 max-w-2xl mx-auto">
          <div className="text-red-400 mb-4">❌ Error in test graph</div>
          <div className="text-gray-400 mb-6 whitespace-pre-line">{error}</div>
          <button
            onClick={fetchTestData}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            Retry Test
          </button>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Graph Test - UAE Legal GraphRAG">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-2">🧪 Graph Test</h1>
            <p className="text-gray-400">Testing vis-network with simple data</p>
          </div>
          
          <div className="flex gap-3">
            <button
              onClick={fetchTestData}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              🔄 Refresh Test
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
            <h3 className="text-lg font-semibold text-white mb-3">📈 Test Stats</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <div className="text-gray-400">Nodes</div>
                <div className="text-white font-semibold">{graphData.stats.nodeCount}</div>
              </div>
              <div>
                <div className="text-gray-400">Edges</div>
                <div className="text-white font-semibold">{graphData.stats.edgeCount}</div>
              </div>
            </div>
          </div>
        )}

        {/* Graph Canvas */}
        <div className="bg-gray-900/50 rounded-xl border border-gray-700/50 overflow-hidden">
          <div
            ref={networkRef}
            className="w-full h-[500px] bg-gray-900"
            style={{ cursor: 'default' }}
          />
        </div>
      </div>
    </Layout>
  );
}
