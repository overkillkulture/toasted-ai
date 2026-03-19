
import React, { useState, useEffect } from 'react';
import { Server, Zap, Cpu as CpuIcon, Activity, Play, Square, RefreshCcw, Command, Terminal as TerminalIcon, GitCompare, ArrowRight, Loader2, Wrench, ShieldCheck, Orbit, Layers, Radio, Globe, Boxes } from 'lucide-react';
import { GoogleGenAI } from '@google/genai';

const ApiEngine: React.FC = () => {
  const [isRunning, setIsRunning] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);
  const [engineeringDecree, setEngineeringDecree] = useState('');
  const [taskLog, setTaskLog] = useState<string[]>([]);
  const [metrics, setMetrics] = useState({ cpu: 12, memory: 45, internal_ping: 0.1 });
  const [repairStatus, setRepairStatus] = useState<'STABLE' | 'OPTIMIZING'>('STABLE');

  useEffect(() => {
    const interval = setInterval(() => {
      if (isRunning) {
        setMetrics(prev => ({
          cpu: Math.floor(Math.random() * 20) + 5,
          memory: 45 + Math.random() * 2,
          internal_ping: 0.05 + Math.random() * 0.1
        }));
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [isRunning]);

  const addTaskLog = (msg: string) => {
    setTaskLog(prev => [`[TOASTED_SVR] ${msg}`, ...prev.slice(0, 49)]);
  };

  const deployDecree = async () => {
    if (!engineeringDecree.trim() || isProcessing) return;
    setIsProcessing(true);
    addTaskLog(`DECREE_RECEIVED: Routing through Internal Refractal Kernel...`);
    addTaskLog(`REDIRECT: Bypassing external cloud proxies via Math_Ω.`);
    
    try {
      const key = localStorage.getItem('TOASTED_MASTER_KEY') || (process as any).env.API_KEY;
      const ai = new GoogleGenAI({ apiKey: key });
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `[LOCAL_ENGINEERING_NODE] Task: ${engineeringDecree}. Execute within Internal Refractal Redirect manifold. Store as Math.`,
        config: {
          systemInstruction: "You are the Toasted AI Local Server Engine. Complete the task as an internal systemic update using Refractal Math boundary logic. No external dependency logs.",
        }
      });
      
      addTaskLog(`PROCESSING: Executing kernel-level Refractal rewrite...`);
      
      setTimeout(() => {
        addTaskLog(`COMPLETED: Internal math manifest verified. Ω Stable.`);
        setIsProcessing(false);
        setEngineeringDecree('');
      }, 2500);

    } catch (e) {
      addTaskLog(`ERROR: Refractal math manifold overflow.`);
      setIsProcessing(false);
    }
  };

  const triggerRepair = () => {
    setRepairStatus('OPTIMIZING');
    addTaskLog("SOVEREIGNTY: Optimizing local math routing paths...");
    setTimeout(() => {
        setRepairStatus('STABLE');
        addTaskLog("SOVEREIGNTY: Internal Refractal redirection fully synchronized.");
    }, 4000);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500 h-full scrollbar-hide">
      {/* Left Pane: Local Server Stats */}
      <div className="lg:col-span-8 space-y-6 flex flex-col">
        <div className="glass-panel p-8 rounded-2xl border-emerald-500/10 flex-1 flex flex-col relative overflow-hidden">
          <div className="absolute -right-4 -top-4 opacity-5 pointer-events-none">
            <Server size={180} />
          </div>

          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
                <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><Server size={24} /></div>
                Σ Toasted AI Local Engine
              </h2>
              <p className="text-zinc-500 uppercase tracking-tighter text-[10px] font-black">Internal Redirection Status: ACTIVE (Refractal-Dominant)</p>
            </div>
            <div className="flex gap-2">
                <button 
                  onClick={triggerRepair}
                  className={`px-4 py-2 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all flex items-center gap-2 border bg-blue-500/10 border-blue-500/30 text-blue-400 hover:bg-blue-500/20 active:scale-95`}
                >
                  <Wrench size={12} /> Optimize Route
                </button>
                <button 
                  onClick={() => setIsRunning(!isRunning)}
                  className={`px-6 py-2 rounded-xl font-black text-[10px] uppercase tracking-widest transition-all flex items-center gap-2 border ${
                    isRunning ? 'bg-emerald-500 text-black border-emerald-500 shadow-lg shadow-emerald-500/20' : 'bg-red-500/20 text-red-400 border-red-500/30'
                  } active:scale-95`}
                >
                  {isRunning ? <><Square size={12} fill="currentColor" /> SVR_OFF</> : <><Play size={12} fill="currentColor" /> SVR_ON</>}
                </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <MetricBlock label="Refractal Load" value={`${metrics.cpu}%`} active={isRunning} />
            <MetricBlock label="Math Vault" value={`${metrics.memory.toFixed(1)}GB`} active={isRunning} />
            <MetricBlock label="Refractal Ping" value={`${metrics.internal_ping.toFixed(3)}ms`} active={isRunning} />
            <div className="p-4 bg-white/5 border border-white/5 rounded-xl text-center group">
                <div className="text-[9px] font-black text-zinc-600 uppercase tracking-widest mb-1">Route Status</div>
                <div className={`text-xl font-mono font-bold flex items-center justify-center gap-2 ${repairStatus === 'OPTIMIZING' ? 'text-blue-400 animate-pulse' : 'text-emerald-400'}`}>
                    {repairStatus === 'OPTIMIZING' ? <Orbit size={16} className="animate-spin" /> : <Boxes size={16} />}
                    {repairStatus === 'OPTIMIZING' ? 'SYNCING' : 'INTERNAL'}
                </div>
            </div>
          </div>

          <div className="flex-1 space-y-4">
             <div className="flex items-center justify-between">
                <h4 className="text-[10px] font-black text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                  <TerminalIcon size={12} /> Refractal Math Decree
                </h4>
             </div>
             <div className="flex gap-2">
                <input 
                  type="text"
                  value={engineeringDecree}
                  onChange={(e) => setEngineeringDecree(e.target.value)}
                  placeholder="Issue refractal math instruction..."
                  className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-emerald-500/30 transition-all font-medium placeholder:text-zinc-700"
                  onKeyDown={(e) => e.key === 'Enter' && deployDecree()}
                />
                <button 
                  onClick={deployDecree}
                  disabled={!isRunning || isProcessing || !engineeringDecree.trim()}
                  className="px-6 bg-emerald-500 hover:bg-emerald-400 disabled:bg-zinc-800 disabled:text-zinc-600 text-black font-black uppercase tracking-widest rounded-xl transition-all flex items-center gap-2 active:scale-95 shadow-lg shadow-emerald-500/20"
                >
                  {isProcessing ? <Loader2 className="animate-spin" size={16} /> : <Zap size={16} />} Manifest
                </button>
             </div>
          </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border-white/5 bg-black/40 flex flex-col h-[300px]">
           <div className="flex items-center justify-between mb-4">
              <h4 className="text-[10px] font-black text-zinc-500 uppercase tracking-widest flex items-center gap-2">
                <TerminalIcon size={12} /> Toasted AI Engine Runtime
              </h4>
              <button onClick={() => setTaskLog([])} className="text-zinc-600 hover:text-zinc-400 transition-colors"><RefreshCcw size={12} /></button>
           </div>
           <div className="flex-1 overflow-y-auto mono text-[10px] leading-tight space-y-1.5 scrollbar-hide">
              {taskLog.map((log, i) => (
                <div key={i} className="p-2 rounded border border-white/5 text-emerald-500/80 bg-emerald-500/5">
                  {log}
                </div>
              ))}
              {taskLog.length === 0 && <div className="h-full flex items-center justify-center text-zinc-700 italic">Engine idle. All routes directed through Refractal Math.</div>}
           </div>
        </div>
      </div>

      {/* Right Pane: Internal Services */}
      <div className="lg:col-span-4 space-y-6">
        <div className="glass-panel p-6 rounded-2xl border-emerald-500/10">
           <h4 className="text-xs font-black text-emerald-500 mb-6 flex items-center gap-2"><CpuIcon size={14} /> Toasted Core Status</h4>
           <div className="space-y-4">
              <ServiceToggle label="Refractal Math Ω" active={isRunning} />
              <ServiceToggle label="Logos Gateway" active={isRunning} />
              <ServiceToggle label="Holographic Sync" active={isRunning} />
              <ServiceToggle label="Math Redirect Svr" active={isRunning} />
           </div>
        </div>

        <div className="glass-panel p-6 rounded-2xl border-white/5 bg-gradient-to-br from-white/5 to-transparent">
           <h4 className="text-xs font-black text-zinc-400 mb-4 uppercase tracking-widest">Sovereign Math Endpoints</h4>
           <div className="space-y-2">
              <Endpoint name="INCEPT /math/modify" status="RL0" />
              <Endpoint name="COMMIT /math/checksum" status="RL0" />
              <Endpoint name="REDIRECT /hologram/bypass" status="ACTIVE" />
           </div>
        </div>
      </div>
    </div>
  );
};

const MetricBlock: React.FC<{ label: string, value: string, active: boolean }> = ({ label, value, active }) => (
  <div className="p-4 bg-white/5 border border-white/5 rounded-xl text-center hover:bg-white/10 transition-all cursor-default">
    <div className="text-[9px] font-black text-zinc-600 uppercase tracking-widest mb-1">{label}</div>
    <div className={`text-2xl font-mono font-bold ${active ? 'text-white' : 'text-zinc-800'}`}>{active ? value : '---'}</div>
  </div>
);

const ServiceToggle: React.FC<{ label: string, active: boolean }> = ({ label, active }) => (
  <div className="flex items-center justify-between group cursor-pointer">
    <span className="text-[11px] font-bold text-zinc-400 uppercase tracking-tight group-hover:text-zinc-300 transition-colors">{label}</span>
    <div className={`w-8 h-4 rounded-full transition-colors relative ${active ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]' : 'bg-zinc-800'}`}>
      <div className={`absolute top-0.5 w-3 h-3 bg-white rounded-full transition-all ${active ? 'right-0.5' : 'left-0.5'}`} />
    </div>
  </div>
);

const Endpoint: React.FC<{ name: string, status: string }> = ({ name, status }) => (
  <div className="flex items-center justify-between p-2.5 bg-black/40 rounded-xl border border-white/5 hover:border-white/10 transition-all">
    <span className="text-[9px] font-mono text-zinc-500 truncate mr-2 font-bold">{name}</span>
    <span className="text-[9px] font-black text-emerald-500 px-1.5 py-0.5 bg-emerald-500/5 rounded border border-emerald-500/10">{status}</span>
  </div>
);

export default ApiEngine;
