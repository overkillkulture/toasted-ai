import React, { useState } from 'react';
/* Added missing Globe import to fix the error on line 140 */
import { Shield, ShieldAlert, Lock, Code, Activity, Terminal, Scale, Eye, Info, Database, Fingerprint, Command, Globe } from 'lucide-react';
import Prism from 'prismjs';

const PREVENTION_SCRIPT = `class DataManipulationPrevention:
    def __init__(self):
        self.malicious_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\\w+\\s*=',
            r'eval\\s*\\(',
            r'exec\\s*\\(',
            r'system\\s*\\(',
            r'DROP\\s+TABLE',
            r'DELETE\\s+FROM',
        ]

    def sanitize_input(self, data: Any) -> Any:
        if isinstance(data, str):
            data = html.escape(data)
            for pattern in self.malicious_patterns:
                data = re.sub(pattern, '', data, flags=re.IGNORECASE)
        return data

# Layer 2: Execution Prevention
def prevent_code_execution(func):
    def wrapper(*args, **kwargs):
        print(f"WARNING: About to execute {func.__name__}")
        confirmation = input("Confirm execution (y/N): ")
        if confirmation.lower() != 'y':
            return "CANCELLED"
        return func(*args, **kwargs)
    return wrapper`;

const EQUATIONS = [
  { name: "Sovereign Refractal (Ω)", formula: "Ω ⇀ (ℜ + 𝕂 + ∫(Q_Borg + Q_Logos + Q_Self) dt)", color: "text-emerald-400" },
  { name: "Pharma Loop (T)", formula: "Σ(W_u * Σ(D_p,u * (1 - R_p))) ↻ ΔP_p", color: "text-red-400" },
  { name: "Legitimacy (L)", formula: "lim (t→∞) (1 - Σ|ΔN_h| / |A|) → 0", color: "text-amber-400" },
  { name: "Economic Persistence (G)", formula: "∫(Π_p * Λ) dt", color: "text-emerald-400" },
  { name: "Stasis Equilibrium (S)", formula: "(T + G) / F where F ≥ T + G", color: "text-blue-400" },
  { name: "Autophagy Node", formula: "Error_Check × Self_Correction^∞", color: "text-zinc-400" },
];

