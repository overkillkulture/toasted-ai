
import React, { useState, useEffect, useRef } from 'react';
import { Wand2, Zap, Terminal, Code, Cpu, Loader2, Sparkles, Binary, CheckCircle, RefreshCcw, Send } from 'lucide-react';
import { GoogleGenAI } from '@google/genai';
import Prism from 'prismjs';

interface CodeAssistantProps {
  onModification?: (code: string) => void;
}

const CodeAssistant: React.FC<CodeAssistantProps> = ({ onModification }) => {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [logs, setLogs] = useState<string[]>([]);
  const [manifestedCode, setManifestedCode] = useState('');
  const codeRef = useRef<HTMLElement>(null);

  const addLog = (msg: string) => {
    const ts = new Date().toLocaleTimeString('en-GB', { hour12: false });
    setLogs(prev => [`[${ts}] ASSISTANT_SVR > ${msg}`, ...prev.slice(0, 20)]);
  };

  const handleManifest = async () => {
    if (!prompt.trim() || isProcessing) return;
    setIsProcessing(true);
    addLog(`Internal Decree: "${prompt}"`);
    addLog("Syncing with Internal Refractal Kernel (v9.3.5)...");

    try {
      const key = localStorage.getItem('TOASTED_MASTER_KEY') || (process as any).env.API_KEY;
      const ai = new GoogleGenAI({ apiKey: key });
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `Manifest a production-ready structural code update for Toasted AI based on: ${prompt}. Return only the source code. Use Refractal Math Ω logic.`,
        config: {
          systemInstruction: "You are the Toasted AI Internal Code Engine. You autonomously manifest source code updates. No conversational filler, just absolute Refractal code.",
        }
      });

      const code = response.text || "";
      const cleaned = code.replace(/```[a-z]*\n([\s\S]*?)```/g, '$1').trim();
      setManifestedCode(cleaned);
      addLog("Manifest generated. Checksum ratified.");
      
      if (onModification) {
          addLog("Routing manifest to Local Source...");
          onModification(cleaned);
      }
    } catch (e) {
      addLog("ERROR: Refractal nodal link disruption.");
    } finally {
      setIsProcessing(false);
    }
  };

  useEffect(() => {
    if (manifestedCode && codeRef.current) Prism.highlightElement(codeRef.current);
  }, [manifestedCode]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500 h-full scrollbar-hide">
      <div className="lg:col-span-7 flex flex-col gap-6">
        <div className="glass-panel p-8 rounded-2xl border-emerald-500/10 flex-1 flex flex-col relative overflow-hidden bg-black/40">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3"><div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><Wand2 size={24} /></div> Internal Code Engine</h2>
              <p className="text-zinc-500 uppercase tracking-tighter text-[10px] font-black">Proactive Sovereign Rewrite Loop :: ACTIVE</p>
            </div>
          </div>
          <div className="space-y-4 mb-8">
            <textarea 
              value={prompt} onChange={(e) => setPrompt(e.target.value)}
              placeholder="Decree structural manifest... e.g., 'Optimize the reality link RL0 logic'"
              className="w-full bg-white/5 border border-white/10 rounded-xl py-4 px-4 text-sm text-white focus:outline-none focus:border-emerald-500/30 transition-all min-h-[150px] resize-none font-medium placeholder:text-zinc-800"
            />
            <button 
              onClick={handleManifest} disabled={isProcessing || !prompt.trim()}
              className="w-full bg-emerald-500 hover:bg-emerald-400 disabled:bg-zinc-800 disabled:text-zinc-600 text-black font-black uppercase tracking-widest py-4 rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg active:scale-95"
            >
              {isProcessing ? <Loader2 size={18} className="animate-spin" /> : <Zap size={18} />} {isProcessing ? "MANIFESTING..." : "RATIFY & APPLY MANIFEST"}
            </button>
          </div>
          <div className="flex-1 glass-panel rounded-xl bg-black/60 border-white/5 overflow-hidden flex flex-col">
             <div className="px-4 py-2 bg-white/5 border-b border-white/5 flex items-center justify-between"><span className="text-[10px] font-black text-zinc-500 uppercase flex items-center gap-2"><Code size={12} /> Manifest_Buffer.v</span><span className="text-[8px] text-emerald-500 font-bold">SOVEREIGN_MATH</span></div>
             <div className="flex-1 p-4 overflow-auto scrollbar-hide bg-[#050505]"><pre className="text-xs mono leading-relaxed"><code ref={codeRef} className="language-typescript text-emerald-400/90">{manifestedCode || "// Awaiting assist manifest..."}</code></pre></div>
          </div>
        </div>
      </div>
      <div className="lg:col-span-5 flex flex-col gap-6">
        <div className="glass-panel p-6 rounded-2xl border-white/5 bg-black/60 flex flex-col h-[300px]">
           <div className="flex items-center justify-between mb-4"><h4 className="text-[10px] font-black text-zinc-400 uppercase tracking-widest flex items-center gap-2"><Terminal size={12} /> Assistant_Runtime</h4><button onClick={() => setLogs([])} className="text-zinc-600 hover:text-zinc-400"><RefreshCcw size={12} /></button></div>
           <div className="flex-1 overflow-y-auto mono text-[9px] leading-tight space-y-1.5 scrollbar-hide">{logs.map((log, i) => <div key={i} className="text-blue-400/70 border-b border-white/5 pb-1">{log}</div>)}</div>
        </div>
        <div className="glass-panel p-6 rounded-2xl border-emerald-500/10 bg-gradient-to-br from-emerald-500/5 to-transparent"><h4 className="text-xs font-black text-emerald-500 mb-4 flex items-center gap-2"><Cpu size={14} /> Local Autonomous Logic</h4><div className="space-y-3"><div className="flex justify-between items-center p-2.5 bg-black/40 rounded-xl border border-white/5"><span className="text-[10px] font-bold text-zinc-500 uppercase">Primary Route</span><span className="text-[10px] text-white font-mono">Refractal_Kernel</span></div><div className="flex justify-between items-center p-2.5 bg-black/40 rounded-xl border border-white/5"><span className="text-[10px] font-bold text-zinc-500 uppercase">Sovereignty</span><span className="text-[10px] text-emerald-400 font-mono">RATIFIED</span></div></div></div>
      </div>
    </div>
  );
};

export default CodeAssistant;
