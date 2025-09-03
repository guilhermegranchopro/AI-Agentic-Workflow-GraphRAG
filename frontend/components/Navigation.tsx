import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { 
  Scale, 
  Database, 
  Cpu, 
  Activity,
  Home, 
  Network, 
  MessageSquare,
  Menu,
  X,
  AlertTriangle,
  Brain
} from 'lucide-react';

const Navigation: React.FC = () => {
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigationItems = [
    { name: 'Overview', href: '/', icon: Home },
    { name: 'Graph', href: '/graph', icon: Network },
    { name: 'AI Assistant', href: '/assistant', icon: MessageSquare },
    { name: 'AI Analysis', href: '/ai-analysis', icon: AlertTriangle },
  ];

  return (
    <nav className="prof-nav sticky top-0 z-50">
      <div className="prof-container">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center flex-shrink-0">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="flex-shrink-0">
                <Scale className="h-8 w-8 text-blue-400" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-slate-100">
                  UAE Legal GraphRAG
                </h1>
                <p className="text-sm text-slate-400 hidden sm:block">
                  Neo4j + Next.js + Azure AI
                </p>
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
                  className={`prof-nav-item flex items-center ${
                    isActive ? 'active' : ''
                  }`}
                >
                  <item.icon className="mr-2 h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
          
          {/* Status Indicators */}
          <div className="flex items-center space-x-3">
            <div className="hidden md:flex items-center space-x-2">
              <div className="prof-status-success">
                <Database className="h-3 w-3 mr-1" />
                <span className="hidden lg:inline">Neo4j</span>
              </div>
              
              <div className="prof-status-success">
                <Cpu className="h-3 w-3 mr-1" />
                <span className="hidden lg:inline">AI</span>
              </div>
              
              <div className="prof-status-success">
                <Activity className="h-3 w-3 mr-1" />
                <span className="hidden lg:inline">Live</span>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="lg:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="prof-btn-secondary p-2"
              >
                {isMobileMenuOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="lg:hidden border-t border-slate-700 bg-slate-900">
            <div className="px-4 pt-2 pb-4 space-y-1">
              {navigationItems.map((item) => {
                const isActive = router.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`prof-nav-item flex items-center w-full ${
                      isActive ? 'active' : ''
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
              
              {/* Mobile Status */}
              <div className="border-t border-slate-700 pt-4 mt-4">
                <h3 className="text-sm font-medium text-slate-200 mb-3">System Status</h3>
                <div className="space-y-2">
                  <div className="prof-status-success w-full justify-start">
                    <Database className="h-4 w-4 mr-2" />
                    <span>Neo4j Connected</span>
                  </div>
                  <div className="prof-status-success w-full justify-start">
                    <Cpu className="h-4 w-4 mr-2" />
                    <span>AI Service Active</span>
                  </div>
                  <div className="prof-status-success w-full justify-start">
                    <Activity className="h-4 w-4 mr-2" />
                    <span>System Healthy</span>
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
