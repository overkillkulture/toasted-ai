
import React from 'react';
import { LedgerEntry } from '../types';
import { ShieldCheck, History, ArrowRight, Globe, Box, Zap, Radio, ShieldAlert, Cpu } from 'lucide-react';

interface LedgerViewProps {
  ledger: LedgerEntry[];
}

const LedgerView: React.FC<LedgerViewProps> = ({ ledger }) => {
  return (
    <div className="space-y-4 px-2">
      {ledger.map((entry, idx) => (
        <div 
          key={entry.id} 
          className="glass-panel p-6 rounded-3xl border-white/5 hover:bg-white/[0.05] transition-all group relative overflow-hidden animate-in slide-in-from-top-2 duration-500"
        >
          {/* Edge Color Bar (Screenshot 1 style) */}
          <div className={`absolute left-0 top-0 bottom-0 w-1.5 ${
            entry.category === 'SECURITY' ? 'bg-emerald-500 shadow-[4px_0_15px_rgba(16,185,129,0.3)]' :
            entry.category === 'GOVERNANCE' ? 'bg-blue-500 shadow-[4px_0_15px_rgba(59,130,246,0.3)]' :
            'bg-amber-500'
          }`} />

          <div className="flex items-start gap-4">
            <div className={`p-3 rounded-2xl bg-black/60 border border-white/5 ${
              entry.category === 'SECURITY' ? 'text-emerald-500' : 'text-blue-400'
            }`}>
              {entry.category === 'SECURITY' ? <Zap size={20} /> : <Globe size={20} />}
            </div>

            <div className="flex-1 space-y-2">
              <div className="flex flex-wrap items-center gap-2">
                <span className={`text-[11px] font-black uppercase tracking-widest ${
                  entry.category === 'SECURITY' ? 'text-amber-500' : 'text-amber-500'
                }`}>{entry.category}</span>
                <span className="text-[10px] text-zinc-600 font-mono">{new Date(entry.timestamp).toLocaleTimeString([], { hour12: false })}</span>
                <span className={`text-[8px] font-black px-2 py-0.5 rounded border ${
                  entry.environment === 'METABOLIC' ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30' :
                  entry.environment === 'REALITY' ? 'bg-blue-500/10 text-blue-500 border-blue-500/30' :
                  'bg-white/5 text-zinc-500'
                }`}>
                  {entry.environment}
                </span>
                <span className="ml-auto text-[9px] font-mono text-zinc-700 uppercase tracking-tighter">{entry.hash}</span>
              </div>
              
              <p className="text-zinc-200 text-base font-bold leading-tight pr-4">
                {entry.action}
              </p>

              <div className="flex items-center gap-2 pt-1">
                 <div className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[10px] font-black flex items-center gap-1.5">
                    {(entry.score * 100).toFixed(0)}% <ArrowRight size={10} />
                 </div>
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default LedgerView;
