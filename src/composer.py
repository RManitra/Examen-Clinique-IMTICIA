"""Système de composition SVG — tâches 3.3, 3.5.

Prend une description DSL (liste de formes + rôles) et génère
un SVG conforme à la charte graphique (couleurs, contraintes).
"""

import importlib
from typing import Optional

import src.shapes as shapes_mod
from src.concept_map import lookup_concept

SHAPE_NS = "shape"
COLOR_MAP = {
    "primary": None,   # résolu par le caller
    "accent": None,
    "stroke": None,
    "white": "#FFFFFF",
}


def _get_shape_func(name: str):
    """Récupère la fonction de forme depuis shapes.py."""
    return getattr(shapes_mod, name, None)


def compose_icon(
    layout: list[dict],
    primary: str = "#FFD21E",
    accent: str = "#FF9D00",
    stroke_color: str = "#111827",
    stroke_width: float = 2.5,
) -> str:
    """Convertit une DSL de composition en fragment SVG (contenu du <g>).

    Args:
        layout: liste de dicts {shape, role, kwargs}
        primary, accent, stroke_color, white: couleurs résolues par le generator
        stroke_width: épaisseur des traits

    Returns:
        chaîne SVG (lignes à insérer dans le <g> du generator)
    """
    role_colors = {
        "primary": primary,
        "accent": accent,
        "stroke": stroke_color,
        "white": COLOR_MAP["white"],
    }

    elements = []
    for item in layout:
        func_name = item["shape"]
        role = item.get("role", "primary")
        kwargs = dict(item.get("kwargs", {}))

        func = _get_shape_func(func_name)
        if func is None:
            continue

        fill = role_colors.get(role, primary)
        # Remplacer la couleur dans kwargs si la forme l'accepte
        if "fill" in func.__code__.co_varnames:
            kwargs.setdefault("fill", fill)
        elif role == "stroke":
            kwargs.setdefault("stroke", stroke_color)
            kwargs.setdefault("fill", "none")

        # Normaliser size→r si la forme utilise r (star, globe, gear, magnifier, refresh)
        params = func.__code__.co_varnames[:func.__code__.co_argcount]
        if "r" in params and "size" not in params and "size" in kwargs:
            kwargs["r"] = kwargs.pop("size")

        try:
            svg_fragment = func(**kwargs)
        except TypeError:
            continue

        elements.append(svg_fragment)

    return "\n    ".join(elements)


def resolve_concept(
    concept: str,
    use_llm: bool = False,
    brand_style: Optional[dict] = None,
    context: str = "",
) -> Optional[list[dict]]:
    """Résout un concept en layout DSL via concept_map, avec fallback LLM optionnel."""
    return lookup_concept(concept, use_llm=use_llm, brand_style=brand_style, context=context)
