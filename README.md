# IconForge AI

## Description

Hackathon d’AI Engineering pour étudiants de niveau M2 disposant pour le Parcours IMTICIA (www.ispm-edu.com).

L’objectif est de construire un système capable de générer une **famille cohérente d’icônes SVG** à partir de concepts exprimés en langage naturel, en respectant une charte graphique imposée et lue à l’exécution.

La charte graphique est une adaptation pédagogique créée pour l’épreuve. Le challenge n’est affilié à aucune marque existante.

## Démarrage rapide

1. Lire `Sujet - Clinique IMTICIA.pdf` et faire lire `brand-guidelines.md` par le programme à l’exécution.
2. Faire analyser la collection du dossier `references/` sans la recopier ni figer ses valeurs dans le code.
3. Développer un système exposant le contrat décrit dans `benchmark/README.md` et résolvant la charte relativement à la racine du dépôt.
4. Générer les concepts de `benchmark/public-concepts.json`.
5. Installer Inkscape puis vérifier les SVG du profil public avec `python tools/validate_svg.py outputs/public/ --requests benchmark/public-concepts.json`.
6. Copier `readme-model.md` sous le nom `README.md` dans le dépôt de remise et le compléter. Le même canevas est également fourni dans `submission-template/README.md`.
7. Avant la remise, tester sans modifier le code une charte variante et un autre dossier de références placés aux mêmes emplacements.
