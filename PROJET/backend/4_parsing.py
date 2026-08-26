"""
[Repartition equipe] Personne 4 - Extraction des reponses Gemini.

Convertit le texte brut renvoye par Gemini (parfois une liste de chunks, ou
entoure de balises markdown) en donnees exploitables : dict JSON ou code SVG.
"""

import json
import re


def _raw_to_text(raw_text) -> str:
    """Normalise une reponse Gemini (str, ou liste de chunks str/dict) en une
    seule chaine de caracteres."""
    if isinstance(raw_text, list):
        parts = []
        for chunk in raw_text:
            if isinstance(chunk, str):
                parts.append(chunk)
            elif isinstance(chunk, dict) and "text" in chunk:
                parts.append(chunk["text"])
        return "".join(parts).strip()
    return str(raw_text).strip()


def extract_json(raw_text) -> dict:
    """Extrait et parse le JSON de la reponse de Gemini."""
    text = _raw_to_text(raw_text)

    # Retire une eventuelle cloture markdown ```json ... ```
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Dernier recours : isoler le premier objet JSON complet du texte
        brace_match = re.search(r"\{.*\}", text, re.DOTALL)
        if not brace_match:
            raise ValueError(f"Reponse Gemini non parsable en JSON : {raw_text!r}")
        return json.loads(brace_match.group(0))


def extract_svg(raw_text) -> str:
    """Extrait le code SVG brut de la reponse de Gemini."""
    text = _raw_to_text(raw_text)

    fence_match = re.search(r"```(?:svg|xml)?\s*(<svg.*</svg>)\s*```", text, re.DOTALL | re.IGNORECASE)
    if fence_match:
        return fence_match.group(1).strip()

    svg_match = re.search(r"<svg.*</svg>", text, re.DOTALL | re.IGNORECASE)
    if not svg_match:
        raise ValueError(f"Reponse Gemini sans balise <svg>...</svg> exploitable : {raw_text!r}")
    return svg_match.group(0).strip()