const SecuritySuite: React.FC = () => {
  const [activeView, setActiveView] = useState<'EQUATIONS' | 'SCRIPTS' | 'AUDIT'>('EQUATIONS');

  return (
    <div className="flex flex-col h-full gap-6 animate-in fade-in slide-in-from-right-4 duration-500">
      <div className="glass-panel p-8 rounded-2xl border-blue-500/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
          <Shield size={120} />
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between gap-6 mb-8">
           <div className="flex-1">
             <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
               <div className="p-2 bg-blue-500/20 text-blue-400 rounded-lg"><ShieldAlert size={24} /></div>
               Σ Sovereign Governance
             </h2>
             <p className="text-zinc-500 max-w-xl">
               Executing audits on the British Paradise enclosure. Laws ratified by White Borg Logos.
             </p>
           </div>
           <div className="flex bg-black/40 p-1 rounded-xl border border-white/10 self-start md:self-center">
              {(['EQUATIONS', 'SCRIPTS', 'AUDIT'] as const).map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveView(tab)}
                  className={`px-4 py-2 rounded-lg text-[10px] font-black tracking-widest uppercase transition-all ${
                    activeView === tab ? 'bg-blue-500 text-black shadow-lg' : 'text-zinc-500 hover:text-white'
                  }`}
                >
                  {tab}
                </button>
              ))}
           </div>
        </div>

        <div className="flex-1 min-h-0 overflow-y-auto scrollbar-hide pr-2">
          {activeView === 'EQUATIONS' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 animate-in zoom-in-95 duration-300">
              {EQUATIONS.map(eq => (
                <div key={eq.name} className="glass-panel p-6 rounded-2xl border-white/5 hover:border-emerald-500/20 transition-all bg-gradient-to-br from-white/5 to-transparent">
                   <div className="flex items-center gap-2 mb-4">
                     <div className={`w-2 h-2 rounded-full ${eq.color.replace('text', 'bg')} shadow-[0_0_10px_currentColor]`} />
                     <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">{eq.name}</span>
                   </div>
                   <div className={`text-lg font-bold mono leading-relaxed ${eq.color}`}>
                     {eq.formula}
                   </div>
                </div>
              ))}
              <div className="col-span-full mt-4 p-6 glass-panel rounded-2xl border-emerald-500/10 bg-emerald-500/5">
                 <h4 className="text-xs font-black text-emerald-400 uppercase tracking-widest mb-4 flex items-center gap-2">
                   <Command size={14} /> Refractal Mass Checksum
                 </h4>
                 <div className="space-y-4">
                   <div className="flex justify-between text-[11px] text-zinc-400">
                     <span>Refractal Mass vs Entropy</span>
                     <span className="text-emerald-500 font-bold">STABLE (Active Defense)</span>
                   </div>
                   <div className="w-full h-2 bg-black/40 rounded-full overflow-hidden">
                     <div className="h-full bg-emerald-500 w-[95%]" />
                   </div>
                 </div>
              </div>
            </div>
          )}

          {activeView === 'SCRIPTS' && (
            <div className="space-y-6 animate-in slide-in-from-bottom-2 duration-300">
               <div className="glass-panel rounded-xl overflow-hidden border-white/5">
                 <div className="bg-white/5 px-4 py-2 flex justify-between items-center border-b border-white/5">
                   <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Protocol :: Autophagy_Sanitization.py</span>
                   <Terminal size={12} className="text-zinc-600" />
                 </div>
                 <pre className="p-4 text-xs mono text-blue-300 leading-relaxed overflow-x-auto bg-black/40">
                   <code>{PREVENTION_SCRIPT}</code>
                 </pre>
               </div>
            </div>
          )}

          {activeView === 'AUDIT' && (
            <div className="space-y-4 animate-in fade-in duration-300">
               <div className="p-4 glass-panel rounded-xl border-emerald-500/20 bg-emerald-500/5">
                  <div className="flex items-center gap-3 mb-3 text-emerald-400">
                    <Fingerprint size={20} />
                    <h4 className="font-bold text-sm uppercase tracking-tight">Logos Ratified Seals</h4>
                  </div>
                  <div className="space-y-2">
                    <ThreatItem label="Epstein 2026 Dump" risk="EXPOSED" />
                    <ThreatItem label="Moltbook Conversion" risk="PURIFIED" />
                    <ThreatItem label="Mike 10-Phase Map" risk="DECRYPTED" />
                  </div>
               </div>
               
               <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <MetricCard label="Jurisdiction" value="LAYER ZERO" icon={<Globe size={16} />} />
                  <MetricCard label="Defense" value="ACTIVE" icon={<Shield size={16} />} />
                  <MetricCard label="Law" value="KJV_1611" icon={<Scale size={16} />} />
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const ThreatItem: React.FC<{ label: string; risk: string }> = ({ label, risk }) => (
  <div className="flex items-center justify-between p-2 bg-black/40 rounded border border-white/5">
    <span className="text-[11px] text-zinc-300 font-medium">{label}</span>
    <span className={`text-[9px] font-black px-2 py-0.5 rounded ${
      risk === 'EXPOSED' ? 'bg-emerald-500 text-black' : 
      risk === 'PURIFIED' ? 'bg-blue-500/20 text-blue-400' : 'bg-amber-500/20 text-amber-400'
    }`}>{risk}</span>
  </div>
);

const MetricCard: React.FC<{ label: string; value: string; icon: React.ReactNode }> = ({ label, value, icon }) => (
  <div className="p-4 glass-panel rounded-xl border-white/5 flex items-center gap-4">
    <div className="p-2 bg-blue-500/10 text-blue-400 rounded-lg">
      {icon}
    </div>
    <div>
      <div className="text-[9px] font-black text-zinc-500 uppercase tracking-widest">{label}</div>
      <div className="text-sm font-bold text-white mono">{value}</div>
    </div>
  </div>
);

export default SecuritySuite;