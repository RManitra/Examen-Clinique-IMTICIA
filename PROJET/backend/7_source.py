"""
Point d'entree CLI d'IconForge.

Compose les modules du dossier backend/, prefixes dans l'ordre du pipeline
pour faciliter la lecture (repartition en 6 taches) :
    1_schema.py     - contrat JSON Schema du challenge
    2_brand.py      - lecture dynamique de la charte de marque
    3_prompts.py    - construction des prompts System/Human
    4_parsing.py    - extraction JSON/SVG des reponses Gemini
    5_validation.py - conformite des reponses (schema + charte SVG)
    6_generation.py - appels Gemini et sauvegarde des fichiers .svg

Ce fichier reste le point d'import utilise par backend/8_main.py (FastAPI) :
generate_icon_requests, generate_icon_svg, save_svg_file, BRAND_GUIDELINES_PATH.
"""

import json
import sys
from pathlib import Path

# Ajoute le dossier de ce fichier a sys.path : necessaire quand ce module est
# charge dynamiquement (via importlib, cf. 8_main.py) depuis un autre
# repertoire, pour que `from _loader import load` resolve correctement.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _loader import load

brand = load("2_brand.py")
generation = load("6_generation.py")

BRAND_GUIDELINES_PATH = brand.BRAND_GUIDELINES_PATH
generate_icon_requests = generation.generate_icon_requests
generate_icon_svg = generation.generate_icon_svg
save_svg_file = generation.save_svg_file

if __name__ == "__main__":
    query = input("Decrivez le besoin d'icone(s) a generer : ")

    result = generate_icon_requests(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    for req in result["requests"]:
        try:
            svg_code = generate_icon_svg(req)
        except ValueError as exc:
            print(f"\n[{req['id']}] echec de validation SVG : {exc}")
            continue

        svg_path = save_svg_file(req["id"], svg_code)
        print(f"\n[{req['id']}] SVG genere -> {svg_path}")
        print(svg_code)
