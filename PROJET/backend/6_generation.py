"""
[Repartition equipe] Personne 6 - Orchestration Gemini & sauvegarde.

Instancie ChatGoogleGenerativeAI et enchaine prompts -> appel Gemini ->
parsing -> validation pour les deux etapes du pipeline, puis ecrit le SVG
genere sur disque.
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from _loader import load

parsing = load("4_parsing.py")
prompts = load("3_prompts.py")
schema = load("1_schema.py")
validation = load("5_validation.py")

load_dotenv()

DEFAULT_MODEL = "gemini-3.6-flash"  # <--- Remplacer ici


def generate_icon_requests(
    user_query: str,
    collection_id: str | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.2,
) -> dict:
    """Interroge Gemini a partir d'une requete utilisateur libre et retourne
    un dict Python strictement conforme au schema IconForge.

    Args:
        user_query: besoin exprime en langage naturel par l'utilisateur de l'application.
        collection_id: identifiant de collection a imposer (optionnel).
        model: nom du modele Gemini a utiliser.
        temperature: temperature d'echantillonnage.

    Returns:
        dict conforme a ICONFORGE_REQUEST_SCHEMA.
    """
    # Meme pattern d'instanciation que 3_answer_generation.py : la cle API
    # est lue automatiquement depuis l'environnement (GOOGLE_API_KEY, charge
    # par load_dotenv()), pas besoin de la passer explicitement.
    llm = ChatGoogleGenerativeAI(
        model=model,
        temperature=temperature,
        response_mime_type="application/json",
        response_schema=schema.GEMINI_RESPONSE_SCHEMA,
    )

    messages = prompts.build_messages(user_query, collection_id)
    response = llm.invoke(messages)

    data = parsing.extract_json(response.content)
    validation.validate_against_schema(data)
    return data


def generate_icon_svg(
    request: dict,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.4,
) -> str:
    """Interroge Gemini pour produire le code SVG d'une requete d'icone
    (issue de generate_icon_requests), en respectant brand-guidelines.md.
    Une eventuelle preference de couleur du client est deja portee par le
    "concept"/"keywords" de `request` (capturee a l'etape 1) : voir
    prompts.build_svg_system_prompt.

    Args:
        request: un element de "requests" (dict avec id/concept/context/keywords).
        model: nom du modele Gemini a utiliser.
        temperature: temperature d'echantillonnage.

    Returns:
        code SVG (str), pret a etre ecrit dans un fichier .svg.
    """
    llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)

    messages = prompts.build_svg_messages(request)
    response = llm.invoke(messages)

    svg_code = parsing.extract_svg(response.content)
    validation.validate_svg_against_guidelines(svg_code)
    return svg_code


def save_svg_file(icon_id: str, svg_code: str, output_dir: Path | None = None) -> Path:
    """Ecrit le code SVG dans <output_dir>/<icon_id>.svg (par defaut : ./output
    a cote de ce module) et retourne le chemin du fichier pour visualisation."""
    output_dir = output_dir or (Path(__file__).resolve().parent / "output")
    output_dir.mkdir(parents=True, exist_ok=True)

    svg_path = output_dir / f"{icon_id}.svg"
    svg_path.write_text(svg_code, encoding="utf-8")
    return svg_path
