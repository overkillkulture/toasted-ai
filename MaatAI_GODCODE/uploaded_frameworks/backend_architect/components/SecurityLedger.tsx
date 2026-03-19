
import React, { useMemo } from 'react';
import { AuditLogEntry } from '../types';

interface SecurityLedgerProps {
  logs: AuditLogEntry[];
}

const SecurityLedger: React.FC<SecurityLedgerProps> = ({ logs }) => {
  const liveLogs = useMemo(() => logs.filter(l => l.source === 'WS_STREAM').slice(0, 5), [logs]);

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight mono">Immutable <span className="text-purple-500">Ledger</span></h2>
          <p className="text-slate-400 mt-1 uppercase text-[10px] tracking-widest mono">Audit-grade reality state synchronization</p>
        </div>
        <div className="flex space-x-6 items-center">
          <div className="flex flex-col text-right">
            <div className="text-[10px] text-slate-600 mono uppercase">Audit Stream</div>
            <div className="flex items-center space-x-2 text-green-500">
               <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-ping"></span>
               <span className="text-xs font-bold mono uppercase">Live_RL0_Socket</span>
            </div>
          </div>
          <div className="text-right border-l border-slate-800 pl-6">
            <div className="text-[10px] text-slate-500 mono uppercase">Checkpoints</div>
            <div className="text-xl font-bold text-purple-400 mono">{logs.length.toString().padStart(4, '0')}</div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <AuditSummaryCard label="Node Integrity" count="100%" color="bg-green-500" />
        <AuditSummaryCard label="Active Sockets" count="01" color="bg-blue-500" />
        <AuditSummaryCard label="Audit Coverage" count="FULL" color="bg-purple-500" />
        <AuditSummaryCard label="Entropy Filter" count="RL0" color="bg-red-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-slate-950/50 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
          <div className="p-4 bg-slate-900/60 border-b border-slate-800 flex justify-between items-center text-[10px] mono text-slate-500 uppercase font-bold tracking-widest">
            <span>Primary Audit Records</span>
            <span className="text-blue-500">Storage: Immutable</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead className="bg-slate-950/80">
                <tr className="border-b border-slate-800">
                  <th className="px-6 py-4 text-[10px] font-bold text-slate-600 uppercase mono">Timestamp</th>
                  <th className="px-6 py-4 text-[10px] font-bold text-slate-600 uppercase mono">Level</th>
                  <th className="px-6 py-4 text-[10px] font-bold text-slate-600 uppercase mono">Source</th>
                  <th className="px-6 py-4 text-[10px] font-bold text-slate-600 uppercase mono">Event Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/40">
                {logs.slice(0, 15).map((log, i) => (
                  <tr key={i} className="hover:bg-blue-500/5 transition-colors group">
                    <td className="px-6 py-3 text-[10px] text-slate-500 mono">{log.timestamp}</td>
                    <td className="px-6 py-3">
                      <span className={`px-2 py-0.5 rounded text-[8px] font-bold mono border ${
                        log.level === 'OMEGA' ? 'bg-purple-900/30 text-purple-400 border-purple-500/30' :
                        log.level === 'CRITICAL' ? 'bg-red-900/30 text-red-400 border-red-500/30' :
                        log.level === 'WARNING' ? 'bg-yellow-900/30 text-yellow-400 border-yellow-500/30' : 
                        'bg-blue-900/30 text-blue-400 border-blue-500/30'
                      }`}>
                        {log.level}
                      </span>
                    </td>
                    <td className="px-6 py-3 text-[10px] text-slate-400 mono">{log.source}</td>
                    <td className="px-6 py-3 text-xs text-slate-200 group-hover:text-white transition-colors">{log.message}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="bg-slate-900/40 border border-slate-800 rounded-2xl flex flex-col overflow-hidden">
          <div className="p-4 bg-slate-950/80 border-b border-slate-800 flex justify-between items-center text-[10px] mono text-blue-400 uppercase font-bold tracking-widest">
            <span>Live Socket Feed</span>
            <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          </div>
          <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-black/20">
            {liveLogs.map((log, i) => (
              <div key={i} className="space-y-1 animate-in slide-in-from-right-2">
                <div className="flex justify-between items-center text-[9px] mono text-slate-600">
                  <span>{log.timestamp}</span>
                  <span className="text-blue-900">RL0_STREAM</span>
                </div>
                <div className="text-[10px] text-slate-300 mono leading-relaxed border-l-2 border-blue-900 pl-3">
                  {log.message}
                </div>
              </div>
            ))}
            {liveLogs.length === 0 && (
              <div className="h-full flex flex-col items-center justify-center space-y-3 opacity-30">
                <div className="w-8 h-8 border-2 border-blue-900 border-t-blue-500 rounded-full animate-spin"></div>
                <span className="text-[10px] mono text-slate-600">Awaiting stream packets...</span>
              </div>
            )}
          </div>
          <div className="p-4 bg-slate-950/80 border-t border-slate-800">
            <div className="text-[9px] text-slate-600 mono uppercase tracking-widest mb-2">Protocol: RealTime_Omega_v2</div>
            <div className="w-full h-1 bg-slate-900 rounded-full overflow-hidden">
               <div className="h-full bg-blue-900 w-2/3 animate-pulse"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const AuditSummaryCard: React.FC<{ label: string; count: string; color: string }> = ({ label, count, color }) => (
  <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl shadow-lg hover:border-purple-500/20 transition-all group">
    <div className="text-[9px] text-slate-600 uppercase mono mb-2 tracking-widest">{label}</div>
    <div className="flex items-end justify-between">
      <div className="text-xl font-bold text-white mono tracking-tighter group-hover:text-purple-400 transition-colors">{count}</div>
      <div className={`w-6 h-0.5 rounded ${color} opacity-40`}></div>
    </div>
  </div>
);

export default SecurityLedger;
