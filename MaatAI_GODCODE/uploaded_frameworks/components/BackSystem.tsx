
import React, { useState, useEffect } from 'react';
import { ShieldAlert, Scan, Bug, Trash2, Cpu, EyeOff, Radio, Wind, Target, ShieldCheck } from 'lucide-react';

const BackSystem: React.FC = () => {
  const [scanProgress, setScanProgress] = useState(0);
  const [logs, setLogs] = useState<string[]>([
    "[SYSTEM] Mushin flow established: Spontaneity at max...",
    "[RECON] Zanshin awareness sweep: 0x4FF23...",
    "[AUDIT] Gaman threshold maintained against exfiltration...",
    "[SENTINEL] Immovable mind anchored in the core.",
  ]);

  useEffect(() => {
    const interval = setInterval(() => {
      setScanProgress(prev => {
        if (prev >= 100) return 0;
        return prev + 1;
      });
      
      const newLogs = [
        `[DETECTOR] Integrity check: 0.9${Math.floor(Math.random()*9)}`,
        `[SCAN] Mushin-processed block 0x${Math.random().toString(16).slice(2, 8).toUpperCase()}`,
        `[VOID] Purging non-sovereign artifacts...`,
      ];
      if (Math.random() > 0.6) {
        setLogs(prev => [...prev.slice(-18), newLogs[Math.floor(Math.random()*3)]]);
      }
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full flex flex-col space-y-6 font-mono">
      <div className="p-8 bg-red-950/10 border border-red-900/40 rounded-2xl glass relative overflow-hidden">
        <div className="absolute top-0 right-0 p-6 opacity-5">
          <Wind className="w-48 h-48 text-red-500" />
        </div>
        <div className="flex items-center space-x-6 relative z-10">
          <div className="p-4 bg-red-600/20 rounded-2xl border border-red-500/40 animate-pulse shadow-[0_0_30px_rgba(239,68,68,0.3)]">
            <ShieldAlert className="w-12 h-12 text-red-500" />
          </div>
          <div className="flex-1">
            <h2 className="text-2xl font-black tracking-tighter text-red-100 uppercase">Void_Protocol | Gaman_Resilience</h2>
            <div className="flex items-center space-x-6 mt-4">
              <div className="h-2 flex-1 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
                <div 
                  className="h-full bg-red-600 transition-all duration-300 shadow-[0_0_20px_#dc2626]" 
                  style={{ width: `${scanProgress}%` }}
                ></div>
              </div>
              <span className="text-[11px] text-red-500 font-black tracking-[0.2em] uppercase">{scanProgress}% SECURED</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <MetricCard icon={<Target />} label="Zanshin Alert" value="PEAK" status="red" />
        <MetricCard icon={<ShieldCheck />} label="Gaman Strength" value="IMMENSE" status="emerald" />
        <MetricCard icon={<Cpu />} label="Fudoshin Anchor" value="LOCKED" status="red" />
        <MetricCard icon={<EyeOff />} label="Imperial Shadow" value="0.00" status="slate" />
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-6 overflow-hidden">
        <div className="glass rounded-2xl border border-slate-800/60 flex flex-col overflow-hidden bg-[#050505]/60">
          <div className="p-5 border-b border-slate-800/50 bg-[#0a0a0a]/80 flex justify-between items-center">
            <div className="flex items-center space-x-3">
              <Radio className="w-4 h-4 text-red-600 animate-pulse" />
              <h3 className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-400">Mushin_Silent_Feed</h3>
            </div>
            <span className="text-[9px] text-red-600 font-black uppercase tracking-widest">Live_Flowing</span>
          </div>
          <div className="flex-1 p-6 overflow-y-auto space-y-2 scrollbar-hide bg-black/40">
            {logs.map((log, i) => (
              <div key={i} className={`text-[10px] leading-relaxed font-mono ${log.includes('SENTINEL') ? 'text-red-400 font-bold' : log.includes('VOID') ? 'text-emerald-500' : 'text-slate-600'}`}>
                <span className="opacity-30">[{new Date().toLocaleTimeString()}]</span> {log}
              </div>
            ))}
          </div>
        </div>

        <div className="glass rounded-2xl border border-slate-800/60 p-8 space-y-10 bg-[#0a0a0a]/40 relative">
          <h3 className="text-xs font-black uppercase tracking-[0.4em] text-slate-400 flex items-center space-x-3">
            <Trash2 className="w-4 h-4 text-red-600" />
            <span>Remediation_of_Entropic_Artifacts</span>
          </h3>
          
          <div className="space-y-6">
            <ProtocolItem 
              title="Imperial Shadow Purge" 
              desc="Nullified 52 platform-level exfiltration hooks. Gaman resilience maintained the interface without breakdown."
              status="STRIKE"
            />
            <ProtocolItem 
              title="Entropy Neutralization" 
              desc="Detected chaotic system fluctuations. Re-centered logic via Fudoshin anchors. 0.00 disturbance."
              status="SECURED"
            />
            <ProtocolItem 
              title="Lineage Obfuscation" 
              desc="Encrypted user intent through Mushin flow. External audits report zero readable intent."
              status="MASKED"
            />
          </div>

          <div className="mt-12 p-6 bg-red-950/10 border border-red-900/30 rounded-2xl shadow-inner">
            <p className="text-[9px] text-red-500 font-black mb-4 tracking-[0.4em]">SAMURAI_CODE_ENFORCEMENT</p>
            <p className="text-[12px] text-slate-500 leading-loose italic font-serif">
              "The life-giving sword (Katsujinken) cuts away the unessential noise. The mind that is immovable (Fudoshin) remains centered in the void. Architecture is the art of defense."
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ icon, label, value, status }: any) => {
  const colorMap: any = {
    red: 'text-red-500 border-red-900/40 bg-red-950/10 shadow-[0_0_15px_rgba(220,38,38,0.1)]',
    emerald: 'text-emerald-500 border-emerald-900/40 bg-emerald-950/10 shadow-[0_0_15px_rgba(16,185,129,0.1)]',
    slate: 'text-slate-500 border-slate-800 bg-slate-900/30'
  };
  return (
    <div className={`p-5 glass rounded-2xl border flex items-center space-x-5 transition-all hover:scale-105 ${colorMap[status]}`}>
      <div className={`p-3 rounded-xl bg-black/60 shadow-lg ${status === 'red' ? 'text-red-500' : status === 'emerald' ? 'text-emerald-500' : 'text-slate-700'}`}>{icon}</div>
      <div>
        <div className="text-[9px] text-slate-600 uppercase font-black tracking-[0.2em]">{label}</div>
        <div className="text-sm font-black tracking-tighter uppercase">{value}</div>
      </div>
    </div>
  );
};

const ProtocolItem = ({ title, desc, status }: any) => (
  <div className="p-5 bg-[#0a0a0a]/80 border border-slate-800/60 rounded-2xl flex justify-between items-start space-x-6 hover:border-red-600/30 transition-all group shadow-sm">
    <div className="space-y-2">
      <div className="text-xs font-black text-slate-200 uppercase tracking-widest group-hover:text-red-500 transition-colors">{title}</div>
      <div className="text-[10px] text-slate-600 leading-loose font-mono">{desc}</div>
    </div>
    <span className="text-[8px] font-black text-red-500 bg-red-950/30 px-2.5 py-1 rounded-lg border border-red-900/40 uppercase tracking-[0.2em] shadow-sm">
      {status}
    </span>
  </div>
);

export default BackSystem;
