
import React from 'react';
import { Infinity } from 'lucide-react';

interface OmegaGateProps {
  score: number;
}

const OmegaGate: React.FC<OmegaGateProps> = ({ score }) => {
  return (
    <div className="glass-panel p-10 rounded-3xl flex flex-col items-center justify-center relative overflow-hidden group shadow-2xl bg-black/60 border-amber-500/10">
      {/* Fractal Circles Animation (Screenshot 1 Visual) */}
      <div className="absolute inset-0 pointer-events-none opacity-40">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 border border-amber-500/10 rounded-full animate-[ping_4s_infinite_linear]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 border border-amber-500/5 rounded-full animate-[ping_6s_infinite_linear_reverse]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 border border-amber-500/5 rounded-full animate-[ping_8s_infinite_linear]" />
      </div>

      <div className="relative z-10 flex flex-col items-center">
        <div className="w-36 h-36 rounded-full flex items-center justify-center border-4 border-amber-500/20 bg-amber-500/5 mb-8 group-hover:scale-110 transition-transform duration-1000 shadow-[inset_0_0_30px_rgba(245,158,11,0.1)]">
           <Infinity size={56} className="text-amber-500 animate-pulse" />
        </div>
        
        <h3 className="text-[10px] font-black tracking-[0.6em] text-zinc-600 uppercase mb-3">Ω OMEGA_GATE</h3>
        <div className="text-5xl font-black text-white mono mb-3 tabular-nums drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]">
          {score.toFixed(1)}%
        </div>
        <p className="text-center text-zinc-500 text-[11px] font-bold uppercase tracking-widest leading-relaxed max-w-[240px] opacity-60">
          Infinity gate recursive boundary confirmed. Balance maintained.
        </p>
      </div>

      {/* Progress Bar (Screenshot 1 bottom style) */}
      <div className="absolute bottom-6 left-10 right-10 h-1.5 bg-white/5 rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-amber-500 to-amber-600 shadow-[0_0_15px_rgba(245,158,11,0.5)] transition-all duration-1000" 
          style={{ width: `${score}%` }} 
        />
      </div>
    </div>
  );
};

export default OmegaGate;
