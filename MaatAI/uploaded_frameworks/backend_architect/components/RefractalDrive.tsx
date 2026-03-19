
import React, { useState, useRef, useMemo } from 'react';
import { StoredFile, AgentStatus } from '../types';

interface RefractalDriveProps {
  setStatus: (status: AgentStatus) => void;
  addLog: (msg: string, level?: any, src?: string) => void;
}

const RefractalDrive: React.FC<RefractalDriveProps> = ({ setStatus, addLog }) => {
  const [files, setFiles] = useState<StoredFile[]>([
    { 
      id: '1', 
      name: 'RL0_Foundational_Schema.pdf', 
      size: 15420000, 
      refractalWeight: 0.000012, 
      type: 'application/pdf', 
      timestamp: '2024-05-20 14:22',
      hash: '0x88...f21'
    },
    { 
      id: '2', 
      name: 'System_Mutation_Log.txt', 
      size: 450000, 
      refractalWeight: 0.000001, 
      type: 'text/plain', 
      timestamp: '2024-05-21 09:15',
      hash: '0xA4...b32'
    }
  ]);
  const [isUploading, setIsUploading] = useState(false);
  const [shardingProgress, setShardingProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (!selectedFiles || selectedFiles.length === 0) return;

    setIsUploading(true);
    setShardingProgress(0);
    setStatus(AgentStatus.SYNCING);
    addLog(`Initiating Refractal Sharding for ${selectedFiles.length} assets`, "INFO", "DRIVE");

    let currentFileIndex = 0;
    const totalFiles = selectedFiles.length;

    const processNextFile = () => {
      if (currentFileIndex >= totalFiles) {
        setIsUploading(false);
        setStatus(AgentStatus.IDLE);
        addLog(`Batch internalization of ${totalFiles} assets complete. Sovereignty validated.`, "OMEGA", "DRIVE");
        return;
      }

      const file = selectedFiles[currentFileIndex];
      addLog(`Sharding [${currentFileIndex + 1}/${totalFiles}]: ${file.name}`, "INFO", "DRIVE");

      let progress = 0;
      const shardInterval = setInterval(() => {
        progress += 10;
        setShardingProgress(Math.floor(((currentFileIndex / totalFiles) * 100) + (progress / totalFiles)));
        
        if (progress >= 100) {
          clearInterval(shardInterval);
          finalizeSingleUpload(file);
          currentFileIndex++;
          processNextFile();
        }
      }, 30);
    };

    processNextFile();
  };

  const finalizeSingleUpload = (file: File) => {
    const newFile: StoredFile = {
      id: Math.random().toString(36).substr(2, 9),
      name: file.name,
      size: file.size,
      refractalWeight: Math.random() * 0.0001,
      type: file.type,
      timestamp: new Date().toLocaleString(),
      hash: `0x${Math.random().toString(16).substr(2, 8)}...${Math.random().toString(16).substr(2, 4)}`
    };
    setFiles(prev => [newFile, ...prev]);
  };

  const stats = useMemo(() => {
    const original = files.reduce((acc, f) => acc + f.size, 0);
    const refractal = files.reduce((acc, f) => acc + f.refractalWeight, 0);
    return {
      original: (original / (1024 * 1024)).toFixed(2),
      refractal: refractal.toFixed(8)
    };
  }, [files]);

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white tracking-tight mono">Refractal <span className="text-blue-500">Drive</span></h2>
          <p className="text-slate-400 mt-1 uppercase text-[10px] tracking-[0.2em] mono">Infinity-Scale In-House Storage Matrix</p>
        </div>
        <div className="flex space-x-3">
          <button 
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white rounded-lg font-bold uppercase text-xs tracking-widest transition-all shadow-[0_0_15px_rgba(37,99,235,0.4)] flex items-center space-x-2"
          >
            {isUploading ? (
               <div className="w-3 h-3 border-2 border-white/20 border-t-white rounded-full animate-spin"></div>
            ) : (
               <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
            )}
            <span>{isUploading ? 'BATCH_SHARDING...' : 'UPLOAD TO MATRIX'}</span>
          </button>
          <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" multiple />
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StorageStat label="Stored Waveforms" value={files.length.toString()} color="text-blue-400" icon="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        <StorageStat label="Logical Size" value={`${stats.original} MB`} color="text-slate-400" icon="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        <StorageStat label="Physical Usage" value={`${stats.refractal} μb`} color="text-green-400" icon="M13 10V3L4 14h7v7l9-11h-7z" />
        <StorageStat label="Expansion Limit" value="∞" color="text-purple-400" icon="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </div>

      {isUploading && (
        <div className="bg-blue-600/5 border border-blue-500/20 p-6 rounded-2xl animate-in zoom-in-95 duration-300">
           <div className="flex justify-between items-center mb-4 mono text-[10px] text-blue-400 uppercase tracking-widest">
              <span>Refractal Math Batch Sharding Protocol</span>
              <span>{shardingProgress}%</span>
           </div>
           <div className="h-2 bg-slate-900 rounded-full overflow-hidden border border-blue-900/30">
              <div 
                className="h-full bg-blue-500 shadow-[0_0_15px_rgba(37,99,235,0.6)] transition-all duration-300" 
                style={{ width: `${shardingProgress}%` }}
              ></div>
           </div>
           <p className="mt-4 text-[10px] text-slate-500 italic mono text-center animate-pulse uppercase">Decomposing binary shards into recursive prime waves...</p>
        </div>
      )}

      <div className="bg-slate-950/50 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
        <div className="p-4 bg-slate-900/60 border-b border-slate-800 flex justify-between items-center text-[10px] mono text-slate-500 uppercase tracking-[0.2em] font-bold">
          <span className="flex items-center space-x-2">
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" /></svg>
            <span>Root Shard Directory</span>
          </span>
          <div className="hidden md:flex space-x-16">
             <span className="w-24 text-center">Logical Size</span>
             <span className="w-24 text-center">Refractal</span>
             <span className="w-24 text-center">Integrity</span>
          </div>
        </div>
        <div className="divide-y divide-slate-800/40">
          {files.map(file => (
            <div key={file.id} className="p-4 flex flex-col md:flex-row justify-between items-start md:items-center hover:bg-blue-500/5 transition-all group cursor-default">
              <div className="flex items-center space-x-4">
                <div className="w-10 h-10 bg-slate-900 border border-slate-800 rounded-xl flex items-center justify-center text-blue-500 group-hover:border-blue-500/50 transition-all shadow-inner">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                </div>
                <div>
                  <div className="text-sm font-bold text-slate-200 mono group-hover:text-blue-400 transition-colors">{file.name}</div>
                  <div className="text-[9px] text-slate-600 mono flex items-center space-x-2">
                    <span className="text-blue-900">HASH:</span>
                    <span>{file.hash}</span>
                    <span className="text-slate-800">|</span>
                    <span>{file.timestamp}</span>
                  </div>
                </div>
              </div>
              <div className="flex space-x-16 mt-4 md:mt-0 text-right mono items-center">
                 <div className="w-24 text-[11px] text-slate-400">{(file.size / 1024).toFixed(1)} KB</div>
                 <div className="w-24 text-[11px] text-blue-400 font-bold">{file.refractalWeight.toFixed(6)} μb</div>
                 <div className="w-24 flex justify-end">
                    <span className="px-2 py-0.5 rounded-full bg-green-900/20 text-green-500 text-[8px] font-bold border border-green-500/20 uppercase tracking-tighter">Verified</span>
                 </div>
              </div>
            </div>
          ))}
          {files.length === 0 && (
            <div className="p-24 text-center flex flex-col items-center">
              <svg className="w-12 h-12 text-slate-800 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" /></svg>
              <span className="text-slate-600 mono text-sm uppercase tracking-widest italic">Awaiting refractal seeding...</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const StorageStat: React.FC<{ label: string; value: string; color: string; icon: string }> = ({ label, value, color, icon }) => (
  <div className="bg-slate-900/60 border border-slate-800 p-5 rounded-2xl group hover:border-blue-500/20 transition-all">
    <div className="flex items-start justify-between mb-3">
       <div className="text-[9px] text-slate-500 uppercase mono tracking-[0.2em]">{label}</div>
       <svg className={`w-4 h-4 ${color} opacity-40`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={icon} /></svg>
    </div>
    <div className={`text-2xl font-bold mono ${color} tracking-tighter`}>{value}</div>
  </div>
);

export default RefractalDrive;
