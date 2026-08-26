"""Mapping concept → formes sémantiques — tâche 3.4.

Dictionnaire statique qui associe des mots-clés à des descriptions
de composition (liste de formes + positions + rôles color).
Mode statique par défaut, fallback LLM optionnel avec --llm.
"""

from typing import Optional

# Chaque entrée : liste de dicts avec :
#   shape  : nom de fonction dans shapes.py
#   role   : "primary" | "accent" | "stroke" | "white"
#   kwargs : paramètres optionnels (cx, cy, size, etc.)

CONCEPT_MAP: dict[str, list[dict]] = {
    # ── IT / Infra ──
    "cloud": [
        {"shape": "cloud_shape", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 24}},
        {"shape": "arrow_up", "role": "accent", "kwargs": {"cx": 32, "cy": 38, "size": 12}},
    ],
    "security": [
        {"shape": "shield", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 24}},
        {"shape": "lock", "role": "accent", "kwargs": {"cx": 32, "cy": 37, "w": 18, "h": 12}},
    ],
    "database": [
        {"shape": "database_icon", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "collaboration": [
        {"shape": "users", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 20}},
        {"shape": "code_brackets", "role": "accent", "kwargs": {"cx": 32, "cy": 42, "size": 10}},
    ],
    "deployment": [
        {"shape": "rocket", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 20}},
        {"shape": "arrow_up", "role": "accent", "kwargs": {"cx": 32, "cy": 46, "size": 10}},
    ],

    # ── Musique / Art ──
    "musique": [
        {"shape": "note_music", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 20}},
        {"shape": "bell", "role": "accent", "kwargs": {"cx": 32, "cy": 44, "size": 8}},
    ],
    "art": [
        {"shape": "pen", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
        {"shape": "star", "role": "accent", "kwargs": {"cx": 44, "cy": 18, "size": 8}},
    ],
    "creation": [
        {"shape": "pen", "role": "primary", "kwargs": {"cx": 30, "cy": 32, "size": 20}},
        {"shape": "star", "role": "accent", "kwargs": {"cx": 42, "cy": 20, "size": 10}},
    ],

    # ── Cuisine ──
    "cuisine": [
        {"shape": "bell", "role": "primary", "kwargs": {"cx": 32, "cy": 24, "size": 16}},
        {"shape": "heart", "role": "accent", "kwargs": {"cx": 32, "cy": 42, "size": 10}},
    ],
    "nourriture": [
        {"shape": "heart", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 16}},
        {"shape": "star", "role": "accent", "kwargs": {"cx": 32, "cy": 46, "size": 8}},
    ],

    # ── Transport ──
    "transport": [
        {"shape": "rocket", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 18}},
        {"shape": "arrow_up", "role": "accent", "kwargs": {"cx": 32, "cy": 48, "size": 8}},
    ],
    "voiture": [
        {"shape": "rocket", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 18}},
    ],

    # ── Analytics / Data ──
    "analytics": [
        {"shape": "bar_chart", "role": "primary", "kwargs": {"cx": 32, "cy": 34, "size": 24}},
        {"shape": "magnifier", "role": "accent", "kwargs": {"cx": 44, "cy": 16, "size": 8}},
    ],
    "tendance": [
        {"shape": "bar_chart", "role": "primary", "kwargs": {"cx": 32, "cy": 34, "size": 24}},
    ],
    "metrique": [
        {"shape": "bar_chart", "role": "primary", "kwargs": {"cx": 32, "cy": 34, "size": 24}},
    ],
    "statistiques": [
        {"shape": "bar_chart", "role": "primary", "kwargs": {"cx": 32, "cy": 34, "size": 24}},
    ],

    # ── Recherche ──
    "recherche": [
        {"shape": "magnifier", "role": "primary", "kwargs": {"cx": 28, "cy": 28, "size": 16}},
    ],
    "exploration": [
        {"shape": "magnifier", "role": "primary", "kwargs": {"cx": 28, "cy": 28, "size": 16}},
        {"shape": "star", "role": "accent", "kwargs": {"cx": 44, "cy": 44, "size": 8}},
    ],

    # ── Code / Dev ──
    "code": [
        {"shape": "code_brackets", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "developpement": [
        {"shape": "code_brackets", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 20}},
        {"shape": "gear", "role": "accent", "kwargs": {"cx": 32, "cy": 46, "size": 8}},
    ],
    "programmation": [
        {"shape": "code_brackets", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],

    # ── Config / Settings ──
    "configuration": [
        {"shape": "gear", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "settings": [
        {"shape": "gear", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "parametre": [
        {"shape": "gear", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],

    # ── Performance / Speed ──
    "performance": [
        {"shape": "lightning", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 24}},
    ],
    "vitesse": [
        {"shape": "lightning", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 24}},
    ],
    "rapide": [
        {"shape": "lightning", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 24}},
    ],
    "energie": [
        {"shape": "lightning", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 24}},
    ],

    # ── Notifications / Alertes ──
    "notification": [
        {"shape": "bell", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 18}},
    ],
    "alerte": [
        {"shape": "bell", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 18}},
    ],
    "messagerie": [
        {"shape": "bell", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 18}},
    ],

    # ── Localisation ──
    "localisation": [
        {"shape": "map_pin", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 22}},
    ],
    "carte": [
        {"shape": "map_pin", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 22}},
    ],
    "geolocalisation": [
        {"shape": "map_pin", "role": "primary", "kwargs": {"cx": 32, "cy": 30, "size": 22}},
    ],

    # ── Temps / Planning ──
    "calendrier": [
        {"shape": "calendar", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "planification": [
        {"shape": "calendar", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "historique": [
        {"shape": "refresh", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "r": 16}},
    ],

    # ── Favoris / Amour ──
    "favoris": [
        {"shape": "heart", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 18}},
    ],
    "like": [
        {"shape": "heart", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 18}},
    ],
    "qualite": [
        {"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "excellence": [
        {"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "premium": [
        {"shape": "star", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],

    # ── Réseau / Globe ──
    "reseau": [
        {"shape": "globe", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "r": 20}},
    ],
    "international": [
        {"shape": "globe", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "r": 20}},
    ],
    "monde": [
        {"shape": "globe", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "r": 20}},
    ],
    "web": [
        {"shape": "globe", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "r": 20}},
    ],

    # ── Maintenance / Outils ──
    "maintenance": [
        {"shape": "wrench", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "outil": [
        {"shape": "wrench", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "reparation": [
        {"shape": "wrench", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],

    # ── Vision / Surveillance ──
    "vision": [
        {"shape": "eye", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "surveillance": [
        {"shape": "eye", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],
    "monitoring": [
        {"shape": "eye", "role": "primary", "kwargs": {"cx": 32, "cy": 32, "size": 22}},
    ],

    # ── Équipe / Personnel ──
    "equipe": [
        {"shape": "users", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 22}},
    ],
    "personnel": [
        {"shape": "users", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 22}},
    ],
    "communaute": [
        {"shape": "users", "role": "primary", "kwargs": {"cx": 32, "cy": 28, "size": 22}},
    ],
}


def lookup_concept(
    concept: str,
    use_llm: bool = False,
    brand_style: Optional[dict] = None,
    context: str = "",
) -> Optional[list[dict]]:
    """Cherche un concept dans la map (insensible à la casse, sans accents simples).

    Si use_llm=True et que le concept n'est pas trouvé dans la map statique,
    appelle Gemini API pour générer un layout dynamique.
    """
    key = concept.lower().strip()
    if key in CONCEPT_MAP:
        return CONCEPT_MAP[key]
    # tentative sans accents courants
    import unicodedata
    normalized = unicodedata.normalize("NFD", key)
    ascii_key = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    if ascii_key in CONCEPT_MAP:
        return CONCEPT_MAP[ascii_key]

    # Fallback LLM si activé
    if use_llm:
        from src.llm_client import generate_layout_llm
        layout = generate_layout_llm(concept, brand_style or {}, context)
        if layout:
            return layout

    return None
