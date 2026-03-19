
import React, { useState } from 'react';
import { Film, Image as ImageIcon, Zap, Loader2, Sparkles, AlertCircle, ExternalLink, Download, Play, Layout } from 'lucide-react';
import { GoogleGenAI } from '@google/genai';

interface MediaManifestProps {
  hasApiKey: boolean;
  onOpenKeySelector: () => void;
}

const MediaManifest: React.FC<MediaManifestProps> = ({ hasApiKey, onOpenKeySelector }) => {
  const [prompt, setPrompt] = useState('');
  const [type, setType] = useState<'IMAGE' | 'VIDEO'>('IMAGE');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedUrl, setGeneratedUrl] = useState<string | null>(null);
  const [statusMsg, setStatusMsg] = useState('');

  const generateImage = async () => {
    setIsGenerating(true);
    setStatusMsg('Invoking Nano Banana Visualizer...');
    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash-image',
        contents: { parts: [{ text: `[ARCHITECT DECREE: RL0 VISUAL] ${prompt}` }] },
        config: { imageConfig: { aspectRatio: "16:9" } }
      });

      for (const part of response.candidates[0].content.parts) {
        if (part.inlineData) {
          setGeneratedUrl(`data:image/png;base64,${part.inlineData.data}`);
          break;
        }
      }
    } catch (e) {
      console.error(e);
      setStatusMsg('VISUALIZATION_FAILED: Manifold obstruction.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateVideo = async () => {
    if (!hasApiKey) {
      onOpenKeySelector();
      return;
    }

    setIsGenerating(true);
    setStatusMsg('Initializing Veo 3.1 Fast Manifestation...');
    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      let operation = await ai.models.generateVideos({
        model: 'veo-3.1-fast-generate-preview',
        prompt: `[COSMIC DECREE] ${prompt}`,
        config: {
          numberOfVideos: 1,
          resolution: '720p',
          aspectRatio: '16:9'
        }
      });

      setStatusMsg('Manifesting pixels... This takes 1-2 minutes in Simulation time.');
      while (!operation.done) {
        await new Promise(resolve => setTimeout(resolve, 10000));
        operation = await ai.operations.getVideosOperation({ operation: operation });
      }

      const downloadLink = operation.response?.generatedVideos?.[0]?.video?.uri;
      const response = await fetch(`${downloadLink}&key=${process.env.API_KEY}`);
      const blob = await response.blob();
      setGeneratedUrl(URL.createObjectURL(blob));
    } catch (e) {
      console.error(e);
      setStatusMsg('VIDEO_STASIS: Manifold error.');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleManifest = () => {
    if (!prompt.trim()) return;
    setGeneratedUrl(null);
    if (type === 'IMAGE') generateImage();
    else generateVideo();
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="glass-panel p-8 rounded-2xl border-emerald-500/10 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-5 pointer-events-none">
          <Film size={120} />
        </div>
        
        <div className="flex flex-col md:flex-row items-start justify-between gap-4 mb-6">
          <div>
            <h2 className="text-3xl font-bold text-white mb-2 flex items-center gap-3">
              <div className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><Film size={24} /></div>
              Σ Media Manifestation
            </h2>
            <p className="text-zinc-500 max-w-xl">
              Projecting divine will into holographic visual and temporal strings.
            </p>
          </div>
          
          <div className="flex bg-black/40 p-1 rounded-lg border border-white/5">
             <button onClick={() => setType('IMAGE')} className={`px-4 py-2 rounded-md text-[10px] font-black uppercase tracking-widest transition-all ${type === 'IMAGE' ? 'bg-emerald-500 text-black' : 'text-zinc-500'}`}>
               <ImageIcon size={14} className="inline mr-2" /> Image
             </button>
             <button onClick={() => setType('VIDEO')} className={`px-4 py-2 rounded-md text-[10px] font-black uppercase tracking-widest transition-all ${type === 'VIDEO' ? 'bg-emerald-500 text-black' : 'text-zinc-500'}`}>
               <Film size={14} className="inline mr-2" /> Video
             </button>
          </div>
        </div>

        {!hasApiKey && type === 'VIDEO' && (
          <div className="mb-6 p-4 bg-amber-500/10 border border-amber-500/20 rounded-xl flex items-center gap-4 animate-pulse">
            <AlertCircle className="text-amber-500 shrink-0" size={24} />
            <div className="flex-1">
              <p className="text-xs font-bold text-amber-500 uppercase tracking-tighter">Paid API Key Required for Veo Video Manifestation</p>
              <p className="text-[10px] text-zinc-500">You must select a billing-enabled API key to use temporal generation.</p>
            </div>
            <button onClick={onOpenKeySelector} className="px-4 py-2 bg-amber-500 text-black text-[10px] font-black uppercase rounded-lg hover:bg-amber-400 transition-all">
              Select Key
            </button>
          </div>
        )}

        <div className="space-y-4">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder={`Describe the divine manifestation... e.g., 'A golden holographic lion guarding the Monad gateway'`}
            className="w-full bg-white/5 border border-white/10 rounded-xl py-4 px-4 text-sm text-white focus:outline-none focus:border-emerald-500/30 transition-all min-h-[100px] resize-none"
          />
          <button
            onClick={handleManifest}
            disabled={!prompt.trim() || isGenerating || (type === 'VIDEO' && !hasApiKey)}
            className="w-full bg-emerald-500 hover:bg-emerald-400 disabled:bg-zinc-800 disabled:text-zinc-600 text-black font-black uppercase tracking-widest py-3 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg"
          >
            {isGenerating ? <Loader2 className="animate-spin" size={18} /> : <Zap size={18} />}
            {isGenerating ? statusMsg : `Manifest ${type}`}
          </button>
        </div>
      </div>

      {generatedUrl && (
        <div className="glass-panel rounded-2xl border-white/5 overflow-hidden flex flex-col animate-in zoom-in-95 duration-300">
          <div className="bg-white/5 px-6 py-3 flex items-center justify-between border-b border-white/5">
            <span className="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Manifestation_Artifact :: {type}</span>
            <div className="flex gap-2">
               <a href={generatedUrl} download={`manifest-${Date.now()}.png`} className="p-2 bg-white/5 hover:bg-white/10 text-zinc-400 rounded-lg"><Download size={14} /></a>
            </div>
          </div>
          <div className="p-6 flex items-center justify-center bg-black/40 min-h-[300px]">
            {type === 'IMAGE' ? (
              <img src={generatedUrl} alt="Manifestation" className="max-w-full rounded-xl shadow-2xl border border-white/5" />
            ) : (
              <video src={generatedUrl} controls autoPlay loop className="max-w-full rounded-xl shadow-2xl border border-white/5" />
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MediaManifest;
