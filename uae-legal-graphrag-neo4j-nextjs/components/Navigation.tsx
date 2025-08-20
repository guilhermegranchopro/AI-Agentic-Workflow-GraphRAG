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
  AlertTriangle
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
    <nav className="bg-gray-900/95 backdrop-blur-xl shadow-2xl border-b border-purple-500/20 transition-all duration-300 relative overflow-hidden">
      {/* Epic Background Gradient */}
      <div className="absolute inset-0 bg-gradient-to-r from-purple-900/10 via-blue-900/10 to-indigo-900/10"></div>
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-purple-500/5 via-transparent to-transparent"></div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="flex justify-between h-18">
          {/* Epic Logo and Brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-4 group">
              <div className="relative">
                <div className="absolute -inset-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-full opacity-20 group-hover:opacity-40 blur transition-opacity duration-300"></div>
                <Scale className="h-10 w-10 text-transparent bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text relative z-10 group-hover:scale-110 transition-transform duration-300" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-transparent bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text group-hover:from-purple-300 group-hover:via-blue-300 group-hover:to-cyan-300 transition-all duration-300">
                  UAE Legal GraphRAG
                </h1>
                <p className="text-sm text-purple-300/70 group-hover:text-purple-300 transition-colors duration-300 hidden sm:block">
                  ⚡ Neo4j + Next.js + Azure AI ⚡
                </p>
              </div>
            </Link>
          </div>

          {/* Epic Desktop Navigation */}
          <div className="hidden lg:flex items-center space-x-2">
            {navigationItems.map((item) => {
              const isActive = router.pathname === item.href;
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`group relative flex items-center px-6 py-3 rounded-xl text-sm font-semibold transition-all duration-300 ${
                    isActive 
                      ? 'text-white bg-gradient-to-r from-purple-600/30 to-blue-600/30 border border-purple-400/50 shadow-lg shadow-purple-500/20' 
                      : 'text-gray-300 hover:text-white hover:bg-gradient-to-r hover:from-purple-600/20 hover:to-blue-600/20 hover:border-purple-400/30 border border-transparent'
                  }`}
                >
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-blue-600/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                  <item.icon className="mr-3 h-5 w-5 relative z-10 group-hover:scale-110 transition-transform duration-300" aria-hidden="true" />
                  <span className="relative z-10">{item.name}</span>
                  {isActive && (
                    <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl opacity-20 blur transition-opacity duration-300"></div>
                  )}
                </Link>
              );
            })}
          </div>
          
          {/* Epic Status Indicators and Controls */}
          <div className="flex items-center space-x-4">
            {/* Futuristic Status Indicators */}
            <div className="hidden md:flex items-center space-x-3">
              <div className="group flex items-center space-x-2 px-3 py-2 rounded-lg bg-gradient-to-r from-green-600/20 to-emerald-600/20 border border-green-500/30">
                <Database className="h-4 w-4 text-green-400 group-hover:scale-110 transition-transform duration-300" />
                <span className="text-sm text-green-300 hidden lg:block font-medium">Neo4j</span>
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              
              <div className="group flex items-center space-x-2 px-3 py-2 rounded-lg bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border border-blue-500/30">
                <Cpu className="h-4 w-4 text-blue-400 group-hover:scale-110 transition-transform duration-300" />
                <span className="text-sm text-blue-300 hidden lg:block font-medium">AI</span>
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
              </div>
              
              <div className="group flex items-center space-x-2 px-3 py-2 rounded-lg bg-gradient-to-r from-purple-600/20 to-violet-600/20 border border-purple-500/30">
                <Activity className="h-4 w-4 text-purple-400 group-hover:scale-110 transition-transform duration-300" />
                <span className="text-sm text-purple-300 hidden lg:block font-medium">Live</span>
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="lg:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="inline-flex items-center justify-center p-3 rounded-xl text-gray-400 hover:text-gray-200 hover:bg-gray-800/50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-purple-500 transition-all duration-300"
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

        {/* Epic Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="lg:hidden border-t border-purple-500/20 bg-gray-900/98 backdrop-blur-xl relative">
            <div className="absolute inset-0 bg-gradient-to-b from-purple-900/5 to-blue-900/5"></div>
            <div className="px-4 pt-4 pb-6 space-y-3 sm:px-6 relative z-10">
              {navigationItems.map((item) => {
                const isActive = router.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`group relative flex items-center px-4 py-4 rounded-xl text-base font-semibold transition-all duration-300 ${
                      isActive 
                        ? 'text-white bg-gradient-to-r from-purple-600/30 to-blue-600/30 border border-purple-400/50 shadow-lg shadow-purple-500/20' 
                        : 'text-gray-300 hover:text-white hover:bg-gradient-to-r hover:from-purple-600/20 hover:to-blue-600/20 hover:border-purple-400/30 border border-transparent'
                    }`}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-purple-600/10 to-blue-600/10 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    <item.icon className="mr-4 h-6 w-6 relative z-10 group-hover:scale-110 transition-transform duration-300" aria-hidden="true" />
                    <span className="relative z-10">{item.name}</span>
                    {isActive && (
                      <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl opacity-20 blur transition-opacity duration-300"></div>
                    )}
                  </Link>
                );
              })}
              
              {/* Epic Mobile Status Indicators */}
              <div className="border-t border-purple-500/20 pt-6 mt-6">
                <h3 className="text-purple-300 font-semibold mb-4 text-sm uppercase tracking-wider">System Status</h3>
                <div className="space-y-3">
                  <div className="flex items-center px-4 py-3 rounded-xl bg-gradient-to-r from-green-600/20 to-emerald-600/20 border border-green-500/30">
                    <Database className="h-5 w-5 text-green-400 mr-3" />
                    <span className="text-sm text-green-300 font-medium">Neo4j Connected</span>
                    <div className="ml-auto w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                  </div>
                  <div className="flex items-center px-4 py-3 rounded-xl bg-gradient-to-r from-blue-600/20 to-cyan-600/20 border border-blue-500/30">
                    <Cpu className="h-5 w-5 text-blue-400 mr-3" />
                    <span className="text-sm text-blue-300 font-medium">AI Service Active</span>
                    <div className="ml-auto w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                  </div>
                  <div className="flex items-center px-4 py-3 rounded-xl bg-gradient-to-r from-purple-600/20 to-violet-600/20 border border-purple-500/30">
                    <Activity className="h-5 w-5 text-purple-400 mr-3" />
                    <span className="text-sm text-purple-300 font-medium">System Healthy</span>
                    <div className="ml-auto w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
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
