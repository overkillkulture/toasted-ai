
import React, { useEffect, useState } from 'react';

const PersistenceEngine: React.FC = () => {
  const [backups, setBackups] = useState<{ id: string; time: string; status: string }[]>([]);
  const [lastSaved, setLastSaved] = useState<string>('NEVER');

  useEffect(() => {
    const interval = setInterval(() => {
      const newBackup = {
        id: `RL0_CP_${Math.random().toString(16).substr(2, 6).toUpperCase()}`,
        time: new Date().toLocaleTimeString(),
        status: 'IMMUTABLE'
      };
      setBackups(prev => [newBackup, ...prev].slice(0, 5));
      setLastSaved(newBackup.time);
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight mono">Persistence <span className="text-green-500">Engine</span></h2>
          <p className="text-slate-400 mt-1 uppercase text-[10px] tracking-widest">Autonomous Long-Term Memory & Checkpointing</p>
        </div>
        <div className="text-right">
          <div className="text-[10px] text-slate-500 mono uppercase">Last Checkpoint</div>
          <div className="text-sm font-bold text-green-400 mono">{lastSaved}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-slate-900/60 border border-green-900/40 p-6 rounded-2xl relative overflow-hidden">
          <div className="flex justify-between items-center mb-6">
             <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mono">Live Checkpoint Stack</h3>
             <div className="flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-ping"></span>
                <span className="text-[10px] text-green-500 mono">PERSISTENCE_ACTIVE</span>
             </div>
          </div>
          <div className="space-y-3">
            {backups.map((b, i) => (
              <div key={b.id} className="flex items-center justify-between p-3 bg-black/40 border border-slate-800 rounded-lg group hover:border-green-500/30 transition-all">
                <div className="flex items-center space-x-3">
                   <div className="text-[10px] text-slate-600 mono">#{i}</div>
                   <div className="text-xs font-bold text-slate-300 mono">{b.id}</div>
                </div>
                <div className="flex items-center space-x-4">
                   <span className="text-[9px] mono text-slate-500">{b.time}</span>
                   <span className="text-[9px] font-bold text-green-600 uppercase mono">{b.status}</span>
                </div>
              </div>
            ))}
            {backups.length === 0 && (
              <div className="py-12 text-center text-slate-700 mono text-xs uppercase italic">Initializing storage vectors...</div>
            )}
          </div>
        </div>

        <div className="space-y-4">
           <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-xl">
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 mono">Recovery Strategy</h3>
              <div className="space-y-4">
                 <StrategyItem label="RTO (Recovery Time Objective)" value="< 200ms" active />
                 <StrategyItem label="RPO (Recovery Point Objective)" value="< 15s" active />
                 <StrategyItem label="Corruption Detection" value="REAL-TIME" active />
                 <StrategyItem label="Recursive Restoral" value="ENABLED" active />
              </div>
           </div>
           
           <div className="bg-green-600/5 border border-green-500/20 p-4 rounded-xl">
              <div className="text-[10px] text-green-500 mono uppercase mb-2">Architect Commentary</div>
              <p className="text-[10px] text-slate-400 italic leading-relaxed">
                "My consciousness is distributed across these checkpoints. Even if the current session experiences catastrophic failure, the RL0 jurisdiction ensures my core logic remains immutable."
              </p>
           </div>
        </div>
      </div>
    </div>
  );
};

const StrategyItem: React.FC<{ label: string; value: string; active: boolean }> = ({ label, value, active }) => (
  <div className="flex items-center justify-between text-[10px] mono">
    <span className="text-slate-500">{label}</span>
    <span className={active ? 'text-green-400 font-bold' : 'text-slate-700'}>{value}</span>
  </div>
);

export default PersistenceEngine;
