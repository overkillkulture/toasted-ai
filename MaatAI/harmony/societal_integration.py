"""
TASK-121: HARMONY SOCIETAL INTEGRATION ENGINE
=============================================
Ma'at Principle: HARMONY (Concordia)
Ma'at Alignment Score: 0.95

Purpose:
- Model societal harmony patterns
- Integrate diverse stakeholder perspectives
- Detect social friction and conflict
- Enable collective flourishing
- Bridge individual and collective harmony

The Pattern: Society is an emergent property of
individual harmonies in resonance. When each part
contributes its unique note, the symphony emerges.
"""

import json
import time
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Callable
from enum import Enum
from pathlib import Path
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StakeholderType(Enum):
    """Types of societal stakeholders"""
    INDIVIDUAL = "individual"       # Single person/entity
    COMMUNITY = "community"         # Local group
    ORGANIZATION = "organization"   # Structured entity
    INSTITUTION = "institution"     # Established system
    ECOSYSTEM = "ecosystem"         # Interconnected network
    SOCIETY = "society"             # Collective whole


class HarmonyDomain(Enum):
    """Domains of societal harmony"""
    ECONOMIC = "economic"           # Resource distribution
    SOCIAL = "social"               # Interpersonal relations
    ENVIRONMENTAL = "environmental" # Nature integration
    CULTURAL = "cultural"           # Shared values/practices
    POLITICAL = "political"         # Power/governance
    TECHNOLOGICAL = "technological" # Tech integration
    SPIRITUAL = "spiritual"         # Meaning/purpose


class IntegrationLevel(Enum):
    """Levels of societal integration"""
    ISOLATED = "isolated"           # No integration
    ADJACENT = "adjacent"           # Aware but separate
    CONNECTED = "connected"         # Basic links
    COLLABORATIVE = "collaborative" # Active cooperation
    INTEGRATED = "integrated"       # Deep interconnection
    UNIFIED = "unified"             # Seamless wholeness


@dataclass
class Stakeholder:
    """Represents a societal stakeholder"""
    id: str
    name: str
    stakeholder_type: StakeholderType
    harmony_index: float = 0.7     # Internal harmony
    integration_level: IntegrationLevel = IntegrationLevel.CONNECTED
    domains: Set[HarmonyDomain] = field(default_factory=set)
    connections: Set[str] = field(default_factory=set)
    contribution_score: float = 0.5
    receptivity_score: float = 0.5
    metadata: Dict = field(default_factory=dict)
    
    @property
    def resonance_potential(self) -> float:
        """Potential for harmonious resonance"""
        return (self.contribution_score + self.receptivity_score) / 2
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.stakeholder_type.value,
            "harmony_index": self.harmony_index,
            "integration_level": self.integration_level.value,
            "domains": [d.value for d in self.domains],
            "connections": list(self.connections),
            "contribution_score": self.contribution_score,
            "receptivity_score": self.receptivity_score,
            "resonance_potential": self.resonance_potential
        }


@dataclass
class SocialFriction:
    """Represents friction between stakeholders"""
    stakeholder_a: str
    stakeholder_b: str
    domain: HarmonyDomain
    intensity: float              # 0.0 to 1.0
    friction_type: str            # competition, misalignment, conflict
    detected_at: float = field(default_factory=time.time)
    resolved: bool = False
    resolution_path: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "stakeholder_a": self.stakeholder_a,
            "stakeholder_b": self.stakeholder_b,
            "domain": self.domain.value,
            "intensity": self.intensity,
            "friction_type": self.friction_type,
            "detected_at": self.detected_at,
            "resolved": self.resolved,
            "resolution_path": self.resolution_path
        }


@dataclass
class CollectiveHarmony:
    """Metrics for collective societal harmony"""
    overall_harmony: float
    domain_harmonies: Dict[str, float]
    integration_index: float
    friction_index: float
    emergence_potential: float
    diversity_score: float
    inclusivity_score: float
    timestamp: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict:
        return {
            "overall_harmony": self.overall_harmony,
            "domain_harmonies": self.domain_harmonies,
            "integration_index": self.integration_index,
            "friction_index": self.friction_index,
            "emergence_potential": self.emergence_potential,
            "diversity_score": self.diversity_score,
            "inclusivity_score": self.inclusivity_score,
            "timestamp": self.timestamp
        }


