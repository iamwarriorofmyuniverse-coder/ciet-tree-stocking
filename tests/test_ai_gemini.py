"""
Automated Unit and Integration Tests for Google Gemini Multimodal AI Engine.
"""

from __future__ import annotations

import io
from PIL import Image
from starlette.testclient import TestClient
from server import app
from src.ai.gemini_engine import (
    diagnose_tree_with_gemini,
    identify_plant_with_gemini,
    chat_with_campus_arborist,
)

client = TestClient(app)


def _generate_test_image_bytes() -> bytes:
    img = Image.new("RGB", (100, 100), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_diagnose_tree_engine():
    img_bytes = _generate_test_image_bytes()
    res = diagnose_tree_with_gemini(img_bytes, mime_type="image/jpeg", tree_context="CIET-TREE-001 Neem")
    assert res.health_score_out_of_100 > 0
    assert res.condition_rating in ["Healthy", "Minor Stress", "Diseased", "Critical"]
    assert len(res.remedial_prescription) > 0


def test_identify_plant_engine():
    img_bytes = _generate_test_image_bytes()
    res = identify_plant_with_gemini(img_bytes, mime_type="image/jpeg")
    assert len(res.common_name) > 0
    assert len(res.scientific_name) > 0
    assert len(res.family) > 0


def test_chat_campus_arborist():
    reply_carbon = chat_with_campus_arborist("Which tree has the most carbon?", "Campus context")
    assert "carbon" in reply_carbon.lower() or "ciet" in reply_carbon.lower()

    reply_medicinal = chat_with_campus_arborist("Tell me about medicinal trees", "Campus context")
    assert "medicinal" in reply_medicinal.lower() or "neem" in reply_medicinal.lower()


def test_api_ai_diagnose_endpoint():
    img_bytes = _generate_test_image_bytes()
    files = {"image": ("test_leaf.jpg", img_bytes, "image/jpeg")}
    data = {"tree_context": "Neem tree with yellowing leaves"}
    resp = client.post("/api/ai/diagnose", files=files, data=data)
    assert resp.status_code == 200
    res = resp.json()
    assert "health_score_out_of_100" in res
    assert "remedial_prescription" in res


def test_api_ai_identify_endpoint():
    img_bytes = _generate_test_image_bytes()
    files = {"image": ("test_sample.jpg", img_bytes, "image/jpeg")}
    resp = client.post("/api/ai/identify", files=files)
    assert resp.status_code == 200
    res = resp.json()
    assert "scientific_name" in res
    assert "common_name" in res


def test_api_ai_chat_endpoint():
    payload = {"message": "What is the total carbon sequestered at CIET?"}
    resp = client.post("/api/ai/chat", json=payload)
    assert resp.status_code == 200
    res = resp.json()
    assert "reply" in res
    assert len(res["reply"]) > 10
