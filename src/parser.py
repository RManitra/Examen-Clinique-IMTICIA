
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional, Union

PathLike = Union[str, Path]

# ---------------------------------------------------------------------------
# Expressions régulières utilisées pour extraire les informations du Markdown
# ---------------------------------------------------------------------------

HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{6}\b")

VIEWBOX_PATTERN = re.compile(
    r'viewBox\s*[:=]\s*["\']?\s*([\-0-9.]+\s+[\-0-9.]+\s+[0-9.]+\s+[0-9.]+)',
    re.IGNORECASE,
)

STROKE_WIDTH_PATTERN = re.compile(
    r"(?:stroke-width|largeur(?: de trait)?)\s*[=:]\s*[\"']?([0-9]+(?:\.[0-9]+)?)",
    re.IGNORECASE,
)

STROKE_LINECAP_PATTERN = re.compile(
    r"(?:stroke-linecap|terminaisons?(?:\s*\([^)]*linecap[^)]*\))?)\s*[=:]\s*[\"']?"
    r"(round|butt|square)",
    re.IGNORECASE,
)

STROKE_LINEJOIN_PATTERN = re.compile(
    r"(?:stroke-linejoin|jonctions?(?:\s*\([^)]*linejoin[^)]*\))?)\s*[=:]\s*[\"']?"
    r"(round|miter|bevel)",
    re.IGNORECASE,
)

MAX_COLORS_PATTERN = re.compile(
    r"(?:maximum|max(?:imum)?)[^0-9]{0,30}([0-9]+)\s+couleurs?", re.IGNORECASE
)

CORNER_RADIUS_PATTERN = re.compile(
    r"(?:rayon(?: de coin)?|corner-radius)[^0-9]{0,20}([0-9]+(?:\.[0-9]+)?)",
    re.IGNORECASE,
)

# Zone utile / marge de sécurité. Tolère plusieurs formulations :
#   "x = 5…59" / "x: 5-59" / "marge de sécurité : 2px"
SAFE_ZONE_RANGE_PATTERN = re.compile(
    r"x\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)\s*[\u2026.\-–]{1,3}\s*([0-9]+(?:\.[0-9]+)?)"
    r".*?"
    r"y\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)\s*[\u2026.\-–]{1,3}\s*([0-9]+(?:\.[0-9]+)?)",
    re.IGNORECASE | re.DOTALL,
)

SAFE_MARGIN_PATTERN = re.compile(
    r"marge de s[eé]curit[eé][^0-9]{0,20}([0-9]+(?:\.[0-9]+)?)\s*px",
    re.IGNORECASE,
)

FORBIDDEN_SECTION_PATTERN = re.compile(
    r"[eé]l[eé]ments? interdits?(.*?)(?:\n##|\Z)", re.IGNORECASE | re.DOTALL
)

FORBIDDEN_TOKEN_PATTERN = re.compile(r"[`\-\*]\s*<?\s*([a-zA-Z][a-zA-Z0-9]*)")

# ---------------------------------------------------------------------------
# Mots-clés stylistiques (extensible sans casser le contrat de sortie)
# ---------------------------------------------------------------------------

STYLE_RULES = {
    "filled_shapes": ["formes pleines", "formes simples", "formes généreuses"],
    "compact_silhouette": ["silhouette douce", "silhouette compacte"],
    "rounded": ["coins arrondis", "arrondis", "terminaisons cohérentes", "round"],
    "asymmetry": ["légère asymétrie", "asymétrie autorisée"],
    "flat_shadows": ["ombres uniquement sous forme d'aplats", "aplats"],
    "frontal_view": ["vue frontale", "quasi frontale"],
    "no_gradient": ["aucun gradient", "pas de gradient", "degrade", "dégradé"],
    "no_filter": ["aucun filtre", "pas de filtre"],
    "no_texture": ["aucune texture", "pas de texture"],
    "no_text": ["aucun texte", "pas de texte"],
}

# Éléments SVG considérés comme des formes (pour le comptage de densité)
SHAPE_TAGS = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}


