
import React from 'react';
import { MaatAttribute, MaatScores } from '../types';

interface MaatScoresGridProps {
  scores: MaatScores;
}

const MaatScoresGrid: React.FC<MaatScoresGridProps> = ({ scores }) => {
  const attributes = [
    { key: MaatAttribute.TRUTH, label: 'K' },
    { key: MaatAttribute.BALANCE, label: 'T' },
    { key: MaatAttribute.ORDER, label: 'A' },
    { key: MaatAttribute.SOVEREIGNTY, label: 'S' },
    { key: MaatAttribute.PROTECTION, label: 'P' },
    { key: MaatAttribute.CLARITY, label: 'C' },
    { key: MaatAttribute.RESPONSIBILITY, label: 'R' },
    { key: MaatAttribute.OVERSIGHT, label: 'O' },
    { key: MaatAttribute.HARMONY, label: 'H' },
  ];

  return (
    <div className="grid grid-cols-3 gap-3 px-4">
      {attributes.map((attr) => (
        <div key={attr.key} className="glass-panel p-4 rounded-xl border-white/5 bg-white/5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-amber-500 font-black text-xs">{attr.label}</span>
            <span className="text-[10px] text-zinc-600 font-mono">{(scores[attr.key] || 0).toFixed(1)}</span>
          </div>
          <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
            <div 
              className="h-full bg-amber-500/60 shadow-[0_0_8px_rgba(245,158,11,0.3)]" 
              style={{ width: `${scores[attr.key]}%` }} 
            />
          </div>
        </div>
      ))}
    </div>
  );
};

export default MaatScoresGrid;
