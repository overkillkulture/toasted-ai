"""
Water Analyzer - Pharmaceutical Contamination Detection
Analyzes water samples for pharmaceutical residues and endocrine disruptors
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class WaterAnalyzer:
    """Analyzes water for pharmaceutical contamination"""
    
    KNOWN_CONTAMINANTS = {
        # Common pharmaceuticals found in water
        "acetaminophen": {"category": "pain_reliever", "concentration_ppb": 0.1},
        "ibuprofen": {"category": "nsaid", "concentration_ppb": 0.5},
        "naproxen": {"category": "nsaid", "concentration_ppb": 0.2},
        "diclofenac": {"category": "nsaid", "concentration_ppb": 0.1},
        "carbamazepine": {"category": "anticonvulsant", "concentration_ppb": 0.1},
        "trimethoprim": {"category": "antibiotic", "concentration_ppb": 0.05},
        "sulfamethoxazole": {"category": "antibiotic", "concentration_ppb": 0.05},
        "ciprofloxacin": {"category": "antibiotic", "concentration_ppb": 0.1},
        "azithromycin": {"category": "antibiotic", "concentration_ppb": 0.05},
        "estradiol": {"category": "hormone", "concentration_ppb": 0.001},
        "estrone": {"category": "hormone", "concentration_ppb": 0.001},
        "progesterone": {"category": "hormone", "concentration_ppb": 0.001},
        "testosterone": {"category": "hormone", "concentration_ppb": 0.001},
        "antidepressants": {"category": "mental_health", "concentration_ppb": 0.01},
        "ssri": {"category": "mental_health", "concentration_ppb": 0.01},
        "beta_blockers": {"category": "heart_medication", "concentration_ppb": 0.05},
        "statins": {"category": "cholesterol", "concentration_ppb": 0.05},
        "ppis": {"category": "acid_reducer", "concentration_ppb": 0.1},
        "blood_thinners": {"category": "anticoagulant", "concentration_ppb": 0.01},
        "diuretics": {"category": "water_pill", "concentration_ppb": 0.1},
    }
    
    ENDOCRINE_DISRUPTORS = [
        "estradiol", "estrone", "progesterone", "testosterone",
        "bisphenol_a", "phthalates", "pesticides", "herbicides"
    ]
    
    def __init__(self):
        self.analysis_history: List[Dict] = []
        
    def analyze_sample(self, sample_data: Dict) -> Dict:
        """
        Analyze a water sample for pharmaceutical contamination
        
        Args:
            sample_data: Dict containing location, date, and detected compounds
            
        Returns:
            Analysis results with contamination levels and risk assessment
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "location": sample_data.get("location", "Unknown"),
            "detected_compounds": [],
            "total_concentration_ppb": 0.0,
            "endocrine_disruptors": [],
            "risk_level": "LOW",
            "health_advisory": [],
            "bioaccumulation_concern": False
        }
        
        detected = sample_data.get("detected", {})
        
        for compound, concentration in detected.items():
            compound_lower = compound.lower()
            
            if compound_lower in self.KNOWN_CONTAMINANTS:
                info = self.KNOWN_CONTAMINANTS[compound_lower]
                results["detected_compounds"].append({
                    "compound": compound,
                    "concentration_ppb": concentration,
                    "category": info["category"],
                    "threshold_ppb": info["concentration_ppb"],
                    "exceeds_threshold": concentration > info["concentration_ppb"]
                })
                results["total_concentration_ppb"] += concentration
                
                # Track endocrine disruptors
                if compound_lower in self.ENDOCRINE_DISRUPTORS:
                    results["endocrine_disruptors"].append(compound)
                    
        # Assess risk level
        if results["total_concentration_ppb"] > 10:
            results["risk_level"] = "CRITICAL"
        elif results["total_concentration_ppb"] > 5:
            results["risk_level"] = "HIGH"
        elif results["total_concentration_ppb"] > 1:
            results["risk_level"] = "MODERATE"
            
        # Bioaccumulation concern
        if len(results["endocrine_disruptors"]) > 2:
            results["bioaccumulation_concern"] = True
            results["health_advisory"].append(
                "Multiple endocrine disruptors detected - bioaccumulation risk elevated"
            )
            
        # Generate health advisories
        for compound in results["detected_compounds"]:
            if compound["exceeds_threshold"]:
                results["health_advisory"].append(
                    f"{compound['compound']} exceeds safe threshold"
                )
                
        self.analysis_history.append(results)
        return results
        
    def get_statistics(self) -> Dict:
        """Get historical analysis statistics"""
        if not self.analysis_history:
            return {"message": "No analyses performed yet"}
            
        total_samples = len(self.analysis_history)
        high_risk = sum(1 for r in self.analysis_history if r["risk_level"] in ["HIGH", "CRITICAL"])
        
        all_compounds = []
        for r in self.analysis_history:
            all_compounds.extend([c["compound"] for c in r["detected_compounds"]])
            
        return {
            "total_samples": total_samples,
            "high_risk_count": high_risk,
            "risk_percentage": (high_risk / total_samples) * 100,
            "most_common_compounds": list(set(all_compounds))[:10]
        }


class ContaminationTracker:
    """Tracks pharmaceutical contamination patterns over time and geography"""
    
    def __init__(self):
        self.tracking_data: Dict[str, List[Dict]] = {}
        
    def track_location(self, location: str, analysis_result: Dict) -> None:
        """Track contamination at a specific location"""
        if location not in self.tracking_data:
            self.tracking_data[location] = []
        self.tracking_data[location].append(analysis_result)
        
    def get_trend(self, location: str) -> Dict:
        """Get contamination trend for a location"""
        if location not in self.tracking_data:
            return {"message": f"No data for location: {location}"}
            
        history = self.tracking_data[location]
        concentrations = [r["total_concentration_ppb"] for r in history]
        
        if len(concentrations) < 2:
            return {"message": "Insufficient data for trend analysis"}
            
        trend = "STABLE"
        if concentrations[-1] > concentrations[0] * 1.5:
            trend = "WORSENING"
        elif concentrations[-1] < concentrations[0] * 0.7:
            trend = "IMPROVING"
            
        return {
            "location": location,
            "trend": trend,
            "first_concentration": concentrations[0],
            "latest_concentration": concentrations[-1],
            "change_percentage": ((concentrations[-1] - concentrations[0]) / concentrations[0]) * 100
        }
        
    def get_all_locations(self) -> List[str]:
        """Get all tracked locations"""
        return list(self.tracking_data.keys())
