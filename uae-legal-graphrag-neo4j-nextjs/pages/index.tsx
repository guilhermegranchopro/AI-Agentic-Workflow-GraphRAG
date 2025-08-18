import React, { useState, useEffect } from 'react';
import Layout from '@/components/Layout';
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
      const response = await fetch('/api/stats');
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
    <div className="card hover:shadow-md transition-shadow duration-200 cursor-pointer"
         onClick={() => window.location.href = href}>
      <div className="flex items-start space-x-4">
        <div className="flex-shrink-0">
          <Icon className="h-8 w-8 text-primary-600" />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-900 mb-2">{title}</h3>
          <p className="text-gray-600">{description}</p>
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
      primary: 'text-primary-600',
      green: 'text-green-600',
      blue: 'text-blue-600',
      purple: 'text-purple-600'
    };

    return (
      <div className="card">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <Icon className={`h-6 w-6 ${colorClasses[color]}`} />
          </div>
          <div className="ml-4">
            <p className="text-sm font-medium text-gray-500">{title}</p>
            <p className="text-2xl font-bold text-gray-900">{value}</p>
          </div>
        </div>
      </div>
    );
  };

  return (
    <Layout title="UAE Legal GraphRAG - Home">
      <div className="animate-fade-in">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">⚖️ UAE Legal GraphRAG</h1>
          <p className="text-xl text-gray-600">Advanced legal research with GraphRAG and AI agents</p>
        </div>

        {/* Health Status */}
        <div className="mb-8">
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">System Health</h2>
              <div className={`status-indicator ${
                healthStatus?.status === 'healthy' ? 'status-healthy' : 'status-error'
              }`}>
                <Activity className="h-4 w-4 mr-1" />
                {healthStatus?.status || 'Checking...'}
              </div>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center space-x-3">
                <Database className={`h-5 w-5 ${
                  healthStatus?.database ? 'text-green-500' : 'text-red-500'
                }`} />
                <span className="text-sm text-gray-600">Database Connection</span>
              </div>
              <div className="flex items-center space-x-3">
                <Zap className={`h-5 w-5 ${
                  healthStatus?.embeddings ? 'text-green-500' : 'text-red-500'
                }`} />
                <span className="text-sm text-gray-600">Embeddings Service</span>
              </div>
              <div className="flex items-center space-x-3">
                <Activity className={`h-5 w-5 ${
                  healthStatus?.ai_service ? 'text-green-500' : 'text-red-500'
                }`} />
                <span className="text-sm text-gray-600">AI Service</span>
              </div>
            </div>
          </div>
        </div>

        {/* Database Statistics */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Database Statistics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
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
        </div>

        {/* GraphRAG Methods Overview */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">GraphRAG Retrieval Methods</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <OverviewCard
              title="🎯 Local RAG"
              description="Entity-centric traversal with temporal filtering for precise legal research"
              icon={Database}
              href="/local"
            />
            <OverviewCard
              title="🌐 Global RAG"
              description="Community-based analysis using Graph Data Science for comprehensive insights"
              icon={Network}
              href="/global"
            />
            <OverviewCard
              title="🎪 DRIFT RAG"
              description="Community-guided local search combining global context with local precision"
              icon={Zap}
              href="/drift"
            />
          </div>
        </div>

        {/* Additional Features */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-6">Additional Features</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <OverviewCard
              title="📊 Graph Visualization"
              description="Interactive exploration of legal knowledge graphs with advanced filtering"
              icon={Network}
              href="/graph"
            />
            <OverviewCard
              title="🤖 Legal Assistant AI"
              description="Multi-agent system for complex legal queries with autonomous reasoning"
              icon={Activity}
              href="/assistant"
            />
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default HomePage;
