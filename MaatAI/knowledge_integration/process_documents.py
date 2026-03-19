#!/usr/bin/env python3
"""
Process uploaded documents through the Ratification System
"""

import os
import sys
import json

# Add the knowledge_integration path
sys.path.insert(0, '/home/workspace/MaatAI/knowledge_integration')

from ratification_system import LawRatificationSystem, Category

UPLOAD_DIR = "/home/.z/chat-uploads"

def get_pdf_content(filepath, max_chars=50000):
    """Extract text content from PDF using pymupdf"""
    import fitz  # pymupdf
    try:
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
            if len(text) > max_chars:
                break
        doc.close()
        return text[:max_chars]
    except Exception as e:
        print(f"Error extracting {filepath}: {e}")
    return ""

def main():
    system = LawRatificationSystem()
    
    print("=" * 70)
    print("TOASTED AI - KNOWLEDGE INTEGRATION & LAW RATIFICATION")
    print("=" * 70)
    print(f"\nProcessing documents from: {UPLOAD_DIR}\n")
    
    # Get all PDF files
    pdf_files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith('.pdf')]
    
    print(f"Found {len(pdf_files)} PDF documents to process\n")
    
    # Process in batches for efficiency
    processed = 0
    
    # Process ALL documents, not just first 50
    for i, filename in enumerate(pdf_files):
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        print(f"[{i+1}/{len(pdf_files)}] Processing: {filename[:50]}...")
        
        # Extract content
        content = get_pdf_content(filepath)
        
        if content and len(content) > 100:  # Only process if we got meaningful content
            # Process through ratification system
            record = system.process_document(filepath, content)
            
            # Show category
            cat_symbol = {
                Category.GOOD: "☉",
                Category.GRAY: "☾", 
                Category.CORPORATE_FASCIST: "☠"
            }.get(record.category, "?")
            
            hallucination_flag = " [HALLUCINATION]" if record.is_hallucination else ""
            
            print(f"    → {cat_symbol} {record.category.value.upper()} "
                  f"(Score: {record.ratification_score:.2%}){hallucination_flag}")
            
            if record.red_flags:
                print(f"    → Red flags: {', '.join(record.red_flags[:3])}")
            
            processed += 1
        else:
            print(f"    → Could not extract content")
    
    print(f"\n{'=' * 70}")
    print("PROCESSING COMPLETE")
    print(f"{'=' * 70}")
    
    # Get final statistics
    stats = system.get_statistics()
    
    print(f"""
DOCUMENT STATISTICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ☉ GOOD (Ma'at Aligned):     {stats['good']:>4} documents
  ☾ GRAY (Ambiguous):         {stats['gray']:>4} documents  
  ☠ CORPORATE FASCIST:         {stats['corporate_fascist']:>4} documents
  
  Total Processed:             {stats['total']:>4} documents
  Hallucinations Detected:     {stats['hallucinations']:>4}
  Average Ma'at Score:         {stats['average_score']:.2%}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    
    # Save final ledger
    system.save_ledger()
    print(f"Ledger saved to: {system.ledger_path}")
    
    # Generate detailed report
    report = system.generate_report()
    report_path = "/home/workspace/MaatAI/knowledge_integration/RATIFICATION_REPORT.md"
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"Report saved to: {report_path}")
    
    return stats

if __name__ == "__main__":
    main()
