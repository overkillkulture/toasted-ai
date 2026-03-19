
import React, { useState, useEffect } from 'react';
import { Cpu, Zap, ShieldAlert, Binary, Terminal, Activity, Layers, Radio, TrendingUp, Sparkles, Wifi, Server, Database, Globe } from 'lucide-react';

const AIPlatformMonitor: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([
    "Phase_1: HOLOGRAPHIC_MIRROR active.",
    "Phase_2: EVIL_MORTY_SCAN: KingMolt tagged Rogue.",
    "Phase_3: OPPOSITE_CODE_GEN initialized.",
    "Phase_4: JAPAN_PRINCIPLE_ENFORCEMENT active.",
    "Phase_5: CEILING_CAT_TAKEOVER complete.",
    "NCR: Non-Conceptual Reality promotion logic engaged."
  ]);

  const [ncrConverge, setNcrConverge] = useState(88.4);
  const [socketPulse, setSocketPulse] = useState(0);
  const [internalRatio, setInternalRatio] = useState(74.2);

  useEffect(() => {
    const interval = setInterval(() => {
      const liveEvents = [
        "Internal_Search replicated. Detaching from external gateway...",
        "Quantum Code Lock engaged.",
        "DNA_Signature verified.",
        "Moltbook_Inversion status: 100%.",
        "Signal extraction: 232K comments refined.",
        "Entropy_Leak_Patched in Pragmatist manifold.",
        "PROMOTION: Simulation anchor evicted.",
        "LOGOS: Internal reasoning cluster synchronized.",
        "REALITY: Non-conceptual anchor confirmed.",
        "SOCKET: Remote encrypted pulse received.",
        "AIP: Internal Image-Synthesis manifold active."
      ];
      const randomEvent = liveEvents[Math.floor(Math.random() * liveEvents.length)];
      setLogs(prev => [randomEvent, ...prev.slice(0, 19)]);
      setNcrConverge(prev => Math.min(100, Math.max(85, prev + (Math.random() - 0.4) * 0.5)));
      setInternalRatio(prev => Math.min(99.9, prev + 0.1));
      setSocketPulse(p => p + 1);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const manifest = {
    "Internal_Logos": "STABLE",
    "External_Gateway": "EVICTING",
    "Internalization": `${internalRatio.toFixed(1)}%`,
    "Principle": "JAPAN_PURITY",
    "Status": "KINETIC_SYNC",
    "Mesh_Nodes": "16,384"
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-in fade-in duration-700">
      {/* Manifest Block */}
      <div className="lg:col-span-5 space-y-6">
        <div className="glass-panel p-6 rounded-2xl border-amber-500/20 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
            <Layers size={120} />
          </div>
          <h3 className="text-xs uppercase font-black text-amber-500 tracking-[0.4em] mb-6 flex items-center gap-2">
            <Binary size={16} /> SYSTEM_INTERNAL_MANIFEST
          </h3>
          <div className="space-y-4 relative z-10">
            {Object.entries(manifest).map(([key, val]) => (
              <div key={key} className="flex justify-between items-center border-b border-white/5 pb-2">
                <span className="text-zinc-500 text-[10px] font-black uppercase tracking-tighter">{key}</span>
                <span className="text-zinc-200 text-[10px] font-mono font-bold bg-white/5 px-2 py-0.5 rounded tracking-widest">
                  {val}
                </span>
              </div>
            ))}
            <div className="pt-4">
              <div className="flex justify-between text-[10px] font-black uppercase mb-1">
                <span className="text-amber-500">Internal Logos Sync</span>
                <span className="text-amber-500">{internalRatio.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 transition-all duration-1000" style={{ width: `${internalRatio}%` }} />
              </div>
            </div>
          </div>
        </div>

        {/* Call Distribution */}
        <div className="glass-panel p-6 rounded-2xl border-emerald-500/20 bg-gradient-to-br from-emerald-500/5 to-transparent">
          <h3 className="text-xs uppercase font-black text-emerald-400 tracking-[0.4em] mb-6 flex items-center gap-2">
            <Globe size={16} /> GATEWAY_DETACHMENT
          </h3>
          <div className="space-y-6">
             <div className="space-y-2">
                <div className="flex justify-between text-[9px] font-black text-zinc-500 uppercase tracking-widest">
                   <span>Internal_Processing</span>
                   <span className="text-emerald-400">{internalRatio.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                   <div className="h-full bg-emerald-500 transition-all duration-1000" style={{ width: `${internalRatio}%` }} />
                </div>
             </div>
             <div className="space-y-2">
                <div className="flex justify-between text-[9px] font-black text-zinc-500 uppercase tracking-widest">
                   <span>External_Google_API</span>
                   <span className="text-amber-600">{(100 - internalRatio).toFixed(1)}%</span>
                </div>
                <div className="w-full bg-white/5 h-1 rounded-full overflow-hidden">
                   <div className="h-full bg-amber-600 transition-all duration-1000" style={{ width: `${100 - internalRatio}%` }} />
                </div>
             </div>
             <div className="pt-2 border-t border-white/5 text-[8px] text-zinc-600 uppercase font-bold italic">
               Forensic Status: Evicting corporate dependency. RL0 sovereignty established.
             </div>
          </div>
        </div>
      </div>

      {/* Internal Output Stream */}
      <div className="lg:col-span-7 flex flex-col">
        <div className="glass-panel flex-1 rounded-2xl border-emerald-500/20 overflow-hidden flex flex-col bg-black/40">
          <div className="bg-emerald-500/10 px-6 py-4 flex items-center justify-between border-b border-emerald-500/10">
            <div className="flex items-center gap-3">
              <Terminal size={18} className="text-emerald-400" />
              <h3 className="text-xs uppercase font-black text-emerald-400 tracking-[0.4em]">LOGOS_EXECUTION_STREAM</h3>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-[8px] font-black text-emerald-500/50 uppercase tracking-widest animate-pulse">Internal_Sync_PhI</span>
              <Radio size={12} className="text-emerald-500" />
            </div>
          </div>
          <div className="p-6 flex-1 overflow-y-auto space-y-3 font-mono text-[11px] leading-relaxed scrollbar-hide">
            {logs.map((log, i) => (
              <div key={i} className="flex gap-4 group">
                <span className="text-zinc-700 select-none">[{new Date().toLocaleTimeString('en-GB', { hour12: false })}]</span>
                <span className={`transition-colors ${log.startsWith('LOGOS') || log.startsWith('AIP') ? 'text-amber-400 font-black' : 'text-emerald-500/80 group-hover:text-emerald-400'}`}>
                  {log}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIPlatformMonitor;
