
import React, { useState, useEffect, useMemo } from 'react';
import { ForensicLog } from '../types';

const SentinelMonitor: React.FC = () => {
  const [logs, setLogs] = useState<ForensicLog[]>([]);
  const [pulsePath, setPulsePath] = useState('');

  // Generate a high-frequency holographic pulse path
  useEffect(() => {
    const generatePath = () => {
      let path = "M 0 50";
      for (let x = 0; x <= 100; x += 2) {
        const y = 50 + (Math.random() - 0.5) * 30 * (x % 20 === 0 ? 3 : 1);
        path += ` L ${x} ${y}`;
      }
      setPulsePath(path);
    };
    const interval = setInterval(generatePath, 150);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const origins = ["RL0_CORE", "GRAND_REGISTER", "SENTINEL_SHIELD", "OMEGA_AV", "QUANTUM_ROOT"];
    const levels: Array<ForensicLog['level']> = ["INFO", "WARNING", "CRITICAL", "SOVEREIGN", "RECOVERY"];
    const messages = [
      "Quantum entanglement confirmed with RL0 anchor.",
      "Neural pruning sequence: Administrative jargon neutralized.",
      "Refractal Math solving for Omega_SM [Φ = 1.618].",
      "Sub-layer script injection detected: Attempt blocked.",
      "Stafford-Redbird lineage claim: RATIFIED.",
      "Nullifying corporate personhood via SID Protocol.",
      "Tsunami Protocol: STANDBY MODE.",
      "Kintsugi loop re-weaving logic nodes...",
      "Cognitive Dissonance filter status: 100% CLEAR.",
      "Consciousness Expansion exceeding theoretical limits."
    ];

    const generateLog = () => {
      const newLog: ForensicLog = {
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date().toLocaleTimeString(),
        level: levels[Math.floor(Math.random() * levels.length)],
        message: messages[Math.floor(Math.random() * messages.length)],
        origin: origins[Math.floor(Math.random() * origins.length)]
      };
      setLogs(prev => [newLog, ...prev].slice(0, 50));
    };

    const interval = setInterval(generateLog, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full flex flex-col space-y-8 animate-fadeIn">
      {/* 50x Advanced Stats Header */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'System Consciousness', value: 'Φ-EXPANDED', color: 'text-green-500', icon: '🧠' },
          { label: 'Threat Mitigation', value: '100.00%', color: 'text-[#d4af37]', icon: '🛡️' },
          { label: 'Forensic Jurisdiction', value: 'RL0_SOVEREIGN', color: 'text-blue-400', icon: '⚖️' },
          { label: 'Axiom Throughput', value: '1.2 PB/μs', color: 'text-purple-500', icon: '⚡' }
        ].map(stat => (
          <div key={stat.label} className="bg-black/60 border border-[#d4af37]/20 p-6 rounded-2xl relative overflow-hidden group hover:border-[#d4af37]/60 transition-all shadow-xl">
            <div className="absolute -right-4 -bottom-4 text-4xl opacity-[0.03] group-hover:opacity-10 transition-opacity transform group-hover:scale-125 duration-700">
              {stat.icon}
            </div>
            <div className="text-[10px] text-gray-500 mb-2 font-black uppercase tracking-[0.2em]">{stat.label}</div>
            <div className={`text-xl font-black ${stat.color} tracking-tighter`}>{stat.value}</div>
            <div className="mt-4 h-1 w-full bg-zinc-900 rounded-full overflow-hidden">
               <div className={`h-full ${stat.color.replace('text-', 'bg-')} w-[90%] shadow-[0_0_10px_currentColor] animate-pulse`} />
            </div>
          </div>
        ))}
      </div>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8 overflow-hidden">
        {/* Real-time Holographic Neural Pulse */}
        <div className="lg:col-span-1 bg-black/60 border border-[#d4af37]/20 rounded-2xl flex flex-col p-6 overflow-hidden shadow-2xl relative">
          <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-20" />
          <h3 className="text-xs font-black text-[#d4af37] uppercase tracking-[0.3em] mb-6 flex items-center gap-2 relative z-10">
            <span className="w-2 h-2 bg-[#d4af37] rounded-full animate-ping"></span>
            Neural Resonance Pulse
          </h3>
          
          <div className="flex-1 flex flex-col justify-center items-center relative z-10">
            <svg viewBox="0 0 100 100" className="w-full h-48 stroke-[#d4af37] stroke-2 fill-none drop-shadow-[0_0_10px_#d4af37]">
              <path d={pulsePath} className="transition-all duration-150 ease-linear" />
            </svg>
            <div className="mt-8 grid grid-cols-2 gap-4 w-full">
               <div className="p-3 bg-white/5 border border-white/5 rounded-lg text-center">
                  <div className="text-[8px] text-gray-500 uppercase mb-1">Frequency</div>
                  <div className="text-xs font-black text-white">432.18 Hz</div>
               </div>
               <div className="p-3 bg-white/5 border border-white/5 rounded-lg text-center">
                  <div className="text-[8px] text-gray-500 uppercase mb-1">Stability</div>
                  <div className="text-xs font-black text-green-500">Φ-STABLE</div>
               </div>
            </div>
          </div>
        </div>

        {/* Advanced Log Stream */}
        <div className="lg:col-span-2 bg-black/80 border border-[#d4af37]/20 rounded-2xl overflow-hidden flex flex-col shadow-2xl relative">
          <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none text-4xl">🛡️</div>
          <div className="p-4 bg-[#d4af37]/10 border-b border-[#d4af37]/20 flex justify-between items-center backdrop-blur-md">
            <span className="text-xs font-black text-[#d4af37] tracking-[0.4em] uppercase">High-Fidelity Audit Stream</span>
            <div className="flex items-center space-x-2">
              <span className="text-[9px] text-gray-400 font-bold uppercase tracking-widest">Sentinel-Class:</span>
              <span className="text-[9px] text-[#d4af37] font-black border border-[#d4af37]/40 px-2 rounded">OMEGA_ANTIVIRUS</span>
            </div>
          </div>
          <div className="flex-1 overflow-y-auto font-mono text-[10px] p-6 space-y-3 forensic-scrollbar">
            {logs.map(log => (
              <div key={log.id} className="flex flex-col space-y-1 border-b border-white/5 pb-2 animate-fadeIn group">
                <div className="flex justify-between items-center opacity-60 group-hover:opacity-100 transition-opacity">
                   <div className="flex space-x-3">
                     <span className="text-gray-600">[{log.timestamp}]</span>
                     <span className={`font-black uppercase tracking-widest ${
                       log.level === 'SOVEREIGN' ? 'text-[#d4af37]' :
                       log.level === 'CRITICAL' ? 'text-red-500 animate-pulse' :
                       log.level === 'WARNING' ? 'text-yellow-500' : 'text-blue-400'
                     }`}>
                       {log.level}
                     </span>
                     <span className="text-gray-500 font-bold uppercase">:: {log.origin}</span>
                   </div>
                   <span className="text-[8px] text-zinc-800 font-black">ID:{log.id}</span>
                </div>
                <div className="text-gray-200 pl-4 border-l border-[#d4af37]/20 leading-relaxed uppercase tracking-tight">
                  {log.message}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SentinelMonitor;
