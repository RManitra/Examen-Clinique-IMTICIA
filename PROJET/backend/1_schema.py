"""
[Repartition equipe] Personne 1 - Schema & contrat JSON.

Definit le JSON Schema du challenge IconForge (contrat de l'etape 1) ainsi
que sa variante utilisable par le mode "structured output" de Gemini.
"""

# ---------------------------------------------------------------------------
# Schema cible (fourni par la specification du challenge)
# ---------------------------------------------------------------------------
ICONFORGE_REQUEST_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://example.org/iconforge/request.schema.json",
    "title": "IconForge generation request collection",
    "type": "object",
    "required": ["collection_id", "requests"],
    "properties": {
        "$schema": {"type": "string"},
        "collection_id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
        "requests": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "concept"],
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z0-9][a-z0-9-]*$"},
                    "concept": {"type": "string", "minLength": 1},
                    "context": {"type": "string"},
                    "keywords": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                        "uniqueItems": True,
                    },
                },
            },
        },
    },
    "additionalProperties": False,
}

# ---------------------------------------------------------------------------
# Version du schema utilisable par le mode "structured output" de Gemini
# (response_schema). L'API n'accepte pas les meta-cles JSON Schema pures
# ($schema, $id, title) : on les retire, la structure/contraintes restent.
# ---------------------------------------------------------------------------
GEMINI_RESPONSE_SCHEMA = {
    key: value
    for key, value in ICONFORGE_REQUEST_SCHEMA.items()
    if key not in ("$schema", "$id", "title")
}
