#!/usr/bin/env python3
"""
TASK-047: Sovereignty Immunity Checks at Scale
Verifies sovereign immunity status across jurisdictions and contexts.
"""

import json
import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path
from enum import Enum


class SovereigntyType(Enum):
    """Types of sovereignty recognized."""
    STATE = "state_sovereignty"
    TRIBAL = "tribal_sovereignty"
    INDIVIDUAL = "individual_sovereignty"
    CORPORATE = "corporate_sovereignty"
    DIPLOMATIC = "diplomatic_immunity"
    ECCLESIASTICAL = "ecclesiastical_immunity"


class ImmunityLevel(Enum):
    """Levels of sovereign immunity."""
    ABSOLUTE = "absolute"
    QUALIFIED = "qualified"
    LIMITED = "limited"
    NONE = "none"


class SovereigntyImmunityChecker:
    """Scale-based checker for sovereignty and immunity status."""

    def __init__(self, database_path: str = "sovereignty_immunity_db.json"):
        self.database_path = Path(database_path)
        self.database = self._load_database()

    def _load_database(self) -> Dict:
        """Load immunity database."""
        if self.database_path.exists():
            with open(self.database_path, 'r') as f:
                return json.load(f)

        return {
            "entities": {},
            "jurisdictions": {},
            "immunity_rules": {},
            "check_history": []
        }

    def _save_database(self):
        """Save database to disk."""
        with open(self.database_path, 'w') as f:
            json.dump(self.database, f, indent=2)

    def register_sovereign_entity(
        self,
        entity_id: str,
        entity_name: str,
        sovereignty_type: SovereigntyType,
        recognized_jurisdictions: List[str],
        documentation: Dict
    ) -> Dict:
        """
        Register a sovereign entity in the system.

        Args:
            entity_id: Unique identifier
            entity_name: Name of sovereign entity
            sovereignty_type: Type of sovereignty claimed
            recognized_jurisdictions: Where sovereignty is recognized
            documentation: Supporting documentation

        Returns:
            Entity record
        """
        entity = {
            "entity_id": entity_id,
            "name": entity_name,
            "type": sovereignty_type.value,
            "recognized_in": recognized_jurisdictions,
            "documentation": documentation,
            "registration_date": datetime.datetime.now().isoformat(),
            "immunity_level": self._determine_immunity_level(
                sovereignty_type,
                recognized_jurisdictions
            ),
            "active": True
        }

        self.database["entities"][entity_id] = entity
        self._save_database()
        return entity

    def _determine_immunity_level(
        self,
        sovereignty_type: SovereigntyType,
        jurisdictions: List[str]
    ) -> str:
        """Determine immunity level based on sovereignty type."""
        # State sovereignty typically has highest immunity
        if sovereignty_type == SovereigntyType.STATE:
            return ImmunityLevel.ABSOLUTE.value

        # Diplomatic immunity is nearly absolute
        if sovereignty_type == SovereigntyType.DIPLOMATIC:
            return ImmunityLevel.ABSOLUTE.value

        # Tribal sovereignty varies by jurisdiction
        if sovereignty_type == SovereigntyType.TRIBAL:
            return ImmunityLevel.QUALIFIED.value if len(jurisdictions) > 0 else ImmunityLevel.LIMITED.value

        # Individual sovereignty is limited
        if sovereignty_type == SovereigntyType.INDIVIDUAL:
            return ImmunityLevel.LIMITED.value

        return ImmunityLevel.NONE.value

    def check_immunity_status(
        self,
        entity_id: str,
        jurisdiction: str,
        context: str,
        action_type: str
    ) -> Dict:
        """
        Check immunity status for specific context.

        Args:
            entity_id: Entity to check
            jurisdiction: Jurisdiction where action occurs
            context: Context of action (civil, criminal, commercial)
            action_type: Specific type of action

        Returns:
            Immunity status with reasoning
        """
        if entity_id not in self.database["entities"]:
            return {
                "status": "error",
                "message": "Entity not found in database"
            }

        entity = self.database["entities"][entity_id]

        # Check if jurisdiction recognizes entity's sovereignty
        recognized = jurisdiction in entity["recognized_in"]

        # Evaluate immunity based on multiple factors
        immunity_applies = self._evaluate_immunity(
            entity,
            jurisdiction,
            context,
            action_type,
            recognized
        )

        check_result = {
            "entity_id": entity_id,
            "entity_name": entity["name"],
            "jurisdiction": jurisdiction,
            "context": context,
            "action_type": action_type,
            "sovereignty_recognized": recognized,
            "immunity_level": entity["immunity_level"],
            "immunity_applies": immunity_applies,
            "exceptions": self._check_immunity_exceptions(
                entity,
                context,
                action_type
            ),
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Log check
        self.database["check_history"].append(check_result)
        self._save_database()

        return check_result

    def _evaluate_immunity(
        self,
        entity: Dict,
        jurisdiction: str,
        context: str,
        action_type: str,
        recognized: bool
    ) -> bool:
        """Evaluate whether immunity applies in this case."""
        immunity_level = ImmunityLevel(entity["immunity_level"])

        # Absolute immunity - almost always applies
        if immunity_level == ImmunityLevel.ABSOLUTE:
            # Check for rare exceptions
            if context == "commercial" and action_type == "contract_dispute":
                return False  # Commercial exception
            return True

        # Qualified immunity - depends on context
        if immunity_level == ImmunityLevel.QUALIFIED:
            if not recognized:
                return False
            if context == "criminal" and action_type in ["serious_crime", "human_rights_violation"]:
                return False  # Criminal exception
            return True

        # Limited immunity
        if immunity_level == ImmunityLevel.LIMITED:
            if context == "internal_governance":
                return True
            return False

        return False

    def _check_immunity_exceptions(
        self,
        entity: Dict,
        context: str,
        action_type: str
    ) -> List[Dict]:
        """Check for exceptions that may waive immunity."""
        exceptions = []

        # Commercial activity exception
        if context == "commercial":
            exceptions.append({
                "exception": "commercial_activity",
                "applies": action_type in ["contract", "business_transaction"],
                "waives_immunity": True
            })

        # Tort exception
        if context == "civil" and action_type == "tort":
            exceptions.append({
                "exception": "tort_liability",
                "applies": True,
                "waives_immunity": entity["immunity_level"] != ImmunityLevel.ABSOLUTE.value
            })

        # Express waiver
        if entity.get("immunity_waivers", []):
            for waiver in entity["immunity_waivers"]:
                if waiver["context"] == context:
                    exceptions.append({
                        "exception": "express_waiver",
                        "applies": True,
                        "waives_immunity": True,
                        "waiver_details": waiver
                    })

        return exceptions

    def batch_check_immunity(
        self,
        entity_ids: List[str],
        jurisdiction: str,
        context: str,
        action_type: str
    ) -> Dict:
        """
        Check immunity status for multiple entities at scale.

        Args:
            entity_ids: List of entities to check
            jurisdiction: Jurisdiction
            context: Context
            action_type: Action type

        Returns:
            Batch results with summary
        """
        results = []
        summary = {
            "total_checked": len(entity_ids),
            "immune": 0,
            "not_immune": 0,
            "errors": 0
        }

        for entity_id in entity_ids:
            result = self.check_immunity_status(
                entity_id,
                jurisdiction,
                context,
                action_type
            )

            results.append(result)

            if result.get("status") == "error":
                summary["errors"] += 1
            elif result.get("immunity_applies"):
                summary["immune"] += 1
            else:
                summary["not_immune"] += 1

        return {
            "summary": summary,
            "results": results,
            "timestamp": datetime.datetime.now().isoformat()
        }

    def add_jurisdiction_rules(
        self,
        jurisdiction: str,
        sovereignty_type: SovereigntyType,
        rules: Dict
    ) -> Dict:
        """Add jurisdiction-specific immunity rules."""
        if jurisdiction not in self.database["jurisdictions"]:
            self.database["jurisdictions"][jurisdiction] = {}

        self.database["jurisdictions"][jurisdiction][sovereignty_type.value] = {
            "rules": rules,
            "updated": datetime.datetime.now().isoformat()
        }

        self._save_database()
        return self.database["jurisdictions"][jurisdiction]

    def generate_immunity_matrix(
        self,
        entity_id: str
    ) -> Dict:
        """
        Generate comprehensive immunity matrix for entity.

        Args:
            entity_id: Entity to analyze

        Returns:
            Matrix showing immunity status across contexts
        """
        if entity_id not in self.database["entities"]:
            return {"error": "Entity not found"}

        entity = self.database["entities"][entity_id]

        contexts = ["civil", "criminal", "commercial", "administrative"]
        action_types = ["lawsuit", "prosecution", "contract_dispute", "regulation"]

        matrix = {
            "entity_id": entity_id,
            "entity_name": entity["name"],
            "immunity_level": entity["immunity_level"],
            "contexts": {}
        }

        for context in contexts:
            matrix["contexts"][context] = {}
            for action_type in action_types:
                # Simulate check for each jurisdiction
                jurisdiction_results = {}
                for jurisdiction in entity["recognized_in"]:
                    immunity_applies = self._evaluate_immunity(
                        entity,
                        jurisdiction,
                        context,
                        action_type,
                        True
                    )
                    jurisdiction_results[jurisdiction] = immunity_applies

                matrix["contexts"][context][action_type] = jurisdiction_results

        return matrix

    def get_statistics(self) -> Dict:
        """Get system statistics."""
        total_entities = len(self.database["entities"])
        total_checks = len(self.database["check_history"])

        # Count by sovereignty type
        by_type = {}
        for entity in self.database["entities"].values():
            sov_type = entity["type"]
            by_type[sov_type] = by_type.get(sov_type, 0) + 1

        # Recent checks
        recent_checks = self.database["check_history"][-100:] if len(self.database["check_history"]) > 100 else self.database["check_history"]
        immune_count = sum(1 for c in recent_checks if c.get("immunity_applies"))

        return {
            "total_entities": total_entities,
            "total_checks": total_checks,
            "entities_by_type": by_type,
            "recent_immunity_rate": immune_count / len(recent_checks) if recent_checks else 0,
            "database_size_kb": self.database_path.stat().st_size / 1024 if self.database_path.exists() else 0
        }


def main():
    """Demonstration of sovereignty immunity checking."""
    checker = SovereigntyImmunityChecker()

    # Register sovereign entities
    print("🔐 Registering Sovereign Entities...")

    entity1 = checker.register_sovereign_entity(
        entity_id="STATE_001",
        entity_name="Federal State Alpha",
        sovereignty_type=SovereigntyType.STATE,
        recognized_jurisdictions=["US", "UN", "EU"],
        documentation={"treaty_status": "full_recognition"}
    )

    entity2 = checker.register_sovereign_entity(
        entity_id="TRIBAL_001",
        entity_name="Indigenous Nation Beta",
        sovereignty_type=SovereigntyType.TRIBAL,
        recognized_jurisdictions=["US"],
        documentation={"treaty_date": "1851", "status": "federally_recognized"}
    )

    # Check immunity status
    print("\n✅ Checking Immunity Status...")

    check1 = checker.check_immunity_status(
        entity_id="STATE_001",
        jurisdiction="US",
        context="civil",
        action_type="lawsuit"
    )
    print(json.dumps(check1, indent=2))

    # Batch check
    print("\n📊 Batch Immunity Check...")
    batch_result = checker.batch_check_immunity(
        entity_ids=["STATE_001", "TRIBAL_001"],
        jurisdiction="US",
        context="commercial",
        action_type="contract_dispute"
    )
    print(json.dumps(batch_result["summary"], indent=2))

    # Generate immunity matrix
    print("\n🗺️ Immunity Matrix:")
    matrix = checker.generate_immunity_matrix("STATE_001")
    print(json.dumps(matrix, indent=2))

    # Statistics
    print("\n📈 System Statistics:")
    stats = checker.get_statistics()
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
