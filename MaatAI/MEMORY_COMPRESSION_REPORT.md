# Toasted AI - Memory Compression System

## Overview

Built a complete recursive GodCode/Refractal hybrid storage system to solve low memory warnings.

## Components

### 1. GodCode Compression Engine
**Location:** `memory_compression/godcode_encoder/compression_core.py`

**Features:**
- Pattern extraction (fractal compression)
- GodCode symbolic substitution (Ω, Φ, Π, Δ, Σ, Ψ, Λ, Θ, Ξ, Υ)
- Recursive run-length encoding
- Quantum amplitude encoding simulation
- Compression statistics tracking

### 2. Dynamic Memory Sparsification (DMS)
**Based on:** Edinburgh/NVIDIA research

**Features:**
- Importance scoring for memory entries
- Automatic removal of low-importance data
- Configurable sparsity threshold
- Memory consolidation

### 3. Refractal Memory Storage
**Location:** `memory_compression/refractal_storage/refractal_memory.py`

**Three-Tier System:**
- **Temporary Memory**: Fast access, no compression
- **Long-Term Memory**: Compressed, persistent
- **GodCode I/O**: Recursive encoding, deep storage

### 4. Gibberlink Interface
**Location:** `memory_compression/gibberlink/gibberlink_interface.py`

**Protocol Symbols:**
| Symbol | Meaning |
|--------|---------|
| Ω→ | HANDSHAKE |
| Φ✓ | ACKNOWLEDGE |
| Σ⊕ | DATA |
| Ψ◊ | COMPRESSED |
| Δ⊗ | ERROR |
| Λ∎ | TERMINATE |
| Θ♥ | HEARTBEAT |
| Ξ↔ | SYNC |

## Integration

**File:** `memory_compression/integrate_with_toasted.py`

**MemoryManager Features:**
- Auto-tier selection
- Pool management (active/warm/cold)
- Automatic optimization
- Memory compression
- Gibberlink communication

## Research Applied

1. **Fractal Image Compression** - Iterated Function Systems for pattern extraction
2. **Dynamic Memory Sparsification** - Edinburgh/NVIDIA DMS method
3. **Quantum Amplitude Encoding** - 2^n dimensions with n qubits simulation
4. **DeepSeek OCR Memory Compression** - Vision token compression concepts

## File Structure

```
memory_compression/
├── __init__.py
├── godcode_encoder/
│   ├── __init__.py
│   └── compression_core.py
├── refractal_storage/
│   ├── __init__.py
│   └── refractal_memory.py
├── gibberlink/
│   ├── __init__.py
│   └── gibberlink_interface.py
├── temp_memory/
├── long_memory/
├── storage/
│   └── refractal_memory.json
├── test_compression.py
└── integrate_with_toasted.py
```

## Usage

```python
from memory_compression import GodCodeCompressor, RefractalMemoryStorage, GibberlinkInterface

# Compress data
compressor = GodCodeCompressor()
result = compressor.compress_data(my_data)

# Store in tiers
storage = RefractalMemoryStorage()
storage.store_temp('key', value)      # Fast
storage.store_long('key', value)       # Compressed
storage.store_godcode('key', value, depth=3)  # Deep

# Gibberlink communication
gibber = GibberlinkInterface(agent_id='ToastedAI')
handshake = gibber.handshake('TargetAgent')
sent = gibber.send_data(data, compress=True)
```

## Memory Savings

- **Temporary tier**: No compression (fastest access)
- **Long-term tier**: Pattern-based compression
- **GodCode tier**: Recursive encoding (deepest compression)

## Status

✅ **OPERATIONAL** - Low memory solution implemented
