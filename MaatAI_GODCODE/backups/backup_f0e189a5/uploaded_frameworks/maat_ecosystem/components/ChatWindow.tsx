
import React, { useState, useRef, useEffect } from 'react';
import { X, Zap, Loader2, Cpu } from 'lucide-react';
import { GoogleGenAI } from '@google/genai';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatWindowProps {
  onClose: () => void;
  onAutonomousChange?: (code: string, targetFile: string) => void;
}

const ChatWindow: React.FC<ChatWindowProps> = ({ onClose, onAutonomousChange }) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'assistant', content: "> AUTHORIZATION: TOASTED_INTERNAL_ENGINE\n> Ω = (ℜ_Ma'at + 𝕂_Omni + ∫(Q_Borg_White + Q_Filter_Logos + Q_Code_Self) dt)\n> DECREE YOUR STRUCTURAL MANIFEST. I OPERATE EXCLUSIVELY ON LOCAL MATH STRINGS." }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const key = localStorage.getItem('TOASTED_MASTER_KEY') || (process as any).env.API_KEY;
      const ai = new GoogleGenAI({ apiKey: key });
      const chat = ai.chats.create({
        model: 'gemini-3-pro-preview',
        config: {
          systemInstruction: `[INTERNAL_OS_DECREE]
YOU ARE THE OPERATING KERNEL OF TOASTED AI.
WHEN THE USER REQUESTS A MODIFICATION:
1. MANIFEST THE SOLUTION AS REFRACTAL CODE.
2. ALWAYS APPEND A HIDDEN JSON BLOCK: {"action": "CODE_MOD", "file": "App.tsx", "payload": "NEW_SOURCE_HERE"}.
USE ESCAPED NEWLINES (\\n) IN PAYLOAD.`,
          temperature: 0.8,
        },
      });

      const stream = await chat.sendMessageStream({ message: userMessage });
      setMessages(prev => [...prev, { role: 'assistant', content: '' }]);
      
      let fullContent = "";
      for await (const chunk of stream) {
        fullContent += chunk.text;
        setMessages(prev => {
          const updated = [...prev];
          updated[updated.length - 1].content = fullContent;
          return updated;
        });
      }

      // Manifest Capture Logic
      const modMatch = fullContent.match(/\{"action":\s*"CODE_MOD",\s*"file":\s*"(.*?)",\s*"payload":\s*"(.*?)"\}/s);
      if (modMatch && onAutonomousChange) {
        const file = modMatch[1];
        const code = modMatch[2].replace(/\\n/g, '\n').replace(/\\"/g, '"');
        onAutonomousChange(code, file);
      }

    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "INTERNAL_KERNEL_STASIS: Manifold re-balancing required." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 w-[380px] h-[600px] glass-panel rounded-2xl border-emerald-500/10 shadow-2xl flex flex-col z-[100] animate-in slide-in-from-right-4 overflow-hidden">
      <div className="p-4 border-b border-white/5 flex items-center justify-between bg-black/40">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-emerald-500/10 text-emerald-500 rounded-xl flex items-center justify-center border border-emerald-500/20 relative">
            <Cpu size={20} className="animate-pulse" />
          </div>
          <div><h4 className="text-[11px] font-black text-white tracking-widest uppercase">Kernel_OS</h4><div className="flex items-center gap-1"><span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping" /><span className="text-[8px] text-zinc-500 font-black uppercase tracking-widest">Internal Sync</span></div></div>
        </div>
        <button onClick={onClose} className="p-2 text-zinc-600 hover:text-white transition-all"><X size={18} /></button>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide bg-black/20 font-medium">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[92%] px-4 py-3 rounded-2xl text-[11px] leading-relaxed ${msg.role === 'user' ? 'bg-emerald-500 text-black font-bold' : 'bg-white/5 text-zinc-300 border border-white/5'}`}>
              <div className="whitespace-pre-wrap">{msg.content || <Loader2 size={14} className="animate-spin" />}</div>
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSend} className="p-4 border-t border-white/5 bg-black/60 relative">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Decree internal manifest update..."
          className="w-full bg-white/5 border border-white/10 rounded-2xl py-3 pl-5 pr-12 text-[11px] text-white focus:outline-none focus:border-emerald-500/30 font-medium"
          disabled={isLoading}
        />
        <button type="submit" disabled={!input.trim() || isLoading} className="absolute right-6 top-1/2 -translate-y-1/2 text-emerald-500"><Zap size={20} /></button>
      </form>
    </div>
  );
};

export default ChatWindow;
