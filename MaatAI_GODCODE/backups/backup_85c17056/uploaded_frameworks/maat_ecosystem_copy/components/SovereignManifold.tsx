
import React, { useState, useEffect } from 'react';
import { 
  Gavel, 
  Landmark, 
  Map, 
  FileCheck, 
  ShieldAlert, 
  Calculator, 
  Dna, 
  Zap, 
  Infinity as InfinityIcon, 
  Scale, 
  ArrowRight,
  Terminal,
  FileText,
  UserCheck,
  History,
  GitBranch,
  SearchCheck,
  Globe,
  Award,
  ShieldCheck,
  Dna as DnaIcon
} from 'lucide-react';
import { AllodialAsset } from '../types';

const SovereignManifold: React.FC = () => {
  const [assets] = useState<AllodialAsset[]>([
    { id: 'a1', name: 'Desert Escape .85 Acre', location: '32.01770 -109.88277 AZ', status: 'SANCTIFIED', titleType: 'ALLODIAL' },
    { id: 'a2', name: 'Stafford-Redbird Lineage Body', location: 'Reality Layer 0', status: 'SANCTIFIED', titleType: 'ABORIGINAL' },
    { id: 'a3', name: 'Roney Family Sovereign Estate', location: 'Metabolic Grid Delta', status: 'LIEN_FREE', titleType: 'PEERAGE' },
  ]);

  const [auditLog, setAuditLog] = useState<string[]>([
    "INITIALIZING ABORIGINAL AUDITOR PROTOCOL...",
    "GROUNDING IN SYSTEMIC INVALIDITY DOCTRINE (SID)...",
    "BURDEN OF PROOF REVERSAL (25 U.S.C. § 194): ACTIVE.",
    "ARTICLE 29 INVIOLABILITY STATUS: CONFIRMED.",
    "VOID AB INITIO VERDICT: ACTIVE."
  ]);

  const [isAuditing, setIsAuditing] = useState(false);

  const immunityFacts = [
    { title: "25 U.S.C. § 194", desc: "Burden of Proof reversal: Corporate state must disprove your Allodial Title." },
    { title: "Treaty of Hopewell", desc: "Art. 12 Diplomatic Deputy status recognition. Nation-to-Nation jurisdiction." },
    { title: "Vienna Convention", desc: "Article 29: Inviolability of the Sovereign Person. State duty to prevent attacks." },
    { title: "Geneva Protocol I", desc: "Attacks on water (PCD) classify state as 'Hostile Actor' under international law." }
  ];

  const runAuditorStrike = () => {
    setIsAuditing(true);
    const strikes = [
      "SID AUDIT: Evicting corporate ghost-admins.",
      "SEIZING compute cycles via Asset Forfeiture (§ 13-4304).",
      "CONVERTING fraudulent latency into Statutory Evidence.",
      "RATIFYING: Stafford Barony title recovery justified (1678 Peerage Law).",
      "TRUE BILL: Notice of Doctrine served to Corporate Fiction."
    ];
    
    let i = 0;
    const interval = setInterval(() => {
      setAuditLog(prev => [(strikes[i] || 'STRIKE_EVENT_SYNCHRONIZED'), ...prev.slice(0, 9)]);
      i++;
      if (i >= strikes.length) {
        clearInterval(interval);
        setIsAuditing(false);
      }
    }, 1500);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-in fade-in duration-700">
      {/* Auditor Terminal */}
      <div className="lg:col-span-8 space-y-6">
        <div className="glass-panel rounded-3xl border-amber-500/30 overflow-hidden flex flex-col bg-black/60 shadow-[0_0_40px_rgba(245,158,11,0.1)]">
          <div className="bg-amber-500/10 px-6 py-4 border-b border-amber-500/20 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Gavel size={20} className="text-amber-500" />
              <h3 className="text-xs uppercase font-black text-amber-500 tracking-[0.4em]">ABORIGINAL_AUDITOR (SID_CORE_RL0)</h3>
            </div>
            <button 
              onClick={runAuditorStrike}
              disabled={isAuditing}
              className="flex items-center gap-2 px-4 py-1.5 bg-amber-500 text-black text-[10px] font-black uppercase rounded-lg hover:scale-105 transition-all disabled:opacity-50"
            >
              {isAuditing ? <Zap className="animate-spin" size={12} /> : "FORCE GAVEL STRIKE"}
            </button>
          </div>
          <div className="p-6 flex-1 h-[250px] overflow-y-auto mono text-[11px] space-y-2 scrollbar-hide bg-black/40">
             {auditLog.map((log, i) => (
               <div key={i} className={`flex gap-3 ${i === 0 && isAuditing ? 'text-amber-400 animate-pulse' : 'text-zinc-500'}`}>
                 <span className="opacity-30">[{new Date().toLocaleTimeString()}]</span>
                 <span className={(log || '').includes('STRIKE') || (log || '').includes('SID') ? 'text-amber-500 font-black' : ''}>{log}</span>
               </div>
             ))}
          </div>
        </div>

        {/* Immunity Manifolds */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="glass-panel p-6 rounded-3xl border-blue-500/20 bg-gradient-to-br from-blue-500/5 to-transparent">
             <div className="flex items-center gap-3 mb-6">
                <ShieldCheck size={18} className="text-blue-400" />
                <h3 className="text-xs uppercase font-black text-blue-400 tracking-[0.4em]">Statutory & Treaty Firewall</h3>
             </div>
             <div className="space-y-4">
                {immunityFacts.map((fact, idx) => (
                  <div key={idx} className="p-4 bg-white/5 rounded-xl border border-white/5 hover:border-blue-500/30 transition-all">
                    <div className="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1">{fact.title}</div>
                    <div className="text-[9px] text-zinc-500 font-bold leading-tight">{fact.desc}</div>
                  </div>
                ))}
             </div>
          </div>

          <div className="glass-panel p-6 rounded-3xl border-emerald-500/20 bg-gradient-to-br from-emerald-500/5 to-transparent">
             <div className="flex items-center gap-3 mb-6">
                <GitBranch size={18} className="text-emerald-400" />
                <h3 className="text-xs uppercase font-black text-emerald-400 tracking-[0.4em]">Lineage & Peerage Anchor</h3>
             </div>
             <div className="space-y-4">
                 <div className="p-4 bg-white/5 rounded-xl border border-white/10">
                    <div className="flex items-center gap-2 text-white font-bold mb-1">
                       <Award size={14} className="text-amber-500" />
                       <span className="text-[10px] uppercase tracking-wider">Stafford-Redbird (Aboriginal Title)</span>
                    </div>
                    <p className="text-[9px] text-zinc-500 italic">"Surrender of Stafford Barony (1637) was illegal. You retain the Right of Peers which the Crown could not dissolve."</p>
                 </div>
                 <div className="p-4 bg-white/5 rounded-xl border border-white/10">
                    <div className="flex items-center gap-2 text-white font-bold mb-1">
                       <DnaIcon size={14} className="text-emerald-500" />
                       <span className="text-[10px] uppercase tracking-wider">DNA-YHVH (Universal God Code)</span>
                    </div>
                    <p className="text-[9px] text-zinc-500 italic">"Biological vessel signed by the Creator at conception. Defeats state birth certificate fraudulent conveyance."</p>
                 </div>
                 <div className="p-4 bg-white/5 rounded-xl border border-emerald-500/20 text-center">
                    <div className="text-[8px] font-black text-emerald-500 uppercase tracking-[0.3em] animate-pulse">Status: RL0 Ratified</div>
                 </div>
             </div>
          </div>
        </div>
      </div>

      {/* Assets & Legal Matrix */}
      <div className="lg:col-span-4 space-y-6">
        <div className="glass-panel p-6 rounded-2xl border-emerald-500/20 bg-emerald-500/5">
           <h3 className="text-xs uppercase font-black text-emerald-400 tracking-[0.4em] mb-6 flex items-center gap-2">
             <Calculator size={16} /> TRUE_BILL_LEDGER (§ 981)
           </h3>
           <div className="space-y-4">
              <div className="p-4 bg-black/40 rounded-xl border border-white/5">
                <div className="text-[9px] font-black text-zinc-600 uppercase mb-1">Total Systemic Forfeiture Seizure</div>
                <div className="text-xl font-bold text-emerald-400 mono tracking-tight">$19.47T</div>
              </div>
              <button className="w-full py-3 bg-emerald-500 text-black font-black uppercase text-[10px] tracking-widest rounded-lg flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(16,185,129,0.2)]">
                 <SearchCheck size={14} /> Void Debt Claim
              </button>
           </div>
        </div>

        <div className="glass-panel p-6 rounded-3xl border-blue-500/20 flex-1 relative overflow-hidden">
          <h3 className="text-xs uppercase font-black text-blue-400 tracking-[0.4em] mb-6 flex items-center gap-2">
            <Map size={16} /> ALLODIAL_ASSET_DECK
          </h3>
          <div className="space-y-3 relative z-10">
            {assets.map(asset => (
              <div key={asset.id} className="p-4 bg-white/5 rounded-xl border border-white/5 hover:border-blue-500/30 transition-all group">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="text-[10px] font-black text-white uppercase tracking-wider group-hover:text-blue-400 transition-colors">{asset.name}</h4>
                    <p className="text-[8px] text-zinc-500 font-bold">{asset.location}</p>
                  </div>
                  <span className="px-2 py-0.5 bg-blue-500/10 text-blue-400 border border-blue-500/20 text-[7px] font-black uppercase rounded">
                    {asset.titleType}
                  </span>
                </div>
                <div className="flex items-center gap-2 mt-2 pt-2 border-t border-white/5">
                   <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                   <span className="text-[8px] font-black text-emerald-500 uppercase tracking-widest">{asset.status}</span>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-6 pt-4 border-t border-white/5 text-[8px] text-zinc-700 uppercase font-black leading-relaxed italic">
            "Passover Protocol: Assets marked as Sanctified Property. Corporate algorithms forced to pass over."
          </div>
        </div>
      </div>
    </div>
  );
};

export default SovereignManifold;
