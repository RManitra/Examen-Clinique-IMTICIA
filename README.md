# [Institut Supérieur Polytechnique de Madagascar - ISPM](http://www.ispm-edu.com/)

## Examen de fin d'études - Master 2 AI Engineering

# Thème du Hackathon

## IconForge AI - Génération d'une famille cohérente d'icônes SVG

IconForge AI génère une collection d'icônes SVG à partir de requêtes en langage naturel, en s'appuyant sur Gemini (via LangChain) et une charte graphique lue sur disque à chaque exécution. Le système est composé d'un pipeline Python en deux étapes (texte → JSON de requêtes → SVG), exposé par une API FastAPI et consommé par une interface React.

# Liste des contributeurs

| Nom | Prénom(s) | Classe | Numéro | Rôle |
|---|---|---|---|---|
| VELOMITASAONA | Francki Aldo | IMTICIA 5 | 06 | Backend - API FastAPI et préparation des prompts envoyés à Gemini |
| RASOLONJATOVO | Soatiana Andrianina | IMTICIA 5 | 08 | Backend - Charte de marque et parsing |
| RAKOTONDRAMANANA | Mamisoa Désiré | IMTICIA 5 | 09 | Backend - Contrat JSON et validation |
| RAKOTOMAMONJY | Sitrakiniaina José | IMTICIA 5 | 03 | Schéma et changement de module |
| RANDRIANAIVO | Balsama Manitra | IMTICIA 5 | 05 | Chef de projet |
| RAMAMPIANDRA | Andriniaina Landry | IMTICIA 5 | 02 | Frontend - Génération JSON et SVG |

# Résumé du travail

## Problématique

Le défi consiste à transformer des concepts en langage naturel en une **famille cohérente** d'icônes SVG, en respectant une charte graphique fournie et remplaçable à l'exécution. La difficulté dépasse la simple génération de SVG indépendants : chaque icône doit non seulement être valide individuellement (viewBox, palette, zone utile), mais l'ensemble de la collection doit aussi partager une épaisseur de trait, des proportions de couleurs, un niveau de détail et un style visuel homogènes — une contrainte transversale qu'un générateur icône par icône ne garantit pas naturellement.

## Approche adoptée

Le pipeline (dossier `backend/`) suit sept étapes numérotées :

