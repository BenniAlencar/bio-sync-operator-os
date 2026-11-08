"""
Tests for SmartSpectraAdapter.
"""

import pytest
from bio_sync.privacy_guard import ConsentError, PrivacyGuard
from bio_sync.smartspectra_adapter import SmartSpectraAdapter


def test_adapter_requires_consent():
    guard = PrivacyGuard()
    adapter = SmartSpectraAdapter(privacy_guard=guard)

    # Calling without consent must fail immediately
    with pytest.raises(ConsentError):
        adapter.sample_telemetry()


def test_adapter_telemetry_generation():
    guard = PrivacyGuard()
    guard.grant_consent(True, True, True)
    guard.set_camera_active(True)

    adapter = SmartSpectraAdapter(privacy_guard=guard, baseline_hr=70.0, baseline_br=14.0)
    packet = adapter.sample_telemetry()

    assert packet.pulse_bpm == 70.0
    assert packet.respiration_brpm == 14.0
    assert -1.0 <= packet.blood_volume_pulse <= 1.0
    assert 0.0 <= packet.respiratory_phase <= 2.0 * 3.1416
    assert packet.confidence_score > 0.80

    # Test stress perturbation
    adapter.inject_stress_perturbation(delta_hr=20.0, delta_br=6.0, delta_rmssd=-20.0)
    stressed = adapter.sample_telemetry()
    assert stressed.pulse_bpm == 90.0
    assert stressed.respiration_brpm == 20.0
    assert stressed.hrv_rmssd == 25.0

    # Reset
    adapter.reset_to_baseline()
    reset_packet = adapter.sample_telemetry()
    assert reset_packet.pulse_bpm == 70.0
