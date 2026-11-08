# Bio-Sync Operator OS 🫀⚡

> **Real-Time Biometric Swarm Governance & 120 FPS Resonant Kinetic Interface powered by Presage SmartSpectra rPPG.**  
> *Built for the Presage SmartSpectra SDK Challenge on DEV Community.*

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![UI: 120 FPS](https://img.shields.io/badge/Benni--Canvas-120_FPS-emerald.svg)](https://benni-os.net)
[![Privacy: Zero-Cloud](https://img.shields.io/badge/Privacy-Zero--Cloud_Local_Only-success.svg)](#consent-and-zero-cloud-privacy-guard)
[![Challenge: Presage](https://img.shields.io/badge/DEV_Challenge-%23presagechallenge-purple.svg)](https://dev.to/t/presagechallenge)

---

> [!WARNING]
> **NON-MEDICAL INFORMATIONAL DISCLAIMER:**  
> Bio-Sync Operator OS and the Presage SmartSpectra SDK integration are experimental research and developer engineering tools designed solely for neuro-ergonomic human-computer interface resonance and autonomous multi-agent throttle governance. **THEY DO NOT DIAGNOSE, TREAT, CURE, MONITOR, OR PREVENT ANY DISEASE OR MEDICAL CONDITION.** They are not medical devices and must never be used for clinical decision-making.

---

## 1. Executive Summary & The Problem

As autonomous AI multi-agent swarms (such as **Benni OS**, **Project Benjamin**, and **Nemesis Gateway**) execute hundreds of high-velocity operations per second—ranging from database migrations and GitHub pull request merges to automated financial settlements—the human-in-the-loop operator experiences severe cognitive overload, vigilance fatigue, and acute stress spikes.

Traditional developer dashboards are completely blind to human physiological strain. When an operator is panicking or experiencing severe autonomic fatigue, they are far more likely to make catastrophic release errors, click accidental approvals, or trigger untested infrastructure teardowns.

**Bio-Sync Operator OS bridges human physiology directly to the autonomous multi-agent swarm:**
1. **Contactless rPPG Sensing via Presage SmartSpectra:** Reads real-time pulse rate (BPM), Heart Rate Variability (HRV RMSSD), respiration rate (BRPM), and optical Blood Volume Pulse (BVP) waveforms directly through a standard laptop webcam without any wearables or electrodes.
2. **120 FPS Resonant Kinetic Canvas (Benni-Canvas Engine):** Couples the interface's physics to the operator's cardiac and respiratory phases using 2nd-order harmonic spring ODEs, providing subconscious neuro-ergonomic visual stabilization.
3. **Autonomous Swarm Governor:** Calculates an observable **Operator Stress Index (OSI)** that dynamically paces high-risk agent actions, enforces cooling leases, and triggers an emergency circuit-breaker on critical infrastructure actions when operator strain exceeds safety boundaries.

---

## 2. System Architecture

```mermaid
flowchart TD
    subgraph Sensing ["1. Contactless Sensing Layer (Presage SmartSpectra SDK)"]
        Cam["Standard Webcam / Video Stream"] --> ROI["Facial ROI Hemoglobin Reflectance"]
        ROI --> rPPG["Optical rPPG Extraction Engine"]
        rPPG --> Privacy["PrivacyGuard: Zero-Cloud RAM Isolation"]
    end

    subgraph Signals ["2. Physiological Telemetry Extraction"]
        Privacy --> Pulse["Cardiac Pulse (BPM) & BVP Waveform"]
        Privacy --> Resp["Respiration Rate (BRPM) & Phase"]
        Privacy --> HRV["Heart Rate Variability (RMSSD / SDNN)"]
    end

    subgraph Resonance ["3. 120 FPS Kinetic Resonator (Benni-Canvas)"]
        Resp --> Spring["2nd-Order Spring ODE: omega_n = 2*pi*(BR/60)"]
        HRV --> Damping["Adaptive Damping: zeta(HRV)"]
        Pulse --> Bokeh["Optical Bokeh CoC & Spectral Luminescence"]
        Spring --> Canvas120["120 FPS Resonant Living Canvas"]
    end

    subgraph Governance ["4. Autonomous Swarm Governor (Project Benjamin & Nemesis)"]
        Pulse & Resp & HRV --> OSI["Operator Stress Index (OSI) Fusion"]
        OSI --> Tier{"Autonomic Tier Evaluation"}
        Tier -->|OPTIMAL: OSI < 0.30| Pass["Unrestricted Swarm Dispatch"]
        Tier -->|ELEVATED: 0.30 - 0.60| Pace["Micro-Throttle High-Risk Agents (1s)"]
        Tier -->|STRAINED: 0.60 - 0.80| Lease["Dynamic Cooling Lease (5s - 15s)"]
        Tier -->|CRITICAL: OSI >= 0.80| Breaker["Emergency Circuit-Breaker: Freeze Destructive Ops"]
    end

    Canvas120 --> Operator["Human Operator (Subconscious Neuro-Feedback)"]
    Breaker --> Swarm["Autonomous Multi-Agent Swarm (Nemesis Gateway 97 Connectors)"]
```

---

## 3. Mathematical Foundations

### A. 2nd-Order Harmonic Spring ODE Interface Coupling
The visual elements of the interface do not use canned CSS keyframes. Instead, motion is numerically integrated at 120 FPS using closed-form Symplectic Euler integration over a damped harmonic oscillator:

$$\ddot{x}(t) + 2\zeta\omega_n \dot{x}(t) + \omega_n^2 x(t) = \omega_n^2 F_{bio}(t)$$

Where:
- **Natural Frequency ($\omega_n$):** Locked to the operator's real-time breathing frequency:
  $$\omega_n = 2\pi \cdot \frac{\text{BRPM}}{60} \quad [\text{rad/s}]$$
- **Dynamic Damping Ratio ($\zeta$):** Coupled to Heart Rate Variability (RMSSD):
  $$\zeta = 1.4 - 0.693 \cdot \text{clamp}\left(\frac{\text{RMSSD} - 15}{65}, 0, 1\right)$$
  - *High HRV (Parasympathetic dominance):* $\zeta \approx 0.707$ (silky critical damping).
  - *Low HRV (Sympathetic stress):* $\zeta \ge 1.2$ (overdamped, grounding the UI to reduce visual agitation).
- **Driving Force ($F_{bio}$):** Weighted linear combination of normalized Blood Volume Pulse and respiratory phase:
  $$F_{bio}(t) = 0.70 \cdot \text{BVP}(t) + 0.30 \cdot \sin(\phi_{resp}(t))$$

### B. Operator Stress Index (OSI)
The multi-sensor physiological fusion index represents instantaneous autonomic load:

$$\text{OSI} = w_1 \cdot \text{clamp}\left(\frac{\text{HR} - \text{HR}_{base}}{40}, 0, 1\right) + w_2 \cdot \left(1 - \text{clamp}\left(\frac{\text{RMSSD} - 15}{\text{RMSSD}_{norm} - 15}, 0, 1\right)\right) + w_3 \cdot \text{clamp}\left(\frac{\text{BR} - \text{BR}_{base}}{12}, 0, 1\right)$$

*Weights calibrated for human autonomic dynamics:* $w_1 = 0.35$ (Cardiac rate), $w_2 = 0.45$ (Vagal tone / HRV), $w_3 = 0.20$ (Tachypnea / Hyperventilation).

---

## 4. Consent and Zero-Cloud Privacy Guard

The architecture follows a strict **Zero-Cloud Local Invariant**:
- **In-Memory Optical Confinement:** Video frames from the camera feed are processed strictly in transient RAM by the SmartSpectra rPPG pipeline. No video frames, facial imagery, or raw camera buffers are ever written to persistent disk or transmitted over the network.
- **Explicit 3-Way Consent:** The `PrivacyGuard` class and Web Modal enforce 3 separate operator acknowledgments:
  1. Camera access consent for optical vital sign extraction.
  2. Local-only zero-cloud processing acknowledgment.
  3. Non-medical research disclaimer agreement.
- **Instant Kill-Switch:** Revoking consent immediately terminates the camera stream, zeroes all telemetry buffers, and logs an immutable audit trail with session nonces.

---

## 5. Quickstart

### Prerequisites
- Python 3.9+
- Modern Web Browser (Chrome / Edge / Firefox) with WebGL support

### Installation
```bash
git clone https://github.com/BenniAlencar/bio-sync-operator-os.git
cd bio-sync-operator-os
pip install -e .
```

### Running the Terminal Telemetry HUD
```bash
# Run real-time streaming demonstration
bio-sync demo --duration 15

# Simulate an acute stress perturbation and observe automatic swarm throttle
bio-sync demo --duration 15 --stress-test

# Run automated diagnostic self-test
bio-sync test
```

### Running Unit Tests
```bash
pytest tests/ -v
```

### Launching the 120 FPS Web Experience
Open `web/index.html` directly in your browser or serve locally:
```bash
python -m http.server 8080 -d web
```
Navigate to `http://localhost:8080` to interact with the full cyber-luminescent dashboard!

---

## 6. Project Structure

```
bio-sync-operator-os/
├── LICENSE                        # Apache 2.0 License
├── pyproject.toml                 # Packaging & pytest configuration
├── README.md                      # Architecture & Developer Guide
├── src/
│   └── bio_sync/
│       ├── __init__.py            # Package exports
│       ├── types.py               # Data contracts (BiometricTelemetry, SwarmAction)
│       ├── privacy_guard.py       # Zero-cloud consent & kill-switch engine
│       ├── smartspectra_adapter.py# Presage SmartSpectra rPPG bridge & fallback
│       ├── kinetic_resonator.py   # 120 FPS 2nd-order harmonic spring ODE solver
│       ├── swarm_governor.py      # Operator Stress Index & throttle leases
│       └── cli.py                 # Interactive terminal telemetry dashboard
├── web/
│   └── index.html                 # 120 FPS Standalone Interactive Web Visualizer
└── tests/
    ├── test_privacy_guard.py      # Privacy & consent verification
    ├── test_smartspectra_adapter.py # rPPG telemetry extraction tests
    ├── test_kinetic_resonator.py  # ODE numerical stability tests
    ├── test_swarm_governor.py     # Autonomic circuit-breaker tests
    └── test_cli.py                # Sparkline & CLI verification
```

---

## 7. Presage SmartSpectra SDK Challenge Details

- **Challenge:** [Presage SmartSpectra SDK Challenge on DEV Community](https://dev.to/devteam/join-the-presage-smartspectra-sdk-challenge-3000-in-prizes-across-10-winners-1370?bb=264850)
- **SDK:** [Presage SmartSpectra Contactless Human Sensing SDK](https://github.com/Presage-Security/SmartSpectra)
- **Categories Targeted:**
  - 🏆 *Best Overall Human-Sensing Experience*
  - 🛡️ *Best Thoughtful Real-World Use*
  - ✨ *Most Creative or Delightful Use*
- **Author:** Benni Alencar ([@bennialencar](https://dev.to/bennialencar)) • [Benni OS Ecosystem](https://benni-os.net)
