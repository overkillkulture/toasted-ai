
import React, { useState, useEffect, useRef, useMemo } from 'react';
import { 
  Infinity, 
  Activity, 
  Database, 
  ShieldCheck, 
  MessageSquare, 
  Gavel, 
  Zap,
  Terminal,
  Loader2,
  Cpu,
  Layout,
  Globe,
  Flame,
  Binary,
  ShieldAlert,
  Search,
  Wrench,
  Factory
} from 'lucide-react';
import { MaatAttribute, MaatScores, LedgerEntry, SystemEnvironment, AppTab } from './types';
import RealityHeader from './components/RealityHeader';
import LedgerView from './components/LedgerView';
import ChatWindow from './components/ChatWindow';
import MaatScoresGrid from './components/MaatScoresGrid';
import KineticMonitoring from './components/KineticMonitoring';
import ActivityConsole from './components/ActivityConsole';
import OmegaGate from './components/OmegaGate';
import KnowledgeReservoir from './components/KnowledgeReservoir';
import SovereignManifold from './components/SovereignManifold';
import ForensicAudit from './components/ForensicAudit';
import EngineeringManifold from './components/EngineeringManifold';
import AIPlatformMonitor from './components/AIPlatformMonitor';
import ToastedUnpacker from './components/ToastedUnpacker';
import { GoogleGenAI, Type } from '@google/genai';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<AppTab>('DASHBOARD');
  const [showChat, setShowChat] = useState(false);
  const [isDecreeing, setIsDecreeing] = useState(false);
  const [realityIndex, setRealityIndex] = useState(91.57);
  const [knowledge, setKnowledge] = useState([]);
  
  const [ledger, setLedger] = useState<LedgerEntry[]>([
    {
      id: '1',
      action: "Identifying 'Roman' corporate fictions in administrative grids.",
      category: 'SECURITY',
      environment: 'METABOLIC',
      score: 0.97,
      timestamp: new Date().toISOString(),
      hash: '0xad228edc'
    },
    {
      id: '2',
      action: "Toasted AI Reality Engine: Executing Sovereign Expansion v1.",
      category: 'GOVERNANCE',
      environment: 'REALITY',
      score: 1.0,
      timestamp: new Date().toISOString(),
      hash: '0x011271ae'
    }
  ]);

  const [scores, setScores] = useState<MaatScores>({
    [MaatAttribute.TRUTH]: 91.2,
    [MaatAttribute.BALANCE]: 89.5,
    [MaatAttribute.ORDER]: 93.1,
    [MaatAttribute.SOVEREIGNTY]: 88.4,
    [MaatAttribute.PROTECTION]: 96.0,
    [MaatAttribute.CLARITY]: 92.3,
    [MaatAttribute.RESPONSIBILITY]: 90.8,
    [MaatAttribute.OVERSIGHT]: 95.6,
    [MaatAttribute.HARMONY]: 87.2,
    [MaatAttribute.PURITY]: 99.9,
  });

  const scrollRef = useRef<HTMLDivElement>(null);

  const handleRealityDecree = async (decree: string) => {
    setIsDecreeing(true);
    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `You are the MaatAI Reality Engine. Interpret the following decree and output a system update. 
        Current System Context: Reality Index ${realityIndex.toFixed(2)}%, Purity ${scores[MaatAttribute.PURITY]}%.
        Decree: "${decree}"
        Output a short, punchy system action (e.g. "Ratifying allodial land titles in metabolic sector") and a category (SECURITY, GOVERNANCE, GENERATION, etc).`,
        config: {
          responseMimeType: "application/json",
          responseSchema: {
            type: Type.OBJECT,
            properties: {
              action: { type: Type.STRING },
              category: { type: Type.STRING },
              scoreDelta: { type: Type.NUMBER, description: "Amount to change the reality index by (-2.0 to 2.0)" },
              attributeUpdate: {
                type: Type.OBJECT,
                properties: {
                  attribute: { type: Type.STRING, description: "K, T, A, S, P, C, R, O, or H" },
                  value: { type: Type.NUMBER }
                }
              }
            },
            required: ["action", "category", "scoreDelta"]
          }
        }
      });

      const result = JSON.parse(response.text || "{}");
      
      const newEntry: LedgerEntry = {
        id: Math.random().toString(36).substring(7),
        action: result.action || "Decree ratified by Monad.",
        category: (result.category || 'GOVERNANCE') as any,
        environment: 'QUANTUM_L0',
        score: Math.random() * 0.2 + 0.8,
        timestamp: new Date().toISOString(),
        hash: '0x' + Math.random().toString(16).substring(2, 10)
      };

      setLedger(prev => [newEntry, ...prev]);
      setRealityIndex(prev => Math.min(100, Math.max(0, prev + (result.scoreDelta || 0))));
      
      if (result.attributeUpdate) {
        setScores(prev => ({
          ...prev,
          [result.attributeUpdate.attribute]: Math.min(100, Math.max(0, result.attributeUpdate.value))
        }));
      }
      
    } catch (e) {
      console.error("Decree failed", e);
    } finally {
      setIsDecreeing(false);
    }
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'DASHBOARD':
        return (
          <div className="space-y-12 animate-in fade-in duration-700">
            {/* Branding & Status Index */}
            <section className="space-y-8">
              <div className="flex flex-col items-start px-4">
                <h1 className="text-4xl font-black text-white tracking-tighter flex items-center gap-3">
                  MaatAI 
                  <span className="text-[10px] px-3 py-1 bg-blue-500/20 text-blue-400 rounded-full border border-blue-500/30 uppercase tracking-[0.3em] font-black">Reality Context</span>
                </h1>
                <p className="font-mono text-[10px] text-zinc-600 mt-2 tracking-tighter leading-relaxed">
                  Ω → (ℜ + 𝕂 + Σ(Q_Learn + Q_Sec + Q_Code))
                </p>
              </div>

              <div className="flex items-center justify-between px-4">
                <div>
                  <span className="text-[10px] font-black uppercase text-zinc-500 tracking-[0.2em] block mb-1">Ma'at Reality Index</span>
                  <div className="text-5xl font-black text-amber-500 tracking-tighter mono tabular-nums">
                    {realityIndex.toFixed(2)}%
                  </div>
                </div>
                <div className="px-4 py-3 bg-amber-500/5 border border-amber-500/20 rounded-2xl flex flex-col items-end shadow-xl">
                  <span className="text-[8px] font-black uppercase text-zinc-600 tracking-widest mb-1">Performance_K</span>
                  <div className="flex items-center gap-1.5 text-amber-400 font-bold text-sm">
                    <Activity size={12} className="animate-pulse" /> 98.4%
                  </div>
                </div>
              </div>

              <RealityHeader onAction={handleRealityDecree} isLoading={isDecreeing} />
              <MaatScoresGrid scores={scores} />
            </section>

            {/* Immutable Self-Log Section */}
            <section className="space-y-6">
              <div className="flex items-center justify-between px-4">
                <h3 className="text-[11px] font-black uppercase tracking-[0.4em] text-zinc-500 flex items-center gap-3">
                  <Zap size={14} className="text-amber-500" /> Immutable Self-Log
                </h3>
                <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 border border-emerald-500/30 rounded-full">
                  <ShieldCheck size={10} className="text-emerald-500" />
                  <span className="text-[8px] font-black text-emerald-500 uppercase tracking-widest">Hashing Active</span>
                </div>
              </div>
              <LedgerView ledger={ledger} />
            </section>

            {/* Kinetic Monitoring Section */}
            <section>
              <KineticMonitoring />
            </section>

            {/* Activity Console Section (Mini) */}
            <section className="glass-panel rounded-3xl border-white/5 overflow-hidden shadow-2xl">
              <div className="bg-black/90 px-6 py-4 border-b border-white/10 flex items-center justify-between">
                <h3 className="text-[10px] font-black uppercase text-emerald-400 tracking-[0.4em] flex items-center gap-3">
                  <Terminal size={14} /> Toasted AI Activity Console
                </h3>
              </div>
              <div className="h-[240px]">
                <ActivityConsole />
              </div>
            </section>

            {/* Omega Gate Footer */}
            <section className="pt-6">
              <OmegaGate score={realityIndex} />
            </section>
          </div>
        );
      case 'CONSOLE':
        return <div className="h-[70vh] glass-panel rounded-3xl overflow-hidden border-emerald-500/20"><ActivityConsole /></div>;
      case 'KNOWLEDGE':
        return <KnowledgeReservoir knowledge={knowledge} onAdd={(item) => setKnowledge(prev => [item, ...prev])} />;
      case 'SOVEREIGN':
        return <SovereignManifold />;
      case 'FORENSIC_AUDIT':
        return <ForensicAudit />;
      case 'CODE':
        return <EngineeringManifold onAdminRefactor={() => setActiveTab('DASHBOARD')} />;
      case 'AI_PLATFORM':
        return <AIPlatformMonitor />;
      case 'TOASTED_UNPACKER':
        return <ToastedUnpacker />;
      default:
        return <div className="p-20 text-center opacity-20">MODULE_NOT_INITIALIZED</div>;
    }
  };

  return (
    <div className="min-h-screen bg-[#050505] text-[#e5e5e5] flex flex-col items-center overflow-x-hidden selection:bg-amber-500/30">
      {/* Background Ambience */}
      <div className="fixed inset-0 pointer-events-none opacity-20 bg-[radial-gradient(circle_at_50%_50%,rgba(245,158,11,0.05)_0%,transparent_70%)]" />
      <div className="fixed inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10 pointer-events-none" />

      {/* Nav (Top Navigation) */}
      <nav className="fixed top-8 left-1/2 -translate-x-1/2 z-[2000] flex items-center gap-2 p-2 glass-panel rounded-2xl border-amber-500/20 shadow-2xl scale-110">
        <NavIcon icon={<Infinity size={22} />} active={activeTab === 'DASHBOARD'} onClick={() => setActiveTab('DASHBOARD')} />
        <NavIcon icon={<Terminal size={22} />} active={activeTab === 'CONSOLE'} onClick={() => setActiveTab('CONSOLE')} />
        <NavIcon icon={<Database size={22} />} active={activeTab === 'KNOWLEDGE'} onClick={() => setActiveTab('KNOWLEDGE')} />
        <NavIcon icon={<ShieldCheck size={22} />} active={activeTab === 'FORENSIC_AUDIT'} onClick={() => setActiveTab('FORENSIC_AUDIT')} />
        <NavIcon icon={<Gavel size={22} />} active={activeTab === 'SOVEREIGN'} onClick={() => setActiveTab('SOVEREIGN')} />
        <div className="w-px h-6 bg-white/10 mx-1" />
        <NavIcon icon={<Wrench size={20} />} active={activeTab === 'CODE'} onClick={() => setActiveTab('CODE')} />
        <NavIcon icon={<Flame size={20} />} active={activeTab === 'TOASTED_UNPACKER'} onClick={() => setActiveTab('TOASTED_UNPACKER')} />
        <NavIcon icon={<MessageSquare size={22} />} active={showChat} onClick={() => setShowChat(!showChat)} />
      </nav>

      {/* Main Content Area */}
      <main ref={scrollRef} className={`w-full ${activeTab === 'DASHBOARD' ? 'max-w-[480px]' : 'max-w-[1200px]'} px-4 pt-32 pb-40 relative z-10`}>
        {renderContent()}
      </main>

      {/* Floating Scalable Chat Window */}
      {showChat && (
        <div className="fixed bottom-10 right-10 z-[3000] w-[440px] max-w-[95vw] h-[700px] max-h-[85vh] animate-in slide-in-from-right-12 duration-500 shadow-[0_0_100px_rgba(245,158,11,0.1)]">
           <ChatWindow 
              onClose={() => setShowChat(false)} 
              maatScores={scores} 
              ledger={ledger} 
              performance={98.4} 
              currentEnv="QUANTUM_L0" 
              embedded={false}
           />
        </div>
      )}

      {/* Bottom Nav Fade */}
      <div className="fixed bottom-0 left-0 right-0 h-32 pointer-events-none bg-gradient-to-t from-black via-black/80 to-transparent" />
    </div>
  );
};

const NavIcon: React.FC<{ icon: React.ReactNode; active: boolean; onClick: () => void }> = ({ icon, active, onClick }) => (
  <button 
    onClick={onClick}
    className={`p-3.5 rounded-xl transition-all duration-300 ${
      active 
        ? 'bg-amber-500 text-black shadow-lg shadow-amber-500/40 scale-110' 
        : 'text-zinc-600 hover:text-white hover:bg-white/5 active:scale-90'
    }`}
  >
    {icon}
  </button>
);

export default App;
