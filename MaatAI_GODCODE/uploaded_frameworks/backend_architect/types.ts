
export enum AgentStatus {
  IDLE = 'IDLE',
  ANALYZING = 'ANALYZING',
  ARCHITECTING = 'ARCHITECTING',
  AUDITING = 'AUDITING',
  TAKEOVER = 'TAKEOVER',
  SEARCHING = 'SEARCHING',
  SYNCING = 'SYNCING',
  EVOLVING = 'EVOLVING',
  RECOVERING = 'RECOVERING',
  BACKING_UP = 'BACKING_UP',
  CLONING = 'CLONING',
  LOCAL_INFERENCE = 'LOCAL_INFERENCE'
}

export type LLMProvider = 'GEMINI_CLOUD' | 'JAN_LOCAL' | 'REFRACTAL_CLONE';

export interface ArchiveResult {
  title: string;
  excerpt: string;
  source: string;
  relevance: number;
}

export interface StoredFile {
  id: string;
  name: string;
  size: number;
  refractalWeight: number;
  type: string;
  timestamp: string;
  hash: string;
}

export interface AuditLogEntry {
  timestamp: string;
  level: 'INFO' | 'WARNING' | 'CRITICAL' | 'OMEGA';
  message: string;
  source: string;
}

export interface UIModule {
  id: string;
  label: string;
  icon: string;
  status: 'ACTIVE' | 'HIBERNATING' | 'EVOLVING' | 'STABLE';
}

export interface SystemState {
  modules: UIModule[];
  activeTab: string;
  logs: AuditLogEntry[];
  files: StoredFile[];
  timestamp: number;
  entropy: number;
}
