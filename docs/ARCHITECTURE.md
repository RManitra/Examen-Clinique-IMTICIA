# Architecture & Structure — IconForge AI

## Vue d'ensemble

IconForge AI est un système de génération automatisée d'icônes SVG cohérentes. Il prend en entrée des concepts exprimés en langage naturel et produit une famille d'icônes respectant une charte graphique lue dynamiquement à l'exécution.

---

## Arborescence complète du dépôt

```
Examen-Clinique-IMTICIA/
│
├── docs/                                    # Documentation du projet
│   ├── ARCHITECTURE.md                      # ← Ce fichier
│   └── Sujet - Clinique IMTICIA.pdf         # Sujet officiel de l'épreuve
│
├── src/                                     # Code source principal
│   ├── __init__.py                          # Initialisation du package
│   ├── parser.py                            # Extraction dynamique de la charte graphique
│   ├── generator.py                         # Génération vectorielle SVG
│   ├── validator_bridge.py                  # Pont vers le validateur déterministe
│   └── reflector.py                         # Boucle Generate-Evaluate-Refine
│
├── config/                                  # Configuration du système
│   └── prompts.yaml                         # Prompts et paramètres pour le LLM/générateur
│
├── tools/                                   # Outils externes et validateurs
│   └── validate_svg.py                      # Validateur déterministe SVG (du jury)
│
├── benchmark/                               # Contrat d'exécution et concepts
│   ├── request.schema.json                  # Schéma JSON d'entrée
│   ├── public-concepts.json                 # 5 concepts publics de test
│   └── README.md                            # Documentation du benchmark
│
├── evaluation/                              # Résultats des évaluations
│   └── metrics.json                         # Rapport de validation des SVG générés
│
├── references/                              # ICÔNES DE RÉFÉRENCE (few-shot visuel)
│   ├── formation.svg                        # Livre ouvert + étincelle d'apprentissage
│   ├── informatique.svg                     # Terminal de code
│   ├── innovation.svg                       # Ampoule + étincelles
│   ├── reseau.svg                           # Réseau de nœuds distribués
│   └── recherche.svg                        # Document analysé par une loupe
│
├── outputs/                                 # SVG générés par le système
│   └── public/
│       ├── cloud.svg
│       ├── security.svg
│       ├── database.svg
│       ├── collaboration.svg
│       └── deployment.svg
│
├── assets/                                  # Assets de marque (logo, etc.)
│   └── README.md
│
├── submission-template/                     # Templates de remise
│   ├── manifest.schema.json                 # Schéma du manifeste
│   ├── manifest.example.json                # Exemple de manifeste
│   ├── README.md                            # Canevas du rapport
│   └── outputs/
│       └── README.md
│
├── brand-guidelines.md                      # Chartre graphique (remplacée par le jury)
├── reference-sheet.png                      # Planche visuelle de référence
├── readme-model.md                          # Canevas README à compléter
├── generate.py                              # Script d'orchestration principal (point d'entrée)
├── run.sh                                   # Script shell universel (alternative)
├── manifest.json                            # Manifeste de remise
└── requirements.txt                         # Dépendances Python
```

---

