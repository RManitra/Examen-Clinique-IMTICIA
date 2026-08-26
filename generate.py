#!/usr/bin/env python3
"""Script principal d'orchestration pour la génération d'icônes IconForge AI."""

import argparse
import json
import sys
from pathlib import Path

from src.parser import BrandParser
from src.validator_bridge import ValidatorBridge
from src.reflector import ReflectorPipeline

def main():
    parser = argparse.ArgumentParser(description="IconForge AI - Générateur de famille d'icônes SVG")
    parser.add_argument("--input", type=Path, required=True, help="Fichier JSON des requêtes de concepts")
    parser.add_argument("--output", type=Path, required=True, help="Dossier de destination des SVG")
    parser.add_argument("--guidelines", type=Path, default=Path("brand-guidelines.md"), help="Fichier de charte graphique")
    parser.add_argument("--references", type=Path, default=Path("references"), help="Dossier des SVG de référence")
    parser.add_argument("--llm", action="store_true", default=False,
                        help="Activer le fallback LLM (Gemini) pour les concepts inconnus")
    args = parser.parse_args()

    # 1. Analyse dynamique de la charte graphique et des références
    brand_parser = BrandParser(args.guidelines, args.references)
    analysis = brand_parser.analyze()
    brand_style = analysis["guidelines"]

    print(f"[IconForge AI] Charte analysée: {len(brand_style['allowed_colors'])} couleurs autorisées.")

    # 2. Chargement des requêtes
    if not args.input.exists():
        print(f"Erreur: Le fichier de requêtes {args.input} n'existe pas.", file=sys.stderr)
        return 1

    with open(args.input, "r", encoding="utf-8") as f:
        request_data = json.load(f)

    requests = request_data.get("requests", [])
    print(f"[IconForge AI] {len(requests)} requêtes à traiter.")

    # 3. Initialisation du pipeline de génération & validation
    validator_bridge = ValidatorBridge()
    pipeline = ReflectorPipeline(brand_style, validator_bridge, use_llm=args.llm)

    if args.llm:
        print("[IconForge AI] Mode LLM activé (Gemini API) pour concepts inconnus.")

    # 4. Traitement
    results = pipeline.process_requests(requests, args.output)

    # 5. Bilan
    all_valid = all(r["valid"] for r in results)
    print(f"[IconForge AI] Génération terminée. Statut: {'SUCCÈS' if all_valid else 'ÉCHEC'}")
    
    # Écriture du rapport d'évaluation métrique
    eval_dir = Path("evaluation")
    eval_dir.mkdir(exist_ok=True)
    metrics = {
        "total": len(results),
        "valid_count": sum(1 for r in results if r["valid"]),
        "results": results
    }
    (eval_dir / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8")

    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())
