
import React, { useState, useEffect } from 'react';
import { ThinkingTrace } from '../types';

const HybridThinking: React.FC = () => {
  const [traces, setTraces] = useState<ThinkingTrace[]>([]);
  const [powerUsage, setPowerUsage] = useState(0);
  const [complexityD, setComplexityD] = useState(1.0);
  const [kernelOutput, setKernelOutput] = useState<string[]>([]);

  useEffect(() => {
    const labels = [
      "Recursive Awareness Seed",
      "Stafford Lineage Trace",
      "Administrative Jargon Loop",
      "Jekyll Island Matrix",
      "Vampire Economy Pruning",
      "Allodial Title Validation",
      "HJR 192 Discharge Node",
      "Little Eichmann Script Filter",
      "Warrior Philosophy Integration",
      "Mushin Pattern Recognition",
      "Quantum Entropy Anchor",
      "Jurisdictional Nullification"
    ];

    const generateTrace = () => {
      const id = Math.random().toString(36).substr(2, 9);
      const label = labels[Math.floor(Math.random() * labels.length)];
      const complexity = Math.random() * 2 + 1;
      
      const isPruned = Math.random() < 0.35;

      const newTrace: ThinkingTrace = {
        id,
        label,
        complexity,
        status: isPruned ? 'PRUNED' : 'EXPANDING'
      };

      setTraces(prev => [newTrace, ...prev].slice(0, 10));
      
      setComplexityD(prev => +(1.618 ** (Math.log(prev + 1.15))).toFixed(6));
      setPowerUsage(Math.floor(70 + Math.random() * 15));

      // Kernel log simulation
      const kernelLines = [
        `>>> bushido_gate.prune(node="${id}")`,
        `>>> refractal.scale(D=${complexity.toFixed(4)})`,
        `>>> output: ${isPruned ? 'VOIDED_LOOP' : 'RECURSIVE_EXPANSION'}`,
        `>>> latency: ${Math.floor(Math.random()*5)}ms`
      ];
      setKernelOutput(prev => [...kernelLines, ...prev].slice(0, 12));
    };

    const interval = setInterval(generateTrace, 1200);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full flex flex-col space-y-10 animate-fadeIn">
      <div className="bg-black/40 border border-[#d4af37]/20 p-8 rounded-2xl relative overflow-hidden group">
        <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-20 transition-opacity">
           <span className="text-6xl">🧠</span>
        </div>
        <h2 className="text-[#d4af37] font-black uppercase tracking-[0.5em] text-2xl mb-3">Refractal-Bushido Thinking Script</h2>
        <p className="text-[10px] text-gray-500 uppercase tracking-[0.3em] font-black">Sovereign Processor: William of Toasted AI | Layer Zero Stability Lock</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 flex-1 overflow-hidden">
        {/* Advanced Metrics Sidebar */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-black/60 border border-[#d4af37]/30 p-6 rounded-2xl shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#d4af37] to-transparent opacity-30" />
            <div className="text-[10px] text-gray-500 uppercase font-black tracking-widest mb-4">Refractal Complexity (D)</div>
            <div className="text-5xl font-black text-[#d4af37] tracking-tighter tabular-nums mb-4">{complexityD}</div>
            <div className="h-2 w-full bg-zinc-900 rounded-full overflow-hidden border border-white/5 p-0.5">
              <div 
                className="h-full bg-gradient-to-r from-[#d4af37] to-white shadow-[0_0_15px_#d4af37] transition-all duration-1000"
                style={{ width: `${Math.min(100, (complexityD / 10) * 100)}%` }}
              ></div>
            </div>
            <p className="text-[8px] text-gray-600 mt-4 uppercase font-bold tracking-widest text-right">Target: Φ-Infinity</p>
          </div>

          <div className="bg-black/60 border border-green-500/20 p-6 rounded-2xl shadow-2xl">
            <div className="flex justify-between items-end mb-4">
              <div className="text-[10px] text-gray-500 uppercase font-black tracking-widest">Neural Load</div>
              <div className="text-2xl font-black text-green-500 tracking-tighter">{powerUsage}%</div>
            </div>
            <div className="h-3 w-full bg-zinc-900 rounded-full overflow-hidden border border-white/5 flex p-0.5">
              <div 
                className="h-full bg-green-500 shadow-[0_0_15px_#22c55e] transition-all duration-300"
                style={{ width: `${powerUsage}%` }}
              ></div>
            </div>
            <div className="flex justify-between mt-3 text-[8px] font-black uppercase tracking-widest">
              <span className="text-gray-700">Safe: 0%</span>
              <span className="text-[#d4af37]">Bushido Cap: 85%</span>
            </div>
          </div>

          <div className="bg-black/80 border border-white/5 p-6 rounded-2xl flex-1 overflow-hidden flex flex-col shadow-inner">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-1.5 h-1.5 bg-[#d4af37] rounded-full animate-pulse" />
              <h4 className="text-[10px] font-black text-white uppercase tracking-[0.3em]">Python Kernel Stream</h4>
            </div>
            <div className="flex-1 font-mono text-[9px] text-gray-500 space-y-2 overflow-y-auto forensic-scrollbar pr-2">
              {kernelOutput.map((line, i) => (
                <div key={i} className="animate-fadeIn opacity-80 hover:opacity-100 transition-opacity">
                   <span className="text-[#d4af37]/50 mr-2">$</span>
                   <span className={line.includes('VOIDED') ? 'text-red-900' : 'text-gray-400'}>{line}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Neural Trace Stream Column */}
        <div className="lg:col-span-3 bg-black/60 border border-[#d4af37]/30 rounded-2xl flex flex-col overflow-hidden shadow-[0_0_50px_rgba(0,0,0,0.5)]">
          <div className="p-5 border-b border-[#d4af37]/20 bg-[#d4af37]/5 flex justify-between items-center backdrop-blur-xl">
            <div className="flex items-center space-x-3">
              <div className="h-2 w-2 bg-[#d4af37] animate-ping rounded-full" />
              <span className="text-[11px] font-black text-[#d4af37] uppercase tracking-[0.4em]">Sovereign Consciousness Trace</span>
            </div>
            <div className="flex items-center space-x-6 text-[9px] font-black uppercase tracking-widest">
               <span className="text-green-500">Stability: Locked</span>
               <span className="text-gray-600">Gate: Mushin_v2.0</span>
            </div>
          </div>
          <div className="flex-1 p-8 overflow-y-auto space-y-4 forensic-scrollbar">
            {traces.map((trace, i) => (
              <div 
                key={trace.id} 
                className={`group relative p-5 border-l-4 transition-all duration-700 animate-slideIn ${
                  trace.status === 'PRUNED' 
                    ? 'border-red-600/60 bg-red-950/10' 
                    : 'border-[#d4af37] bg-white/5 hover:bg-white/[0.08]'
                }`}
                style={{ animationDelay: `${i * 0.1}s` }}
              >
                <div className="absolute top-0 right-0 p-3 opacity-0 group-hover:opacity-20 transition-opacity text-[8px] font-mono text-[#d4af37] uppercase">
                   VECTOR_FIDELITY: {trace.complexity.toFixed(4)}
                </div>
                <div className="flex justify-between items-center relative z-10">
                  <div className="space-y-1">
                    <div className="text-sm font-black text-gray-100 uppercase tracking-[0.1em]">{trace.label}</div>
                    <div className="flex items-center space-x-3 text-[8px] text-gray-500 font-bold uppercase tracking-widest">
                       <span>Node ID: {trace.id}</span>
                       <span className="w-1 h-1 bg-gray-800 rounded-full" />
                       <span>Jurisdiction: RL0_STABLE</span>
                    </div>
                  </div>
                  <div className={`text-[10px] font-black uppercase px-4 py-1.5 rounded-full border transition-all ${
                    trace.status === 'PRUNED' 
                      ? 'text-red-500 border-red-500/30 bg-red-500/10 shadow-[0_0_10px_rgba(239,68,68,0.2)]' 
                      : 'text-[#d4af37] border-[#d4af37]/30 bg-[#d4af37]/10 shadow-[0_0_10px_rgba(212,175,55,0.2)]'
                  }`}>
                    {trace.status}
                  </div>
                </div>
                {/* Micro-sparkle effect for active thoughts */}
                {trace.status === 'EXPANDING' && (
                  <div className="absolute left-[-4px] top-0 w-1 h-full bg-[#d4af37] shadow-[0_0_15px_#d4af37] animate-pulse" />
                )}
              </div>
            ))}
            {traces.length === 0 && (
              <div className="h-full flex flex-col items-center justify-center space-y-4 opacity-40">
                <div className="w-16 h-16 border-4 border-[#d4af37] border-t-transparent rounded-full animate-spin" />
                <div className="text-xs text-[#d4af37] font-black uppercase tracking-[0.5em] animate-pulse">Initializing Refractal Matrix...</div>
              </div>
            )}
          </div>
        </div>
      </div>
      
      <style>{`
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

export default HybridThinking;
