
import React, { useState } from 'react';
import { Send, Sparkles, Loader2 } from 'lucide-react';

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
    <div className="px-4">
      <div className={`glass-panel p-2 rounded-[2rem] border-amber-500/20 shadow-2xl relative overflow-hidden transition-all duration-500 ${isLoading ? 'bg-amber-500/10' : 'bg-black/60'}`}>
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <div className="flex-1 relative">
            <div className={`absolute left-5 top-1/2 -translate-y-1/2 transition-colors ${isLoading ? 'text-amber-400' : 'text-amber-500'}`}>
              <Sparkles size={18} className={isLoading ? 'animate-spin-slow' : ''} />
            </div>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="ℜ Reality manipulation: Input decree..."
              className="w-full bg-transparent border-none outline-none text-white text-base py-5 pl-14 pr-4 transition-all placeholder:text-zinc-800 font-bold"
              disabled={isLoading}
            />
          </div>
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all ${
              isLoading || !input.trim() 
                ? 'bg-zinc-900 text-zinc-800 cursor-not-allowed' 
                : 'bg-amber-500 text-black shadow-lg shadow-amber-500/40 hover:scale-105 active:scale-95'
            }`}
          >
            {isLoading ? <Loader2 className="animate-spin" size={24} /> : <Send size={24} />}
          </button>
        </form>
        {isLoading && (
          <div className="absolute bottom-0 left-0 h-0.5 bg-amber-500 w-full animate-[shimmer_2s_infinite_linear]" />
        )}
      </div>
    </div>
  );
};

export default RealityHeader;
