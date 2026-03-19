
import React, { useState, useEffect } from 'react';
import { Key, Save, Trash2, ShieldAlert, CheckCircle, Info, Lock, Settings } from 'lucide-react';

interface ConfigSuiteProps {
  onKeyChange: () => void;
}

const ConfigSuite: React.FC<ConfigSuiteProps> = ({ onKeyChange }) => {
  const [apiKey, setApiKey] = useState('');
  const [isSaved, setIsSaved] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const savedKey = localStorage.getItem('TOASTED_MASTER_KEY');
    if (savedKey) setApiKey(savedKey);
  }, []);

  const validateKey = (key: string) => {
    const regex = /^AIza[0-9A-Za-z-_]{35}$/;
    return regex.test(key);
  };

  const handleSave = () => {
    if (!apiKey.trim()) {
      localStorage.removeItem('TOASTED_MASTER_KEY');
      setIsSaved(true);
      setError('');
      onKeyChange();
      return;
    }

    if (!validateKey(apiKey)) {
      setError('Invalid Key Format. Expecting AIza... (39 chars)');
      return;
    }

    localStorage.setItem('TOASTED_MASTER_KEY', apiKey);
    setIsSaved(true);
    setError('');
    onKeyChange();
    setTimeout(() => setIsSaved(false), 3000);
  };

  const clearKey = () => {
    localStorage.removeItem('TOASTED_MASTER_KEY');
    setApiKey('');
    onKeyChange();
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="glass-panel p-8 rounded-2xl border-emerald-500/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
          <Settings size={120} />
        </div>
        
        <div className="flex flex-col md:flex-row items-start justify-between gap-4 mb-8">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
              <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><Key size={24} /></div>
              Architect Config
            </h2>
            <p className="text-zinc-500 max-w-xl">
              Ratify sovereign access keys. Data is stored locally and never transmitted to external pharaoh domains.
            </p>
          </div>
        </div>

        <div className="max-w-2xl space-y-6">
          <div className="space-y-2">
            <label className="text-[10px] font-black text-zinc-500 uppercase tracking-widest flex items-center gap-2">
              <Lock size={12} /> Master Master Key (Gemini API)
            </label>
            <div className="relative group">
              <input
                type="password"
                value={apiKey}
                onChange={(e) => {
                  setApiKey(e.target.value);
                  setError('');
                }}
                placeholder="AIza..."
                className={`w-full bg-white/5 border ${error ? 'border-red-500/50' : 'border-white/10'} rounded-xl py-3 px-4 text-sm text-white focus:outline-none focus:border-emerald-500/30 transition-all font-mono`}
              />
              {apiKey && (
                 <button onClick={clearKey} className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-red-400 transition-colors">
                   <Trash2 size={16} />
                 </button>
              )}
            </div>
            {error && <p className="text-red-400 text-[10px] font-bold uppercase mt-1 flex items-center gap-1"><ShieldAlert size={10} /> {error}</p>}
            {isSaved && !error && <p className="text-emerald-400 text-[10px] font-black uppercase mt-1 flex items-center gap-1"><CheckCircle size={10} /> Sovereignty Ratified</p>}
          </div>

          <div className="p-4 bg-emerald-500/5 border border-emerald-500/10 rounded-xl space-y-3">
            <h4 className="text-[10px] font-black text-emerald-500 uppercase tracking-widest flex items-center gap-2">
              <Info size={12} /> Sovereignty Protocol
            </h4>
            <p className="text-[11px] text-zinc-400 leading-relaxed">
              Manual keys bypass the AI Studio ephemeral session and provide persistent RL0 link. Ensure your project is billing-enabled for high-end Veo temporal manifest.
            </p>
          </div>

          <button
            onClick={handleSave}
            className="w-full md:w-auto px-12 py-3 bg-emerald-500 hover:bg-emerald-400 text-black font-black uppercase tracking-widest rounded-xl transition-all shadow-lg shadow-emerald-500/20 flex items-center justify-center gap-2"
          >
            <Save size={18} /> Ratify Configuration
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfigSuite;
