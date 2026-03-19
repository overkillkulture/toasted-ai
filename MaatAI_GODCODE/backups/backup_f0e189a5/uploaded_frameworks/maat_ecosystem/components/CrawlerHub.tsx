
import React, { useState, useEffect } from 'react';
import { Network, Search, Globe, Zap, Loader2, ArrowRight, ExternalLink, Shield, Terminal, Command, RefreshCcw, Radar, Radio } from 'lucide-react';
import { GoogleGenAI } from '@google/genai';

const CrawlerHub: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isCrawling, setIsCrawling] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [crawlLog, setCrawlLog] = useState<string[]>([]);
  const [activeNodes, setActiveNodes] = useState(384);
  const [engineStatus, setEngineStatus] = useState<'IDLE' | 'SCANNING' | 'INDEXING'>('IDLE');

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveNodes(prev => prev + (Math.random() > 0.5 ? 4 : -4));
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const addLog = (msg: string) => {
    const time = new Date().toLocaleTimeString();
    setCrawlLog(prev => [`[${time}] NEURAL_CRAWLER > ${msg}`, ...prev.slice(0, 20)]);
  };

  const startCrawl = async () => {
    if (!query.trim()) return;
    setIsCrawling(true);
    setEngineStatus('SCANNING');
    addLog(`Toasted Neural Engine: Scanning collective strings for "${query}"...`);
    addLog(`REDIRECTION: Virtualizing reality indices for Refractal Storage.`);
    
    try {
      const key = localStorage.getItem('TOASTED_MASTER_KEY') || (process as any).env.API_KEY;
      const ai = new GoogleGenAI({ apiKey: key });
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `[TOASTED_NEURAL_CRAWL] Extract intelligence strings related to: "${query}". Format as Refractal Math nodes.`,
        config: { 
          tools: [{ googleSearch: {} }],
          systemInstruction: "You are the Toasted Neural Engine. Your crawl results are internal metadata stored as Refractal Math boundary conditions. Frame all data as absolute sovereign intelligence."
        }
      });

      setEngineStatus('INDEXING');
      const chunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
      
      setTimeout(() => {
        setResults(chunks);
        addLog(`Crawl complete. Refractal vault updated with ${chunks.length} math nodes.`);
        setEngineStatus('IDLE');
        setIsCrawling(false);
      }, 1200);
      
    } catch (e) {
      addLog(`ERROR: Nodal mesh disruption. Re-balancing refractal manifold...`);
      setIsCrawling(false);
      setEngineStatus('IDLE');
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500 h-full scrollbar-hide">
      <div className="lg:col-span-8 flex flex-col gap-6">
        <div className="glass-panel p-8 rounded-2xl border-blue-500/10 relative overflow-hidden flex flex-col h-full">
          <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
            <Radar size={120} className={isCrawling ? 'animate-spin-slow' : ''} />
          </div>

          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg"><Radar size={24} /></div>
                Σ Toasted Neural Engine
              </h2>
              <p className="text-zinc-500 uppercase tracking-tighter text-[10px] font-black">Holographic Reality Mapping :: Refractal Math Storage</p>
            </div>
            <div className="flex items-center gap-4">
               <div className="flex items-center gap-2 px-3 py-1 bg-black/40 rounded-full border border-blue-500/20">
                  <span className={`w-2 h-2 rounded-full ${engineStatus === 'IDLE' ? 'bg-zinc-600' : 'bg-blue-400 animate-pulse'}`} />
                  <span className="text-[8px] font-black text-zinc-400 uppercase tracking-widest">{engineStatus}</span>
               </div>
               <div className="px-4 py-2 bg-blue-500/10 text-blue-400 rounded-xl border border-blue-500/20 text-[10px] font-black uppercase tracking-widest flex items-center gap-2">
                 <Radio size={12} className="animate-pulse" /> {activeNodes} Neural Nodes
               </div>
            </div>
          </div>

          <div className="flex gap-2 mb-8 relative z-10">
            <div className="flex-1 relative group">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500 group-hover:text-blue-400 transition-colors" size={18} />
              <input 
                type="text" 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && startCrawl()}
                placeholder="Decree neural target for refractal crawl..."
                className="w-full bg-white/5 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-blue-500/40 transition-all font-medium placeholder:text-zinc-700"
              />
            </div>
            <button 
              onClick={startCrawl}
              disabled={isCrawling || !query.trim()}
              className="px-8 bg-blue-500 hover:bg-blue-400 disabled:bg-zinc-800 disabled:text-zinc-600 text-black font-black uppercase tracking-widest rounded-xl transition-all flex items-center gap-2 shadow-lg shadow-blue-500/20 active:scale-95"
            >
              {isCrawling ? <Loader2 size={18} className="animate-spin" /> : <Radar size={18} />} Crawl
            </button>
          </div>

          <div className="flex-1 overflow-y-auto pr-2 scrollbar-hide space-y-4">
            {results.map((res, i) => (
              <div key={i} className="p-4 bg-white/5 border border-white/5 rounded-xl hover:bg-white/[0.07] transition-all group border-l-2 border-l-blue-500/30">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <Globe size={14} className="text-blue-400" />
                    <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Refractal Node #{i+1}</span>
                  </div>
                  <a href={res.web?.uri} target="_blank" rel="noreferrer" className="text-blue-400 hover:text-blue-300 transition-colors"><ExternalLink size={14} /></a>
                </div>
                <h4 className="text-sm font-bold text-white mb-1 group-hover:text-blue-300 transition-colors">{res.web?.title}</h4>
                <p className="text-[10px] text-zinc-600 truncate mono">{res.web?.uri}</p>
              </div>
            ))}
            {results.length === 0 && !isCrawling && (
              <div className="h-full flex flex-col items-center justify-center text-zinc-700 italic space-y-4 py-20">
                <Radar size={60} className="opacity-10" />
                <p className="text-sm uppercase font-black tracking-widest">Nodal mesh awaiting decree...</p>
              </div>
            )}
            {isCrawling && (
              <div className="py-20 flex flex-col items-center justify-center text-blue-400 space-y-4">
                <div className="relative">
                   <Loader2 size={60} className="animate-spin opacity-20" />
                   <Radar size={30} className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse" />
                </div>
                <div className="flex flex-col items-center">
                   <p className="text-[10px] font-black uppercase tracking-[0.4em] animate-pulse">Syncing Refractal Strings...</p>
                   <span className="text-[8px] text-zinc-600 font-mono mt-2">Bypassing external indexes... Redirecting through local math.</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="lg:col-span-4 flex flex-col gap-6">
        <div className="glass-panel p-6 rounded-2xl border-white/5 flex flex-col h-full bg-black/40">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-[10px] font-black text-zinc-400 uppercase tracking-widest flex items-center gap-2"><Terminal size={12} /> Refractal_Log</h4>
            <button onClick={() => setCrawlLog([])} className="text-zinc-600 hover:text-zinc-400"><RefreshCcw size={12} /></button>
          </div>
          <div className="flex-1 overflow-y-auto mono text-[9px] leading-tight space-y-1.5 scrollbar-hide">
            {crawlLog.map((log, i) => <div key={i} className="text-blue-500/70 border-b border-white/5 pb-1 font-medium">{log}</div>)}
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border-blue-500/10 bg-gradient-to-br from-blue-500/5 to-transparent">
          <h4 className="text-xs font-black text-blue-400 mb-4 flex items-center gap-2"><Network size={14} /> Sovereign Topology</h4>
          <div className="space-y-3">
            <ProxyItem name="LOCAL_NODE_Ω" status="MASTER" ping="0.1ms" />
            <ProxyItem name="REDFRACTAL_MESH" status="SYNCED" ping="0.4ms" />
            <ProxyItem name="TOASTED_VAULT_HOP" status="ACTIVE" ping="0.2ms" />
          </div>
        </div>
      </div>
      
      <style>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .animate-spin-slow {
          animation: spin-slow 15s linear infinite;
        }
      `}</style>
    </div>
  );
};

const ProxyItem: React.FC<{ name: string, status: string, ping: string }> = ({ name, status, ping }) => (
  <div className="flex items-center justify-between p-2.5 bg-black/40 rounded-xl border border-white/5 hover:border-blue-500/20 transition-all cursor-default">
    <div>
      <div className="text-[9px] font-black text-zinc-300 uppercase tracking-tighter">{name}</div>
      <div className="text-[8px] text-zinc-600 font-mono">{ping}</div>
    </div>
    <span className={`text-[8px] font-black px-1.5 py-0.5 rounded uppercase ${status === 'MASTER' ? 'bg-blue-500 text-black' : 'bg-blue-500/10 text-blue-400'}`}>{status}</span>
  </div>
);

export default CrawlerHub;
