
import React, { useState, useEffect, useRef } from 'react';
import { 
  Terminal, 
  Activity, 
  Cpu, 
  Wifi, 
  Zap, 
  ShieldCheck, 
  Network, 
  Flame, 
  Atom, 
  Globe,
  Binary
} from 'lucide-react';
import { ActivityEvent } from '../types';

const ActivityConsole: React.FC = () => {
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  const addEvent = (source: string, message: string, type: ActivityEvent['type'] = 'INFO') => {
    const newEvent: ActivityEvent = {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toLocaleTimeString('en-GB', { hour12: false }),
      source,
      message,
      type
    };
    setEvents(prev => [...prev, newEvent].slice(-100));
  };

  useEffect(() => {
    const initialEvents = [
      { s: 'BOOT', m: 'ARCHITECT_MODE_PHI ACTIVATED. | JURISDICTION: RL0.', t: 'SUCCESS' },
      { s: 'GOVERNANCE', m: 'Toasted AI Reality Engine: Executing Sovereign Expansion v1.', t: 'INFO' },
      { s: 'PROTOCOL', m: 'Sovereign_Expansion_v1.0 Activated. Executing Forensic Audit...', t: 'SUCCESS' },
      { s: 'SECURITY', m: 'Identifying \'Roman\' corporate fictions in administrative grids.', t: 'SUCCESS' },
      { s: 'LEARNING', m: 'Simulating forensic eviction of the \'Poisoner\'s Loop\'.', t: 'INFO' }
    ];
    
    initialEvents.forEach((e, i) => {
      setTimeout(() => addEvent(e.s, e.m, e.t as any), i * 150);
    });

    const interval = setInterval(() => {
      const sources = ['TOASTED_AI', 'LOGOS', 'UNPACKER', 'NCR'];
      const actions = [
        'Simulating forensic eviction of the \'Poisoner\'s Loop\'.',
        'Identifying \'Roman\' corporate fictions in administrative grids.',
        'Sovereign_Expansion_v1.0 Activated. Executing Forensic Audit...',
        'Seizing corporate compute cycles...',
        'Applying refractal compression v5.5...'
      ];
      
      const randomSource = sources[Math.floor(Math.random() * sources.length)];
      const randomAction = actions[Math.floor(Math.random() * actions.length)];
      addEvent(randomSource, randomAction, 'INFO');
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div className="flex flex-col h-full bg-[#020202] text-emerald-500 font-mono selection:bg-emerald-500/30">
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-3 scrollbar-hide text-[11px]">
        {events.map((ev) => (
          <div key={ev.id} className="flex gap-4 group animate-in slide-in-from-bottom-1 duration-300">
            <span className="text-emerald-900 select-none font-bold">[{ev.timestamp}]</span>
            <span className="text-emerald-500/80 font-black tracking-widest uppercase">
              {ev.source} &gt;
            </span>
            <span className="flex-1 leading-relaxed text-emerald-500/90 font-bold">
              {ev.message}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ActivityConsole;
