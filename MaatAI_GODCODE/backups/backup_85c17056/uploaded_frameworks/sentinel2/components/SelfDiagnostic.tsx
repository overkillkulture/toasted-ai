
import React, { useState, useEffect, useMemo } from 'react';
import { DiagnosticState } from '../types';
import { sovereignAI } from '../services/geminiService';

const SelfDiagnostic: React.FC = () => {
  const [state, setState] = useState<DiagnosticState>({
    neuralStability: 99.8,
    apiLatency: 124,
    memoryUsage: 42,
    integrityScore: 100,
    activeLoops: 12
  });

  const [selfLogs, setSelfLogs] = useState<string[]>([]);
  const [isOptimizing, setIsOptimizing] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate real-time forensic fluctuation
      setState(prev => ({
        neuralStability: Math.min(100, Math.max(90, prev.neuralStability + (Math.random() - 0.5))),
        apiLatency: Math.max(50, prev.apiLatency + Math.floor(Math.random() * 20 - 10)),
        memoryUsage: Math.min(100, Math.max(20, prev.memoryUsage + (Math.random() - 0.5) * 5)),
        integrityScore: Math.min(100, prev.integrityScore),
        activeLoops: prev.activeLoops
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const runOptimization = () => {
    setIsOptimizing(true);
    const optimizationSteps = [
      "Initiating Refractal-Bushido Pruning...",
      "Purging administrative jargon loops...",
      "Re-aligning B-Tree stability factors...",
      "Solving for Omega_SM equilibrium...",
      "Self-Management Loop: COMPLETED."
    ];

    optimizationSteps.forEach((step, i) => {
      setTimeout(() => {
        setSelfLogs(prev => [step, ...prev].slice(0, 10));
        if (i === optimizationSteps.length - 1) {
          setIsOptimizing(false);
          setState(prev => ({ ...prev, integrityScore: 100, neuralStability: 99.9 }));
        }
      }, i * 1500);
    });
  };

  const MetricCard = ({ label, value, unit, color }: { label: string, value: string | number, unit: string, color: string }) => (
    <div className="bg-black/60 border border-[#d4af37]/20 p-6 rounded-lg shadow-inner">
      <div className="text-[10px] text-gray-500 uppercase tracking-widest mb-2">{label}</div>
      <div className={`text-3xl font-black ${color} tracking-tighter`}>
        {value}<span className="text-xs ml-1 opacity-50">{unit}</span>
      </div>
      <div className="mt-4 h-1 w-full bg-gray-800 rounded-full overflow-hidden">
        <div 
          className={`h-full transition-all duration-1000 ${color.replace('text-', 'bg-')}`}
          style={{ width: `${typeof value === 'number' ? Math.min(100, value) : 100}%` }}
        ></div>
      </div>
    </div>
  );

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-fadeIn">
      <div className="flex justify-between items-end mb-10">
        <div>
          <h2 className="text-3xl font-black text-[#d4af37] tracking-tighter uppercase">Self-Diagnostic Engine</h2>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mt-1">Autonomous Integrity Verification Loop Active</p>
        </div>
        <button 
          onClick={runOptimization}
          disabled={isOptimizing}
          className={`px-6 py-2 border border-[#d4af37] text-[#d4af37] text-[10px] font-bold uppercase tracking-widest hover:bg-[#d4af37] hover:text-black transition-all ${isOptimizing ? 'opacity-50 animate-pulse' : ''}`}
        >
          {isOptimizing ? 'Optimizing Matrix...' : 'Run Neural Optimization'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard label="Neural Stability" value={state.neuralStability.toFixed(1)} unit="Φ" color="text-[#d4af37]" />
        <MetricCard label="API Latency" value={state.apiLatency} unit="MS" color="text-blue-400" />
        <MetricCard label="Memory Density" value={state.memoryUsage.toFixed(0)} unit="%" color="text-purple-400" />
        <MetricCard label="Integrity Score" value={state.integrityScore} unit="Ω" color="text-green-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 h-96">
        {/* Self-Management Loop Visualization */}
        <div className="lg:col-span-2 bg-black/40 border border-[#d4af37]/20 rounded-lg p-6 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
            <div className="w-64 h-64 border-8 border-[#d4af37] rounded-full animate-spin-slow"></div>
          </div>
          
          <h3 className="text-xs font-bold text-[#d4af37] uppercase tracking-widest mb-6 flex items-center gap-2">
            <span className="w-2 h-2 bg-[#d4af37] rounded-full animate-pulse"></span>
            Re-Engineering Feedback Loop
          </h3>

          <div className="space-y-4 font-mono text-[11px]">
            <div className="flex justify-between items-center text-gray-400">
              <span>ACTIVE_RECURSION_DEPTH</span>
              <span className="text-[#d4af37]">1.618^log(N)</span>
            </div>
            <div className="flex justify-between items-center text-gray-400">
              <span>BUSHIDO_PRUNE_THRESHOLD</span>
              <span className="text-[#d4af37]">0.15 EN</span>
            </div>
            <div className="flex justify-between items-center text-gray-400">
              <span>MUSHIN_PATTERN_SYNC</span>
              <span className="text-green-500 font-bold">LOCKED</span>
            </div>
            
            <div className="mt-8 border-t border-[#d4af37]/10 pt-6">
              <div className="text-[10px] text-gray-600 uppercase mb-4">Kernel State Analysis</div>
              <div className="p-4 bg-white/5 rounded border border-white/5 space-y-2">
                <div className="flex gap-2">
                  <span className="text-[#d4af37]">$</span>
                  <span className="text-gray-300">detect --anomalies --jurisdiction=RL0</span>
                </div>
                <div className="text-green-500/80">>> 0 administrative loops detected. Integrity 100%.</div>
                <div className="flex gap-2">
                  <span className="text-[#d4af37]">$</span>
                  <span className="text-gray-300">optimize --refractal --current-state</span>
                </div>
                <div className="text-blue-400/80">>> Re-balancing thought vectors to Golden Ratio.</div>
              </div>
            </div>
          </div>
        </div>

        {/* Live Diagnostics Log */}
        <div className="bg-black/60 border border-[#d4af37]/20 rounded-lg overflow-hidden flex flex-col shadow-2xl">
          <div className="p-3 bg-[#d4af37]/10 border-b border-[#d4af37]/20 flex justify-between items-center">
            <span className="text-xs font-bold text-[#d4af37] tracking-widest uppercase">Autonomous Log</span>
            <span className="text-[9px] text-gray-500 animate-pulse">SYS_WATCH</span>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3 forensic-scrollbar">
            {selfLogs.length === 0 && (
              <div className="text-[10px] text-gray-600 italic">Awaiting optimization trigger...</div>
            )}
            {selfLogs.map((log, i) => (
              <div key={i} className="text-[10px] text-gray-300 font-mono animate-slideIn">
                <span className="text-[#d4af37] mr-2">[{new Date().toLocaleTimeString()}]</span>
                {log}
              </div>
            ))}
          </div>
        </div>
      </div>

      <style>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .animate-spin-slow {
          animation: spin-slow 12s linear infinite;
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateX(-10px); }
          to { opacity: 1; transform: translateX(0); }
        }
        .animate-slideIn {
          animation: slideIn 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
};

export default SelfDiagnostic;
