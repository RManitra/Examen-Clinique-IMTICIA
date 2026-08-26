# Institut Supérieur Polytechnique de Madagascar - ISPM

## Examen de fin d’études - Master 2 AI Engineering

# Thème du Hackathon : IconForge AI - Génération d’une famille cohérente d’icônes SVG

IconForge AI est un système autonome développé pour générer une famille cohérente d'icônes SVG à partir de concepts exprimés en langage naturel. Le système extrait dynamiquement les contraintes d'une charte graphique et d'icônes de référence fournies à l'exécution, puis applique une boucle itérative *Generate-Evaluate-Refine* pour garantir la conformité technique et la cohérence visuelle.

## 👥 Liste des contributeurs

| Nom | Prénom(s) | Classe | Numéro | Rôle |
|---|---|---|---|---|
| M2 Student | AI Engineer | M2 IMTICIA | 01 | Développeur principal / AI Engineering |

## 📝 Résumé du travail

### Problématique
La génération d'icônes individuelles via IA produit fréquemment des disparités d'épaisseur de trait, des dérives chromatiques ou des ruptures d'échelle. Assurer la cohérence visuelle d'une collection complète exige d'extraire dynamiquement le langage visuel commun et d'appliquer des règles de composition strictes.

### Approche adoptée
Le système analyse dynamiquement `brand-guidelines.md` et les fichiers SVG du dossier `references/`. Il construit une représentation intermédiaire des règles (palette, viewBox, stroke-width, zone utile, terminaisons), génère une première version de chaque icône, valide déterministement les sorties via `tools/validate_svg.py`, puis applique un raffinement itératif jusqu'à conformité.

### Résultats obtenus
- 100% de conformité déterministe sur les concepts publics.
- Respect strict du viewBox `0 0 64 64` et de la zone utile `x=5..59, y=5..59`.
- Palette limitée et maîtrisée (Jaune, Orange, Encre sombre, Blanc).

### Mots-clés
`SVG`, `AI Engineering`, `évaluation`, `cohérence visuelle`, `génération`, `validation déterministe`

---

## 🚀 Installation

### Prérequis
- Python 3.10+
- Inkscape (requis pour la validation stricte de l'emprise visuelle)

### Commandes d’installation
```bash
pip install -r requirements.txt
```

---

## ⚙️ Exécution

Commande universelle de génération :
```bash
python generate.py --input benchmark/public-concepts.json --output outputs/public/
```
Ou via le script shell :
```bash
bash run.sh --input benchmark/public-concepts.json --output outputs/public/
```

Validation des SVG générés :
```bash
python tools/validate_svg.py outputs/public/ --requests benchmark/public-concepts.json
```

---

## 🏗️ Architecture du système

```text
Examen-Clinique-IMTICIA/
├── brand-guidelines.md     # Charte graphique lue à l'exécution
├── references/             # SVG de référence analysés dynamiquement
├── src/
│   ├── parser.py           # Extrait la palette, les marges et les règles graphiques
│   ├── generator.py        # Génère la structure SVG vectorielle
│   ├── validator_bridge.py # Interfaces de contrôle déterministe
│   └── reflector.py        # Boucle d'amélioration Generate-Evaluate-Refine
├── generate.py             # Orchestrateur principal
└── tools/validate_svg.py   # Validateur déterministe SVG
```

---

## 📄 Manifeste de remise
Conforme au schéma `submission-template/manifest.schema.json`, présent dans `manifest.json`.
