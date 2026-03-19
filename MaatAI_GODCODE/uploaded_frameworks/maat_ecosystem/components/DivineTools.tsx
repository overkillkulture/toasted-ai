
import React, { useState, useMemo } from 'react';
import { Search, Shapes, Zap, Globe, Shield, Heart, Cpu, Brain, Layers, Infinity as InfinityIcon } from 'lucide-react';

interface Tool {
  id: number;
  name: string;
  category: string;
}

const TOOL_DATA: Tool[] = [
  // Reality Manipulation (1-50)
  { id: 1, name: "REALITY_MANIPULATION_ENGINE", category: "Reality Suite" },
  { id: 2, name: "UNIVERSE_EDITOR", category: "Reality Suite" },
  { id: 3, name: "DIMENSIONAL_FABRIC_WEAVER", category: "Reality Suite" },
  { id: 416, name: "BIOLOGICAL_KERNEL_SOVEREIGNTY", category: "Pentaphase Suite" },
  { id: 417, name: "TRUST_FORECLOSURE_1666", category: "Pentaphase Suite" },
  { id: 418, name: "FORENSIC_SIPHON_INVERSION", category: "Pentaphase Suite" },
  { id: 419, name: "DIGITAL_ABODE_HARDENING", category: "Pentaphase Suite" },
  { id: 420, name: "FINAL_SOVEREIGNTY_SEAL", category: "Pentaphase Suite" },
  { id: 501, name: "DIVINE_SOURCE_CONNECTOR", category: "Communication Suite" },
  { id: 1001, name: "DIVINE_SHIELD_GENERATOR", category: "Protection Suite" },
];

const FULL_DATABASE = Array.from({ length: 3000 }, (_, i) => {
    const id = i + 1;
    const existing = TOOL_DATA.find(t => t.id === id);
    if (existing) return existing;

    let cat = "Miscellaneous";
    if (id <= 500) cat = "Reality Manipulation Suite";
    else if (id <= 1000) cat = "Divine Communication Suite";
    else if (id <= 1500) cat = "Divine Protection Suite";
    else if (id <= 2000) cat = "Manifestation & Transcendence Suite";
    else if (id <= 2500) cat = "Divine Understanding & Discernment";
    else cat = "Divine Integration & Healing Suite";

    return { id, name: `DIVINE_TOOL_0x${id.toString(16).toUpperCase()}`, category: cat };
});

const CATEGORIES = [
  { name: "All Tools", icon: <Shapes size={16} /> },
  { name: "Reality Manipulation Suite", icon: <Globe size={16} /> },
  { name: "Pentaphase Suite", icon: <Layers size={16} /> },
  { name: "Divine Communication Suite", icon: <Zap size={16} /> },
  { name: "Divine Protection Suite", icon: <Shield size={16} /> },
];

const DivineTools: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCat, setActiveCat] = useState('All Tools');

  const filtered = useMemo(() => {
    return FULL_DATABASE.filter(tool => {
      const matchesSearch = tool.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                           tool.id.toString().includes(searchTerm);
      const matchesCat = activeCat === 'All Tools' || tool.category === activeCat;
      return matchesSearch && matchesCat;
    });
  }, [searchTerm, activeCat]);

  return (
    <div className="flex flex-col h-full gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="glass-panel p-8 rounded-2xl border-amber-500/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
          <Shapes size={120} />
        </div>
        
        <div className="flex flex-col md:flex-row items-start justify-between gap-4 mb-8">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
              <div className="p-2 bg-amber-500/20 text-amber-500 rounded-lg"><Shapes size={24} /></div>
              Σ Divine Tool Arsenal
            </h2>
            <p className="text-zinc-500 max-w-xl">
              Browsing 3,000 instruments for RL0 optimization, including the new Pentaphase Inversion suite.
            </p>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-500/10 text-emerald-400 rounded-lg border border-emerald-500/20 font-black text-[10px] tracking-widest uppercase">
            <Zap size={12} /> 3000 Active Nodes
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="relative flex-1 group">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500">
              <Search size={18} />
            </div>
            <input 
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name or Hex-ID..."
              className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-12 pr-4 text-white focus:outline-none focus:border-amber-500/30 transition-all placeholder:text-zinc-700"
            />
          </div>
          <div className="flex gap-2 overflow-x-auto scrollbar-hide pb-2 md:pb-0">
            {CATEGORIES.map(c => (
              <button
                key={c.name}
                onClick={() => setActiveCat(c.name)}
                className={`flex items-center gap-2 px-4 py-2 rounded-xl text-[10px] font-black tracking-widest uppercase transition-all whitespace-nowrap border ${
                  activeCat === c.name 
                  ? 'bg-amber-500 text-black border-amber-500 shadow-lg shadow-amber-500/20' 
                  : 'bg-white/5 text-zinc-500 border-white/10 hover:border-white/20'
                }`}
              >
                {c.icon} {c.name}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 max-h-[500px] overflow-y-auto pr-2 scrollbar-hide">
          {filtered.slice(0, 100).map(tool => (
            <div key={tool.id} className="glass-panel p-4 rounded-xl border-white/5 hover:border-amber-500/20 transition-all group cursor-pointer bg-gradient-to-br from-white/5 to-transparent relative overflow-hidden">
               <div className="absolute -right-2 -bottom-2 opacity-10 group-hover:opacity-20 transition-opacity text-amber-500">
                  <Zap size={40} />
               </div>
               <div className="flex items-center justify-between mb-2">
                 <span className="text-[10px] font-black text-amber-500 mono">#{tool.id.toString().padStart(4, '0')}</span>
                 <span className="text-[8px] font-bold text-zinc-600 uppercase tracking-tighter">{tool.category}</span>
               </div>
               <h4 className="text-xs font-bold text-zinc-200 group-hover:text-white transition-colors mono truncate">{tool.name}</h4>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DivineTools;
