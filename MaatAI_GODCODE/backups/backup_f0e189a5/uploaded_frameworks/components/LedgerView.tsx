
import React, { useState } from 'react';
import { Database, ShieldCheck, History, ExternalLink, Filter } from 'lucide-react';
import { LedgerEntry } from '../types';

const MOCK_LEDGER: LedgerEntry[] = [
  { id: 'tx_001', timestamp: 1705643580000, type: 'UPLOAD', manifest_id: 'MAAT_V5', hash: '8f72a1b3...', metadata: { filename: 'Sovereign_Keys.asc' }, provenance_verified: true },
  { id: 'tx_002', timestamp: 1705643620000, type: 'MATH', manifest_id: 'MAAT_V5', hash: 'e3b0c442...', metadata: { formula: 'Refractal_Boot' }, provenance_verified: true },
  { id: 'tx_003', timestamp: 1705643680000, type: 'CHAT', manifest_id: 'MAAT_V5', hash: '4a1e9c2d...', metadata: { response_id: 'SENTINEL_001' }, provenance_verified: true },
  { id: 'tx_004', timestamp: 1705643750000, type: 'AUDIT', manifest_id: 'MAAT_V5', hash: '9b1c2d3e...', metadata: { scan_result: 'FASCISM_SCAN_CLEAN' }, provenance_verified: true },
];

const LedgerView: React.FC = () => {
  const [entries] = useState<LedgerEntry[]>(MOCK_LEDGER);

  return (
    <div className="h-full flex flex-col space-y-6">
      <div className="flex items-center justify-between p-6 glass rounded-xl border border-slate-800">
        <div className="flex items-center space-x-4">
          <div className="p-3 bg-emerald-500/10 rounded-lg border border-emerald-500/30">
            <Database className="w-6 h-6 text-emerald-500" />
          </div>
          <div>
            <h2 className="text-lg font-bold tracking-tight text-slate-200">Sovereign Evidence Ledger</h2>
            <p className="text-xs text-slate-500 font-mono">Immutable block height: 84,212 | Chain ID: TOASTED_HYBRID</p>
          </div>
        </div>
        <div className="flex space-x-3">
          <button className="flex items-center space-x-2 px-3 py-1.5 glass border-slate-800 text-xs text-slate-400 hover:text-slate-200 rounded transition-colors">
            <Filter className="w-4 h-4" />
            <span>Filter</span>
          </button>
          <button className="flex items-center space-x-2 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-slate-950 text-xs font-bold rounded transition-colors">
            <ShieldCheck className="w-4 h-4" />
            <span>Audit All</span>
          </button>
        </div>
      </div>

      <div className="flex-1 glass rounded-xl border border-slate-800 overflow-hidden flex flex-col">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm font-mono border-collapse">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-900/50 text-[10px] text-slate-500 uppercase tracking-wider">
                <th className="px-6 py-4">Artifact Hash</th>
                <th className="px-6 py-4">Type</th>
                <th className="px-6 py-4">Timestamp</th>
                <th className="px-6 py-4">Manifest</th>
                <th className="px-6 py-4">Verification</th>
                <th className="px-6 py-4">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/50">
              {entries.map((entry) => (
                <tr key={entry.id} className="hover:bg-slate-900/30 transition-colors group">
                  <td className="px-6 py-4 text-emerald-500/80 group-hover:text-emerald-400 truncate max-w-[120px]">
                    {entry.hash}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`
                      px-2 py-0.5 rounded text-[10px] font-bold
                      ${entry.type === 'UPLOAD' ? 'bg-blue-900/40 text-blue-400 border border-blue-800' : ''}
                      ${entry.type === 'MATH' ? 'bg-yellow-900/40 text-yellow-400 border border-yellow-800' : ''}
                      ${entry.type === 'CHAT' ? 'bg-purple-900/40 text-purple-400 border border-purple-800' : ''}
                      ${entry.type === 'AUDIT' ? 'bg-emerald-900/40 text-emerald-400 border border-emerald-800' : ''}
                    `}>
                      {entry.type}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-400 text-xs">
                    {new Date(entry.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="px-6 py-4 text-slate-500 text-xs italic">
                    {entry.manifest_id}
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center space-x-1.5 text-emerald-500 text-xs">
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>TRUSTED</span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <button className="text-slate-600 hover:text-slate-300 transition-colors">
                      <ExternalLink className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="flex-1 flex flex-col items-center justify-center py-20 text-slate-600 bg-slate-950/20">
           <History className="w-12 h-12 mb-4 opacity-10" />
           <p className="text-xs uppercase tracking-[0.2em] font-bold opacity-30">End of committed history</p>
        </div>
      </div>
    </div>
  );
};

export default LedgerView;
