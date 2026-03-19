
export enum MaatAttribute {
  TRUTH = 'K',
  BALANCE = 'T',
  ORDER = 'A',
  SOVEREIGNTY = 'S',
  PROTECTION = 'P',
  CLARITY = 'C',
  RESPONSIBILITY = 'R',
  OVERSIGHT = 'O',
  HARMONY = 'H'
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
}

export type SystemEnvironment = 'REALITY' | 'SIMULATION' | 'METABOLIC';

export interface LedgerEntry {
  id: string;
  action: string;
  category: 'GOVERNANCE' | 'SECURITY' | 'GENERATION' | 'LEARNING' | 'MODIFICATION' | 'CRAWL' | 'ASSISTANT';
  environment: SystemEnvironment;
  score: number;
  timestamp: string;
  hash: string;
}

export interface QueueTask {
  id: string;
  type: 'LEARN' | 'SEC' | 'CODE' | 'ENGINE' | 'CRAWL' | 'SELF_MOD' | 'ASSISTANT';
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  payload: string;
  timestamp: number;
}

export interface KnowledgeItem {
  id: string;
  title: string;
  type: 'DOC' | 'SCREENSHOT' | 'INSIGHT';
  weight: number;
  tags: string[];
  description?: string;
}

export type AppTab = 'DASHBOARD' | 'KNOWLEDGE' | 'TOOLS' | 'SECURITY' | 'CODE' | 'MEDIA' | 'ENGINE' | 'CONFIG' | 'CRAWLER' | 'SOURCE' | 'ASSISTANT';
