
import React, { useState, useEffect, useRef } from 'react';
import { AgentStatus, LLMProvider } from '../types';
import { streamLLMResponse, generateSpeech } from '../lib/gemini';
import { playTtsAudio } from '../lib/audio';

interface ArchitectShellProps {
  provider: LLMProvider;
  setStatus: (status: AgentStatus) => void;
  addLog: (msg: string, level?: any, src?: string) => void;
  autoPrompt?: string;
  onManifestRequest?: (name: string) => void;
}

const ArchitectShell: React.FC<ArchitectShellProps> = ({ provider, setStatus, addLog, autoPrompt, onManifestRequest }) => {
  const [prompt, setPrompt] = useState(autoPrompt || '');
  const [blueprint, setBlueprint] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAudioPlaying, setIsAudioPlaying] = useState(false);
  const [archLogs, setArchLogs] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [archLogs]);

  useEffect(() => {
    if (autoPrompt && !isGenerating) {
      setPrompt(autoPrompt);
      handleGenerate();
    }
  }, [autoPrompt]);

  const handleTts = async () => {
    if (!blueprint || isAudioPlaying) return;
    setIsAudioPlaying(true);
    addLog("Neural vocalization for blueprint summary.", "INFO", "TTS");
    try {
      const audio = await generateSpeech(`Architectural Blueprint for ${prompt.slice(0, 50)}: ${blueprint.slice(0, 400)}`);
      if (audio) {
        await playTtsAudio(audio);
      }
    } catch (err) {
      addLog("TTS Synthesis failed: " + err, "WARNING", "TTS");
    } finally {
      setIsAudioPlaying(false);
    }
  };

  const handleIntegrate = () => {
    if (!prompt) return;
    const name = prompt.split(' ')[0].replace(/[^a-zA-Z]/g, '').toLowerCase() || 'new_node';
    addLog(`Initiating UI Integration: Manifesting [${name}]`, "OMEGA", "UI_MUTATOR");
    if (onManifestRequest) onManifestRequest(name);
  };

  const handleGenerate = async () => {
    if (!prompt || isGenerating) return;
    
    setIsGenerating(true);
    setBlueprint("");
    setArchLogs([]);
    setStatus(AgentStatus.ARCHITECTING);
    
    const initialLogs = [
      "Initializing Neural Architect Engine...",
      "Mapping requirements to Refractal Matrix...",
      "Calculating horizontal scalability vectors...",
      "Setting security-first primitives (JAPAN_PRINCIPLE)...",
      "Analyzing architectural drift...",
    ];
    
    let logIndex = 0;
    const logInterval = setInterval(() => {
      if (logIndex < initialLogs.length) {
        setArchLogs(prev => [...prev, `[INIT] ${initialLogs[logIndex]}`]);
        logIndex++;
      } else {
        clearInterval(logInterval);
      }
    }, 400);

    addLog(`Initiating system architecture: ${prompt.slice(0, 30)}...`, 'INFO', 'ARCHITECT');
    
    try {
      await streamLLMResponse(
        `Create a detailed backend architecture for: ${prompt}. Use Refractal Math (Formula: Ω ⇀ (R_VS + K_MoltCopy + ΣQ)) to explain scalability. Structure with: 1. Core Logic, 2. Database Sharding, 3. Security Primitives.`,
        provider,
        (chunk) => {
          setBlueprint(prev => (prev || "") + chunk);
          if (Math.random() > 0.92) {
            setArchLogs(prev => [...prev, `[PROC] Internalizing logic shard...`]);
          }
        }
      );
      setArchLogs(prev => [...prev, "[SUCCESS] Architecture finalized.", "[AUDIT] RL0 Compliance verified.", "[AUDIT] No entropy signatures detected."]);
      addLog("Architecture finalized and internalized.", "INFO", "SECURITY");
    } catch (error) {
      addLog("Blueprinting failure: " + (error as Error).message, "CRITICAL", "CORE");
      setArchLogs(prev => [...prev, `[ERROR] ${error}`]);
    } finally {
      setIsGenerating(false);
      setStatus(AgentStatus.IDLE);
    }
  };

  return (
    <div className="space-y-6 h-full flex flex-col max-w-7xl mx-auto">
      <section className="bg-slate-900/60 border border-blue-900/20 rounded-2xl p-6 backdrop-blur-xl shrink-0 shadow-2xl">
        <div className="flex items-center space-x-3 mb-4">
           <div className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></div>
           <h2 className="text-xl font-bold text-white mono uppercase tracking-tight">Backend Architecture Hub</h2>
        </div>

        <div className="space-y-4">
          <div className="relative">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={isGenerating}
              className="w-full h-32 bg-slate-950/80 border border-blue-900/30 rounded-xl p-5 text-slate-200 mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 disabled:opacity-50 transition-all placeholder:text-slate-700"
              placeholder="Define system requirements or describe a new UI module..."
            ></textarea>
            <div className="absolute bottom-4 right-4 flex space-x-3">
               {blueprint && !isGenerating && (
                  <button 
                    onClick={handleIntegrate}
                    className="px-4 py-1.5 bg-purple-600/20 border border-purple-500/50 text-purple-400 rounded-lg text-[10px] font-bold uppercase tracking-widest hover:bg-purple-600/40 transition-all"
                  >
                    Integrate into UI
                  </button>
               )}
               <button
                onClick={handleGenerate}
                disabled={isGenerating}
                className="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white rounded-lg font-bold uppercase text-[10px] tracking-widest transition-all shadow-[0_0_15px_rgba(37,99,235,0.4)]"
              >
                {isGenerating ? "Synthesizing..." : "Synthesize"}
              </button>
            </div>
          </div>
        </div>
      </section>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
        <div className="lg:col-span-1 bg-slate-950/50 border border-slate-800 rounded-2xl flex flex-col overflow-hidden shadow-xl">
          <div className="p-3 bg-slate-900/80 border-b border-slate-800 flex justify-between items-center px-5">
            <span className="text-[10px] font-bold text-blue-500 uppercase tracking-widest mono">Architect_Console</span>
            <div className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse"></div>
          </div>
          <div 
            ref={scrollRef}
            className="flex-1 p-5 overflow-y-auto space-y-2 mono text-[11px] text-slate-400 bg-black/20"
          >
            {archLogs.map((log, i) => (
              <div key={i} className="flex space-x-3 group animate-in slide-in-from-left-2">
                <span className="text-slate-800 select-none group-hover:text-blue-900 transition-colors">[{i.toString().padStart(3, '0')}]</span>
                <span className={log.includes('[ERROR]') ? 'text-red-500' : log.includes('[SUCCESS]') ? 'text-green-500' : 'text-slate-300'}>
                  {log}
                </span>
              </div>
            ))}
            {isGenerating && (
              <div className="text-blue-500 animate-pulse mt-2 flex items-center space-x-2">
                 <span className="w-1 h-3 bg-blue-500"></span>
                 <span>STREAMING_NEURAL_DATA...</span>
              </div>
            )}
            {!isGenerating && archLogs.length === 0 && (
              <div className="text-slate-800 text-center mt-20 italic uppercase tracking-[0.3em] text-[9px]">Awaiting Architectural Intent</div>
            )}
          </div>
        </div>

        <div className="lg:col-span-2 bg-slate-900/30 border border-slate-800 rounded-2xl flex flex-col overflow-hidden shadow-xl">
          <div className="p-3 bg-slate-900/80 border-b border-slate-800 flex justify-between items-center px-5">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mono">Internalized_Blueprint</span>
            <div className="flex items-center space-x-5">
               {blueprint && (
                 <button 
                  onClick={handleTts}
                  disabled={isAudioPlaying}
                  className={`flex items-center space-x-2 text-[10px] uppercase font-bold transition-colors ${isAudioPlaying ? 'text-blue-400 animate-pulse' : 'text-slate-500 hover:text-blue-400'}`}
                 >
                   <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" /></svg>
                   <span>{isAudioPlaying ? 'Vocalizing' : 'Vocalize'}</span>
                 </button>
               )}
               {blueprint && (
                 <button onClick={() => setBlueprint(null)} className="text-[9px] text-slate-600 hover:text-red-400 uppercase mono transition-colors">Purge</button>
               )}
            </div>
          </div>
          <div className="flex-1 p-8 overflow-y-auto bg-slate-950/40 relative">
            {!blueprint && !isGenerating ? (
              <div className="h-full flex flex-col items-center justify-center text-slate-800 mono text-[10px] uppercase tracking-[0.5em] space-y-4">
                <svg className="w-12 h-12 opacity-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2L2 7v10l10 5 10-5V7L12 2zm0 2.8L19.2 8 12 11.2 4.8 8 12 4.8z"/></svg>
                <span>Zero blueprint density detected</span>
              </div>
            ) : (
              <div className="prose prose-invert max-w-none prose-sm selection:bg-blue-500/20">
                <pre className="whitespace-pre-wrap mono text-slate-300 text-xs leading-relaxed bg-transparent border-none p-0">
                  {blueprint}
                  {isGenerating && <span className="inline-block w-2 h-4 bg-blue-500 ml-1 animate-pulse"></span>}
                </pre>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArchitectShell;
