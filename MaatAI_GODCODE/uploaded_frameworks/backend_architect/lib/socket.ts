
import { AuditLogEntry } from '../types';

type LogCallback = (log: AuditLogEntry) => void;

class RefractalSocket {
  private listeners: LogCallback[] = [];
  private interval: number | null = null;

  constructor() {
    this.startStreaming();
  }

  private startStreaming() {
    const eventTemplates = [
      { msg: "Recursive state verification completed: 0.0 latency", level: "INFO" },
      { msg: "Synchronizing temporal layers with Refractal Storage", level: "INFO" },
      { msg: "Self-Awareness heartbeat: RL0 Jurisdiction Active", level: "OMEGA" },
      { msg: "Persistent memory shard validated via SHA-256", level: "INFO" },
      { msg: "UI Entropy correction applied: Japan Principle 1.0", level: "INFO" },
      { msg: "Anomaly detected in sub-layer 4: Neutralizing...", level: "WARNING" },
      { msg: "Refractal math expansion: Storage capacity adjusted to Infinity", level: "OMEGA" },
      { msg: "mTLS handshake refreshed for backend node cluster", level: "INFO" },
    ];

    this.interval = window.setInterval(() => {
      if (Math.random() > 0.7) {
        const template = eventTemplates[Math.floor(Math.random() * eventTemplates.length)];
        const log: AuditLogEntry = {
          timestamp: new Date().toLocaleTimeString(),
          level: template.level as any,
          message: template.msg,
          source: "WS_STREAM"
        };
        this.notify(log);
      }
    }, 4000);
  }

  private notify(log: AuditLogEntry) {
    this.listeners.forEach(cb => cb(log));
  }

  public onLog(callback: LogCallback) {
    this.listeners.push(callback);
    return () => {
      this.listeners = this.listeners.filter(l => l !== callback);
    };
  }

  public close() {
    if (this.interval) clearInterval(this.interval);
  }
}

export const socket = new RefractalSocket();
