
import React from 'react';
import { QueueTask } from '../types';
import { RefreshCw, ShieldAlert, Cpu } from 'lucide-react';

interface QueueMonitorProps {
  tasks: QueueTask[];
}

const QueueMonitor: React.FC<QueueMonitorProps> = ({ tasks }) => {
  // Mock active tasks if empty for visual appeal
  const activeTasks = tasks.length > 0 ? tasks : [
    { id: 't1', type: 'LEARN', status: 'PROCESSING', payload: 'Screenshot ingestion protocol', timestamp: Date.now() },
    { id: 't2', type: 'SEC', status: 'PENDING', payload: 'Adversarial audit on ledger', timestamp: Date.now() - 5000 },
    { id: 't3', type: 'CODE', status: 'COMPLETED', payload: 'MaatEngine v2 compiler fix', timestamp: Date.now() - 10000 },
  ];

  return (
    <div className="glass-panel p-6 rounded-2xl">
      <h3 className="text-sm uppercase font-bold text-zinc-400 tracking-widest mb-6 flex items-center justify-between">
        <span className="flex items-center gap-2 underline decoration-amber-500 decoration-2 underline-offset-4">Σ Cyclic Queues</span>
        <span className="text-[10px] font-normal opacity-50">v4.2.1-stable</span>
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <QueueSection title="Q_Learn" icon={<RefreshCw size={14} />} color="text-amber-400" tasks={activeTasks.filter(t => t.type === 'LEARN')} />
        <QueueSection title="Q_Sec" icon={<ShieldAlert size={14} />} color="text-red-400" tasks={activeTasks.filter(t => t.type === 'SEC')} />
        <QueueSection title="Q_Code" icon={<Cpu size={14} />} color="text-blue-400" tasks={activeTasks.filter(t => t.type === 'CODE')} />
      </div>
    </div>
  );
};

const QueueSection: React.FC<{ title: string; icon: React.ReactNode; color: string; tasks: any[] }> = ({ title, icon, color, tasks }) => (
  <div className="space-y-3 p-4 bg-white/5 rounded-xl border border-white/5 flex flex-col min-h-[160px]">
    <div className={`flex items-center gap-2 text-xs font-bold uppercase tracking-tight ${color}`}>
      {icon} {title}
    </div>
    <div className="flex-1 space-y-2">
      {tasks.map(task => (
        <div key={task.id} className="p-2 bg-black/40 rounded border border-white/5 flex flex-col gap-1">
          <div className="flex items-center justify-between text-[10px]">
            <span className="text-zinc-500 mono truncate max-w-[120px]">{task.payload}</span>
            <span className={`${task.status === 'PROCESSING' ? 'text-amber-500 animate-pulse' : 'text-zinc-600'}`}>
              {task.status}
            </span>
          </div>
          <div className="w-full bg-white/5 h-0.5 rounded-full overflow-hidden">
            <div 
              className={`h-full ${task.status === 'PROCESSING' ? 'bg-amber-500' : 'bg-zinc-700'}`} 
              style={{ width: task.status === 'COMPLETED' ? '100%' : task.status === 'PROCESSING' ? '60%' : '10%' }} 
            />
          </div>
        </div>
      ))}
      {tasks.length === 0 && (
        <div className="h-full flex items-center justify-center italic text-zinc-600 text-xs">
          Idle
        </div>
      )}
    </div>
  </div>
);

export default QueueMonitor;