class BrandParser:
    """Parse dynamiquement la charte et les références SVG."""

    def __init__(self, guidelines_path: PathLike, references_dir: PathLike):
        self.guidelines_path = Path(guidelines_path)
        self.references_dir = Path(references_dir)

    # -- Lecture -------------------------------------------------------

    def _read_guidelines(self) -> str:
        if not self.guidelines_path.exists():
            raise FileNotFoundError(f"Charte non trouvée : {self.guidelines_path}")
        return self.guidelines_path.read_text(encoding="utf-8")

    # -- Extraction charte (markdown) -----------------------------------

    def _extract_colors(self, content: str) -> list[str]:
        colors = HEX_COLOR_PATTERN.findall(content)
        return sorted(set(c.upper() for c in colors))

    def _extract_viewbox(self, content: str) -> Optional[str]:
        match = VIEWBOX_PATTERN.search(content)
        if match:
            return re.sub(r"\s+", " ", match.group(1).strip())
        return None

    def _extract_stroke_width(self, content: str) -> Optional[float]:
        match = STROKE_WIDTH_PATTERN.search(content)
        return float(match.group(1)) if match else None

    def _extract_linecap(self, content: str) -> Optional[str]:
        match = STROKE_LINECAP_PATTERN.search(content)
        return match.group(1).lower() if match else None

    def _extract_linejoin(self, content: str) -> Optional[str]:
        match = STROKE_LINEJOIN_PATTERN.search(content)
        return match.group(1).lower() if match else None

    def _extract_max_colors(self, content: str) -> Optional[int]:
        match = MAX_COLORS_PATTERN.search(content)
        return int(match.group(1)) if match else None

    def _extract_corner_radius(self, content: str) -> Optional[float]:
        match = CORNER_RADIUS_PATTERN.search(content)
        return float(match.group(1)) if match else None

    def _extract_safe_zone(self, content: str) -> Optional[dict]:
        """Zone utile explicite ('x = 5…59 / y = 5…59'), sinon dérivée de la
        marge de sécurité ('marge de sécurité : 2px') combinée au viewBox."""
        match = SAFE_ZONE_RANGE_PATTERN.search(content)
        if match:
            return {
                "x_min": float(match.group(1)),
                "x_max": float(match.group(2)),
                "y_min": float(match.group(3)),
                "y_max": float(match.group(4)),
            }

        margin_match = SAFE_MARGIN_PATTERN.search(content)
        viewbox = self._extract_viewbox(content)
        if margin_match and viewbox:
            try:
                _, _, w, h = (float(v) for v in viewbox.split())
            except ValueError:
                return None
            m = float(margin_match.group(1))
            return {"x_min": m, "x_max": w - m, "y_min": m, "y_max": h - m}

        return None

    def _extract_forbidden_elements(self, content: str) -> list[str]:
        forbidden = set()
        keywords = {
            "image": ["image", "matricielle"],
            "text": ["texte"],
            "font": ["police"],
            "gradient": ["gradient", "dégradé"],
            "filter": ["filtre"],
            "mask": ["masque"],
            "texture": ["texture"],
            "opacity": ["transparence", "opacité"],
    }

        for line in content.splitlines():
            line_lower = line.lower()
            if any(word in line_lower for word in ["aucun", "aucune", "interdit", "proscrit"]):
                for key, terms in keywords.items():
                    if any(t in line_lower for t in terms):
                        forbidden.add(key)

        return sorted(forbidden)
    

    def _extract_style_rules(self, content: str) -> dict:
        content_lower = content.lower()
        return {
            name: any(kw.lower() in content_lower for kw in kws)
            for name, kws in STYLE_RULES.items()
        }
    

    def parse_guidelines(self) -> dict:
        """Analyse complètement brand-guidelines.md et retourne un dict plat,
        directement consommable par generator.py / reflector.py."""
        content = self._read_guidelines()

        safe_zone = self._extract_safe_zone(content)

        result = {
            "allowed_colors": self._extract_colors(content),
            "view_box": self._extract_viewbox(content),
            "safe_zone": safe_zone,
            "safe_min": safe_zone["x_min"] if safe_zone else None,
            "safe_max": safe_zone["x_max"] if safe_zone else None,
            "stroke_width": self._extract_stroke_width(content),
            "stroke_linecap": self._extract_linecap(content),
            "stroke_linejoin": self._extract_linejoin(content),
            "corner_radius": self._extract_corner_radius(content),
            "max_colors": self._extract_max_colors(content),
            "forbidden_elements": self._extract_forbidden_elements(content),
            "style": self._extract_style_rules(content),
        }
        return result

    # -- Extraction références (SVG) ------------------------------------

    def _extract_svg_colors(self, root: ET.Element) -> list[str]:
        colors = set()
        for element in root.iter():
            for attribute in ("fill", "stroke", "color"):
                value = element.get(attribute)
                if value:
                    colors.update(m.upper() for m in HEX_COLOR_PATTERN.findall(value))
        return sorted(colors)

    def _extract_svg_stroke_widths(self, root: ET.Element) -> list[float]:
        widths = set()
        for element in root.iter():
            value = element.get("stroke-width")
            if value:
                try:
                    widths.add(float(value))
                except ValueError:
                    pass
        return sorted(widths)

    def _has_stroke(self, root: ET.Element) -> bool:
        for element in root.iter():
            stroke = element.get("stroke")
            if stroke and stroke.lower() != "none":
                return True
        return False

    def _count_shapes(self, root: ET.Element) -> dict:
        counts: dict[str, int] = {}
        for element in root.iter():
            tag = element.tag.split("}")[-1]
            if tag in SHAPE_TAGS:
                counts[tag] = counts.get(tag, 0) + 1
        return counts

    def _analyze_reference(self, svg_file: Path) -> dict:
        tree = ET.parse(svg_file)
        root = tree.getroot()
        shape_counts = self._count_shapes(root)
        return {
            "filename": svg_file.name,
            "tag": root.tag,
            "view_box": root.get("viewBox"),
            "colors": self._extract_svg_colors(root),
            "color_count": len(self._extract_svg_colors(root)),
            "shape_count": sum(shape_counts.values()),
            "shape_counts": shape_counts,
            "has_stroke": self._has_stroke(root),
            "stroke_widths": self._extract_svg_stroke_widths(root),
        }

    def parse_references(self) -> list[dict]:
        references_data = []
        if not self.references_dir.exists():
            return references_data
        for svg_file in sorted(self.references_dir.glob("*.svg")):
            try:
                references_data.append(self._analyze_reference(svg_file))
            except (ET.ParseError, OSError) as error:
                print(f"Attention : impossible d'analyser {svg_file.name}: {error}")
        return references_data

    def summarize_references(self, references: list[dict]) -> dict:
        if not references:
            return {
                "reference_count": 0,
                "common_colors": [],
                "all_colors": [],
                "average_shape_count": 0,
                "stroke_widths": [],
                "view_boxes": [],
            }

        all_colors: set[str] = set()
        stroke_widths: set[float] = set()
        view_boxes: list[str] = []
        shape_counts: list[int] = []

        for reference in references:
            all_colors.update(reference.get("colors", []))
            stroke_widths.update(reference.get("stroke_widths", []))
            if reference.get("view_box"):
                view_boxes.append(reference["view_box"])
            shape_counts.append(reference.get("shape_count", 0))

        common_colors = set(references[0].get("colors", []))
        for reference in references[1:]:
            common_colors.intersection_update(reference.get("colors", []))

        average_shape_count = sum(shape_counts) / len(shape_counts) if shape_counts else 0

        return {
            "reference_count": len(references),
            "common_colors": sorted(common_colors),
            "all_colors": sorted(all_colors),
            "average_shape_count": round(average_shape_count, 2),
            "stroke_widths": sorted(stroke_widths),
            "view_boxes": sorted(set(view_boxes)),
        }

    def analyze(self) -> dict:
        """Point d'entrée unique utilisé par generator.py / reflector.py.

        Certaines chartes décrivent une contrainte déterministe (ex. l'épaisseur
        de trait) uniquement en langage qualitatif ("épaisseur optique stable"),
        sans jamais donner le chiffre en texte. Dans ce cas, la valeur réelle
        n'existe que dans les SVG de référence : on la déduit d'eux, à condition
        qu'elle soit strictement identique sur toutes les références (sinon on
        laisse None plutôt que de deviner)."""
        guidelines = self.parse_guidelines()
        references = self.parse_references()
        reference_summary = self.summarize_references(references)

        sources = {"stroke_width": "guidelines", "view_box": "guidelines"}

        if guidelines["stroke_width"] is None:
            widths = reference_summary["stroke_widths"]
            if len(widths) == 1:
                guidelines["stroke_width"] = widths[0]
                sources["stroke_width"] = "references"

        if guidelines["view_box"] is None:
            view_boxes = reference_summary["view_boxes"]
            if len(view_boxes) == 1:
                guidelines["view_box"] = view_boxes[0]
                sources["view_box"] = "references"

        return {
            "guidelines": guidelines,
            "references": references,
            "reference_summary": reference_summary,
            "value_sources": sources,
        }


if __name__ == "__main__":
    import json
    import sys

    gpath = sys.argv[1] if len(sys.argv) > 1 else "brand-guidelines.md"
    rdir = sys.argv[2] if len(sys.argv) > 2 else "references"
    parser = BrandParser(gpath, rdir)
    print(json.dumps(parser.analyze(), indent=2, ensure_ascii=False))