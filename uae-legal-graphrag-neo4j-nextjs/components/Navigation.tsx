import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  Scale, 
  Database, 
  Cpu, 
  Activity,
  Home, 
  Target, 
  Globe, 
  Sparkles, 
  Network, 
  MessageSquare,
  Menu,
  X
} from 'lucide-react';

const Navigation: React.FC = () => {
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigationItems = [
    { name: 'Overview', href: '/', icon: Home },
    { name: 'Local RAG', href: '/local', icon: Target },
    { name: 'Global RAG', href: '/global', icon: Globe },
    { name: 'DRIFT RAG', href: '/drift', icon: Sparkles },
    { name: 'Graph', href: '/graph', icon: Network },
    { name: 'Assistant', href: '/assistant', icon: MessageSquare },
  ];

  return (
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-3">
              <Scale className="h-8 w-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">UAE Legal GraphRAG</h1>
                <p className="text-xs text-gray-500 hidden sm:block">Neo4j + Next.js + Azure OpenAI</p>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-1">
            {navigationItems.map((item) => {
              const isActive = router.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 ${
                    isActive 
                      ? 'bg-primary-100 text-primary-700 border border-primary-200' 
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  <item.icon className="mr-2 h-4 w-4" aria-hidden="true" />
                  {item.name}
                </Link>
              );
            })}
          </div>
          
          {/* Status Indicators and Mobile Menu Button */}
          <div className="flex items-center space-x-4">
            {/* Status Indicators */}
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <Database className="h-4 w-4 text-gray-400" />
                <span className="text-sm text-gray-600 hidden lg:block">Connected</span>
              </div>
              
              <div className="flex items-center space-x-1">
                <Cpu className="h-4 w-4 text-gray-400" />
                <span className="text-sm text-gray-600 hidden lg:block">AI Ready</span>
              </div>
              
              <div className="flex items-center space-x-1">
                <Activity className="h-4 w-4 text-green-500" />
                <span className="text-sm text-green-600 hidden lg:block">Healthy</span>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="lg:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500"
                aria-expanded="false"
              >
                <span className="sr-only">Open main menu</span>
                {isMobileMenuOpen ? (
                  <X className="block h-6 w-6" aria-hidden="true" />
                ) : (
                  <Menu className="block h-6 w-6" aria-hidden="true" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="lg:hidden border-t border-gray-200">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigationItems.map((item) => {
                const isActive = router.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`flex items-center px-3 py-2 rounded-md text-base font-medium ${
                      isActive 
                        ? 'bg-primary-100 text-primary-700' 
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" aria-hidden="true" />
                    {item.name}
                  </Link>
                );
              })}
              
              {/* Mobile Status Indicators */}
              <div className="border-t border-gray-200 pt-4 mt-4">
                <div className="space-y-2">
                  <div className="flex items-center px-3 py-2">
                    <Database className="h-4 w-4 text-gray-400 mr-2" />
                    <span className="text-sm text-gray-600">Database Connected</span>
                  </div>
                  <div className="flex items-center px-3 py-2">
                    <Cpu className="h-4 w-4 text-gray-400 mr-2" />
                    <span className="text-sm text-gray-600">AI Ready</span>
                  </div>
                  <div className="flex items-center px-3 py-2">
                    <Activity className="h-4 w-4 text-green-500 mr-2" />
                    <span className="text-sm text-green-600">System Healthy</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
