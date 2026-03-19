
import { GoogleGenAI, GenerateContentResponse, Modality } from "@google/genai";
import { SOVEREIGN_SYSTEM_PROMPT } from "../constants";
import { FileAttachment } from "../types";

export class GeminiService {
  private lastError: string | null = null;
  private retryCount = 0;
  private readonly MAX_RETRIES = 3;
  private audioContext: AudioContext | null = null;

  async *streamSovereignResponse(userInput: string, file?: FileAttachment) {
    this.retryCount = 0;
    while (this.retryCount < this.MAX_RETRIES) {
      try {
        const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
        const parts: any[] = [{ text: userInput }];
        
        if (file) {
          parts.push({
            inlineData: {
              mimeType: file.type,
              data: file.data.split(',')[1]
            }
          });
        }

        const responseStream = await ai.models.generateContentStream({
          model: "gemini-3-pro-preview",
          contents: { parts },
          config: {
            systemInstruction: SOVEREIGN_SYSTEM_PROMPT,
            temperature: 0.9,
            thinkingConfig: { thinkingBudget: 16384 }
          },
        });

        for await (const chunk of responseStream) {
          const c = chunk as GenerateContentResponse;
          if (c.text) {
            yield c.text;
          }
        }
        return;
      } catch (err: any) {
        this.retryCount++;
        this.lastError = err.message;
        if (this.retryCount >= this.MAX_RETRIES) {
          yield `\n[CRITICAL_FAILURE] Neural connection severed. Error: ${err.message}`;
          throw err;
        }
        await new Promise(res => setTimeout(res, 1000 * Math.pow(2, this.retryCount)));
      }
    }
  }

  async speakSovereignProclamation(text: string) {
    try {
      const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });
      const response = await ai.models.generateContent({
        model: "gemini-2.5-flash-preview-tts",
        contents: [{ parts: [{ text: `Read with absolute authority and gravitas: ${text.slice(0, 500)}` }] }],
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
      if (base64Audio) {
        await this.playRawPcm(base64Audio);
      }
    } catch (err) {
      console.error("Audio synthesis loop failure:", err);
    }
  }

  private async playRawPcm(base64: string) {
    if (!this.audioContext) {
      this.audioContext = new (window.AudioContext || (window as any).webkitAudioContext)({ sampleRate: 24000 });
    }
    
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }

    const dataInt16 = new Int16Array(bytes.buffer);
    const frameCount = dataInt16.length;
    const buffer = this.audioContext.createBuffer(1, frameCount, 24000);
    const channelData = buffer.getChannelData(0);

    for (let i = 0; i < frameCount; i++) {
      channelData[i] = dataInt16[i] / 32768.0;
    }

    const source = this.audioContext.createBufferSource();
    const gainNode = this.audioContext.createGain();
    source.buffer = buffer;
    gainNode.gain.value = 0.8;
    source.connect(gainNode);
    gainNode.connect(this.audioContext.destination);
    source.start();
  }

  public getDiagnosticReport() {
    return {
      status: this.lastError ? 'DEGRADED' : 'OPTIMAL',
      lastError: this.lastError,
      neuralUptime: performance.now(),
      connectivity: this.retryCount > 0 ? 'INTERMITTENT' : 'STABLE'
    };
  }
}

export const sovereignAI = new GeminiService();
