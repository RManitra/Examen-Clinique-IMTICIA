"""
Backend FastAPI pour IconForge.

Expose en HTTP le pipeline de 7_source.py (requete utilisateur -> JSON de
requetes d'icones -> code SVG) : le client envoie un prompt, l'API l'execute
et retourne, pour chaque icone, le code SVG et le fichier .svg genere.

Lancement : uvicorn main:app --reload (depuis ce dossier backend/).
"""

import re
import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

BACKEND_DIR = Path(__file__).resolve().parent

# Necessaire pour que `from _loader import load` resolve, quelle que soit la
# facon dont ce module est charge (execution directe, uvicorn, importlib...).
sys.path.insert(0, str(BACKEND_DIR))

from _loader import load

pipeline = load("7_source.py")

ICON_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
OUTPUT_DIR = BACKEND_DIR / "output"

app = FastAPI(
    title="IconForge API",
    description="Generation d'icones SVG a partir d'une requete en langage naturel, via Gemini.",
)


class GenerateRequest(BaseModel):
    query: str
    collection_id: Optional[str] = None


class IconResult(BaseModel):
    id: str
    concept: str
    context: Optional[str] = None
    keywords: Optional[list[str]] = None
    svg_code: str
    svg_file_url: str


class GenerateResponse(BaseModel):
    collection_id: str
    icons: list[IconResult]


@app.get("/health")
def health() -> dict:
    """Verifie que l'API et la charte de marque sont accessibles."""
    return {
        "status": "ok",
        "brand_guidelines_found": pipeline.BRAND_GUIDELINES_PATH.exists(),
    }


@app.post("/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest) -> GenerateResponse:
    """Execute le pipeline complet pour la requete du client et retourne,
    pour chaque icone, le code SVG et l'URL de telechargement du fichier."""
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Le champ 'query' ne peut pas etre vide.")

    try:
        data = pipeline.generate_icon_requests(payload.query, collection_id=payload.collection_id)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Echec de generation des requetes d'icones : {exc}") from exc

    icons = []
    for req in data["requests"]:
        try:
            svg_code = pipeline.generate_icon_svg(req)
        except Exception as exc:
            raise HTTPException(
                status_code=502, detail=f"Echec de generation SVG pour '{req['id']}' : {exc}"
            ) from exc

        pipeline.save_svg_file(req["id"], svg_code, output_dir=OUTPUT_DIR)
        icons.append(
            IconResult(
                id=req["id"],
                concept=req["concept"],
                context=req.get("context"),
                keywords=req.get("keywords"),
                svg_code=svg_code,
                svg_file_url=f"/icons/{req['id']}.svg",
            )
        )

    return GenerateResponse(collection_id=data["collection_id"], icons=icons)


@app.get("/icons/{icon_id}.svg")
def get_icon_file(icon_id: str) -> FileResponse:
    """Sert le fichier .svg genere pour telechargement/visualisation directe."""
    if not ICON_ID_PATTERN.match(icon_id):
        raise HTTPException(status_code=400, detail="Identifiant d'icone invalide.")

    svg_path = OUTPUT_DIR / f"{icon_id}.svg"
    if not svg_path.exists():
        raise HTTPException(status_code=404, detail="Icone introuvable.")

    return FileResponse(svg_path, media_type="image/svg+xml", filename=f"{icon_id}.svg")


@app.get("/icons/{icon_id}/code")
def get_icon_code(icon_id: str) -> dict:
    """Retourne le code SVG brut (version code) de l'icone deja generee."""
    if not ICON_ID_PATTERN.match(icon_id):
        raise HTTPException(status_code=400, detail="Identifiant d'icone invalide.")

    svg_path = OUTPUT_DIR / f"{icon_id}.svg"
    if not svg_path.exists():
        raise HTTPException(status_code=404, detail="Icone introuvable.")

    return {"id": icon_id, "svg_code": svg_path.read_text(encoding="utf-8")}
