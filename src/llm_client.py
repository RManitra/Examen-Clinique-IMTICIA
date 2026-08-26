"""Client LLM pour la génération de layouts d'icônes via Gemini API.

Envoie le concept + charte graphique + formes disponibles à Gemini,
reçoit un JSON structuré que le composer existant se charge de renderer.
Fallback automatique si l'API est indisponible ou si la clé manque.
"""

import json
import os
import re
import warnings
from typing import Optional


AVAILABLE_SHAPES = [
    "shield", "lock", "note_music", "cloud_shape", "arrow_up",
    "gear", "star", "heart", "magnifier", "bar_chart",
    "code_brackets", "lightning", "bell", "pen", "map_pin",
    "calendar", "refresh", "globe", "rocket", "eye",
    "users", "wrench", "database_icon",
]

SYSTEM_PROMPT = """\
Tu es un générateur de layouts d'icônes SVG vectorielles.
Tu reçois un concept en langage naturel et une charte graphique.

Tu dois retourner UNIQUEMENT un objet JSON valide (pas de markdown, pas d'explication, pas de commentaire).

Le JSON contient une liste de 1 à 3 formes à dessiner :
[
  {{
    "shape": "nom_de_forme",
    "role": "primary|accent|secondary|stroke|white",
    "kwargs": {{"cx": 32, "cy": 32, "size": 20}}
  }}
]

Formes disponibles : {shapes}

Règles strictes :
- viewBox toujours 64x64
- Zone utile : x=5..59, y=5..59 (toute emprise visuelle doit rester dans cette zone)
- Maximum 3 formes par icône
- Maximum 4 couleurs visibles
- Les coords cx, cy doivent être centrées autour de 32,32
- size typique : 16..24 pour une forme principale, 8..12 pour un accent
- rôle "primary" = couleur dominante (jaune)
- rôle "accent" = couleur d'accent (orange)
- rôle "stroke" = contour sombre
- rôle "white" = blanc

Exemple pour le concept "musique jazz" :
[
  {{"shape": "note_music", "role": "primary", "kwargs": {{"cx": 32, "cy": 28, "size": 20}}}},
  {{"shape": "bell", "role": "accent", "kwargs": {{"cx": 32, "cy": 44, "size": 8}}}}
]

Retourne UNIQUEMENT le JSON, rien d'autre.
""".format(shapes=", ".join(AVAILABLE_SHAPES))


def _get_api_key() -> Optional[str]:
    """Récupère la clé API Gemini depuis les variables d'environnement."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    return key if key else None


def _parse_llm_response(text: str) -> Optional[list[dict]]:
    """Parse la réponse du LLM en liste de layouts valides."""
    cleaned = text.strip()

    # Retirer les fences markdown si présents
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()

    # Extraire le JSON si entouré de texte
    match = re.search(r'\[[\s\S]*\]', cleaned)
    if match:
        cleaned = match.group(0)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    if not isinstance(data, list) or len(data) == 0:
        return None

    # Valider chaque entrée
    valid_shapes = set(AVAILABLE_SHAPES)
    valid_roles = {"primary", "accent", "secondary", "stroke", "white"}
    result = []
    for item in data:
        if not isinstance(item, dict):
            continue
        shape = item.get("shape", "")
        role = item.get("role", "primary")
        kwargs = item.get("kwargs", {})
        if shape not in valid_shapes or role not in valid_roles:
            continue
        if not isinstance(kwargs, dict):
            continue
        result.append({"shape": shape, "role": role, "kwargs": kwargs})

    return result if result else None


def generate_layout_llm(
    concept: str,
    brand_style: dict,
    context: str = "",
) -> Optional[list[dict]]:
    """Appelle Gemini pour générer un layout à partir d'un concept.

    Args:
        concept: le concept en langage naturel
        brand_style: dict de la charte (couleurs, viewBox, etc.)
        context: contexte optionnel

    Returns:
        Liste de dicts {shape, role, kwargs} ou None si échec
    """
    api_key = _get_api_key()
    if not api_key:
        warnings.warn(
            "[LLM] GEMINI_API_KEY non défini — fallback mode statique.",
            stacklevel=2,
        )
        return None

    try:
        from google import genai
    except ImportError:
        warnings.warn(
            "[LLM] google-genai non installé — pip install google-genai",
            stacklevel=2,
        )
        return None

    # Construire le contexte charte pour le prompt
    charte_ctx = {
        "viewBox": brand_style.get("view_box", "0 0 64 64"),
        "couleurs_autorisees": brand_style.get("allowed_colors", []),
        "couleur_principale": brand_style.get("required_colors", ["#FFD21E"])[0]
        if brand_style.get("required_colors") else "#FFD21E",
        "couleur_accent": brand_style.get("accent_colors", ["#FF9D00"])[0]
        if brand_style.get("accent_colors") else "#FF9D00",
        "stroke_width": brand_style.get("stroke_width", 2.5),
        "zone_utile": "x=5..59, y=5..59",
    }

    user_msg = (
        f'{SYSTEM_PROMPT}\n\n'
        f'concept="{concept}"\n'
        f'contexte="{context}"\n'
        f'charte={json.dumps(charte_ctx, ensure_ascii=False)}'
    )

    try:
        client = genai.Client(api_key=api_key)
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=user_msg,
        )
        text = interaction.output_text
        if not text:
            return None
        return _parse_llm_response(text)

    except Exception as e:
        warnings.warn(
            f"[LLM] Erreur API Gemini: {e} — fallback mode statique.",
            stacklevel=2,
        )
        return None
