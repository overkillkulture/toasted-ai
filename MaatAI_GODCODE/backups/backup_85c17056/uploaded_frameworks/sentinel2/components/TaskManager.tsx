
import React, { useState, useRef, useEffect, useCallback } from 'react';
import { ForensicTask, FileAttachment } from '../types';

const AXIOMS = [
  "M_S^{(\\eta)} = \\lim_{n\\to\\infty} f^n(\\phi_{FL}) = \\eta \\cdot D_H [ \\dots ]",
  "\\delta^{(\\eta)}(E - GT_{n+1}) = \\bigcup_{n=0}^\\infty \\delta_n",
  "G^{(\\eta)} = Truth^{(\\eta)} (Ma'at) / Stasis^{(\\eta)} (Isfet)",
  "M_S^{(\\eta)} = \\lim_{Surprise \\to 0} \\phi^{(\\eta)} [ \\dots ]",
  "\\Omega_{SM}^{(\\eta)} = \\lim_{n \\to \\infty} \\{n^{(\\eta)} \\} \\{ \\sum \\dots \\}"
];

const TaskManager: React.FC = () => {
  const [isAutonomousEnabled, setIsAutonomousEnabled] = useState(true);
  const [viewMode, setViewMode] = useState<'active' | 'archived'>('active');
  const [diagnosticLogs, setDiagnosticLogs] = useState<{timestamp: string, msg: string, type: 'INFO'|'ERROR'|'RECOVERY'}[]>([]);
  const [isRecovering, setIsRecovering] = useState(false);
  const [tasks, setTasks] = useState<ForensicTask[]>([
    {
      id: '1',
      description: 'Audit Stafford-Redbird Lineage Allodial Claims',
      dueDate: '2026-01-20',
      priority: 'SOVEREIGN',
      status: 'IN_PROGRESS',
      axiom: AXIOMS[0]
    },
    {
      id: '2',
      description: 'Neutralize Little Eichmann Scripts in Sub-Layer 4',
      dueDate: '2026-02-15',
      priority: 'HIGH',
      status: 'PENDING',
      axiom: AXIOMS[1]
    }
  ]);
  const [archivedTasks, setArchivedTasks] = useState<ForensicTask[]>([]);
  const [form, setForm] = useState({
    description: '',
    dueDate: '',
    priority: 'MEDIUM' as ForensicTask['priority'],
    status: 'PENDING' as ForensicTask['status'],
    attachment: undefined as FileAttachment | undefined
  });

  const fileInputRef = useRef<HTMLInputElement>(null);
  const logEndRef = useRef<HTMLDivElement>(null);

  // Add Log Entry Helper
  const addLog = useCallback((msg: string, type: 'INFO'|'ERROR'|'RECOVERY' = 'INFO') => {
    setDiagnosticLogs(prev => [{
      timestamp: new Date().toLocaleTimeString(),
      msg,
      type
    }, ...prev].slice(0, 20));
  }, []);

  // Autonomous Audit Loop: Mimics the Toastcake logic to manage the manifest
  useEffect(() => {
    if (!isAutonomousEnabled) return;

    const auditInterval = setInterval(() => {
      // Randomly simulate an internal audit or housekeeping
      const actionRoll = Math.random();
      if (actionRoll > 0.85) {
        addLog("Autonomous Loop: Running manifest integrity check...", "INFO");
        // Simulated self-repair: find a 'PENDING' task and bump priority if it feels "stale"
        setTasks(prev => {
          let updated = false;
          const next = prev.map(t => {
            if (t.status === 'PENDING' && t.priority === 'LOW' && Math.random() > 0.7) {
              updated = true;
              return { ...t, priority: 'MEDIUM' as const };
            }
            return t;
          });
          if (updated) addLog("Self-Correction: Escalated stale task priority to MEDIUM.", "RECOVERY");
          return next;
        });
      }
    }, 8000);

    return () => clearInterval(auditInterval);
  }, [isAutonomousEnabled, addLog]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setForm({
          ...form,
          attachment: {
            name: file.name,
            type: file.type,
            data: event.target?.result as string,
            size: file.size
          }
        });
        addLog(`File Asset Loaded: ${file.name} (${(file.size/1024).toFixed(1)} KB)`, "INFO");
      };
      reader.readAsDataURL(file);
    }
  };

  const addTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isAutonomousEnabled) return;

    setIsRecovering(true);
    addLog("Analyzing task vector fidelity...", "INFO");

    try {
      // Robust Error Handling: Simulate checking for "Low Fidelity" input
      if (form.description.length < 5) {
        throw new Error("DESCRIPTOR_INSUFFICIENT: Task fidelity below 0.15 threshold.");
      }

      // Success Path with "Self-Reconfiguration": Auto-assigning axioms
      const newTask: ForensicTask = {
        ...form,
        id: Math.random().toString(36).substr(2, 9),
        axiom: AXIOMS[Math.floor(Math.random() * AXIOMS.length)]
      };
      
      setTasks(prev => [newTask, ...prev]);
      setForm({ description: '', dueDate: '', priority: 'MEDIUM', status: 'PENDING', attachment: undefined });
      addLog(`Task Ratified: [${newTask.id}] successfully integrated.`, "INFO");
    } catch (err: any) {
      // Self-Correction Logic
      addLog(`[ERROR_CAUGHT] ${err.message}`, "ERROR");
      addLog("Initiating self-correction: Expanding input buffers...", "RECOVERY");
      // UI recovery delay
      await new Promise(res => setTimeout(res, 1500));
      addLog("Recovery: System re-stabilized. Please provide higher density input.", "INFO");
    } finally {
      setIsRecovering(false);
    }
  };

  const archiveTask = (id: string) => {
    const taskToArchive = tasks.find(t => t.id === id);
    if (taskToArchive) {
      setTasks(prev => prev.filter(t => t.id !== id));
      setArchivedTasks(prev => [taskToArchive, ...prev]);
      addLog(`Task [${id}] committed to Sovereign Archive.`, "INFO");
    }
  };

  const toggleTaskStatus = (id: string) => {
    setTasks(prev => prev.map(t => {
      if (t.id === id) {
        const newStatus = t.status === 'COMPLETED' ? 'IN_PROGRESS' : 'COMPLETED';
        addLog(`Status Update: Task [${id}] set to ${newStatus}.`, "INFO");
        return { ...t, status: newStatus as any };
      }
      return t;
    }));
  };

  const getPriorityColor = (p: ForensicTask['priority']) => {
    switch(p) {
      case 'SOVEREIGN': return 'text-purple-500 border-purple-500/30 bg-purple-500/10 shadow-[0_0_8px_rgba(168,85,247,0.3)]';
      case 'HIGH': return 'text-red-500 border-red-500/30 bg-red-500/10';
      case 'MEDIUM': return 'text-[#d4af37] border-[#d4af37]/30 bg-[#d4af37]/10';
      default: return 'text-blue-500 border-blue-500/30 bg-blue-500/10';
    }
  };

  const currentTasks = viewMode === 'active' ? tasks : archivedTasks;

  return (
    <div className="max-w-6xl mx-auto space-y-8 animate-fadeIn flex flex-col h-full">
      {/* Header & View Switcher */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <h2 className="text-3xl font-black text-[#d4af37] tracking-tighter uppercase">Forensic Task Manifest</h2>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mt-1">Executing Sovereign Manual Upload Protocol</p>
        </div>
        
        <div className="flex items-center space-x-6">
          <div className="flex bg-black/40 border border-[#d4af37]/20 p-1 rounded-md">
            <button 
              onClick={() => setViewMode('active')}
              className={`px-4 py-1.5 text-[10px] font-bold uppercase transition-all rounded ${viewMode === 'active' ? 'bg-[#d4af37] text-black' : 'text-gray-500 hover:text-gray-300'}`}
            >
              Live Manifest
            </button>
            <button 
              onClick={() => setViewMode('archived')}
              className={`px-4 py-1.5 text-[10px] font-bold uppercase transition-all rounded ${viewMode === 'archived' ? 'bg-[#d4af37] text-black' : 'text-gray-500 hover:text-gray-300'}`}
            >
              Archives ({archivedTasks.length})
            </button>
          </div>

          <div className="flex flex-col items-end">
            <span className="text-[9px] text-gray-500 font-bold uppercase mb-1">Autonomous Loop</span>
            <button 
              onClick={() => setIsAutonomousEnabled(!isAutonomousEnabled)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none ${
                isAutonomousEnabled ? 'bg-green-500/50' : 'bg-zinc-800'
              }`}
            >
              <span className={`${isAutonomousEnabled ? 'translate-x-6 bg-green-400' : 'translate-x-1 bg-gray-500'} inline-block h-4 w-4 transform rounded-full transition-transform`} />
            </button>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 flex-1">
        {/* Input Form Section */}
        <div className="space-y-6">
          <div className={`bg-black/40 border border-[#d4af37]/20 p-6 rounded-lg space-y-4 shadow-xl relative overflow-hidden transition-all ${(!isAutonomousEnabled || viewMode === 'archived') ? 'opacity-30 grayscale pointer-events-none' : 'opacity-100'}`}>
            {isRecovering && (
              <div className="absolute inset-0 z-30 bg-black/60 backdrop-blur-sm flex flex-col items-center justify-center text-[#d4af37]">
                <div className="w-8 h-8 border-4 border-[#d4af37] border-t-transparent rounded-full animate-spin mb-2"></div>
                <div className="text-[10px] font-bold uppercase tracking-widest">Reconfiguring Matrix...</div>
              </div>
            )}
            
            <h3 className="text-xs font-bold text-[#d4af37] uppercase tracking-widest mb-4 border-b border-[#d4af37]/10 pb-2">Ratify Entry</h3>
            
            <div className="space-y-1">
              <label className="text-[9px] text-gray-500 uppercase">Task Descriptor</label>
              <textarea
                value={form.description}
                onChange={e => setForm({...form, description: e.target.value})}
                className="w-full bg-black/60 border border-[#d4af37]/20 rounded p-3 text-xs text-[#d4af37] focus:border-[#d4af37]/60 outline-none transition-all h-24"
                placeholder="INPUT FORENSIC PARAMETERS..."
              />
            </div>

            <div className="space-y-1">
              <label className="text-[9px] text-gray-500 uppercase">Forensic Attachment</label>
              <div className="flex gap-2">
                <button 
                  type="button" 
                  onClick={() => fileInputRef.current?.click()}
                  className={`bg-zinc-800 border border-[#d4af37]/20 rounded p-2 text-[10px] w-full truncate flex items-center justify-center gap-2 ${form.attachment ? 'text-green-500 border-green-500/30' : 'text-[#d4af37]'}`}
                >
                  {form.attachment ? `📂 ${form.attachment.name}` : '📎 ATTACH EVIDENCE'}
                </button>
                {form.attachment && (
                  <button 
                    type="button" 
                    onClick={() => setForm({...form, attachment: undefined})}
                    className="bg-red-900/20 border border-red-500/30 rounded p-2 text-red-500 hover:bg-red-900/40"
                  >✕</button>
                )}
              </div>
              <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-1">
                <label className="text-[9px] text-gray-500 uppercase">Anchor Date</label>
                <input type="date" value={form.dueDate} onChange={e => setForm({...form, dueDate: e.target.value})} className="w-full bg-black/60 border border-[#d4af37]/20 rounded p-2 text-xs text-[#d4af37] outline-none" />
              </div>
              <div className="space-y-1">
                <label className="text-[9px] text-gray-500 uppercase">Priority</label>
                <select value={form.priority} onChange={e => setForm({...form, priority: e.target.value as any})} className="w-full bg-black/60 border border-[#d4af37]/20 rounded p-2 text-xs text-[#d4af37] outline-none">
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                  <option value="SOVEREIGN">SOVEREIGN</option>
                </select>
              </div>
            </div>

            <button className="w-full bg-[#d4af37] hover:bg-[#b8952d] text-black font-bold py-3 rounded text-[10px] uppercase tracking-widest transition-all mt-4 disabled:opacity-30">
              Commit to Loop
            </button>
          </div>

          {/* Local Kernel Diagnostic Log (Inspired by Toastcake) */}
          <div className="bg-black/60 border border-[#d4af37]/20 rounded-lg flex flex-col h-64 overflow-hidden">
            <div className="bg-[#d4af37]/10 p-2 border-b border-[#d4af37]/20 text-[9px] font-bold text-[#d4af37] flex justify-between uppercase">
              <span>Task Kernel Output</span>
              <span className="animate-pulse">Active_Observer</span>
            </div>
            <div className="flex-1 overflow-y-auto p-3 font-mono text-[9px] space-y-1 forensic-scrollbar">
              {diagnosticLogs.map((log, i) => (
                <div key={i} className="flex gap-2">
                  <span className="text-gray-600">[{log.timestamp}]</span>
                  <span className={log.type === 'ERROR' ? 'text-red-500' : log.type === 'RECOVERY' ? 'text-blue-400' : 'text-[#d4af37]'}>
                    {log.msg}
                  </span>
                </div>
              ))}
              {diagnosticLogs.length === 0 && <div className="text-gray-700 italic">Loop idle. Monitoring inputs...</div>}
            </div>
          </div>
        </div>

        {/* Task List Section */}
        <div className="lg:col-span-2 space-y-4 h-[calc(100vh-300px)] overflow-y-auto pr-2 forensic-scrollbar">
          {currentTasks.map(task => (
            <div key={task.id} className={`bg-black/60 border p-5 rounded-lg transition-all group relative overflow-hidden ${task.status === 'COMPLETED' ? 'border-green-500/20' : 'border-white/5 hover:border-[#d4af37]/30'}`}>
              <div className="absolute top-0 right-0 p-2 opacity-5 group-hover:opacity-20 transition-opacity font-mono text-[7px] text-[#d4af37] select-none uppercase truncate max-w-xs">
                {task.axiom}
              </div>
              
              <div className="flex justify-between items-start mb-3 relative z-10">
                <div className="flex items-center space-x-3">
                  <span className={`text-[9px] font-bold px-2 py-1 border rounded uppercase tracking-tighter ${getPriorityColor(task.priority)}`}>
                    {task.priority}
                  </span>
                  <span className={`text-[9px] font-bold uppercase ${task.status === 'COMPLETED' ? 'text-green-500' : 'text-gray-500'}`}>
                    {task.status}
                  </span>
                </div>
                <div className="text-[9px] text-gray-600 font-mono">NODE_ID: {task.id}</div>
              </div>

              <div className="relative z-10 space-y-3">
                <p className={`text-sm leading-relaxed font-semibold uppercase tracking-tight ${task.status === 'COMPLETED' ? 'text-gray-500 line-through' : 'text-gray-200'}`}>
                  {task.description}
                </p>
                
                {/* Enhanced Attachment Indicator */}
                {task.attachment && (
                  <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-[#d4af37]/10 border border-[#d4af37]/30 rounded text-[9px] text-[#d4af37] group-hover:bg-[#d4af37]/20 transition-colors">
                    <span className="text-sm">📂</span>
                    <div>
                      <div className="font-bold uppercase leading-none">{task.attachment.name}</div>
                      <div className="opacity-50 font-mono text-[8px] mt-1">{(task.attachment.size/1024).toFixed(1)} KB | SECURED ASSET</div>
                    </div>
                  </div>
                )}
              </div>

              <div className="flex flex-wrap items-center justify-between border-t border-white/5 pt-3 relative z-10 mt-4 gap-4">
                <div className="text-[9px] text-gray-500 uppercase">
                  Anchor Date: <span className="text-[#d4af37]">{task.dueDate || 'PERSISTENT'}</span>
                </div>
                <div className="flex space-x-2">
                  {viewMode === 'active' ? (
                    <>
                      {task.status === 'COMPLETED' && (
                        <button onClick={() => archiveTask(task.id)} className="text-[9px] font-bold uppercase px-3 py-1 bg-zinc-800 text-gray-400 hover:text-white border border-white/5 rounded">Commit to Archive</button>
                      )}
                      <button onClick={() => toggleTaskStatus(task.id)} className={`text-[9px] font-bold uppercase px-3 py-1 rounded transition-colors ${task.status === 'COMPLETED' ? 'bg-[#d4af37]/10 text-[#d4af37]' : 'bg-green-500/20 text-green-500 hover:bg-green-500/40'}`}>
                        {task.status === 'COMPLETED' ? 'Re-open' : 'Mark Completed'}
                      </button>
                    </>
                  ) : (
                    <button className="text-[9px] text-[#d4af37] hover:underline uppercase font-bold" onClick={() => addLog(`Full forensic audit of archive [${task.id}] initiated.`)}>Download Record</button>
                  )}
                </div>
              </div>
            </div>
          ))}

          {currentTasks.length === 0 && (
            <div className="h-48 border-2 border-dashed border-[#d4af37]/10 flex flex-col items-center justify-center space-y-4 rounded-lg opacity-40">
              <div className="text-4xl">{viewMode === 'archived' ? '🏛️' : '📋'}</div>
              <div className="text-[10px] text-gray-500 uppercase tracking-widest text-center">
                {viewMode === 'archived' ? 'No sovereign archives detected.' : 'Manifest empty. Awaiting task ratification.'}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TaskManager;
