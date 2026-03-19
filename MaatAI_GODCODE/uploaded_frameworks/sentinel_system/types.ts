
export enum SystemModule {
  CHAT = 'CHAT',
  MATH = 'MATH',
  FILES = 'FILES',
  LEDGER = 'LEDGER',
  MANIFEST = 'MANIFEST',
  BACK_SYSTEM = 'BACK_SYSTEM',
  DOJO = 'DOJO'
}

export interface Manifest {
  rule_id: string;
  weight_vector: number[];
  allowed_auto_actions: string[];
  emergency_carveouts: boolean;
  activation_nonce: string;
  public_anchor: string;
}

export interface LedgerEntry {
  id: string;
  timestamp: number;
  type: 'UPLOAD' | 'MATH' | 'CHAT' | 'AUDIT';
  manifest_id: string;
  hash: string;
  metadata: any;
  provenance_verified: boolean;
}

export interface FileNode {
  id: string;
  name: string;
  type: 'file' | 'directory';
  hash?: string;
  children?: FileNode[];
  parentId?: string;
}

export interface RefractalResult {
  depth: number;
  R_prev: number;
  R_next: number;
  curiosity_triggered: boolean;
  curiosity_value: number | null;
}
