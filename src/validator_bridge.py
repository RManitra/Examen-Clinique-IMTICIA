"""Pont d'intégration avec le validateur déterministe SVG (tools/validate_svg.py)."""

import sys
from pathlib import Path

# Importer directement validate_file et load_profile depuis tools/validate_svg.py
TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import validate_svg

class ValidatorBridge:
    def __init__(self, profile_path: str | Path | None = None):
        self.profile = validate_svg.load_profile(Path(profile_path) if profile_path else None)

    def validate(self, svg_path: str | Path, xml_only: bool = True) -> dict:
        """Valide un fichier SVG généré par rapport aux contraintes du profil."""
        path = Path(svg_path)
        if not path.exists():
            return {
                "file": str(path),
                "valid": False,
                "errors": ["Le fichier n'existe pas."],
                "warnings": []
            }
        
        return validate_svg.validate_file(path, self.profile, xml_only=xml_only)
