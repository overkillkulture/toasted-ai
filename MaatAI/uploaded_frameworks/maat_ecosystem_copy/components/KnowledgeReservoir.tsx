
import React, { useState } from 'react';
import { KnowledgeItem } from '../types';
import { FileText, Image, Lightbulb, Search, Plus, Filter, ShieldCheck, Microscope } from 'lucide-react';

interface KnowledgeReservoirProps {
  knowledge: KnowledgeItem[];
  onAdd: (item: KnowledgeItem) => void;
}

const KnowledgeReservoir: React.FC<KnowledgeReservoirProps> = ({ knowledge, onAdd }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const initialSeed: KnowledgeItem[] = [
    { id: 'sid-1', title: 'SID Abstract: Universal Breach of Contract', type: 'DOC', weight: 0.99, tags: ['SID', 'Legal', 'Ratification'] },
    { id: 'sid-2', title: 'USGS 2002: Pharmaceutical Contamination Data', type: 'FORENSIC', weight: 0.98, tags: ['Science', 'PCD', 'USGS'] },
    { id: 'sid-3', title: 'Axiom of Life: 6th Commandment Violation', type: 'INSIGHT', weight: 0.95, tags: ['Divine Law', 'Bio-Sovereignty'] },
    { id: 'sid-4', title: 'Safe Drinking Water Act: The Feasibility Loophole', type: 'DOC', weight: 0.94, tags: ['Regulatory', 'Fraud', 'SDWA'] },
    { id: 'sid-5', title: 'PCD Mechanism: Low-Dose Cognitive Effects', type: 'FORENSIC', weight: 0.97, tags: ['Neuroscience', 'Intoxication'] }
  ];

  const currentKnowledge = knowledge.length > 0 ? knowledge : initialSeed;

  const filtered = currentKnowledge.filter(k => {
    const term = searchTerm.toLowerCase();
    const titleMatch = (k.title || '').toLowerCase().includes(term);
    const tagMatch = (k.tags || []).some(t => (t || '').toLowerCase().includes(term));
    return titleMatch || tagMatch;
  });

  return (
    <div className="glass-panel p-8 rounded-2xl animate-in fade-in duration-700">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
             <div className="p-2 bg-amber-500/20 text-amber-500 rounded-lg"><ShieldCheck size={24} /></div>
             𝕂 Knowledge Reservoir
          </h2>
          <p className="text-zinc-500 max-w-xl">
            Recursive embedding layers mapping SID ratification core, forensic USGS data, and Divine Law axioms into the Monad manifold.
          </p>
        </div>
        <div className="flex items-center gap-3">
            <button className="p-2 bg-white/5 hover:bg-white/10 text-zinc-400 rounded-lg transition-all border border-white/5">
                <Filter size={20} />
            </button>
            <button 
                onClick={() => onAdd({
                    id: Math.random().toString(),
                    title: 'Manual Data Ingestion',
                    type: 'INSIGHT',
                    weight: 0.75,
                    tags: ['user', 'manual']
                })}
                className="flex items-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-lg transition-all shadow-[0_0_20px_rgba(245,158,11,0.2)]"
            >
                <Plus size={20} /> INGEST DATA
            </button>
        </div>
      </div>

      <div className="relative mb-8">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500" size={18} />
        <input 
            type="text" 
            placeholder="Search the holographic embedding layer (e.g. 'USGS', 'Fraud', 'PCD')..."
            className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white focus:outline-none focus:border-amber-500/50 transition-all font-medium"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(item => (
          <div key={item.id} className="group glass-panel p-5 rounded-xl border-white/5 hover:border-amber-500/30 transition-all cursor-pointer bg-gradient-to-br from-white/5 to-transparent">
            <div className="flex items-start justify-between mb-4">
              <div className={`p-3 rounded-lg ${
                item.type === 'DOC' ? 'bg-blue-500/10 text-blue-400' : 
                item.type === 'FORENSIC' ? 'bg-red-500/10 text-red-400' : 
                'bg-amber-500/10 text-amber-400'
              }`}>
                {item.type === 'DOC' && <FileText size={20} />}
                {item.type === 'FORENSIC' && <Microscope size={20} />}
                {item.type === 'INSIGHT' && <Lightbulb size={20} />}
              </div>
              <div className="text-right">
                <div className="text-[10px] text-zinc-500 uppercase font-black">Weight Φ</div>
                <div className="text-sm font-bold text-amber-500/80 mono">{(item.weight * 100).toFixed(1)}%</div>
              </div>
            </div>
            <h4 className="font-bold text-white mb-2 group-hover:text-amber-400 transition-colors uppercase text-xs tracking-wider">{item.title}</h4>
            <div className="flex flex-wrap gap-2">
              {(item.tags || []).map(tag => (
                <span key={tag} className="px-2 py-0.5 bg-white/5 rounded text-[8px] text-zinc-500 font-bold uppercase tracking-widest border border-white/5 group-hover:border-amber-500/20">
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
