"""
Bio-Sync Operator OS: Real-Time Biometric Swarm Governance & Kinetic Resonance.
"""

from bio_sync.kinetic_resonator import KineticResonator
from bio_sync.privacy_guard import ConsentError, PrivacyGuard
from bio_sync.smartspectra_adapter import SmartSpectraAdapter
from bio_sync.swarm_governor import SwarmGovernor
from bio_sync.types import (
    ActionRiskLevel,
    BiometricTelemetry,
    ConsentRecord,
    GovernanceDecision,
    KineticResonanceState,
    StressTier,
    SwarmAction,
)

__version__ = "0.1.0"
__all__ = [
    "BiometricTelemetry",
    "ConsentRecord",
    "KineticResonanceState",
    "SwarmAction",
    "GovernanceDecision",
    "StressTier",
    "ActionRiskLevel",
    "PrivacyGuard",
    "ConsentError",
    "SmartSpectraAdapter",
    "KineticResonator",
    "SwarmGovernor",
]
