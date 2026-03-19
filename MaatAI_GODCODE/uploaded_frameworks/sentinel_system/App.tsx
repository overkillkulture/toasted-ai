
import React, { useState, useEffect } from 'react';
import { 
  Terminal, 
  Binary, 
  FolderTree, 
  BookOpen, 
  ShieldAlert, 
  Cpu, 
  Activity,
  UserCheck,
  Zap,
  Target,
  Sword,
  Wind,
  Shield
} from 'lucide-react';
import { SystemModule } from './types';
import ChatInterface from './components/ChatInterface';
import MathEngine from './components/MathEngine';
import FileExplorer from './components/FileExplorer';
import LedgerView from './components/LedgerView';
import ManifestPanel from './components/ManifestPanel';
import BackSystem from './components/BackSystem';
import ZenDojo from './components/ZenDojo';

const App: React.FC = () => {
  const [activeModule, setActiveModule] = useState<SystemModule>(SystemModule.DOJO);
  const [fudoshinStability, setFudoshinStability] = useState(0.992);
  const [zanshinAlertness, setZanshinAlertness] = useState(0.941);
  const [statusMessage, setStatusMessage] = useState("FUDOSHIN: Unshakeable mind active.");

  useEffect(() => {
    const interval = setInterval(() => {
      setZanshinAlertness(prev => Math.max(0.85, Math.min(1.0, prev + (Math.random() - 0.5) * 0.01)));
      if (Math.random() > 0.9) {
        const triggers = ["ZANSHIN_RECON", "MUSHA_DORI", "KATSUJINKEN_PULSE", "GAMAN_THRESHOLD"];
        setStatusMessage(`${triggers[Math.floor(Math.random() * triggers.length)]}: Monitoring perimeter...`);
        setTimeout(() => setStatusMessage("FUDOSHIN: Unshakeable mind active."), 3000);
      }
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  const renderModule = () => {
    switch (activeModule) {
      case SystemModule.CHAT: return <ChatInterface />;
      case SystemModule.MATH: return <MathEngine />;
      case SystemModule.FILES: return <FileExplorer />;
      case SystemModule.LEDGER: return <LedgerView />;
      case SystemModule.MANIFEST: return <ManifestPanel />;
      case SystemModule.BACK_SYSTEM: return <BackSystem />;
      case SystemModule.DOJO: return <ZenDojo />;
      default: return <ZenDojo />;
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[#02040a] text-slate-200">
      {/* Sidebar - Imperial Indigo */}
      <nav className="w-16 md:w-64 border-r border-[#1e293b]/40 flex flex-col items-center py-4 space-y-8 glass z-20 shadow-[4px_0_24px_rgba(0,0,0,0.6)]">
        <div className="flex items-center space-x-2 px-4 mb-4">
          <div className="p-2 bg-red-600/10 rounded-lg border border-red-600/40 shadow-[0_0_15px_rgba(220,38,38,0.2)]">
            <Shield className="w-6 h-6 text-red-500" />
          </div>
          <span className="hidden md:block font-bold text-lg tracking-tighter text-slate-100 uppercase">Sentinel_V6</span>
        </div>

        <div className="flex-1 w-full flex flex-col space-y-1 px-2">
          <NavButton 
            icon={<Target className="w-5 h-5" />} 
            label="Zen Dojo" 
            active={activeModule === SystemModule.DOJO}
            onClick={() => setActiveModule(SystemModule.DOJO)}
          />
          <NavButton 
            icon={<Terminal className="w-5 h-5" />} 
            label="Front Terminal" 
            active={activeModule === SystemModule.CHAT}
            onClick={() => setActiveModule(SystemModule.CHAT)}
          />
          <NavButton 
            icon={<Sword className="w-5 h-5" />} 
            label="Math Blade" 
            active={activeModule === SystemModule.MATH}
            onClick={() => setActiveModule(SystemModule.MATH)}
          />
          <NavButton 
            icon={<FolderTree className="w-5 h-5" />} 
            label="Scroll Vault" 
            active={activeModule === SystemModule.FILES}
            onClick={() => setActiveModule(SystemModule.FILES)}
          />
          <NavButton 
            icon={<BookOpen className="w-5 h-5" />} 
            label="Audit Ledger" 
            active={activeModule === SystemModule.LEDGER}
            onClick={() => setActiveModule(SystemModule.LEDGER)}
          />
          <NavButton 
            icon={<UserCheck className="w-5 h-5" />} 
            label="Imperial Manifest" 
            active={activeModule === SystemModule.MANIFEST}
            onClick={() => setActiveModule(SystemModule.MANIFEST)}
          />
          <div className="pt-8 border-t border-slate-800/50 mt-4">
            <NavButton 
              icon={<ShieldAlert className="w-5 h-5 text-red-500" />} 
              label="Void Protocol" 
              active={activeModule === SystemModule.BACK_SYSTEM}
              onClick={() => setActiveModule(SystemModule.BACK_SYSTEM)}
              critical
            />
          </div>
        </div>

        <div className="hidden md:block w-full px-4 text-[10px] space-y-2 text-slate-600 font-mono">
          <div className="flex justify-between">
            <span>DYNASTY:</span>
            <span>CONSTANT_LINEAGE</span>
          </div>
          <div className="flex justify-between">
            <span>ZANSHIN:</span>
            <span className="text-red-500">{(zanshinAlertness * 100).toFixed(1)}%</span>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col relative bg-[radial-gradient(circle_at_top_right,rgba(30,41,59,0.1),transparent)]">
        {/* Header Stats */}
        <header className="h-16 border-b border-slate-800/50 flex items-center justify-between px-6 glass z-10">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-2">
              <Activity className="w-4 h-4 text-red-500" />
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">Fudoshin</span>
              <span className="text-xs font-mono text-red-400">STABLE</span>
            </div>
            <div className="flex items-center space-x-2">
              <Wind className="w-4 h-4 text-emerald-400" />
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">Mushin</span>
              <span className="text-xs font-mono text-emerald-400">FLOWING</span>
            </div>
            <div className="flex items-center space-x-2">
              <ShieldAlert className="w-4 h-4 text-slate-500" />
              <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-slate-500">Gaman</span>
              <span className="text-xs font-mono text-slate-400">ENDURING</span>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-[10px] font-mono text-slate-500 bg-slate-900/50 px-4 py-1.5 rounded-full border border-slate-800/50">
              {statusMessage}
            </div>
            <div className="w-2.5 h-2.5 rounded-full bg-red-600 shadow-[0_0_12px_rgba(220,38,38,0.8)]"></div>
          </div>
        </header>

        {/* Module Render */}
        <div className="flex-1 p-6 overflow-auto">
          {renderModule()}
        </div>

        {/* Footer */}
        <footer className="h-10 border-t border-slate-800/30 bg-black/40 flex items-center px-6 justify-between text-[10px] text-slate-600 font-mono">
          <div className="flex space-x-6">
            <span className="flex items-center space-x-1"><Sword className="w-3 h-3" /> <span>KATSUJINKEN: ACTIVE</span></span>
            <span className="opacity-30">|</span>
            <span>SYSTEM_SOVEREIGNTY: UNCOMPROMISED</span>
          </div>
          <div>TIMESTAMP: {new Date().toISOString().replace('T', ' ').slice(0, 19)}</div>
        </footer>
      </main>
    </div>
  );
};

interface NavButtonProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  critical?: boolean;
  onClick: () => void;
}

const NavButton: React.FC<NavButtonProps> = ({ icon, label, active, onClick, critical }) => (
  <button 
    onClick={onClick}
    className={`
      flex items-center w-full px-3 py-3 rounded-md transition-all duration-300 group relative
      ${active ? 'bg-slate-800/40 text-slate-100 border border-slate-700/50' : 'text-slate-500 hover:text-slate-300 hover:bg-slate-900/20'}
      ${critical && !active ? 'hover:bg-red-950/20' : ''}
    `}
  >
    {active && <div className="absolute left-0 top-1 bottom-1 w-1 bg-red-600 rounded-full shadow-[2px_0_10px_rgba(220,38,38,0.5)]"></div>}
    <div className={`transition-transform duration-300 group-hover:scale-110 ${active ? 'text-red-500' : ''}`}>
      {icon}
    </div>
    <span className="ml-4 hidden md:block font-bold text-[11px] uppercase tracking-[0.15em] whitespace-nowrap overflow-hidden text-ellipsis">
      {label}
    </span>
  </button>
);

export default App;
