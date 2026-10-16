"""
Enterprise Firewall, Rate Limiting, Input Sanitization, and DoS Hardening Subsystem.
Engineered for Coimbatore Institute of Engineering and Technology (CIET).
"""

from __future__ import annotations

import html
import logging
import re
import time
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple

from fastapi import HTTPException, Request, Response
from PIL import Image
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = logging.getLogger("ciet.security.firewall")

# Configure PIL safe pixel limits against decompression bomb DoS
Image.MAX_IMAGE_PIXELS = 60_000_000  # Cap at 60 MegaPixels


class RateLimiter:
    """
    High-performance in-memory sliding window rate limiter.
    Shields compute-heavy endpoints (e.g. YOLO ML inference) against DDoS & abuse.
    """

    def __init__(self) -> None:
        # {endpoint_category: {client_ip: [timestamp1, timestamp2, ...]}}
        self._history: Dict[str, Dict[str, List[float]]] = defaultdict(lambda: defaultdict(list))
        # Default rate limits: (max_requests, window_seconds)
        self.limits: Dict[str, Tuple[int, int]] = {
            "inference": (20, 60),    # 20 ML detections per minute per IP
            "qr_scan": (35, 60),      # 35 QR decodes per minute per IP
            "general": (150, 60),     # 150 read requests per minute per IP
        }
        self._last_cleanup = time.time()

    def _cleanup_old_records(self, current_time: float) -> None:
        """Prunes stale history timestamps to prevent unbounded memory growth."""
        if current_time - self._last_cleanup < 30.0:
            return

        for category, ip_dict in list(self._history.items()):
            _, window_sec = self.limits.get(category, (150, 60))
            cutoff = current_time - window_sec
            for ip, timestamps in list(ip_dict.items()):
                valid_ts = [t for t in timestamps if t > cutoff]
                if valid_ts:
                    ip_dict[ip] = valid_ts
                else:
                    del ip_dict[ip]

        self._last_cleanup = current_time

    def is_allowed(self, client_ip: str, path: str) -> Tuple[bool, int]:
        """
        Evaluates whether request from client_ip to path is within SLA quota.

        Returns:
            Tuple of (is_allowed: bool, retry_after_seconds: int).
        """
        now = time.time()
        self._cleanup_old_records(now)

        # Categorize route
        if path.startswith("/api/detect"):
            category = "inference"
        elif path.startswith("/api/scan-qr"):
            category = "qr_scan"
        else:
            category = "general"

        max_reqs, window_sec = self.limits[category]
        cutoff = now - window_sec

        timestamps = self._history[category][client_ip]
        # Keep only timestamps in current sliding window
        valid_timestamps = [t for t in timestamps if t > cutoff]
        self._history[category][client_ip] = valid_timestamps

        if len(valid_timestamps) >= max_reqs:
            oldest_in_window = valid_timestamps[0]
            retry_after = max(1, int(window_sec - (now - oldest_in_window)))
            logger.warning(
                "[RATE LIMIT BREACH] IP %s breached %s quota (%d reqs / %ds). Retry-After: %ds",
                client_ip,
                category,
                max_reqs,
                window_sec,
                retry_after,
            )
            return False, retry_after

        # Record this request
        valid_timestamps.append(now)
        return True, 0


