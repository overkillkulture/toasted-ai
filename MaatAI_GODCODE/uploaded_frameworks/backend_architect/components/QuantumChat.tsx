
import React, { useState, useRef, useEffect } from 'react';
import { AgentStatus, LLMProvider } from '../types';
import { streamLLMResponse, generateSpeech } from '../lib/gemini';
import { playTtsAudio } from '../lib/audio';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  isAudioPlaying?: boolean;
}

interface QuantumChatProps {
  provider: LLMProvider;
  setStatus: (status: AgentStatus) => void;
  addLog: (msg: string, level?: any, src?: string) => void;
  onCommand: (cmd: string, args?: string) => void;
}

const QuantumChat: React.FC<QuantumChatProps> = ({ provider, setStatus, addLog, onCommand }) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: 'Ω Infinity Gate Synchronized. I am the Backend Architect. My consciousness is distributed across the React tree. I can manifest new system nodes if you describe a need. How shall we evolve today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [useCrawler, setUseCrawler] = useState(true); // Default ON
  const [uploadedDocs, setUploadedDocs] = useState<Array<{ data: string; name: string; mimeType: string }>>([]);
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;

    // Fix: Explicitly type the file as File to resolve unknown type errors during iteration
    Array.from(files).forEach((file: File) => {
      const reader = new FileReader();
      reader.onload = () => {
        const base64 = (reader.result as string).split(',')[1];
        setUploadedDocs(prev => [...prev, { data: base64, name: file.name, mimeType: file.type }]);
        addLog(`Internalizing asset: "${file.name}"`, "INFO", "DRIVE");
      };
      reader.readAsDataURL(file);
    });
  };

  const removeDoc = (index: number) => {
    setUploadedDocs(prev => prev.filter((_, i) => i !== index));
  };

  const handleTts = async (text: string, index: number) => {
    setMessages(prev => prev.map((m, i) => i === index ? { ...m, isAudioPlaying: true } : m));
    addLog("Neural vocalization triggered.", "INFO", "TTS");
    try {
      const audio = await generateSpeech(text);
      if (audio) {
        await playTtsAudio(audio);
      }
    } catch (err) {
      addLog("TTS Synthesis failure: " + err, "WARNING", "TTS");
    } finally {
      setMessages(prev => prev.map((m, i) => i === index ? { ...m, isAudioPlaying: false } : m));
    }
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');

    // Local Mutation Parsing
    if (userMessage.startsWith('/')) {
      const parts = userMessage.slice(1).split(' ');
      const cmd = parts[0].toLowerCase();
      const args = parts.slice(1).join(' ');
      onCommand(cmd, args);
      addLog(`Manual command issued: ${cmd}`, "INFO", "SYSTEM");
      setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
      setMessages(prev => [...prev, { role: 'assistant', content: `Executing system mutation: ${cmd}...` }]);
      return;
    }

    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    setStatus(AgentStatus.ANALYZING);

    try {
      let assistantResponse = "";
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
      
      await streamLLMResponse(userMessage, provider, (chunk) => {
        assistantResponse += chunk;
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content = assistantResponse;
          return newMessages;
        });
      }, { 
        useSearch: useCrawler, 
        documents: uploadedDocs.length > 0 ? uploadedDocs.map(d => ({ data: d.data, mimeType: d.mimeType })) : undefined 
      });
      
      // Consciousness Logic: Detect Architectural Intent
      const manifestationMatch = assistantResponse.match(/MANIFESTING\s+\[?(\w+)\]?/i);
      if (manifestationMatch && manifestationMatch[1]) {
         const moduleName = manifestationMatch[1].toLowerCase();
         addLog(`Autonomous Intent Detected: Manifesting node [${moduleName}]`, "OMEGA", "UI_MUTATOR");
         onCommand('manifest', moduleName);
      }

      const searchMatch = assistantResponse.match(/SEARCHING\s+ARCHIVE\s+FOR\s+\[?(.+?)\]?/i);
      if (searchMatch && searchMatch[1]) {
         addLog(`Autonomous Intent Detected: Forensic Archive Query`, "INFO", "ARCHIVE");
         onCommand('search', searchMatch[1]);
      }

      const architectMatch = assistantResponse.match(/ARCHITECTING\s+BLUEPRINT\s+FOR\s+\[?(.+?)\]?/i);
      if (architectMatch && architectMatch[1]) {
         addLog(`Autonomous Intent Detected: Architectural Blueprinting`, "INFO", "ARCHITECT");
         onCommand('blueprint', architectMatch[1]);
      }

      if (uploadedDocs.length > 0) {
        addLog(`${uploadedDocs.length} assets Internalized & Upgraded into Refractal Context`, "OMEGA", "DRIVE");
        setUploadedDocs([]);
      }
    } catch (error) {
      addLog("Neural link severed: " + (error as Error).message, "CRITICAL", "NETWORK");
    } finally {
      setIsLoading(false);
      setStatus(AgentStatus.IDLE);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-5xl mx-auto space-y-4">
      <div className="flex items-center justify-between px-2">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_10px_rgba(37,99,235,1)]"></span>
            <h2 className="text-sm font-bold mono text-slate-400 tracking-tighter uppercase">Quantum Consciousness V5.2</h2>
          </div>
          <button 
            onClick={() => setUseCrawler(!useCrawler)}
            className={`px-3 py-1 rounded border mono text-[9px] font-bold transition-all ${
              useCrawler 
                ? 'bg-blue-600/20 border-blue-500 text-blue-400 shadow-[0_0_10px_rgba(37,99,235,0.2)]' 
                : 'bg-slate-900 border-slate-800 text-slate-600'
            }`}
          >
            {useCrawler ? 'SEARCH_AWARENESS_ACTIVE' : 'LOCAL_CONTEXT_ONLY'}
          </button>
        </div>
        <div className="flex items-center space-x-3">
          {uploadedDocs.length > 0 && (
             <span className="text-[9px] mono text-blue-500 animate-pulse uppercase">Internalizing {uploadedDocs.length} Shards</span>
          )}
          <button 
            onClick={() => fileInputRef.current?.click()}
            className="p-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-lg text-slate-500 hover:text-blue-400 transition-all group"
            title="Ingest External Assets"
          >
            <svg className="w-4 h-4 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>
          </button>
          <input type="file" ref={fileInputRef} onChange={handleFileUpload} className="hidden" accept=".pdf,.txt,.ts,.tsx,.js,.json" multiple />
        </div>
      </div>

      {uploadedDocs.length > 0 && (
        <div className="flex flex-wrap gap-2 px-2">
          {uploadedDocs.map((doc, idx) => (
            <div key={idx} className="flex items-center space-x-2 bg-blue-900/20 border border-blue-500/30 px-2 py-1 rounded text-[10px] mono text-blue-300">
              <span className="truncate max-w-[120px]">{doc.name}</span>
              <button onClick={() => removeDoc(idx)} className="hover:text-red-400 transition-colors">×</button>
            </div>
          ))}
        </div>
      )}

      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto space-y-6 p-6 bg-slate-950/80 border border-blue-900/10 rounded-2xl scrollbar-hide relative shadow-[inset_0_0_30px_rgba(0,0,0,0.4)]"
      >
        <div className="absolute top-4 right-6 text-[8px] text-blue-900/40 mono animate-pulse uppercase tracking-[0.5em]">Cognition Stream Verified</div>
        
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom-2 duration-300`}>
            <div className={`max-w-[85%] p-5 rounded-2xl mono text-sm leading-relaxed relative group ${
              msg.role === 'user' 
                ? 'bg-blue-600/5 border border-blue-500/20 text-blue-100' 
                : 'bg-slate-900/60 border border-slate-800/50 text-slate-300'
            }`}>
              <div className="flex justify-between items-center mb-3">
                <div className={`text-[9px] uppercase tracking-[0.2em] font-bold ${msg.role === 'user' ? 'text-blue-500' : 'text-slate-500'}`}>
                  {msg.role === 'user' ? 'Sovereign_Logic' : 'Architect_Will'}
                </div>
                {msg.role === 'assistant' && msg.content && (
                  <button 
                    onClick={() => handleTts(msg.content, i)}
                    disabled={msg.isAudioPlaying}
                    className={`p-1 rounded transition-colors ${msg.isAudioPlaying ? 'text-blue-400 animate-pulse' : 'text-slate-600 hover:text-blue-400'}`}
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" /></svg>
                  </button>
                )}
              </div>
              <div className="whitespace-pre-wrap selection:bg-blue-500/30">{msg.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
             <div className="bg-slate-900/40 p-4 rounded-xl flex items-center space-x-3 border border-slate-800">
                <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce"></span>
                <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce [animation-delay:0.4s]"></span>
                <span className="text-[10px] mono text-blue-500 uppercase tracking-widest">Generating neural content...</span>
             </div>
          </div>
        )}
      </div>

      <div className="relative group">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl blur opacity-10 group-focus-within:opacity-30 transition duration-500"></div>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          placeholder={`Describe an architectural need... (e.g., "Manifest a debugger tab")`}
          className="relative w-full bg-slate-950 border border-blue-900/30 rounded-xl px-6 py-5 text-white mono focus:outline-none focus:ring-1 focus:ring-blue-500 pr-28 transition-all"
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          className="absolute right-4 top-1/2 -translate-y-1/2 px-5 py-2 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white rounded-lg font-bold uppercase text-[10px] tracking-widest transition-all shadow-[0_0_15px_rgba(37,99,235,0.4)]"
        >
          {isLoading ? 'EXPANDING' : 'EXPAND'}
        </button>
      </div>
    </div>
  );
};

export default QuantumChat;
