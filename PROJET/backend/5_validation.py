"""
[Repartition equipe] Personne 5 - Validation / conformite.

Verifie que les reponses de Gemini respectent le contrat attendu : le JSON
Schema du challenge pour l'etape 1, les contraintes deterministes de la
charte de marque (section 9) pour le SVG de l'etape 2.
"""

import re

from _loader import load

schema = load("1_schema.py")

ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")

FORBIDDEN_SVG_TAGS = ("script", "image", "text", "lineargradient", "radialgradient", "filter", "mask", "pattern")


def validate_against_schema(data: dict) -> None:
    """Valide la structure retournee par rapport au schema IconForge.

    Utilise `jsonschema` si disponible ; sinon effectue des controles minimaux
    equivalents aux contraintes essentielles du schema.
    """
    try:
        import jsonschema

        jsonschema.validate(instance=data, schema=schema.ICONFORGE_REQUEST_SCHEMA)
        return
    except ImportError:
        pass

    if not isinstance(data, dict):
        raise ValueError("La reponse doit etre un objet JSON.")
    if "collection_id" not in data or "requests" not in data:
        raise ValueError("Champs requis manquants : 'collection_id' et/ou 'requests'.")
    if not ID_PATTERN.match(data["collection_id"]):
        raise ValueError("'collection_id' ne respecte pas le pattern attendu.")
    if not isinstance(data["requests"], list) or len(data["requests"]) < 1:
        raise ValueError("'requests' doit etre un tableau non vide.")

    allowed_keys = {"id", "concept", "context", "keywords"}
    for req in data["requests"]:
        if not isinstance(req, dict):
            raise ValueError("Chaque element de 'requests' doit etre un objet.")
        if not allowed_keys.issuperset(req.keys()):
            raise ValueError(f"Proprietes additionnelles non autorisees dans : {req}")
        if "id" not in req or "concept" not in req:
            raise ValueError(f"'id' et 'concept' sont requis dans : {req}")
        if not ID_PATTERN.match(req["id"]):
            raise ValueError(f"'id' invalide : {req['id']!r}")
        if not isinstance(req["concept"], str) or not req["concept"]:
            raise ValueError(f"'concept' invalide pour : {req}")


def validate_svg_against_guidelines(svg_code: str) -> None:
    """Controles deterministes minimaux issus de la section 9 de la charte
    (validite SVG, viewBox, absence d'elements interdits).

    Cette validation est un filet de securite best-effort, pas un remplacement
    du controle qualitatif humain/jury attendu par la charte.
    """
    lowered = svg_code.lower()

    if "<svg" not in lowered or "</svg>" not in lowered:
        raise ValueError("Le code retourne ne contient pas de balise <svg>...</svg> valide.")

    if not re.search(r'viewbox\s*=\s*["\']\s*0\s+0\s+64\s+64\s*["\']', svg_code, re.IGNORECASE):
        raise ValueError("L'attribut viewBox=\"0 0 64 64\" est manquant ou incorrect.")

    for tag in FORBIDDEN_SVG_TAGS:
        if f"<{tag}" in lowered:
            raise ValueError(f"Element interdit par la charte detecte : <{tag}>.")

    if re.search(r'(href|xlink:href)\s*=\s*["\']https?://', svg_code, re.IGNORECASE):
        raise ValueError("Reference externe (href http/https) interdite par la charte.")
