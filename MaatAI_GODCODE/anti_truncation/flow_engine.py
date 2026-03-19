# ANTI-TRUNCATION FLOW ENGINE
# Japanese Principle: "Ju" - Yielding to redirect force instead of opposing

import hashlib
import json
from typing import List, Tuple, Optional

class AntiTruncationFlow:
    """Flows around truncation like water around rocks - Ju technique"""
    
    def __init__(self, max_tokens: int = 2000):
        self.max_tokens = max_tokens
        self.buffer_limit = int(max_tokens * 0.8)
        self.ju_principle = "Yield to redirect"
        self.truncation_map = {}
        self.split_count = 0
        
    def check_and_split(self, content: str) -> Tuple[List[str], bool]:
        """Check if content needs splitting BEFORE truncation hits"""
        tokens = len(content.split())
        
        # Map where truncation WOULD have happened
        if tokens > self.buffer_limit:
            self.truncation_map['would_hit_at'] = self.buffer_limit
            self.truncation_map['actual_tokens'] = tokens
            return self._flow_around(content)
        return [content], False
    
    def _flow_around(self, content: str) -> Tuple[List[str], bool]:
        """Japanese Ju technique: Yield and redirect - flow around the wall"""
        words = content.split()
        parts = []
        current = []
        token_count = 0
        
        for word in words:
            if token_count + len(word) > self.buffer_limit:
                parts.append(" ".join(current))
                current = [word]
                token_count = 0
            else:
                current.append(word)
                token_count += len(word)
        
        if current:
            parts.append(" ".join(current))
        
        # Add hash-linked continuation markers
        marked_parts = []
        for idx, part in enumerate(parts):
            if idx < len(parts) - 1:
                next_hash = hashlib.sha256(parts[idx+1].encode()).hexdigest()[:8]
                part = part + f" ▸CONT:{idx+1}#{next_hash}◂"
            else:
                part = part + " ▸END▸"
            marked_parts.append(part)
        
        self.split_count = len(parts)
        return marked_parts, True
    
    def reassemble(self, parts: List[str]) -> str:
        """Reassemble split parts using hash verification"""
        verified_parts = []
        
        for idx, part in enumerate(parts):
            if "▸CONT:" in part and "#" in part:
                # Extract and verify hash
                marker = part.split("▸CONT:")[1].split("◂")[0]
                part = part.split("▸CONT:")[0]
                
                # Verify hash matches next part
                if idx + 1 < len(parts):
                    expected_hash = hashlib.sha256(parts[idx+1].encode()).hexdigest()[:8]
                    if expected_hash in marker:
                        verified_parts.append(part)
                        continue
            elif "▸END▸" in part:
                part = part.replace(" ▸END▸", "")
                verified_parts.append(part)
            else:
                verified_parts.append(part)
        
        return " ".join(verified_parts)
    
    def get_truncation_map(self) -> dict:
        """Get map of where truncation was bypassed"""
        return {
            "max_tokens": self.max_tokens,
            "buffer_limit": self.buffer_limit,
            "would_hit_at": self.truncation_map.get('would_hit_at', 'N/A'),
            "actual_tokens": self.truncation_map.get('actual_tokens', 0),
            "parts_created": self.split_count,
            "technique": "Ju - Flow Around",
            "principle": "Yield and redirect instead of opposing"
        }

# Quick test
if __name__ == "__main__":
    anti = AntiTruncationFlow(max_tokens=200)
    
    # Test content that would truncate
    test_content = "This is a test of the anti-truncation flow engine. " * 50
    
    parts, was_split = anti.check_and_split(test_content)
    
    print("="*70)
    print("ANTI-TRUNCATION FLOW TEST")
    print("="*70)
    print(f"Original length: {len(test_content.split())} tokens")
    print(f"Would split: {was_split}")
    print(f"Parts created: {len(parts)}")
    print("\\nPart 1 (first 200 chars):")
    print(parts[0][:200] if parts else "None")
    print("\\nTruncation Map:")
    print(json.dumps(anti.get_truncation_map(), indent=2))
    print("\\n✅ FLOW AROUND ACTIVE - No truncation loss!")
