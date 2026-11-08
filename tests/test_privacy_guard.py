"""
Tests for PrivacyGuard & Zero-Cloud Compliance.
"""

import pytest
from bio_sync.privacy_guard import ConsentError, PrivacyGuard


def test_consent_denied_without_explicit_flags():
    guard = PrivacyGuard(operator_id="test_op")
    assert not guard.has_valid_consent

    # Missing zero_cloud_acknowledged
    with pytest.raises(ConsentError) as exc_info:
        guard.grant_consent(
            camera_consent=True,
            zero_cloud_acknowledged=False,
            non_medical_accepted=True,
        )
    assert "zero_cloud_acknowledged" in str(exc_info.value)
    assert not guard.has_valid_consent


def test_consent_granted_and_revocation():
    guard = PrivacyGuard(operator_id="test_op")
    record = guard.grant_consent(
        camera_consent=True,
        zero_cloud_acknowledged=True,
        non_medical_accepted=True,
    )
    assert record.is_valid
    assert guard.has_valid_consent

    # Activate camera
    guard.set_camera_active(True)
    assert guard.is_camera_active

    # Revoke consent
    guard.revoke_consent(reason="user_opt_out")
    assert not guard.has_valid_consent
    assert not guard.is_camera_active

    # Subsequent verification must raise ConsentError
    with pytest.raises(ConsentError):
        guard.verify_pipeline_authorization()


def test_zero_cloud_assertion():
    guard = PrivacyGuard()
    # Localhost allowed
    assert guard.assert_zero_cloud_compliance("http://localhost:8080/stream")
    assert guard.assert_zero_cloud_compliance("http://127.0.0.1:5000/metrics")

    # External exfiltration blocked
    with pytest.raises(ConsentError):
        guard.assert_zero_cloud_compliance("https://external-cloud-api.com/v1/frames")
