"""
Bio-Sync Operator OS: 120 FPS Kinetic Resonator Engine.

Couples real-time human cardiac and respiratory rhythms to interface motion physics
using closed-form 2nd-order harmonic spring ordinary differential equations (ODE):

    x''(t) + 2*zeta*omega_n*x'(t) + omega_n^2*x(t) = F_bio(t)

Where:
- omega_n (natural frequency) is locked to the operator's breathing frequency: omega_n = 2*pi*(BR / 60)
- zeta (damping ratio) dynamically adapts to Heart Rate Variability (HRV):
    * High HRV (parasympathetic dominance) -> zeta = 0.707 (silky critical damping)
    * Low HRV (sympathetic stress) -> zeta >= 1.2 (overdamped, grounded stabilization)
- Optical bokeh Circle of Confusion (CoC) expands and contracts in respiratory harmony.
"""

from __future__ import annotations

import math
import time
from typing import Optional

from bio_sync.types import BiometricTelemetry, KineticResonanceState


class KineticResonator:
    """
    120 FPS deterministic physics integrator coupling human biometrics to UI dynamics.
    
    Guarantees:
    - Numerical stability across variable dt (up to 120 FPS).
    - Conservative energy dissipation preventing unbounded spring explosions.
    - Continuous neuro-ergonomic visual feedback.
    """

    def __init__(
        self,
        base_bokeh_pixels: float = 12.0,
        base_hue: float = 165.0,  # Emerald Cyan
    ):
        self.base_bokeh_pixels = base_bokeh_pixels
        self.base_hue = base_hue

        # Internal state variables
        self._displacement: float = 0.0
        self._velocity: float = 0.0
        self._last_tick_time: float = time.time()
        self._state = KineticResonanceState()

    @property
    def current_state(self) -> KineticResonanceState:
        return self._state

    def step(self, telemetry: BiometricTelemetry, dt: Optional[float] = None) -> KineticResonanceState:
        """
        Advance the harmonic oscillator by time delta dt (seconds).
        If dt is None, wall-clock time difference is used.
        """
        now = time.time()
        if dt is None:
            dt = max(0.001, min(0.05, now - self._last_tick_time))
        self._last_tick_time = now

        # Compute natural frequency omega_n (rad/s) from breathing rate (BRPM)
        # Standard resting human breathing: 10 - 20 BRPM -> 0.166 - 0.333 Hz
        breathing_hz = max(0.1, telemetry.respiration_brpm / 60.0)
        omega_n = 2.0 * math.pi * breathing_hz

        # Compute damping ratio zeta:
        # High RMSSD (> 50 ms) -> zeta ~ 0.707 (optimal critical damping)
        # Low RMSSD (< 20 ms) -> zeta rises up to 1.4 (overdamped, grounding)
        norm_hrv = max(0.0, min(1.0, (telemetry.hrv_rmssd - 15.0) / 65.0))
        zeta = 1.4 - (0.693 * norm_hrv)

        # External driving force F_bio derived from blood volume pulse & respiratory phase
        # Smooth cyclical attractor [-1.0, 1.0]
        f_bio = (0.7 * telemetry.blood_volume_pulse) + (0.3 * math.sin(telemetry.respiratory_phase))

        # Numerical integration using semi-implicit Symplectic Euler
        # Acceleration: a = f_bio - 2*zeta*omega_n*v - omega_n^2 * x
        spring_force = -(omega_n ** 2) * self._displacement
        damping_force = -2.0 * zeta * omega_n * self._velocity
        acceleration = spring_force + damping_force + (omega_n ** 2 * f_bio)

        self._velocity += acceleration * dt
        self._displacement += self._velocity * dt

        # Bound displacement to prevent numerical overshoot in extreme transients
        self._displacement = max(-2.0, min(2.0, self._displacement))

        # Compute Optical Bokeh Circle of Confusion (CoC)
        # Expands on inhalation, focuses on exhalation
        respiratory_envelope = (1.0 + math.sin(telemetry.respiratory_phase)) * 0.5
        bokeh_coc = self.base_bokeh_pixels + (8.0 * respiratory_envelope)

        # Compute Subconscious Color Luminescence & Hue
        # High stress / low HRV shifts hue towards amber (45) or coral (15)
        # Optimal relaxed states glow at pure Benni Emerald (165)
        stress_factor = 1.0 - norm_hrv
        computed_hue = self.base_hue - (stress_factor * 125.0)  # 165 down to 40
        luminescence = 0.75 + (0.25 * math.sin(telemetry.respiratory_phase))

        self._state = KineticResonanceState(
            timestamp=now,
            natural_frequency_hz=breathing_hz,
            damping_ratio=zeta,
            current_displacement=self._displacement,
            velocity=self._velocity,
            target_displacement=f_bio,
            bokeh_coc_pixels=bokeh_coc,
            color_luminescence=luminescence,
            hue_degrees=computed_hue,
        )

        return self._state

    def reset(self) -> None:
        """Reset oscillator position and velocity to neutral zero."""
        self._displacement = 0.0
        self._velocity = 0.0
        self._last_tick_time = time.time()
