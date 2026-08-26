"""
Utilitaire commun de chargement dynamique.

Les fichiers de backend/ sont nommes avec un prefixe numerique (1_schema.py,
2_brand.py, ...) pour rendre l'ordre du pipeline lisible dans l'explorateur
de fichiers. Un nom de module Python ne pouvant pas commencer par un chiffre,
`import 1_schema` est une erreur de syntaxe : ce chargeur importe donc ces
fichiers depuis leur chemin exact via importlib (avec un cache pour eviter de
re-executer un meme fichier plusieurs fois si plusieurs modules le chargent).
"""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

BACKEND_DIR = Path(__file__).resolve().parent
_cache: dict[str, ModuleType] = {}


def load(filename: str) -> ModuleType:
    """Charge (et met en cache) le module backend/<filename> par son chemin exact."""
    if filename in _cache:
        return _cache[filename]

    module_name = f"iconforge_{Path(filename).stem}"
    spec = importlib.util.spec_from_file_location(module_name, BACKEND_DIR / filename)
    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module
    _cache[filename] = module
    spec.loader.exec_module(module)
    return module
