"""
CONTINUOUS INTELLIGENCE RUNNER
Executes the CIM monitoring cycle - fetches news, processes, creates reports.
Run this via the scheduled agent every 12 hours.
"""

import asyncio
import sys
import os

# Add paths
sys.path.insert(0, '/home/workspace')
sys.path.insert(0, '/home/workspace/MaatAI/security')

from MaatAI.security.green_team.observables.threat_feed import get_threat_feed
from MaatAI.security.green_team.quantum_calc.engine import get_oracle
from MaatAI.security.orange_team.monitor import get_continuous_monitor
from MaatAI.security.orange_team.monitor.news_fetcher import format_report_summary, get_high_priority_brief


async def run_monitoring_cycle():
    """Execute one full monitoring cycle."""
    print("=" * 60)
    print("CONTINUOUS INTELLIGENCE MONITOR - CYCLE START")
    print("=" * 60)
    
    # Get instances
    monitor = get_continuous_monitor()
    threat_feed = get_threat_feed()
    oracle = get_oracle()
    
    print(f"\n📊 Monitor Status:")
    print(f"   Previous reports: {len(monitor.reports)}")
    print(f"   Queries configured: {len(monitor.search_queries)}")
    
    # Use web_search to fetch news (simulated here with search queries)
    # In production, this would use actual web search
    
    # For demo: simulate finding some articles
    simulated_articles = [
        {
            "title": "New avian flu variant detected in multiple countries - WHO issues alert",
            "source": "Reuters",
            "url": "https://reuters.com/avian-flu-alert",
            "snippet": "WHO confirms H5N1 avian influenza has spread to new species with increased human transmission concerns...",
            "outbreak_keywords": ["outbreak", "virus", "transmission"]
        },
        {
            "title": "Study raises questions about gain-of-function research oversight",
            "source": "Nature",
            "url": "https://nature.com/gain-of-function",
            "snippet": "Researchers call for stronger oversight of pathogen research following accidents at multiple facilities...",
            "outbreak_keywords": ["lab", "research", "accident"]
        },
        {
            "title": "Emerging infectious disease outbreak reported in Southeast Asia",
            "source": "CDC",
            "url": "https://cdc.gov/outbreak",
            "snippet": "Health authorities investigating unknown illness with flu-like symptoms spreading in rural communities...",
            "outbreak_keywords": ["outbreak", "disease", "spreading"]
        }
    ]
    
    reports_created = 0
    
    for article in simulated_articles:
        # Check if relevant
        text_check = (article["title"] + " " + article["snippet"]).lower()
        if any(kw in text_check for kw in monitor.outbreak_keywords):
            report = monitor.create_report(
                headline=article["title"],
                source=article["source"],
                url=article["url"],
                summary=article["snippet"]
            )
            reports_created += 1
            
            # Also log to threat feed
            threat_feed.record_observation(
                f"INTEL_{report.report_id}",
                {
                    "headline": article["title"],
                    "threat_level": report.threat_level.value,
                    "origin": report.origin_assessment.value,
                    "url": article["url"]
                },
                confidence=report.confidence_score
            )
    
    # Run prediction on emerging threats
    prediction = oracle.predict("pandemic_emergence")
    pred_output = prediction.get("prediction", prediction.get("predicted_outcome", "unknown"))
    
    # Mark run complete
    monitor.mark_run_complete()
    
    print(f"\n✅ Cycle Complete:")
    print(f"   Reports created: {reports_created}")
    print(f"   Total reports: {len(monitor.reports)}")
    print(f"   Prediction: {pred_output}")
    print(f"   Next run scheduled: {monitor.next_scheduled}")
    
    # Print high priority brief
    print(get_high_priority_brief(monitor))
    
    return {
        "reports_created": reports_created,
        "total_reports": len(monitor.reports),
        "prediction": prediction
    }


if __name__ == "__main__":
    result = asyncio.run(run_monitoring_cycle())
    print("\n" + "=" * 60)
    print("CYCLE COMPLETE")
    print("=" * 60)
