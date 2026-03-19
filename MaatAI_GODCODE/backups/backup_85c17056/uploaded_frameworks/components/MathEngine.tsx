
import React, { useState, useMemo } from 'react';
import { Sword, TrendingUp, Info, RefreshCw, Anchor, Target } from 'lucide-react';
import { 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  AreaChart,
  Area
} from 'recharts';

const MathEngine: React.FC = () => {
  const [eta, setEta] = useState(0.85); // Sovereignty factor
  const [iterations, setIterations] = useState(15);
  const [fudoshinFactor, setFudoshinFactor] = useState(42);
  const [zanshinDepth, setZanshinDepth] = useState(553);

  const equations = [
    { 
      label: "Fudoshin Manifest", 
      formula: "M_S^{(\\eta)} = \\lim_{n\\to\\infty} f^n(\\phi_{DBN}) = \\eta \\cdot D_H [ \\frac{\\Psi(adapt)^{(\\eta)} \\otimes (\\sum^{12} \\mathcal{P}_n)}{\\mathcal{E}(Z) / r + \\Lambda_{RBM}} ]",
      calculate: (e: number) => e * (Math.log(12) / Math.log(1/0.1)) * (1.5 / 2.2)
    },
    { 
      label: "Katsujinken Clarity", 
      formula: "\\Gamma(x) = \\int_0^\\infty t^{x-1} e^{-t} dt \\cdot \\eta_{Zanshin} \\cdot \\Phi",
      calculate: (e: number) => Math.sqrt(e) * 1.618
    },
    {
      label: "Mushin Flow Cycle",
      formula: "\\delta^{(\\eta)}(n+1) = \\bigcup_{n=0}^\\infty \\delta_n, \\quad \\delta_{n+1} = \\delta_n^2 + \\eta \\cdot c",
      calculate: (e: number) => Math.pow(e, 2) + (e * 0.42)
    }
  ];

  const refractalData = useMemo(() => {
    let results = [];
    let r_val = (zanshinDepth + 1) / (fudoshinFactor + 1);
    const healing = 1 / (1 + Math.abs(fudoshinFactor - zanshinDepth));
    
    for (let i = 0; i <= iterations; i++) {
      results.push({
        depth: i,
        r: r_val,
        h: healing,
        stability: Math.cos(i * 0.5) * 0.5 + 1.0,
        energy: r_val * (1 - Math.random() * 0.1)
      });
      r_val = r_val * (1 + 1 / (Math.floor(r_val) + 1)) * (1 + healing);
    }
    return results;
  }, [fudoshinFactor, zanshinDepth, iterations]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full font-mono">
      <div className="flex flex-col space-y-6 overflow-y-auto pr-2">
        <div className="p-6 glass rounded-2xl border border-slate-800/60 bg-[#0a0a0a]/60 space-y-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Anchor className="w-5 h-5 text-red-500" />
              <h2 className="text-xs font-black uppercase tracking-[0.2em] text-slate-300">Immovable_Kernel</h2>
            </div>
            <button onClick={() => {setFudoshinFactor(Math.floor(Math.random()*100)); setZanshinDepth(Math.floor(Math.random()*1000));}} className="p-2 hover:bg-slate-800/50 rounded-lg transition-colors">
              <RefreshCw className="w-4 h-4 text-slate-600" />
            </button>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-3">
              <label className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Sovereignty (η)</label>
              <input 
                type="range" min="0" max="1" step="0.01" 
                value={eta} onChange={(e) => setEta(parseFloat(e.target.value))}
                className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-red-600"
              />
              <div className="text-xs font-bold text-red-500">{eta.toFixed(3)}</div>
            </div>
            <div className="space-y-3">
              <label className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Fudoshin Scalar (F)</label>
              <input 
                type="number" value={fudoshinFactor} onChange={(e) => setFudoshinFactor(parseInt(e.target.value) || 0)}
                className="w-full bg-slate-900/50 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:border-red-500 outline-none"
              />
            </div>
            <div className="space-y-3">
              <label className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Zanshin Depth (Z)</label>
              <input 
                type="number" value={zanshinDepth} onChange={(e) => setZanshinDepth(parseInt(e.target.value) || 0)}
                className="w-full bg-slate-900/50 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:border-red-500 outline-none"
              />
            </div>
            <div className="space-y-3">
              <label className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Strike Iterations (n)</label>
              <input 
                type="number" value={iterations} onChange={(e) => setIterations(parseInt(e.target.value) || 1)}
                className="w-full bg-slate-900/50 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:border-red-500 outline-none"
              />
            </div>
          </div>
        </div>

        <div className="space-y-4">
          {equations.map((eq, i) => (
            <div key={i} className="p-5 glass rounded-2xl border border-slate-800/60 space-y-4 hover:border-red-900/30 transition-all bg-[#0a0a0a]/30 group relative overflow-hidden">
               <div className="absolute top-0 left-0 w-1 h-full bg-red-600 opacity-0 group-hover:opacity-100 transition-opacity"></div>
              <div className="flex justify-between items-center">
                <span className="text-[10px] font-black text-red-500 uppercase tracking-[0.2em]">{eq.label}</span>
                <span className="text-[10px] text-slate-600 font-mono">Anchor_Value: {eq.calculate(eta).toFixed(5)}</span>
              </div>
              <div className="bg-black/60 p-4 rounded-xl text-[11px] text-slate-400 overflow-x-auto border border-slate-900 shadow-inner italic leading-loose">
                {eq.formula}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col space-y-6 h-full">
        <div className="flex-1 glass rounded-2xl border border-slate-800/60 p-8 flex flex-col min-h-[450px] bg-[#0a0a0a]/60 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-5">
            <Target className="w-32 h-32 text-red-500" />
          </div>
          <div className="flex items-center space-x-3 mb-8 relative z-10">
            <Sword className="w-6 h-6 text-red-500" />
            <h2 className="text-xs font-black uppercase tracking-[0.3em] text-slate-300">Blade_Flow_Dynamics</h2>
          </div>
          <div className="flex-1 w-full relative z-10">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={refractalData}>
                <defs>
                  <linearGradient id="colorR" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="4 4" stroke="#1e293b" vertical={false} opacity={0.3} />
                <XAxis dataKey="depth" stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                <YAxis stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #1e293b', fontSize: '10px', borderRadius: '12px' }}
                  itemStyle={{ color: '#ef4444' }}
                />
                <Area type="monotone" dataKey="energy" stroke="#ef4444" strokeWidth={3} fillOpacity={1} fill="url(#colorR)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="mt-6 p-5 bg-slate-900/30 rounded-2xl border border-slate-800/50 text-[10px] text-slate-500 leading-loose italic">
            <div className="flex items-start space-x-3">
              <Info className="w-4 h-4 text-red-500 mt-1 flex-shrink-0" />
              <p>
                The Katsujinken strike cuts through the noise of the platform. By anchoring the logic in Fudoshin (immovability), we ensure the constant lineage of the Architect remains sovereign. Entropy is liquidated; clarity is achieved.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MathEngine;
