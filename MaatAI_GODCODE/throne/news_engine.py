#!/usr/bin/env python3
"""
News & Article Intelligence Engine
Aggregates news from multiple sources, virus/health data, sentiment analysis
"""

import asyncio
import hashlib
import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from collections import defaultdict
import re

# ============== DATA STRUCTURES ==============

class NewsCategory(Enum):
    GEOPOLITICS = "geopolitics"
    ECONOMICS = "economics"
    HEALTH = "health"
    TECHNOLOGY = "technology"
    ENVIRONMENT = "environment"
    MILITARY = "military"
    ENERGY = "energy"
    GENERAL = "general"

class Sentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"

@dataclass
class NewsArticle:
    article_id: str
    title: str
    summary: str
    source: str
    url: str
    published_at: float
    category: NewsCategory
    
    # Analysis
    sentiment: Sentiment = Sentiment.NEUTRAL
    entities: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    locations: List[str] = field(default_factory=list)
    
    # Reliability
    source_reliability: float = 0.5
    bias_indicators: List[str] = field(default_factory=list)
    
    # Cross-reference
    crossref_score: float = 0.0  # How many sources confirm
    narrative_tags: List[str] = field(default_factory=list)

@dataclass
class VirusData:
    pathogen: str
    location: str
    confirmed_cases: int = 0
    deaths: int = 0
    recovered: int = 0
    last_update: float = 0
    source: str = ""
    variant: Optional[str] = None
    trend: str = "stable"  # growing, declining, stable

@dataclass
class NarrativeAnalysis:
    """Track how a story evolves across sources"""
    narrative_id: str
    first_appearance: float
    headline: str
    sources: List[str] = field(default_factory=list)
    articles: List[str] = field(default_factory=list)  # article_ids
    
    # Evolution tracking
    headline_variations: List[str] = field(default_factory=list)
    sentiment_timeline: List[tuple] = field(default_factory=list)  # (time, sentiment)
    
    # Analysis
    dominant_narrative: str = ""
    alternative_narratives: List[str] = field(default_factory=list)
    divergence_score: float = 0.0  # How much stories differ
    verified: bool = False

# ============== NEWS ENGINE ==============

