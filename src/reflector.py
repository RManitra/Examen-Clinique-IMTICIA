"""Module d'évaluation et de raffinement itératif (Generate-Evaluate-Refine)."""

import copy
import statistics
from pathlib import Path
from lxml import etree

from src.generator import IconGenerator
from src.validator_bridge import ValidatorBridge

SVG_NS = "http://www.w3.org/2000/svg"
PRIMITIVES = ("path", "circle", "rect", "line", "polygon", "polyline", "ellipse")


class ReflectorPipeline:
    def __init__(self, brand_style: dict, validator_bridge: ValidatorBridge,
                 max_iter: int = 5, use_llm: bool = False):
        self.brand_style = brand_style
        self.validator = validator_bridge
        self.generator = IconGenerator(brand_style, use_llm=use_llm)
        self.max_iter = max_iter
        self.use_llm = use_llm

    # ─────────────────────────────────────────────
    # Boucle principale — tâche 2.1 (P0) + 2.3 log
    # ─────────────────────────────────────────────
    def process_requests(self, requests: list[dict], output_dir: Path) -> list[dict]:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []

        for req in requests:
            result = self._generate_with_refine(req, output_dir)
            results.append(result)

        # cohérence sur la collection ENTIÈRE — tâche 4.2 / 2.6
        valid_files = [Path(r["file"]) for r in results if r["valid"]]
        collection_score = self.collection_consistency(valid_files)
        for r in results:
            r["collection_score"] = collection_score["score"]

        return results

    def _generate_with_refine(self, req: dict, output_dir: Path) -> dict:
        """Régénère tant que la validation hard échoue, jusqu'à max_iter."""
        req_id = req["id"]
        out_file = output_dir / f"{req_id}.svg"
        iterations = []
        report = {"valid": False, "errors": [], "warnings": []}
        svg_content = ""

        working_req = copy.deepcopy(req)

        for i in range(self.max_iter):
            svg_content = self.generator.generate_icon(working_req)
            out_file.write_text(svg_content, encoding="utf-8")
            report = self.validator.validate(out_file, xml_only=True)

            iterations.append({          # traçabilité pour le README (2.3)
                "iter": i,
                "valid": report["valid"],
                "errors": report.get("errors", []),
            })

            if report["valid"]:
                break

            # ajustement paramétrique après échec — tâche 2.4
            working_req = self._adjust(working_req, report)

        return {
            "id": req_id,
            "file": str(out_file),
            "valid": report["valid"],
            "errors": report.get("errors", []),
            "warnings": report.get("warnings", []),
            "iterations": len(iterations),
            "history": iterations,
            "semantic_score": self.semantic_fidelity(req, out_file)["score"],
        }

    def _adjust(self, req: dict, report: dict) -> dict:
        """Modifie la requête/hints pour la prochaine tentative selon l'erreur.
        Ne code AUCUNE valeur de charte : lit self.brand_style."""
        hints = req.setdefault("_hints", {})
        errors = " ".join(report.get("errors", [])).lower()

        if "viewbox" in errors or "emprise" in errors or "zone" in errors:
            hints["shrink"] = hints.get("shrink", 1.0) * 0.9   # rentrer dans la marge
        if "palette" in errors or "couleur" in errors or "color" in errors:
            hints["strict_palette"] = True
        if "stroke" in errors or "trait" in errors:
            hints["force_stroke_from_spec"] = True
        if "interdit" in errors or "forbidden" in errors:
            hints["strip_forbidden"] = True

        return req

    # ─────────────────────────────────────────────
    # Mesure d'un SVG — tâche 3.1 / 4.1
    # ─────────────────────────────────────────────
    @staticmethod
    def measure_svg(svg_path: Path) -> dict:
        tree = etree.parse(str(svg_path))
        root = tree.getroot()

        strokes, prims = [], []
        for e in root.iter():
            local = etree.QName(e).localname
            if local in PRIMITIVES:
                prims.append(local)
            sw = e.get("stroke-width")
            if sw:
                try:
                    strokes.append(float(sw))
                except ValueError:
                    pass

        vocab = {s: prims.count(s) for s in set(prims)}
        return {
            "stroke_widths": strokes,
            "primitive_count": len(prims),
            "shape_vocab": vocab,
        }

    # ─────────────────────────────────────────────
    # Cohérence de collection — tâche 4.2 / 2.6
    # Consistency(S) = f(trait, densité, ...)
    # ─────────────────────────────────────────────
    def collection_consistency(self, svg_paths: list[Path]) -> dict:
        if len(svg_paths) < 2:
            return {"score": 1.0, "terms": {}, "note": "collection trop petite"}

        metrics = [self.measure_svg(p) for p in svg_paths]
        stroke_meds = [statistics.median(m["stroke_widths"])
                       for m in metrics if m["stroke_widths"]]
        densities = [m["primitive_count"] for m in metrics]

        terms = {
            "stroke_consistency":  self._homogeneity(stroke_meds),
            "density_homogeneity": self._homogeneity(densities),
        }
        # poids à justifier dans le README
        weights = {"stroke_consistency": 0.5, "density_homogeneity": 0.5}
        score = sum(terms[k] * weights[k] for k in terms)
        return {"score": round(score, 4), "terms": terms, "weights": weights}

    # ─────────────────────────────────────────────
    # Fidélité sémantique — tâche 2.5 (P2)
    # Compare les mots-clés du concept à la desc SVG
    # ─────────────────────────────────────────────
    @staticmethod
    def semantic_fidelity(request: dict, svg_path: Path) -> dict:
        tree = etree.parse(str(svg_path))
        root = tree.getroot()
        NS = {"svg": "http://www.w3.org/2000/svg"}

        desc_el = root.find(".//svg:desc", NS)
        desc_text = (desc_el.text or "").lower() if desc_el is not None else ""
        title_el = root.find(".//svg:title", NS)
        title_text = (title_el.text or "").lower() if title_el is not None else ""

        concept_words = set(request.get("concept", "").lower().split())
        context_words = set(request.get("context", "").lower().split())
        query_words = concept_words | context_words

        svg_words = set(desc_text.split()) | set(title_text.split())

        if not query_words:
            return {"score": 1.0, "matched": [], "missing": []}

        matched = query_words & svg_words
        missing = query_words - svg_words
        score = len(matched) / len(query_words) if query_words else 1.0

        return {"score": round(score, 4), "matched": sorted(matched), "missing": sorted(missing)}

    @staticmethod
    def _homogeneity(values: list[float]) -> float:
        """1.0 = identiques, tend vers 0 quand la variance grandit."""
        clean = [v for v in values if v is not None]
        if len(clean) < 2:
            return 1.0
        mean = statistics.mean(clean)
        if mean == 0:
            return 1.0
        cv = statistics.pstdev(clean) / mean   # coefficient de variation
        return 1.0 / (1.0 + cv)

    # ─────────────────────────────────────────────
    # Normalisation des proportions — tâche 4.3 (P2)
    # Ajuste stroke-width et nombre de formes pour
    # réduire la variance intra-collection.
    # ─────────────────────────────────────────────
    def normalize_collection(self, svg_paths: list[Path]) -> dict:
        """Analyse la collection et retourne les écarts à corriger."""
        if len(svg_paths) < 2:
            return {"adjusted": 0, "note": "collection trop petite"}

        metrics = [self.measure_svg(p) for p in svg_paths]
        stroke_meds = [statistics.median(m["stroke_widths"])
                       for m in metrics if m["stroke_widths"]]
        densities = [m["primitive_count"] for m in metrics]

        target_stroke = statistics.median(stroke_meds) if stroke_meds else 2.5
        target_density = statistics.median(densities) if densities else 4

        adjustments = []
        for path, m in zip(svg_paths, metrics):
            issues = []
            if m["stroke_widths"]:
                med = statistics.median(m["stroke_widths"])
                if abs(med - target_stroke) > 0.5:
                    issues.append(f"stroke_median={med:.1f} vs target={target_stroke:.1f}")
            if abs(m["primitive_count"] - target_density) > 3:
                issues.append(f"density={m['primitive_count']} vs target={target_density}")
            if issues:
                adjustments.append({"file": str(path), "issues": issues})

        return {
            "target_stroke": round(target_stroke, 2),
            "target_density": target_density,
            "adjustments_needed": adjustments,
            "adjusted": len(adjustments),
        }

    # ─────────────────────────────────────────────
    # Validation cohérence par paires — tâche 4.4 (P2)
    # Compare chaque paire d'icônes et calcule un
    # score de similarité structurelle.
    # ─────────────────────────────────────────────
    def pairwise_coherence(self, svg_paths: list[Path]) -> dict:
        """Compare chaque paire d'icônes et retourne un score moyen."""
        if len(svg_paths) < 2:
            return {"score": 1.0, "pairs": []}

        metrics = [self.measure_svg(p) for p in svg_paths]
        pairs = []

        for i in range(len(svg_paths)):
            for j in range(i + 1, len(svg_paths)):
                m1, m2 = metrics[i], metrics[j]
                # Similarité de densité (nombre de formes)
                d1, d2 = m1["primitive_count"], m2["primitive_count"]
                if max(d1, d2) == 0:
                    density_sim = 1.0
                else:
                    density_sim = 1.0 - abs(d1 - d2) / max(d1, d2)

                # Similarité de vocabulaire (types de formes)
                v1 = set(m1["shape_vocab"].keys())
                v2 = set(m2["shape_vocab"].keys())
                if not v1 and not v2:
                    vocab_sim = 1.0
                else:
                    intersection = len(v1 & v2)
                    union = len(v1 | v2)
                    vocab_sim = intersection / union if union else 1.0

                pair_score = 0.5 * density_sim + 0.5 * vocab_sim
                pairs.append({
                    "file_a": str(svg_paths[i]),
                    "file_b": str(svg_paths[j]),
                    "density_sim": round(density_sim, 4),
                    "vocab_sim": round(vocab_sim, 4),
                    "score": round(pair_score, 4),
                })

        mean_score = statistics.mean(p["score"] for p in pairs) if pairs else 1.0
        return {"score": round(mean_score, 4), "pairs": pairs}