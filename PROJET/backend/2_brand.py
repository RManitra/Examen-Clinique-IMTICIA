"""
[Repartition equipe] Personne 2 - Charte de marque.

Lit brand-guidelines.md depuis le disque a chaque appel, jamais mise en dur :
le jury remplace ce fichier (et le dossier references/) a l'evaluation finale,
donc aucune de ses valeurs (couleurs, contraintes de style...) ne doit devenir
une constante du code.
"""

from pathlib import Path

BRAND_GUIDELINES_PATH = Path(__file__).resolve().parent.parent / "brand-guidelines.md"


def load_brand_guidelines() -> str:
    """Charge le contenu actuel de brand-guidelines.md, sans en figer les valeurs."""
    try:
        return BRAND_GUIDELINES_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return ""
