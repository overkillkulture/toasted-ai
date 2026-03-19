
import React from 'react';
import { ExternalLink, Globe } from 'lucide-react';

interface GroundingResultsProps {
  links: any[];
}

const GroundingResults: React.FC<GroundingResultsProps> = ({ links }) => {
  if (!links || links.length === 0) return null;

  // Extract URLs from grounding chunks as per rules
  // The structure returned by the API is typically { web: { uri: string, title: string } }
  return (
    <div className="mt-4 pt-4 border-t border-white/5">
      <h4 className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-3 flex items-center gap-2">
        <Globe size={12} /> Informing Sources
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {links.map((chunk, index) => {
          const web = chunk.web;
          if (!web) return null;
          
          return (
            <a 
              key={index}
              href={web.uri}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-between p-3 bg-white/5 hover:bg-white/10 border border-white/5 hover:border-purple-500/30 rounded-lg transition-all group"
            >
              <div className="flex-1 min-w-0 pr-3">
                <div className="text-[10px] text-purple-400 font-bold uppercase truncate">
                  Source {index + 1}
                </div>
                <div className="text-xs text-zinc-300 truncate group-hover:text-white">
                  {web.title || web.uri}
                </div>
              </div>
              <ExternalLink size={14} className="text-zinc-600 group-hover:text-purple-400" />
            </a>
          );
        })}
      </div>
    </div>
  );
};

export default GroundingResults;
