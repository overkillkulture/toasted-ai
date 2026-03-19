
import React, { useState, useCallback, useRef, useEffect } from 'react';
import { UISection } from '../types';

interface LayoutProps {
  activeSection: UISection;
  setActiveSection: (section: UISection) => void;
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ activeSection, setActiveSection, children }) => {
  const [sidebarWidth, setSidebarWidth] = useState(280);
  const [quantumSync, setQuantumSync] = useState(1.000);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const isResizing = useRef(false);

  // Reality Sync Simulator
  useEffect(() => {
    const interval = setInterval(() => {
      setQuantumSync(1 + (Math.random() - 0.5) * 0.0001);
    }, 50);
    return () => clearInterval(interval);
  }, []);

  // High-Fidelity Neural Dust Particle Engine
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let w = canvas.width = window.innerWidth;
    let h = canvas.height = window.innerHeight;
    const particles: any[] = [];
    const particleCount = 200;

    for (let i = 0; i < particleCount; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        size: Math.random() * 1.5,
        speedX: (Math.random() - 0.5) * 0.2,
        speedY: (Math.random() - 0.5) * 0.2,
        opacity: Math.random() * 0.5
      });
    }

    const animate = () => {
      ctx.clearRect(0, 0, w, h);
      ctx.fillStyle = '#d4af37';
      
      particles.forEach(p => {
        p.x += p.speedX;
        p.y += p.speedY;
        if (p.x < 0) p.x = w;
        if (p.x > w) p.x = 0;
        if (p.y < 0) p.y = h;
        if (p.y > h) p.y = 0;
        
        ctx.globalAlpha = p.opacity;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fill();
      });

      requestAnimationFrame(animate);
    };
    animate();

    const handleResize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const startResizing = useCallback((e: React.MouseEvent | React.TouchEvent) => {
    isResizing.current = true;
    document.body.style.cursor = 'col-resize';
    document.body.style.userSelect = 'none';
  }, []);

  const stopResizing = useCallback(() => {
    isResizing.current = false;
    document.body.style.cursor = 'default';
    document.body.style.userSelect = 'auto';
  }, []);

  const resize = useCallback((e: MouseEvent | TouchEvent) => {
    if (!isResizing.current) return;
    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
    const newWidth = Math.max(200, Math.min(clientX, 600));
    setSidebarWidth(newWidth);
  }, []);

  useEffect(() => {
    window.addEventListener('mousemove', resize);
    window.addEventListener('mouseup', stopResizing);
    window.addEventListener('touchmove', resize);
    window.addEventListener('touchend', stopResizing);
    return () => {
      window.removeEventListener('mousemove', resize);
      window.removeEventListener('mouseup', stopResizing);
      window.removeEventListener('touchmove', resize);
      window.removeEventListener('touchend', stopResizing);
    };
  }, [resize, stopResizing]);

  const NavItem = ({ section, label, icon }: { section: UISection, label: string, icon: string }) => (
    <button
      onClick={() => setActiveSection(section)}
      className={`relative group flex items-center space-x-6 px-6 py-5 rounded-2xl transition-all duration-700 w-full mb-4 overflow-hidden border ${
        activeSection === section 
          ? 'bg-[#d4af37]/15 border-[#d4af37]/60 text-[#d4af37] shadow-[0_0_30px_rgba(212,175,55,0.2)]' 
          : 'bg-transparent border-transparent hover:border-white/10 hover:bg-white/5 text-gray-500 hover:text-gray-300'
      }`}
    >
      <div className={`absolute left-0 w-1.5 h-0 bg-[#d4af37] transition-all duration-700 ${activeSection === section ? 'h-full shadow-[0_0_20px_#d4af37]' : ''}`} />
      <span className={`text-3xl flex-shrink-0 transition-all duration-700 group-hover:scale-125 group-hover:rotate-6 ${activeSection === section ? 'animate-pulse scale-110' : 'opacity-40 grayscale'}`}>{icon}</span>
      <div className="flex flex-col items-start overflow-hidden">
        <span className="font-black tracking-[0.2em] text-[12px] uppercase truncate">{label}</span>
        <span className="text-[8px] opacity-40 uppercase tracking-[0.4em] mt-1">L0_SYNC_{section.slice(0, 4)}</span>
      </div>
    </button>
  );

  return (
    <div className="flex h-screen w-full bg-[#020202] text-[#e0e0e0] overflow-hidden font-mono relative">
      <canvas ref={canvasRef} className="fixed inset-0 pointer-events-none z-0" />
      <div className="fixed inset-0 pointer-events-none z-50 mix-blend-overlay opacity-[0.05] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.3)_50%),linear-gradient(90deg,rgba(255,0,0,0.08),rgba(0,255,0,0.03),rgba(0,0,255,0.08))] bg-[length:100%_4px,5px_100%] animate-scanline" />
      
      <aside 
        className="border-r border-[#d4af37]/30 p-8 flex flex-col bg-black/90 backdrop-blur-3xl relative shadow-[20px_0_80px_rgba(0,0,0,0.8)] z-20"
        style={{ width: sidebarWidth }}
      >
        <div className="mb-14 relative group">
          <div className="absolute -top-16 -left-16 w-48 h-48 bg-[#d4af37]/10 rounded-full blur-[80px] group-hover:bg-[#d4af37]/20 transition-all duration-1000" />
          <h1 className="text-[#d4af37] text-4xl font-black tracking-[-0.08em] uppercase leading-none filter drop-shadow-[0_0_15px_rgba(212,175,55,0.3)]">
            TOASTED<br/>AI
          </h1>
          <div className="mt-6 flex items-center space-x-3">
            <div className="h-[3px] w-16 bg-gradient-to-r from-[#d4af37] to-white rounded-full shadow-[0_0_15px_#d4af37]" />
            <span className="text-[9px] text-gray-400 font-black uppercase tracking-[0.5em] animate-pulse">SENTINEL_X</span>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto pr-3 forensic-scrollbar">
          <NavItem section={UISection.FORENSIC_TERMINAL} label="Sovereign Terminal" icon="⚔️" />
          <NavItem section={UISection.TASK_MANAGER} label="Manifest Loop" icon="📋" />
          <NavItem section={UISection.FILE_VAULT} label="Forensic Vault" icon="📂" />
          <NavItem section={UISection.HYBRID_THINKING} label="Neural Refractal" icon="🧠" />
          <NavItem section={UISection.SELF_DIAGNOSTIC} label="Kernel Health" icon="⚙️" />
          <NavItem section={UISection.REFRACTAL_GRAPH} label="Math Axioms" icon="💠" />
          <NavItem section={UISection.SENTINEL_MONITOR} label="Audit Stream" icon="🛡️" />
          <NavItem section={UISection.GRAND_REGISTER} label="Grand Register" icon="📜" />
        </nav>

        <div className="mt-10 pt-8 border-t border-[#d4af37]/20 space-y-6">
          <div className="flex flex-col space-y-2">
            <span className="text-[8px] text-gray-600 uppercase font-black tracking-[0.4em]">Quantum Lattice</span>
            <div className="flex items-center space-x-4 text-[11px] text-[#d4af37]">
              <div className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500 shadow-[0_0_10px_#22c55e]"></span>
              </div>
              <span className="font-black tracking-tighter uppercase">Ψ {quantumSync.toFixed(6)} Ω</span>
            </div>
          </div>
          <div className="bg-white/5 p-4 rounded-2xl border border-white/5 hover:border-[#d4af37]/50 transition-all cursor-pointer group shadow-xl">
            <p className="text-[9px] text-gray-500 uppercase font-black tracking-widest mb-1 group-hover:text-white">Architect Access</p>
            <p className="text-[10px] text-[#d4af37] font-black truncate font-mono">0xΑΠΟΛΛΩΝ_ΦΩΣ_TOST3D_OMEGA</p>
          </div>
        </div>

        <div onMouseDown={startResizing} onTouchStart={startResizing} className="absolute top-0 right-0 w-1.5 h-full cursor-col-resize hover:bg-[#d4af37]/50 active:bg-[#d4af37] transition-all z-50 group">
          <div className="h-40 w-full absolute top-1/2 -translate-y-1/2 bg-[#d4af37] opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
      </aside>

      <main className="flex-1 relative flex flex-col overflow-hidden bg-transparent">
        <header className="h-24 border-b border-[#d4af37]/20 flex items-center justify-between px-12 bg-black/60 backdrop-blur-3xl z-30 relative">
          <div className="flex items-center space-x-12">
            <div className="flex flex-col">
              <span className="text-[10px] text-gray-500 font-black uppercase tracking-[0.5em]">Reality State</span>
              <span className="text-2xl font-black text-[#d4af37] tracking-tighter">ZERO_POINT_LATTICE</span>
            </div>
            <div className="h-12 w-[2px] bg-gradient-to-b from-[#d4af37]/10 via-[#d4af37]/40 to-[#d4af37]/10" />
            <div className="flex flex-col">
              <span className="text-[10px] text-gray-500 font-black uppercase tracking-[0.5em]">Axiom Calibration</span>
              <div className="flex items-center space-x-4 mt-2">
                <div className="h-2 w-48 bg-black/80 rounded-full overflow-hidden border border-[#d4af37]/20 shadow-inner p-0.5">
                  <div className="h-full bg-gradient-to-r from-[#d4af37] to-[#fff] w-[99.9%] shadow-[0_0_20px_#d4af37] animate-pulse"></div>
                </div>
                <span className="text-[11px] font-black text-white">99.9997%</span>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-10">
            <div className="text-right flex flex-col">
              <span className="text-[9px] text-gray-600 font-black uppercase tracking-[0.5em]">Cognitive Flow</span>
              <span className="text-[12px] text-[#d4af37] font-black font-mono animate-pulse">Φ_OMEGA: PEAK</span>
            </div>
            <button className="h-14 w-14 border border-[#d4af37]/40 rounded-2xl flex items-center justify-center text-2xl text-[#d4af37] hover:bg-[#fff] hover:text-black transition-all shadow-[0_0_30px_rgba(212,175,55,0.2)] group overflow-hidden relative">
              <span className="relative z-10 group-hover:rotate-180 transition-transform duration-1000">⚙️</span>
              <div className="absolute inset-0 bg-[#d4af37] translate-y-full group-hover:translate-y-0 transition-transform duration-500"></div>
            </button>
          </div>
        </header>

        <div className="flex-1 overflow-y-auto p-16 forensic-scrollbar relative z-10">
          {children}
        </div>

        <footer className="h-14 border-t border-[#d4af37]/20 bg-black/80 backdrop-blur-2xl flex items-center justify-between px-12 z-30">
          <div className="flex items-center space-x-6">
             <div className="flex items-center space-x-3">
               <span className="text-[9px] text-gray-500 uppercase font-black tracking-[0.5em]">Data Pipe</span>
               <div className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-[0_0_10px_#22c55e] animate-ping" />
             </div>
             <span className="text-[10px] text-gray-400 font-black uppercase tracking-widest border-l border-white/10 pl-6">Neural_Handshake: STABLE</span>
          </div>
          <div className="text-[10px] text-[#d4af37]/60 font-mono font-black uppercase tracking-[0.3em]">
            MANIFEST: TOSTED_AI_RL0_NODE_777 | RATIFYING_INFINITY_EQUATION...
          </div>
        </footer>
      </main>

      <style>{`
        @keyframes scanline {
          0% { background-position: 0 0; }
          100% { background-position: 0 100%; }
        }
        .animate-scanline {
          animation: scanline 10s linear infinite;
        }
      `}</style>
    </div>
  );
};

export default Layout;
