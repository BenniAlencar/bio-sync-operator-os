"""
Tests for KineticResonator 120 FPS physics integrator.
"""

from bio_sync.kinetic_resonator import KineticResonator
from bio_sync.types import BiometricTelemetry


def test_kinetic_resonator_integration_step():
    resonator = KineticResonator(base_bokeh_pixels=10.0, base_hue=165.0)

    telemetry = BiometricTelemetry(
        pulse_bpm=75.0,
        respiration_brpm=15.0,
        hrv_rmssd=45.0,
        blood_volume_pulse=0.5,
        respiratory_phase=1.57,  # peak inhalation
    )

    state = resonator.step(telemetry, dt=1.0 / 120.0)
    assert state.natural_frequency_hz == 15.0 / 60.0
    assert 0.5 <= state.damping_ratio <= 1.5
    assert -2.0 <= state.current_displacement <= 2.0
    assert state.bokeh_coc_pixels > 10.0
    assert 0.0 <= state.color_luminescence <= 1.0


def test_kinetic_resonator_stability():
    resonator = KineticResonator()
    telemetry = BiometricTelemetry(
        pulse_bpm=120.0,
        respiration_brpm=28.0,
        hrv_rmssd=18.0,  # low HRV
        blood_volume_pulse=-0.8,
        respiratory_phase=0.0,
    )

    # Run 100 simulation frames at 120 FPS
    for _ in range(100):
        state = resonator.step(telemetry, dt=1.0 / 120.0)
        assert not (state.current_displacement != state.current_displacement)  # No NaN
        assert abs(state.current_displacement) <= 2.0  # Bounded
