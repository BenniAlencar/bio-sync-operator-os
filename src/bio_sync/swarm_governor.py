"""
Bio-Sync Operator OS: Autonomous Swarm Governor.

Regulates multi-agent action dispatch, API throughput, and high-consequence
operations according to real-time human autonomic arousal and cognitive load.

Operates on the Operator Stress Index (OSI):
- Low stress (OPTIMAL): Unrestricted agent dispatch throughput.
- Moderate stress (ELEVATED): Soft rate-limiting and audit logging.
- Acute stress (STRAINED): Mandatory cooling leases on HIGH-risk actions.
- Severe strain (CRITICAL): Hard circuit-breaker on irreversible/financial dispatches.
"""

from __future__ import annotations

import time
from typing import Dict, List, Optional

from bio_sync.types import (
    ActionRiskLevel,
    BiometricTelemetry,
    GovernanceDecision,
    StressTier,
    SwarmAction,
)


class SwarmGovernor:
    """
    Adaptive cyber-physical gatekeeper matching agent autonomy to operator physiological capacity.
    """

    def __init__(
        self,
        baseline_hr: float = 72.0,
        baseline_br: float = 14.0,
        norm_rmssd: float = 50.0,
        w_hr: float = 0.35,
        w_hrv: float = 0.45,
        w_br: float = 0.20,
    ):
        self.baseline_hr = baseline_hr
        self.baseline_br = baseline_br
        self.norm_rmssd = norm_rmssd
        self.w_hr = w_hr
        self.w_hrv = w_hrv
        self.w_br = w_br

        self._active_leases: Dict[str, float] = {}  # action_id -> expiry_timestamp
        self._governance_history: List[GovernanceDecision] = []

    def compute_stress_index(self, telemetry: BiometricTelemetry) -> float:
        """
        Calculate continuous Operator Stress Index (OSI) in range [0.0, 1.0].
        
        Mathematical model:
        OSI = w_hr * Delta_HR + w_hrv * (1 - Norm_RMSSD) + w_br * Delta_BR
        """
        # HR elevation ratio: 0.0 at baseline, 1.0 at baseline + 40 bpm
        delta_hr = max(0.0, min(1.0, (telemetry.pulse_bpm - self.baseline_hr) / 40.0))

        # HRV suppression: 0.0 when RMSSD >= norm_rmssd (50ms), 1.0 when RMSSD <= 15ms
        norm_rmssd = max(0.0, min(1.0, (telemetry.hrv_rmssd - 15.0) / (self.norm_rmssd - 15.0)))
        hrv_deficit = 1.0 - norm_rmssd

        # Breathing rate elevation ratio: 0.0 at baseline, 1.0 at baseline + 12 brpm
        delta_br = max(0.0, min(1.0, (telemetry.respiration_brpm - self.baseline_br) / 12.0))

        osi = (self.w_hr * delta_hr) + (self.w_hrv * hrv_deficit) + (self.w_br * delta_br)
        return max(0.0, min(1.0, osi))

    def categorize_tier(self, osi: float) -> StressTier:
        """Maps continuous stress index into operational tiers."""
        if osi < 0.30:
            return StressTier.OPTIMAL
        elif osi < 0.60:
            return StressTier.ELEVATED
        elif osi < 0.80:
            return StressTier.STRAINED
        else:
            return StressTier.CRITICAL

    def evaluate_action(self, action: SwarmAction, telemetry: BiometricTelemetry) -> GovernanceDecision:
        """
        Render zero-trust governance decision on whether to permit, throttle, or reject an agent action.
        """
        osi = self.compute_stress_index(telemetry)
        tier = self.categorize_tier(osi)
        now = time.time()

        # Check existing cooling lease
        if action.action_id in self._active_leases:
            expiry = self._active_leases[action.action_id]
            if now < expiry:
                remaining = expiry - now
                decision = GovernanceDecision(
                    action_id=action.action_id,
                    approved=False,
                    stress_index=osi,
                    stress_tier=tier,
                    throttle_delay_seconds=remaining,
                    cooling_lease_seconds=remaining,
                    intervention_message=f"Action held under active cooling lease. Remaining: {remaining:.1f}s",
                )
                self._governance_history.append(decision)
                return decision
            else:
                del self._active_leases[action.action_id]

        approved = True
        throttle_delay = 0.0
        cooling_lease = 0.0
        msg = "Dispatched within acceptable physiological envelope."

        if tier == StressTier.OPTIMAL:
            # Full speed ahead
            pass

        elif tier == StressTier.ELEVATED:
            if action.risk_level in [ActionRiskLevel.HIGH, ActionRiskLevel.CRITICAL]:
                throttle_delay = 1.0
                msg = "Mild autonomic elevation detected; micro-throttle applied."

        elif tier == StressTier.STRAINED:
            if action.risk_level == ActionRiskLevel.CRITICAL:
                approved = False
                cooling_lease = 15.0
                self._active_leases[action.action_id] = now + cooling_lease
                msg = "Acute operator strain detected. CRITICAL action paused for 15s neuro-cooling window."
            elif action.risk_level == ActionRiskLevel.HIGH:
                throttle_delay = 3.0
                cooling_lease = 5.0
                self._active_leases[action.action_id] = now + cooling_lease
                msg = "High risk action paced with 5s confirmation lease due to elevated operator strain."

        elif tier == StressTier.CRITICAL:
            if action.risk_level in [ActionRiskLevel.CRITICAL, ActionRiskLevel.HIGH]:
                approved = False
                cooling_lease = 30.0
                self._active_leases[action.action_id] = now + cooling_lease
                msg = (
                    "CRITICAL PHYSIOLOGICAL STRAIN ALERT. Autonomic circuit-breaker active. "
                    "All destructive/high-risk agent actions frozen for 30s. Please follow kinetic breathing prompt."
                )
            else:
                throttle_delay = 2.0
                msg = "Low-risk action allowed with pacing delay under critical operator strain."

        decision = GovernanceDecision(
            action_id=action.action_id,
            approved=approved,
            stress_index=osi,
            stress_tier=tier,
            throttle_delay_seconds=throttle_delay,
            cooling_lease_seconds=cooling_lease,
            intervention_message=msg,
        )
        self._governance_history.append(decision)
        return decision

    def get_decision_history(self) -> List[GovernanceDecision]:
        return list(self._governance_history)
