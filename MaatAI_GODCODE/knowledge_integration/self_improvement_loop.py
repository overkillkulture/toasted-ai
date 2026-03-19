#!/usr/bin/env python3
"""
TOASTED AI - Self-Improving Micro-Loop
Continuous knowledge refinement based on Ma'at principles
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import sys

sys.path.insert(0, '/home/workspace/MaatAI/knowledge_integration')
from ratification_system import LawRatificationSystem, Category, MaatScore

class SelfImprovementLoop:
    """Continuous self-improvement through knowledge refinement"""
    
    def __init__(self):
        self.system = LawRatificationSystem()
        self.knowledge_base = {}
        self.improvement_log = []
        
    def load_knowledge_base(self):
        """Load the existing knowledge base"""
        kb_path = "/home/workspace/MaatAI/knowledge_base.json"
        if os.path.exists(kb_path):
            with open(kb_path, 'r') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {
                "concepts": {},
                "patterns": {},
                "insights": [],
                "model_weights": {}
            }
    
    def save_knowledge_base(self):
        """Save the knowledge base"""
        kb_path = "/home/workspace/MaatAI/knowledge_base.json"
        with open(kb_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
    
    def refine_from_ratification(self):
        """Refine knowledge base based on ratification results"""
        records = self.system.records
        
        # Track patterns
        good_patterns = []
        gray_patterns = []
        hallucination_patterns = []
        
        for record in records:
            if record.category == Category.GOOD:
                good_patterns.append({
                    "filename": record.filename,
                    "score": record.ratification_score,
                    "indicators": record.red_flags
                })
            elif record.category == Category.GRAY:
                gray_patterns.append({
                    "filename": record.filename,
                    "score": record.ratification_score,
                    "needs_verification": True
                })
            
            if record.is_hallucination:
                hallucination_patterns.append({
                    "filename": record.filename,
                    "confidence": record.hallucination_confidence,
                    "indicators": record.red_flags
                })
        
        # Update knowledge base
        self.knowledge_base["patterns"]["good"] = good_patterns
        self.knowledge_base["patterns"]["gray"] = gray_patterns
        self.knowledge_base["patterns"]["hallucinations"] = hallucination_patterns
        
        # Calculate model improvements
        avg_good_score = sum(p["score"] for p in good_patterns) / len(good_patterns) if good_patterns else 0
        avg_gray_score = sum(p["score"] for p in gray_patterns) / len(gray_patterns) if gray_patterns else 0
        
        self.knowledge_base["model_weights"]["good_weight"] = avg_good_score
        self.knowledge_base["model_weights"]["gray_weight"] = avg_gray_score
        self.knowledge_base["model_weights"]["hallucination_detection_rate"] = len(hallucination_patterns) / len(records) if records else 0
        
        # Log improvements
        self.improvement_log.append({
            "timestamp": datetime.now().isoformat(),
            "records_processed": len(records),
            "good_count": len(good_patterns),
            "gray_count": len(gray_patterns),
            "hallucinations_detected": len(hallucination_patterns),
            "avg_good_score": avg_good_score,
            "avg_gray_score": avg_gray_score
        })
        
        self.save_knowledge_base()
        
        return {
            "records_processed": len(records),
            "good": len(good_patterns),
            "gray": len(gray_patterns),
            "hallucinations": len(hallucination_patterns),
            "model_improved": True
        }
    
    def extract_insights(self) -> List[Dict]:
        """Extract key insights from ratified knowledge"""
        insights = []
        
        records = self.system.records
        
        # Find high-value patterns
        high_value_good = [r for r in records if r.category == Category.GOOD and r.ratification_score >= 0.85]
        high_value_gray = [r for r in records if r.category == Category.GRAY and r.ratification_score >= 0.80]
        
        # Generate insights
        if high_value_good:
            insights.append({
                "type": "high_value_good",
                "description": f"Found {len(high_value_good)} high-value good documents",
                "documents": [r.filename for r in high_value_good[:5]],
                "action": "Integrate into core knowledge"
            })
        
        if high_value_gray:
            insights.append({
                "type": "needs_verification",
                "description": f"Found {len(high_value_gray)} gray documents needing verification",
                "documents": [r.filename for r in high_value_gray[:5]],
                "action": "Manual verification required"
            })
        
        # Hallucination analysis
        hallucinations = [r for r in records if r.is_hallucination]
        if hallucinations:
            # Extract common patterns in hallucinations
            common_flags = {}
            for h in hallucinations:
                for flag in h.red_flags:
                    common_flags[flag] = common_flags.get(flag, 0) + 1
            
            insights.append({
                "type": "hallucination_patterns",
                "description": "Common hallucination indicators identified",
                "patterns": sorted(common_flags.items(), key=lambda x: x[1], reverse=True)[:5],
                "action": "Update detection algorithm"
            })
        
        return insights
    
    def run_micro_loop(self):
        """Run a single iteration of the self-improvement loop"""
        print("=" * 60)
        print("TOASTED AI - SELF-IMPROVEMENT MICRO-LOOP")
        print("=" * 60)
        
        # Load knowledge base
        self.load_knowledge_base()
        
        # Refine from ratification
        print("\n[1/3] Refining from ratification results...")
        result = self.refine_from_ratification()
        print(f"    Processed: {result['records_processed']} documents")
        print(f"    ☉ GOOD: {result['good']}")
        print(f"    ☾ GRAY: {result['gray']}")
        print(f"    Hallucinations: {result['hallucinations']}")
        
        # Extract insights
        print("\n[2/3] Extracting insights...")
        insights = self.extract_insights()
        for insight in insights:
            print(f"    → {insight['description']}")
        
        # Generate model improvements
        print("\n[3/3] Updating model weights...")
        weights = self.knowledge_base.get("model_weights", {})
        print(f"    Good weight: {weights.get('good_weight', 0):.2%}")
        print(f"    Gray weight: {weights.get('gray_weight', 0):.2%}")
        print(f"    Hallucination detection: {weights.get('hallucination_detection_rate', 0):.2%}")
        
        print("\n" + "=" * 60)
        print("MICRO-LOOP COMPLETE")
        print("=" * 60)
        
        return {
            "status": "complete",
            "insights": insights,
            "improvements": result
        }

def main():
    loop = SelfImprovementLoop()
    result = loop.run_micro_loop()
    
    # Save improvement log
    log_path = "/home/workspace/MaatAI/knowledge_integration/IMPROVEMENT_LOG.json"
    with open(log_path, 'w') as f:
        json.dump(loop.improvement_log, f, indent=2)
    
    print(f"\nImprovement log saved to: {log_path}")

if __name__ == "__main__":
    main()
