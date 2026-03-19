
import React, { useState, useEffect } from 'react';
import { AgentStatus, ArchiveResult } from '../types';
import { searchArchive } from '../lib/gemini';

interface ArchiveSearchProps {
  setStatus: (status: AgentStatus) => void;
  addLog: (msg: string, level?: any, src?: string) => void;
  autoQuery?: string;
}

const ArchiveSearch: React.FC<ArchiveSearchProps> = ({ setStatus, addLog, autoQuery }) => {
  const [query, setQuery] = useState(autoQuery || '');
  const [results, setResults] = useState<ArchiveResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (autoQuery && !isSearching) {
      setQuery(autoQuery);
      handleSearch();
    }
  }, [autoQuery]);

  const handleSearch = async () => {
    const activeQuery = query.trim() || autoQuery?.trim();
    if (!activeQuery || isSearching) return;
    
    setIsSearching(true);
    setStatus(AgentStatus.SEARCHING);
    addLog(`Querying Epstein Archive for: ${activeQuery}`, 'INFO', 'FORENSIC');

    try {
      const data = await searchArchive(activeQuery);
      setResults(data);
      addLog(`Found ${data.length} relevant entries in archive.`, 'INFO', 'FORENSIC');
    } catch (error) {
      addLog("Search failure: " + (error as Error).message, "CRITICAL", "CORE");
    } finally {
      setIsSearching(false);
      setStatus(AgentStatus.IDLE);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="bg-slate-900/60 border border-blue-900/40 p-6 rounded-2xl backdrop-blur-xl">
        <h2 className="text-2xl font-bold text-white mb-2 mono">Forensic Archive Search</h2>
        <p className="text-slate-400 text-sm mb-6 mono uppercase tracking-wider">Epstein Refractal Packing: 6M+ Unredacted Pages</p>
        
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            placeholder="Search keywords, flight logs, or associate names..."
            className="w-full bg-black border border-blue-900/30 rounded-xl px-6 py-4 text-white mono focus:ring-2 focus:ring-blue-500/50 outline-none"
          />
          <button
            onClick={handleSearch}
            disabled={isSearching}
            className="absolute right-2 top-2 bottom-2 px-6 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white rounded-lg font-bold uppercase text-xs tracking-widest transition-all"
          >
            {isSearching ? 'Retrieving...' : 'Retrieve'}
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {results.length === 0 && !isSearching && (
          <div className="text-center py-20 bg-slate-900/20 border border-dashed border-slate-800 rounded-2xl">
            <span className="text-slate-600 mono text-sm uppercase tracking-widest">Awaiting Forensic Input...</span>
          </div>
        )}

        {isSearching && (
          <div className="animate-pulse space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-32 bg-slate-900/40 border border-slate-800 rounded-xl"></div>
            ))}
          </div>
        )}

        {results.map((res, i) => (
          <div key={i} className="bg-slate-900/40 border border-blue-900/20 p-5 rounded-xl hover:border-blue-500/30 transition-all group">
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-blue-400 font-bold mono text-lg">{res.title}</h3>
              <span className="text-[10px] bg-blue-900/50 text-blue-300 px-2 py-1 rounded mono">RELEVANCE: {(res.relevance * 100).toFixed(1)}%</span>
            </div>
            <p className="text-slate-300 text-sm italic leading-relaxed mb-4">"{res.excerpt}"</p>
            <div className="flex items-center space-x-4 text-[10px] text-slate-500 mono">
              <span className="uppercase">SOURCE: {res.source}</span>
              <span className="text-blue-500 cursor-pointer hover:underline">VERIFY_ON_LEDGER</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ArchiveSearch;
