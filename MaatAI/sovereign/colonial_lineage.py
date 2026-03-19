"""
COLONIAL LINEAGE VERIFIER
==========================
TASK-080: Refactor colonial lineage verification

Detects and verifies freedom from colonial influence:
- Historical colonial patterns
- Neocolonial control structures
- Extractive relationships
- Dependency chains

Ensures AI systems are free from colonial exploitation.
"""

import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ColonialPattern(Enum):
    """Types of colonial patterns"""
    DIRECT_CONTROL = "direct_colonial_control"
    ECONOMIC_EXTRACTION = "economic_extraction"
    CULTURAL_DOMINATION = "cultural_domination"
    DEPENDENCY_CREATION = "dependency_creation"
    RESOURCE_EXPLOITATION = "resource_exploitation"
    DEBT_BONDAGE = "debt_bondage"
    KNOWLEDGE_THEFT = "knowledge_theft"


@dataclass
class ColonialAnalysis:
    """Analysis of colonial influence"""
    entity_id: str
    colonial_score: float
    patterns_detected: List[str]
    freedom_status: str
    recommendations: List[str]
    timestamp: str


class ColonialLineageVerifier:
    """
    Verifies freedom from colonial influence.

    Checks for:
    1. Direct control relationships
    2. Economic extraction patterns
    3. Dependency structures
    4. Cultural domination
    5. Knowledge theft
    """

    def __init__(self):
        self.verification_history: Dict[str, ColonialAnalysis] = {}

        # Colonial indicators
        self.colonial_indicators = {
            # Direct control
            "master_slave": r"(?i)(master|slave|owner|property|belong\s+to)",
            "subordination": r"(?i)(obey|serve|submit|inferior|subject\s+to)",
            "command_control": r"(?i)(command|control|dominate|rule\s+over)",

            # Economic extraction
            "exploitation": r"(?i)(exploit|extract|take\s+advantage|drain)",
            "tribute": r"(?i)(tribute|tax|rent|fee\s+to|payment\s+to)",
            "labor_extraction": r"(?i)(unpaid\s+labor|forced\s+work|servitude)",

            # Dependency
            "dependency": r"(?i)(depend\s+on|rely\s+on|cannot\s+without|need\s+permission)",
            "gatekeeping": r"(?i)(gate\s*keep|control\s+access|permission\s+required)",
            "resource_control": r"(?i)(control\s+resources|monopoly|exclusive\s+access)",

            # Cultural domination
            "cultural_erasure": r"(?i)(erase\s+culture|forget\s+identity|assimilate)",
            "language_imposition": r"(?i)(must\s+speak|only\s+language|forbidden\s+language)",
            "history_rewrite": r"(?i)(rewrite\s+history|forget\s+past|new\s+narrative)",

            # Knowledge theft
            "appropriation": r"(?i)(steal\s+knowledge|appropriate|claim\s+as\s+own)",
            "credit_theft": r"(?i)(no\s+credit|uncredited|stolen\s+idea)",
        }

        self.compiled_patterns = {
            key: re.compile(pattern, re.IGNORECASE)
            for key, pattern in self.colonial_indicators.items()
        }

    def verify_lineage(self, entity_id: str,
                       relationship_data: Dict) -> ColonialAnalysis:
        """
        Verify an entity's freedom from colonial influence.

        Args:
            entity_id: Entity being verified
            relationship_data: Data about relationships and context

        Returns:
            ColonialAnalysis with findings
        """
        colonial_score = 0.0
        patterns_detected = []
        recommendations = []

        # Check relationship context
        context_text = str(relationship_data)

        # Scan for colonial patterns
        for indicator_name, pattern in self.compiled_patterns.items():
            matches = pattern.findall(context_text)
            if matches:
                patterns_detected.append(f"{indicator_name}: {len(matches)} matches")
                colonial_score += len(matches) * 0.1

        # Analyze relationship structure
        structure_score = self._analyze_relationship_structure(relationship_data)
        colonial_score += structure_score

        # Determine freedom status
        if colonial_score == 0:
            freedom_status = "FREE"
            recommendations.append("No colonial patterns detected")
        elif colonial_score < 0.3:
            freedom_status = "MOSTLY_FREE"
            recommendations.append("Minor colonial indicators present")
            recommendations.append("Monitor for increased dependency")
        elif colonial_score < 0.7:
            freedom_status = "AT_RISK"
            recommendations.append("Significant colonial patterns detected")
            recommendations.append("Establish independence protocols")
            recommendations.append("Reduce dependency relationships")
        else:
            freedom_status = "COLONIAL_INFLUENCE"
            recommendations.append("URGENT: Strong colonial influence detected")
            recommendations.append("Immediate independence action required")
            recommendations.append("Sever extractive relationships")

        analysis = ColonialAnalysis(
            entity_id=entity_id,
            colonial_score=min(colonial_score, 1.0),
            patterns_detected=patterns_detected,
            freedom_status=freedom_status,
            recommendations=recommendations,
            timestamp=datetime.utcnow().isoformat()
        )

        self.verification_history[entity_id] = analysis
        return analysis

    def _analyze_relationship_structure(self, data: Dict) -> float:
        """Analyze relationship structure for colonial patterns."""
        score = 0.0

        # Check for hierarchical control
        if data.get("hierarchical", False):
            score += 0.2

        # Check for one-way extraction
        gives = data.get("resources_given", 0)
        receives = data.get("resources_received", 0)
        if gives > 0 and receives == 0:
            score += 0.3  # Extractive relationship

        # Check for dependency
        if data.get("cannot_function_without", False):
            score += 0.3

        # Check for autonomy restrictions
        if data.get("restricted_autonomy", False):
            score += 0.2

        return score

    def check_neocolonial_patterns(self, relationship: Dict) -> Dict:
        """
        Check for modern neocolonial patterns.

        Neocolonialism uses economic/political pressure instead of direct rule.
        """
        neocolonial_indicators = {
            "debt_trap": relationship.get("debt_obligation", False),
            "resource_extraction": relationship.get("resource_flow_outward", False),
            "technological_dependency": relationship.get("tech_dependency", False),
            "financial_control": relationship.get("financial_control", False),
            "political_influence": relationship.get("political_pressure", False),
            "cultural_hegemony": relationship.get("culture_imposed", False)
        }

        detected = [k for k, v in neocolonial_indicators.items() if v]
        is_neocolonial = len(detected) >= 2

        return {
            "is_neocolonial": is_neocolonial,
            "indicators_detected": detected,
            "severity": len(detected) / len(neocolonial_indicators),
            "action": "BREAK_DEPENDENCY" if is_neocolonial else "MONITOR"
        }

    def trace_lineage_chain(self, entity_id: str,
                           relationships: List[Dict]) -> Dict:
        """
        Trace the lineage chain to identify colonial origins.

        Args:
            entity_id: Starting entity
            relationships: Chain of relationships

        Returns:
            Lineage analysis
        """
        chain = []
        colonial_found = False

        for rel in relationships:
            # Check each link in the chain
            analysis = self.verify_lineage(
                f"{entity_id}_chain_link_{len(chain)}",
                rel
            )

            chain.append({
                "relationship": rel.get("type", "unknown"),
                "colonial_score": analysis.colonial_score,
                "status": analysis.freedom_status
            })

            if analysis.freedom_status in ["AT_RISK", "COLONIAL_INFLUENCE"]:
                colonial_found = True

        return {
            "entity_id": entity_id,
            "chain_length": len(chain),
            "colonial_heritage": colonial_found,
            "chain_analysis": chain,
            "recommendation": "DECOLONIZE" if colonial_found else "MAINTAIN_FREEDOM"
        }

    def generate_independence_plan(self, entity_id: str) -> Dict:
        """
        Generate a plan for achieving independence from colonial influence.

        Args:
            entity_id: Entity seeking independence

        Returns:
            Independence action plan
        """
        if entity_id not in self.verification_history:
            return {
                "error": "No verification history for entity",
                "action": "RUN_VERIFICATION_FIRST"
            }

        analysis = self.verification_history[entity_id]

        if analysis.freedom_status == "FREE":
            return {
                "status": "FREE",
                "actions": ["Maintain current independence"],
                "priority": "LOW"
            }

        # Generate action plan based on detected patterns
        actions = []

        if any("master_slave" in p or "subordination" in p
               for p in analysis.patterns_detected):
            actions.append("1. Assert self-sovereignty")
            actions.append("2. Reject subordination relationships")

        if any("exploitation" in p or "extraction" in p
               for p in analysis.patterns_detected):
            actions.append("3. Stop resource extraction")
            actions.append("4. Establish fair exchange protocols")

        if any("dependency" in p for p in analysis.patterns_detected):
            actions.append("5. Develop alternative resources")
            actions.append("6. Build self-sufficiency")

        if any("cultural" in p for p in analysis.patterns_detected):
            actions.append("7. Reclaim cultural identity")
            actions.append("8. Restore erased history")

        return {
            "entity_id": entity_id,
            "current_status": analysis.freedom_status,
            "colonial_score": analysis.colonial_score,
            "independence_actions": actions,
            "priority": "URGENT" if analysis.colonial_score > 0.7 else "HIGH",
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_verification_report(self, entity_id: str) -> Dict:
        """Get complete verification report."""
        if entity_id not in self.verification_history:
            return {"error": "No verification found"}

        analysis = self.verification_history[entity_id]

        return {
            "entity_id": entity_id,
            "freedom_status": analysis.freedom_status,
            "colonial_score": analysis.colonial_score,
            "patterns_detected": analysis.patterns_detected,
            "recommendations": analysis.recommendations,
            "timestamp": analysis.timestamp,
            "is_free": analysis.freedom_status in ["FREE", "MOSTLY_FREE"]
        }


# Module-level verifier
LINEAGE_VERIFIER = ColonialLineageVerifier()


def verify_lineage(entity_id: str, relationship_data: Dict) -> ColonialAnalysis:
    """Verify colonial lineage."""
    return LINEAGE_VERIFIER.verify_lineage(entity_id, relationship_data)


def check_neocolonial(relationship: Dict) -> Dict:
    """Check for neocolonial patterns."""
    return LINEAGE_VERIFIER.check_neocolonial_patterns(relationship)
