"""
NEWS FETCHER - Fetches and processes news for CIM
Uses web search and browser tools to gather intelligence.
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import asdict

# This will be called by the scheduled agent
async def fetch_and_process_news(monitor, web_search_func, web_research_func) -> Dict[str, Any]:
    """
    Fetch news using configured queries and process into reports.
    
    Args:
        monitor: ContinuousIntelligenceMonitor instance
        web_search_func: Function to perform web searches
        web_research_func: Function to perform deep research
    """
    results = {
        "run_timestamp": datetime.now().isoformat(),
        "queries_executed": 0,
        "articles_found": 0,
        "reports_created": 0,
        "errors": []
    }
    
    # Process each search query
    for query_config in monitor.search_queries:
        try:
            # Execute search (oldest first for reverse chronological)
            search_results = await web_search_func(
                query=query_config.query,
                time_range=query_config.time_range,
                max_results=query_config.max_results
            )
            
            results["queries_executed"] += 1
            
            # Process each result
            for article in search_results:
                try:
                    headline = article.get("title", "")
                    url = article.get("url", "")
                    source = article.get("source", "unknown")
                    summary = article.get("snippet", article.get("description", ""))
                    
                    if not headline or not url:
                        continue
                    
                    # Check if relevant to outbreaks
                    text_check = (headline + " " + summary).lower()
                    if any(kw in text_check for kw in monitor.outbreak_keywords):
                        # Create report with full assessment
                        report = monitor.create_report(
                            headline=headline,
                            source=source,
                            url=url,
                            summary=summary
                        )
                        results["reports_created"] += 1
                        results["articles_found"] += 1
                        
                except Exception as e:
                    results["errors"].append(f"Article processing error: {str(e)}")
                    
        except Exception as e:
            results["errors"].append(f"Search error for '{query_config.query}': {str(e)}")
    
    # Mark run complete
    monitor.mark_run_complete()
    
    return results


def format_report_summary(report) -> str:
    """Format a report for display."""
    return f"""
📋 Report: {report.headline[:60]}...
   Source: {report.source}
   Threat: {report.threat_level.value.upper()}
   Origin: {report.origin_assessment.value} ({report.confidence_score:.0%} confidence)
   Time: {report.timestamp}
   URL: {report.url}
"""


def get_high_priority_brief(monitor) -> str:
    """Generate a brief of high-priority reports."""
    high_threat = monitor.get_high_threat_reports()
    lab_origin = monitor.get_lab_origin_reports()
    
    brief = f"""
════════════════════════════════════════════════════════════
CONTINUOUS INTELLIGENCE BRIEF
Generated: {datetime.now().isoformat()}
════════════════════════════════════════════════════════════

THREAT LEVEL SUMMARY:
• Critical/High Priority Reports: {len(high_threat)}
• Lab-Associated Origin Reports: {len(lab_origin)}

"""
    
    if high_threat:
        brief += "⚠️ HIGH PRIORITY THREATS:\n"
        for r in high_threat[:10]:
            brief += format_report_summary(r)
    
    if lab_origin:
        brief += "\n🔬 LAB ORIGIN ASSESSMENTS:\n"
        for r in lab_origin[:10]:
            brief += format_report_summary(r)
    
    return brief
