import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Scale, Database, Cpu, Activity } from 'lucide-react';

const Navigation: React.FC = () => {
  const router = useRouter();

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-3">
              <Scale className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">UAE Legal GraphRAG</h1>
                <p className="text-xs text-gray-500">Neo4j + Next.js + Azure OpenAI</p>
              </div>
            </Link>
          </div>
          
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-1">
              <Database className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">Connected</span>
            </div>
            
            <div className="flex items-center space-x-1">
              <Cpu className="h-4 w-4 text-gray-400" />
              <span className="text-sm text-gray-600">AI Ready</span>
            </div>
            
            <div className="flex items-center space-x-1">
              <Activity className="h-4 w-4 text-green-500" />
              <span className="text-sm text-green-600">Healthy</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