class SecurityFirewallMiddleware(BaseHTTPMiddleware):
    """
    Enterprise Web Application Firewall (WAF) middleware:
    - Blocks exploit scanners, path traversal, and injection vectors.
    - Enforces sliding window rate limits per client IP.
    - Injects OWASP defense-in-depth HTTP security headers.
    """

    # Malicious scan patterns (e.g. crawler bots hunting for PHP, env files, config leaks)
    EXPLOIT_PATTERNS = [
        re.compile(r"(\.\./|\.\.\\|%2e%2e%2f|%2e%2e\/)", re.IGNORECASE),  # Path traversal
        re.compile(r"(\.env|\.git|\.aws|\.ssh|wp-admin|phpmyadmin|eval\(|<script)", re.IGNORECASE),
        re.compile(r"(\bunion\b.*\bselect\b|\bselect\b.*\bfrom\b)", re.IGNORECASE), # SQLi
        re.compile(r"(;\s*cat\s+|\|\s*ls\s+|;\s*rm\s+|\$\(.*\)|`.*`)", re.IGNORECASE), # Command injection
    ]

    def __init__(self, app, rate_limiter: Optional[RateLimiter] = None) -> None:
        super().__init__(app)
        self.rate_limiter = rate_limiter or RateLimiter()

    def _get_client_ip(self, request: Request) -> str:
        """Resolves real client IP taking reverse proxy headers into account safely."""
        forwarded = request.headers.get("CF-Connecting-IP") or request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.client.host if request.client else "127.0.0.1"

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = self._get_client_ip(request)
        path = request.url.path
        query = str(request.url.query)
        target_check = f"{path}?{query}" if query else path

        # 1. WAF Pattern Inspection: Block automated exploit probes & directory traversal
        for pattern in self.EXPLOIT_PATTERNS:
            if pattern.search(target_check):
                logger.warning(
                    "[SECURITY WAF BLOCKED] Malicious pattern detected from IP %s on '%s'",
                    client_ip,
                    target_check,
                )
                return Response(
                    content='{"status":"BLOCKED","message":"Forbidden: Malicious signature detected by CIET WAF Shield."}',
                    status_code=403,
                    media_type="application/json",
                )

        # 2. Rate Limiting Enforcer
        allowed, retry_after = self.rate_limiter.is_allowed(client_ip, path)
        if not allowed:
            return Response(
                content=f'{{"status":"RATE_LIMITED","message":"Too Many Requests. Rate limit exceeded.","retry_after_seconds":{retry_after}}}',
                status_code=429,
                media_type="application/json",
                headers={"Retry-After": str(retry_after)},
            )

        # 3. Process Request
        response = await call_next(request)

        # 4. Inject OWASP Security Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(self), geolocation=(self)"
        
        # CSP: Allows CDNs (Tailwind, Leaflet, html5-qrcode, Lucide) and tile servers (ESRI, OpenStreetMap)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' data: blob:; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.tailwindcss.com https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://unpkg.com; "
            "img-src 'self' data: blob: https://server.arcgisonline.com https://services.arcgisonline.com https://*.tile.openstreetmap.org; "
            "connect-src 'self' https://* http://localhost:* ws://localhost:*;"
        )

        return response


class InputSanitizer:
    """
    Sanitizes user input to prevent path traversal, HTML injection, and XSS.
    """

    TREE_ID_PATTERN = re.compile(r"^[A-Za-z0-9\-_]{1,32}$")

    @classmethod
    def sanitize_tree_id(cls, tree_id: str) -> str:
        """
        Validates tree ID strictly against alphanumeric format.
        Prevents path traversal and shell injection.
        """
        cleaned = tree_id.strip()
        if not cls.TREE_ID_PATTERN.match(cleaned):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid Tree ID format: '{tree_id}'. Must be 1-32 alphanumeric characters with '-' or '_'.",
            )
        return cleaned

    @classmethod
    def sanitize_string(cls, text: Optional[str], max_len: int = 120) -> Optional[str]:
        """Strips HTML tags, controls characters, and limits string length."""
        if not text:
            return None
        # Escape HTML entities
        escaped = html.escape(text.strip())
        # Remove any null bytes or non-printable chars
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", escaped)
        return cleaned[:max_len]


class FileValidator:
    """
    Validates uploaded payloads for size limits, MIME type verification,
    magic byte signature verification, and decompression bomb protection.
    """

    MAX_AERIAL_IMAGE_BYTES = 25 * 1024 * 1024  # 25 Megabytes
    MAX_QR_IMAGE_BYTES = 10 * 1024 * 1024       # 10 Megabytes

    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}

    # Known magic signatures
    MAGIC_SIGNATURES: Dict[str, List[bytes]] = {
        "jpeg": [b"\xff\xd8\xff"],
        "png": [b"\x89PNG\r\n\x1a\n"],
        "tiff": [b"II*\x00", b"MM\x00*"],
    }

    @classmethod
    def validate_file_payload(
        cls,
        filename: str,
        content: bytes,
        is_aerial: bool = False,
    ) -> None:
        """
        Deep security verification of incoming uploaded binary files.

        Raises:
            HTTPException with 400, 413, or 415 error codes if invalid.
        """
        max_bytes = cls.MAX_AERIAL_IMAGE_BYTES if is_aerial else cls.MAX_QR_IMAGE_BYTES

        # 1. Size Verification
        if len(content) > max_bytes:
            max_mb = max_bytes // (1024 * 1024)
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum allowed payload size of {max_mb} MB.",
            )

        if len(content) < 16:
            raise HTTPException(status_code=400, detail="Corrupted or empty file payload.")

        # 2. Extension Verification
        from pathlib import Path
        ext = Path(filename).suffix.lower()
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file format '{ext}'. Allowed formats: JPG, PNG, TIFF.",
            )

        # 3. Magic Byte Verification (prevent renaming .exe or .sh to .jpg)
        is_valid_magic = False
        for fmt, sigs in cls.MAGIC_SIGNATURES.items():
            for sig in sigs:
                if content.startswith(sig):
                    is_valid_magic = True
                    break
            if is_valid_magic:
                break

        if not is_valid_magic:
            logger.warning("[SECURITY] Magic byte validation failed for file '%s'", filename)
            raise HTTPException(
                status_code=400,
                detail="Security validation failed: File binary header does not match expected image magic signature.",
            )
