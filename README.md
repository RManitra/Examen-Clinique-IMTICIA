# [Institut Superieur Polytechnique de Madagascar - ISPM](http://www.ispm-edu.com/)

## Examen de fin d'etudes - Master 2 AI Engineering

# Theme du Hackathon

## IconForge AI - Generation d'une famille coherente d'icones SVG

IconForge AI est un systeme autonome qui genere une famille coherente d'icones SVG a partir de concepts exprimes en langage naturel. Le systeme extrait dynamiquement les contraintes d'une charte graphique et d'icones de reference fournies a l'execution, puis applique une boucle iterative *Generate-Evaluate-Refine* pour garantir la conformite technique et la coherence visuelle.

# Liste des contributeurs

| Nom | Prenom(s) | Classe | Numero | Role |
|---|---|---|---|---|
| A completer | A completer | A completer | A completer | A completer |
| A completer | A completer | A completer | A completer | A completer |

# Resume du travail

## Problematique

La generation d'icones individuelles via IA produit frequemment des disparites d'epaisseur de trait, des derivees chromatiques ou des ruptures d'echelle. Assurer la coherence visuelle d'une collection complete exige d'extraire dynamiquement le langage visuel commun et d'appliquer des regles de composition strictes, ce qui est fondamentalement different de la simple generation de SVG independants.

## Approche adoptee

Notre systeme suit une chaine complete en 5 etapes :

1. **Analyse dynamique** (`parser.py`) : lecture a l'execution de `brand-guidelines.md` et extraction de la palette, du viewBox, de la stroke-width, de la zone utile, des terminaisons et des elements interdits. Analyse des SVG de reference pour extraire le vocabulaire formel.

2. **Mapping concept-formes** (`concept_map.py` + `shapes.py`) : dictionnaire statique de ~40 concepts mappes a des formes SVG reutilisables (bouclier, note, engrenage, fusée, etc.).

3. **Composition parametrique** (`composer.py` + `generator.py`) : assemblage des formes selon un DSL intermediaire (JSON), application des couleurs de la charte (primary/accent/stroke), respect du viewBox et de la zone utile.

4. **Validation deterministe** (`tools/validate_svg.py`) : verification XML, palette, stroke-width, zone utile (fallback Python sans Inkscape), elements interdits.

5. **Boucle Generate-Evaluate-Refine** (`reflector.py` ) : re-generation itérative avec hints (shrink, strict_palette) jusqu'a conformite, plus scoring de fidélite semantique et coherence de collection.

## Resultats obtenus