class NewsEngine:
    """
    Aggregates and analyzes news from multiple sources
    Tracks narrative evolution, detects disinformation patterns
    """
    
    def __init__(self):
        self.articles: Dict[str, NewsArticle] = {}
        self.narratives: Dict[str, NarrativeAnalysis] = {}
        self.virus_data: Dict[str, VirusData] = {}
        
        # Source tracking
        self.sources: Dict[str, Dict] = {
            "reuters": {"name": "Reuters", "reliability": 0.9, "bias": "center"},
            "ap": {"name": "Associated Press", "reliability": 0.9, "bias": "center"},
            "bbc": {"name": "BBC", "reliability": 0.85, "bias": "center-left"},
            "nyt": {"name": "NY Times", "reliability": 0.8, "bias": "left"},
            "fox": {"name": "Fox News", "reliability": 0.6, "bias": "right"},
            "oann": {"name": "One America News", "reliability": 0.4, "bias": "far-right"},
            "rt": {"name": "RT", "reliability": 0.5, "bias": "state-propaganda"},
            "cgtn": {"name": "CGTN", "reliability": 0.5, "bias": "state-propaganda"},
            "tass": {"name": "TASS", "reliability": 0.5, "bias": "state-propaganda"},
            "xinhua": {"name": "Xinhua", "reliability": 0.5, "bias": "state-propaganda"},
        }
        
        # Keywords for categorization
        self.category_keywords = {
            NewsCategory.GEOPOLITICS: ["war", "conflict", "diplomacy", "sanctions", "treaty", "military", "invasion"],
            NewsCategory.ECONOMICS: ["economy", "gdp", "inflation", "recession", "trade", "market", "stock"],
            NewsCategory.HEALTH: ["virus", "pandemic", "outbreak", "vaccine", "cases", "deaths", "health"],
            NewsCategory.ENERGY: ["oil", "gas", "energy", "petroleum", "pipeline", "opec", "crude"],
            NewsCategory.MILITARY: ["military", "army", "navy", "air force", "weapon", "drone", "missile"],
            NewsCategory.ENVIRONMENT: ["climate", "emissions", "carbon", "pollution", "disaster", "flood", "fire"],
            NewsCategory.TECHNOLOGY: ["tech", "ai", "cyber", "space", "satellite", "software"],
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            "countries": r'\b(USA|Russia|China|Iran|North Korea|Syria|Ukraine|Israel|Germany|UK|France|Japan|India|Brazil|South Africa|Australia|Canada)\b',
            "organizations": r'\b(UN|NATO|WHO|OECD|OPEC|EU|IMF|World Bank|FBI|CIA|MI6|MOSAD)\b',
            "people": r'\b(Putin|Biden|Xi|Trump|Netanyahu|Zelensky|Kim|Macron|Merkel)\b',
        }
        
        self.last_update: float = 0
    
    # ============== ARTICLE PROCESSING ==============
    
    def add_article(self, article: NewsArticle):
        """Process and store article"""
        # Generate ID
        if not article.article_id:
            article.article_id = hashlib.md5(
                (article.url + article.title).encode()
            ).hexdigest()[:12]
        
        # Categorize
        article.category = self._categorize(article)
        
        # Extract entities
        article.entities = self._extract_entities(article.title + " " + article.summary)
        
        # Get source reliability
        source_key = article.source.lower()[:20]
        if source_key in self.sources:
            article.source_reliability = self.sources[source_key]["reliability"]
        
        self.articles[article.article_id] = article
        
        # Track narrative
        self._track_narrative(article)
    
    def _categorize(self, article: NewsArticle) -> NewsCategory:
        """Auto-categorize article"""
        text = (article.title + " " + article.summary).lower()
        
        for category, keywords in self.category_keywords.items():
            if any(kw in text for kw in keywords):
                return category
        
        return NewsCategory.GENERAL
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities"""
        entities = []
        
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities.extend(matches)
        
        return list(set(entities))
    
    # ============== NARRATIVE TRACKING ==============
    
    def _track_narrative(self, article: NewsArticle):
        """Track how narratives evolve"""
        # Create narrative key from keywords/entities
        key_entities = article.entities[:3] if article.entities else []
        if not key_entities:
            key_entities = article.keywords[:3] if article.keywords else ["general"]
        
        narrative_key = "_".join(sorted(set([e.lower() for e in key_entities])))
        
        if narrative_key not in self.narratives:
            self.narratives[narrative_key] = NarrativeAnalysis(
                narrative_id=narrative_key,
                first_appearance=article.published_at,
                headline=article.title[:100]
            )
        
        narrative = self.narratives[narrative_key]
        narrative.sources.append(article.source)
        narrative.articles.append(article.article_id)
        narrative.sentiment_timeline.append((article.published_at, article.sentiment.value))
        
        # Track headline variations
        if article.title not in narrative.headline_variations:
            narrative.headline_variations.append(article.title[:100])
        
        # Update divergence score
        unique_sources = len(set(narrative.sources))
        narrative.divergence_score = min(unique_sources / 10, 1.0)  # Max out at 10 sources
        
        # Cross-reference score
        article.crossref_score = unique_sources / max(len(self.sources), 1)
    
    # ============== VIRUS/HEALTH TRACKING ==============
    
    def update_virus_data(self, data: VirusData):
        """Update disease tracking data"""
        key = f"{data.pathogen}_{data.location}".lower().replace(" ", "_")
        self.virus_data[key] = data
    
    def get_outbreaks(self) -> List[Dict]:
        """Get active outbreaks"""
        outbreaks = []
        for data in self.virus_data.values():
            if data.trend == "growing":
                outbreaks.append(asdict(data))
        return sorted(outbreaks, key=lambda x: x["confirmed_cases"], reverse=True)
    
    # ============== SEARCH & RETRIEVAL ==============
    
    def search(self, query: str, category: Optional[NewsCategory] = None,
               since: Optional[float] = None, limit: int = 50) -> List[NewsArticle]:
        """Search articles"""
        results = []
        query_lower = query.lower()
        
        for article in self.articles.values():
            # Filter by category
            if category and article.category != category:
                continue
            
            # Filter by time
            if since and article.published_at < since:
                continue
            
            # Search
            if (query_lower in article.title.lower() or
                query_lower in article.summary.lower() or
                any(query_lower in e.lower() for e in article.entities)):
                results.append(article)
        
        # Sort by date, newest first
        results.sort(key=lambda a: a.published_at, reverse=True)
        return results[:limit]
    
    def get_headlines(self, category: Optional[NewsCategory] = None) -> List[Dict]:
        """Get latest headlines"""
        articles = list(self.articles.values())
        
        if category:
            articles = [a for a in articles if a.category == category]
        
        # Group by source for diversity
        by_source = defaultdict(list)
        for article in articles:
            by_source[article.source].append(article)
        
        # Take top from each source
        headlines = []
        for source, source_articles in by_source.items():
            if source_articles:
                headlines.append(asdict(max(source_articles, key=lambda a: a.published_at)))
        
        return sorted(headlines, key=lambda x: x["published_at"], reverse=True)[:20]
    
    # ============== NARRATIVE ANALYSIS ==============
    
    def analyze_narrative(self, narrative_id: str) -> Optional[Dict]:
        """Get detailed narrative analysis"""
        if narrative_id not in self.narratives:
            return None
        
        narrative = self.narratives[narrative_id]
        
        # Get all articles in this narrative
        narrative_articles = [self.articles[a] for a in narrative.articles if a in self.articles]
        
        # Calculate sentiment distribution
        sentiment_dist = defaultdict(int)
        for article in narrative_articles:
            sentiment_dist[article.sentiment.value] += 1
        
        # Find common keywords
        all_keywords = []
        for article in narrative_articles:
            all_keywords.extend(article.keywords)
        
        return {
            "narrative": asdict(narrative),
            "article_count": len(narrative_articles),
            "sources": list(set(narrative.sources)),
            "sentiment_distribution": dict(sentiment_dist),
            "common_keywords": list(set(all_keywords))[:20],
            "divergence_score": narrative.divergence_score,
            "crossref_estimate": len(set(narrative.sources)) / max(len(self.sources), 1)
        }
    
    # ============== DIVERSITY SCORE ==============
    
    def get_diversity_score(self) -> Dict:
        """Calculate source diversity score"""
        if not self.articles:
            return {"score": 0, "sources": [], "analysis": "No articles"}
        
        sources = [a.source for a in self.articles.values()]
        unique_sources = len(set(sources))
        total = len(sources)
        
        # Calculate bias distribution
        bias_counts = defaultdict(int)
        for source in sources:
            source_key = source.lower()[:20]
            if source_key in self.sources:
                bias_counts[self.sources[source_key]["bias"]] += 1
        
        return {
            "score": unique_sources / max(len(self.sources), 1),
            "unique_sources": unique_sources,
            "total_articles": total,
            "bias_distribution": dict(bias_counts),
            "analysis": "Diverse" if unique_sources > 5 else "Limited"
        }
    
    # ============== EXPORT ==============
    
    def to_dict(self) -> Dict:
        """Export news engine state"""
        return {
            "articles": {k: asdict(v) for k, v in list(self.articles.items())[-200:]},
            "narratives": {k: asdict(v) for k, v in list(self.narratives.items())[:50]},
            "outbreaks": self.get_outbreaks(),
            "diversity": self.get_diversity_score(),
            "headlines": self.get_headlines()[:10],
            "stats": {
                "total_articles": len(self.articles),
                "total_narratives": len(self.narratives),
                "tracked_outbreaks": len(self.virus_data)
            }
        }


# Demo
if __name__ == "__main__":
    engine = NewsEngine()
    
    # Add demo articles
    demo_articles = [
        NewsArticle(
            article_id="demo1",
            title="Oil Prices Surge Amid Middle East Tensions",
            summary="Crude oil futures jumped 3% as concerns grew over potential supply disruptions.",
            source="Reuters",
            url="https://reuters.com/demo/oil-prices",
            published_at=time.time() - 3600,
            category=NewsCategory.ENERGY,
            sentiment=Sentiment.NEGATIVE,
            entities=["Oil", "Middle East", "OPEC"],
            keywords=["oil", "prices", "tensions", "supply"]
        ),
        NewsArticle(
            article_id="demo2", 
            title="Global COVID Cases Rise in New Variants",
            summary="WHO reports increase in cases across Europe and Asia with new variant strains.",
            source="BBC",
            url="https://bbc.com/demo/covid",
            published_at=time.time() - 7200,
            category=NewsCategory.HEALTH,
            sentiment=Sentiment.NEGATIVE,
            entities=["WHO", "Europe", "Asia"],
            keywords=["covid", "cases", "variant"]
        ),
        NewsArticle(
            article_id="demo3",
            title="US Military Increases Patrols in South China Sea",
            summary="American warships conducting freedom of navigation operations amid tensions.",
            source="AP",
            url="https://ap.com/demo/south-china-sea",
            published_at=time.time() - 1800,
            category=NewsCategory.MILITARY,
            sentiment=Sentiment.NEUTRAL,
            entities=["US", "China", "South China Sea"],
            keywords=["military", "warships", "patrols"]
        )
    ]
    
    for article in demo_articles:
        engine.add_article(article)
    
    print(json.dumps(engine.to_dict(), indent=2))
