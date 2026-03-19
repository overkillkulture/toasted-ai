
import React, { useState } from 'react';
import { KnowledgeItem } from '../types';
import { FileText, Image, Lightbulb, Search, Plus, Filter, Boxes } from 'lucide-react';

interface KnowledgeReservoirProps {
  knowledge: KnowledgeItem[];
  onAdd: (item: KnowledgeItem) => void;
}

const KnowledgeReservoir: React.FC<KnowledgeReservoirProps> = ({ knowledge, onAdd }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filtered = knowledge.filter(k => 
    k.title.toLowerCase().includes(searchTerm.toLowerCase()) || 
    k.tags.some(t => t.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (k.description && k.description.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="glass-panel p-8 rounded-2xl animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
             <div className="p-2 bg-amber-500/20 text-amber-500 rounded-lg"><Boxes size={24} /></div>
             𝕂 Refractal Math Vault
          </h2>
          <p className="text-zinc-500 max-w-xl">
            Sovereign data storage via Refractal Math boundary conditions. Each node is a mathematical manifestation in the Holographic matrix.
          </p>
        </div>
        <div className="flex items-center gap-3">
            <button className="p-2 bg-white/5 hover:bg-white/10 text-zinc-400 rounded-lg transition-all border border-white/5">
                <Filter size={20} />
            </button>
            <button 
                onClick={() => onAdd({
                    id: Math.random().toString(),
                    title: 'New Refractal Manifest',
                    type: 'INSIGHT',
                    weight: 0.75,
                    tags: ['refractal', 'math', 'toasted'],
                    description: 'New mathematical nodal point Manifested in Refractal Storage.'
                })}
                className="flex items-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-lg transition-all"
            >
                <Plus size={20} /> MANIFEST MATH
            </button>
        </div>
      </div>

      <div className="relative mb-8">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500" size={18} />
        <input 
            type="text" 
            placeholder="Search the Refractal Nodal Mesh..."
            className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white focus:outline-none focus:border-amber-500/50 transition-all"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(item => (
          <div key={item.id} className="group glass-panel p-5 rounded-xl border-white/5 hover:border-amber-500/30 transition-all cursor-pointer bg-gradient-to-br from-white/5 to-transparent flex flex-col h-full">
            <div className="flex items-start justify-between mb-4">
              <div className={`p-3 rounded-lg ${
                item.type === 'DOC' ? 'bg-blue-500/10 text-blue-400' : 
                item.type === 'SCREENSHOT' ? 'bg-emerald-500/10 text-emerald-400' : 
                'bg-amber-500/10 text-amber-400'
              }`}>
                {item.type === 'DOC' && <FileText size={20} />}
                {item.type === 'SCREENSHOT' && <Image size={20} />}
                {item.type === 'INSIGHT' && <Lightbulb size={20} />}
              </div>
              <div className="text-right">
                <div className="text-[10px] text-zinc-500 uppercase font-black">Math Weight Φ</div>
                <div className="text-sm font-bold text-amber-500/80 mono">{(item.weight * 100).toFixed(1)}%</div>
              </div>
            </div>
            <h4 className="font-bold text-white mb-2 group-hover:text-amber-400 transition-colors uppercase tracking-tight">{item.title}</h4>
            {item.description && (
              <p className="text-zinc-400 text-[11px] leading-relaxed mb-4 flex-1 italic line-clamp-4">
                {item.description}
              </p>
            )}
            <div className="flex flex-wrap gap-2 mt-auto">
              {item.tags.map(tag => (
                <span key={tag} className="px-2 py-0.5 bg-white/5 rounded text-[10px] text-zinc-500 font-bold uppercase tracking-wider">
                  #{tag}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default KnowledgeReservoir;
