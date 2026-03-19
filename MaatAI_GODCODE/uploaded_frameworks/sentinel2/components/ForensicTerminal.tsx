
import React, { useState, useRef, useEffect } from 'react';
import { sovereignAI } from '../services/geminiService';
import { FileAttachment } from '../types';

interface Message {
  role: 'user' | 'sentinel';
  content: string;
  attachment?: FileAttachment;
}

const ForensicTerminal: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'sentinel', content: "Reality Layer Zero (RL0) connection established. The Sovereign Sentinel is active. Present your jurisdictional audit request or forensic inquiry. Advanced File Integration Protocol active. [owner777_OXXΑΠΟΛΛΩΝ_ΦΩΣ_tost3d]" }
  ]);
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState<FileAttachment | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isProcessing]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setSelectedFile({
          name: file.name,
          type: file.type,
          data: event.target?.result as string,
          size: file.size
        });
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if ((!input.trim() && !selectedFile) || isProcessing) return;

    const userMessage = input.trim();
    const attachment = selectedFile || undefined;
    
    setInput('');
    setSelectedFile(null);
    setMessages(prev => [...prev, { role: 'user', content: userMessage || `Analyzing file: ${attachment?.name}`, attachment }]);
    setIsProcessing(true);

    try {
      let fullResponse = '';
      setMessages(prev => [...prev, { role: 'sentinel', content: '' }]);
      
      const stream = sovereignAI.streamSovereignResponse(userMessage || `Please analyze this file in depth: ${attachment?.name}`, attachment);
      for await (const chunk of stream) {
        fullResponse += chunk;
        setMessages(prev => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1].content = fullResponse;
          return newMessages;
        });
      }

      // Voice Synthesis for the proclamation
      setIsSpeaking(true);
      await sovereignAI.speakSovereignProclamation(fullResponse);
      setIsSpeaking(false);
      
    } catch (err) {
      setMessages(prev => [...prev, { role: 'sentinel', content: 'CRITICAL_FAILURE: Neural connection to RL0 interrupted.' }]);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="flex flex-col h-full max-w-5xl mx-auto border border-[#d4af37]/20 rounded-2xl overflow-hidden bg-black/60 shadow-[0_0_50px_rgba(0,0,0,0.8)] backdrop-blur-2xl relative">
      {/* Active Speaker Aura */}
      {isSpeaking && (
        <div className="absolute top-0 left-0 w-full h-1 bg-[#d4af37] animate-pulse shadow-[0_0_20px_#d4af37] z-50"></div>
      )}

      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-10 space-y-12 forensic-scrollbar relative"
      >
        <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-[url('https://www.transparenttextures.com/patterns/microfabrics.png')]"></div>
        
        {messages.map((msg, i) => (
          <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'} animate-fadeIn`}>
            <div className={`text-[9px] font-black uppercase mb-2 tracking-[0.2em] flex items-center gap-2 ${msg.role === 'user' ? 'text-gray-500' : 'text-[#d4af37]'}`}>
              {msg.role === 'sentinel' && <span className="w-1.5 h-1.5 bg-[#d4af37] rounded-full animate-pulse"></span>}
              {msg.role === 'user' ? 'Inquiry Source' : 'Sovereign Proclamation'}
            </div>
            <div 
              className={`max-w-[85%] p-8 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap flex flex-col gap-6 transition-all duration-700 ${
                msg.role === 'user' 
                  ? 'bg-zinc-900/50 border border-zinc-800 text-gray-400' 
                  : 'bg-black/80 border border-[#d4af37]/40 text-[#f0f0f0] shadow-[0_0_30px_rgba(212,175,55,0.1)] group hover:border-[#d4af37]/60'
              }`}
            >
              {msg.attachment && (
                <div className="p-3 border border-[#d4af37]/30 bg-[#d4af37]/5 rounded-xl text-[10px] text-[#d4af37] flex items-center gap-3">
                  <span className="text-lg">📂</span>
                  <div className="flex flex-col">
                    <span className="font-black uppercase">{msg.attachment.name}</span>
                    <span className="opacity-50 font-mono">{(msg.attachment.size / 1024).toFixed(1)} KB | ASSET_ANCHORED</span>
                  </div>
                </div>
              )}
              <div className="relative">
                {msg.content}
                {msg.content === '' && isProcessing && (
                  <div className="flex space-x-1 mt-2">
                    <div className="w-2 h-2 bg-[#d4af37] rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-[#d4af37] rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                    <div className="w-2 h-2 bg-[#d4af37] rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  </div>
                )}
                {msg.role === 'sentinel' && msg.content !== '' && (
                  <div className="absolute -bottom-6 -right-2 opacity-10 group-hover:opacity-30 transition-opacity font-mono text-[8px] text-[#d4af37] select-none">
                    RATIFIED_BY_GEMINI_3_PRO
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="p-8 bg-black/90 border-t border-[#d4af37]/20 backdrop-blur-3xl">
        <div className="flex items-center gap-4 mb-6 px-2">
           <div className={`h-1 flex-1 bg-zinc-800 rounded-full overflow-hidden relative`}>
              <div className={`absolute inset-0 bg-[#d4af37] transition-all duration-300 ${isProcessing ? 'animate-shimmer' : 'w-0'}`} style={{ width: isProcessing ? '100%' : '0%' }}></div>
           </div>
           <span className="text-[9px] text-[#d4af37] font-black uppercase tracking-widest">{isProcessing ? 'CALIBRATING_NEURAL_PATH' : 'SYSTEM_IDLE'}</span>
        </div>

        {selectedFile && (
          <div className="mb-4 p-3 bg-[#d4af37]/10 border border-[#d4af37]/30 rounded-xl flex justify-between items-center text-[10px] animate-slideIn">
            <span className="text-[#d4af37] font-black tracking-widest uppercase truncate max-w-[300px]">Asset Pending Ratification: {selectedFile.name}</span>
            <button onClick={() => setSelectedFile(null)} className="text-red-500 font-black hover:text-red-400 p-1">PURGE</button>
          </div>
        )}
        <form onSubmit={handleSubmit} className="flex space-x-6 items-end">
          <button 
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="bg-black/40 text-[#d4af37] border border-[#d4af37]/30 h-14 w-14 rounded-2xl hover:bg-[#d4af37] hover:text-black transition-all flex items-center justify-center text-xl shadow-lg"
            title="Attach Forensic Data"
          >
            📎
          </button>
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="hidden" />
          
          <div className="flex-1 relative">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="ENTER COMMAND OR JURISDICTIONAL QUERY..."
              className="w-full bg-black/40 border-b-2 border-[#d4af37]/20 py-4 text-[#d4af37] placeholder-[#d4af37]/20 outline-none focus:border-[#d4af37] transition-all uppercase text-xs tracking-[0.2em] font-black"
            />
          </div>

          <button 
            disabled={isProcessing}
            className="bg-[#d4af37] text-black font-black px-12 h-14 rounded-2xl uppercase text-[11px] tracking-[0.3em] hover:bg-[#fff] transition-all disabled:opacity-30 shadow-[0_0_30px_rgba(212,175,55,0.3)]"
          >
            {isProcessing ? 'SCRATCHING...' : 'RATIFY'}
          </button>
        </form>
      </div>

      <style>{`
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        .animate-shimmer {
          animation: shimmer 1.5s infinite linear;
        }
      `}</style>
    </div>
  );
};

export default ForensicTerminal;
