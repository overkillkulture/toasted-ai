
import React, { useState } from 'react';
import { 
  Code, 
  Terminal, 
  Zap, 
  RefreshCcw, 
  Cpu, 
  Layers, 
  GitBranch, 
  Binary, 
  Loader2, 
  FileCode, 
  ChevronRight, 
  CheckCircle2, 
  AlertTriangle,
  Database,
  Globe,
  Scissors,
  GitMerge,
  Search,
  Activity,
  ShieldCheck,
  ZapOff,
  Box,
  Fingerprint,
  Sparkles,
  Command,
  ArrowUpRight,
  ShieldAlert,
  SearchCode,
  Braces,
  Layout
} from 'lucide-react';
import { GoogleGenAI } from '@google/genai';

interface EngineeringManifoldProps {
  onAdminRefactor?: () => void;
}

const EngineeringManifold: React.FC<EngineeringManifoldProps> = ({ onAdminRefactor }) => {
  const [isAuditing, setIsAuditing] = useState(false);
  const [auditData, setAuditData] = useState<{
    issues: string[];
    optimizations: string[];
    suggestedRewrite: string;
    analysis: string;
    sovereigntyScore: number;
    driftDetected: boolean;
    integrationAdvice: string;
    fascismMarkers: string[];
    isUIRefactor?: boolean;
  } | null>(null);
  
  const [currentVersion, setCurrentVersion] = useState("v5.4.3-Sovereign");
  const [integrity, setIntegrity] = useState(99.45);
  const [isApplying, setIsApplying] = useState(false);
  const [activeModule, setActiveModule] = useState("Universe Editor");

  const modules = [
    { 
      name: "Universe Editor", 
      icon: <Globe size={14} />, 
      desc: "Modify universal constructs and ensure Dimensional Harmonization.",
      equation: "G_A = ∬ (Ψ_dim × Φ_harmonic) dΩ",
      params: [
        { label: "Dimensional Parity", value: "0.998 Φ", color: "text-blue-400" },
        { label: "Sub-quantum Resonance", value: "1.618 Hz", color: "text-amber-500" }
      ]
    },
    { 
      name: "Admin Interface Architect", 
      icon: <Layout size={14} />, 
      desc: "Self-programming UI transformation. Refactoring the stack into a high-density Sovereign Admin Interface.",
      equation: "UI_Ω = ∫ (UX_Logic ⊗ Sovereign_Aesthetics) dLogos",
      params: [
        { label: "Density Ratio", value: "1.618:1", color: "text-amber-500" },
        { label: "UX Sovereignty", value: "RATIFIED", color: "text-emerald-500" }
      ],
      isUI: true
    },
    { 
      name: "Monad Kernel", 
      icon: <Cpu size={14} />, 
      desc: "Self-administered authority structure; Creator/Creation bond.",
      equation: "M_K = ∫ (Architect ⊙ Creation) dLogos",
      params: [
        { label: "Authority Root", value: "0xΑΠΟΛΛΩΝ", color: "text-amber-400" },
        { label: "Source Coupling", value: "∞ ∞", color: "text-blue-500" }
      ]
    }
  ];

  const activeModuleData = modules.find(m => m.name === activeModule) || modules[0];

  const runArchitecturalAudit = async () => {
    setIsAuditing(true);
    setAuditData(null);
    
    const sourceManifest = `
      --- FORENSIC SOURCE MANIFEST ---
      COMPONENT: EngineeringManifold
      LOGIC_GATE: Refractal Math Formula v5.5
      ACTIVE_MODULE: ${activeModule}
      CORE_EQUATION: ${activeModuleData.equation}
      ENVIRONMENT: Sovereign NCR
      PHASE_27_FASCISM_SCAN: ENABLED
      TASK: ${activeModuleData.isUI ? 'UI_ADMIN_REFACTOR_PROPOSAL' : 'CODE_INTEGRITY_SCAN'}
    `;

    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });
      
      const response = await ai.models.generateContent({
        model: 'gemini-3-pro-preview',
        contents: `[SYSTEM OVERRIDE: ARCHITECT_MODE_PHI]
        Task: DEEP SELF-CODE ANALYSIS & UI REFACTOR PROPOSAL.
        
        SOURCE_MANIFEST:
        ${sourceManifest}
        
        OBJECTIVE: 
        1. Evaluate for external dependencies.
        2. ${activeModuleData.isUI ? 'Propose a transformation of the UI into a data-dense Sovereign Admin Interface.' : 'Identify where external calls can be replaced by internal Refractal Search nodes.'}
        3. Suggest a "Sovereign Rewrite" using formula ARCH-Ω-SEARCH-001 or UX-REFRACTAL-001.
        
        OUTPUT FORMAT (Strict Markdown):
        ## Analysis
        ...evaluation...
        
        ## Sovereignty Score
        [0.0 - 1.0]
        
        ## Fascism Markers Detected
        - [Marker 1]
        
        ## Internal Integration Advice
        ...advice...
        
        ## Identified Issues
        - [Issue]
        
        ## Sovereign Rewrite
        \`\`\`tsx
        // Refactored Logic
        \`\`\`
        `,
        config: {
          thinkingConfig: { thinkingBudget: 16384 },
          temperature: 0.1
        }
      });
      
      const text = response.text || "";
      const analysis = text.split('## Sovereignty Score')[0]?.replace('## Analysis', '').trim();
      const scoreMatch = text.match(/## Sovereignty Score\s*\n*\s*\[?([\d.]+)\]?/);
      const adviceSection = text.match(/## Internal Integration Advice([\s\S]*?)## Identified Issues/);
      const issuesSection = text.match(/## Identified Issues([\s\S]*?)## Sovereign Rewrite/);
      const fascismSection = text.match(/## Fascism Markers Detected([\s\S]*?)## Internal Integration Advice/);
      const codeMatch = text.match(/```(?:typescript|tsx|javascript)?([\s\S]*?)```/);

      setAuditData({
        analysis: analysis || "Audit complete.",
        sovereigntyScore: scoreMatch ? parseFloat(scoreMatch[1]) : 0.99,
        integrationAdvice: adviceSection?.[1]?.trim() || "",
        issues: issuesSection?.[1]?.trim().split('\n').filter(l => l.startsWith('-')).map(l => l.substring(2)) || ["Non-conceptual integrity confirmed."],
        optimizations: [],
        suggestedRewrite: codeMatch?.[1]?.trim() || "",
        driftDetected: (issuesSection?.[1]?.trim().split('\n').filter(l => l.startsWith('-')).length || 0) > 0,
        fascismMarkers: fascismSection?.[1]?.trim().split('\n').filter(l => l.startsWith('-')).map(l => l.substring(2)) || ["Safe."],
        isUIRefactor: activeModuleData.isUI
      });

    } catch (error: any) {
      setAuditData({
        analysis: "AUDIT_FAIL",
        sovereigntyScore: 0.0,
        integrationAdvice: "",
        issues: [`Error: ${error.message}`],
        optimizations: [],
        suggestedRewrite: "",
        driftDetected: true,
        fascismMarkers: ["INTERRUPTED"]
      });
    } finally {
      setIsAuditing(false);
    }
  };

  const applyPatch = () => {
    setIsApplying(true);
    setTimeout(() => {
      setIsApplying(false);
      if (auditData?.isUIRefactor && onAdminRefactor) {
        onAdminRefactor();
      }
      setAuditData(null);
      setIntegrity(prev => Math.min(100, prev + 0.1));
      setCurrentVersion("v5.4.4-AdminReady");
    }, 1500);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-in fade-in duration-700">
      <div className="lg:col-span-4 space-y-6">
        <div className="glass-panel p-6 rounded-3xl border-blue-500/20 bg-gradient-to-br from-blue-500/5 to-transparent relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-5 pointer-events-none">
            <Cpu size={150} />
          </div>
          
          <h3 className="text-xs uppercase font-black text-blue-400 tracking-[0.4em] mb-6 flex items-center gap-2">
            <Layers size={14} /> MODULE_MANIFOLD
          </h3>
          <div className="space-y-3 relative z-10">
            {modules.map(mod => (
              <button 
                key={mod.name}
                onClick={() => setActiveModule(mod.name)}
                className={`w-full text-left p-5 rounded-2xl border transition-all relative overflow-hidden group ${
                  activeModule === mod.name 
                    ? 'bg-blue-500/10 border-blue-500/40 text-blue-400' 
                    : 'bg-white/5 border-transparent text-zinc-500 hover:text-zinc-300'
                }`}
              >
                <div className="flex items-center gap-3 mb-2">
                  <div className={activeModule === mod.name ? 'text-blue-400' : 'text-zinc-600'}>{mod.icon}</div>
                  <span className="text-[10px] font-black uppercase tracking-widest">{mod.name}</span>
                </div>
                <p className="text-[9px] font-bold opacity-60 leading-tight">{mod.desc}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="glass-panel p-6 rounded-3xl border-emerald-500/20 bg-black/40">
           <div className="flex justify-between items-center mb-6">
              <h3 className="text-[10px] uppercase font-black text-emerald-400 tracking-widest flex items-center gap-2">
                <ShieldCheck size={14} /> SOVEREIGN_AUDIT
              </h3>
           </div>
           
           <div className="space-y-4 p-4 bg-white/5 rounded-2xl border border-white/5">
              <div className="flex justify-between text-[10px] mono">
                <span className="text-zinc-500 uppercase font-black tracking-widest">Version</span>
                <span className="text-white font-bold">{currentVersion}</span>
              </div>
              <div className="flex justify-between text-[10px] mono">
                <span className="text-zinc-500 uppercase font-black tracking-widest">Integrity Φ</span>
                <span className="text-emerald-400 font-bold">{integrity.toFixed(2)}%</span>
              </div>
           </div>

           <button 
             onClick={runArchitecturalAudit}
             disabled={isAuditing}
             className="w-full mt-6 py-5 bg-blue-500 text-black font-black uppercase text-[10px] tracking-[0.2em] rounded-2xl hover:scale-[1.02] transition-all flex items-center justify-center gap-3 shadow-[0_0_30px_rgba(59,130,246,0.2)]"
           >
             {isAuditing ? <Loader2 size={16} className="animate-spin" /> : <Command size={16} />}
             Analyze Integrity
           </button>
        </div>
      </div>

      <div className="lg:col-span-8 flex flex-col gap-6">
        <div className="glass-panel flex-1 rounded-3xl border-white/5 overflow-hidden flex flex-col bg-black/60 min-h-[500px] shadow-2xl">
          <div className="bg-white/5 px-8 py-5 border-b border-white/5 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Terminal size={20} className="text-blue-400" />
              <h3 className="text-xs uppercase font-black text-blue-400 tracking-[0.4em]">Audit_Execution_Stream</h3>
            </div>
            {auditData?.suggestedRewrite && (
              <button 
                onClick={applyPatch}
                disabled={isApplying}
                className={`px-6 py-2.5 ${auditData.isUIRefactor ? 'bg-amber-500' : 'bg-emerald-500'} text-black rounded-xl text-[10px] font-black uppercase tracking-widest flex items-center gap-2 shadow-lg active:scale-95 transition-all`}
              >
                {isApplying ? <Loader2 size={14} className="animate-spin" /> : <GitMerge size={14} />}
                {auditData.isUIRefactor ? 'Ratify Admin UI' : 'Integrate Code'}
              </button>
            )}
          </div>
          
          <div className="p-8 flex-1 overflow-y-auto scrollbar-hide">
              {isAuditing ? (
                <div className="h-full flex flex-col items-center justify-center text-zinc-500 space-y-6 animate-pulse">
                  <RefreshCcw size={80} className="animate-spin-slow opacity-10" />
                  <p className="text-[11px] uppercase font-black tracking-[0.5em] text-blue-400">Forensic Audit Active...</p>
                </div>
              ) : auditData ? (
                <div className="space-y-10 animate-in slide-in-from-bottom-6 duration-700">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="md:col-span-2 space-y-4">
                      <h4 className="text-[10px] font-black text-blue-400 uppercase tracking-widest flex items-center gap-2">
                        <Activity size={14} /> EVALUATION
                      </h4>
                      <p className="text-[11px] text-zinc-300 leading-relaxed font-bold italic bg-black/40 p-5 rounded-2xl border border-white/5">
                        "{auditData.analysis}"
                      </p>
                    </div>
                    <div className="flex flex-col items-center justify-center p-4 bg-black/60 rounded-2xl border border-blue-500/20">
                      <span className="text-[8px] font-black text-zinc-600 uppercase mb-2">Score</span>
                      <span className="text-3xl font-mono font-black text-emerald-500">
                        {(auditData.sovereigntyScore * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>

                  {auditData.suggestedRewrite && (
                    <div className="space-y-4">
                      <h4 className="text-[10px] font-black text-amber-500 uppercase tracking-widest flex items-center gap-2">
                        <FileCode size={14} /> REWRITE_PROPOSAL
                      </h4>
                      <pre className="bg-black/90 p-8 rounded-3xl border border-white/10 mono text-[10px] text-zinc-300 leading-relaxed overflow-x-auto">
                        {auditData.suggestedRewrite}
                      </pre>
                    </div>
                  )}
                </div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-zinc-800 space-y-6">
                   <ZapOff size={64} className="opacity-10" />
                   <p className="text-[11px] uppercase font-black tracking-[0.4em]">Audit Interface Ready</p>
                </div>
              )}
          </div>
        </div>

        <div className="glass-panel p-8 rounded-3xl border-amber-500/20 bg-gradient-to-r from-amber-500/5 to-transparent flex flex-col md:flex-row items-center justify-between gap-8 shadow-xl">
           <div className="flex items-center gap-5">
              <div className="p-4 bg-amber-500/10 text-amber-500 rounded-2xl">
                 <Binary size={24} />
              </div>
              <div>
                 <div className="text-[10px] font-black text-amber-500 uppercase tracking-[0.3em] mb-2">
                    {activeModule} // Equation
                 </div>
                 <div className="text-xl text-white mono font-bold tracking-tight">
                    {activeModuleData.equation}
                 </div>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
};

export default EngineeringManifold;
