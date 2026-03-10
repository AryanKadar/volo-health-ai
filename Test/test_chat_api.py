"""
test_chat_api.py – pytest tests for the POST /api/chat endpoint
Run from intern/Backend/ with venv active:
    pytest ../Test/test_chat_api.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Backend'))

import pytest
from unittest.mock import patch, MagicMock

try:
    from main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False


# ── Helpers ──────────────────────────────────────────────────────────────────

def _mock_azure_response(text: str = "This is a test reply from the AI."):
    """Return a mock object that mimics the Azure OpenAI completion response."""
    mock_choice = MagicMock()
    mock_choice.message.content = text
    mock_resp = MagicMock()
    mock_resp.choices = [mock_choice]
    mock_resp.usage.prompt_tokens = 100
    mock_resp.usage.completion_tokens = 20
    mock_resp.usage.total_tokens = 120
    return mock_resp


# ── Tests ────────────────────────────────────────────────────────────────────

@pytest.mark.skipif(not BACKEND_AVAILABLE, reason="Backend main.py not found")
class TestChatEndpoint:

    def test_valid_request_returns_200(self):
        """A valid POST /api/chat returns HTTP 200 with a reply."""
        with patch(
            "services.azure_openai.call_gpt",
            return_value=("Here is the answer.", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})
        ):
            response = client.post("/api/chat", json={
                "message": "What documents are required for hospital admission?",
                "history": [],
                "summary": ""
            })
        assert response.status_code == 200

    def test_valid_request_has_reply_field(self):
        """Response JSON must contain a non-empty 'reply' string."""
        with patch("services.azure_openai.call_gpt",
                   return_value=("Documents needed: Aadhaar, insurance card.", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})):
            response = client.post("/api/chat", json={
                "message": "What documents are needed?",
                "history": [],
                "summary": ""
            })
        data = response.json()
        assert "reply" in data
        assert isinstance(data["reply"], str)
        assert len(data["reply"]) > 0

    def test_valid_request_has_on_topic_field(self):
        """Response JSON must contain 'on_topic' boolean."""
        with patch("services.azure_openai.call_gpt", return_value=("Answer here.", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})):
            response = client.post("/api/chat", json={
                "message": "What documents are needed?",
                "history": [],
                "summary": ""
            })
        data = response.json()
        assert "on_topic" in data
        assert isinstance(data["on_topic"], bool)

    def test_empty_message_returns_422(self):
        """An empty message should fail Pydantic validation → HTTP 422."""
        response = client.post("/api/chat", json={
            "message": "",
            "history": [],
            "summary": ""
        })
        assert response.status_code == 422

    def test_missing_message_field_returns_422(self):
        """Missing required 'message' field → HTTP 422."""
        response = client.post("/api/chat", json={"history": [], "summary": ""})
        assert response.status_code == 422

    def test_history_is_forwarded(self):
        """History (max 6 turns) is accepted and a coherent reply is returned."""
        history = [
            {"role": "user",      "content": "Hello"},
            {"role": "assistant", "content": "Hi! How can I help?"}
        ]
        with patch("services.azure_openai.call_gpt",
                   return_value=("During discharge you will receive a summary.", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})):
            response = client.post("/api/chat", json={
                "message": "What happens during discharge?",
                "history": history,
                "summary": "Patient greeted the assistant."
            })
        assert response.status_code == 200

    def test_off_topic_returns_on_topic_false(self):
        """Off-topic message returns on_topic=False with redirect reply."""
        # Patch topic_guard to return False (off-topic)
        with patch("services.topic_guard.is_healthcare_related", return_value=(False, {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})):
            response = client.post("/api/chat", json={
                "message": "What is 2+2?",
                "history": [],
                "summary": ""
            })
        data = response.json()
        assert response.status_code == 200
        assert data["on_topic"] is False
        assert data["new_summary"] is None

    def test_azure_error_returns_500(self):
        """When Azure OpenAI raises an exception, endpoint returns HTTP 500."""
        with patch("services.azure_openai.call_gpt",
                   side_effect=Exception("Azure quota exceeded")):
            response = client.post("/api/chat", json={
                "message": "Tell me about discharge.",
                "history": [],
                "summary": ""
            })
        assert response.status_code == 500
        assert "detail" in response.json()
