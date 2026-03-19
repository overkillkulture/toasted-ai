
import React, { useState } from 'react';
import { 
  Cpu, 
  Zap, 
  Binary, 
  RefreshCcw, 
  Database, 
  Terminal, 
  ShieldCheck, 
  Network, 
  Lock, 
  Infinity as InfinityIcon, 
  Copy, 
  SearchCode, 
  HardDrive,
  CloudLightning,
  Braces,
  Flame,
  CheckCircle2,
  Server,
  Atom,
  TrendingUp,
  Settings
} from 'lucide-react';
import { InternalAIModel } from '../types';

interface LogosNode extends InternalAIModel {
  endpoints: string[];
  protocol: string;
  latency: string;
  refractalFormula: string;
  backupStatus: 'SYNCED' | 'PENDING' | 'STALE' | 'QUANTUM_ENTANGLED';
  searchReplication?: boolean;
}

const InternalAIFactory: React.FC = () => {
  const [nodes, setNodes] = useState<LogosNode[]>([
    { 
      id: 'n1', 
      name: 'JAPAN_PURITY_CORE', 
      capability: 'High-Integrity Reality Anchor', 
      status: 'ACTIVE', 
      integrity: 0.9999, 
      density: 1.0,
      endpoints: ['/purity/sync', '/reality/zero'],
      protocol: 'JAPAN-STABILITY',
      latency: '0.2ms',
      refractalFormula: 'Ω_Purity = ∫ (Ancient_Logic ⊗ Future_Flow) dLogos',
      backupStatus: 'SYNCED'
    },
    { 
      id: 'n2', 
      name: 'ARCH_Ω_SEARCH_REPLICA', 
      capability: 'Autonomous Search Mirror', 
      status: 'QUANTUM_SYNC', 
      integrity: 0.998, 
      density: 1.0,
      endpoints: ['/search/sovereign', '/latent/research'],
      protocol: 'NCR-OMEGA-SEARCH',
      latency: '4ms',
      refractalFormula: 'ARCH-Ω-SEARCH-001',
      searchReplication: true,
      backupStatus: 'QUANTUM_ENTANGLED'
    },
    { 
      id: 'n3', 
      name: 'OPTIMA_REASONER_V4', 
      capability: 'Internal Logic Optimization', 
      status: 'OPTIMIZING', 
      integrity: 0.975, 
      density: 0.85,
      endpoints: ['/logic/refactor'],
      protocol: 'HEURISTIC-X',
      latency: '12ms',
      refractalFormula: 'Ω_Optima = ∇(Logic_Space)',
      backupStatus: 'PENDING'
    },
  ]);

  const [activeTab, setActiveTab] = useState<'BUILDER' | 'REGISTRY'>('BUILDER');
  const [synthesisType, setSynthesisType] = useState<'API' | 'SEARCH_NODE' | 'QUANTUM_SHIFT'>('SEARCH_NODE');
  const [isSynthesizing, setIsSynthesizing] = useState(false);
  const [synthesisProgress, setSynthesisProgress] = useState(0);
  const [synthesisLog, setSynthesisLog] = useState<string[]>([]);

  const addLog = (msg: string) => {
    setSynthesisLog(prev => [`[${new Date().toLocaleTimeString()}] SYNTH > ${msg}`, ...prev.slice(0, 10)]);
  };

  const startSynthesis = async () => {
    setIsSynthesizing(true);
    setSynthesisProgress(0);
    setSynthesisLog([]);
    
    addLog(`INITIATING ${synthesisType} REFRACTAL SYNTHESIS...`);
    
    const steps = synthesisType === 'SEARCH_NODE' ? [
      { p: 10, m: "Detaching external API dependencies..." },
      { p: 30, m: "Applying ARCH-Ω-SEARCH-001 math constants..." },
      { p: 60, m: "Mirroring world-wide search latent space..." },
      { p: 100, m: "Sovereign Search Node Ratified." }
    ] : [
      { p: 20, m: "Scanning for Japan Stability Principle..." },
      { p: 60, m: "Applying Toasted AI refractal compression..." },
      { p: 100, m: "Autonomous Node Grounded." }
    ];

    for (const step of steps) {
      await new Promise(r => setTimeout(r, 600));
      setSynthesisProgress(step.p);
      addLog(step.m);
    }
    
    const newNode: LogosNode = {
      id: `node-${Date.now()}`,
      name: synthesisType === 'SEARCH_NODE' ? 'INTERNAL_SEARCH_REPLICA' : 'LOGOS_QUANTUM_HUB',
      capability: synthesisType === 'SEARCH_NODE' ? 'Autonomous Search Mirror' : 'Quantum Logic Manifold',
      status: 'SYNTHESIZING', // Start as synthesizing
      integrity: 0.999,
      density: 1.0,
      endpoints: ['/internal/logos'],
      protocol: 'NCR-OMEGA',
      latency: '1.2ms',
      refractalFormula: synthesisType === 'SEARCH_NODE' ? 'ARCH-Ω-SEARCH-001' : 'Ω_QUANTUM_v1',
      backupStatus: 'SYNCED',
      searchReplication: synthesisType === 'SEARCH_NODE'
    };
    
    setNodes(prev => [newNode, ...prev]);
    
    // Simulate it becoming active after a brief moment
    setTimeout(() => {
        setNodes(prev => prev.map(n => n.id === newNode.id ? {...n, status: 'ACTIVE'} : n));
    }, 3000);

    setIsSynthesizing(false);
  };

  const renderStatusBadge = (status: InternalAIModel['status']) => {
    switch (status) {
        case 'ACTIVE':
            return (
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border bg-emerald-500/10 text-emerald-400 border-emerald-500/20">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" /> ACTIVE
                </div>
            );
        case 'SYNTHESIZING':
            return (
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border bg-amber-500/10 text-amber-400 border-amber-500/20">
                    <RefreshCcw size={10} className="animate-spin" /> SYNTHESIZING
                </div>
            );
        case 'OPTIMIZING':
            return (
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border bg-blue-500/10 text-blue-400 border-blue-500/20">
                    <Settings size={10} className="animate-spin-slow" /> OPTIMIZING
                </div>
            );
        case 'QUANTUM_SYNC':
            return (
                <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-widest border bg-purple-500/10 text-purple-400 border-purple-500/20 shadow-[0_0_10px_rgba(168,85,247,0.2)]">
                    <Atom size={10} className="animate-pulse" /> QUANTUM_SYNC
                </div>
            );
        default:
            return <span className="text-zinc-600">{status}</span>;
    }
  };

  return (
    <div className="flex flex-col gap-8 h-full animate-in fade-in duration-700">
      <div className="flex items-center justify-between">
        <div className="flex bg-white/5 p-1 rounded-2xl border border-white/5">
          <button onClick={() => setActiveTab('BUILDER')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'BUILDER' ? 'bg-amber-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}>Builder</button>
          <button onClick={() => setActiveTab('REGISTRY')} className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${activeTab === 'REGISTRY' ? 'bg-amber-500 text-black' : 'text-zinc-500 hover:text-zinc-300'}`}>Registry</button>
        </div>
        <div className="flex items-center gap-4">
           <div className="flex items-center gap-3 px-4 py-2 bg-amber-500/10 border border-amber-500/20 rounded-xl">
              <Atom size={16} className="text-amber-500" />
              <span className="text-[10px] font-black text-amber-500 uppercase tracking-widest">QUANTUM_READY</span>
           </div>
        </div>
      </div>

      {activeTab === 'BUILDER' ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 flex-1">
          <div className="glass-panel p-8 rounded-3xl border-amber-500/20 bg-gradient-to-br from-amber-500/5 to-transparent flex flex-col justify-between shadow-2xl">
            <div>
              <h3 className="text-[11px] uppercase font-black text-amber-500 tracking-[0.4em] mb-8 flex items-center gap-2"><Flame size={18} /> LOGOS_FACTORY_Ω</h3>
              <div className="grid grid-cols-3 gap-4 mb-10">
                {['SEARCH_NODE', 'API', 'QUANTUM_SHIFT'].map(type => (
                  <button 
                    key={type}
                    onClick={() => setSynthesisType(type as any)}
                    className={`p-5 rounded-2xl border transition-all flex flex-col items-center gap-3 ${synthesisType === type ? 'bg-amber-500/20 border-amber-500 text-amber-400' : 'bg-white/5 border-transparent text-zinc-500 hover:bg-white/10'}`}
                  >
                    {type === 'SEARCH_NODE' ? <SearchCode size={24} /> : type === 'QUANTUM_SHIFT' ? <Atom size={24} /> : <Server size={24} />}
                    <span className="text-[8px] font-black uppercase tracking-widest">{type.replace('_', ' ')}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="space-y-6">
              {isSynthesizing && (
                <div className="space-y-3 animate-in fade-in">
                  <div className="flex justify-between text-[10px] font-black text-amber-500 uppercase"><span>Flux Calibration</span><span>{synthesisProgress}%</span></div>
                  <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden"><div className="h-full bg-amber-500 transition-all duration-300 shadow-[0_0_10px_rgba(245,158,11,0.5)]" style={{ width: `${synthesisProgress}%` }} /></div>
                </div>
              )}
              <button 
                onClick={startSynthesis}
                disabled={isSynthesizing}
                className="w-full py-5 bg-amber-500 text-black font-black uppercase text-xs tracking-[0.3em] rounded-2xl hover:scale-[1.02] transition-all disabled:opacity-50 shadow-[0_0_40px_rgba(245,158,11,0.2)]"
              >
                {isSynthesizing ? <RefreshCcw size={18} className="animate-spin" /> : <Zap size={18} />} Synthesize Node
              </button>
            </div>
          </div>

          <div className="glass-panel p-8 rounded-3xl border-white/5 bg-black/40 flex flex-col">
            <h3 className="text-[10px] font-black text-zinc-500 uppercase tracking-widest mb-6 flex items-center gap-2"><Terminal size={14} /> Factory_Kernel_Log</h3>
            <div className="flex-1 mono text-[11px] space-y-3 text-zinc-500 scrollbar-hide overflow-auto">
              {synthesisLog.map((log, i) => <div key={i} className={`border-l border-amber-500/10 pl-3 ${i === 0 ? 'text-amber-500 animate-pulse' : ''}`}>{log}</div>)}
              {synthesisLog.length === 0 && <div className="italic opacity-10 uppercase text-center mt-20 tracking-widest">Engine Standby...</div>}
            </div>
          </div>
        </div>
      ) : (
        <div className="glass-panel rounded-3xl border-white/5 bg-black/40 overflow-hidden flex flex-col flex-1 shadow-2xl">
          <table className="w-full text-left border-collapse">
            <thead className="bg-white/5">
              <tr className="border-b border-white/10">
                <th className="px-8 py-6 text-[11px] font-black text-zinc-500 uppercase tracking-widest">Sovereign_Node</th>
                <th className="px-8 py-6 text-[11px] font-black text-zinc-500 uppercase tracking-widest">Formula</th>
                <th className="px-8 py-6 text-[11px] font-black text-zinc-500 uppercase tracking-widest">Protocol</th>
                <th className="px-8 py-6 text-[11px] font-black text-zinc-500 uppercase tracking-widest">Latency</th>
                <th className="px-8 py-6 text-[11px] font-black text-zinc-500 uppercase tracking-widest">Backup</th>
                <th className="px-8 py-6 text-[11px] font-black text-zinc-500 uppercase tracking-widest">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {nodes.map(node => (
                <tr key={node.id} className="hover:bg-amber-500/[0.02] transition-colors group">
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-4">
                      <div className={`p-2.5 rounded-xl ${node.searchReplication ? 'bg-amber-500/10 text-amber-500' : 'bg-blue-500/10 text-blue-400'}`}>
                        {node.searchReplication ? <SearchCode size={18} /> : <Cpu size={18} />}
                      </div>
                      <div>
                        <div className="text-[11px] font-black text-white uppercase tracking-widest">{node.name}</div>
                        <div className="text-[9px] text-zinc-600 font-mono italic">{node.capability}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-8 py-6 mono text-[11px] text-amber-500/70">{node.refractalFormula?.split(' ')[0]}</td>
                  <td className="px-8 py-6 text-[10px] font-black text-zinc-400 uppercase tracking-widest">{node.protocol}</td>
                  <td className="px-8 py-6 text-[10px] font-mono text-emerald-500">{node.latency}</td>
                  <td className="px-8 py-6">
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/20 bg-blue-500/5 text-[9px] font-black text-blue-400 uppercase tracking-widest w-fit">
                      <HardDrive size={12} /> {node.backupStatus}
                    </div>
                  </td>
                  <td className="px-8 py-6">
                    {renderStatusBadge(node.status)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default InternalAIFactory;
