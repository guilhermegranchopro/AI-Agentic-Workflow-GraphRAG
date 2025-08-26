import { useState, useEffect, useRef } from 'react';
import Layout from '../components/Layout';
import Container from '@/components/ui/Container';

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

export default function Graph() {
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null);
  const [maxNodes, setMaxNodes] = useState(149);
  const [selectedRelationships, setSelectedRelationships] = useState([
    'ESTABLISHES', 'DEFINES', 'REGULATES', 'PROTECTS', 'GOVERNED_BY', 
    'REQUIRES', 'HAS_PRINCIPLE', 'ALIGNS_WITH', 'OVERSEES', 'ENFORCES',
    'ADMINISTERS', 'RECOGNIZES', 'DEFINED_BY', 'PROVIDES',
    'REGULATED_BY', 'HAS_COURT', 'PROTECTED_BY', 'PREVENTS',
    'AMENDS', 'SUPPLEMENTS', 'ENFORCED_BY', 'SPECIALIZES_IN',
    'ALTERNATIVE_TO', 'PRECEDES', 'SIMILAR_TO', 'INCLUDES', 'IMPOSED_BY',
    'ADMINISTERED_BY', 'GUARANTEED_BY', 'HEARD_BY'
  ]);
  const networkRef = useRef<HTMLDivElement>(null);
  const networkInstance = useRef<any>(null);

  const availableRelationships = [
    'ESTABLISHES', 'DEFINES', 'REGULATES', 'PROTECTS', 'GOVERNED_BY', 
    'REQUIRES', 'HAS_PRINCIPLE', 'ALIGNS_WITH', 'OVERSEES', 'ENFORCES',
    'ADMINISTERS', 'RECOGNIZES', 'DEFINED_BY', 'PROVIDES',
    'REGULATED_BY', 'HAS_COURT', 'PROTECTED_BY', 'PREVENTS',
    'AMENDS', 'SUPPLEMENTS', 'ENFORCED_BY', 'SPECIALIZES_IN',
    'ALTERNATIVE_TO', 'PRECEDES', 'SIMILAR_TO', 'INCLUDES', 'IMPOSED_BY',
    'ADMINISTERED_BY', 'GUARANTEED_BY', 'HEARD_BY'
  ];

  useEffect(() => {
    fetchGraphData();
  }, [maxNodes, selectedRelationships]);

  useEffect(() => {
    if (graphData && networkRef.current && !networkInstance.current && typeof window !== 'undefined') {
      initializeNetwork();
    }
  }, [graphData]);

  // No need for separate vis-network loading since we import dynamically

  const fetchGraphData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const params = new URLSearchParams({
        max_nodes: maxNodes.toString(),
        relationships: selectedRelationships.join(',')
      });
      
      const response = await fetch(`/api/graph?${params}`);
      
      if (!response.ok) {
        // Try to get detailed error information
        let errorMessage = 'Failed to fetch graph data';
        try {
          const errorData = await response.json();
          if (errorData.message) {
            errorMessage = errorData.message;
          } else if (errorData.error) {
            errorMessage = errorData.error;
          }
          
          // Show configuration help for 503 errors
          if (response.status === 503) {
            errorMessage += '\n\nPlease check your .env file and ensure Neo4j credentials are configured.';
          }
        } catch {
          // Fall back to status text if JSON parsing fails
          errorMessage = `HTTP ${response.status}: ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }
      
      const data = await response.json();
      setGraphData(data);
    } catch (err) {
      console.error('Graph fetch error:', err);
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  const initializeNetwork = async () => {
    if (!graphData || !networkRef.current) {
      console.log('❌ Cannot initialize network:', { 
        graphData: !!graphData,
        networkRef: !!networkRef.current
      });
      return;
    }

    try {
      console.log('🔄 Initializing network with data:', graphData);
      console.log('📊 Nodes count:', graphData.nodes.length);
      console.log('🔗 Edges count:', graphData.edges.length);
      
      // Dynamic import of vis-network
      const { Network } = await import('vis-network/standalone/umd/vis-network.min');

      // Simple data transformation (no DataSet)
      const data = {
        nodes: graphData.nodes.map(node => ({
          id: node.id,
          label: node.label,
          color: getNodeColor(node.type),
          title: `${node.type}: ${node.label}`,
          shape: 'dot',
          size: 20,
          font: { color: '#ffffff', size: 12 }
        })),
        edges: graphData.edges.map(edge => ({
          from: edge.from,
          to: edge.to,
          label: edge.type,
          arrows: 'to',
          color: { color: '#6366f1', opacity: 0.8 },
          width: 2,
          font: { size: 10, color: '#ffffff', strokeWidth: 2, strokeColor: '#000000' }
        }))
      };

      console.log('📝 Sample transformed node:', data.nodes[0]);
      console.log('🔗 Sample transformed edge:', data.edges[0]);

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
          width: 3,
          shadow: true,
          smooth: {
            enabled: true,
            type: 'continuous',
            roundness: 0.2,
          },
          font: {
            size: 10,
            color: '#ffffff',
            strokeWidth: 2,
            strokeColor: '#000000'
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

      if (data.nodes.length === 0) {
        setError('No nodes available to display');
        return;
      }

      console.log('Creating Network instance...');
      
      // Clear container first
      if (networkRef.current) {
        networkRef.current.innerHTML = '';
      }

      networkInstance.current = new Network(networkRef.current, data, options);
      console.log('Network created successfully!');

      // Add event listeners
      networkInstance.current.on('click', (params: any) => {
        if (params.nodes.length > 0) {
          const nodeId = params.nodes[0];
          const node = graphData.nodes.find(n => n.id === nodeId);
          setSelectedNode(node || null);
        } else {
          setSelectedNode(null);
        }
      });

      networkInstance.current.on('hoverNode', () => {
        if (networkRef.current) {
          networkRef.current.style.cursor = 'pointer';
        }
      });

      networkInstance.current.on('blurNode', () => {
        if (networkRef.current) {
          networkRef.current.style.cursor = 'default';
        }
      });

      networkInstance.current.on('stabilizationIterationsDone', () => {
        console.log('✅ Network stabilization complete');
      });

      console.log('✅ Network initialized successfully!');

    } catch (err) {
      console.error('❌ Error initializing network:', err);
      setError(`Failed to initialize graph visualization: ${err instanceof Error ? err.message : 'Unknown error'}`);
    }
  };

  const getNodeColor = (nodeType: string): string => {
    const colors: Record<string, string> = {
      // Constitutional & Legal Framework
      'Constitutional': '#ff6b6b',    // Red for constitutional
      'Law': '#4ecdc4',              // Teal for laws
      'Regulation': '#45b7d1',        // Blue for regulations
      
      // Entities & Organizations
      'EntityType': '#f9ca24',        // Yellow for entity types
      'FreeZone': '#6c5ce7',          // Purple for free zones
      'Regulator': '#fd79a8',         // Pink for regulators
      'Court': '#00b894',             // Green for courts
      'InternationalBody': '#e17055', // Orange for international bodies
      
      // Legal Concepts & Types
      'LegalConcept': '#74b9ff',      // Light blue for legal concepts
      'ContractType': '#a29bfe',      // Light purple for contract types
      'IPType': '#fd79a8',            // Pink for IP types
      'EmployeeType': '#fdcb6e',      // Light orange for employee types
      'TaxType': '#e84393',           // Dark pink for tax types
      'PropertyType': '#00cec9',      // Cyan for property types
      'LegalProcedure': '#fdcb6e',    // Light orange for procedures
      'CriminalOffense': '#d63031',   // Dark red for criminal offenses
      'LegalRemedy': '#00b894',       // Green for remedies
      'BusinessActivity': '#6c5ce7',  // Purple for business activities
      'LegalDocument': '#fd79a8',     // Pink for documents
      'ComplianceRequirement': '#e17055', // Orange for compliance
      'LegalProfession': '#74b9ff',   // Light blue for professions
      'LegalCase': '#f9ca24',         // Yellow for legal cases
      'PracticeArea': '#a29bfe',      // Light purple for practice areas
      'DisputeResolution': '#00cec9', // Cyan for dispute resolution
      'LiabilityType': '#e84393',     // Dark pink for liability types
      'LegalRight': '#fdcb6e',        // Light orange for legal rights
      'LegalSanction': '#d63031',     // Dark red for sanctions
      'LegalProcess': '#6c5ce7',      // Purple for processes
      'EmploymentAction': '#fd79a8',  // Pink for employment actions
      
      // Default
      'Unknown': '#95a5a6',           // Gray for unknown
    };
    return colors[nodeType] || colors['Unknown'];
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
          <div className="text-center space-y-4">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
            <div className="text-gray-300">
              Loading knowledge graph...
            </div>
            <div className="text-sm text-gray-400 space-y-1">
              <div>Loading: {loading ? '✅' : '❌'}</div>
              <div>Graph Data: {graphData ? '✅' : '❌'}</div>
            </div>
          </div>
        </div>
      </Layout>
    );
  }

  if (error) {
    return (
      <Layout title="Graph Visualization - UAE Legal GraphRAG">
        <div className="text-center py-12 max-w-2xl mx-auto">
          <div className="text-red-400 mb-4">❌ Error loading graph</div>
          <div className="text-gray-400 mb-6 whitespace-pre-line">{error}</div>
          
          {error.includes('Neo4j') && (
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-4 mb-6 text-left shadow-lg">
              <h3 className="text-yellow-400 font-semibold mb-2">⚠️ Configuration Required</h3>
              <p className="text-gray-300 text-sm mb-3">
                The graph visualization requires Neo4j database connection. 
                Please create a <code className="bg-gray-700 px-1 rounded">.env</code> file with:
              </p>
              <pre className="bg-gray-900 p-3 rounded text-xs text-gray-300 overflow-x-auto">
{`NEO4J_URI=bolt+s://your-host:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password`}
              </pre>
              <div className="mt-3 text-xs text-gray-400">
                💡 Diagnostics:{' '}
                <a 
                  href="/api/diagnostics/debug" 
                  target="_blank" 
                  className="text-blue-400 hover:text-blue-300 underline"
                >
                  Environment
                </a>
                {' | '}
                <a 
                  href="/api/diagnostics/neo4j" 
                  target="_blank" 
                  className="text-blue-400 hover:text-blue-300 underline"
                >
                  Neo4j Config
                </a>
              </div>
            </div>
          )}
          
          <div className="flex gap-3">
            <button
              onClick={fetchGraphData}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all duration-200 shadow-lg hover:shadow-purple-500/25"
            >
              Retry
            </button>
            <a
              href="/api/graph"
              target="_blank"
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-all duration-200 shadow-lg hover:shadow-gray-500/25"
            >
              Test API
            </a>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout title="Graph Visualization - UAE Legal GraphRAG">
      <Container>
        <div className="space-y-3 md:space-y-4 lg:space-y-6">
          {/* Header */}
          <div className="text-center">
            <h1 className="text-xl md:text-2xl lg:text-3xl font-bold text-white mb-2 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              🧠 UAE Legal Knowledge Graph
            </h1>
            <p className="text-sm md:text-base lg:text-lg text-gray-300 leading-relaxed">
              Comprehensive interactive exploration of UAE legal framework with 29 entity types and relationships
            </p>
            {graphData && (
              <div className="flex justify-center space-x-4 md:space-x-6 mt-3 md:mt-4 text-xs md:text-sm text-gray-400">
                <span className="bg-purple-900/30 px-2 py-1 rounded-lg border border-purple-500/30">📊 {graphData.stats.nodeCount} nodes</span>
                <span className="bg-blue-900/30 px-2 py-1 rounded-lg border border-blue-500/30">🔗 {graphData.stats.edgeCount} edges</span>
                <span className="bg-green-900/30 px-2 py-1 rounded-lg border border-green-500/30">🎨 {Object.keys(graphData.stats.nodeTypes).length} node types</span>
              </div>
            )}
        </div>

        {/* Graph Configuration Controls */}
        <div className="bg-gray-800/60 backdrop-blur-sm rounded-xl p-4 border border-gray-700/50">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Max Nodes Control */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Max Nodes: {maxNodes}
              </label>
              <input
                type="range"
                min="10"
                max="149"
                value={maxNodes}
                onChange={(e) => setMaxNodes(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer slider"
              />
            </div>

            {/* Relationships Filter */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Relationship Types
              </label>
              <div className="flex flex-wrap gap-2">
                {availableRelationships.map(rel => (
                  <label key={rel} className="inline-flex items-center">
                    <input
                      type="checkbox"
                      checked={selectedRelationships.includes(rel)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedRelationships([...selectedRelationships, rel]);
                        } else {
                          setSelectedRelationships(selectedRelationships.filter(r => r !== rel));
                        }
                      }}
                      className="mr-1 rounded"
                    />
                    <span className="text-xs text-gray-300">{rel}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Search Controls */}
        <div className="bg-gray-800/60 backdrop-blur-sm rounded-xl p-4 border border-gray-700/50">
          <div className="flex flex-wrap gap-4 items-center">
            <div className="flex-1 min-w-64">
              <div className="flex">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Search nodes by ID or label..."
                  className="flex-1 bg-gray-900/50 border border-gray-600/50 rounded-l-lg px-4 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all duration-200"
                  onKeyPress={(e) => e.key === 'Enter' && focusNode()}
                />
                <button
                  onClick={focusNode}
                  className="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-r-lg transition-all duration-200 shadow-lg hover:shadow-purple-500/25"
                >
                  🔍 Search
                </button>
              </div>
            </div>
            <button
              onClick={resetView}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-gray-500/25"
            >
              🎯 Reset View
            </button>
            <button
              onClick={fetchGraphData}
              className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-green-500/25"
            >
              🔄 Refresh Data
            </button>
            <button
              onClick={() => {
                console.log('Manual re-initialization triggered');
                setError(null);
                initializeNetwork();
              }}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-all duration-200 shadow-lg hover:shadow-blue-500/25"
            >
              ⚙️ Reinitialize
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
                        style={{ backgroundColor: getNodeColor(selectedNode.type) + '40', color: getNodeColor(selectedNode.type) }}
                      >
                        {selectedNode.type}
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
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 max-h-64 overflow-y-auto">
            {[
              // Constitutional & Legal Framework
              { type: 'Constitutional', desc: 'Constitutional framework' },
              { type: 'Law', desc: 'Federal laws & regulations' },
              { type: 'Regulation', desc: 'Specific regulations & decrees' },
              
              // Entities & Organizations
              { type: 'EntityType', desc: 'Business entity types' },
              { type: 'FreeZone', desc: 'Free zones & economic zones' },
              { type: 'Regulator', desc: 'Regulatory bodies' },
              { type: 'Court', desc: 'Courts & judicial bodies' },
              { type: 'InternationalBody', desc: 'International organizations' },
              
              // Legal Concepts & Types
              { type: 'LegalConcept', desc: 'Legal principles & concepts' },
              { type: 'ContractType', desc: 'Types of contracts' },
              { type: 'IPType', desc: 'Intellectual property types' },
              { type: 'EmployeeType', desc: 'Employment classifications' },
              { type: 'TaxType', desc: 'Tax categories' },
              { type: 'PropertyType', desc: 'Property classifications' },
              { type: 'LegalProcedure', desc: 'Legal procedures' },
              { type: 'CriminalOffense', desc: 'Criminal offenses' },
              { type: 'LegalRemedy', desc: 'Legal remedies' },
              { type: 'BusinessActivity', desc: 'Business activities' },
              { type: 'LegalDocument', desc: 'Legal documents' },
              { type: 'ComplianceRequirement', desc: 'Compliance requirements' },
              { type: 'LegalProfession', desc: 'Legal professions' },
              { type: 'LegalCase', desc: 'Legal cases & precedents' },
              { type: 'PracticeArea', desc: 'Legal practice areas' },
              { type: 'DisputeResolution', desc: 'Dispute resolution methods' },
              { type: 'LiabilityType', desc: 'Types of liability' },
              { type: 'LegalRight', desc: 'Legal rights' },
              { type: 'LegalSanction', desc: 'Legal sanctions' },
              { type: 'LegalProcess', desc: 'Legal processes' },
              { type: 'EmploymentAction', desc: 'Employment actions' }
            ].map(({ type, desc }) => (
              <div key={type} className="flex items-center space-x-2">
                <div 
                  className="w-4 h-4 rounded-full"
                  style={{ backgroundColor: getNodeColor(type) }}
                />
                <div>
                  <div className="text-gray-300 text-sm font-medium">{type}</div>
                  <div className="text-gray-500 text-xs">{desc}</div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-4 pt-4 border-t border-gray-700">
            <h5 className="text-gray-400 font-medium mb-2">Relationship Types:</h5>
            <div className="text-xs text-gray-500 space-y-1 max-h-32 overflow-y-auto">
              <div><strong>ESTABLISHES:</strong> Establishes legal framework</div>
              <div><strong>DEFINES:</strong> Defines legal concepts</div>
              <div><strong>REGULATES:</strong> Regulates activities</div>
              <div><strong>PROTECTS:</strong> Protects rights/interests</div>
              <div><strong>GOVERNED_BY:</strong> Governed by law</div>
              <div><strong>REQUIRES:</strong> Requires compliance</div>
              <div><strong>HAS_PRINCIPLE:</strong> Has legal principle</div>
              <div><strong>ALIGNS_WITH:</strong> Aligns with standards</div>
              <div><strong>OVERSEES:</strong> Oversees operations</div>
              <div><strong>ENFORCES:</strong> Enforces regulations</div>
              <div><strong>ADMINISTERS:</strong> Administers systems</div>
              <div><strong>RECOGNIZES:</strong> Recognizes entities</div>
              <div><strong>DEFINED_BY:</strong> Defined by law</div>
              <div><strong>PROVIDES:</strong> Provides remedies</div>
              <div><strong>REGULATED_BY:</strong> Regulated by authority</div>
              <div><strong>HAS_COURT:</strong> Has court system</div>
              <div><strong>PROTECTED_BY:</strong> Protected by law</div>
              <div><strong>PREVENTS:</strong> Prevents violations</div>
              <div><strong>AMENDS:</strong> Amends existing law</div>
              <div><strong>SUPPLEMENTS:</strong> Supplements law</div>
              <div><strong>ENFORCED_BY:</strong> Enforced by authority</div>
              <div><strong>SPECIALIZES_IN:</strong> Specializes in area</div>
              <div><strong>ALTERNATIVE_TO:</strong> Alternative to process</div>
              <div><strong>PRECEDES:</strong> Precedes action</div>
              <div><strong>SIMILAR_TO:</strong> Similar to concept</div>
              <div><strong>INCLUDES:</strong> Includes elements</div>
              <div><strong>IMPOSED_BY:</strong> Imposed by authority</div>
              <div><strong>ADMINISTERED_BY:</strong> Administered by body</div>
              <div><strong>GUARANTEED_BY:</strong> Guaranteed by constitution</div>
              <div><strong>HEARD_BY:</strong> Heard by court</div>
            </div>
          </div>
        </div>
        </div>
      </Container>
    </Layout>
  );
}
