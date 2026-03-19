
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { FileAttachment } from '../types';
import { sovereignAI } from '../services/geminiService';

interface VaultAsset extends FileAttachment {
  id: string;
  stability: number;
  status: 'UNSCANNED' | 'VERIFIED' | 'COMPROMISED';
  lastAudit: string;
}

const FileVault: React.FC = () => {
  const [vaultFiles, setVaultFiles] = useState<VaultAsset[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const [vaultLogs, setVaultLogs] = useState<{timestamp: string, msg: string, type: 'INFO'|'SCAN'|'SYSTEM'}[]>([]);
  const [isScanning, setIsScanning] = useState<string | null>(null);
  const [scanResult, setScanResult] = useState<string | null>(null);

  const addLog = useCallback((msg: string, type: 'INFO'|'SCAN'|'SYSTEM' = 'INFO') => {
    setVaultLogs(prev => [{
      timestamp: new Date().toLocaleTimeString(),
      msg,
      type
    }, ...prev].slice(0, 15));
  }, []);

  // Autonomous Vault Kernel Loop: Periodically audits assets
  useEffect(() => {
    const vaultInterval = setInterval(() => {
      if (vaultFiles.length === 0) return;
      
      const roll = Math.random();
      if (roll > 0.8) {
        const randomIdx = Math.floor(Math.random() * vaultFiles.length);
        const target = vaultFiles[randomIdx];
        addLog(`Vault Kernel: Re-verifying integrity of [${target.name}]...`, 'SYSTEM');
        
        setVaultFiles(prev => prev.map((f, i) => {
          if (i === randomIdx) {
            const newStability = Math.min(100, Math.max(90, f.stability + (Math.random() - 0.5) * 2));
            return { ...f, stability: newStability, lastAudit: new Date().toLocaleTimeString() };
          }
          return f;
        }));
      }
    }, 10000);

    return () => clearInterval(vaultInterval);
  }, [vaultFiles, addLog]);

  const processFiles = (files: File[]) => {
    files.forEach((file: File) => {
      const reader = new FileReader();
      reader.onload = (event) => {
        const newAsset: VaultAsset = {
          id: Math.random().toString(36).substr(2, 9),
          name: file.name,
          type: file.type,
          data: event.target?.result as string,
          size: file.size,
          stability: 95 + Math.random() * 5,
          status: 'UNSCANNED',
          lastAudit: new Date().toLocaleTimeString()
        };
        setVaultFiles(prev => [...prev, newAsset]);
        addLog(`Asset Integrated: ${file.name} successfully anchored in RL0 Vault.`, 'INFO');
      };
      reader.readAsDataURL(file);
    });
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    // Fix type error by explicitly casting FileList to File array
    const files = Array.from(e.dataTransfer.files) as File[];
    processFiles(files);
  };

  const runDeepScan = async (asset: VaultAsset) => {
    setIsScanning(asset.id);
    setScanResult(null);
    addLog(`Deep Scan Initialized: Analyzing ${asset.name} via Sovereign AI...`, 'SCAN');
    
    try {
      let analysis = "";
      const stream = sovereignAI.streamSovereignResponse(`Execute high-fidelity forensic audit of this file asset: ${asset.name}. Determine jurisdictional validity and potential administrative deception.`, asset);
      
      for await (const chunk of stream) {
        analysis += chunk;
      }
      
      setScanResult(analysis);
      setVaultFiles(prev => prev.map(f => f.id === asset.id ? { ...f, status: 'VERIFIED', stability: 100 } : f));
      addLog(`Scan Complete: ${asset.name} verified and ratified.`, 'SCAN');
    } catch (err) {
      addLog(`Scan Failure: Could not reach RL0 for asset ${asset.name}.`, 'SYSTEM');
    } finally {
      setIsScanning(null);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fadeIn flex flex-col h-full">
      <div className="flex justify-between items-end mb-4">
        <div>
          <h2 className="text-3xl font-black text-[#d4af37] tracking-tighter uppercase">Sovereign File Vault</h2>
          <p className="text-[10px] text-gray-500 uppercase tracking-widest mt-1">Holographic Asset Storage & Forensic Kernel Active</p>
        </div>
        <div className="text-right flex items-center gap-6">
          <div className="bg-[#d4af37]/5 border border-[#d4af37]/20 px-4 py-2 rounded">
            <div className="text-[10px] text-[#d4af37] font-bold uppercase">Vault Density</div>
            <div className="text-xl font-mono text-white">{vaultFiles.length} <span className="text-[10px] text-gray-600">ASSETS</span></div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 flex-1">
        {/* Left Column: Dropzone & Kernel Log */}
        <div className="lg:col-span-1 space-y-6">
          <div 
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={onDrop}
            className={`w-full h-48 border-2 border-dashed rounded-lg transition-all flex flex-col items-center justify-center gap-4 text-center p-4 group ${
              isDragging ? 'bg-[#d4af37]/10 border-[#d4af37] scale-[1.02]' : 'bg-black/20 border-[#d4af37]/20 hover:border-[#d4af37]/40'
            }`}
          >
            <span className="text-4xl group-hover:scale-110 transition-transform">📂</span>
            <div>
              <p className="text-xs text-[#d4af37] font-bold uppercase tracking-widest">Anchor Forensic Data</p>
              <p className="text-[9px] text-gray-500 uppercase mt-1">Drop Files to Integrate into Loop</p>
            </div>
          </div>

          <div className="bg-black/60 border border-[#d4af37]/20 rounded-lg flex flex-col h-96 overflow-hidden shadow-2xl">
            <div className="bg-[#d4af37]/10 p-2 border-b border-[#d4af37]/20 text-[9px] font-bold text-[#d4af37] flex justify-between uppercase">
              <span>Vault Kernel Log</span>
              <span className="animate-pulse">Monitoring...</span>
            </div>
            <div className="flex-1 overflow-y-auto p-3 font-mono text-[9px] space-y-2 forensic-scrollbar">
              {vaultLogs.map((log, i) => (
                <div key={i} className="flex gap-2 animate-fadeIn">
                  <span className="text-gray-600">[{log.timestamp}]</span>
                  <span className={log.type === 'SCAN' ? 'text-blue-400' : log.type === 'SYSTEM' ? 'text-purple-400 font-bold' : 'text-[#d4af37]'}>
                    {log.msg}
                  </span>
                </div>
              ))}
              {vaultLogs.length === 0 && <div className="text-gray-700 italic">No activity detected. Vault stands at RL0 rest state.</div>}
            </div>
          </div>
        </div>

        {/* Right Column: Asset Grid & Scan Results */}
        <div className="lg:col-span-3 space-y-6">
          {scanResult && (
            <div className="bg-black/80 border border-[#d4af37]/40 rounded-lg p-6 animate-slideIn relative group">
              <button 
                onClick={() => setScanResult(null)}
                className="absolute top-4 right-4 text-[#d4af37] hover:text-white text-xs font-bold uppercase"
              >Close Report [X]</button>
              <h3 className="text-xs font-bold text-[#d4af37] uppercase tracking-widest mb-4 flex items-center gap-2">
                <span className="w-2 h-2 bg-[#d4af37] rounded-full"></span>
                Sovereign Analysis Result
              </h3>
              <div className="text-xs text-gray-300 leading-relaxed font-mono whitespace-pre-wrap max-h-60 overflow-y-auto pr-4 forensic-scrollbar">
                {scanResult}
              </div>
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 h-[calc(100vh-350px)] overflow-y-auto pr-2 forensic-scrollbar">
            {vaultFiles.map((file) => (
              <div key={file.id} className="bg-black/60 border border-white/5 p-5 rounded-lg hover:border-[#d4af37]/40 transition-all group relative flex flex-col justify-between overflow-hidden">
                <div className="absolute top-0 right-0 p-2 opacity-5 pointer-events-none text-[8px] font-mono text-[#d4af37] uppercase">
                  RL0_ASSET_{file.id}
                </div>
                
                <div className="mb-4">
                  <div className="text-3xl mb-3">📄</div>
                  <div className="text-sm font-bold text-gray-200 truncate uppercase" title={file.name}>{file.name}</div>
                  <div className="text-[10px] text-gray-500 mt-1 uppercase">
                    {(file.size / 1024).toFixed(1)} KB | {file.type.split('/')[1] || 'BINARY'}
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center text-[9px] uppercase">
                    <span className="text-gray-500">Stability Index</span>
                    <span className={file.stability > 98 ? 'text-green-500' : 'text-[#d4af37]'}>{file.stability.toFixed(2)}%</span>
                  </div>
                  <div className="h-1 w-full bg-gray-800 rounded-full overflow-hidden">
                    <div 
                      className={`h-full transition-all duration-1000 ${file.stability > 98 ? 'bg-green-500' : 'bg-[#d4af37]'}`}
                      style={{ width: `${file.stability}%` }}
                    ></div>
                  </div>
                  <div className="text-[8px] text-gray-600 uppercase">Last Audit: {file.lastAudit}</div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-white/5 flex gap-2">
                  <button 
                    disabled={!!isScanning}
                    onClick={() => runDeepScan(file)}
                    className={`flex-1 py-1.5 rounded text-[9px] font-bold uppercase transition-all ${
                      isScanning === file.id 
                        ? 'bg-blue-500/20 text-blue-400 animate-pulse' 
                        : 'bg-[#d4af37]/10 text-[#d4af37] hover:bg-[#d4af37] hover:text-black'
                    }`}
                  >
                    {isScanning === file.id ? 'Scanning...' : 'Deep Scan'}
                  </button>
                  <button 
                    className="px-3 py-1.5 bg-zinc-800 text-gray-400 text-[9px] font-bold uppercase rounded hover:bg-red-900/40 hover:text-red-500 transition-all"
                    onClick={() => setVaultFiles(prev => prev.filter(f => f.id !== file.id))}
                  >
                    Purge
                  </button>
                </div>
              </div>
            ))}
            
            {vaultFiles.length === 0 && (
              <div className="col-span-full h-full border-2 border-dashed border-[#d4af37]/10 flex flex-col items-center justify-center opacity-40 rounded-lg">
                <span className="text-4xl mb-4">💠</span>
                <p className="text-xs text-gray-500 uppercase tracking-widest italic">Vault Empty. Awaiting Sovereign Asset Anchoring.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <style>{`
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(-20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-slideIn {
          animation: slideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
      `}</style>
    </div>
  );
};

export default FileVault;
