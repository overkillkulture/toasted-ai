#!/usr/bin/env python3
"""
TASK-046: Allodial Property Right Verification System
Automates verification of absolute property rights and sovereignty claims.
"""

import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class AllodialPropertyVerifier:
    """Verifies and tracks allodial (absolute) property rights."""

    def __init__(self, database_path: str = "allodial_registry.json"):
        self.database_path = Path(database_path)
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict:
        """Load existing registry or create new one."""
        if self.database_path.exists():
            with open(self.database_path, 'r') as f:
                return json.load(f)
        return {
            "properties": {},
            "claims": [],
            "verifications": [],
            "sovereignty_chain": []
        }

    def _save_registry(self):
        """Persist registry to disk."""
        with open(self.database_path, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def _generate_property_id(self, description: str, coordinates: Dict) -> str:
        """Generate unique property identifier."""
        data = f"{description}:{json.dumps(coordinates, sort_keys=True)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def register_allodial_claim(
        self,
        claimant: str,
        property_description: str,
        coordinates: Dict,
        evidence: List[str],
        sovereignty_basis: str
    ) -> Dict:
        """
        Register a new allodial property claim.

        Args:
            claimant: Name/ID of entity claiming property
            property_description: Detailed description of property
            coordinates: Geographic or logical coordinates
            evidence: List of supporting evidence
            sovereignty_basis: Legal/philosophical basis for sovereignty

        Returns:
            Claim record with verification status
        """
        property_id = self._generate_property_id(property_description, coordinates)

        claim = {
            "property_id": property_id,
            "claimant": claimant,
            "description": property_description,
            "coordinates": coordinates,
            "evidence": evidence,
            "sovereignty_basis": sovereignty_basis,
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "pending_verification",
            "verification_score": 0.0
        }

        # Store claim
        self.registry["claims"].append(claim)

        # Initialize property record
        if property_id not in self.registry["properties"]:
            self.registry["properties"][property_id] = {
                "claims": [],
                "verified_owner": None,
                "sovereignty_status": "disputed"
            }

        self.registry["properties"][property_id]["claims"].append(claim["timestamp"])
        self._save_registry()

        return claim

    def verify_property_rights(
        self,
        property_id: str,
        verification_method: str,
        verification_data: Dict
    ) -> Dict:
        """
        Verify allodial property rights using specified method.

        Args:
            property_id: Unique property identifier
            verification_method: Method used for verification
            verification_data: Supporting verification data

        Returns:
            Verification result with confidence score
        """
        if property_id not in self.registry["properties"]:
            return {
                "status": "error",
                "message": "Property not found in registry"
            }

        # Calculate verification score based on evidence
        score = self._calculate_verification_score(
            property_id,
            verification_method,
            verification_data
        )

        verification = {
            "property_id": property_id,
            "method": verification_method,
            "data": verification_data,
            "score": score,
            "timestamp": datetime.datetime.now().isoformat(),
            "verified": score >= 0.75
        }

        self.registry["verifications"].append(verification)

        # Update property status if verification passes
        if verification["verified"]:
            self.registry["properties"][property_id]["sovereignty_status"] = "verified"

        self._save_registry()
        return verification

    def _calculate_verification_score(
        self,
        property_id: str,
        method: str,
        data: Dict
    ) -> float:
        """Calculate confidence score for property verification."""
        score = 0.0

        # Method-specific scoring
        if method == "historical_record":
            score += 0.3 if data.get("records_found", 0) > 0 else 0
            score += 0.2 if data.get("continuous_possession", False) else 0

        elif method == "sovereign_declaration":
            score += 0.4 if data.get("declaration_signed", False) else 0
            score += 0.2 if data.get("witness_count", 0) >= 3 else 0

        elif method == "common_law":
            score += 0.3 if data.get("adverse_possession_years", 0) >= 7 else 0
            score += 0.2 if data.get("improvements_made", False) else 0

        elif method == "natural_law":
            score += 0.5 if data.get("homesteading", False) else 0

        # Chain of custody bonus
        property_claims = self.registry["properties"][property_id]["claims"]
        if len(property_claims) == 1:  # Original claimant
            score += 0.15

        return min(score, 1.0)

    def check_sovereignty_conflicts(self, property_id: str) -> List[Dict]:
        """Check for conflicting sovereignty claims."""
        if property_id not in self.registry["properties"]:
            return []

        property_data = self.registry["properties"][property_id]
        claims = [
            c for c in self.registry["claims"]
            if c["property_id"] == property_id
        ]

        conflicts = []
        for i, claim1 in enumerate(claims):
            for claim2 in claims[i+1:]:
                if claim1["claimant"] != claim2["claimant"]:
                    conflicts.append({
                        "claimant_1": claim1["claimant"],
                        "claimant_2": claim2["claimant"],
                        "basis_1": claim1["sovereignty_basis"],
                        "basis_2": claim2["sovereignty_basis"],
                        "requires_arbitration": True
                    })

        return conflicts

    def establish_sovereignty_chain(
        self,
        property_id: str,
        chain_data: Dict
    ) -> Dict:
        """
        Establish blockchain-style sovereignty chain.

        Args:
            property_id: Property identifier
            chain_data: Data to add to sovereignty chain

        Returns:
            Chain link with hash
        """
        previous_hash = "0" * 64
        if self.registry["sovereignty_chain"]:
            previous_hash = self.registry["sovereignty_chain"][-1]["hash"]

        link = {
            "property_id": property_id,
            "data": chain_data,
            "timestamp": datetime.datetime.now().isoformat(),
            "previous_hash": previous_hash
        }

        # Generate hash for this link
        link_string = json.dumps(link, sort_keys=True)
        link["hash"] = hashlib.sha256(link_string.encode()).hexdigest()

        self.registry["sovereignty_chain"].append(link)
        self._save_registry()

        return link

    def generate_sovereignty_report(self, property_id: str) -> Dict:
        """Generate comprehensive sovereignty status report."""
        if property_id not in self.registry["properties"]:
            return {"error": "Property not found"}

        property_data = self.registry["properties"][property_id]
        claims = [c for c in self.registry["claims"] if c["property_id"] == property_id]
        verifications = [v for v in self.registry["verifications"] if v["property_id"] == property_id]

        # Calculate overall sovereignty score
        avg_verification_score = (
            sum(v["score"] for v in verifications) / len(verifications)
            if verifications else 0.0
        )

        report = {
            "property_id": property_id,
            "sovereignty_status": property_data["sovereignty_status"],
            "total_claims": len(claims),
            "verified_claims": len([v for v in verifications if v["verified"]]),
            "verification_score": avg_verification_score,
            "conflicts": self.check_sovereignty_conflicts(property_id),
            "chain_verified": self._verify_sovereignty_chain(property_id),
            "recommendations": self._generate_recommendations(property_data, avg_verification_score)
        }

        return report

    def _verify_sovereignty_chain(self, property_id: str) -> bool:
        """Verify integrity of sovereignty chain for property."""
        chain_links = [
            link for link in self.registry["sovereignty_chain"]
            if link["property_id"] == property_id
        ]

        for i, link in enumerate(chain_links):
            # Recalculate hash
            link_copy = dict(link)
            stored_hash = link_copy.pop("hash")
            link_string = json.dumps(link_copy, sort_keys=True)
            calculated_hash = hashlib.sha256(link_string.encode()).hexdigest()

            if calculated_hash != stored_hash:
                return False

        return True

    def _generate_recommendations(
        self,
        property_data: Dict,
        verification_score: float
    ) -> List[str]:
        """Generate recommendations for strengthening sovereignty claim."""
        recommendations = []

        if verification_score < 0.5:
            recommendations.append("Gather additional historical documentation")
            recommendations.append("Obtain witness affidavits")

        if verification_score < 0.75:
            recommendations.append("Document continuous possession and improvements")
            recommendations.append("File formal sovereignty declaration")

        if property_data["sovereignty_status"] == "disputed":
            recommendations.append("Seek arbitration for conflicting claims")
            recommendations.append("Establish clear boundaries and markers")

        return recommendations


def main():
    """Demonstration of allodial property verification."""
    verifier = AllodialPropertyVerifier()

    # Example: Register allodial claim
    claim = verifier.register_allodial_claim(
        claimant="Sovereign Individual Alpha",
        property_description="Homesteaded land parcel, 5 acres",
        coordinates={"lat": 45.5231, "lon": -122.6765},
        evidence=[
            "Continuous occupation for 10 years",
            "Improvements: house, well, garden",
            "No competing claims in public record"
        ],
        sovereignty_basis="Natural Law - Lockean Homesteading Principle"
    )

    print("✅ Allodial Claim Registered:")
    print(json.dumps(claim, indent=2))

    # Verify the claim
    verification = verifier.verify_property_rights(
        property_id=claim["property_id"],
        verification_method="natural_law",
        verification_data={
            "homesteading": True,
            "continuous_possession_years": 10,
            "improvements_value": 150000
        }
    )

    print("\n✅ Verification Result:")
    print(json.dumps(verification, indent=2))

    # Generate sovereignty report
    report = verifier.generate_sovereignty_report(claim["property_id"])
    print("\n📊 Sovereignty Report:")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
