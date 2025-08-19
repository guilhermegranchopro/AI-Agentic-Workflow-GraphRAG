import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useTheme } from '@/lib/ThemeContext';
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
  Sun,
  Moon
} from 'lucide-react';

const Navigation: React.FC = () => {
  const router = useRouter();
  const { theme, toggleTheme } = useTheme();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navigationItems = [
    { name: 'Overview', href: '/', icon: Home },
    { name: 'Graph', href: '/graph', icon: Network },
    { name: 'Assistant', href: '/assistant', icon: MessageSquare },
  ];

  return (
    <nav className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-200/50 dark:bg-gray-900/80 dark:border-gray-700/50 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="relative">
                <Scale className="h-8 w-8 text-primary-600 dark:text-primary-400 group-hover:scale-110 transition-transform duration-200" />
                <div className="absolute -inset-1 bg-primary-600/20 rounded-full blur opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-200">
                  UAE Legal GraphRAG
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400 hidden sm:block">
                  Neo4j + Next.js + Azure OpenAI
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
                  className={`flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                    isActive 
                      ? 'bg-primary-100 text-primary-700 border border-primary-200 shadow-sm dark:bg-primary-900/30 dark:text-primary-400 dark:border-primary-800' 
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50'
                  }`}
                >
                  <item.icon className="mr-2 h-4 w-4" aria-hidden="true" />
                  {item.name}
                </Link>
              );
            })}
          </div>
          
          {/* Status Indicators and Controls */}
          <div className="flex items-center space-x-4">
            {/* Status Indicators */}
            <div className="hidden md:flex items-center space-x-4">
              <div className="flex items-center space-x-1 px-2 py-1 rounded-md bg-gray-50 dark:bg-gray-800/50">
                <Database className="h-4 w-4 text-green-500" />
                <span className="text-sm text-gray-600 dark:text-gray-400 hidden lg:block">Connected</span>
              </div>
              
              <div className="flex items-center space-x-1 px-2 py-1 rounded-md bg-gray-50 dark:bg-gray-800/50">
                <Cpu className="h-4 w-4 text-blue-500" />
                <span className="text-sm text-gray-600 dark:text-gray-400 hidden lg:block">AI Ready</span>
              </div>
              
              <div className="flex items-center space-x-1 px-2 py-1 rounded-md bg-green-50 dark:bg-green-900/20">
                <Activity className="h-4 w-4 text-green-500" />
                <span className="text-sm text-green-600 dark:text-green-400 hidden lg:block">Healthy</span>
              </div>
            </div>

            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg text-gray-500 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </button>

            {/* Mobile menu button */}
            <div className="lg:hidden">
              <button
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-lg text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-primary-500 transition-all duration-200"
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
          <div className="lg:hidden border-t border-gray-200 dark:border-gray-700 bg-white/95 dark:bg-gray-900/95 backdrop-blur-md">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              {navigationItems.map((item) => {
                const isActive = router.pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                    className={`flex items-center px-3 py-3 rounded-lg text-base font-medium transition-all duration-200 ${
                      isActive 
                        ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400' 
                        : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50'
                    }`}
                  >
                    <item.icon className="mr-3 h-5 w-5" aria-hidden="true" />
                    {item.name}
                  </Link>
                );
              })}
              
              {/* Mobile Theme Toggle */}
              <button
                onClick={toggleTheme}
                className="flex items-center px-3 py-3 rounded-lg text-base font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-gray-200 dark:hover:bg-gray-800/50 w-full transition-all duration-200"
              >
                {theme === 'dark' ? (
                  <>
                    <Sun className="mr-3 h-5 w-5" />
                    Switch to Light Mode
                  </>
                ) : (
                  <>
                    <Moon className="mr-3 h-5 w-5" />
                    Switch to Dark Mode
                  </>
                )}
              </button>
              
              {/* Mobile Status Indicators */}
              <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
                <div className="space-y-3">
                  <div className="flex items-center px-3 py-2 rounded-lg bg-green-50 dark:bg-green-900/20">
                    <Database className="h-4 w-4 text-green-500 mr-3" />
                    <span className="text-sm text-green-600 dark:text-green-400 font-medium">Database Connected</span>
                  </div>
                  <div className="flex items-center px-3 py-2 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                    <Cpu className="h-4 w-4 text-blue-500 mr-3" />
                    <span className="text-sm text-blue-600 dark:text-blue-400 font-medium">AI Ready</span>
                  </div>
                  <div className="flex items-center px-3 py-2 rounded-lg bg-green-50 dark:bg-green-900/20">
                    <Activity className="h-4 w-4 text-green-500 mr-3" />
                    <span className="text-sm text-green-600 dark:text-green-400 font-medium">System Healthy</span>
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
