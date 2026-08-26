"""
[Repartition equipe] Personne 3 - Construction des prompts.

Assemble les messages System/Human envoyes a Gemini pour les deux etapes du
pipeline : generation des requetes d'icones (JSON), puis generation du SVG.
"""

import json

from langchain_core.messages import HumanMessage, SystemMessage

from _loader import load

brand = load("2_brand.py")
schema = load("1_schema.py")


def _guidelines_block(fallback: str) -> str:
    """Bloc de charte a injecter dans un system prompt, ou un texte de repli
    si brand-guidelines.md est absent (memes raisons que 2_brand.py)."""
    guidelines = brand.load_brand_guidelines()
    if not guidelines:
        return fallback
    return (
        f"Charte de marque en vigueur (source : {brand.BRAND_GUIDELINES_PATH.name}, "
        "son contenu peut changer, ne t'appuie que sur ce texte, jamais sur une "
        f"valeur memorisee) :\n\n{guidelines}"
    )


def build_system_prompt() -> str:
    """System prompt de l'etape 1 (requetes d'icones), relisant la charte a
    chaque appel pour toujours refleter le contenu courant du fichier."""
    guidelines_block = _guidelines_block(
        "Aucune charte de marque n'est disponible pour cet appel : "
        "propose des concepts/keywords neutres, sans reference de couleur ou de style imposee."
    )

    return f"""Tu es le module de preparation de requetes du generateur d'icones IconForge.

Ton unique role est de transformer la demande en langage naturel d'un utilisateur
en une collection de requetes de generation d'icones, strictement conforme au
JSON Schema suivant (draft 2020-12) :

{json.dumps(schema.ICONFORGE_REQUEST_SCHEMA, ensure_ascii=False, indent=2)}

{guidelines_block}

Regles imperatives :
- Ta reponse doit etre EXCLUSIVEMENT un objet JSON valide, sans texte avant ou apres,
  sans balises markdown (pas de ```json), sans commentaires.
- L'objet JSON doit respecter exactement le schema : proprietes autorisees uniquement
  ("collection_id", "requests", "$schema" en option), pas de proprietes additionnelles.
- "collection_id" et chaque "id" de requete doivent respecter le pattern ^[a-z0-9][a-z0-9-]*$
  (minuscules, chiffres, tirets, pas d'espace ni d'accent).
- "requests" doit contenir au moins un element derive du besoin exprime par l'utilisateur.
- "concept" resume en une phrase claire l'icone a generer, coherente avec la charte ci-dessus.
- Si l'utilisateur exprime une preference de couleur dans sa demande (ex. "en couleur
  vert et violet", "dans les tons bleus"), reformule-la explicitement dans "concept"
  (ex. "Icone de parametre dans les tons vert et violet") et ajoute les couleurs
  citees a "keywords" : cette preference doit rester lisible pour l'etape suivante,
  qui genere le SVG a partir de ce "concept"/"keywords".
- "context" (optionnel) precise l'usage ou le contexte d'affichage de l'icone.
- "keywords" (optionnel) est une liste de mots-cles uniques, pertinents pour l'icone.
"""


def build_messages(user_query: str, collection_id: str | None = None) -> list:
    """Construit les messages System/Human envoyes a Gemini a partir d'une requete utilisateur."""
    instruction = user_query.strip()
    if collection_id:
        instruction += f"\n\n(collection_id impose : {collection_id})"

    return [
        SystemMessage(content=build_system_prompt()),
        HumanMessage(content=instruction),
    ]


def build_svg_system_prompt() -> str:
    """System prompt pour la generation SVG, relisant la charte a chaque appel
    (memes raisons que build_system_prompt : le fichier peut etre remplace).

    Le client n'a pas de champ dedie pour la couleur : s'il en a exprime une
    dans sa demande initiale, elle a ete reportee par l'etape 1 dans le
    "concept"/"keywords" de la requete (cf. build_system_prompt). Ce prompt
    demande donc explicitement de la detecter a cet endroit et de la
    prioriser sur la palette par defaut de la charte."""
    guidelines_block = _guidelines_block(
        "Aucune charte de marque n'est disponible : utilise un style simple, "
        "des couleurs plates et un viewBox 0 0 64 64."
    )

    return f"""Tu es le moteur de generation SVG d'IconForge.

Ton unique role est de transformer une requete d'icone (id, concept, context,
keywords) en un unique fichier SVG autonome, en respectant strictement la
charte de marque suivante :

{guidelines_block}

Regles imperatives :
- Ta reponse doit etre EXCLUSIVEMENT le code SVG, du tag `<svg` au tag
  `</svg>` inclus. Aucun texte avant/apres, aucune balise markdown, aucun
  commentaire XML.
- Respecte a la lettre toutes les contraintes deterministes de la charte
  (viewBox, zone utile, fond transparent, nombre de couleurs, absence
  d'image matricielle/texte/script/gradient/filtre/masque/lien externe).
- Respecte le langage graphique decrit dans la charte. Pour la palette : si le
  concept, le context ou les keywords ci-dessous mentionnent une ou plusieurs
  couleurs (ex. "vert et violet", "tons bleus"), utilise-les en priorite au
  lieu de la palette par defaut de la charte, tout en respectant les
  contraintes techniques (max 4 couleurs visibles, pas de gradient). Sinon,
  utilise la palette de la charte.
- Le rendu doit correspondre fidelement au concept fourni par l'utilisateur.
"""


def build_svg_messages(request: dict) -> list:
    """Construit les messages System/Human pour generer le SVG d'une requete d'icone."""
    lines = [f"concept: {request['concept']}"]
    if request.get("context"):
        lines.append(f"context: {request['context']}")
    if request.get("keywords"):
        lines.append(f"keywords: {', '.join(request['keywords'])}")
    instruction = "Genere l'icone SVG pour la requete suivante :\n" + "\n".join(lines)

    return [
        SystemMessage(content=build_svg_system_prompt()),
        HumanMessage(content=instruction),
    ]
