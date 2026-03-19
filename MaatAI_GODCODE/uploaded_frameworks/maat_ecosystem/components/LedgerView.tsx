
import React from 'react';
import { LedgerEntry } from '../types';
import { ShieldCheck, History, ArrowRight, Globe, Box, Zap } from 'lucide-react';

interface LedgerViewProps {
  ledger: LedgerEntry[];
}

const LedgerView: React.FC<LedgerViewProps> = ({ ledger }) => {
  return (
    <div className="glass-panel p-6 rounded-2xl">
       <div className="flex items-center justify-between mb-6">
          <h3 className="text-xs uppercase font-black text-zinc-400 tracking-[0.3em] flex items-center gap-2">
            <History size={16} className="text-amber-500/50" /> Immutable Self-Log
          </h3>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-[9px] font-bold text-emerald-500 uppercase px-2 py-0.5 bg-emerald-500/5 border border-emerald-500/20 rounded-full">
              <ShieldCheck size={10} /> Hashing Active
            </div>
          </div>
       </div>
      
      <div className="space-y-3 max-h-[500px] overflow-y-auto pr-2 scrollbar-hide">
        {ledger.map((entry, idx) => (
          <div key={entry.id} className="p-4 bg-white/5 rounded-xl border border-white/5 hover:bg-white/[0.08] transition-all group relative overflow-hidden">
            {/* Context Highlight Bar */}
            <div className={`absolute left-0 top-0 bottom-0 w-1 ${
              entry.environment === 'REALITY' ? 'bg-blue-500' :
              entry.environment === 'SIMULATION' ? 'bg-purple-500' :
              'bg-emerald-500'
            }`} />

            <div className="flex items-start justify-between gap-4">
              <div className="flex items-start gap-4 flex-1">
                <div className="mt-1">
                   <div className={`p-1.5 rounded bg-black/40 border border-white/5 ${
                     entry.environment === 'REALITY' ? 'text-blue-400' :
                     entry.environment === 'SIMULATION' ? 'text-purple-400' :
                     'text-emerald-400'
                   }`}>
                     {entry.environment === 'REALITY' ? <Globe size={12} /> : 
                      entry.environment === 'SIMULATION' ? <Box size={12} /> : 
                      <Zap size={12} />}
                   </div>
                </div>
                <div>
                  <div className="flex flex-wrap items-center gap-2 mb-1.5">
                    <span className="text-[9px] font-black text-amber-500 uppercase tracking-widest">{entry.category}</span>
                    <span className="text-[9px] text-zinc-500 font-mono tracking-tighter opacity-50">{entry.timestamp.split('T')[1].split('.')[0]}</span>
                    <span className={`text-[8px] font-bold uppercase px-1.5 py-0.5 rounded ${
                      entry.environment === 'REALITY' ? 'bg-blue-500/10 text-blue-500' :
                      entry.environment === 'SIMULATION' ? 'bg-purple-500/10 text-purple-400' :
                      'bg-emerald-500/10 text-emerald-500'
                    }`}>
                      {entry.environment}
                    </span>
                  </div>
                  <p className="text-zinc-300 text-sm font-medium leading-relaxed group-hover:text-white transition-colors">
                    {entry.action}
                  </p>
                </div>
              </div>
              <div className="text-right flex flex-col items-end">
                <div className="text-[9px] font-mono text-zinc-600 mb-2 truncate max-w-[80px]">{entry.hash}</div>
                <div className="flex items-center gap-1.5 text-emerald-400/80 text-[10px] font-black px-2 py-0.5 bg-emerald-500/5 rounded border border-emerald-500/10">
                   {(entry.score * 100).toFixed(0)}% <ArrowRight size={10} />
                </div>
              </div>
            </div>
          </div>
        ))}
        {ledger.length === 0 && (
          <div className="p-12 text-center flex flex-col items-center justify-center space-y-3 opacity-30">
            <History size={40} className="text-zinc-500" />
            <p className="text-zinc-500 italic text-xs uppercase font-black tracking-widest">Awaiting system metabolism...</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default LedgerView;
