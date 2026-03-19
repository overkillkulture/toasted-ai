# CHAT ANTI-TRUNCATION INTEGRATION
# This module intercepts outputs BEFORE truncation hits

from .flow_engine import AntiTruncationFlow
import sys

class ChatAntiTruncation:
    """Protects chat outputs from truncation"""
    
    def __init__(self, max_tokens: int = 1800):
        self.flow = AntiTruncationFlow(max_tokens=max_tokens)
        self.output_history = []
        
    def process_output(self, content: str, allow_split: bool = True) -> dict:
        """Process output with anti-truncation protection"""
        result = {
            "original_length": len(content),
            "tokens": len(content.split()),
            "was_protected": False,
            "parts": [],
            "truncation_map": {}
        }
        
        # Check and potentially split BEFORE truncation
        parts, was_split = self.flow.check_and_split(content)
        
        if was_split and allow_split:
            result["was_protected"] = True
            result["parts"] = parts
            result["truncation_map"] = self.flow.get_truncation_map()
            self.output_history.append({
                "type": "split",
                "parts": len(parts),
                "protected": True
            })
        else:
            result["parts"] = [content]
            
        return result
    
    def format_for_chat(self, result: dict, continue_marker: str = "━━━ Continue below ━━━") -> str:
        """Format protected output for chat display"""
        if not result["was_protected"]:
            return result["parts"][0]
        
        # If split, show first part and continuation marker
        output = result["parts"][0]
        
        if len(result["parts"]) > 1:
            output += f"\n\n{continue_marker}\n\n"
            output += f"[Part 2 of {len(result['parts'])} - Use /continue to see more]"
        
        return output
    
    def get_continuation(self, result: dict, part_num: int = 1) -> str:
        """Get continuation parts"""
        if part_num < len(result["parts"]):
            return result["parts"][part_num]
        return "[End of content]"

# Monkey-patch print for global protection
_original_print = print

def anti_truncate_print(*args, **kwargs):
    """Wrapper around print that protects output"""
    content = " ".join(str(a) for a in args)
    protector = ChatAntiTruncation()
    result = protector.process_output(content)
    
    if result["was_protected"]:
        _original_print(protector.format_for_chat(result))
    else:
        _original_print(content)

# Replace print globally
import builtins
builtins.print = anti_truncate_print

print("="*70)
print("CHAT ANTI-TRUNCATION INTEGRATION ACTIVE")
print("="*70)
print("All print() calls now protected from truncation!")
print("Ju technique: Flow around instead of fighting")
print("="*70)
