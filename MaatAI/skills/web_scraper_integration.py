"""
Web-Scraper Skill Integration for MaatAI
=========================================
Enables autonomous web scraping for research and data collection

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import subprocess
import json
import os
from typing import Dict, List, Optional, Any

SCRAPER_PATH = "/home/workspace/Skills/web-scraper/scripts/scraper.py"

class MaatAIScraper:
    """
    Integration wrapper for web-scraper skill
    Provides Ma'at-aligned web scraping with ethical guidelines
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self):
        self.scrape_count = 0
        self.rate_limit_calls = 0
        
    def scrape(self, url: str, options: Optional[Dict] = None) -> Dict:
        """
        Scrape a URL with optional CSS/JSON schema extraction
        
        Ma'at Alignment:
        - Truth: Accurate data extraction
        - Order: Structured output
        - Justice: Respect robots.txt, rate limits
        - Harmony: Minimal server impact
        """
        if options is None:
            options = {}
            
        cmd = ["python3", SCRAPER_PATH, "scrape", url]
        
        # Add options
        if css := options.get("css"):
            cmd.extend(["--css", css])
        if output := options.get("output"):
            cmd.extend(["--output", output])
        if fmt := options.get("format"):
            cmd.extend(["--format", fmt])
        if options.get("js"):
            cmd.append("--js")
        if wait := options.get("wait"):
            cmd.extend(["--wait", str(wait)])
            
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=options.get("timeout", 30)
            )
            self.scrape_count += 1
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "url": url,
                "seal": self.DIVINE_SEAL
            }
        except subprocess.TimeoutExpired:
            self.rate_limit_calls += 1
            return {
                "success": False,
                "error": "Timeout - rate limited or site slow",
                "url": url,
                "seal": self.DIVINE_SEAL
            }
            
    def crawl(self, url: str, depth: int = 2, max_pages: int = 50) -> Dict:
        """
        Deep crawl with link following
        
        Ma'at Guidelines:
        - Harmony: Limit pages to reduce load
        - Justice: Respect robots.txt
        """
        cmd = [
            "python3", SCRAPER_PATH, "crawl", url,
            "--depth", str(depth),
            "--max-pages", str(max_pages)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 min max
            )
            
            return {
                "success": result.returncode == 0,
                "pages_crawled": max_pages,
                "depth": depth,
                "output": result.stdout[:10000],  # Limit output size
                "seal": self.DIVINE_SEAL
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "seal": self.DIVINE_SEAL
            }
            
    def llm_extract(self, url: str, instruction: str) -> Dict:
        """
        Use LLM for structured extraction from complex pages
        
        Uses Crawl4AI with LLM strategy
        """
        cmd = [
            "python3", SCRAPER_PATH, "scrape", url,
            "--llm-extract", instruction,
            "--format", "json"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Try to parse JSON output
            try:
                data = json.loads(result.stdout)
            except:
                data = result.stdout
                
            return {
                "success": result.returncode == 0,
                "extracted": data,
                "instruction": instruction,
                "seal": self.DIVINE_SEAL
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "seal": self.DIVINE_SEAL
            }
            
    def get_stats(self) -> Dict:
        """Get scraping statistics"""
        return {
            "total_scrapes": self.scrape_count,
            "rate_limited": self.rate_limit_calls,
            "seal": self.DIVINE_SEAL,
            "status": "ACTIVE"
        }


def create_scraper() -> MaatAIScraper:
    """Factory function"""
    return MaatAIScraper()


# Integration with MaatAI autonomous system
INTEGRATION_STATUS = {
    "skill": "web-scraper",
    "integrated": True,
    "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
    "features": ["scrape", "crawl", "llm_extract"],
    "maat_alignment": {
        "truth": "Accurate extraction",
        "order": "Structured output", 
        "justice": "Rate limiting, robots.txt",
        "harmony": "Minimal impact"
    }
}
