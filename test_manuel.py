from src.parser import BrandParser
from src.generator import IconGenerator
import xml.etree.ElementTree as ET

# 1. On extrait la spec depuis la vraie charte
spec = BrandParser("brand-guidelines.md", "references").analyze()["guidelines"]
print("=== SPEC EXTRAITE ===")
print(spec)
print()

# 2. On génère une icône avec cette spec
gen = IconGenerator(spec)
svg = gen.generate_icon({"id": "cloud", "concept": "Cloud", "context": "stockage distant"})
print("=== SVG PRODUIT ===")
print(svg)
print()

# 3. On vérifie que le XML est valide et que le viewBox correspond bien à la charte
root = ET.fromstring(svg)
print("XML valide. viewBox =", root.get("viewBox"))
assert root.get("viewBox") == spec["view_box"], "Le viewBox du SVG ne correspond pas à la charte !"
print("OK : le viewBox du SVG correspond bien à la charte.")