1. `1_schema.py` définit le JSON Schema du contrat de requêtes (et sa variante pour le mode "structured output" de Gemini) ;
2. `2_brand.py` relit `brand-guidelines.md` depuis le disque à chaque appel, sans jamais figer ses valeurs en constante ;
3. `3_prompts.py` construit les prompts System/Human en y injectant le schéma et le contenu courant de la charte ;
4. `6_generation.py` interroge Gemini (`ChatGoogleGenerativeAI`, via LangChain) une première fois en mode structuré pour obtenir la collection de requêtes JSON, puis une seconde fois par icône pour produire le SVG correspondant ;
5. `4_parsing.py` extrait le JSON ou le code SVG brut de la réponse (retrait des balises markdown, isolement de l'objet JSON ou du tag `<svg>...</svg>`) ;
6. `5_validation.py` vérifie la conformité au schéma et les contraintes déterministes du SVG (viewBox, balises interdites, absence de lien externe) ;
7. `7_source.py` assemble ces modules et expose `generate_icon_requests` / `generate_icon_svg` / `save_svg_file`, utilisés à la fois par le CLI (`__main__` de `7_source.py`) et par l'API FastAPI (`main.py`).

Le frontend (`frontend/src/App.js`) envoie la requête utilisateur à `POST /generate`, puis affiche chaque icône (aperçu SVG, code source, téléchargement).

Il n'y a actuellement **ni représentation intermédiaire structurée du langage visuel, ni boucle de raffinement automatique** : la charte est injectée telle quelle (texte brut) dans les prompts, et une icône qui échoue à la validation est simplement rejetée plutôt que renvoyée à Gemini avec le motif d'échec pour une nouvelle tentative. Voir la section [Limites et améliorations possibles](#limites-et-améliorations-possibles).

## Résultats obtenus

À ce stade, deux icônes d'exemple ont été produites manuellement pendant le développement (`backend/output/ballon-foot.svg`, `backend/output/laptop-green-red.svg`) ; aucune exécution scriptée sur `benchmark/public-concepts.json` n'a encore été réalisée ni versionnée.

En exécutant le validateur officiel du challenge sur ces deux fichiers (`python tools/validate_svg.py PROJET/backend/output/ --xml-only --json`), **les deux échouent** :

- `ballon-foot.svg` : couleurs `#000000`, `#1A1D20`, `#E2E8F0` hors palette autorisée (`#FFD21E`, `#FF9D00`, `#6B7280`, `#111827`, `#FFFFFF`), `stroke-width="2"` sur les polygones/lignes internes alors que la charte impose `2.5`, `stroke-linecap`/`stroke-linejoin` du cercle extérieur non `round`, remplissage noir implicite non déclaré.
- `laptop-green-red.svg` : toutes ses couleurs (`#064E3B`, `#10B981`, `#ECFDF5`, `#EF4444`) sont hors palette — attendu, puisque le prompt système (`3_prompts.py`) demande explicitement à Gemini de **prioriser une couleur exprimée par l'utilisateur** sur la palette de la charte, ce qui entre directement en conflit avec la contrainte de palette stricte du validateur officiel.

C'est la découverte la plus importante à date : le validateur interne (`5_validation.py`) ne contrôle que la structure (balise `<svg>`, `viewBox="0 0 64 64"`, absence de balises interdites, absence de lien externe), pas la palette exacte, le nombre de couleurs, le `stroke-width`/`stroke-linecap`/`stroke-linejoin` ni la zone utile — autant de contraintes que `tools/validate_svg.py` vérifie strictement. Le système peut donc considérer une icône comme valide alors qu'elle serait comptée comme non produite par le jury.

## Mots-clés

`SVG`, `AI Engineering`, `Gemini`, `LangChain`, `FastAPI`, `React`, `charte graphique`, `cohérence visuelle`, `validation déterministe`, `génération`

# Installation

## Prérequis

- système d'exploitation testé : Windows 11 (le pipeline étant écrit en Python/Node standard, il est utilisable sous Linux/macOS) ;
- Python 3.10 (voir les fichiers compilés dans `backend/__pycache__`) ;
- Node.js ≥ 18 pour le frontend (Create React App / `react-scripts` 5.0.1, React 19) ;
- ressources matérielles : aucune (pas d'inférence locale ; un accès réseau à l'API Gemini suffit) ;
- variables d'environnement : `GOOGLE_API_KEY` dans `backend/.env` (modèle fourni par `backend/.env.exemple`) ; `REACT_APP_API_BASE` optionnel dans `frontend/.env` (défaut `http://localhost:8000`).

## Commandes d'installation

```bash
# Backend
cd PROJET/backend
python -m venv venv
venv\Scripts\activate        # (sous Linux/macOS : source venv/bin/activate)
pip install -r requirements.txt
copy .env.exemple .env       # puis renseigner GOOGLE_API_KEY

# Frontend
cd PROJET/frontend
npm install
```

# Exécution

Le pipeline n'implémente pas encore la commande de référence attendue (`python generate.py --input requests.json --output outputs/`) : il n'existe pas de script `generate.py` acceptant `--input`/`--output` en batch. Les points d'entrée actuels sont :

```bash
# CLI interactif (une requête en langage naturel à la fois)
cd PROJET/backend
python 7_source.py

# API FastAPI (utilisée par le frontend)
cd PROJET/backend
uvicorn main:app --reload --port 8000

# Frontend (http://localhost:3000)
cd PROJET/frontend
npm start
```

**À faire avant la remise** : ajouter un adaptateur (`run.sh`/`run.bat` ou `generate.py`) qui lit un fichier de concepts au format `benchmark/request.schema.json`, appelle `generate_icon_svg` pour chaque requête et écrit `outputs/<id>.svg`, afin de respecter le contrat exact attendu par `benchmark/README.md` et utilisé par le jury.

## Exemple reproductible

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"icones pour un tableau de bord cloud : stockage, securite, deploiement\"}"
```

# Architecture du système

```
Requête utilisateur (texte libre)
        │
        ▼
3_prompts.build_messages()  ──►  Gemini (structured output, response_schema=1_schema)
        │
        ▼
4_parsing.extract_json()  ──►  5_validation.validate_against_schema()
        │  (collection_id + liste de requêtes id/concept/context/keywords)
        ▼
Pour chaque requête :
   3_prompts.build_svg_messages()  ──►  Gemini (texte libre)
        │
        ▼
   4_parsing.extract_svg()  ──►  5_validation.validate_svg_against_guidelines()
        │
        ▼
   6_generation.save_svg_file()  ──►  backend/output/<id>.svg
        │
        ▼
   main.py (FastAPI) sert /generate, /icons/{id}.svg, /icons/{id}/code
        │
        ▼
   frontend/src/App.js (React) : formulaire + galerie + téléchargement
```

`2_brand.py` est lu par `3_prompts.py` à chaque construction de prompt (étapes 1 et 2), garantissant que la charte courante (et non une valeur mise en cache) est utilisée. `_loader.py` est un utilitaire technique permettant d'importer les modules numérotés (`1_schema.py`, etc.), dont le nom ne peut pas être un identifiant Python valide.

Il n'existe pas de boucle d'amélioration automatisée à ce stade : une icône qui échoue à `validate_svg_against_guidelines` est simplement écartée (CLI) ou fait échouer toute la requête HTTP (API, `main.py` lève une exception dès le premier échec au lieu d'ignorer l'icône concernée).

# Formalisation de la charte graphique

`brand-guidelines.md` n'est jamais copié ni recopié en dur dans le code : `2_brand.py` le relit intégralement à chaque appel (`BRAND_GUIDELINES_PATH = .../brand-guidelines.md`, résolu relativement à la racine du dépôt) et `3_prompts.py` insère ce texte brut dans les system prompts des deux étapes. Concrètement, la palette, la géométrie et la zone utile, les traits et arrondis, la densité/complexité ainsi que les contraintes hard et soft **ne sont pas extraites ni structurées par du code Python** : c'est Gemini qui doit les interpréter directement depuis le texte Markdown de la charte, à chaque appel.

Cela empêche bien que des valeurs de la charte publique (`viewBox`, palette, largeur de trait, marges, style) soient figées comme constantes du code — aucune de ces valeurs n'apparaît en dur dans `1_schema.py`, `3_prompts.py` ou `6_generation.py`. En revanche, cela signifie aussi qu'il n'existe **aucune couche de vérification déterministe correspondant à la charte complète** : `5_validation.py` ne contrôle que ce qui est générique à toute charte (présence de `<svg>`, `viewBox` exact, balises interdites génériques, absence de lien externe), pas les valeurs propres à la charte active (palette autorisée, nombre max de couleurs, largeur de trait, zone utile chiffrée). C'est cet écart que révèlent les échecs documentés dans [Résultats obtenus](#résultats-obtenus).

Par ailleurs, le dossier `references/` (few-shot visuel : `formation.svg`, `informatique.svg`, `recherche.svg`, `reseau.svg`, `innovation.svg`) **n'est actuellement lu par aucun module** du pipeline : seul `brand-guidelines.md` est exploité. Le système ne bénéficie donc pas encore des exemples visuels fournis par la charte, ce qui est un manque pour la généralisation à une charte secrète (le jury remplace charte *et* références).

# Stratégie de génération

Le passage du concept en langage naturel au SVG se fait en deux appels génératifs distincts, sans étape paramétrique ou symbolique intermédiaire :

- **Étape 1 (semi-contrainte)** : Gemini est appelé en mode "structured output" (`response_mime_type="application/json"`, `response_schema=GEMINI_RESPONSE_SCHEMA`), ce qui contraint la forme JSON en sortie (clés, types, pattern des identifiants) mais laisse le contenu (`concept`, `context`, `keywords`) entièrement génératif.
- **Étape 2 (générative libre)** : Gemini reçoit le concept/context/keywords et la charte, puis produit directement le code SVG en texte libre — aucun gabarit, aucune bibliothèque de formes prédéfinies, aucune construction procédurale du dessin. La seule contrainte imposée en amont est textuelle (le prompt), la conformité étant vérifiée après coup (déterministe, via `5_validation.py`).

Il n'y a donc pas de composante purement paramétrique ou symbolique dans la génération du dessin lui-même ; le caractère déterministe du système se limite au contrat JSON (étape 1) et à la validation post-génération (étapes 1 et 2).

# Évaluation et boucle d'amélioration

## Contraintes déterministes

`5_validation.py` implémente deux validateurs :

- `validate_against_schema` : conformité au `ICONFORGE_REQUEST_SCHEMA` (via `jsonschema` si disponible, sinon des contrôles manuels équivalents) — présence de `collection_id`/`requests`, pattern `^[a-z0-9][a-z0-9-]*$` des identifiants, propriétés additionnelles interdites, `concept` non vide.
- `validate_svg_against_guidelines` : présence des balises `<svg>`/`</svg>`, `viewBox="0 0 64 64"` exact, absence des balises `script`, `image`, `text`, `linearGradient`, `radialGradient`, `filter`, `mask`, `pattern`, absence de référence externe (`href`/`xlink:href` en `http(s)://`).

Ces contrôles sont volontairement décrits dans le code comme un « filet de sécurité best-effort », pas un remplacement du contrôle qualitatif humain/jury. Comme détaillé plus haut, ils ne couvrent pas la palette exacte, le nombre maximal de couleurs, le `stroke-width`/`stroke-linecap`/`stroke-linejoin` imposés, ni la zone utile (`x`/`y` entre 5 et 59) — contrairement à `tools/validate_svg.py`.

## Contraintes qualitatives

Aucun contrôle qualitatif automatisé (fidélité sémantique, lisibilité, simplicité, style) n'est implémenté à ce jour : ces critères sont uniquement demandés dans les prompts système (`build_svg_system_prompt`), sans vérification a posteriori.

## Cohérence de collection

Aucune fonction ni protocole d'évaluation de la cohérence du set complet n'est implémenté. La cohérence repose uniquement sur le fait que la même charte (texte de `brand-guidelines.md`) est injectée dans chaque appel de génération SVG ; il n'existe pas de mesure croisée entre icônes (palette partagée, épaisseur de trait, densité, complexité) après génération.

## Boucle Generate - Evaluate - Refine

La boucle actuelle s'arrête après **Generate → Evaluate** : en cas d'échec de validation, le CLI (`7_source.py`) journalise l'erreur et passe à l'icône suivante ; l'API (`main.py`) lève une `HTTPException` 502 qui interrompt toute la requête. Dans les deux cas, **aucune étape de raffinement automatique** (nouvel appel à Gemini avec le motif d'échec pour corriger le SVG) n'est implémentée.

# Résultats et expériences

- **Concepts publics** : aucune exécution scriptée sur `benchmark/public-concepts.json` n'a été réalisée à ce jour ; seules deux icônes ad hoc existent dans `backend/output/`.
- **Taux de conformité technique** : sur les 2 fichiers actuellement disponibles, `python tools/validate_svg.py PROJET/backend/output/ --xml-only --json` renvoie **0/2 valides** (voir détail en [Résultats obtenus](#résultats-obtenus)).
- **Scores/observations qualitatives** : non mesurés (pas d'outil de scoring qualitatif mis en place).
- **Concepts hors domaine, charte variante, dégradation, échec instructif** : non encore testés.
- **Échec instructif déjà identifié** : la fonctionnalité qui priorise une couleur demandée par l'utilisateur (`3_prompts.build_svg_system_prompt`) produit systématiquement des couleurs hors de la palette autorisée par le validateur officiel dès que l'utilisateur exprime une préférence de couleur (cas `laptop-green-red.svg`) — un compromis produit/conformité à trancher avant la remise.
- **Limites actuelles** : voir [Limites et améliorations possibles](#limites-et-améliorations-possibles).

# Structure du dépôt

```text
PROJET/
├── backend/
│   ├── main.py            # API FastAPI (/generate, /icons/{id}.svg, /icons/{id}/code, /health)
│   ├── 1_schema.py        # JSON Schema du contrat de requêtes + variante Gemini
│   ├── 2_brand.py         # lecture de brand-guidelines.md à l'exécution
│   ├── 3_prompts.py       # construction des prompts System/Human (étapes 1 et 2)
│   ├── 4_parsing.py       # extraction JSON/SVG des réponses Gemini
│   ├── 5_validation.py    # validation schema + contraintes déterministes SVG
│   ├── 6_generation.py    # appels Gemini (LangChain) et sauvegarde des .svg
│   ├── 7_source.py        # assemblage du pipeline + CLI interactif
│   ├── _loader.py         # chargeur dynamique des modules numérotés
│   ├── requirements.txt
│   ├── .env.exemple
│   └── output/             # SVG générés (ex. ballon-foot.svg, laptop-green-red.svg)
└── frontend/
    ├── src/
    │   ├── App.js          # formulaire de requête + galerie d'icônes générées
    │   └── App.css
    ├── public/
    └── package.json        # Create React App (react-scripts 5.0.1, React 19)
```

# Manifeste de remise

Le fichier `manifest.json` doit respecter `submission-template/manifest.schema.json` et utiliser les clés imposées par le sujet :

```json
{
  "equipe": [
    "VELOMITASAONA Francki Aldo",
    "RASOLONJATOVO Soatiana Andrianina",
    "RAKOTONDRAMANANA Mamisoa Désiré",
    "RAKOTOMAMONJY Sitrakiniaina José",
    "RANDRIANAIVO Balsama Manitra",
    "RAMAMPIANDRA Andriniaina Landry"
  ],
  "methode": "pipeline en 2 étapes (JSON de requêtes structuré puis SVG en texte libre) via Gemini/LangChain, sans représentation intermédiaire structurée ni boucle de raffinement",
  "modeles": [{"nom": "gemini-3.6-flash", "version": "À vérifier - valeur placeholder dans 6_generation.py à confirmer avant remise", "local": false}],
  "bibliotheques": [
    "fastapi==0.141.1",
    "uvicorn==0.46.0",
    "pydantic==2.13.4",
    "python-dotenv==1.0.1",
    "langchain-core==1.6.0",
    "langchain-google-genai==4.3.5",
    "jsonschema==4.26.0",
    "react==19.2.8"
  ],
  "services_distants": ["Google Gemini API (langchain-google-genai)"],
  "repli_gratuit": "À compléter : préciser la solution locale/gratuite de secours si l'accès à l'API Gemini est indisponible."
}
```

> ⚠️ `backend/6_generation.py` définit `DEFAULT_MODEL = "gemini-3.6-flash"` avec un commentaire `# <--- Remplacer ici` laissé dans le code : ce nom de modèle ne correspond à aucune version connue de Gemini et doit être vérifié/corrigé avant la remise, sous peine de faire échouer tous les appels API.

# Vidéo de présentation

- lien vers la vidéo de 3 à 5 minutes : **À compléter**
- durée : **À compléter**

# Transparence sur les outils IA utilisés dans le développement et dans la documentation

## Outils IA utilisés dans le développement

| Outil ou modèle | Version | Mode d'accès | Utilisation précise | Parties produites ou modifiées | Vérification humaine |
|---|---|---|---|---|---|
| Google Gemini (via `langchain-google-genai`) | `gemini-3.6-flash` (à vérifier, cf. avertissement ci-dessus) | distant, payant/gratuit selon quota | génération des requêtes JSON d'icônes et du code SVG | `backend/output/*.svg`, réponses de `6_generation.py` | À compléter par l'équipe |
| À compléter | À compléter | local, gratuit ou payant | code, prompts, tests, architecture... | fichiers ou composants concernés | contrôle effectué |

Pour chaque outil, précisez également :

- les prompts ou familles de prompts importants (voir `backend/3_prompts.py` pour les prompts système versionnés dans le code) ;
- les modifications humaines apportées aux sorties ;
- les erreurs ou hallucinations détectées (par exemple, le nom de modèle `gemini-3.6-flash` à vérifier) ;
- les éventuelles limites de reproductibilité (température non nulle : `0.2` pour les requêtes, `0.4` pour le SVG) ;
- la solution gratuite ou locale de repli si un service distant a été utilisé.

## Outils IA utilisés dans la documentation

| Outil ou modèle | Version | Document concerné | Nature de l'assistance | Vérification et corrections humaines |
|---|---|---|---|---|
| À compléter | À compléter | README, rapport, schéma, vidéo... | rédaction, reformulation, traduction, synthèse... | À compléter |

## Déclaration de transparence

> Nous déclarons avoir listé de manière fidèle les outils d'intelligence artificielle utilisés pour le développement et pour la documentation. Nous assumons la responsabilité finale du code, des SVG, des résultats, des analyses et des textes remis.

# Modèles, bibliothèques, données et services

| Ressource | Version ou commit | Licence | Usage | Lien |
|---|---|---|---|---|
| Google Gemini API | `gemini-3.6-flash` (à vérifier) | propriétaire, usage soumis aux conditions Google | génération des requêtes JSON et du SVG | https://ai.google.dev/ |
| langchain-google-genai | 4.3.5 | MIT | intégration LangChain ↔ Gemini | À compléter |
| langchain-core | 1.6.0 | MIT | messages System/Human | À compléter |
| FastAPI | 0.141.1 | MIT | API HTTP du backend | https://fastapi.tiangolo.com/ |
| React | 19.2.8 | MIT | interface frontend | https://react.dev/ |
| jsonschema | 4.26.0 | MIT | validation du contrat JSON | À compléter |

# Contributions individuelles

Décrivez précisément les contributions de chaque membre au-delà du rôle général indiqué dans le tableau de la première section (tâches effectivement réalisées, fichiers modifiés, décisions prises). **À compléter par chaque membre de l'équipe.**

# Limites et améliorations possibles

- **Validation incomplète** : `5_validation.py` ne vérifie ni la palette exacte, ni le nombre maximal de couleurs, ni le `stroke-width`/`stroke-linecap`/`stroke-linejoin`, ni la zone utile (5–59) — contrairement à `tools/validate_svg.py`, qui a fait échouer les deux seuls exemples produits à ce jour.
- **Absence de boucle de raffinement** : aucune tentative de correction automatique (renvoyer l'erreur de validation à Gemini) n'est implémentée ; une icône non conforme est perdue.
- **`references/` non exploité** : le pipeline ne lit que `brand-guidelines.md`, jamais les exemples SVG du dossier `references/`, ce qui limite la fidélité au langage visuel attendu et la robustesse au changement de charte.
- **Aucune mesure de cohérence de collection** : pas de fonction `Consistency(S)` ni de comparaison inter-icônes.
- **Comportement incohérent entre CLI et API en cas d'échec** : le CLI ignore l'icône en échec et continue, l'API interrompt toute la requête (`HTTPException`).
- **Contrat CLI non conforme au sujet** : pas de script batch `--input`/`--output` équivalent à `python generate.py --input requests.json --output outputs/`.
- **Nom de modèle Gemini à vérifier** : `gemini-3.6-flash` (placeholder laissé dans le code) doit être remplacé par un identifiant de modèle réellement disponible avant toute exécution par le jury.
- **Priorité couleur utilisateur vs. palette de la charte** : la fonctionnalité qui laisse l'utilisateur imposer une couleur peut faire échouer la conformité technique dès qu'elle est utilisée ; à documenter comme compromis assumé ou à revoir.
- Avec une journée supplémentaire, priorités suggérées : ajouter les contrôles de palette/trait/zone utile dans `5_validation.py`, implémenter une boucle de refine (retry avec le motif d'échec), lire `references/` dans les prompts, et écrire l'adaptateur batch conforme au contrat du benchmark.

# Licence et propriété

Indiquez la licence du dépôt et vérifiez que toutes les ressources externes (Google Gemini, LangChain, FastAPI, React, palette Hugging Face citée à titre pédagogique dans `brand-guidelines.md`) sont compatibles avec cette licence. **À compléter par l'équipe.**
