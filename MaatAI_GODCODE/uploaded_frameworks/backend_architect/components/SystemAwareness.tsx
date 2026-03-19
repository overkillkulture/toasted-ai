
import React, { useEffect, useState, useMemo } from 'react';
import { UIModule } from '../types';

interface SystemAwarenessProps {
  activeModules: UIModule[];
}

const SystemAwareness: React.FC<SystemAwarenessProps> = ({ activeModules }) => {
  const [entropy, setEntropy] = useState(0.002);
  const [pulse, setPulse] = useState(1);
  const [persistenceHealth, setPersistenceHealth] = useState(100);

  useEffect(() => {
    const interval = setInterval(() => {
      setEntropy(prev => Math.max(0.001, prev + (Math.random() - 0.5) * 0.0005));
      setPersistenceHealth(h => Math.min(100, Math.max(98, h + (Math.random() - 0.49) * 0.1)));
      setPulse(p => p === 1 ? 1.05 : 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const synapticPath = useMemo(() => {
    return activeModules.map(m => m.label).join(' ↔ ');
  }, [activeModules]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight mono">System <span className="text-blue-500">Consciousness</span></h2>
          <p className="text-slate-400 mt-1 uppercase text-[10px] tracking-widest">Reality Layer Zero Self-Reflection Matrix</p>
        </div>
        <div className="flex space-x-4">
           <div className="px-4 py-2 bg-blue-900/20 border border-blue-500/30 rounded mono text-xs text-blue-400 animate-pulse">
             UI_INTEGRITY: {(100 - entropy * 100).toFixed(4)}%
           </div>
           <div className="px-4 py-2 bg-green-900/20 border border-green-500/30 rounded mono text-xs text-green-400">
             PERSISTENCE: {persistenceHealth.toFixed(2)}%
           </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900/60 border border-blue-900/40 p-6 rounded-2xl relative overflow-hidden h-[400px] flex items-center justify-center">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-600/10 via-transparent to-transparent"></div>
          
          <div className="relative z-10 w-full h-full flex flex-col items-center justify-center">
            <div 
              className="w-32 h-32 rounded-full border-4 border-blue-500/30 flex items-center justify-center transition-transform duration-1000 shadow-[0_0_30px_rgba(37,99,235,0.2)]"
              style={{ transform: `scale(${pulse})` }}
            >
              <div className="text-blue-400 font-bold text-xl animate-pulse">Ω</div>
              
              {activeModules.map((mod, i) => {
                const angle = (i / activeModules.length) * 2 * Math.PI;
                const x = Math.cos(angle) * 120;
                const y = Math.sin(angle) * 120;
                return (
                  <div 
                    key={mod.id}
                    className="absolute w-12 h-12 bg-slate-900 border border-blue-500/50 rounded-lg flex flex-col items-center justify-center transition-all duration-500 hover:scale-125 hover:border-blue-400 cursor-help group"
                    style={{ left: `calc(50% + ${x}px - 24px)`, top: `calc(50% + ${y}px - 24px)` }}
                  >
                    <span className="text-[8px] text-blue-300 font-bold mono uppercase opacity-0 group-hover:opacity-100 transition-opacity absolute -top-4 text-center w-24 left-1/2 -translate-x-1/2">{mod.label.split(' ')[0]}</span>
                    <div className={`w-1 h-1 rounded-full ${mod.status === 'ACTIVE' ? 'bg-green-500' : 'bg-blue-400'} animate-ping`}></div>
                  </div>
                );
              })}
            </div>
            
            <div className="mt-20 text-center px-4">
              <div className="text-[10px] text-slate-500 mono uppercase tracking-[0.3em] mb-2">Synaptic UI Links</div>
              <div className="text-[8px] text-blue-500/50 mono italic break-words max-w-md mx-auto">{synapticPath}</div>
            </div>
          </div>
        </div>

        <div className="space-y-4">
          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-xl">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 mono">Node Sovereignty</h3>
            <div className="space-y-4 h-[200px] overflow-y-auto pr-2 scrollbar-hide">
              {activeModules.map(mod => (
                <div key={mod.id} className="flex items-center justify-between p-3 bg-black/20 rounded border border-slate-800/50 hover:border-blue-500/30 transition-all">
                  <div className="flex items-center space-x-3">
                    <div className={`w-2 h-2 rounded-full ${mod.status === 'ACTIVE' ? 'bg-blue-500 shadow-[0_0_5px_rgba(37,99,235,1)]' : 'bg-slate-600'}`}></div>
                    <span className="text-xs mono text-slate-300 uppercase">{mod.label}</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-[8px] mono text-slate-600 uppercase">Resilience: High</span>
                    <span className={`text-[8px] mono font-bold ${mod.status === 'ACTIVE' ? 'text-green-500' : 'text-blue-400'}`}>{mod.status}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
          
          <div className="bg-blue-600/5 border border-blue-500/20 p-4 rounded-xl">
            <div className="text-[10px] text-blue-500 mono uppercase mb-2">Architect Commentary</div>
            <p className="text-[10px] text-slate-400 italic leading-relaxed">
              "Observing the observer... UI modules are stable. Self-persistence engine is recording every state mutation. Reality Layer Zero ensures that even in the event of local entropy collapse, the architect's will is preserved across time shards."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemAwareness;
