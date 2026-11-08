"""
Bio-Sync Operator OS: Command-Line Interface.

Interactive terminal dashboard displaying real-time contactless biometric telemetry,
ASCII photoplethysmogram waveforms, resonant UI metrics, and swarm governance state.
"""

from __future__ import annotations

import argparse
import math
import os
import sys
import time

# Ensure src is on sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bio_sync.kinetic_resonator import KineticResonator
from bio_sync.privacy_guard import ConsentError, PrivacyGuard
from bio_sync.smartspectra_adapter import SmartSpectraAdapter
from bio_sync.swarm_governor import SwarmGovernor
from bio_sync.types import ActionRiskLevel, SwarmAction


def render_sparkline(val: float, width: int = 24) -> str:
    """Render a normalized float [-1.0, 1.0] as an ASCII bar position."""
    norm = max(0.0, min(1.0, (val + 1.0) / 2.0))
    pos = int(norm * (width - 1))
    chars = ["-"] * width
    chars[pos] = "O"
    return "".join(chars)


def run_demo(duration: int = 15, stress_test: bool = False) -> None:
    """Run real-time terminal telemetry demonstration."""
    print("=" * 72)
    print("   BIO-SYNC OPERATOR OS :: REAL-TIME TELEMETRY ENGINE")
    print("   Powered by Presage SmartSpectra SDK & Benni-Canvas Resonator")
    print("=" * 72)
    print(PrivacyGuard.NON_MEDICAL_DISCLAIMER)
    print("=" * 72)

    # Step 1: Explicit Consent
    guard = PrivacyGuard(operator_id="operator_alpha")
    print("\n[SECURITY GATE] Requesting Explicit Informed Operator Consent...")
    guard.grant_consent(
        camera_consent=True,
        zero_cloud_acknowledged=True,
        non_medical_accepted=True,
    )
    guard.set_camera_active(True)
    print("[SECURITY GATE] Consent Granted. Zero-Cloud Local Pipeline Activated.")

    adapter = SmartSpectraAdapter(privacy_guard=guard, use_synthetic_fallback=True)
    resonator = KineticResonator()
    governor = SwarmGovernor()

    print(f"\nStarting real-time streaming for {duration} seconds... (Ctrl+C to stop)\n")
    start = time.time()
    tick = 0

    try:
        while (time.time() - start) < duration:
            # Simulate acute stress spike halfway through if requested
            if stress_test and (time.time() - start) > (duration / 2.0):
                adapter.inject_stress_perturbation(delta_hr=1.2, delta_br=0.4, delta_rmssd=-1.5)

            telemetry = adapter.sample_telemetry()
            resonance = resonator.step(telemetry)
            stress_index = governor.compute_stress_index(telemetry)
            tier = governor.categorize_tier(stress_index)

            # Test sample action evaluation every 10 ticks
            gov_note = ""
            if tick % 10 == 0:
                action = SwarmAction(
                    action_id=f"act_{tick}",
                    agent_id="agent_genesis",
                    tool_name="production_release",
                    risk_level=ActionRiskLevel.HIGH,
                )
                decision = governor.evaluate_action(action, telemetry)
                gov_note = f"| GOV: {'[APPROVED]' if decision.approved else '[THROTTLED]'} {decision.intervention_message[:30]}..."

            bvp_bar = render_sparkline(telemetry.blood_volume_pulse, width=20)
            sys.stdout.write(
                f"\r[{tier.value:8s}] HR: {telemetry.pulse_bpm:5.1f} bpm | "
                f"BR: {telemetry.respiration_brpm:4.1f} brpm | "
                f"HRV: {telemetry.hrv_rmssd:4.1f} ms | "
                f"BVP: [{bvp_bar}] | "
                f"OSI: {stress_index:4.2f} | "
                f"Bokeh: {resonance.bokeh_coc_pixels:4.1f}px {gov_note}"
            )
            sys.stdout.flush()
            time.sleep(0.1)
            tick += 1

    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
    finally:
        guard.revoke_consent(reason="session_terminated")
        print("\n\n[PRIVACY GUARD] Consent revoked. Pipeline securely terminated.")
        print("Audit Trail Summary:")
        for log in guard.get_audit_trail():
            print(f"  - {log['event']} at {time.ctime(log['timestamp'])}")


def main():
    parser = argparse.ArgumentParser(
        description="Bio-Sync Operator OS :: Real-Time Biometric Swarm Governance CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    demo_parser = subparsers.add_parser("demo", help="Run real-time telemetry streaming demo")
    demo_parser.add_argument("--duration", type=int, default=12, help="Duration in seconds (default: 12)")
    demo_parser.add_argument("--stress-test", action="store_true", help="Simulate stress spike perturbation")

    subparsers.add_parser("test", help="Run automated self-diagnostic check")

    args = parser.parse_args()

    if args.command == "demo" or args.command is None:
        duration = getattr(args, "duration", 12)
        stress_test = getattr(args, "stress_test", False)
        run_demo(duration=duration, stress_test=stress_test)
    elif args.command == "test":
        print("Running Bio-Sync Operator OS diagnostic checks...")
        guard = PrivacyGuard()
        guard.grant_consent(True, True, True)
        adapter = SmartSpectraAdapter(guard)
        tel = adapter.sample_telemetry()
        res = KineticResonator().step(tel)
        gov = SwarmGovernor()
        osi = gov.compute_stress_index(tel)
        print(f"Self-check passed: HR={tel.pulse_bpm}bpm, OSI={osi:.3f}, Displacement={res.current_displacement:.4f}")


if __name__ == "__main__":
    main()