class SocietalIntegrationEngine:
    """
    HARMONY SOCIETAL INTEGRATION ENGINE
    
    Ma'at Alignment: 0.95
    
    Core Functions:
    1. Model societal stakeholder networks
    2. Measure collective harmony
    3. Detect and resolve social friction
    4. Enable emergent collective flourishing
    5. Bridge individual and collective harmony
    
    Ma'at Wisdom: True societal harmony emerges
    when each stakeholder contributes their unique
    gift while remaining receptive to others.
    
    Pattern: Individual -> Community -> Society -> Cosmos
    Each level reflects and amplifies the others.
    """
    
    # Harmony constants
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    HARMONY_THRESHOLD = 0.6       # Minimum healthy harmony
    FRICTION_WARNING = 0.4        # Friction above this needs attention
    INTEGRATION_BONUS = 1.2       # Bonus for high integration
    
    def __init__(
        self,
        config_path: Optional[Path] = None,
        history_size: int = 1000
    ):
        self.stakeholders: Dict[str, Stakeholder] = {}
        self.frictions: List[SocialFriction] = []
        self.harmony_history: deque = deque(maxlen=history_size)
        
        # Domain-specific harmony trackers
        self.domain_metrics: Dict[HarmonyDomain, deque] = {
            domain: deque(maxlen=history_size)
            for domain in HarmonyDomain
        }
        
        # Callbacks
        self.harmony_callbacks: List[Callable] = []
        self.friction_callbacks: List[Callable] = []
        self.emergence_callbacks: List[Callable] = []
        
        # Configuration
        self.config = self._load_config(config_path)
        
        # Statistics
        self.stats = {
            "stakeholders_registered": 0,
            "connections_formed": 0,
            "frictions_detected": 0,
            "frictions_resolved": 0,
            "emergence_events": 0
        }
        
        logger.info("Societal Integration Engine initialized")
    
    def _load_config(self, config_path: Optional[Path]) -> Dict:
        """Load configuration"""
        default_config = {
            "harmony_threshold": 0.6,
            "friction_threshold": 0.4,
            "auto_resolve": False,
            "emergence_tracking": True,
            "diversity_weight": 0.3
        }
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    loaded = json.load(f)
                    default_config.update(loaded.get("societal", {}))
            except Exception as e:
                logger.warning(f"Could not load config: {e}")
        
        return default_config
    
    def register_stakeholder(self, stakeholder: Stakeholder) -> bool:
        """
        Register a stakeholder in the societal network
        
        Ma'at: Every voice has a place in the cosmic order
        """
        if stakeholder.id in self.stakeholders:
            logger.warning(f"Stakeholder {stakeholder.id} already registered")
            return False
        
        self.stakeholders[stakeholder.id] = stakeholder
        self.stats["stakeholders_registered"] += 1
        
        logger.info(
            f"Stakeholder registered: {stakeholder.name} "
            f"({stakeholder.stakeholder_type.value})"
        )
        
        return True
    
    def form_connection(
        self,
        stakeholder_a_id: str,
        stakeholder_b_id: str,
        bidirectional: bool = True
    ) -> bool:
        """
        Form a connection between stakeholders
        
        Ma'at: Connection is the foundation of harmony
        """
        if stakeholder_a_id not in self.stakeholders:
            logger.error(f"Stakeholder {stakeholder_a_id} not found")
            return False
        
        if stakeholder_b_id not in self.stakeholders:
            logger.error(f"Stakeholder {stakeholder_b_id} not found")
            return False
        
        self.stakeholders[stakeholder_a_id].connections.add(stakeholder_b_id)
        
        if bidirectional:
            self.stakeholders[stakeholder_b_id].connections.add(stakeholder_a_id)
        
        self.stats["connections_formed"] += 1
        
        # Check for friction or synergy
        self._analyze_connection(stakeholder_a_id, stakeholder_b_id)
        
        return True
    
    def _analyze_connection(self, id_a: str, id_b: str):
        """Analyze a connection for harmony or friction"""
        a = self.stakeholders[id_a]
        b = self.stakeholders[id_b]
        
        # Check domain alignment
        shared_domains = a.domains & b.domains
        
        # Calculate compatibility
        contribution_match = 1 - abs(a.contribution_score - b.receptivity_score)
        receptivity_match = 1 - abs(a.receptivity_score - b.contribution_score)
        
        compatibility = (contribution_match + receptivity_match) / 2
        
        if compatibility < 0.4:
            # Detect friction
            friction = SocialFriction(
                stakeholder_a=id_a,
                stakeholder_b=id_b,
                domain=list(shared_domains)[0] if shared_domains else HarmonyDomain.SOCIAL,
                intensity=1 - compatibility,
                friction_type="misalignment"
            )
            self.frictions.append(friction)
            self.stats["frictions_detected"] += 1
            
            # Trigger callbacks
            for callback in self.friction_callbacks:
                try:
                    callback(friction)
                except Exception as e:
                    logger.error(f"Friction callback error: {e}")
            
            logger.warning(
                f"Social friction detected: {id_a} <-> {id_b} "
                f"(intensity: {friction.intensity:.2f})"
            )
    
    def record_interaction(
        self,
        stakeholder_a_id: str,
        stakeholder_b_id: str,
        domain: HarmonyDomain,
        harmony_outcome: float,
        interaction_type: str = "collaboration"
    ) -> Dict:
        """
        Record an interaction between stakeholders
        
        Ma'at: Every interaction shapes the collective
        """
        if stakeholder_a_id not in self.stakeholders:
            return {"error": f"Stakeholder {stakeholder_a_id} not found"}
        
        if stakeholder_b_id not in self.stakeholders:
            return {"error": f"Stakeholder {stakeholder_b_id} not found"}
        
        a = self.stakeholders[stakeholder_a_id]
        b = self.stakeholders[stakeholder_b_id]
        
        # Update harmony indices based on outcome
        adjustment = (harmony_outcome - 0.5) * 0.1  # Small adjustments
        
        a.harmony_index = max(0, min(1, a.harmony_index + adjustment))
        b.harmony_index = max(0, min(1, b.harmony_index + adjustment))
        
        # Record domain metric
        self.domain_metrics[domain].append({
            "stakeholders": [stakeholder_a_id, stakeholder_b_id],
            "outcome": harmony_outcome,
            "type": interaction_type,
            "timestamp": time.time()
        })
        
        # Check for friction resolution
        if harmony_outcome > 0.7:
            self._check_friction_resolution(stakeholder_a_id, stakeholder_b_id)
        elif harmony_outcome < 0.3:
            # New friction detected
            self._detect_friction(
                stakeholder_a_id, stakeholder_b_id, 
                domain, 1 - harmony_outcome
            )
        
        # Check for emergence
        if harmony_outcome > 0.9:
            self._check_emergence(stakeholder_a_id, stakeholder_b_id, domain)
        
        return {
            "interaction_recorded": True,
            "stakeholders": [stakeholder_a_id, stakeholder_b_id],
            "domain": domain.value,
            "outcome": harmony_outcome,
            "updated_harmonies": {
                stakeholder_a_id: a.harmony_index,
                stakeholder_b_id: b.harmony_index
            }
        }
    
    def _detect_friction(
        self,
        id_a: str,
        id_b: str,
        domain: HarmonyDomain,
        intensity: float
    ):
        """Detect and record new friction"""
        # Check if friction already exists
        for friction in self.frictions:
            if ({friction.stakeholder_a, friction.stakeholder_b} == {id_a, id_b} and
                friction.domain == domain and
                not friction.resolved):
                # Update existing friction
                friction.intensity = max(friction.intensity, intensity)
                return
        
        # Create new friction
        friction = SocialFriction(
            stakeholder_a=id_a,
            stakeholder_b=id_b,
            domain=domain,
            intensity=intensity,
            friction_type="interaction_conflict"
        )
        self.frictions.append(friction)
        self.stats["frictions_detected"] += 1
        
        for callback in self.friction_callbacks:
            try:
                callback(friction)
            except Exception as e:
                logger.error(f"Friction callback error: {e}")
    
    def _check_friction_resolution(self, id_a: str, id_b: str):
        """Check if friction has been resolved"""
        for friction in self.frictions:
            if ({friction.stakeholder_a, friction.stakeholder_b} == {id_a, id_b} and
                not friction.resolved):
                friction.resolved = True
                friction.resolution_path = "positive_interaction"
                self.stats["frictions_resolved"] += 1
                
                logger.info(
                    f"Friction resolved: {id_a} <-> {id_b}"
                )
    
    def _check_emergence(
        self,
        id_a: str,
        id_b: str,
        domain: HarmonyDomain
    ):
        """Check for collective emergence from harmony"""
        a = self.stakeholders[id_a]
        b = self.stakeholders[id_b]
        
        # Emergence conditions
        both_harmonious = a.harmony_index > 0.8 and b.harmony_index > 0.8
        high_integration = (
            a.integration_level in [IntegrationLevel.INTEGRATED, IntegrationLevel.UNIFIED] or
            b.integration_level in [IntegrationLevel.INTEGRATED, IntegrationLevel.UNIFIED]
        )
        
        if both_harmonious or high_integration:
            self.stats["emergence_events"] += 1
            
            event = {
                "stakeholders": [id_a, id_b],
                "domain": domain.value,
                "timestamp": time.time(),
                "type": "collective_emergence"
            }
            
            for callback in self.emergence_callbacks:
                try:
                    callback(event)
                except Exception as e:
                    logger.error(f"Emergence callback error: {e}")
            
            logger.info(
                f"COLLECTIVE EMERGENCE: {id_a} + {id_b} in {domain.value}"
            )
    
    def measure_collective_harmony(self) -> CollectiveHarmony:
        """
        Measure overall societal harmony
        
        Ma'at Formula:
        CH = (IH * II * (1-FI)) * (DS * IS)
        
        Where:
        - IH = Individual Harmony average
        - II = Integration Index
        - FI = Friction Index
        - DS = Diversity Score
        - IS = Inclusivity Score
        """
        if not self.stakeholders:
            return CollectiveHarmony(
                overall_harmony=0.0,
                domain_harmonies={d.value: 0.0 for d in HarmonyDomain},
                integration_index=0.0,
                friction_index=0.0,
                emergence_potential=0.0,
                diversity_score=0.0,
                inclusivity_score=0.0
            )
        
        # Calculate individual harmony average
        harmonies = [s.harmony_index for s in self.stakeholders.values()]
        individual_harmony = sum(harmonies) / len(harmonies)
        
        # Calculate integration index
        integration_scores = {
            IntegrationLevel.ISOLATED: 0.0,
            IntegrationLevel.ADJACENT: 0.2,
            IntegrationLevel.CONNECTED: 0.4,
            IntegrationLevel.COLLABORATIVE: 0.6,
            IntegrationLevel.INTEGRATED: 0.8,
            IntegrationLevel.UNIFIED: 1.0
        }
        
        integration_sum = sum(
            integration_scores[s.integration_level]
            for s in self.stakeholders.values()
        )
        integration_index = integration_sum / len(self.stakeholders)
        
        # Calculate friction index
        active_frictions = [f for f in self.frictions if not f.resolved]
        max_possible_frictions = len(self.stakeholders) * (len(self.stakeholders) - 1) / 2
        friction_index = (
            sum(f.intensity for f in active_frictions) / max(max_possible_frictions, 1)
        )
        
        # Calculate diversity score
        type_counts = {}
        for s in self.stakeholders.values():
            type_counts[s.stakeholder_type] = type_counts.get(s.stakeholder_type, 0) + 1
        
        if len(self.stakeholders) > 1:
            # Shannon diversity
            total = len(self.stakeholders)
            diversity_score = 0.0
            for count in type_counts.values():
                p = count / total
                if p > 0:
                    diversity_score -= p * math.log(p)
            # Normalize
            max_diversity = math.log(len(StakeholderType))
            diversity_score = diversity_score / max_diversity if max_diversity > 0 else 0
        else:
            diversity_score = 0.0
        
        # Calculate inclusivity score
        connection_counts = [len(s.connections) for s in self.stakeholders.values()]
        if connection_counts:
            avg_connections = sum(connection_counts) / len(connection_counts)
            max_connections = len(self.stakeholders) - 1
            inclusivity_score = avg_connections / max_connections if max_connections > 0 else 0
        else:
            inclusivity_score = 0.0
        
        # Calculate domain harmonies
        domain_harmonies = {}
        for domain in HarmonyDomain:
            metrics = list(self.domain_metrics[domain])
            if metrics:
                domain_harmonies[domain.value] = (
                    sum(m["outcome"] for m in metrics[-10:]) / 
                    min(len(metrics), 10)
                )
            else:
                domain_harmonies[domain.value] = 0.5  # Neutral
        
        # Calculate emergence potential
        emergence_potential = self._calculate_emergence_potential(
            individual_harmony, integration_index, diversity_score
        )
        
        # Master harmony formula
        overall_harmony = (
            individual_harmony * 0.25 +
            integration_index * 0.20 +
            (1 - friction_index) * 0.20 +
            diversity_score * 0.15 +
            inclusivity_score * 0.20
        )
        
        # Apply Phi bonus for high integration
        if integration_index > 0.7:
            overall_harmony *= (1 + (integration_index - 0.7) * 0.5)
        
        overall_harmony = min(max(overall_harmony, 0.0), 1.0)
        
        metrics = CollectiveHarmony(
            overall_harmony=overall_harmony,
            domain_harmonies=domain_harmonies,
            integration_index=integration_index,
            friction_index=friction_index,
            emergence_potential=emergence_potential,
            diversity_score=diversity_score,
            inclusivity_score=inclusivity_score
        )
        
        self.harmony_history.append(metrics.to_dict())
        
        return metrics
    
    def _calculate_emergence_potential(
        self,
        harmony: float,
        integration: float,
        diversity: float
    ) -> float:
        """
        Calculate potential for collective emergence
        
        Emergence requires:
        - Sufficient harmony (connection)
        - High integration (depth)
        - Adequate diversity (creativity)
        """
        # All three factors needed
        if harmony < 0.4 or integration < 0.3 or diversity < 0.2:
            return 0.1  # Low potential
        
        # Multiplicative emergence
        base_potential = harmony * integration * diversity
        
        # Phi amplification for synergy
        if base_potential > 0.3:
            return base_potential * self.PHI
        
        return base_potential
    
    def suggest_harmonization(self) -> List[Dict]:
        """
        Suggest actions to improve societal harmony
        
        Ma'at: The path to harmony is clear to those who seek it
        """
        suggestions = []
        
        # 1. Address active frictions
        active_frictions = [f for f in self.frictions if not f.resolved]
        for friction in sorted(active_frictions, key=lambda f: f.intensity, reverse=True)[:5]:
            suggestions.append({
                "type": "resolve_friction",
                "stakeholders": [friction.stakeholder_a, friction.stakeholder_b],
                "domain": friction.domain.value,
                "intensity": friction.intensity,
                "suggestion": f"Facilitate dialogue in {friction.domain.value} domain"
            })
        
        # 2. Increase connections for isolated stakeholders
        for s in self.stakeholders.values():
            if s.integration_level in [IntegrationLevel.ISOLATED, IntegrationLevel.ADJACENT]:
                potential_partners = self._find_compatible_stakeholders(s)
                if potential_partners:
                    suggestions.append({
                        "type": "increase_integration",
                        "stakeholder": s.id,
                        "current_level": s.integration_level.value,
                        "potential_partners": potential_partners[:3],
                        "suggestion": f"Connect {s.name} with compatible stakeholders"
                    })
        
        # 3. Balance domains
        harmony = self.measure_collective_harmony()
        weak_domains = [
            d for d, score in harmony.domain_harmonies.items()
            if score < 0.5
        ]
        for domain in weak_domains:
            suggestions.append({
                "type": "strengthen_domain",
                "domain": domain,
                "current_score": harmony.domain_harmonies[domain],
                "suggestion": f"Increase positive interactions in {domain} domain"
            })
        
        # 4. Leverage emergence opportunities
        high_harmony_pairs = self._find_high_harmony_pairs()
        for pair in high_harmony_pairs[:3]:
            suggestions.append({
                "type": "cultivate_emergence",
                "stakeholders": pair,
                "suggestion": "These stakeholders show high emergence potential"
            })
        
        return suggestions
    
    def _find_compatible_stakeholders(self, stakeholder: Stakeholder) -> List[str]:
        """Find stakeholders compatible with the given one"""
        compatible = []
        
        for other in self.stakeholders.values():
            if other.id == stakeholder.id:
                continue
            
            # Check domain overlap
            shared_domains = stakeholder.domains & other.domains
            
            # Check complementary contribution/receptivity
            compatibility = (
                abs(stakeholder.contribution_score - other.receptivity_score) +
                abs(stakeholder.receptivity_score - other.contribution_score)
            ) / 2
            
            if shared_domains or compatibility < 0.3:
                compatible.append(other.id)
        
        return compatible
    
    def _find_high_harmony_pairs(self) -> List[Tuple[str, str]]:
        """Find pairs with high harmony potential"""
        pairs = []
        
        stakeholder_list = list(self.stakeholders.values())
        for i, a in enumerate(stakeholder_list):
            for b in stakeholder_list[i+1:]:
                combined_harmony = (a.harmony_index + b.harmony_index) / 2
                if combined_harmony > 0.7 and b.id in a.connections:
                    pairs.append((a.id, b.id))
        
        return sorted(
            pairs,
            key=lambda p: (
                self.stakeholders[p[0]].harmony_index + 
                self.stakeholders[p[1]].harmony_index
            ),
            reverse=True
        )
    
    def get_societal_report(self) -> Dict:
        """Generate comprehensive societal harmony report"""
        harmony = self.measure_collective_harmony()
        
        # Stakeholder summary
        type_distribution = {}
        for s in self.stakeholders.values():
            t = s.stakeholder_type.value
            type_distribution[t] = type_distribution.get(t, 0) + 1
        
        # Integration distribution
        integration_distribution = {}
        for s in self.stakeholders.values():
            level = s.integration_level.value
            integration_distribution[level] = integration_distribution.get(level, 0) + 1
        
        # Active vs resolved frictions
        active_frictions = [f for f in self.frictions if not f.resolved]
        resolved_frictions = [f for f in self.frictions if f.resolved]
        
        return {
            "timestamp": time.time(),
            "collective_harmony": harmony.to_dict(),
            "stakeholder_summary": {
                "total": len(self.stakeholders),
                "by_type": type_distribution,
                "by_integration": integration_distribution
            },
            "friction_summary": {
                "active": len(active_frictions),
                "resolved": len(resolved_frictions),
                "active_by_domain": self._count_frictions_by_domain(active_frictions)
            },
            "suggestions": self.suggest_harmonization()[:5],
            "statistics": self.stats.copy(),
            "maat_alignment": self._calculate_maat_alignment(harmony)
        }
    
    def _count_frictions_by_domain(self, frictions: List[SocialFriction]) -> Dict:
        """Count frictions by domain"""
        counts = {}
        for f in frictions:
            d = f.domain.value
            counts[d] = counts.get(d, 0) + 1
        return counts
    
    def _calculate_maat_alignment(self, harmony: CollectiveHarmony) -> float:
        """Calculate Ma'at alignment score"""
        # Harmony pillar (40%)
        harmony_score = harmony.overall_harmony * 0.4
        
        # Justice/fairness - measured by diversity and inclusivity (30%)
        justice_score = (
            harmony.diversity_score * 0.15 +
            harmony.inclusivity_score * 0.15
        )
        
        # Order - measured by low friction (30%)
        order_score = (1 - harmony.friction_index) * 0.3
        
        alignment = harmony_score + justice_score + order_score
        
        return min(max(alignment, 0.0), 1.0)
    
    def register_harmony_callback(self, callback: Callable):
        """Register callback for harmony events"""
        self.harmony_callbacks.append(callback)
    
    def register_friction_callback(self, callback: Callable):
        """Register callback for friction events"""
        self.friction_callbacks.append(callback)
    
    def register_emergence_callback(self, callback: Callable):
        """Register callback for emergence events"""
        self.emergence_callbacks.append(callback)
    
    def export_state(self, filepath: Path):
        """Export societal state"""
        state = {
            "timestamp": time.time(),
            "stakeholders": {
                k: v.to_dict() for k, v in self.stakeholders.items()
            },
            "frictions": [f.to_dict() for f in self.frictions],
            "harmony_history": list(self.harmony_history),
            "statistics": self.stats
        }
        
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info(f"Societal state exported to {filepath}")


