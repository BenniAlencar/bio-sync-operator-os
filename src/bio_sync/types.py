"""
Bio-Sync Operator OS: Core Type Definitions.

Data contracts for contactless photoplethysmography (rPPG) telemetry,
neuro-ergonomic kinetic resonance, and autonomous swarm governance.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class StressTier(str, Enum):
    """Categorized human autonomic arousal levels."""
    OPTIMAL = "OPTIMAL"          # Relaxed, high focus, high HRV
    ELEVATED = "ELEVATED"        # Mild cognitive load, acceptable throughput
    STRAINED = "STRAINED"        # Acute stress, impaired decision-making
    CRITICAL = "CRITICAL"        # Severe stress / panic, emergency circuit-breaker active


class ActionRiskLevel(str, Enum):
    """Risk tier for autonomous multi-agent dispatches."""
    LOW = "LOW"                  # Read-only queries, telemetry, local drafting
    MEDIUM = "MEDIUM"            # Non-destructive writes, staging deployments
    HIGH = "HIGH"                # Code merges, production releases, public posts
    CRITICAL = "CRITICAL"        # Financial execution, key rotation, infra tear-down


@dataclass
class BiometricTelemetry:
    """
    Real-time physiological packet extracted via Presage SmartSpectra rPPG.
    
    All calculations are processed strictly in-memory on the local device.
    No optical frames or video buffers are persisted or transmitted.
    """
    timestamp: float = field(default_factory=time.time)
    pulse_bpm: float = 72.0                # Cardiac rate in Beats Per Minute
    respiration_brpm: float = 14.0         # Breathing rate in Breaths Per Minute
    hrv_rmssd: float = 48.0                # Root Mean Square of Successive Differences (ms)
    hrv_sdnn: float = 52.0                 # Standard Deviation of NN intervals (ms)
    optical_snr_db: float = 24.5           # Optical signal-to-noise ratio in decibels
    confidence_score: float = 0.95         # SmartSpectra tracking confidence (0.0 to 1.0)
    blood_volume_pulse: float = 0.0        # Instantaneous normalized arterial pulse waveform (-1.0 to 1.0)
    respiratory_phase: float = 0.0         # Current phase in respiratory cycle [0, 2pi)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "pulse_bpm": round(self.pulse_bpm, 2),
            "respiration_brpm": round(self.respiration_brpm, 2),
            "hrv_rmssd": round(self.hrv_rmssd, 2),
            "hrv_sdnn": round(self.hrv_sdnn, 2),
            "optical_snr_db": round(self.optical_snr_db, 2),
            "confidence_score": round(self.confidence_score, 3),
            "blood_volume_pulse": round(self.blood_volume_pulse, 4),
            "respiratory_phase": round(self.respiratory_phase, 4),
        }


@dataclass
class ConsentRecord:
    """
    Immutable audit proof of explicit operator consent for optical human sensing.
    """
    operator_id: str
    camera_consent_granted: bool
    zero_cloud_processing_acknowledged: bool
    non_medical_disclaimer_accepted: bool
    granted_at: float = field(default_factory=time.time)
    revoked_at: Optional[float] = None
    session_nonce: str = ""

    @property
    def is_valid(self) -> bool:
        return (
            self.camera_consent_granted
            and self.zero_cloud_processing_acknowledged
            and self.non_medical_disclaimer_accepted
            and self.revoked_at is None
        )


@dataclass
class KineticResonanceState:
    """
    Physical parameters of the 120 FPS Benni-Canvas resonant interface.
    
    Coupled to the operator's respiration and pulse frequency via 2nd-order harmonic ODE:
    x'' + 2*zeta*omega_n*x' + omega_n^2*x = F_bio(t)
    """
    timestamp: float = field(default_factory=time.time)
    natural_frequency_hz: float = 0.233    # omega_n derived from respiration (14 bpm = 0.233 Hz)
    damping_ratio: float = 0.707           # zeta (critically damped baseline = 0.707)
    current_displacement: float = 0.0      # Instantaneous spring displacement x(t)
    velocity: float = 0.0                  # Instantaneous velocity x'(t)
    target_displacement: float = 0.0       # Target attractor
    bokeh_coc_pixels: float = 12.0         # Optical Circle of Confusion blur radius
    color_luminescence: float = 0.85       # Subconscious luminescence intensity [0.0, 1.0]
    hue_degrees: float = 165.0             # Emerald cyan (165 deg) to warning amber (40 deg)


@dataclass
class SwarmAction:
    """
    Proposed dispatch packet for an autonomous agent or tool execution.
    """
    action_id: str
    agent_id: str
    tool_name: str
    risk_level: ActionRiskLevel
    estimated_cost_usd: float = 0.0
    payload: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)


@dataclass
class GovernanceDecision:
    """
    Verdict rendered by SwarmGovernor based on real-time Operator Stress Index.
    """
    action_id: str
    approved: bool
    stress_index: float                    # Observable score in [0.0, 1.0]
    stress_tier: StressTier
    throttle_delay_seconds: float = 0.0    # Forced cooldown before dispatch
    cooling_lease_seconds: float = 0.0     # Duration of hold
    intervention_message: str = ""
    timestamp: float = field(default_factory=time.time)
