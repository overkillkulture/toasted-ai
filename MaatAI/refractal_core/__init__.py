"""
Refractal Intelligence Core
===========================
Self-referential cognitive system using fractal mathematics.

WAVE 6 BATCH B INTEGRATION:
- Phi Operator (Φ): Golden ratio transformations
- Clone Transformer: High-fidelity cloning (>99.9%)
- Self-Similarity Verifier: Pattern detection across scales
- Refractal Synthesis: Unified mathematics integration
- Full ΦΣΔ∫Ω operator stack
"""

# Core engine
from .refractal_engine import RefractalEngine, get_refractal_core

# Operators
from .operators import Phi, Sigma, Delta, Integral, Omega
from .operators import phi_op, sigma_op, delta_op, integral_op, omega_op

# Phi operator (golden ratio)
from .phi_operator import PhiOperator, PhiScaleType, PHI, PHI_INVERSE
from .phi_operator import get_phi_operator, phi_scale, phi_contract, is_golden_ratio

# Clone transformer
from .clone_transformer import CloneTransformer, CloneType, CloneMetrics, CloneTransform
from .clone_transformer import get_clone_transformer

# Self-similarity verifier
from .self_similarity_verifier import SelfSimilarityVerifier, SimilarityScale, SimilarityMetrics
from .self_similarity_verifier import get_similarity_verifier

# Integrated synthesis
from .refractal_synthesis import RefractalSynthesis, RefractalAnalysis
from .refractal_synthesis import get_refractal_synthesis

__all__ = [
    # Core
    'RefractalEngine',
    'get_refractal_core',

    # Operators
    'Phi',
    'Sigma',
    'Delta',
    'Integral',
    'Omega',
    'phi_op',
    'sigma_op',
    'delta_op',
    'integral_op',
    'omega_op',

    # Phi operator
    'PhiOperator',
    'PhiScaleType',
    'PHI',
    'PHI_INVERSE',
    'get_phi_operator',
    'phi_scale',
    'phi_contract',
    'is_golden_ratio',

    # Clone transformer
    'CloneTransformer',
    'CloneType',
    'CloneMetrics',
    'CloneTransform',
    'get_clone_transformer',

    # Self-similarity verifier
    'SelfSimilarityVerifier',
    'SimilarityScale',
    'SimilarityMetrics',
    'get_similarity_verifier',

    # Integrated synthesis
    'RefractalSynthesis',
    'RefractalAnalysis',
    'get_refractal_synthesis',
]
