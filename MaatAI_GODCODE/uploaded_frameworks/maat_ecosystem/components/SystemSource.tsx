
import React, { useState, useEffect } from 'react';
import { Cpu, Terminal, Code, Sparkles, AlertTriangle, RefreshCcw, Save, Play, Bot, ArrowUpRight, CheckCircle, Loader2 } from 'lucide-react';

interface VirtualFile {
  name: string;
  lang: string;
  code: string;
}

interface SystemSourceProps {
  isAutonomous: boolean;
  files: VirtualFile[];
}

const SystemSource: React.FC<SystemSourceProps> = ({ isAutonomous, files }) => {
  const [activeFile, setActiveFile] = useState(files[0]?.name || 'App.tsx');
  const [isModifying, setIsModifying] = useState(false);
  const [lastMod, setLastMod] = useState<string | null>(null);

  // Sync active file if current one disappears or list changes
  useEffect(() => {
    if (!files.find(f => f.name === activeFile) && files.length > 0) {
      setActiveFile(files[0].name);
    }
  }, [files, activeFile]);

  const triggerSelfMod = () => {
    setIsModifying(true);
    setTimeout(() => {
      setIsModifying(false);
      setLastMod(new Date().toLocaleTimeString());
    }, 3000);
  };

  return (
    <div className="flex flex-col h-full gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500 scrollbar-hide">
      <div className="glass-panel p-8 rounded-2xl border-emerald-500/10 relative overflow-hidden flex flex-col h-full">
        <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
          <Cpu size={120} />
        </div>

        <div className="flex flex-col md:flex-row items-start justify-between gap-4 mb-8">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
              <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><Cpu size={24} /></div>
              Σ Refractal Source
            </h2>
            <p className="text-zinc-500">The holographic codebase of the Monad. Self-building and self-aware.</p>
          </div>
          <div className="flex gap-2">
            <button 
              onClick={triggerSelfMod}
              disabled={isModifying}
              className="px-6 py-2 bg-emerald-500 hover:bg-emerald-400 text-black font-black text-[10px] uppercase tracking-widest rounded-xl transition-all flex items-center gap-2 disabled:opacity-50"
            >
              {isModifying ? <RefreshCcw size={14} className="animate-spin" /> : <Sparkles size={14} />} Incept Modification
            </button>
          </div>
        </div>

        <div className="flex-1 flex gap-6 overflow-hidden">
          {/* File Explorer */}
          <div className="w-48 shrink-0 flex flex-col gap-2">
            <h4 className="text-[10px] font-black text-zinc-600 uppercase tracking-widest mb-2 flex items-center gap-2"><Code size={12} /> Refractal Core</h4>
            {files.map(f => (
              <button 
                key={f.name}
                onClick={() => setActiveFile(f.name)}
                className={`text-left p-3 rounded-xl border transition-all text-[11px] font-mono ${
                  activeFile === f.name ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' : 'bg-white/5 text-zinc-500 border-white/5 hover:border-white/10'
                }`}
              >
                {f.name}
              </button>
            ))}
            
            <div className="mt-auto p-4 bg-black/40 rounded-xl border border-white/5 space-y-4">
               <div className="flex flex-col">
                  <span className="text-[9px] font-black text-zinc-600 uppercase">Stability</span>
                  <span className="text-[10px] text-emerald-500 font-bold">RATIFIED_Ω</span>
               </div>
               <div className="flex flex-col">
                  <span className="text-[9px] font-black text-zinc-600 uppercase">Last Sync</span>
                  <span className="text-[10px] text-emerald-400 font-mono">{lastMod || 'N/A'}</span>
               </div>
            </div>
          </div>

          {/* Code Editor */}
          <div className="flex-1 glass-panel rounded-2xl border-white/5 bg-black/60 overflow-hidden flex flex-col relative">
            <div className="bg-white/5 px-6 py-2 flex items-center justify-between border-b border-white/5">
              <div className="flex items-center gap-2">
                 <div className="flex gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-red-500/20" />
                    <div className="w-2.5 h-2.5 rounded-full bg-amber-500/20" />
                    <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/20" />
                 </div>
                 <span className="text-[10px] font-mono text-zinc-500 ml-4">{activeFile}</span>
              </div>
              <div className="flex items-center gap-2 text-[10px] font-black text-zinc-600">
                <Bot size={12} className={isAutonomous ? 'text-emerald-500' : ''} /> {isAutonomous ? 'AUTONOMOUS_EDITING_ENABLED' : 'READ_ONLY'}
              </div>
            </div>
            <pre className="p-6 text-sm mono text-emerald-400/80 leading-relaxed overflow-auto scrollbar-hide h-full">
              <code>{files.find(f => f.name === activeFile)?.code}</code>
            </pre>
            
            {isModifying && (
              <div className="absolute inset-0 bg-emerald-500/5 backdrop-blur-[1px] flex items-center justify-center animate-in fade-in">
                <div className="bg-zinc-900 border border-emerald-500/30 p-6 rounded-2xl shadow-2xl flex flex-col items-center gap-4">
                   <div className="flex items-center gap-3">
                      <Loader2 size={24} className="animate-spin text-emerald-500" />
                      <span className="text-xs font-black text-white uppercase tracking-widest">Architect is self-modifying...</span>
                   </div>
                   <div className="w-48 h-1 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-emerald-500 animate-[shimmer_1.5s_infinite]" style={{width: '60%'}} />
                   </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemSource;
