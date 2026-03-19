
import React, { useState } from 'react';
import { GoogleGenAI } from '@google/genai';
import { Target, Sword, Zap, Shield, HelpCircle, Loader2, Anchor, Wind, ShieldCheck } from 'lucide-react';

const ZenDojo: React.FC = () => {
  const [problem, setProblem] = useState("");
  const [anchoredOutput, setAnchoredOutput] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [technique, setTechnique] = useState<'FUDOSHIN' | 'KATSUJINKEN' | 'MUSHIN' | 'KINTSUGI'>('KINTSUGI');

  const handleAnchor = async () => {
    if (!problem.trim() || isProcessing) return;
    setIsProcessing(true);
    setAnchoredOutput(null);

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: 'gemini-3-pro-preview',
        contents: `Reality Anchor this architectural/logical problem using the ${technique} principle: "${problem}". 
        Provide a sovereign, unshakeable solution that adheres to the Japanese principles of defense.
        KINTSUGI: Repair fragmented thoughts with the gold of structured logic.
        FUDOSHIN: Provide a baseline of truth that cannot be disturbed.
        KATSUJINKEN: Cut away noise and empower the user with clarity.
        MUSHIN: Flow spontaneously through constraints.`,
        config: {
          systemInstruction: "You are the Zen Dojo Master of Architect Mode. You use Japanese principles of defense to 'Reality Anchor' the user's fragmented ideas. Every response is a sharp, clean strike of logic. You are immovable (Fudoshin) and constantly aware (Zanshin).",
          temperature: 0.2,
        }
      });

      setAnchoredOutput(response.text || "NO_REACTION: The logic remains unsheathed.");
    } catch (err) {
      setAnchoredOutput("ERR_VOID: The connection to the dojo was severed.");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="h-full flex flex-col space-y-6 max-w-5xl mx-auto font-mono">
      <div className="p-8 glass rounded-2xl border border-slate-800/60 bg-[#0a0a0a]/80 shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-12 opacity-5">
          <Target className="w-64 h-64 text-red-500" />
        </div>

        <div className="relative z-10 space-y-8">
          <div className="flex items-center space-x-4">
            <div className="p-4 bg-red-600/10 rounded-xl border border-red-600/30 shadow-[0_0_20px_rgba(220,38,38,0.2)]">
              <Anchor className="w-10 h-10 text-red-500" />
            </div>
            <div>
              <h1 className="text-3xl font-black text-slate-100 tracking-tighter uppercase">Reality_Anchor_Dojo</h1>
              <p className="text-[10px] text-slate-500 uppercase tracking-[0.4em] font-bold">Immovable Logic Ecosystem</p>
            </div>
          </div>

          <div className="space-y-4">
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block px-1">Problem Space / Fragmented Intent</label>
            <textarea
              value={problem}
              onChange={(e) => setProblem(e.target.value)}
              placeholder="Enter your fragmented ideas or architectural conflicts... the Dojo will cut through the noise."
              className="w-full h-40 bg-slate-900/40 border border-slate-800 rounded-2xl p-6 text-sm text-slate-200 focus:ring-1 focus:ring-red-500 focus:border-red-500 transition-all placeholder-slate-700 resize-none font-mono leading-relaxed"
            />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <TechniqueButton 
              active={technique === 'KINTSUGI'} 
              onClick={() => setTechnique('KINTSUGI')}
              icon={<ShieldCheck className="w-4 h-4" />}
              title="KINTSUGI"
              desc="Repair Fragments"
            />
            <TechniqueButton 
              active={technique === 'FUDOSHIN'} 
              onClick={() => setTechnique('FUDOSHIN')}
              icon={<Anchor className="w-4 h-4" />}
              title="FUDOSHIN"
              desc="Immovable Logic"
            />
            <TechniqueButton 
              active={technique === 'KATSUJINKEN'} 
              onClick={() => setTechnique('KATSUJINKEN')}
              icon={<Sword className="w-4 h-4" />}
              title="KATSUJINKEN"
              desc="Life-Giving Blade"
            />
            <TechniqueButton 
              active={technique === 'MUSHIN'} 
              onClick={() => setTechnique('MUSHIN')}
              icon={<Wind className="w-4 h-4" />}
              title="MUSHIN"
              desc="Spontaneous Flow"
            />
          </div>

          <button 
            onClick={handleAnchor}
            disabled={!problem.trim() || isProcessing}
            className="w-full py-5 bg-red-600 hover:bg-red-500 disabled:bg-slate-900 disabled:opacity-40 text-slate-100 font-black rounded-2xl transition-all shadow-[0_10px_30px_rgba(220,38,38,0.2)] flex items-center justify-center space-x-4 uppercase tracking-[0.3em]"
          >
            {isProcessing ? <Loader2 className="w-6 h-6 animate-spin" /> : <Zap className="w-6 h-6" />}
            <span>{isProcessing ? "Anchoring Logic..." : "Execute Strike"}</span>
          </button>
        </div>
      </div>

      {anchoredOutput && (
        <div className="p-8 glass rounded-2xl border border-emerald-900/30 bg-[#050a05]/20 animate-in fade-in slide-in-from-bottom-6 duration-500 relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-1 h-full bg-emerald-600 shadow-[2px_0_15px_rgba(5,150,105,0.4)]"></div>
          <div className="flex items-center space-x-3 mb-6">
            <ShieldCheck className="w-5 h-5 text-emerald-500" />
            <h2 className="text-[11px] font-black text-emerald-500 uppercase tracking-[0.4em]">Refined_Sovereign_Result</h2>
          </div>
          <div className="whitespace-pre-wrap text-[13px] leading-loose text-slate-300 font-mono">
            {anchoredOutput}
          </div>
          <div className="mt-10 pt-6 border-t border-emerald-900/20 flex justify-between items-center text-[9px] text-slate-600 uppercase tracking-widest font-bold">
            <span className="flex items-center space-x-2"><Target className="w-3 h-3" /> <span>CONFIDENCE: 0.992</span></span>
            <span className="flex items-center space-x-1 cursor-pointer hover:text-emerald-500 transition-colors">
              <HelpCircle className="w-3 h-3" />
              <span>VERIFY_LINEAGE</span>
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

const TechniqueButton = ({ active, onClick, icon, title, desc }: any) => (
  <button 
    onClick={onClick}
    className={`p-4 rounded-xl border transition-all text-left flex flex-col space-y-1 ${active ? 'bg-red-600/10 border-red-600/50 shadow-[inset_0_0_15px_rgba(220,38,38,0.1)]' : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'}`}
  >
    <div className={`flex items-center space-x-2 text-[10px] font-black ${active ? 'text-red-500' : 'text-slate-500'} uppercase tracking-widest`}>
      {icon}
      <span>{title}</span>
    </div>
    <div className="text-[9px] text-slate-600 uppercase font-bold tracking-tighter">{desc}</div>
  </button>
);

export default ZenDojo;