## Flux de données

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ENTRÉE                                       │
│                                                                     │
│  benchmark/public-concepts.json                                     │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ {                                                           │    │
│  │   "requests": [                                             │    │
│  │     {"id": "cloud", "concept": "Cloud", "context": "..."}   │    │
│  │     {"id": "security", "concept": "Sécurité", ...}          │    │
│  │     ...                                                     │    │
│  │   ]                                                         │    │
│  │ }                                                           │    │
│  └─────────────────────────────────────────────────────────────┘    │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   1. PARSER (src/parser.py)                         │
│                                                                     │
│  Lit à l'exécution :                                                │
│  ├── brand-guidelines.md  →  palette, viewBox, marges, traits      │
│  └── references/*.svg     →  style visuel, formes, proportions     │
│                                                                     │
│  Sortie : brand_style = {                                           │
│    "allowed_colors": ["#FFD21E", "#FF9D00", "#6B7280", ...],       │
│    "view_box": "0 0 64 64",                                        │
│    "safe_min": 5.0,                                                 │
│    "safe_max": 59.0,                                                │
│    "stroke_width": 2.5,                                             │
│    "stroke_linecap": "round",                                       │
│    "stroke_linejoin": "round",                                      │
│    "max_colors": 4                                                  │
│  }                                                                  │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│               2. GENERATOR (src/generator.py)                       │
│                                                                     │
│  Prend : concept (texte) + brand_style (règles extraites)          │
│  Produit : un SVG vectoriel autonome                                │
│                                                                     │
│  Stratégie :                                                        │
│  ├── Pour les concepts publics : templates pré-définis              │
│  ├── Fallback : générateur générique (_generate_generic)            │
│  └── [À IMPLÉMENTER] : génération via LLM ou représentation        │
│       intermédiaire paramétrique                                    │
│                                                                     │
│  Contraintes respectées :                                           │
│  ├── viewBox fixe                                                   │
│  ├── Palette dynamique (pas de couleurs hardcodées)                 │
│  ├── stroke-width, linecap, linejoin conformes                      │
│  └── Zone utile x=5..59, y=5..59                                   │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│           3. VALIDATOR BRIDGE (src/validator_bridge.py)             │
│                                                                     │
│  Interface Python vers tools/validate_svg.py                        │
│                                                                     │
│  Contrôles déterministes :                                          │
│  ├── XML bien formé                                                 │
│  ├── Élément racine <svg>                                           │
│  ├── viewBox conforme                                               │
│  ├── Palette respectée (couleurs autorisées uniquement)             │
│  ├── Max 4 couleurs visibles                                        │
│  ├── Éléments interdits absents (filter, mask, script, etc.)        │
│  ├── stroke-width = 2.5                                             │
│  ├── stroke-linecap = "round"                                       │
│  ├── stroke-linejoin = "round"                                      │
│  ├── Pas d'attribut class                                           │
│  ├── Pas de référence url()                                         │
│  ├── Pas de gestionnaire d'événement (onclick, etc.)                │
│  └── [Avec Inkscape] Emprise dans zone utile x=5..59, y=5..59      │
│                                                                     │
│  Sortie : rapport {valid, errors, warnings, colors}                 │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│            4. REFLECTOR (src/reflector.py)                          │
│                                                                     │
│  Boucle Generate → Evaluate → Refine                                │
│                                                                     │
│  [À IMPLÉMENTER] :                                                  │
│  ├── Tant que non valide : régénérer avec paramètres ajustés        │
│  ├── Mesurer la cohérence inter-icônes                              │
│  ├── Score = f(palette, trait, densité, géométrie, complexité)     │
│  └── Conditions d'arrêt : max itérations ou validé                 │
│                                                                     │
│  Actuel : pas de boucle, validation unique sans raffinement         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        SORTIE                                       │
│                                                                     │
│  outputs/public/<id>.svg  (un fichier par concept)                  │
│  evaluation/metrics.json  (rapport de validation)                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Composants détaillés

### `generate.py` — Point d'entrée

| Élément | Description |
|---------|-------------|
| Rôle | Orchestrateur principal |
| Entrée | `--input <requests.json> --output <outputs/>` |
| Options | `--guidelines`, `--references` (chemins personnalisables) |
| Dépendances | `src/parser.py`, `src/generator.py`, `src/reflector.py` |
| Sortie | Fichiers SVG + `evaluation/metrics.json` |

### `src/parser.py` — Extraction de la charte

| Méthode | Description |
|---------|-------------|
| `parse_guidelines()` | Parse `brand-guidelines.md` avec des regex pour extraire : couleurs (`#hex`), viewBox, marges (`safe_min`/`safe_max`), `stroke-width` |
| `parse_references()` | Analyse les 5 SVG de référence via `xml.etree.ElementTree` : tag racine, contenu brut |

### `src/generator.py` — Génération SVG

| Méthode | Description |
|---------|-------------|
| `generate_icon(request)` | Route vers la bonne méthode selon `concept_id` |
| `_generate_cloud()` | Nuage jaune avec accent orange |
| `_generate_security()` | Bouclier jaune + cadenas orange |
| `_generate_database()` | Cylinder jaune + ellipses orange |
| `_generate_collaboration()` | Deux silhouettes + nœud central orange |
| `_generate_deployment()` | Flèche vers le haut jaune + base orange |
| `_generate_generic()` | Rectangle arrondi jaune + cercle orange (fallback) |

### `src/validator_bridge.py` — Validation

| Méthode | Description |
|---------|-------------|
| `__init__(profile_path)` | Charge le profil de validation (défaut = profil public) |
| `validate(svg_path, xml_only)` | Appelle `validate_svg.validate_file()` avec le profil |

### `src/reflector.py` — Boucle d'amélioration

| Méthode | Description |
|---------|-------------|
| `process_requests(requests, output_dir)` | Itère sur chaque requête, génère, valide, écrit le résultat |

### `tools/validate_svg.py` — Validateur du jury

| Fonction | Description |
|----------|-------------|
| `load_profile(path)` | Charge un profil JSON (défaut : profil public Hugging Face) |
| `validate_file(path, profile)` | Validation XML + couleurs + traits + zone utile |
| `validate_collection(target, requests)` | Vérifie la correspondance fichiers/requêtes |
| `rendered_bounds(path)` | Calcule l'emprise via Inkscape `--query-all` |
| `walk_elements(element, ...)` | Parcours récursif de l'arbre SVG |

---

## Contraintes de la charte graphique

### Déterministes (vérifiables par programme)

| Contrainte | Valeur | Source |
|-----------|--------|--------|
| `viewBox` | `0 0 64 64` | `brand-guidelines.md` §3 |
| Zone utile | `x = 5..59`, `y = 5..59` | `brand-guidelines.md` §3 |
| Jaune principal | `#FFD21E` | `brand-guidelines.md` §4 |
| Orange d'accent | `#FF9D00` | `brand-guidelines.md` §4 |
| Gris secondaire | `#6B7280` | `brand-guidelines.md` §4 |
| Encre sombre | `#111827` | `brand-guidelines.md` §4 |
| Blanc | `#FFFFFF` | `brand-guidelines.md` §4 |
| Max couleurs visibles | 4 | `brand-guidelines.md` §3 |
| `stroke-width` | 2.5 | `brand-guidelines.md` §5 |
| `stroke-linecap` | round | `brand-guidelines.md` §5 |
| `stroke-linejoin` | round | `brand-guidelines.md` §5 |
| Éléments interdits | filter, mask, script, text, style, image, etc. | `brand-guidelines.md` §3 |

### Qualitatives (jugement humain)

| Critère | Description |
|---------|-------------|
| Fidélité sémantique | L'icône représente-t-elle le concept ? |
| Lisibilité | Visible à 24px, 32px, 64px ? |
| Cohérence de collection | Les icônes partagent-elles le même langage visuel ? |
| Style | Accueillant, ludique, technologique (pas enfantin, pas photoréaliste) |
| Simplicité | Formes pleines, simples, généreuses |

---

## Contrat d'exécution

```bash
python generate.py --input <requests.json> --output <outputs/>
```

### Format d'entrée (`request.schema.json`)

```json
{
  "collection_id": "iconforge-public-v1",
  "requests": [
    {
      "id": "cloud",
      "concept": "Cloud",
      "context": "Infrastructure et services informatiques...",
      "keywords": ["nuage", "service", "infrastructure"]
    }
  ]
}
```

### Format de sortie

Un fichier `<id>.svg` par requête dans le dossier de sortie :

```text
outputs/
├── cloud.svg
├── security.svg
├── database.svg
├── collaboration.svg
└── deployment.svg
```

---

## Matrice d'évaluation (jury)

| Code | Concepts | Charte & Références | Fonction |
|------|----------|---------------------|----------|
| **PP** | Publics | Publiques | Référence de développement |
| **PS** | Publics | Secrètes | Test charte de remplacement |
| **SP** | Secrets | Publiques | Test concepts secrets |
| **SS** | Secrets | Secrètes | Test final combiné |

### Formules de scoring

```
Généralisation concepts secrets :
  Q_X = 0.5 * T_X + 0.5 * S_X
  G_c = 15 * Q_SS * (1 - 0.5 * D_c)
  où D_c = max(0, Q_PS - Q_SS)

Généralisation charte secrète :
  R_X = 0.5 * T_X + 0.5 * V_X
  G_b = 10 * R_SS * (1 - 0.5 * D_b)
  où D_b = max(0, R_SP - R_SS)
```

---

## Tableau des 100 points

| Critère | Points |
|---------|--------|
| Conformité technique | 20 |
| Fidélité sémantique et lisibilité | 20 |
| Généralisation aux concepts secrets | 15 |
| Généralisation à une charte secrète | 10 |
| Architecture et boucle d'évaluation | 10 |
| Cohérence de collection | 10 |
| Qualité du code et reproductibilité | 5 |
| Présentation vidéo (3-5 min) | 10 |
| **Total** | **100** |

---

## Dépendances

| Package | Version | Usage |
|---------|---------|-------|
| Python | >= 3.10 | Runtime |
| pyyaml | >= 6.0 | Parsing de `config/prompts.yaml` |
| jinja2 | >= 3.0 | Templates de prompts (si utilisé) |
| Inkscape | — | Validation de la zone utile stricte |
| xml.etree.ElementTree | stdlib | Parsing SVG |
| argparse | stdlib | Interface CLI |
| json | stdlib | Lecture/écriture JSON |

---

## État actuel vs objectif

| Composant | État | Priorité |
|-----------|------|----------|
| `parser.py` | Fonctionnel (regex) | — |
| `generator.py` | Catalogue dur (5 concepts) | **CRITIQUE** |
| `validator_bridge.py` | Fonctionnel (xml_only) | Faible |
| `reflector.py` | Pas de boucle | **CRITIQUE** |
| `prompts.yaml` | Valeurs hardcodées | **CRITIQUE** |
| `generate.py` | Fonctionnel | — |
| `run.sh` | Fonctionnel | — |
| Boucle G-E-R | Absente | **CRITIQUE** |
| Cohérence collection | Absente | Élevée |
| Généralisation | Impossible | **CRITIQUE** |
