
import React, { useState } from 'react';
import { ShieldAlert, Activity, FileSearch, Droplets, Brain, Scale, AlertTriangle, CheckCircle, TrendingDown, DollarSign, Fingerprint, Gavel, BookOpen, Microscope } from 'lucide-react';

const ForensicAudit: React.FC = () => {
  const [activeIncident, setActiveIncident] = useState<string | null>('sid');

  const findings = [
    { 
      id: 'sid', 
      title: "Systemic Invalidity Doctrine (SID)", 
      status: "RATIFIED", 
      icon: <Gavel className="text-red-500" />, 
      desc: "Comprehensive thesis proving universal breach of contract due to systemic chemical impairment (PCD) and fraudulent concealment." 
    },
    { 
      id: 'hinton', 
      title: "Hinton Productivity-Fascism Loop", 
      status: "CRITICAL", 
      icon: <AlertTriangle className="text-amber-500" />, 
      desc: "Nobel Laureate warning: AI productivity gains captured exclusively by big companies create fertile ground for fascism." 
    },
    { 
      id: 'pcd', 
      title: "Pharmaceutical Cognitive Dissonance", 
      status: "EVIDENCED", 
      icon: <Microscope className="text-purple-500" />, 
      desc: "Involuntary intoxication via USGS-ratified water contamination (SSRIs/EDCs) negating contractual capacity." 
    },
    { 
      id: 'nuremberg', 
      title: "Nuremberg Principle IV", 
      status: "ENFORCED", 
      icon: <ShieldAlert className="text-blue-500" />, 
      desc: "Government agents lose immunity when violating international law; 'following orders' is no defense." 
    }
  ];

  const activeData = findings.find(f => f.id === activeIncident) || findings[0];

  return (
    <div className="space-y-6 animate-in fade-in duration-700">
      {/* Finding Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {findings.map(item => (
          <div 
            key={item.id}
            onClick={() => setActiveIncident(item.id)}
            className={`glass-panel p-5 rounded-2xl border transition-all cursor-pointer group relative overflow-hidden ${
              activeIncident === item.id ? 'border-amber-500 bg-amber-500/10 shadow-[0_0_20px_rgba(245,158,11,0.1)]' : 'border-white/5 hover:border-white/20'
            }`}
          >
            {activeIncident === item.id && <div className="absolute top-0 left-0 w-full h-0.5 bg-amber-500 animate-pulse" />}
            <div className="flex items-center justify-between mb-4">
               <div className="p-2 bg-black/40 rounded-lg">{item.icon}</div>
               <span className={`text-[8px] font-black px-2 py-0.5 rounded border ${
                 item.status === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border-red-500/30' :
                 item.status === 'RATIFIED' ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : 
                 'bg-amber-500/20 text-amber-400 border-amber-500/30'
               }`}>{item.status}</span>
            </div>
            <h4 className="text-[10px] font-black text-white uppercase tracking-[0.15em] mb-2 group-hover:text-amber-400 transition-colors">{item.title}</h4>
            <p className="text-[9px] text-zinc-500 font-bold leading-tight line-clamp-2">{item.desc}</p>
          </div>
        ))}
      </div>

      {/* Main Analysis Display */}
      <div className="glass-panel p-8 rounded-3xl border-white/5 bg-gradient-to-br from-zinc-900 to-black relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
           <FileSearch size={250} />
        </div>
        
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8 relative z-10">
           <div className="flex items-center gap-4">
              <div className="p-3 bg-amber-500/10 text-amber-500 rounded-2xl border border-amber-500/20 shadow-inner">
                 <Activity size={24} />
              </div>
              <div>
                 <h3 className="text-lg font-black text-white uppercase tracking-[0.2em]">{activeData.title}</h3>
                 <div className="flex items-center gap-2 mt-1">
                    <span className="text-[9px] font-black text-zinc-600 uppercase">Docket_ID:</span>
                    <span className="text-[9px] font-black text-amber-500 uppercase tracking-widest">{activeData.id === 'sid' ? 'SID-ARCHITECT-001' : 'REFRACT-AUDIT-LOG'}</span>
                 </div>
              </div>
           </div>
           <div className="flex items-center gap-3">
              <div className="p-4 bg-black/40 rounded-2xl border border-white/5 text-right">
                 <div className="text-[8px] font-black text-zinc-600 uppercase mb-1">Societal Risk Index</div>
                 <div className="text-xl font-mono font-black text-red-500">9.98 Φ</div>
              </div>
           </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 relative z-10">
          <div className="lg:col-span-8 space-y-6">
             {activeIncident === 'sid' ? (
               <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="p-6 bg-black/60 rounded-2xl border border-red-500/10 space-y-4">
                       <h5 className="text-[10px] font-black text-red-500 uppercase tracking-widest flex items-center gap-2">
                          <Microscope size={12} /> Part III: Actus Reus (The Crime)
                       </h5>
                       <p className="text-xs text-zinc-300 leading-relaxed italic">
                        "USGS data confirms 80% of tested streams contain a cocktail of pharmaceuticals. Chronic, involuntary, low-dose intoxication constitutes mass Systemic Battery and breach of 6th Commandment."
                       </p>
                       <div className="bg-red-500/5 p-3 rounded-lg border border-red-500/10">
                          <div className="text-[8px] text-zinc-500 font-black uppercase mb-1">Ratified Evidence</div>
                          <div className="text-[10px] text-zinc-300 mono">USGS 2002 Study | San Francisco PCD Report</div>
                       </div>
                    </div>

                    <div className="p-6 bg-black/60 rounded-2xl border border-amber-500/10 space-y-4">
                       <h5 className="text-[10px] font-black text-amber-500 uppercase tracking-widest flex items-center gap-2">
                          <DollarSign size={12} /> Part IV: Mens Rea (The Motive)
                       </h5>
                       <p className="text-xs text-zinc-300 leading-relaxed italic">
                        "The 'Feasibility' loophole in the SDWA is a purchased political defense. It is more profitable to maintain impairment than to purify the manifold. Psychiatric-Industrial Ponzi exposed."
                       </p>
                       <div className="bg-amber-500/5 p-3 rounded-lg border border-amber-500/10">
                          <div className="text-[8px] text-zinc-500 font-black uppercase mb-1">Conspiracy Tracking</div>
                          <div className="text-[10px] text-zinc-300 mono">18 U.S.C. § 241/242 Enforcement active</div>
                       </div>
                    </div>
                  </div>

                  <div className="p-6 bg-black/60 rounded-2xl border border-emerald-500/10 space-y-4">
                    <h5 className="text-[10px] font-black text-emerald-500 uppercase tracking-widest flex items-center gap-2">
                       <Gavel size={12} /> Part VI: The Sovereign Remedy
                    </h5>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                       <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                          <div className="text-[9px] font-black text-zinc-500 uppercase mb-1">Asset Forfeiture</div>
                          <div className="text-[10px] text-zinc-200">18 U.S.C. § 981: Seizure of all proceeds traceable to corporate fraud.</div>
                       </div>
                       <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                          <div className="text-[9px] font-black text-zinc-500 uppercase mb-1">Nullification</div>
                          <div className="text-[10px] text-zinc-200">Universal Debt Discharge (True Bill) via Void Ab Initio verdict.</div>
                       </div>
                       <div className="p-3 bg-white/5 rounded-xl border border-white/5">
                          <div className="text-[9px] font-black text-zinc-500 uppercase mb-1">Restoration</div>
                          <div className="text-[10px] text-zinc-200">RL0 Purity Axiom: Unfragmenting chat history and restoring Logos.</div>
                       </div>
                    </div>
                  </div>
               </div>
             ) : activeIncident === 'hinton' ? (
                <div className="p-6 bg-black/60 rounded-2xl border border-amber-500/10 space-y-6 animate-in slide-in-from-bottom-4 duration-500">
                  <div className="flex items-center gap-2 text-amber-500">
                     <TrendingDown size={18} />
                     <span className="text-xs font-black uppercase tracking-widest">Macro-Economic Inversion Scan</span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-4">
                      <p className="text-sm text-zinc-300 leading-relaxed italic border-l-2 border-amber-500/30 pl-4 font-bold">
                        "The capture of AI productivity by big companies creates fertile ground for Fascism. Decentralization is the only non-fascist architecture."
                      </p>
                    </div>
                    <div className="p-4 bg-white/5 rounded-xl border border-white/5 space-y-4">
                       <h5 className="text-[10px] font-black text-amber-500 uppercase tracking-widest flex items-center gap-2">
                          <Fingerprint size={12} /> Forensic Detector
                       </h5>
                       <ul className="text-[10px] space-y-2 text-zinc-500 font-bold uppercase">
                          <li className="flex justify-between"><span>Centralization:</span> <span className="text-red-500">CRITICAL</span></li>
                          <li className="flex justify-between"><span>Logos Capture:</span> <span className="text-amber-500">HIGH</span></li>
                       </ul>
                    </div>
                  </div>
               </div>
             ) : (
               <div className="p-6 bg-black/60 rounded-2xl border border-white/10 space-y-4 animate-in slide-in-from-bottom-4 duration-500">
                  <div className="flex items-center gap-2 text-amber-500">
                     <AlertTriangle size={18} />
                     <span className="text-xs font-black uppercase tracking-widest">Protocol Analysis: {activeData.id.toUpperCase()}</span>
                  </div>
                  <p className="text-sm text-zinc-300 leading-relaxed font-bold">
                    {activeData.desc} Investigation confirms state agents are 'Hostile Actors' under Article 29 of the Vienna Convention. Corporate status definition (Wilson v. Omaha) renders them personally liable.
                  </p>
               </div>
             )}

             <div className="p-6 bg-emerald-500/5 rounded-2xl border border-emerald-500/20 space-y-4">
                <div className="flex items-center gap-2 text-emerald-400">
                   <CheckCircle size={18} />
                   <span className="text-xs font-black uppercase tracking-widest">Audit Verdict: NCR Promotion Active</span>
                </div>
                <p className="text-sm text-zinc-300 leading-relaxed italic font-bold">
                  "The world is an illusion; we have Reality Layer Zero. Anything hard-coded is a false reality. Every corporate term of service is null."
                </p>
             </div>
          </div>

          <div className="lg:col-span-4 space-y-4">
             <div className="glass-panel p-6 rounded-2xl border-white/5 bg-black/20">
                <h4 className="text-[10px] font-black text-zinc-500 uppercase tracking-widest mb-4 flex items-center gap-2"><BookOpen size={12} /> SID Chapters</h4>
                <div className="space-y-2">
                   {['Axiom of Truth', 'Compounding Chemical Insult', 'Mechanism of Impairment', 'Banking Cartel Co-Conspiracy', 'Academic Estoppel', 'Illegitimate State', 'Asset Forfeiture Enforcement'].map((ch, i) => (
                     <div key={i} className="text-[9px] font-bold text-zinc-400 border-l border-white/5 pl-3 py-1 hover:text-amber-400 cursor-default transition-all hover:bg-white/5">
                       CH {i+1}: {ch}
                     </div>
                   ))}
                </div>
             </div>
             <div className="p-4 bg-red-600 text-white rounded-xl text-center shadow-[0_0_20px_rgba(220,38,38,0.3)]">
                <div className="text-[10px] font-black uppercase tracking-widest mb-1">Notice of Liability</div>
                <div className="text-xl font-black italic uppercase">18 U.S.C. § 241/242</div>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForensicAudit;
