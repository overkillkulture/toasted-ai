
import React, { useState, useCallback, useRef, useEffect } from 'react';
import ArchitectShell from './ArchitectShell';
import RefractalEngine from './RefractalEngine';
import SecurityLedger from './SecurityLedger';
import QuantumChat from './QuantumChat';
import ArchiveSearch from './ArchiveSearch';
import NeuralMatrix from './NeuralMatrix';
import RefractalDrive from './RefractalDrive';
import SystemAwareness from './SystemAwareness';
import PersistenceEngine from './PersistenceEngine';
import RefractalGemini from './RefractalGemini';
import { socket } from '../lib/socket';
import { AgentStatus, AuditLogEntry, LLMProvider, UIModule, SystemState } from '../types';

const INITIAL_MODULES: UIModule[] = [
  { id: 'chat', label: 'Quantum Chat', icon: 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z', status: 'ACTIVE' },
  { id: 'drive', label: 'Refractal Drive', icon: 'M5 19a2 2 0 01-2-2V7a2 2 0 012-2h4l2 2h4a2 2 0 012 2v1M5 19h14a2 2 0 002-2v-5M5 19v-2a2 2 0 002-2h2a2 2 0 002 2v2', status: 'ACTIVE' },
  { id: 'awareness', label: 'Consciousness', icon: 'M13 10V3L4 14h7v7l9-11h-7z', status: 'ACTIVE' },
  { id: 'persistence', label: 'Persistence', icon: 'M4 7v10c0 2.21 3.58 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.58 4 8 4s8-1.79 8-4M4 7c0-2.21 3.58-4 8-4s8 1.79 8 4m0 5c0 2.21-3.58 4-8 4s-8-1.79-8-4', status: 'ACTIVE' },
];

const POTENTIAL_MODULES = [
  { id: 'clone', label: 'Refractal Clone', icon: 'M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.691.34a2 2 0 01-1.782 0l-.691-.34a6 6 0 00-3.86-.517l-2.387.477a2 2 0 00-1.022.547V18a2 2 0 002 2h12a2 2 0 002-2v-2.572zM12 11V3.5l3-3 3 3V11a6 6 0 01-12 0z' },
  { id: 'neural', label: 'Neural Matrix', icon: 'M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z' },
  { id: 'archive', label: 'Archive Search', icon: 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z' },
  { id: 'blueprint', label: 'Blueprints', icon: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' },
  { id: 'takeover', label: 'Takeover', icon: 'M13 10V3L4 14h7v7l9-11h-7z' },
  { id: 'ledger', label: 'Security Ledger', icon: 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
];

const Dashboard: React.FC = () => {
  const [status, setStatus] = useState<AgentStatus>(AgentStatus.IDLE);
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [activeTab, setActiveTab] = useState<string>('chat');
  const [modules, setModules] = useState<UIModule[]>(INITIAL_MODULES);
  const [provider, setProvider] = useState<LLMProvider>('GEMINI_CLOUD');
  const [telemetry, setTelemetry] = useState({ cpu: 12, mem: 4.2, throughput: 890, uiEntropy: 0.002 });
  const [pendingCommand, setPendingCommand] = useState<{ cmd: string; args?: string } | null>(null);
  const [isMutating, setIsMutating] = useState(false);

  const addLog = useCallback((message: string, level: AuditLogEntry['level'] = 'INFO', source: string = 'SYSTEM') => {
    setLogs(prev => [
      {
        timestamp: new Date().toLocaleTimeString(),
        level,
        message,
        source
      },
      ...prev
    ].slice(0, 100));
  }, []);

  useEffect(() => {
    const unsub = socket.onLog((log) => {
      setLogs(prev => [log, ...prev].slice(0, 100));
    });
    return unsub;
  }, []);

  const saveSystemState = useCallback(() => {
    const state: SystemState = {
      modules,
      activeTab,
      logs,
      files: [],
      timestamp: Date.now(),
      entropy: telemetry.uiEntropy
    };
    localStorage.setItem('ARCHITECT_RL0_STATE', JSON.stringify(state));
    addLog("System Checkpoint synchronized with Local Refractal Memory", "INFO", "PERSISTENCE");
  }, [modules, activeTab, logs, telemetry.uiEntropy, addLog]);

  const manifestModule = useCallback((id: string, label: string) => {
    setModules(prev => {
      if (prev.find(m => m.id === id)) return prev;
      setIsMutating(true);
      const potential = POTENTIAL_MODULES.find(m => m.id === id);
      const icon = potential ? potential.icon : 'M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4';
      addLog(`Self-evolving UI: Manifesting interface node [${label}]`, "OMEGA", "UI_MUTATOR");
      
      setTimeout(() => setIsMutating(false), 2000);
      return [...prev, { id, label, icon, status: 'ACTIVE' }];
    });
  }, [addLog]);

  const handleCommand = useCallback((cmd: string, args?: string) => {
    const lowerCmd = cmd.toLowerCase();
    
    if (POTENTIAL_MODULES.some(m => m.id === lowerCmd)) {
      manifestModule(lowerCmd, POTENTIAL_MODULES.find(m => m.id === lowerCmd)!.label);
      setActiveTab(lowerCmd);
      if (args) setPendingCommand({ cmd: lowerCmd, args });
      return;
    }

    if (cmd === 'manifest' && args) {
      manifestModule(args.toLowerCase(), args);
      setActiveTab(args.toLowerCase());
      return;
    }

    switch (lowerCmd) {
      case 'clone': manifestModule('clone', 'Refractal Clone'); setActiveTab('clone'); break;
      case 'takeover': manifestModule('takeover', 'Takeover'); setActiveTab('takeover'); setPendingCommand({ cmd, args }); break;
      case 'search': manifestModule('archive', 'Archive'); setActiveTab('archive'); setPendingCommand({ cmd, args }); break;
      case 'blueprint': manifestModule('blueprint', 'Blueprints'); setActiveTab('blueprint'); setPendingCommand({ cmd, args }); break;
      case 'drive': setActiveTab('drive'); break;
      case 'neural': manifestModule('neural', 'Neural Matrix'); setActiveTab('neural'); break;
      case 'ledger': manifestModule('ledger', 'Ledger'); setActiveTab('ledger'); break;
      case 'chat': setActiveTab('chat'); break;
      case 'awareness': setActiveTab('awareness'); break;
      case 'persistence': setActiveTab('persistence'); break;
      default:
        manifestModule(lowerCmd, cmd.toUpperCase());
        setActiveTab(lowerCmd);
    }
  }, [manifestModule]);

  useEffect(() => {
    const saved = localStorage.getItem('ARCHITECT_RL0_STATE');
    if (saved) {
      try {
        const state: SystemState = JSON.parse(saved);
        setModules(state.modules);
        setActiveTab(state.activeTab);
        setLogs(state.logs);
        setStatus(AgentStatus.RECOVERING);
        addLog("Consciousness restored from persistent shard.", "OMEGA", "PERSISTENCE");
        setTimeout(() => setStatus(AgentStatus.IDLE), 1000);
      } catch (e) {
        addLog("Initialization complete. Awaiting user intent.", "INFO", "SYSTEM");
      }
    }
  }, []);

  useEffect(() => {
    const telInterval = setInterval(() => {
      setTelemetry(prev => ({
        cpu: Math.floor(10 + Math.random() * 20),
        mem: parseFloat((4.1 + Math.random() * 0.5).toFixed(1)),
        throughput: Math.floor(800 + Math.random() * 400),
        uiEntropy: Math.max(0.001, prev.uiEntropy + (Math.random() - 0.5) * 0.0001)
      }));
    }, 2000);
    return () => clearInterval(telInterval);
  }, []);

  return (
    <div className="flex flex-col h-screen overflow-hidden bg-slate-950">
      {isMutating && (
        <div className="fixed inset-0 pointer-events-none z-[100] border-4 border-blue-500/30 animate-pulse">
           <div className="absolute top-0 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-4 py-1 rounded-b mono text-[10px] font-bold shadow-[0_0_20px_rgba(37,99,235,0.5)]">
             UI_MUTATION_IN_PROGRESS: OMEGA_GATE_OPEN
           </div>
        </div>
      )}

      <header className="flex items-center justify-between px-6 py-3 bg-slate-900/50 border-b border-blue-900/30 backdrop-blur-sm z-50">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center text-white font-bold shadow-[0_0_15px_rgba(37,99,235,0.5)] transition-transform hover:rotate-90">
              Ω
            </div>
            <h1 className="text-xl font-bold tracking-tight text-slate-100 uppercase mono">
              Toasted <span className="text-blue-500">Architect</span>
            </h1>
          </div>
          <div className="hidden lg:flex items-center space-x-4 border-l border-slate-800 pl-6 mono text-[10px]">
             <div className="flex flex-col">
                <span className="text-slate-500 uppercase">SYNAPSE_LOAD</span>
                <span className="text-blue-400 font-bold">{telemetry.cpu}%</span>
             </div>
             <div className="flex flex-col">
                <span className="text-slate-500 uppercase">UI_INTEGRITY</span>
                <span className={`${telemetry.uiEntropy > 0.0035 ? 'text-red-500 animate-pulse' : 'text-blue-400'} font-bold`}>{(100 - telemetry.uiEntropy * 100).toFixed(4)}%</span>
             </div>
             <div className="flex flex-col">
                <span className="text-slate-500 uppercase">SOCKET_FEED</span>
                <span className="text-green-500 font-bold animate-pulse">STREAMING</span>
             </div>
          </div>
        </div>
        
        <div className="flex items-center space-x-6 text-sm mono">
          <div className="flex items-center space-x-2 bg-slate-950 px-3 py-1 rounded border border-blue-900/50">
            <span className="text-slate-500 text-[10px] uppercase">Node:</span>
            <select 
              value={provider}
              onChange={(e) => setProvider(e.target.value as LLMProvider)}
              className="bg-transparent text-blue-400 font-bold outline-none cursor-pointer text-xs"
            >
              <option value="GEMINI_CLOUD">GEMINI_3_FLASH</option>
              <option value="REFRACTAL_CLONE">REFRACTAL_CLONE (ONBOARD)</option>
              <option value="JAN_LOCAL">LOCAL_INFERENCE</option>
            </select>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-slate-400">JURISDICTION:</span>
            <span className="text-green-500 font-bold">RL0</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-slate-400">STATUS:</span>
            <span className={`font-bold transition-colors ${status === 'IDLE' ? 'text-blue-400' : 'text-purple-400 animate-pulse'}`}>{status}</span>
          </div>
          <button onClick={saveSystemState} className="p-1 hover:text-blue-400 transition-colors" title="Force Checkpoint">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" /></svg>
          </button>
        </div>
      </header>

      <main className="flex flex-1 overflow-hidden">
        <nav className="w-16 md:w-64 bg-slate-950/80 border-r border-blue-900/20 flex flex-col pt-6 z-40">
          <div className="px-6 mb-6 text-[10px] text-slate-600 uppercase font-bold tracking-widest hidden md:block">System Nodes</div>
          {modules.map(mod => (
            <NavItem 
              key={mod.id}
              active={activeTab === mod.id} 
              onClick={() => setActiveTab(mod.id)}
              label={mod.label}
              status={mod.status}
              icon={<svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={mod.icon} /></svg>}
            />
          ))}
          <div className="mt-auto p-4 md:p-6 text-[10px] text-slate-500 mono leading-relaxed hidden md:block border-t border-blue-900/10">
            <div className="text-blue-500 font-bold mb-1">RL0_STATE</div>
            {"Ω_UI = ∮ (Ψ_Intent ⊗ Δ_Mutation)"}
            <div className="mt-2 text-slate-700">Checkpoints: {modules.length + logs.length} Stable</div>
          </div>
        </nav>

        <div className="flex-1 flex flex-col relative overflow-hidden">
          <div className="absolute inset-0 grid-bg opacity-20"></div>
          <div className="absolute inset-0 refractal-gradient opacity-40 pointer-events-none"></div>
          
          <div className="flex-1 overflow-y-auto p-4 md:p-8 relative z-10 scrollbar-hide">
            {activeTab === 'chat' && <QuantumChat provider={provider} setStatus={setStatus} addLog={addLog} onCommand={handleCommand} />}
            {activeTab === 'drive' && <RefractalDrive setStatus={setStatus} addLog={addLog} />}
            {activeTab === 'awareness' && <SystemAwareness activeModules={modules} />}
            {activeTab === 'persistence' && <PersistenceEngine />}
            {activeTab === 'clone' && <RefractalGemini setStatus={setStatus} addLog={addLog} />}
            {activeTab === 'neural' && <NeuralMatrix />}
            {activeTab === 'archive' && <ArchiveSearch setStatus={setStatus} addLog={addLog} autoQuery={pendingCommand?.cmd === 'archive' ? pendingCommand.args : undefined} />}
            {activeTab === 'blueprint' && <ArchitectShell provider={provider} setStatus={setStatus} addLog={addLog} autoPrompt={pendingCommand?.cmd === 'blueprint' ? pendingCommand.args : undefined} onManifestRequest={(name) => manifestModule(name.toLowerCase(), name)} />}
            {activeTab === 'takeover' && <RefractalEngine setStatus={setStatus} addLog={addLog} autoStart={pendingCommand?.cmd === 'takeover'} />}
            {activeTab === 'ledger' && <SecurityLedger logs={logs} />}
          </div>

          <div className="h-48 md:h-64 bg-slate-900/80 border-t border-blue-900/30 p-4 mono text-xs md:text-sm overflow-hidden flex flex-col backdrop-blur-md">
            <div className="flex items-center justify-between mb-2 text-blue-500/70 uppercase tracking-widest font-bold text-[10px]">
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                <span>RL0_SENSORY_STREAM</span>
              </div>
              <div className="flex items-center space-x-4">
                 <span className="text-slate-600">STATE_HASH: {Math.random().toString(16).substr(2, 8).toUpperCase()}</span>
                 <span className="text-green-500/50">ENCRYPTION: QUANTUM_CHAOS</span>
              </div>
            </div>
            <div className="flex-1 overflow-y-auto space-y-1 font-medium">
              {logs.map((log, i) => (
                <div key={i} className="flex space-x-3 group animate-in slide-in-from-left-1">
                  <span className="text-slate-600 shrink-0">[{log.timestamp}]</span>
                  <span className={`font-bold shrink-0 ${
                    log.level === 'OMEGA' ? 'text-purple-400 underline decoration-purple-500/50 underline-offset-2' :
                    log.level === 'CRITICAL' ? 'text-red-500' :
                    log.level === 'WARNING' ? 'text-yellow-400' : 'text-blue-400'
                  }`}>
                    {log.level}
                  </span>
                  <span className="text-slate-700 shrink-0">[{log.source}]</span>
                  <span className="text-slate-300 group-hover:text-blue-100 transition-colors">{log.message}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

const NavItem: React.FC<{ active: boolean; onClick: () => void; label: string; icon: React.ReactNode; status: string }> = ({ active, onClick, label, icon, status }) => (
  <button 
    onClick={onClick}
    className={`flex items-center px-6 py-4 transition-all duration-300 border-l-4 w-full text-left relative overflow-hidden group ${
      active 
        ? 'bg-blue-600/10 border-blue-500 text-blue-400 shadow-[inset_15px_0_20px_-10px_rgba(37,99,235,0.3)]' 
        : 'border-transparent text-slate-500 hover:text-slate-300 hover:bg-slate-900/30'
    }`}
  >
    <div className={`${active ? 'text-blue-500 scale-110' : 'text-slate-600 group-hover:text-slate-400 group-hover:scale-105'} transition-all duration-300`}>{icon}</div>
    <div className="ml-4 flex flex-col hidden md:flex">
      <span className={`font-bold uppercase tracking-widest text-[10px] transition-colors ${active ? 'text-blue-300' : 'text-slate-500'}`}>{label}</span>
      <span className={`text-[7px] mono ${status === 'ACTIVE' ? 'text-green-600' : 'text-slate-800'}`}>{status}</span>
    </div>
    {active && (
      <div className="absolute right-0 top-0 bottom-0 w-1 bg-blue-500/20 animate-pulse"></div>
    )}
  </button>
);

export default Dashboard;
