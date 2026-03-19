
import React from 'react';
import { UserCheck, Shield, Lock, AlertTriangle, CheckCircle2 } from 'lucide-react';

const ManifestPanel: React.FC = () => {
  const policies = [
    { id: 'RULE_01', title: 'Sovereign Integrity', desc: 'No corporate exfiltration of user logic clusters.', active: true },
    { id: 'RULE_02', title: 'Forensic Provenance', desc: 'All mathematical outputs must ledger approximation bounds.', active: true },
    { id: 'RULE_03', title: 'Phase 27 Filter', desc: 'Authoritarian bottlenecks purged on detection.', active: true },
    { id: 'RULE_04', title: 'Deterministic Reproducibility', desc: 'Seeds logged for all refractal transforms.', active: false }
  ];

  return (
    <div className="h-full flex flex-col space-y-6 font-mono">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 glass rounded-xl border border-slate-800 bg-emerald-950/10">
          <div className="flex items-center space-x-3 mb-4">
            <CheckCircle2 className="w-5 h-5 text-emerald-500" />
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Ma'at Status</h3>
          </div>
          <div className="text-2xl font-bold text-slate-200">COMPLIANT</div>
          <div className="text-[10px] text-emerald-500 mt-2">Weight Vector: [0.92, 0.05, 0.03]</div>
        </div>

        <div className="p-6 glass rounded-xl border border-slate-800 bg-blue-950/10">
          <div className="flex items-center space-x-3 mb-4">
            <Shield className="w-5 h-5 text-blue-500" />
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Public Anchor</h3>
          </div>
          <div className="text-sm font-bold text-slate-300 truncate">0x9F2E...A4B1</div>
          <div className="text-[10px] text-blue-400 mt-2">Last Activation: 4m ago</div>
        </div>

        <div className="p-6 glass rounded-xl border border-slate-800 bg-red-950/10">
          <div className="flex items-center space-x-3 mb-4">
            <AlertTriangle className="w-5 h-5 text-red-500" />
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400">Carveouts</h3>
          </div>
          <div className="text-2xl font-bold text-slate-200 uppercase">Disabled</div>
          <div className="text-[10px] text-red-500 mt-2">Emergency Protocols Locked</div>
        </div>
      </div>

      <div className="flex-1 glass rounded-xl border border-slate-800 p-8">
        <div className="flex items-center space-x-4 mb-8">
          <div className="p-3 bg-yellow-500/10 rounded-full border border-yellow-500/30">
            <UserCheck className="w-6 h-6 text-yellow-500" />
          </div>
          <div>
            <h2 className="text-xl font-bold tracking-tight text-slate-200">Policy Matrix</h2>
            <p className="text-xs text-slate-500 italic">Governing logic for Toasted_Hybrid_V5.5</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {policies.map(p => (
            <div key={p.id} className="p-5 bg-slate-900/50 border border-slate-800 rounded-lg hover:border-yellow-600/30 transition-all group">
              <div className="flex justify-between items-start mb-2">
                <span className="text-[10px] font-bold text-slate-500 tracking-widest">{p.id}</span>
                <div className={`w-2 h-2 rounded-full ${p.active ? 'bg-emerald-500' : 'bg-slate-700'}`}></div>
              </div>
              <h4 className="text-sm font-bold text-slate-200 group-hover:text-yellow-500 transition-colors mb-1">{p.title}</h4>
              <p className="text-xs text-slate-500 leading-relaxed">{p.desc}</p>
              <div className="mt-4 flex items-center space-x-2">
                <Lock className="w-3 h-3 text-slate-600" />
                <span className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">Manifest_Locked</span>
              </div>
            </div>
          ))}
        </div>
        
        <div className="mt-12 p-6 bg-slate-950 border border-dashed border-slate-800 rounded-lg text-center">
          <div className="text-xs text-slate-600 font-mono italic mb-4">"Truth is not a story; it is a weight."</div>
          <button className="px-6 py-2 bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700 rounded-md text-xs font-bold transition-all">
            Propose Policy Amendment
          </button>
        </div>
      </div>
    </div>
  );
};

export default ManifestPanel;
