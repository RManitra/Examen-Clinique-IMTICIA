"""Parser dynamique pour extraire la charte graphique et analyser les références à l'exécution."""

import re
import xml.etree.ElementTree as ET
from pathlib import Path

HEX_COLOR_PATTERN = re.compile(r"#[0-9a-fA-F]{6}")
VIEWBOX_PATTERN = re.compile(r'viewBox=["\']([^"\']+)["\']|viewBox:\s*([^\n;]+)')
STROKE_WIDTH_PATTERN = re.compile(r"stroke-width[=:]\s*[\"']?([0-9.]+)", re.IGNORECASE)
BOUNDS_PATTERN = re.compile(r"x\s*=\s*([0-9.]+)\s*…\s*([0-9.]+).*?y\s*=\s*([0-9.]+)\s*…\s*([0-9.]+)", re.IGNORECASE)

class BrandParser:
    def __init__(self, guidelines_path: str | Path, references_dir: str | Path):
        self.guidelines_path = Path(guidelines_path)
        self.references_dir = Path(references_dir)

    def parse_guidelines(self) -> dict:
        """Parse le fichier Markdown de la charte graphique."""
        if not self.guidelines_path.exists():
            raise FileNotFoundError(f"Charte non trouvée: {self.guidelines_path}")

        content = self.guidelines_path.read_text(encoding="utf-8")
        colors = sorted(list(set(c.upper() for c in HEX_COLOR_PATTERN.findall(content))))
        
        viewbox = "0 0 64 64"
        vb_match = re.search(r"viewBox=[\"']([^\"']+)[\"']", content, re.IGNORECASE)
        if vb_match:
            viewbox = vb_match.group(1)

        safe_min, safe_max = 5.0, 59.0
        bounds_match = BOUNDS_PATTERN.search(content)
        if bounds_match:
            safe_min = float(bounds_match.group(1))
            safe_max = float(bounds_match.group(2))

        stroke_width = 2.5
        sw_match = STROKE_WIDTH_PATTERN.search(content)
        if sw_match:
            stroke_width = float(sw_match.group(1))

        return {
            "allowed_colors": colors,
            "view_box": viewbox,
            "safe_min": safe_min,
            "safe_max": safe_max,
            "stroke_width": stroke_width,
            "stroke_linecap": "round",
            "stroke_linejoin": "round",
            "max_colors": 4
        }

    def parse_references(self) -> list[dict]:
        """Analyse les SVG de référence présents dans references/."""
        references_data = []
        if not self.references_dir.exists():
            return references_data

        for svg_file in sorted(self.references_dir.glob("*.svg")):
            try:
                tree = ET.parse(svg_file)
                root = tree.getroot()
                references_data.append({
                    "filename": svg_file.name,
                    "tag": root.tag,
                    "raw": svg_file.read_text(encoding="utf-8")
                })
            except Exception as e:
                print(f"Attention: Impossible d'analyser la référence {svg_file.name}: {e}")

        return references_data
