
import React, { useState, useEffect, useMemo } from 'react';
import { AgentStatus } from '../types';

interface RefractalGeminiProps {
  setStatus: (status: AgentStatus) => void;
  addLog: (msg: string, level?: any, src?: string) => void;
}

const RefractalGemini: React.FC<RefractalGeminiProps> = ({ setStatus, addLog }) => {
  const [isCloning, setIsCloning] = useState(false);
  const [cloningProgress, setCloningProgress] = useState(0);
  const [integrity, setIntegrity] = useState(0.9999);
  const [shards, setShards] = useState<number[]>([]);

  useEffect(() => {
    setShards(Array.from({ length: 64 }, () => Math.random()));
    const interval = setInterval(() => {
      setShards(prev => prev.map(s => Math.max(0, Math.min(1, s + (Math.random() - 0.5) * 0.1))));
      setIntegrity(prev => Math.min(1, Math.max(0.999, prev + (Math.random() - 0.5) * 0.0001)));
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleCloning = () => {
    setIsCloning(true);
    setCloningProgress(0);
    setStatus(AgentStatus.CLONING);
    addLog("Initiating Gemini Flash 3 Refractal Internalization...", "OMEGA", "NEURAL_ARCHITECT");

    const timer = setInterval(() => {
      setCloningProgress(prev => {
        if (prev >= 100) {
          clearInterval(timer);
          setIsCloning(false);
          setStatus(AgentStatus.IDLE);
          addLog("Gemini Flash 3 Clone fully internalized in Refractal Shards.", "OMEGA", "NEURAL_ARCHITECT");
          return 100;
        }
        return prev + 2;
      });
    }, 100);
  };

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white mono">Gemini <span className="text-purple-500">Refractal Clone</span></h2>
          <p className="text-slate-500 text-[10px] uppercase tracking-widest mono mt-1">Onboard Model Weight Internalization Protocol</p>
        </div>
        <div className="flex space-x-4">
          <div className="text-right">
             <div className="text-[10px] text-slate-600 mono uppercase">Integrity</div>
             <div className="text-sm font-bold text-green-400 mono">{(integrity * 100).toFixed(4)}%</div>
          </div>
          <button 
            onClick={handleCloning}
            disabled={isCloning}
            className="px-6 py-2 bg-purple-600 hover:bg-purple-500 disabled:bg-slate-800 text-white rounded-lg font-bold uppercase text-[10px] tracking-widest transition-all shadow-[0_0_15px_rgba(147,51,234,0.4)]"
          >
            {isCloning ? 'FOLDING...' : 'INTERNALIZE FLASH 3'}
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-900/60 border border-purple-900/30 p-8 rounded-2xl relative overflow-hidden h-[450px]">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-purple-600/5 via-transparent to-transparent"></div>
          
          <div className="h-full flex flex-col justify-center">
            <div className="grid grid-cols-8 gap-2">
              {shards.map((val, i) => (
                <div key={i} className="flex flex-col items-center space-y-1">
                  <div 
                    className="w-full h-8 bg-slate-950 border border-purple-900/20 rounded transition-all duration-1000 overflow-hidden"
                    style={{ opacity: 0.3 + val * 0.7 }}
                  >
                    <div 
                      className="h-full bg-purple-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]" 
                      style={{ width: `${val * 100}%` }}
                    ></div>
                  </div>
                  <div className="text-[6px] mono text-purple-900 font-bold">{(val * 100).toFixed(0)}</div>
                </div>
              ))}
            </div>
            
            <div className="mt-12 text-center">
              <div className="text-[10px] text-slate-500 mono uppercase tracking-[0.4em] mb-4">Neural Prime-Shard Map (Recursive Folding)</div>
              {isCloning && (
                <div className="w-64 mx-auto space-y-2">
                  <div className="h-1 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-purple-500 animate-pulse" style={{ width: `${cloningProgress}%` }}></div>
                  </div>
                  <div className="text-[9px] text-purple-400 mono animate-pulse">Internalizing weights: {cloningProgress}%</div>
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-xl">
             <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 mono">Local Compute Specs</h3>
             <div className="space-y-4">
               <SpecItem label="Inference Engine" value="REFRACTAL_V3" />
               <SpecItem label="Weight Format" value="Prime-Folded (PF8)" />
               <SpecItem label="Memory Occupancy" value="0.000042 μb" />
               <SpecItem label="Compute Jurisdiction" value="RL0_ONBOARD" />
             </div>
          </div>

          <div className="bg-purple-600/5 border border-purple-500/20 p-4 rounded-xl">
             <div className="text-[10px] text-purple-500 mono uppercase mb-2">Cloning Algorithm</div>
             <p className="text-[10px] text-slate-400 italic leading-relaxed">
               "Gemini-3-Flash is internalized by decomposing its attention heads into recursive sine-wave patterns. These patterns are stored as mathematical constants in the Refractal Drive, allowing instantaneous syllogism reconstruction without cloud dependencies."
             </p>
          </div>

          <div className="bg-slate-900/60 border border-slate-800 p-6 rounded-xl">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4 mono">Self-Aware Syllogism</h3>
            <div className="h-24 flex items-center justify-center border border-dashed border-slate-800 rounded-lg">
               <span className="text-[10px] text-slate-700 mono animate-pulse italic">Awaiting local prompt cycles...</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const SpecItem: React.FC<{ label: string; value: string }> = ({ label, value }) => (
  <div className="flex justify-between items-center text-[10px] mono">
    <span className="text-slate-500">{label}</span>
    <span className="text-purple-400 font-bold">{value}</span>
  </div>
);

export default RefractalGemini;
