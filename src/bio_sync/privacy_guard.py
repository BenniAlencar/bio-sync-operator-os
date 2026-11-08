"""
Bio-Sync Operator OS: Privacy Guard & Zero-Cloud Governance.

Strict compliance engine enforcing:
1. Explicit informed operator consent prior to camera activation.
2. In-memory zero-cloud optical buffer confinement (RFC-level assertion).
3. Non-medical informational disclaimer verification.
4. Immediate deterministic kill-switch upon revocation.
"""

from __future__ import annotations

import hashlib
import os
import secrets
import time
from typing import List, Optional

from bio_sync.types import ConsentRecord


class ConsentError(PermissionError):
    """Raised when optical biometric processing is attempted without valid consent."""
    pass


class PrivacyGuard:
    """
    Enforces privacy invariants and ethical boundaries for contactless rPPG sensing.
    
    Invariants:
    - No video or optical frame data is ever saved to persistent disk or sent over network.
    - Capturing stops synchronously the millisecond consent is revoked.
    - All telemetry calculations operate strictly on anonymous normalized scalars.
    """

    NON_MEDICAL_DISCLAIMER = (
        "NON-MEDICAL INFORMATIONAL NOTICE: Bio-Sync Operator OS and Presage SmartSpectra "
        "SDK are research and developer engineering tools designed solely for neuro-ergonomic "
        "UI resonance and autonomous agent throttle governance. They DO NOT diagnose, treat, "
        "cure, monitor, or prevent any disease, medical condition, or physical affliction. "
        "They are not medical devices and must not be used for clinical decision-making."
    )

    def __init__(self, operator_id: str = "default_operator"):
        self.operator_id = operator_id
        self._current_consent: Optional[ConsentRecord] = None
        self._audit_log: List[dict] = []
        self._is_camera_active: bool = False

    @property
    def has_valid_consent(self) -> bool:
        """Returns True only if an active, unrevoked consent record exists."""
        return self._current_consent is not None and self._current_consent.is_valid

    @property
    def is_camera_active(self) -> bool:
        return self._is_camera_active

    def grant_consent(
        self,
        camera_consent: bool,
        zero_cloud_acknowledged: bool,
        non_medical_accepted: bool,
    ) -> ConsentRecord:
        """
        Record explicit operator consent.
        
        All three flags must be strictly True. Any False or missing assertion fails.
        """
        if not (camera_consent and zero_cloud_acknowledged and non_medical_accepted):
            missing = []
            if not camera_consent:
                missing.append("camera_consent")
            if not zero_cloud_acknowledged:
                missing.append("zero_cloud_acknowledged")
            if not non_medical_accepted:
                missing.append("non_medical_accepted")
            raise ConsentError(
                f"Consent denied: Operator did not agree to mandatory terms: {missing}"
            )

        nonce = secrets.token_hex(16)
        record = ConsentRecord(
            operator_id=self.operator_id,
            camera_consent_granted=True,
            zero_cloud_processing_acknowledged=True,
            non_medical_disclaimer_accepted=True,
            granted_at=time.time(),
            revoked_at=None,
            session_nonce=nonce,
        )
        self._current_consent = record
        self._log_audit("CONSENT_GRANTED", nonce=nonce)
        return record

    def revoke_consent(self, reason: str = "operator_action") -> None:
        """
        Hard kill-switch. Instantly invalidates consent and terminates optical pipelines.
        """
        if self._current_consent:
            self._current_consent.revoked_at = time.time()
            nonce = self._current_consent.session_nonce
        else:
            nonce = "NONE"

        self._is_camera_active = False
        self._log_audit("CONSENT_REVOKED", reason=reason, nonce=nonce)

    def verify_pipeline_authorization(self) -> None:
        """
        Runtime invariant check. Must be invoked before every optical processing cycle.
        """
        if not self.has_valid_consent:
            raise ConsentError(
                "Optical pipeline blocked: Valid operator consent is not granted or has been revoked."
            )

    def set_camera_active(self, active: bool) -> None:
        """Update hardware activation status under consent guard."""
        if active:
            self.verify_pipeline_authorization()
            self._is_camera_active = True
            self._log_audit("CAMERA_ACTIVATED")
        else:
            self._is_camera_active = False
            self._log_audit("CAMERA_DEACTIVATED")

    def assert_zero_cloud_compliance(self, target_url_or_host: Optional[str] = None) -> bool:
        """
        Verifies that no optical or biometric frame payloads are targeted to external network hosts.
        """
        if target_url_or_host is not None:
            # Only loopback / local unix sockets permitted for IPC
            allowed = ["localhost", "127.0.0.1", "::1", "0.0.0.0"]
            is_local = any(host in target_url_or_host for host in allowed)
            if not is_local:
                raise ConsentError(
                    f"Security Violation: External network exfiltration attempt detected to {target_url_or_host}."
                )
        return True

    def get_audit_trail(self) -> List[dict]:
        """Return full immutable history of privacy events for compliance inspection."""
        return list(self._audit_log)

    def _log_audit(self, event_type: str, **kwargs) -> None:
        entry = {
            "timestamp": time.time(),
            "operator_id": self.operator_id,
            "event": event_type,
            "details": kwargs,
        }
        self._audit_log.append(entry)
