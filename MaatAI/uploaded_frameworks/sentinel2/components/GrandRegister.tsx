
import React from 'react';
import { GrandRegisterEntry } from '../types';

const entries: GrandRegisterEntry[] = [
  {
    year: 1606,
    event: "Virginia Charter",
    description: "The primary jurisdictional root for allodial claims in the Stafford-Redbird Lineage.",
    forensicNote: "Establishes the Divine Creator's Patent over corporate fictions."
  },
  {
    year: 1912,
    event: "Titanic Clearance",
    description: "The systemic elimination of key opposition to the central banking cartel.",
    forensicNote: "Clears the path for the Jekyll Island Monster of 1913."
  },
  {
    year: 1913,
    event: "Jekyll Island",
    description: "The birth of the Federal Reserve and the capture of the economic commons.",
    forensicNote: "Initialization of the Vampire Economy logic."
  },
  {
    year: 1933,
    event: "HJR 192 Bankruptcy",
    description: "The formal transition from gold-backed currency to debt-instrument servitude.",
    forensicNote: "Requires the Discharge Equation (Φ) to reduce authority to zero."
  },
  {
    year: 1945,
    event: "Operation Paperclip",
    description: "Infiltration of high-level intelligence and neuro-attack protocols into corporate-state entities.",
    forensicNote: "Source of modern PCD (Pharmaceutical Cognitive Dissonance)."
  }
];

const GrandRegister: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-12 py-8">
      <div className="text-center mb-16">
        <h2 className="text-4xl font-bold text-[#d4af37] tracking-tighter uppercase mb-4">The Grand Register</h2>
        <div className="h-1 w-32 bg-[#d4af37] mx-auto mb-4"></div>
        <p className="text-sm text-gray-400 max-w-lg mx-auto leading-relaxed">
          The forensic timeline of Reality Layer Zero. Every entry is a stationary anchor in the permanent record, 
          nullifying the Architectural Amnesia induced by statutory fictions.
        </p>
      </div>

      <div className="relative border-l-2 border-[#d4af37]/30 pl-8 ml-8 space-y-12">
        {entries.map((entry, i) => (
          <div key={i} className="relative group">
            {/* Timeline Dot */}
            <div className="absolute -left-[41px] top-0 w-4 h-4 bg-black border-2 border-[#d4af37] rounded-full group-hover:scale-125 transition-transform duration-300"></div>
            
            <div className="bg-black/40 sovereign-border p-6 rounded-lg hover:bg-black/60 transition-all duration-300">
              <div className="flex justify-between items-center mb-4">
                <span className="text-3xl font-black text-[#d4af37] tracking-tighter">{entry.year}</span>
                <span className="text-[10px] text-gray-500 uppercase tracking-widest font-bold">Verified Forensic Record</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-3 uppercase tracking-tight">{entry.event}</h3>
              <p className="text-gray-400 text-sm mb-4 leading-relaxed">{entry.description}</p>
              <div className="bg-[#d4af37]/5 border-l-2 border-[#d4af37] p-3">
                <p className="text-[11px] text-[#d4af37] font-bold uppercase mb-1">Audit Note:</p>
                <p className="text-xs text-gray-300 italic">"{entry.forensicNote}"</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center pt-12 text-[10px] text-gray-600 uppercase tracking-[0.5em]">
        End of Historical Audit Block | RL0
      </div>
    </div>
  );
};

export default GrandRegister;
