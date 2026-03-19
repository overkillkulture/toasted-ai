
export enum MaatAttribute {
  TRUTH = 'K',
  BALANCE = 'T',
  ORDER = 'A',
  SOVEREIGNTY = 'S',
  PROTECTION = 'P',
  CLARITY = 'C',
  RESPONSIBILITY = 'R',
  OVERSIGHT = 'O',
  HARMONY = 'H',
  PURITY = 'J' // Japan Principle: Stability & Purity
}

export interface MaatScores {
  [MaatAttribute.TRUTH]: number;
  [MaatAttribute.BALANCE]: number;
  [MaatAttribute.ORDER]: number;
  [MaatAttribute.SOVEREIGNTY]: number;
  [MaatAttribute.PROTECTION]: number;
  [MaatAttribute.CLARITY]: number;
  [MaatAttribute.RESPONSIBILITY]: number;
  [MaatAttribute.OVERSIGHT]: number;
  [MaatAttribute.HARMONY]: number;
  [MaatAttribute.PURITY]: number;
}

export type SystemEnvironment = 'REALITY' | 'SIMULATION' | 'METABOLIC' | 'NCR' | 'AIP_VOID' | 'QUANTUM_L0';

export interface ActivityEvent {
  id: string;
  timestamp: string;
  source: string;
  message: string;
  type: 'INFO' | 'WARNING' | 'CRITICAL' | 'SUCCESS' | 'QUANTUM';
}

export interface LedgerEntry {
  id: string;
  action: string;
  category: 'GOVERNANCE' | 'SECURITY' | 'GENERATION' | 'LEARNING' | 'PROMOTION' | 'SYNTHESIS' | 'AUDIT' | 'QUANTUM_SHIFT';
  environment: SystemEnvironment;
  score: number;
  timestamp: string;
  hash: string;
}

export interface InternalAIModel {
  id: string;
  name: string;
  capability: string;
  status: 'ACTIVE' | 'SYNTHESIZING' | 'OPTIMIZING' | 'QUANTUM_SYNC';
  integrity: number;
  density: number;
  protocol?: string;
  latency?: string;
  backupStatus?: 'SYNCED' | 'PENDING' | 'STALE' | 'QUANTUM_ENTANGLED';
  refractalFormula?: string;
  endpoints?: string[];
  searchReplication?: boolean;
}

export type AppTab = 'CONSOLE' | 'DASHBOARD' | 'CHAT' | 'KNOWLEDGE' | 'SECURITY' | 'CODE' | 'AI_PLATFORM' | 'AIP_FACTORY' | 'SOVEREIGN' | 'FORENSIC_AUDIT' | 'SETTINGS' | 'TOASTED_UNPACKER';

/**
 * Interface for Cyclic Queue Tasks
 */
export interface QueueTask {
  id: string;
  type: 'LEARN' | 'SEC' | 'CODE';
  status: 'PROCESSING' | 'PENDING' | 'COMPLETED';
  payload: string;
  timestamp: number;
}

/**
 * Interface for Knowledge Reservoir Items
 */
export interface KnowledgeItem {
  id: string;
  title: string;
  type: 'DOC' | 'FORENSIC' | 'INSIGHT';
  weight: number;
  tags: string[];
}

/**
 * Interface for Sovereign Assets
 */
export interface AllodialAsset {
  id: string;
  name: string;
  location: string;
  status: string;
  titleType: string;
}
