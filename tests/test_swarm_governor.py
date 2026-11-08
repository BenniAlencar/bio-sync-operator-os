"""
Tests for SwarmGovernor autonomic rate-limiting and circuit breaking.
"""

from bio_sync.swarm_governor import SwarmGovernor
from bio_sync.types import (
    ActionRiskLevel,
    BiometricTelemetry,
    StressTier,
    SwarmAction,
)


def test_swarm_governor_stress_index():
    gov = SwarmGovernor(baseline_hr=70.0, baseline_br=14.0, norm_rmssd=50.0)

    relaxed = BiometricTelemetry(pulse_bpm=70.0, respiration_brpm=14.0, hrv_rmssd=50.0)
    osi_relaxed = gov.compute_stress_index(relaxed)
    assert osi_relaxed < 0.20
    assert gov.categorize_tier(osi_relaxed) == StressTier.OPTIMAL

    stressed = BiometricTelemetry(pulse_bpm=110.0, respiration_brpm=26.0, hrv_rmssd=15.0)
    osi_stressed = gov.compute_stress_index(stressed)
    assert osi_stressed >= 0.80
    assert gov.categorize_tier(osi_stressed) == StressTier.CRITICAL


def test_action_evaluation_under_stress():
    gov = SwarmGovernor()
    critical_action = SwarmAction(
        action_id="act_release_001",
        agent_id="deploy_bot",
        tool_name="drop_database",
        risk_level=ActionRiskLevel.CRITICAL,
    )

    # Under relaxed state, action is approved
    relaxed_tel = BiometricTelemetry(pulse_bpm=68.0, respiration_brpm=13.0, hrv_rmssd=55.0)
    decision = gov.evaluate_action(critical_action, relaxed_tel)
    assert decision.approved
    assert decision.throttle_delay_seconds == 0.0

    # Under critical stress, critical action is rejected and lease enforced
    stressed_tel = BiometricTelemetry(pulse_bpm=120.0, respiration_brpm=28.0, hrv_rmssd=12.0)
    decision_stressed = gov.evaluate_action(critical_action, stressed_tel)
    assert not decision_stressed.approved
    assert decision_stressed.cooling_lease_seconds > 0.0
    assert "CRITICAL PHYSIOLOGICAL STRAIN" in decision_stressed.intervention_message
