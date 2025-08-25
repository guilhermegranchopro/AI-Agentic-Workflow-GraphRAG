import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
import Container from '@/components/ui/Container';
import { DatabaseStats, HealthCheck } from '@/types';
import { Database, Activity, Users, FileText, Network, Zap } from 'lucide-react';

const HomePage: React.FC = () => {
  const [healthStatus, setHealthStatus] = useState<HealthCheck | null>(null);
  const [dbStats, setDbStats] = useState<DatabaseStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHealthStatus();
    fetchDatabaseStats();
  }, []);

  const fetchHealthStatus = async () => {
    try {
      const response = await fetch('/api/health');
      const data = await response.json();
      setHealthStatus(data);
    } catch (error) {
      console.error('Failed to fetch health status:', error);
    }
  };

  const fetchDatabaseStats = async () => {
    try {
      const response = await fetch('/api/stats-new');
      const data = await response.json();
      setDbStats(data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch database stats:', error);
      setLoading(false);
    }
  };

  const OverviewCard = ({ 
    title, 
    description, 
    icon: Icon, 
    href 
  }: { 
    title: string; 
    description: string; 
    icon: any; 
    href: string; 
  }) => (
    <div 
      className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 p-6 cursor-pointer transition-all duration-300 hover:shadow-xl hover:shadow-purple-500/10 hover:border-purple-500/40 backdrop-blur-sm"
      onClick={() => window.location.href = href}
    >
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-600/20 to-blue-600/20 border border-purple-500/30 flex items-center justify-center shadow-lg">
            <Icon className="h-6 w-6 text-purple-400" />
          </div>
        </div>
        <div className="flex-1 min-w-0">
          <h3 className="text-lg font-semibold text-white mb-2">{title}</h3>
          <p className="text-sm text-gray-300 mb-4 leading-relaxed">{description}</p>
          <div className="flex items-center text-sm text-purple-400 font-medium group">
            <span>Launch Experience</span>
            <svg className="ml-2 w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </div>
        </div>
      </div>
    </div>
  );

  const StatCard = ({ 
    title, 
    value, 
    icon: Icon, 
    color = 'primary' 
  }: { 
    title: string; 
    value: string | number; 
    icon: any; 
    color?: 'primary' | 'green' | 'blue' | 'purple'; 
  }) => {
    const colorClasses = {
      primary: 'text-purple-400 bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30',
      green: 'text-green-400 bg-gradient-to-br from-green-600/20 to-green-800/20 border-green-500/30',
      blue: 'text-blue-400 bg-gradient-to-br from-blue-600/20 to-blue-800/20 border-blue-500/30',
      purple: 'text-purple-400 bg-gradient-to-br from-purple-600/20 to-purple-800/20 border-purple-500/30'
    };

    return (
      <div className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 p-6 shadow-lg backdrop-blur-sm">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className={`w-12 h-12 rounded-xl ${colorClasses[color]} border flex items-center justify-center shadow-lg`}>
              <Icon className={`h-6 w-6 ${colorClasses[color].split(' ')[0]}`} />
            </div>
          </div>
          <div className="ml-4 flex-1">
            <p className="text-sm font-medium text-gray-400 mb-1">{title}</p>
            <p className="text-2xl font-bold text-white">{value}</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <Layout title="UAE Legal GraphRAG - Home">
      <Container>
        <div className="space-y-12">
          {/* Professional Hero Section */}
          <div className="text-center py-16">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white mb-6 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              UAE Legal GraphRAG
            </h1>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8 leading-relaxed">
              Advanced legal research platform powered by GraphRAG technology and AI agents for comprehensive UAE legal analysis
            </p>
            <div className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-600/20 to-blue-600/20 text-purple-300 rounded-xl text-sm font-medium border border-purple-500/30 backdrop-blur-sm shadow-lg">
              <span>Neo4j • Next.js • Azure AI</span>
            </div>
          </div>

          {/* System Health */}
          <section>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl md:text-3xl font-bold text-white flex items-center">
                <Activity className="h-6 w-6 mr-3 text-purple-400" />
                System Health
              </h2>
              <div className={`px-4 py-2 rounded-xl text-sm font-medium flex items-center ${
                healthStatus?.status === 'healthy' 
                  ? 'bg-green-900/30 text-green-400 border border-green-500/30' 
                  : 'bg-red-900/30 text-red-400 border border-red-500/30'
              }`}>
                <Activity className="h-4 w-4 mr-2" />
                {healthStatus?.status || 'Checking...'}
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 p-4 flex items-center space-x-3 shadow-lg backdrop-blur-sm">
                <Database className={`h-6 w-6 ${
                  healthStatus?.database ? 'text-green-400' : 'text-red-400'
                }`} />
                <span className="font-medium text-gray-300">Database Connection</span>
              </div>
              <div className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 p-4 flex items-center space-x-3 shadow-lg backdrop-blur-sm">
                <Zap className={`h-6 w-6 ${
                  healthStatus?.embeddings ? 'text-green-400' : 'text-red-400'
                }`} />
                <span className="font-medium text-gray-300">Embeddings Service</span>
              </div>
              <div className="bg-gradient-to-br from-gray-900/50 to-gray-800/50 rounded-xl border border-purple-500/20 p-4 flex items-center space-x-3 shadow-lg backdrop-blur-sm">
                <Activity className={`h-6 w-6 ${
                  healthStatus?.ai_service ? 'text-green-400' : 'text-red-400'
                }`} />
                <span className="font-medium text-gray-300">AI Service</span>
              </div>
            </div>
          </section>

          {/* Database Statistics */}
          <section>
            <h2 className="text-2xl md:text-3xl font-bold text-white flex items-center mb-6">
              <Database className="h-6 w-6 mr-3 text-purple-400" />
              Database Statistics
            </h2>
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard
                title="Documents"
                value={dbStats?.total_documents?.toLocaleString() || '---'}
                icon={FileText}
                color="blue"
              />
              <StatCard
                title="Entities"
                value={dbStats?.total_entities?.toLocaleString() || '---'}
                icon={Users}
                color="green"
              />
              <StatCard
                title="Relationships"
                value={dbStats?.total_relationships?.toLocaleString() || '---'}
                icon={Network}
                color="purple"
              />
              <StatCard
                title="Communities"
                value={dbStats?.communities?.toLocaleString() || '---'}
                icon={Database}
                color="primary"
              />
            </div>
          </section>

          {/* GraphRAG Methods */}
          <section>
            <h2 className="text-2xl md:text-3xl font-bold text-white flex items-center mb-6">
              <Network className="h-6 w-6 mr-3 text-purple-400" />
              GraphRAG Retrieval Methods
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <OverviewCard
                title="Local RAG"
                description="Entity-centric traversal with temporal filtering for precise legal research"
                icon={Database}
                href="/assistant"
              />
              <OverviewCard
                title="Global RAG"
                description="Community-based analysis using Graph Data Science for comprehensive insights"
                icon={Network}
                href="/assistant"
              />
              <OverviewCard
                title="DRIFT RAG"
                description="Dynamic temporal analysis for tracking legal evolution over time"
                icon={Zap}
                href="/assistant"
              />
            </div>
          </section>

          {/* Additional Features */}
          <section>
            <h2 className="text-2xl md:text-3xl font-bold text-white flex items-center mb-6">
              <Zap className="h-6 w-6 mr-3 text-purple-400" />
              Additional Features
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <OverviewCard
                title="Graph Visualization"
                description="Interactive exploration of legal knowledge graphs with advanced filtering"
                icon={Network}
                href="/graph"
              />
              <OverviewCard
                title="AI Assistant"
                description="Multi-agent system for complex legal queries with autonomous reasoning"
                icon={Activity}
                href="/assistant"
              />
              <OverviewCard
                title="AI Analysis"
                description="Automated contradiction finder with harmonisation recommendations"
                icon={Activity}
                href="/ai-analysis"
              />
            </div>
          </section>
        </div>
      </Container>
    </Layout>
  );
};

export default HomePage;
