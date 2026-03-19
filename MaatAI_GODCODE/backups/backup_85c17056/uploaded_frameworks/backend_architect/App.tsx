
import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import { AgentStatus } from './types';

const App: React.FC = () => {
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsInitializing(false);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  if (isInitializing) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-slate-950 text-blue-500 mono">
        <div className="text-2xl font-bold mb-4 animate-pulse">
          INITIALIZING OMEGA GATE...
        </div>
        <div className="w-64 h-1 bg-slate-900 rounded-full overflow-hidden">
          <div className="h-full bg-blue-600 animate-[loading_2s_ease-in-out_infinite]"></div>
        </div>
        <style>{`
          @keyframes loading {
            0% { width: 0%; }
            50% { width: 100%; }
            100% { width: 0%; }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="min-h-screen grid-bg selection:bg-blue-500/30">
      <Dashboard />
    </div>
  );
};

export default App;
