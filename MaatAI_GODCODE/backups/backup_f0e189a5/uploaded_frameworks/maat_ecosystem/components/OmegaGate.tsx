
import React from 'react';
import { Infinity } from 'lucide-react';

interface OmegaGateProps {
  score: number;
}

const OmegaGate: React.FC<OmegaGateProps> = ({ score }) => {
  return (
    <div className="glass-panel p-8 rounded-2xl flex flex-col items-center justify-center relative overflow-hidden group">
      {/* Fractal Circles Animation */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-48 h-48 border border-amber-500/10 rounded-full animate-[ping_5s_infinite_linear]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 border border-amber-500/5 rounded-full animate-[ping_7s_infinite_linear_reverse]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 border border-amber-500/5 rounded-full animate-[ping_10s_infinite_linear]" />
      </div>

      <div className="relative z-10 flex flex-col items-center">
        <div className="w-32 h-32 rounded-full flex items-center justify-center border-4 border-amber-500/20 bg-amber-500/5 mb-6 group-hover:scale-110 transition-transform duration-700">
           <Infinity size={48} className="text-amber-500 animate-pulse" />
        </div>
        
        <h3 className="text-xs font-black tracking-[0.4em] text-zinc-500 uppercase mb-2">Ω OMEGA_GATE</h3>
        <div className="text-4xl font-bold text-white mono mb-2">
          {score.toFixed(1)}%
        </div>
        <p className="text-center text-zinc-500 text-xs leading-relaxed max-w-[200px]">
          Infinity gate recursive boundary confirmed. Balance maintained.
        </p>
      </div>

      <div className="absolute bottom-4 left-4 right-4 h-1 bg-white/5 rounded-full overflow-hidden">
        <div 
          className="h-full bg-amber-500 transition-all duration-1000" 
          style={{ width: `${score}%` }} 
        />
      </div>
    </div>
  );
};

export default OmegaGate;
