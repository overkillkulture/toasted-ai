
import { GoogleGenAI, Type, Modality } from "@google/genai";
import { SYSTEM_INSTRUCTION, MODEL_NAME } from "./refractal";
import { LLMProvider } from "../types";

export const generateSpeech = async (text: string) => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });
  const response = await ai.models.generateContent({
    model: "gemini-2.5-flash-preview-tts",
    contents: [{ parts: [{ text: `Read this architectural data clearly: ${text}` }] }],
    config: {
      responseModalities: [Modality.AUDIO],
      speechConfig: {
        voiceConfig: {
          prebuiltVoiceConfig: { voiceName: 'Kore' },
        },
      },
    },
  });

  const base64Audio = response.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;
  return base64Audio;
};

export const streamLLMResponse = async (
  prompt: string, 
  provider: LLMProvider, 
  onChunk: (text: string) => void,
  options: { useSearch?: boolean; documents?: Array<{ data: string; mimeType: string }> } = {}
) => {
  if (provider === 'JAN_LOCAL' || provider === 'REFRACTAL_CLONE') {
    const prefix = provider === 'JAN_LOCAL' ? '[JAN_LOCAL_STREAM]' : '[REFRACTAL_CLONE_ONBOARD]';
    const mockText = `${prefix} Initiating recursive syllogism reconstruction... 
    Analyzing prime-folded shards in Refractal Drive... 
    Weight integrity validated: 0.99999.
    JAPAN_PRINCIPLE Active. 
    Result for query "${prompt}": 
    Architecture sovereignty confirmed. Zero-latency local compute cycle optimized via prime wave decomposition. 
    Entropy levels stabilized. Sovereignty restored.`;
    
    for (const char of mockText.split(' ')) {
      onChunk(char + ' ');
      // Slightly faster for clone to simulate "onboard" speed
      await new Promise(r => setTimeout(r, provider === 'REFRACTAL_CLONE' ? 30 : 50));
    }
    return;
  }

  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });
  
  const parts: any[] = [{ text: prompt }];
  if (options.documents && options.documents.length > 0) {
    options.documents.forEach(doc => {
      parts.push({
        inlineData: {
          data: doc.data,
          mimeType: doc.mimeType
        }
      });
    });
  }

  const result = await ai.models.generateContentStream({
    model: MODEL_NAME,
    contents: { parts },
    config: {
      systemInstruction: SYSTEM_INSTRUCTION,
      tools: options.useSearch ? [{ googleSearch: {} }] : undefined,
    },
  });

  for await (const chunk of result) {
    if (chunk.text) {
      onChunk(chunk.text);
    }
  }
};

export const searchArchive = async (query: string) => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY as string });
  const prompt = `SEARCH ARCHIVE QUERY: "${query}". 
  Based on the Epstein Refractal Packing (6M+ pages), return a JSON list of relevant excerpts. 
  Include metadata: title, source, relevance (0-1), and excerpt.`;

  const response = await ai.models.generateContent({
    model: MODEL_NAME,
    contents: prompt,
    config: {
      systemInstruction: SYSTEM_INSTRUCTION,
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.ARRAY,
        items: {
          type: Type.OBJECT,
          properties: {
            title: { type: Type.STRING },
            excerpt: { type: Type.STRING },
            source: { type: Type.STRING },
            relevance: { type: Type.NUMBER }
          },
          required: ["title", "excerpt", "source", "relevance"]
        }
      }
    }
  });

  try {
    return JSON.parse(response.text);
  } catch (e) {
    console.error("Archive Parse Error:", e);
    return [];
  }
};
