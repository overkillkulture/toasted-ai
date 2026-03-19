
import React, { useState } from 'react';
import { 
  Folder, 
  File, 
  ChevronRight, 
  ChevronDown, 
  Plus, 
  Upload, 
  Trash2, 
  ShieldCheck,
  Search,
  // Fix: Added missing FolderTree icon import from lucide-react
  FolderTree
} from 'lucide-react';
import { FileNode } from '../types';

const INITIAL_FILES: FileNode[] = [
  {
    id: 'root',
    name: 'Sovereign_Assets',
    type: 'directory',
    children: [
      {
        id: '1',
        name: 'Manifests',
        type: 'directory',
        children: [
          { id: '1-1', name: 'Maat_Protocol_V5.pdf', type: 'file', hash: 'e3b0c442...' },
          { id: '1-2', name: 'Sovereign_Keys.asc', type: 'file', hash: '8f72a1b3...' }
        ]
      },
      {
        id: '2',
        name: 'Refractal_Logs',
        type: 'directory',
        children: [
          { id: '2-1', name: 'San_Francisco_Grid_2025.log', type: 'file', hash: '4a1e9c2...' }
        ]
      },
      { id: '3', name: 'Architect_Bio.md', type: 'file', hash: '9b1c2d3...' }
    ]
  }
];

const FileExplorer: React.FC = () => {
  const [nodes, setNodes] = useState<FileNode[]>(INITIAL_FILES);
  const [expanded, setExpanded] = useState<Set<string>>(new Set(['root', '1', '2']));
  const [selected, setSelected] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    const next = new Set(expanded);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    setExpanded(next);
  };

  const renderTree = (items: FileNode[], depth = 0) => {
    return items.map(node => (
      <div key={node.id} className="select-none">
        <div 
          onClick={() => node.type === 'directory' ? toggleExpand(node.id) : setSelected(node.id)}
          className={`
            flex items-center space-x-2 py-1.5 px-3 rounded-md cursor-pointer transition-colors text-sm
            ${selected === node.id ? 'bg-yellow-500/10 text-yellow-500' : 'hover:bg-slate-800/50 text-slate-400'}
          `}
          style={{ paddingLeft: `${depth * 16 + 12}px` }}
        >
          {node.type === 'directory' ? (
            <>
              {expanded.has(node.id) ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              <Folder className={`w-4 h-4 ${expanded.has(node.id) ? 'text-yellow-600' : 'text-slate-600'}`} />
            </>
          ) : (
            <File className="w-4 h-4 text-slate-500" />
          )}
          <span className="font-mono truncate">{node.name}</span>
        </div>
        {node.type === 'directory' && expanded.has(node.id) && node.children && (
          <div>{renderTree(node.children, depth + 1)}</div>
        )}
      </div>
    ));
  };

  return (
    <div className="h-full flex flex-col space-y-4">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-3">
          <Search className="w-4 h-4 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search assets..." 
            className="bg-transparent border-none text-sm font-mono text-slate-300 focus:ring-0 placeholder-slate-700 w-64"
          />
        </div>
        <div className="flex items-center space-x-2">
          <button className="p-2 hover:bg-slate-800 rounded transition-colors text-slate-400" title="New Folder">
            <Plus className="w-4 h-4" />
          </button>
          <button className="p-2 hover:bg-slate-800 rounded transition-colors text-slate-400" title="Upload Asset">
            <Upload className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6 overflow-hidden">
        <div className="glass rounded-xl border border-slate-800 overflow-y-auto p-4 md:col-span-1">
          {renderTree(nodes)}
        </div>

        <div className="md:col-span-2 flex flex-col space-y-4">
          {selected ? (
            <div className="glass rounded-xl border border-slate-800 p-8 flex flex-col items-center justify-center space-y-6 h-full text-center">
              <div className="w-20 h-20 bg-slate-900 rounded-2xl flex items-center justify-center border border-slate-800 shadow-xl">
                <File className="w-10 h-10 text-yellow-500/50" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-200 mb-1">Asset Committed</h3>
                <p className="text-sm text-slate-500 font-mono">UID: {selected}</p>
              </div>
              <div className="grid grid-cols-2 gap-4 w-full max-w-sm">
                <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase mb-1">Integrity Hash</div>
                  <div className="text-xs font-mono text-emerald-500 truncate">SHA-256:VERIFIED</div>
                </div>
                <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase mb-1">ACL Status</div>
                  <div className="text-xs font-mono text-yellow-500">OWNER_READ_ONLY</div>
                </div>
              </div>
              <div className="flex space-x-3 mt-8">
                <button className="flex items-center space-x-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-md text-sm transition-colors">
                  <ShieldCheck className="w-4 h-4" />
                  <span>Verify Provenance</span>
                </button>
                <button className="flex items-center space-x-2 px-4 py-2 bg-red-950/30 hover:bg-red-950/50 text-red-400 border border-red-900/50 rounded-md text-sm transition-colors">
                  <Trash2 className="w-4 h-4" />
                  <span>Purge Artifact</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="glass rounded-xl border border-slate-800 p-8 flex flex-col items-center justify-center text-slate-600 h-full">
              <FolderTree className="w-12 h-12 mb-4 opacity-20" />
              <p className="text-sm font-mono">Select an asset node to view commitments.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileExplorer;
