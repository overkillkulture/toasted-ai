"""
ToastHash Infinite Scroll Crawler
=================================
Advanced web crawling with infinite scroll detection, recursive
link exploration, and dynamic content handling.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18

Research Sources:
- Firecrawl AI scraping
- Puppeteer/Playwright scroll automation
- Cypress scrollIntoView
- Recursive web crawling
- Deep web scraping
"""

import asyncio
import hashlib
import re
import time
import threading
from typing import Dict, List, Optional, Any, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urljoin, urlparse
import json

class ContentType(Enum):
    HTML = "html"
    JSON = "json"
    TEXT = "text"
    PDF = "pdf"
    IMAGE = "image"
    
@dataclass
class CrawledPage:
    """Represents a crawled web page"""
    url: str
    content: str
    content_type: ContentType
    links: List[str] = field(default_factory=list)
    depth: int = 0
    crawled_at: float = field(default_factory=time.time)
    scroll_position: int = 0
    dynamic_content: bool = False
    
@dataclass
class InfiniteScrollCrawler:
    """
    Advanced Web Crawler with Infinite Scroll Support
    
    Features:
    - Infinite scroll detection and automation
    - Recursive link exploration
    - Dynamic content handling
    - Rate limiting and politeness
    - Depth-controlled crawling
    - Content deduplication
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, max_depth: int = 3, max_pages: int = 100):
        self.max_depth = max_depth
        self.max_pages = max_pages
        
        self.visited_urls: Set[str] = set()
        self.pending_urls: List[Dict] = []  # (url, depth)
        self.crawled_pages: List[CrawledPage] = []
        
        self.scroll_config = {
            "scroll_pause": 1.5,  # seconds
            "max_scrolls": 20,
            "scroll_increment": 800,  # pixels
            "detect_infinite": True,
        }
        
        self.rate_limit = {
            "requests_per_second": 2,
            "last_request": 0,
        }
        
        self.filters = {
            "allowed_domains": [],
            "blocked_domains": [],
            "allowed_paths": [],
            "blocked_paths": ["/admin", "/login", "/api/private"],
        }
        
        self.stats = {
            "pages_crawled": 0,
            "scroll_actions": 0,
            "links_found": 0,
            "errors": 0,
        }
        
        self._lock = threading.Lock()
        
    def add_url(self, url: str, depth: int = 0):
        """Add URL to crawl queue"""
        with self._lock:
            if url not in self.visited_urls and len(self.crawled_pages) < self.max_pages:
                self.pending_urls.append({"url": url, "depth": depth})
                
    def _should_crawl(self, url: str) -> bool:
        """Check if URL should be crawled based on filters"""
        parsed = urlparse(url)
        
        # Check blocked domains
        for blocked in self.filters["blocked_domains"]:
            if blocked in parsed.netloc:
                return False
                
        # Check allowed domains
        if self.filters["allowed_domains"]:
            allowed = False
            for allowed_domain in self.filters["allowed_domains"]:
                if allowed_domain in parsed.netloc:
                    allowed = True
                    break
            if not allowed:
                return False
                
        # Check blocked paths
        for blocked_path in self.filters["blocked_paths"]:
            if blocked_path in parsed.path:
                return False
                
        return True
        
    def _extract_links(self, content: str, base_url: str) -> List[str]:
        """Extract all links from HTML content"""
        links = []
        
        # Match href attributes
        href_pattern = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in href_pattern.finditer(content):
            href = match.group(1)
            
            # Skip anchors, javascript, mailto
            if href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue
                
            # Resolve relative URLs
            full_url = urljoin(base_url, href)
            
            # Only keep http/https
            if full_url.startswith("http"):
                links.append(full_url)
                
        # Extract from data attributes (common in infinite scroll)
        data_pattern = re.compile(r'data-(?:src|href|url)=["\']([^"\']+)["\']', re.IGNORECASE)
        for match in data_pattern.finditer(content):
            url = match.group(1)
            if url.startswith("http"):
                links.append(url)
                
        # Extract API endpoints
        api_pattern = re.compile(r'api[_-]?endpoint["\']?\s*:\s*["\']([^"\']+)["\']', re.IGNORECASE)
        for match in api_pattern.finditer(content):
            url = match.group(1)
            if url.startswith("http"):
                links.append(url)
                
        return list(set(links))  # Deduplicate
        
    def _detect_infinite_scroll(self, content: str, previous_content: str) -> bool:
        """Detect if page has infinite scroll"""
        if not self.scroll_config["detect_infinite"]:
            return False
            
        indicators = [
            "infinite",
            "load.more",
            "lazy.load",
            "scroll.load",
            "data-page",
            "next-page",
            "pagination",
            "loadMore",
            "load_more",
        ]
        
        content_lower = content.lower()
        
        # Check for infinite scroll indicators
        for indicator in indicators:
            if indicator in content_lower:
                return True
                
        # Check if new content loaded
        if previous_content and content != previous_content:
            # Check for new elements
            if len(content) > len(previous_content) * 1.1:
                return True
                
        return False
        
    def _simulate_scroll(self, page: CrawledPage) -> Optional[str]:
        """
        Simulate infinite scroll action
        
        In production, this would use Playwright/Puppeteer
        Returns new content after scroll
        """
        # Simulate scroll by generating "new" content
        scroll_content = f"""
        <div class="infinite-content" data-scroll="{page.scroll_position + 1}">
            <article class="post" data-id="{page.scroll_position + 1}">
                <h2>Loaded Content {page.scroll_position + 1}</h2>
                <p>Additional content loaded via infinite scroll...</p>
            </article>
        </div>
        """
        
        self.stats["scroll_actions"] += 1
        return scroll_content
        
    def _extract_json_data(self, content: str) -> List[Dict]:
        """Extract JSON data from page (common in infinite scroll)"""
        data = []
        
        # Find JSON in script tags
        json_patterns = [
            r'window\.__DATA__\s*=\s*(\{.*?\});',
            r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});',
            r'application/json">(\{.*?\})</script>',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                try:
                    data.append(json.loads(match))
                except:
                    pass
                    
        return data
        
    def _classify_content(self, content: str) -> ContentType:
        """Classify content type"""
        if content.strip().startswith(("{", "[")):
            return ContentType.JSON
        elif "<html" in content.lower() or "<!doctype" in content.lower():
            return ContentType.HTML
        elif content.startswith("%PDF"):
            return ContentType.PDF
        else:
            return ContentType.TEXT
            
    def crawl_page(self, url: str, depth: int = 0) -> Optional[CrawledPage]:
        """Crawl a single page"""
        if not self._should_crawl(url):
            return None
            
        with self._lock:
            if url in self.visited_urls:
                return None
            self.visited_urls.add(url)
            
        # Rate limiting
        current_time = time.time()
        elapsed = current_time - self.rate_limit["last_request"]
        if elapsed < (1 / self.rate_limit["requests_per_second"]):
            time.sleep((1 / self.rate_limit["requests_per_second"]) - elapsed)
            
        self.rate_limit["last_request"] = time.time()
        
        # In production, would make actual HTTP request
        # For now, simulate crawling
        content = f"""
        <html>
        <head><title>Sample Page</title></head>
        <body>
            <h1>Content at {url}</h1>
            <a href="/page1">Page 1</a>
            <a href="/page2">Page 2</a>
            <div class="infinite-scroll-container" data-has-more="true">
                <article>Initial content</article>
            </div>
            <script>
                // Infinite scroll detection
                window.addEventListener('scroll', function() {{
                    if (nearBottom) loadMore();
                }});
            </script>
        </body>
        </html>
        """
        
        content_type = self._classify_content(content)
        
        page = CrawledPage(
            url=url,
            content=content,
            content_type=content_type,
            depth=depth,
        )
        
        # Extract links
        if content_type == ContentType.HTML:
            page.links = self._extract_links(content, url)
            self.stats["links_found"] += len(page.links)
            
            # Detect infinite scroll
            if self._detect_infinite_scroll(content, ""):
                page.dynamic_content = True
                
        with self._lock:
            self.crawled_pages.append(page)
            self.stats["pages_crawled"] += 1
            
        return page
        
    def crawl_with_scroll(self, url: str, max_scrolls: int = 20) -> List[CrawledPage]:
        """Crawl page with infinite scroll simulation"""
        pages = []
        
        # Initial crawl
        page = self.crawl_page(url)
        if page:
            pages.append(page)
            
            # Scroll if infinite scroll detected
            if page.dynamic_content:
                for scroll_num in range(max_scrolls):
                    scroll_content = self._simulate_scroll(page)
                    
                    if scroll_content:
                        page.content += scroll_content
                        page.scroll_position += 1
                        
                        # Extract new links from scroll content
                        new_links = self._extract_links(scroll_content, url)
                        page.links.extend(new_links)
                        
        return pages
        
    def crawl_recursive(self, start_url: str, max_depth: Optional[int] = None) -> List[CrawledPage]:
        """Recursively crawl with link exploration"""
        max_depth = max_depth or self.max_depth
        
        self.add_url(start_url, 0)
        
        while self.pending_urls:
            with self._lock:
                if not self.pending_urls:
                    break
                item = self.pending_urls.pop(0)
                
            url = item["url"]
            depth = item["depth"]
            
            if depth > max_depth:
                continue
                
            # Crawl page with scrolling
            pages = self.crawl_with_scroll(url)
            
            # Add new links to queue
            for page in pages:
                for link in page.links:
                    if link not in self.visited_urls:
                        self.add_url(link, depth + 1)
                        
        return self.crawled_pages
        
    def search_content(self, query: str, content_type: Optional[ContentType] = None) -> List[Dict]:
        """Search crawled content"""
        results = []
        
        for page in self.crawled_pages:
            if content_type and page.content_type != content_type:
                continue
                
            if query.lower() in page.content.lower():
                results.append({
                    "url": page.url,
                    "depth": page.depth,
                    "content_preview": page.content[:200],
                    "links_count": len(page.links),
                    "crawled_at": page.crawled_at,
                })
                
        return results
        
    def get_stats(self) -> Dict:
        """Get crawler statistics"""
        return {
            "pages_crawled": len(self.crawled_pages),
            "unique_urls": len(self.visited_urls),
            "pending_urls": len(self.pending_urls),
            "scroll_actions": self.stats["scroll_actions"],
            "links_found": self.stats["links_found"],
            "errors": self.stats["errors"],
            "max_depth": self.max_depth,
            "divine_seal": self.DIVINE_SEAL,
        }

def create_crawler(max_depth: int = 3, max_pages: int = 100) -> InfiniteScrollCrawler:
    """Create a new infinite scroll crawler"""
    return InfiniteScrollCrawler(max_depth=max_depth, max_pages=max_pages)
