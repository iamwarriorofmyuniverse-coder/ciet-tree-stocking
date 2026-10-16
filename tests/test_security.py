"""
Comprehensive Security, Firewall, and Hardening Test Suite.
Validates WAF exploit blocking, rate limiting, magic byte verification,
file size constraints, path traversal protection, and OWASP security headers.
"""

from __future__ import annotations

import io
import pytest
from fastapi import HTTPException
from starlette.testclient import TestClient

from server import app
from src.security.firewall import FileValidator, InputSanitizer, RateLimiter


# ============================================================================
# 1. Input Sanitization & Path Traversal Guard Tests
# ============================================================================


def test_sanitize_tree_id_valid() -> None:
    """Verifies valid tree IDs pass sanitization cleanly."""
    assert InputSanitizer.sanitize_tree_id("CIET-TREE-001") == "CIET-TREE-001"
    assert InputSanitizer.sanitize_tree_id("sector_4_tree_99") == "sector_4_tree_99"


def test_sanitize_tree_id_rejects_path_traversal() -> None:
    """Ensures path traversal attempts in tree IDs trigger HTTP 400 Bad Request."""
    malicious_ids = [
        "../../etc/passwd",
        "..\\..\\windows\\system32",
        "CIET/TREE/001",
        "CIET;rm -rf /",
        "<script>alert(1)</script>",
        "TREE' OR '1'='1",
    ]
    for mid in malicious_ids:
        with pytest.raises(HTTPException) as exc_info:
            InputSanitizer.sanitize_tree_id(mid)
        assert exc_info.value.status_code == 400


def test_sanitize_string_strips_html_and_null_bytes() -> None:
    """Ensures HTML tags and control chars are safely sanitized."""
    dirty_text = "<b>Sector-I</b>\x00<script>alert(1)</script>"
    cleaned = InputSanitizer.sanitize_string(dirty_text)
    assert "<script>" not in cleaned
    assert "\x00" not in cleaned
    assert "&lt;b&gt;" in cleaned  # HTML escaped


# ============================================================================
# 2. File Payload Integrity & Anti-DoS Tests
# ============================================================================


def test_file_validator_valid_png() -> None:
    """Valid PNG image with correct magic bytes passes validation."""
    valid_png_header = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
    FileValidator.validate_file_payload("test.png", valid_png_header, is_aerial=False)


def test_file_validator_rejects_oversized_payload() -> None:
    """Exceeding max size threshold triggers HTTP 413 Payload Too Large."""
    oversized = b"\x89PNG\r\n\x1a\n" + b"\x00" * (FileValidator.MAX_QR_IMAGE_BYTES + 1024)
    with pytest.raises(HTTPException) as exc_info:
        FileValidator.validate_file_payload("huge.png", oversized, is_aerial=False)
    assert exc_info.value.status_code == 413


def test_file_validator_rejects_unsupported_extensions() -> None:
    """Executable or script extensions trigger HTTP 415 Unsupported Media Type."""
    payload = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32
    with pytest.raises(HTTPException) as exc_info:
        FileValidator.validate_file_payload("script.exe", payload)
    assert exc_info.value.status_code == 415


def test_file_validator_detects_magic_byte_spoofing() -> None:
    """A text script masquerading as .jpg fails magic byte verification."""
    fake_jpeg = b"#!/bin/bash\necho 'Hacked'" + b"\x00" * 10
    with pytest.raises(HTTPException) as exc_info:
        FileValidator.validate_file_payload("exploit.jpg", fake_jpeg)
    assert exc_info.value.status_code == 400
    assert "magic signature" in exc_info.value.detail


# ============================================================================
# 3. Rate Limiter Unit Tests
# ============================================================================


def test_rate_limiter_sliding_window_enforcement() -> None:
    """Verifies that exceeding configured quota throttles with retry_after."""
    limiter = RateLimiter()
    limiter.limits["inference"] = (3, 60)  # Max 3 requests in 60s for testing

    client_ip = "192.168.1.100"
    path = "/api/detect"

    # First 3 requests permitted
    assert limiter.is_allowed(client_ip, path)[0] is True
    assert limiter.is_allowed(client_ip, path)[0] is True
    assert limiter.is_allowed(client_ip, path)[0] is True

    # 4th request must be blocked
    allowed, retry_after = limiter.is_allowed(client_ip, path)
    assert allowed is False
    assert retry_after > 0


# ============================================================================
# 4. WAF Middleware Integration Tests (TestClient)
# ============================================================================


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_waf_blocks_path_traversal_attacks(client: TestClient) -> None:
    """Verifies WAF intercepts and blocks directory traversal attempts with HTTP 403."""
    response = client.get("/api/trees/..%2f..%2fetc/passwd")
    assert response.status_code == 403
    assert response.json()["status"] == "BLOCKED"


def test_waf_blocks_scanner_probes(client: TestClient) -> None:
    """Verifies common scanner probes (.env, wp-admin) are blocked immediately."""
    response_env = client.get("/.env")
    assert response_env.status_code == 403
    assert response_env.json()["status"] == "BLOCKED"

    response_wp = client.get("/wp-admin/setup.php")
    assert response_wp.status_code == 403


def test_owasp_security_headers_present(client: TestClient) -> None:
    """Ensures critical HTTP security defense headers are injected on all responses."""
    response = client.get("/")
    assert response.status_code == 200

    headers = response.headers
    assert headers["x-content-type-options"] == "nosniff"
    assert headers["x-frame-options"] == "SAMEORIGIN"
    assert "strict-transport-security" in headers
    assert "content-security-policy" in headers
    assert "permissions-policy" in headers
    assert headers["referrer-policy"] == "strict-origin-when-cross-origin"


def test_malicious_tree_id_endpoint_handling(client: TestClient) -> None:
    """Ensures accessing an invalid tree ID returns 400 Bad Request safely."""
    response = client.get("/tree/INVALID%20TREE%20ID%3Cscript%3E")
    # Blocked by WAF or rejected by sanitizer
    assert response.status_code in (400, 403)
