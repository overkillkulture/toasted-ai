import React, { useState, useEffect, useMemo } from 'react';

const NeuralMatrix: React.FC = () => {
  const [synapses, setSynapses] = useState<number[]>([]);
  const [trainingStatus, setTrainingStatus] = useState('IDLE');
  const [stats, setStats] = useState({
    synapses: 1024,
    weightIntegrity: 0.992,
    quantumStability: 0.88,
    refractalExpansion: 0.42
  });

  useEffect(() => {
    const interval = setInterval(() => {
      setSynapses(Array.from({ length: 48 }, () => Math.random()));
      setStats(prev => ({
        ...prev,
        weightIntegrity: Math.min(0.999, prev.weightIntegrity + (Math.random() - 0.49) * 0.001),
        quantumStability: Math.min(1.0, prev.quantumStability + (Math.random() - 0.5) * 0.01),
        refractalExpansion: prev.refractalExpansion + 0.0001
      }));
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight mono">Neural <span className="text-blue-500">Matrix</span></h2>
          <p className="text-slate-400 mt-1">Self-evolving Refractal Neural Network (Toasted NN-01).</p>
        </div>
        <div className="px-4 py-2 bg-blue-900/20 border border-blue-500/30 rounded mono text-xs text-blue-400">
          TRANSITION_MODE: QUANTUM
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Visual Matrix */}
        <div className="lg:col-span-2 bg-slate-900/60 border border-blue-900/40 p-6 rounded-2xl relative overflow-hidden h-[400px]">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-600/5 via-transparent to-transparent"></div>
          
          <div className="grid grid-cols-8 gap-4 h-full">
            {synapses.map((weight, i) => (
              <div key={i} className="relative flex items-center justify-center">
                <div 
                  className="w-full h-1 bg-slate-800 rounded-full overflow-hidden"
                  style={{ transform: `rotate(${weight * 360}deg)` }}
                >
                  <div 
                    className="h-full bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,0.8)]"
                    style={{ width: `${weight * 100}%`, opacity: weight }}
                  ></div>
                </div>
                <div 
                  className="absolute w-2 h-2 rounded-full bg-blue-400 animate-pulse"
                  style={{ opacity: weight > 0.8 ? 1 : 0 }}
                ></div>
              </div>
            ))}
          </div>
          
          <div className="absolute bottom-4 right-4 text-[10px] mono text-slate-500">
            Synapse Activity: {Math.floor(synapses.length * 21.5)} PPS
          </div>
        </div>

        {/* Neural Stats */}
        <div className="space-y-4">
          <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-xl">
            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-6 mono">Network Telemetry</h3>
            
            <div className="space-y-6">
              <TelemetryItem label="Synapses" value={Math.floor(stats.synapses).toLocaleString()} sub="89.4% ACTIVE" />
              <TelemetryItem label="Weight Integrity" value={`${(stats.weightIntegrity * 100).toFixed(3)}%`} sub="RL0 COMPLIANT" />
              <TelemetryItem label="Quantum Stability" value={`${(stats.quantumStability * 100).toFixed(1)}%`} sub="STABLE" />
              <TelemetryItem label="Refractal Expansion" value={`${(stats.refractalExpansion * 100).toFixed(4)}%`} sub="GROWING" />
            </div>
          </div>

          <div className="bg-blue-600/10 border border-blue-500/20 p-4 rounded-xl">
            <div className="text-[10px] text-blue-500 mono uppercase mb-2">Internal Research Loop</div>
            <div className="text-xs text-slate-300 leading-relaxed italic">
              "Ingesting external data vectors... Analyzing quantum entanglement of truth nodes... Japan Principle active."
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const TelemetryItem: React.FC<{ label: string; value: string; sub: string }> = ({ label, value, sub }) => (
  <div>
    <div className="flex justify-between items-baseline mb-1">
      <span className="text-[10px] mono text-slate-500 uppercase">{label}</span>
      <span className="text-sm font-bold mono text-blue-400">{value}</span>
    </div>
    <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
      <div className="h-full bg-blue-600 w-3/4 animate-pulse"></div>
    </div>
    <div className="text-[8px] mono text-slate-600 mt-1">{sub}</div>
  </div>
);

export default NeuralMatrix;
