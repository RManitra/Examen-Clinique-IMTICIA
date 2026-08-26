# tests/test_composer.py
import pytest
from src.shapes import circle, rect, shield, note_music, gear, star, heart, bar_chart, code_brackets, lightning
from src.concept_map import lookup_concept, CONCEPT_MAP
from src.composer import compose_icon, resolve_concept


def test_all_shapes_return_svg():
    """Chaque fonction de forme retourne une chaîne SVG valide."""
    shapes_with_args = [
        (circle, {"cx": 32, "cy": 32, "r": 10}),
        (rect, {"x": 10, "y": 10, "w": 20, "h": 20}),
        (shield, {}),
        (note_music, {}),
        (gear, {}),
        (star, {}),
        (heart, {}),
        (bar_chart, {}),
        (code_brackets, {}),
        (lightning, {}),
    ]
    for f, default_kwargs in shapes_with_args:
        result = f(**default_kwargs)
        assert isinstance(result, str)
        assert "<" in result


def test_concept_map_keys_are_strings():
    """Toutes les clés du concept map sont des strings."""
    for key in CONCEPT_MAP:
        assert isinstance(key, str)


def test_lookup_concept_known():
    """Un concept connu est trouvé."""
    result = lookup_concept("musique")
    assert result is not None
    assert len(result) > 0
    assert result[0]["shape"] == "note_music"


def test_lookup_concept_case_insensitive():
    """La recherche est insensible à la casse."""
    assert lookup_concept("MUSIQUE") is not None
    assert lookup_concept("Musique") is not None


def test_lookup_concept_unknown():
    """Un concept inconnu retourne None."""
    assert lookup_concept("xylophone_inexistant_xyz") is None


def test_resolve_concept_delegates():
    """resolve_concept délègue à lookup_concept."""
    assert resolve_concept("cloud") is not None
    assert resolve_concept("unknown_xyz") is None


def test_compose_icon_produces_svg():
    """compose_icon retourne un fragment SVG."""
    layout = [{"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "r": 20}}]
    svg = compose_icon(layout, primary="#FFD21E", accent="#FF9D00", stroke_color="#111827")
    assert "path" in svg
    assert "FFD21E" in svg


def test_compose_icon_roles_colors():
    """Les rôles accent utilisent la couleur accent."""
    layout = [
        {"shape": "shield", "role": "primary"},
        {"shape": "heart", "role": "accent"},
    ]
    svg = compose_icon(layout, primary="#FFD21E", accent="#FF9D00")
    assert "#FFD21E" in svg
    assert "#FF9D00" in svg


def test_compose_icon_skips_unknown_shape():
    """Une forme inconnue est ignorée silencieusement."""
    layout = [{"shape": "shape_inexistante_xyz", "role": "primary"}]
    svg = compose_icon(layout)
    assert svg == ""  # rien produit


def test_compose_icon_multiple_shapes():
    """Plusieurs formes sont assemblées."""
    layout = [
        {"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 20, "r": 12}},
        {"shape": "heart", "role": "accent", "kwargs": {"cx": 32, "cy": 44, "size": 8}},
    ]
    svg = compose_icon(layout, primary="#FFD21E", accent="#FF9D00")
    assert "path" in svg
    # Les deux formes sont présentes
    assert svg.count("<path") >= 2
