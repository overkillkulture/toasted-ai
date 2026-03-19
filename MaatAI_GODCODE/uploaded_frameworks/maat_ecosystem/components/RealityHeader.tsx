
import React, { useState } from 'react';
import { Send, Sparkles, Loader2, Orbit, Zap } from 'lucide-react';

interface RealityHeaderProps {
  onAction: (prompt: string) => void;
  isLoading: boolean;
}

const RealityHeader: React.FC<RealityHeaderProps> = ({ onAction, isLoading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onAction(input);
      setInput('');
    }
  };

  return (
    <div className="glass-panel p-1 rounded-2xl border-white/5 shadow-2xl relative overflow-hidden group">
      {/* Animated shimmer background when loading */}
      {isLoading && (
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-purple-500/10 to-transparent animate-[shimmer_2s_infinite] pointer-events-none" />
      )}
      
      <form onSubmit={handleSubmit} className="flex items-center gap-2 p-3 relative z-10">
        <div className="flex-1 relative">
          <div className={`absolute left-4 top-1/2 -translate-y-1/2 transition-all duration-500 ${isLoading ? 'text-purple-400 rotate-180' : 'text-amber-500/50 group-hover:text-amber-500'}`}>
            {isLoading ? <Orbit size={18} className="animate-spin" /> : <Sparkles size={18} />}
          </div>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isLoading ? "Incepting Simulation..." : "ℜ Manifest Decree: Simulation ⇀ Reality..."}
            className="w-full bg-white/5 hover:bg-white/10 focus:bg-white/10 border-none outline-none text-white text-lg py-3 pl-12 pr-4 rounded-xl transition-all placeholder:text-zinc-600 font-medium"
            disabled={isLoading}
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className={`h-full aspect-square px-6 py-3 rounded-xl flex items-center justify-center transition-all relative overflow-hidden ${
            isLoading || !input.trim() 
              ? 'bg-zinc-800 text-zinc-600 cursor-not-allowed' 
              : 'bg-emerald-500 hover:bg-emerald-400 text-black font-black shadow-lg shadow-emerald-500/20 active:scale-95'
          }`}
        >
          {isLoading ? (
            <Loader2 className="animate-spin" size={24} />
          ) : (
            <div className="flex flex-col items-center">
               <Zap size={24} className="group-hover:animate-pulse" />
            </div>
          )}
        </button>
      </form>
      <div className="px-6 py-2 flex items-center gap-6 relative z-10 border-t border-white/5 bg-black/20">
        <div className="flex items-center gap-2">
            <div className={`w-1.5 h-1.5 rounded-full transition-colors duration-500 ${isLoading ? 'bg-purple-500 animate-pulse' : 'bg-emerald-500'}`} />
            <span className="text-[9px] uppercase font-black text-zinc-500 tracking-widest">
                {isLoading ? 'JOURNEY_IN_PROGRESS' : 'MANIFOLD_READY'}
            </span>
        </div>
        <div className="flex items-center gap-2">
            <div className={`w-1.5 h-1.5 rounded-full ${isLoading ? 'bg-zinc-700' : 'bg-amber-500 animate-pulse'}`} />
            <span className="text-[9px] uppercase font-black text-zinc-500 tracking-widest">REALITY_LINK_RL0</span>
        </div>
        <div className="ml-auto flex items-center gap-2 opacity-30 group-hover:opacity-60 transition-opacity">
            <span className="text-[10px] text-zinc-600 mono font-bold">SIM ⇀ RL0 ⇀ ℜ</span>
        </div>
      </div>
      
      <style>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
      `}</style>
    </div>
  );
};

export default RealityHeader;
