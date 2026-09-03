import pytest
from unittest.mock import Mock, patch

from gemini_client import GeminiClient
from exceptions import GeminiAPIError


def create_mock_interaction(text):
    interaction = Mock()
    interaction.output_text = text
    return interaction


@patch("gemini_client.genai.Client")
def test_gemini_client_initializes(mock_client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")

    client = GeminiClient()

    assert client.client is mock_client.return_value
    mock_client.assert_called_once_with(
        api_key="test-api-key"
    )


@patch("gemini_client.genai.Client")
def test_generate_preview(mock_client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")

    mock_client.return_value.interactions.create.return_value = (
        create_mock_interaction(
            "Arsenal vs Chelsea should be an interesting fixture."
        )
    )

    client = GeminiClient()

    result = client.generate_preview(
        home_team="Arsenal",
        away_team="Chelsea",
        home_form="W W D W L",
        away_form="W D L W W",
        fixture_date="2026-09-01",
        venue="Emirates Stadium"
    )

    assert result == (
        "Arsenal vs Chelsea should be an interesting fixture."
    )

    mock_client.return_value.interactions.create.assert_called_once()

    prompt = (
        mock_client.return_value.interactions.create
        .call_args.kwargs["input"]
    )

    assert "Arsenal" in prompt
    assert "Chelsea" in prompt
    assert "W W D W L" in prompt
    assert "W D L W W" in prompt
    assert "2026-09-01" in prompt
    assert "Emirates Stadium" in prompt


@patch("gemini_client.genai.Client")
def test_generate_summary(mock_client, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")

    mock_client.return_value.interactions.create.return_value = (
        create_mock_interaction(
            "Arsenal won the match 2-1."
        )
    )

    client = GeminiClient()

    result = client.generate_summary(
        home_team="Arsenal",
        away_team="Chelsea",
        score="2-1",
        fixture_date="2026-08-20",
        venue="Emirates Stadium"
    )

    assert result == "Arsenal won the match 2-1."

    mock_client.return_value.interactions.create.assert_called_once()

    prompt = (
        mock_client.return_value.interactions.create
        .call_args.kwargs["input"]
    )

    assert "Arsenal" in prompt
    assert "Chelsea" in prompt
    assert "2-1" in prompt
    assert "2026-08-20" in prompt
    assert "Emirates Stadium" in prompt


@patch("gemini_client.genai.Client")
def test_gemini_empty_response_raises_error(
    mock_client,
    monkeypatch
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")

    mock_client.return_value.interactions.create.return_value = (
        create_mock_interaction("")
    )

    client = GeminiClient()

    with pytest.raises(GeminiAPIError):
        client.generate_preview(
            home_team="Arsenal",
            away_team="Chelsea",
            home_form="W W D W L",
            away_form="W D L W W"
        )


@patch("gemini_client.genai.Client")
def test_gemini_request_failure_raises_error(
    mock_client,
    monkeypatch
):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key")

    mock_client.return_value.interactions.create.side_effect = (
        Exception("API connection failed")
    )

    client = GeminiClient()

    with pytest.raises(
        GeminiAPIError,
        match="Gemini request failed"
    ):
        client.generate_preview(
            home_team="Arsenal",
            away_team="Chelsea",
            home_form="W W D W L",
            away_form="W D L W W"
        )


@patch("gemini_client.load_dotenv")
def test_missing_gemini_api_key_raises_error(
    mock_load_dotenv,
    monkeypatch
):
    monkeypatch.delenv(
        "GEMINI_API_KEY",
        raising=False
    )

    with pytest.raises(
        GeminiAPIError,
        match="GEMINI_API_KEY was not found"
    ):
        GeminiClient()
