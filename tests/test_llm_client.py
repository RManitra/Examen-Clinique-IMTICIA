"""Tests pour le client LLM Gemini (src/llm_client.py)."""

import json
import os
import pytest
from unittest.mock import patch, MagicMock

from src.llm_client import _parse_llm_response, generate_layout_llm, AVAILABLE_SHAPES


class TestParseLLMResponse:
    """Tests du parsing des réponses LLM."""

    def test_parse_valid_json(self):
        layout = _parse_llm_response('[{"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 32}}]')
        assert layout is not None
        assert len(layout) == 1
        assert layout[0]["shape"] == "star"
        assert layout[0]["role"] == "primary"

    def test_parse_json_with_markdown_fences(self):
        response = '```json\n[{"shape": "heart", "role": "accent", "kwargs": {"cx": 32, "size": 12}}]\n```'
        layout = _parse_llm_response(response)
        assert layout is not None
        assert layout[0]["shape"] == "heart"

    def test_parse_json_embedded_in_text(self):
        response = 'Voici le layout : [{"shape": "gear", "role": "primary", "kwargs": {}}] J\'espère que ça aide.'
        layout = _parse_llm_response(response)
        assert layout is not None
        assert layout[0]["shape"] == "gear"

    def test_parse_multiple_shapes(self):
        response = json.dumps([
            {"shape": "shield", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 24}},
            {"shape": "lock", "role": "accent", "kwargs": {"cx": 32, "cy": 37, "w": 18, "h": 12}},
        ])
        layout = _parse_llm_response(response)
        assert layout is not None
        assert len(layout) == 2

    def test_parse_invalid_json(self):
        assert _parse_llm_response("ce n'est pas du JSON") is None

    def test_parse_empty_list(self):
        assert _parse_llm_response("[]") is None

    def test_parse_invalid_shape(self):
        response = '[{"shape": "unicorn", "role": "primary", "kwargs": {}}]'
        assert _parse_llm_response(response) is None

    def test_parse_invalid_role(self):
        response = '[{"shape": "star", "role": "rainbow", "kwargs": {}}]'
        assert _parse_llm_response(response) is None

    def test_parse_missing_shape_key(self):
        response = '[{"role": "primary", "kwargs": {}}]'
        assert _parse_llm_response(response) is None


class TestGenerateLayoutLLM:
    """Tests de l'appel LLM (mocké)."""

    def test_no_api_key_returns_none(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": ""}, clear=False):
            result = generate_layout_llm("test", {})
            assert result is None

    def test_import_error_returns_none(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"}):
            with patch.dict("sys.modules", {"google": None}):
                result = generate_layout_llm("test", {})
                assert result is None

    def test_api_error_returns_none(self):
        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"}):
            mock_genai = MagicMock()
            mock_genai.Client.side_effect = Exception("API Error")
            with patch.dict("sys.modules", {"google": MagicMock(genai=mock_genai)}):
                result = generate_layout_llm("test", {})
                assert result is None

    def test_valid_api_response(self):
        mock_interaction = MagicMock()
        mock_interaction.output_text = json.dumps([
            {"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 20}},
        ])
        mock_client = MagicMock()
        mock_client.interactions.create.return_value = mock_interaction

        with patch.dict(os.environ, {"GEMINI_API_KEY": "fake-key"}):
            mock_genai = MagicMock()
            mock_genai.Client.return_value = mock_client
            with patch.dict("sys.modules", {"google": MagicMock(genai=mock_genai)}):
                result = generate_layout_llm(
                    "étoile",
                    {"view_box": "0 0 64 64", "allowed_colors": ["#FFD21E"]},
                )
                assert result is not None
                assert result[0]["shape"] == "star"


class TestAvailableShapes:
    """Vérifie que toutes les formes dans AVAILABLE_SHAPES existent dans shapes.py."""

    def test_all_shapes_exist(self):
        import src.shapes as shapes_mod
        for shape_name in AVAILABLE_SHAPES:
            assert hasattr(shapes_mod, shape_name), f"Forme '{shape_name}' manquante dans shapes.py"
