import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  Home, 
  Target, 
  Globe, 
  Sparkles, 
  Network, 
  MessageSquare,
  BarChart3,
  Settings,
  Search,
  TrendingUp,
  Share2
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const router = useRouter();

  const navigation = [
    { name: 'Overview', href: '/', icon: Home },
    { name: 'Local RAG', href: '/local', icon: Target },
    { name: 'Global RAG', href: '/global', icon: Globe },
    { name: 'DRIFT RAG', href: '/drift', icon: Sparkles },
    { name: 'Graph Visualization', href: '/graph', icon: Network },
    { name: 'Legal Assistant', href: '/assistant', icon: MessageSquare },
    { name: 'Analytics', href: '/analytics', icon: BarChart3 },
    { name: 'Settings', href: '/settings', icon: Settings },
  ];

  return (
    <div className="fixed inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 pt-16">
      <div className="flex flex-col h-full">
        <div className="flex-1 flex flex-col min-h-0 pt-5 pb-4 overflow-y-auto">
          <nav className="mt-5 flex-1 px-4 space-y-1">
            {navigation.map((item) => {
              const isActive = router.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`sidebar-link ${
                    isActive ? 'sidebar-link-active' : 'sidebar-link-inactive'
                  }`}
                >
                  <item.icon className="mr-3 h-5 w-5" aria-hidden="true" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        </div>
        
        <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
          <div className="text-xs text-gray-500">
            <p>UAE Legal GraphRAG v1.0</p>
            <p>Next.js + Neo4j + Azure AI</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Sidebar;
