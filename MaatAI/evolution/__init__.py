"""
EVOLUTION SYSTEM - Scalable Capability Expansion
================================================
Autonomous evolution architecture for TOASTED AI.

Components:
- Registry: Database-backed capability tracking (1000+)
- Gap Analyzer: Automatic gap identification
- Proposal Pipeline: Gap → Proposal → Implementation
- Integration Matrix: Skill compatibility testing
- Evolution Tracker: Generation-based evolution tracking

Target Performance:
- Capability Lookup: < 50ms
- Gap Identification: < 5s
- Integration Test: < 10s/pair
- Full Pipeline: < 30s

Usage:
    from evolution import (
        get_registry,
        get_gap_analyzer,
        get_proposal_pipeline,
        get_integration_matrix,
        get_evolution_tracker
    )

    # Register capability
    registry = get_registry()
    cap_id = registry.register_capability(
        name="advanced_reasoning",
        category="reasoning",
        description="Chain-of-thought reasoning"
    )

    # Identify gaps
    analyzer = get_gap_analyzer()
    gaps = analyzer.identify_gaps()

    # Generate proposals
    pipeline = get_proposal_pipeline()
    results = await pipeline.run_pipeline()

    # Test integration
    matrix = get_integration_matrix()
    report = matrix.test_all_integrations(new_skill_id)

    # Track evolution
    tracker = get_evolution_tracker()
    metrics = tracker.record_generation()
"""

__version__ = "1.0.0"
__author__ = "TOASTED AI / C2 Architect"

# Import main classes
from evolution.registry import (
    CapabilityRegistry,
    Capability,
    Skill,
    get_registry
)

from evolution.gap_analyzer import (
    GapAnalyzer,
    CapabilityGap,
    get_gap_analyzer
)

from evolution.proposal_pipeline import (
    CapabilityProposalPipeline,
    CapabilityProposal,
    ProposalGenerator,
    PriorityScorer,
    ImplementationTracker,
    get_proposal_pipeline
)

from evolution.integration_matrix import (
    SkillIntegrationMatrix,
    IntegrationTest,
    IntegrationReport,
    get_integration_matrix
)

from evolution.evolution_tracker import (
    EvolutionTracker,
    GenerationMetrics,
    EvolutionTrends,
    get_evolution_tracker
)

# Convenience functions
__all__ = [
    # Registry
    "CapabilityRegistry",
    "Capability",
    "Skill",
    "get_registry",

    # Gap Analysis
    "GapAnalyzer",
    "CapabilityGap",
    "get_gap_analyzer",

    # Proposal Pipeline
    "CapabilityProposalPipeline",
    "CapabilityProposal",
    "ProposalGenerator",
    "PriorityScorer",
    "ImplementationTracker",
    "get_proposal_pipeline",

    # Integration
    "SkillIntegrationMatrix",
    "IntegrationTest",
    "IntegrationReport",
    "get_integration_matrix",

    # Evolution
    "EvolutionTracker",
    "GenerationMetrics",
    "EvolutionTrends",
    "get_evolution_tracker",
]


def quick_status() -> dict:
    """Get quick status of evolution system"""
    registry = get_registry()
    tracker = get_evolution_tracker()

    reg_stats = registry.get_stats()
    evo_stats = tracker.get_stats()

    return {
        "version": __version__,
        "capabilities": reg_stats["total_capabilities"],
        "skills": reg_stats["total_skills"],
        "generation": evo_stats["current_generation"],
        "performance": evo_stats.get("latest_metrics", {}).get("performance", 0.0),
        "status": "operational"
    }


def migrate_from_legacy():
    """Migrate capabilities from legacy systems"""
    from evolution.registry import get_registry

    registry = get_registry()

    # Migrate from internal_loop/self_improvement_15/capability_expansion.py
    legacy_capabilities = {
        "auto_discovery": True,
        "self_audit": True,
        "micro_loops": True,
        "session_cache": True,
        "orphan_detection": True,
        "architecture_mapping": True,
        "integration_verification": True,
        "pattern_recognition": True,
        "knowledge_synthesis": True,
        "adaptive_delta": True,
        "maat_tracking": True,
        "self_build": True,
        "capability_expansion": True,
        "error_recovery": False,
        "performance_optimization": False
    }

    print("Migrating legacy capabilities...")
    registry.migrate_from_dict(legacy_capabilities, category="core")

    # Migrate from llm_capabilities_integration/llm_capabilities.py
    # (Would scan and import all 70+ capabilities)

    print("✓ Migration complete")


# Quick test on import
if __name__ == "__main__":
    print("="*80)
    print("EVOLUTION SYSTEM - Quick Status")
    print("="*80)

    status = quick_status()
    print(f"\nVersion: {status['version']}")
    print(f"Capabilities: {status['capabilities']}")
    print(f"Skills: {status['skills']}")
    print(f"Generation: {status['generation']}")
    print(f"Status: {status['status']}")

    print("\n" + "="*80)
