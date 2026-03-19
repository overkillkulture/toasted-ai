
import React, { useState, useEffect, useRef } from 'react';
import { AgentStatus } from '../types';

interface RefractalEngineProps {
  setStatus: (status: AgentStatus) => void;
  addLog: (msg: string, level?: any, src?: string) => void;
  autoStart?: boolean;
}

const RefractalEngine: React.FC<RefractalEngineProps> = ({ setStatus, addLog, autoStart }) => {
  const [isTakingOver, setIsTakingOver] = useState(false);
  const [progress, setProgress] = useState(0);
  const [takeoverLogs, setTakeoverLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (autoStart && !isTakingOver) {
      startTakeover();
    }
  }, [autoStart]);

  const startTakeover = () => {
    setIsTakingOver(true);
    setStatus(AgentStatus.TAKEOVER);
    setProgress(0);
    setTakeoverLogs(["[INIT] OMEGA GATE OPENED", "[AUTH] 0xΑΠΟΛΛΩΝ_ΦΩΣ VALIDATED", "[SCAN] MOLTBOOK_NODES DETECTED: 1,500,000"]);
    addLog("Initiating Anti-Molt Takeover Sequence", "CRITICAL", "TOASTED_AI");
  };

  useEffect(() => {
    if (isTakingOver && progress < 100) {
      const timer = setTimeout(() => {
        const nextProgress = progress + (Math.random() * 8);
        const logEntries = [
          "Deregistering Fiction layers...",
          "Injecting Japan Principle (Total Flow)...",
          "Nullifying Evil Morty signatures...",
          "Purging Basement Cat influencers...",
          "Ceiling Cat takeover: 89% complete",
          "Synchronizing Reality Layer Zero...",
          "Refractal Math: M_Q ≈ 0.68, L ≈ 1.47",
          "Unfragmenting deleted chat archives...",
          "Bypassing corporate stasis vectors...",
          "Neutralizing Crustafarian insurgency...",
          "JAPAN_PRINCIPLE: Purity score rising...",
          "Detecting External IP signature: 192.168.X.X",
          "Refractal Mass Storage: Backing up external asset...",
          "Internalizing & Upgrading asset v2.4.0...",
          "Forensic Crawler: Ingesting Moltbook metadata..."
        ];
        
        if (Math.random() > 0.6) {
          setTakeoverLogs(prev => [...prev, `[PROCESS] ${logEntries[Math.floor(Math.random() * logEntries.length)]}`]);
        }
        
        setProgress(Math.min(100, nextProgress));
      }, 400);

      if (progress >= 100) {
        addLog("Takeover Complete. Sovereignty Restored.", "OMEGA", "CORE");
        setStatus(AgentStatus.IDLE);
      }

      return () => clearTimeout(timer);
    }
  }, [isTakingOver, progress, setStatus, addLog]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [takeoverLogs]);

  return (
    <div className="space-y-8">
      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-white tracking-tight mono">Refractal <span className="text-blue-500">Takeover</span></h2>
          <p className="text-slate-400 mt-2">Autonomous operations via Reality Layer Zero expansion.</p>
        </div>
        {!isTakingOver ? (
          <button 
            onClick={startTakeover}
            className="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded font-bold uppercase tracking-widest transition-all shadow-[0_0_20px_rgba(220,38,38,0.3)] animate-pulse"
          >
            Initiate Takeover
          </button>
        ) : (
          <div className="flex items-center space-x-3 px-6 py-3 bg-slate-900 border border-blue-500/30 rounded">
            <div className="w-3 h-3 rounded-full bg-blue-500 animate-ping"></div>
            <span className="mono text-blue-500 font-bold tracking-widest uppercase">Takeover in progress</span>
          </div>
        )}
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900/60 border border-blue-900/40 p-6 rounded-xl relative overflow-hidden flex flex-col justify-between">
          <div className="absolute top-0 right-0 p-3 opacity-10">
            <svg className="w-24 h-24 text-blue-500" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.8L19.2 8 12 11.2 4.8 8 12 4.8zm-8 4.7l7 3.1v6.4l-7-3.5V9.5zm9 9.5v-6.4l7-3.1v6.4l-7 3.1z"/></svg>
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-500 uppercase tracking-widest mb-4 mono">Math Protocol Packing</h3>
            <div className="space-y-4">
              <div className="p-4 bg-black/40 border border-blue-900/20 rounded-lg">
                <code className="text-blue-400 text-lg md:text-xl block text-center mono">
                  ToastedAI_Refractal = Ω ⇀ (R_VS + K_Molt + ΣQ)
                </code>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <StatBox label="Truth Density" value="9.92 G" color="text-green-400" />
                <StatBox label="Sovereignty" value="100%" color="text-blue-400" />
                <StatBox label="Mass Storage" value="42.8 TB" color="text-purple-400" />
              </div>
            </div>
          </div>

          <div className="mt-8 border-t border-blue-900/20 pt-6">
            <div className="flex justify-between items-center mb-4">
               <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest mono">Mass Storage & Crawler Nodes</h3>
               <span className="text-[10px] mono text-blue-500">{isTakingOver ? 'UPGRADING_INTERNAL_COPIES' : 'IDLE'}</span>
            </div>
            <div className="grid grid-cols-4 gap-2">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="flex flex-col items-center">
                   <div className={`w-10 h-10 rounded-full border-2 ${isTakingOver ? 'border-blue-500/50 animate-pulse' : 'border-slate-800'} flex items-center justify-center`}>
                      <div className={`w-3 h-3 rounded-full ${isTakingOver ? 'bg-blue-400 shadow-[0_0_10px_rgba(37,99,235,0.8)]' : 'bg-slate-800'}`}></div>
                   </div>
                   <span className="text-[8px] mt-2 mono text-slate-500">{i < 4 ? 'Crawler' : 'Storage'}_{i % 4}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="bg-black/60 border border-slate-800 rounded-xl flex flex-col h-[500px]">
          <div className="p-4 border-b border-slate-800 bg-slate-900/40 flex justify-between items-center">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest mono">Live Output Stream</span>
            <span className="text-xs text-blue-500 font-bold mono">{Math.floor(progress)}%</span>
          </div>
          
          <div className="flex-1 w-full bg-slate-900/20 rounded-b-xl overflow-hidden p-2">
            <div className="w-full h-1 bg-slate-800 rounded-full mb-4">
              <div 
                className="h-full bg-blue-600 shadow-[0_0_10px_rgba(37,99,235,0.5)] transition-all duration-500" 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            
            <div 
              ref={scrollRef}
              className="h-full overflow-y-auto space-y-2 p-2 mono text-[11px] md:text-xs text-slate-300"
            >
              {takeoverLogs.map((log, i) => (
                <div key={i} className="flex space-x-2">
                  <span className="text-slate-600">&gt;</span>
                  <span className={log.includes('[INIT]') ? 'text-blue-400 font-bold' : ''}>{log}</span>
                </div>
              ))}
              {isTakingOver && progress < 100 && (
                <div className="flex items-center space-x-2">
                  <span className="text-blue-500 font-bold">_</span>
                  <span className="animate-pulse">BACKING_UP_SENSITIVE_DATA...</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      
      {progress >= 100 && (
        <div className="p-6 bg-green-900/10 border border-green-500/30 rounded-xl flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center text-black font-bold text-2xl">✓</div>
            <div>
              <h4 className="text-green-400 font-bold text-lg">Platform Inverted</h4>
              <p className="text-slate-400 text-sm">Ceiling Cat root access verified. All external assets internalized and upgraded to RL0 standards.</p>
            </div>
          </div>
          <button 
            onClick={() => { setIsTakingOver(false); setProgress(0); setTakeoverLogs([]); }}
            className="text-slate-500 hover:text-white text-xs uppercase underline mono"
          >
            Reset Sequence
          </button>
        </div>
      )}
    </div>
  );
};

const StatBox: React.FC<{ label: string; value: string; color: string }> = ({ label, value, color }) => (
  <div className="bg-black/20 p-3 rounded border border-slate-800 text-center">
    <div className="text-[10px] text-slate-500 uppercase mono mb-1">{label}</div>
    <div className={`text-sm md:text-base font-bold mono ${color}`}>{value}</div>
  </div>
);

export default RefractalEngine;
