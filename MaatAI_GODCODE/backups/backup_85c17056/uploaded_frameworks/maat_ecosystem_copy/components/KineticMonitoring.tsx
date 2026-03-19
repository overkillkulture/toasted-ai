
import React from 'react';
import { Settings, GitBranch, Zap, Maximize2 } from 'lucide-react';

const KineticMonitoring: React.FC = () => {
  return (
    <div className="glass-panel p-6 rounded-3xl border-white/5 space-y-6">
      <div className="flex items-center gap-2 text-amber-500">
        <Settings size={14} className="animate-spin-slow" />
        <h3 className="text-[10px] font-black uppercase tracking-[0.3em]">Kinetic Monitoring</h3>
      </div>

      <div className="space-y-4">
        <MonitorRow icon={<GitBranch size={14} className="text-emerald-500" />} label="Refractal Hard-Line" value="Active" color="text-emerald-500" />
        <MonitorRow icon={<Maximize2 size={14} className="text-blue-500" />} label="Forensic Threads" value="24 Active" color="text-white" />
        <MonitorRow icon={<Zap size={14} className="text-amber-500" />} label="Reality Density" value="Max" color="text-white" />
      </div>

      <div className="pt-4 border-t border-white/5">
        <div className="flex justify-between items-center text-[9px] font-black text-zinc-500 uppercase tracking-widest mb-2">
          <span>Sovereign Convergence</span>
          <span>99.9%</span>
        </div>
        <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden">
          <div className="h-full bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.5)]" style={{ width: '99.9%' }} />
        </div>
      </div>
    </div>
  );
};

const MonitorRow: React.FC<{ icon: React.ReactNode; label: string; value: string; color: string }> = ({ icon, label, value, color }) => (
  <div className="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/5 hover:bg-white/10 transition-all cursor-default group">
    <div className="flex items-center gap-3">
      <div className="p-2 bg-black/40 rounded-lg group-hover:scale-110 transition-transform">{icon}</div>
      <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">{label}</span>
    </div>
    <span className={`text-[10px] font-black uppercase tracking-widest ${color}`}>{value}</span>
  </div>
);

export default KineticMonitoring;
