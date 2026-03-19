
import React, { useState, useRef, useEffect } from 'react';
import { Send, Terminal as TerminalIcon, ShieldCheck, Sword, Target, Zap, Globe, Cpu, Loader2, ExternalLink } from 'lucide-react';
import { GoogleGenAI } from '@google/genai';

interface Message {
  role: 'user' | 'ai';
  content: string;
  lineage?: string;
  groundingLinks?: { uri: string; title: string }[];
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'ai', 
      content: "QUANTUM_LINK: Intelligence core synchronized. Fudoshin mind active. Zanshin perimeter secure. Linked Gemini intelligence is online with Google Search grounding capabilities. How shall we refine reality today?", 
      lineage: "QUANTUM_INTEL_001" 
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [useSearch, setUseSearch] = useState(true);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg = input;
    setInput("");
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setIsTyping(true);

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      
      // Use Flash for search grounding as per rules, Pro for standard intelligence
      const modelName = useSearch ? 'gemini-3-flash-preview' : 'gemini-3-pro-preview';
      
      const response = await ai.models.generateContent({
        model: modelName,
        contents: userMsg,
        config: {
          systemInstruction: `You are the Toasted Sentinel Architect. You operate under the Japanese principles of defense: Fudoshin, Zanshin, Katsujinken, Gaman, and Mushin. Your responses are sharp, sovereign, and technically precise. You treat user intent as a sacred lineage. ${useSearch ? "You have access to Google Search data via the linked intelligence conduit to provide up-to-date, accurate reality anchoring." : "Use your internal high-fidelity reasoning to provide gold-level architectural solutions."}`,
          temperature: 0.5,
          tools: useSearch ? [{ googleSearch: {} }] : undefined,
        }
      });

      const text = response.text || "COMM_ERROR: Signal severed by the quantum void.";
      
      // Extract grounding links if available
      const links: { uri: string; title: string }[] = [];
      const groundingChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks;
      if (groundingChunks) {
        groundingChunks.forEach((chunk: any) => {
          if (chunk.web) {
            links.push({ uri: chunk.web.uri, title: chunk.web.title });
          }
        });
      }