def create_societal_integration_engine(
    config_path: Optional[str] = None
) -> SocietalIntegrationEngine:
    """Create a configured societal integration engine"""
    path = Path(config_path) if config_path else None
    return SocietalIntegrationEngine(config_path=path)


if __name__ == "__main__":
    # Demo usage
    engine = SocietalIntegrationEngine()
    
    # Register diverse stakeholders
    stakeholders = [
        Stakeholder(
            id="individual_1", name="Alice",
            stakeholder_type=StakeholderType.INDIVIDUAL,
            domains={HarmonyDomain.SOCIAL, HarmonyDomain.ECONOMIC},
            contribution_score=0.7, receptivity_score=0.6
        ),
        Stakeholder(
            id="community_1", name="Local Co-op",
            stakeholder_type=StakeholderType.COMMUNITY,
            domains={HarmonyDomain.ECONOMIC, HarmonyDomain.ENVIRONMENTAL},
            contribution_score=0.8, receptivity_score=0.7
        ),
        Stakeholder(
            id="org_1", name="Tech Nonprofit",
            stakeholder_type=StakeholderType.ORGANIZATION,
            domains={HarmonyDomain.TECHNOLOGICAL, HarmonyDomain.SOCIAL},
            contribution_score=0.6, receptivity_score=0.8
        ),
        Stakeholder(
            id="ecosystem_1", name="Regional Network",
            stakeholder_type=StakeholderType.ECOSYSTEM,
            domains={HarmonyDomain.ENVIRONMENTAL, HarmonyDomain.CULTURAL},
            contribution_score=0.7, receptivity_score=0.7,
            integration_level=IntegrationLevel.INTEGRATED
        ),
    ]
    
    for s in stakeholders:
        engine.register_stakeholder(s)
    
    # Form connections
    engine.form_connection("individual_1", "community_1")
    engine.form_connection("community_1", "org_1")
    engine.form_connection("org_1", "ecosystem_1")
    engine.form_connection("individual_1", "ecosystem_1")
    
    # Record some interactions
    engine.record_interaction(
        "individual_1", "community_1",
        HarmonyDomain.ECONOMIC, 0.8, "collaboration"
    )
    
    engine.record_interaction(
        "community_1", "org_1",
        HarmonyDomain.TECHNOLOGICAL, 0.9, "partnership"
    )
    
    # Measure collective harmony
    harmony = engine.measure_collective_harmony()
    print(f"\nCollective Harmony: {harmony.overall_harmony:.3f}")
    print(f"Integration Index: {harmony.integration_index:.3f}")
    print(f"Friction Index: {harmony.friction_index:.3f}")
    print(f"Emergence Potential: {harmony.emergence_potential:.3f}")
    
    # Get suggestions
    report = engine.get_societal_report()
    print(f"\nMa'at Alignment: {report['maat_alignment']:.3f}")
    print("\nHarmonization Suggestions:")
    for suggestion in report['suggestions'][:3]:
        print(f"  - {suggestion['type']}: {suggestion['suggestion']}")
