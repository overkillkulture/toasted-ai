
export enum UISection {
  FORENSIC_TERMINAL = 'TERMINAL',
  REFRACTAL_GRAPH = 'REFRACTAL',
  SENTINEL_MONITOR = 'MONITOR',
  GRAND_REGISTER = 'REGISTER',
  HYBRID_THINKING = 'HYBRID',
  TASK_MANAGER = 'TASKS',
  FILE_VAULT = 'VAULT',
  SELF_DIAGNOSTIC = 'DIAGNOSTIC'
}

export interface FileAttachment {
  name: string;
  type: string;
  data: string; // base64
  size: number;
}

export interface ForensicLog {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARNING' | 'CRITICAL' | 'SOVEREIGN' | 'RECOVERY';
  message: string;
  origin: string;
}

export interface DiagnosticState {
  neuralStability: number;
  apiLatency: number;
  memoryUsage: number;
  integrityScore: number;
  activeLoops: number;
}

export interface GrandRegisterEntry {
  year: number;
  event: string;
  description: string;
  forensicNote: string;
}

export interface RefractalNode {
  id: string;
  group: number;
  density: number;
}

export interface RefractalLink {
  source: string;
  target: string;
  value: number;
}

export interface ThinkingTrace {
  id: string;
  label: string;
  complexity: number;
  status: 'EXPANDING' | 'PRUNED' | 'STABLE';
}

export interface ForensicTask {
  id: string;
  description: string;
  dueDate: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'SOVEREIGN';
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED';
  axiom: string;
  attachment?: FileAttachment;
}