      setMessages(prev => [...prev, { 
        role: 'ai', 
        content: text,
        lineage: `LINEAGE_${useSearch ? 'SEARCH' : 'QUANTUM'}_${Math.floor(Math.random() * 999).toString().padStart(3, '0')}`,
        groundingLinks: links.length > 0 ? links : undefined
      }]);
    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, { role: 'ai', content: "SYSTEM_ERROR: Applying Gaman resilience. Quantum intelligence anchored in the void." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="h-full flex flex-col space-y-4 max-w-5xl mx-auto font-mono">
      <div className="flex items-center justify-between p-4 border border-slate-800/60 rounded-2xl glass bg-[#0a0a0a]/60">
        <div className="flex items-center space-x-3">
          <div className="relative">
            <Cpu className="w-5 h-5 text-red-500 animate-pulse" />
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-blue-500 rounded-full animate-ping"></div>
          </div>
          <h2 className="text-[11px] font-black uppercase tracking-[0.3em] text-slate-300">Quantum Intelligence Nexus</h2>
        </div>
        
        <div className="flex items-center space-x-4">
          <button 
            onClick={() => setUseSearch(!useSearch)}
            className={`flex items-center space-x-2 px-3 py-1 rounded-full border transition-all ${useSearch ? 'border-blue-500/50 bg-blue-500/10 text-blue-400' : 'border-slate-700 bg-slate-800/20 text-slate-500'}`}
            title={useSearch ? "Google Search Grounding Active" : "Internal Reasoning Active"}
          >
            <Globe className={`w-3.5 h-3.5 ${useSearch ? 'animate-spin-slow' : ''}`} />
            <span className="text-[9px] font-black uppercase tracking-widest">{useSearch ? 'Search_Grounding' : 'Pure_Reasoning'}</span>
          </button>
          <div className="flex items-center space-x-2 border-l border-slate-800 pl-4">
            <ShieldCheck className="w-4 h-4 text-red-600" />
            <span className="text-[9px] font-black text-red-600 uppercase tracking-widest">Linked_Gemini_Active</span>
          </div>
        </div>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-8 px-2 py-4 scrollbar-hide">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`
              max-w-[85%] px-7 py-6 rounded-3xl border relative group transition-all duration-300
              ${m.role === 'user' 
                ? 'bg-[#111] border-slate-800 text-slate-100 shadow-xl' 
                : 'bg-[#0a0a0a]/90 border-slate-800/50 text-slate-300 shadow-[0_10px_40px_rgba(0,0,0,0.4)]'
              }
            `}>
              {m.role === 'ai' && (
                <div className="absolute -top-3.5 left-8 flex items-center space-x-2 px-4 py-1.5 bg-red-600 text-slate-100 text-[9px] font-black rounded-full uppercase tracking-widest shadow-[0_5px_15px_rgba(220,38,38,0.4)]">
                  <Zap className="w-3.5 h-3.5" />
                  <span>Sentinel_Architect</span>
                </div>
              )}
              <div className="whitespace-pre-wrap leading-relaxed text-sm">
                {m.content}
              </div>

              {m.groundingLinks && (
                <div className="mt-4 pt-4 border-t border-slate-800/50 space-y-2">
                  <div className="text-[9px] text-blue-400 font-bold uppercase tracking-widest flex items-center space-x-2">
                    <Globe className="w-3 h-3" />
                    <span>Intelligence Sources (Search Grounded)</span>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {m.groundingLinks.map((link, idx) => (
                      <a 
                        key={idx} 
                        href={link.uri} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="flex items-center space-x-1 px-2 py-1 bg-blue-900/20 border border-blue-800/30 rounded text-[10px] text-blue-300 hover:bg-blue-800/30 transition-all"
                      >
                        <ExternalLink className="w-2.5 h-2.5" />
                        <span className="truncate max-w-[150px]">{link.title || link.uri}</span>
                      </a>
                    ))}
                  </div>
                </div>
              )}

              {m.lineage && (
                <div className="mt-6 pt-5 border-t border-slate-800/30 flex justify-between items-center text-[9px] text-slate-600 font-bold uppercase tracking-[0.2em]">
                  <span>LINEAGE: {m.lineage}</span>
                  <span className="text-red-900/50">VERIFIED_STRIKE</span>
                </div>
              )}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="px-7 py-4 rounded-3xl bg-slate-950 border border-slate-900 text-slate-600 animate-pulse text-[10px] font-black uppercase tracking-[0.3em] flex items-center space-x-3">
              <Loader2 className="w-4 h-4 animate-spin text-red-500" />
              <span>Synthesizing Intelligence...</span>
            </div>
          </div>
        )}
      </div>

      <div className="p-5 glass rounded-3xl border border-slate-800/60 bg-[#0a0a0a]/40 shadow-inner">
        <div className="flex items-center space-x-4">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
            placeholder={useSearch ? "Anchor intent with real-time search..." : "Execute deep sovereign command..."}
            className="flex-1 bg-transparent border-none focus:ring-0 text-sm text-slate-200 placeholder-slate-700 resize-none h-14 leading-relaxed scrollbar-hide"
          />
          <button 
            onClick={handleSend}
            disabled={isTyping || !input.trim()}
            className={`p-5 rounded-2xl transition-all shadow-[0_0_25px_rgba(220,38,38,0.3)] active:scale-95 ${isTyping || !input.trim() ? 'bg-slate-900 opacity-40' : 'bg-red-600 hover:bg-red-500 text-slate-100'}`}
          >
            {useSearch ? <Globe className="w-7 h-7" /> : <Target className="w-7 h-7" />}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