- **100% de conformite deterministe** sur les 5 concepts publics (cloud, security, database, collaboration, deployment).
- **Respect strict** du viewBox `0 0 64 64` et de la zone utile `x=5..59, y=5..59`.
- **Palette maitrisee** : Jaune (#FFD21E), Orange (#FF9D00), Encre sombre (#111827), Blanc (#FFFFFF).
- **Generation pour concepts inconnus** : le systeme genere des icones significatives pour ~40 concepts (musique, cuisine, transport, analytics, etc.) grace au moteur de composition.
- **Fallback robuste** : tout concept non mappe produit une icone conforme (rectangle + cercle dans la zone utile).
- **22 tests unitaires** passes, validation complete sans Inkscape.

## Mots-cles

`SVG`, `AI Engineering`, `evaluation`, `coherence visuelle`, `generation`, `validation deterministe`, `boucle iterative`, `charte graphique dynamique`

# Installation

## Prerequis

- Systeme d'exploitation teste : Linux (Fedora 44), compatible macOS/Windows
- Version de Python : 3.10+
- Ressources materielles : aucune ressource specifique (CPU suffit)
- Variables d'environnement : aucune

## Commandes d'installation

```bash
# Cloner le depot
git clone https://github.com/RManitra/Examen-Clinique-IMTICIA.git
cd Examen-Clinique-IMTICIA

# Creer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dependances
pip install -r requirements.txt
```

# Execution

La commande de reference est :

```bash
python generate.py --input benchmark/public-concepts.json --output outputs/public/
```

Ou via le script shell :

```bash
bash run.sh --input benchmark/public-concepts.json --output outputs/public/
```

## Exemple reproductible

```bash
# Generation des icones publiques
python generate.py --input benchmark/public-concepts.json --output outputs/public/

# Validation complete (XML + zone utile)
python tools/validate_svg.py outputs/public/ --requests benchmark/public-concepts.json

# Validation XML seule (sans controle d'emprise)
python tools/validate_svg.py outputs/public/ --requests benchmark/public-concepts.json --xml-only

# Rapport JSON complet
python tools/validate_svg.py outputs/public/ --json

# Validation avec un profil personnalise
python tools/validate_svg.py outputs/public/ --profile mon-profil.json
```

# Architecture du systeme

```text
Examen-Clinique-IMTICIA/
├── brand-guidelines.md          # Charte graphique lue a l'execution
├── references/                  # SVG de reference analyses dynamiquement
│   ├── formation.svg
│   ├── informatique.svg
│   ├── innovation.svg
│   ├── recherche.svg
│   └── reseau.svg
├── src/
│   ├── parser.py                # Extraction dynamique de la charte et des references
│   ├── generator.py             # Generation SVG vectorielle parametrique
│   ├── composer.py              # Moteur de composition DSL -> SVG
│   ├── concept_map.py           # Mapping concept -> formes semantiques (~40 concepts)
│   ├── shapes.py                # Bibliotheque de 20+ formes SVG reutilisables
│   ├── reflector.py             # Boucle Generate-Evaluate-Refine + scoring
│   └── validator_bridge.py      # Pont d'integration avec le validateur
├── tools/
│   └── validate_svg.py          # Validateur deterministe SVG (fallback Python)
├── tests/
│   ├── test_parser.py           # 6 tests du parser
│   ├── test_reflector.py        # 8 tests du reflector
│   └── test_composer.py         # 10 tests du composer
├── benchmark/
│   ├── public-concepts.json     # Concepts publics du challenge
│   └── request.schema.json      # Schema JSON des requetes
├── outputs/
│   └── public/                  # Icones SVG generees
├── config/
│   └── prompts.yaml             # Configuration (rules vides)
├── evaluation/
│   └── metrics.json             # Metriques de debug
├── generate.py                  # Orchestrateur principal
├── run.sh                       # Script d'execution universel
├── requirements.txt             # Dependances Python
└── manifest.json                # Manifeste de remise
```

### Composants cles

| Module | Role |
|--------|------|
| `parser.py` | Analyse `brand-guidelines.md` et `references/` pour extraire palette, viewBox, stroke-width, zone utile, terminaisons, elements interdites |
| `generator.py` | Genere le SVG final en appliquant les couleurs de la charte et en composant les formes |
| `concept_map.py` | Dictionnaire statique ~40 concepts -> layout de formes (note, bouclier, engrenage, etc.) |
| `shapes.py` | Bibliotheque de 20+ formes SVG parametriques (shield, lock, note, gear, star, heart, magnifier, etc.) |
| `composer.py` | Convertit un layout DSL (JSON) en fragment SVG avec resolution des roles (primary/accent/stroke) |
| `reflector.py` | Boucle G-E-R, scoring semantique, coherence de collection, normalisation |
| `validate_svg.py` | Validateur deterministe : XML, palette, stroke-width, zone utile (fallback Python), elements interdits |

# Formalisation de la charte graphique

Notre systeme extrait et represente, a chaque execution :

### Palette
Les couleurs sont extraites par regex depuis `brand-guidelines.md`. Le systeme identifie automatiquement les roles :
- `required_colors` : couleurs dominantes ( Jaune `#FFD21E`)
- `accent_colors` : couleurs d'accent (Orange `#FF9D00`)
- `allowed_colors` : palette complete autorisee

### Geometrie et zone utile
- `viewBox` : extrait par regex (`"0 0 64 64"`)
- Zone utile : `safe_min=5.0`, `safe_max=5.9` extrait depuis le texte ("x = 5...59")
- Le systeme compense la stroke-width dans les coordonnees internes

### Traits et arrondis
- `stroke-width` : extrait par regex depuis "contours sombres de `2.5` unites"
- `stroke-linecap` : extrait par regex ("terminaisons arrondies")
- `stroke-linejoin` : extrait par regex ("jonctions arrondies")

### Densite et complexite
- `measure_svg()` compte les primitives (path, circle, rect, etc.) et les types de formes
- `collection_consistency()` calcule la variance intra-collection

### Contraintes hard
- Palette strictement respectee (4 couleurs max)
- viewBox exact `0 0 64 64`
- Zone utile stricte x=5..59, y=5..59
- Aucun element interdit (gradient, filter, text, script, etc.)
- Stroke-width conforme (2.5)

### Contraintes soft
- Fidelite semantique (mots-cles du concept dans le titre/description SVG)
- Coherence de collection (variance de stroke et densite)
-lisibilite a petite taille

### Protection contre le hardcoding
Aucune valeur de la charte publique n'est figee dans le code :
- `generator.py` lit `brand_style["view_box"]`, `brand_style["stroke_width"]`, etc.
- Les couleurs sont resolues dynamiquement depuis `required_colors` et `accent_colors`
- La zone utile est lue depuis `brand_style["safe_zone"]`
- Les hints du reflector (shrink, strict_palette) ajustent la generation

# Strategie de generation

Un concept en langage naturel devient un SVG en 4 etapes :

1. **Lookup** : `concept_map.py` recherche le concept dans un dictionnaire de ~40 entrees. Chaque entree definit un layout de formes avec des roles (primary, accent, stroke).

2. **Resolution** : `composer.py` resout chaque forme en appelant la fonction correspondante dans `shapes.py` (ex: `shield()`, `note_music()`, `gear()`).

3. **Composition** : Les fragments SVG sont assembles avec les couleurs resolues depuis la charte (primary=jaune, accent=orange, stroke=encre sombre).

4. **Validation** : Le validateur deterministe verifie XML, palette, stroke-width, zone utile. Si echec, la boucle G-E-R ajuste les hints et re-genere.

**Generatif** : les coordonnees des formes sont parametriques (cx, cy, r, size).
**Parametrique** : les couleurs et le scale dependent de la charte.
**Symbolique** : le mapping concept->formes est statique et semantique.
**Deterministe** : la validation est 100% deterministe (pas de LLM).

# Evaluation et boucle d'amelioration

## Contraintes deterministes

Le validateur `tools/validate_svg.py` verifie :
- Validite XML
- ViewBox exact
- Palette autorisee (4 couleurs max)
- Stroke-width conforme (2.5)
- Stroke-linecap/linejoin (round)
- Zone utile stricte (x=5..59, y=5..59) via fallback Python (cairosvg+Pillow)
- Aucun element interdit (filter, gradient, text, script, etc.)
- Aucun gestionnaire d'evenement (onclick, etc.)
- Aucun attribut `class` ou `href`

## Contraintes qualitatives

- **Fidelite semantique** : `semantic_fidelity()` compare les mots-cles du concept au titre+description SVG, score 0..1.
- **Lisibilite** : les formes sont simples, compactes, reconnaissables a 24px.
- **Simplicite** : chaque icone utilise 2-4 formes max.

## Coherence de collection

```
Consistency(S) = 0.5 * stroke_consistency + 0.5 * density_homogeneity
```

Ou :
- `stroke_consistency` : homogeneite des stroke-widths medianes (coefficient de variation)
- `density_homogeneity` : homogeneite du nombre de formes par icone

`normalize_collection()` identifie les icones dont les proportions dévient des cibles medianes.

## Boucle Generate - Evaluate - Refine

```
┌─────────────────────────────────────────────────────┐
│  for i in range(max_iter=5):                        │
│    svg = generator.generate_icon(request)            │
│    report = validator.validate(svg)                  │
│    if report["valid"]: break                         │
│    request = reflector.adjust(request, report)       │
│      └─ hints: shrink, strict_palette, strip_forbidden│
└─────────────────────────────────────────────────────┘
```

**Conditions d'arret** : validation OK ou 5 iterations atteintes.
**Resultats mesures** : errors, warnings, semantic_score, collection_score, pairwise_coherence.

# Resultats et experiences

### Concepts publics (5/5 valides)

| Concept | Conformite | Emprise | Score semantique |
|---------|------------|---------|------------------|
| Cloud | OK | (5.88, 14.50) -> (55.38, 47.25) | 1.0 |
| Security | OK | (10.75, 5.75) -> (53.25, 58.25) | 1.0 |
| Database | OK | (10.75, 6.75) -> (53.25, 57.25) | 1.0 |
| Collaboration | OK | (7.75, 11.75) -> (56.25, 50.25) | 1.0 |
| Deployment | OK | (14.75, 5.75) -> (49.25, 58.25) | 1.0 |

### Concepts secrets (testes)

| Concept | Conformite | Formes utilisees |
|---------|------------|------------------|
| Musique | OK | note_music + bell |
| Cuisine | OK | bell + heart |
| Transport | OK | rocket + arrow_up |
| Analytics | OK | bar_chart + magnifier |

### Concepts hors domaine (fallback)

| Concept | Conformite | Comportement |
|---------|------------|--------------|
| Xylophone (inconnu) | OK | Fallback rectangle + cercle |

### Test avec charte variante

Le test `test_generalization_to_unknown_charte` valide que le systeme s'adapte a une charte avec des couleurs et viewBox differents, sans modification du code.

### Degradation observee

- **Changement de concept** : les concepts hors domaine produisent des icones generiques (rectangle + cercle) mais conformes.
- **Changement de charte** : le systeme s'adapte dynamiquement. La degradation est minime si les contraintes restent dans les memes plages.

### Echec instructif

Sans le fallback Python, le validateur exige Inkscape pour verifier la zone utile. Notre solution : un fallback qui rend le SVG via cairosvg et mesure l'emprise des pixels non-transparents, offrant la meme validation sans dependance systeme.

### Limites actuelles

- Le dictionnaire concept->formes est statique (~40 concepts). Un concept tres niche produira un fallback generique.
- La composition est simple (2-4 formes). Des icones complexes avec many details ne sont pas generees.
- Pas de generation par LLM : le systeme est 100% local et deterministe.

# Structure du depot

```text
Examen-Clinique-IMTICIA/
├── brand-guidelines.md          # Charte graphique
├── references/                  # 5 SVG de reference
├── src/
│   ├── parser.py                # Analyse dynamique charte + references
│   ├── generator.py             # Generation SVG parametrique
│   ├── composer.py              # Moteur de composition DSL
│   ├── concept_map.py           # Mapping ~40 concepts
│   ├── shapes.py                # 20+ formes SVG reutilisables
│   ├── reflector.py             # Boucle G-E-R + scoring
│   └── validator_bridge.py      # Pont validation
├── tools/
│   └── validate_svg.py          # Validateur deterministe
├── tests/
│   ├── test_parser.py           # 6 tests
│   ├── test_reflector.py        # 8 tests
│   └── test_composer.py         # 10 tests
├── benchmark/
│   ├── public-concepts.json     # Concepts publics
│   └── request.schema.json      # Schema JSON
├── outputs/public/              # Icones generees (10 SVGs)
├── config/prompts.yaml          # Configuration
├── evaluation/metrics.json      # Metriques debug
├── generate.py                  # Orchestrateur
├── run.sh                       # Script execution
├── requirements.txt             # Dependances
└── manifest.json                # Manifeste remise
```

# Manifeste de remise

Le fichier `manifest.json` doit respecter `submission-template/manifest.schema.json` et utiliser les cles imposees par le sujet :

```json
{
  "equipe": ["A completer avec les vrais noms"],
  "methode": "Analyse dynamique de charte + generation vectorielle parametrique + boucle iterative Generate-Evaluate-Refine",
  "modeles": [{"nom": "iconforge-svg-engine", "version": "1.0.0", "local": true}],
  "bibliotheques": ["pyyaml", "lxml", "cairosvg", "Pillow"],
  "services_distants": [],
  "repli_gratuit": "Generateur parametrique vectoriel local et boucle de raffinement deterministe"
}
```

# Video de presentation

- Lien vers la video de 3 a 5 minutes : **A completer**
- Duree : **A completer**

# Transparence sur les outils IA utilises dans le developpement et dans la documentation

Toute utilisation d'un outil d'IA doit etre declaree, y compris lorsqu'il uniquement servi a reformuler la documentation. Ajoutez ou supprimez des lignes selon vos besoins.

## Outils IA utilises dans le developpement

| Outil ou modele | Version | Mode d'acces | Utilisation precise | Parties produites ou modifiees | Verification humaine |
|---|---|---|---|---|---|
| A completer | A completer | local, gratuit ou payant | code, SVG, prompts, tests, architecture... | fichiers ou composants concernes | controle effectue |

Pour chaque outil, precisez egalement :

- les prompts ou familles de prompts importants ;
- les modifications humaines apportees aux sorties ;
- les erreurs ou hallucinations detectees ;
- les eventuelles limites de reproductibilite ;
- la solution gratuite ou locale de repli si un service distant a ete utilise.

## Outils IA utilises dans la documentation

| Outil ou modele | Version | Document concerne | Nature de l'assistance | Verification et corrections humaines |
|---|---|---|---|---|
| A completer | A completer | README, rapport, schema, video... | redaction, reformulation, traduction, synthese... | A completer |

## Declaration de transparence

> Nous declarons avoir liste de maniere fidele les outils d'intelligence artificielle utilises pour le developpement et pour la documentation. Nous assumons la responsabilite finale du code, des SVG, des resultats, des analyses et des textes remis.

# Modeles, bibliotheques, donnees et services

| Ressource | Version ou commit | Licence | Usage | Lien |
|---|---|---|---|---|
| pyyaml | >=6.0 | MIT | Parsing YAML (prompts.yaml) | https://pypi.org/project/PyYAML/ |
| lxml | >=4.9 | BSD | Parsing XML/SVG | https://pypi.org/project/lxml/ |
| cairosvg | >=2.7 | LGPL | Rendu SVG pour validation zone utile | https://pypi.org/project/CairoSVG/ |
| Pillow | >=10.0 | MIT | Analyse pixels pour emprise | https://pypi.org/project/Pillow/ |
| pytest | >=7.0 | MIT | Tests unitaires | https://pypi.org/project/pytest/ |

# Contributions individuelles

Decrivez precisement les contributions de chaque membre. Les roles generaux ne remplacent pas la description des taches effectivement realisees.

**A completer pour chaque membre de l'equipe.**

# Limites et ameliorations possibles

### Limites actuelles
- Dictionnaire concept->formes statique (~40 concepts). Un concept tres niche produit un fallback generique.
- Composition simple (2-4 formes par icone). Pas de details complexes.
- Pas de generation par LLM : le systeme est 100% local et deterministe.
- La coherence de collection est mesuree sur stroke-width et densite, pas sur la forme visuelle.

### Ameliorations avec une journee de plus
- Integrer un LLM pour generer des layouts de formes pour des concepts inconnus.
- Enrichir le dictionnaire a 100+ concepts.
- Ajouter un scoring de similarite visuelle (hash de forme, distance de contour).
- Generer automatiquement la video de presentation.
- Ajouter un mode interactif pour que l'utilisateur ajuste les icones.

# Licence et proprieté

**A completer** : indiquez la licence du depot et verifiez que toutes les ressources externes sont compatibles avec cette licence.
