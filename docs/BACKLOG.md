# Backlog — IconForge AI

## Légende des priorités

| Priorité | Signification                               |
| -------- | ------------------------------------------- |
| **P0**   | Critique — bloquante pour la soumission     |
| **P1**   | Haute — nécessaire pour un score acceptable |
| **P2**   | Moyenne — amélioration significative        |
| **P3**   | Basse — polish et optimisation              |

---

## Phase 1 — Chaîne minimale (P0)

> Objectif : un concept → un SVG valide de bout en bout.

| #        | Tâche                                                                                                | Priorité | Statut | Notes                                                                                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------- | -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.1 | Corriger `config/prompts.yaml` : supprimer les valeurs hardcodées | P0 | ✅ | `rules: {}` — les valeurs sont extraites dynamiquement par `src/parser.py` |
| 1.2      | Corriger `generator.py` : supprimer les couleurs hardcodées (`self.yellow`, `self.orange`, etc.)     | P0       | ✅     | Couleurs dynamiques via `brand_style["allowed_colors"]`, convention 1ère=stroke, 2e=primary, 3e=accent                                                                                         |
| 1.3 | Corriger `parser.py` : extraire les `required_colors` depuis le markdown | P0 | ✅ | `required_colors` et `accent_colors` extraits par rôle sémantique ("principal", "accent") dans la charte |
| 1.4      | Corriger `parser.py` : parser le `stroke-linecap` et `stroke-linejoin` depuis le markdown            | P0       | ✅     | Extraits dynamiquement via regex                                                                                                                                                               |
| 1.5      | Corriger `parser.py` : extraire `max_colors` depuis le markdown                                      | P0       | ✅     | Extrait dynamiquement via regex                                                                                                                                                                |
| 1.6 | Corriger `parser.py` : parser les balises interdites depuis le markdown | P0 | ✅ | Logique par mots-clés : 8 éléments extraits (filter, font, gradient, image, mask, opacity, text, texture) |
| 1.7      | Implémenter un vrai fallback dans `generator.py` pour les concepts inconnus                          | P0       | ⬜     | `_generate_generic()` est trop basique (rect+circle+croix)                                                                                                                                     |
| 1.8      | Tester `generate.py` avec un concept non public (ex: "intelligence artificielle")                    | P0       | ⬜     | Vérifier que le SVG produit est valide                                                                                                                                                         |
| 1.9      | Tester avec Inkscape installé pour valider la zone utile                                             | P0       | ⬜     | `--xml-only` masque les erreurs d'emprise                                                                                                                                                      |
| **1.10** | **[BUG B1] Corriger `generate.py` : utiliser `analyze()` au lieu de `parse_guidelines()`**           | **P0**   | ⬜     | **`parse_guidelines()` retourne `stroke_width=None` → fallback 1.5 → tous les SVG échouent (validator attend 2.5)**                                                                            |
| **1.11** | **[BUG B2] Corriger regex `STROKE_WIDTH_PATTERN` pour matcher "contours sombres de \`2.5\` unités"** | **P0**   | ⬜     | **Le pattern actuel exige préfixe `stroke-width:` ou `largeur de trait:` — il faut ajouter "unités", "unité", "contours", "épaisseur"**                                                        |
| **1.12** | **[BUG B3] Corriger l'ordre des couleurs dans le generator pour utiliser `#FFD21E` comme primaire** | **P0** | ✅ | **Generator utilise `required_colors[0]` comme `primary` et `accent_colors[0]` comme `accent` — Mapping correct : jaune→primary, orange→accent, encre→stroke** |

---

## Phase 2 — Boucle Generate-Evaluate-Refine (P0)

> Objectif : le système améliore ses sorties de manière itérative.

| #       | Tâche                                                                                        | Priorité | Statut | Notes                                                                                                                                                                              |
| ------- | -------------------------------------------------------------------------------------------- | -------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2.1     | Implémenter la boucle `while not valid` dans `reflector.py`                                  | P0       | ✅     | `_generate_with_refine()` avec `for i in range(max_iter)`                                                                                                                          |
| 2.2     | Ajouter un compteur d'itérations max (ex: 5)                                                 | P0       | ✅     | `max_iter=5` en paramètre du constructeur                                                                                                                                          |
| 2.3     | Logger chaque itération (numéro, erreur, SVG produit)                                        | P1       | ✅     | `history` dans le retour avec iter, valid, errors                                                                                                                                  |
| 2.4     | Implémenter un ajustement paramétrique après échec                                           | P1       | 🔶     | `_adjust()` crée des hints mais `generate_icon()` ne les lit pas — no-op (⚠️ **BUG B4**)                                                                                           |
| 2.5     | Ajouter un scoring de fidélité sémantique                                                    | P2       | ⬜     | Mesurer si le SVG correspond au concept                                                                                                                                            |
| 2.6     | Ajouter un scoring de cohérence de collection                                                | P2       | ✅     | `collection_consistency()` avec score stroke + densité via `_homogeneity()`                                                                                                        |
| **2.7** | **[BUG B4] Connecter `_adjust()` au generator : les hints doivent influencer la génération** | **P1**   | ⬜     | **Actuellement `_adjust()` set des hints mais `generate_icon()` les ignore. Il faut que le generator lise les hints pour ajuster : réduire taille (shrink), forcer palette, etc.** |

---

## Phase 3 — Génération intelligente (P1)

> Objectif : le système peut produire des icônes pour n'importe quel concept.

| #   | Tâche                                                                           | Priorité | Statut | Notes                                                                         |
| --- | ------------------------------------------------------------------------------- | -------- | ------ | ----------------------------------------------------------------------------- |
| 3.1 | Analyser les 5 SVG de référence pour extraire le vocabulaire formel             | P1       | ✅     | `parse_references()` extrait couleurs, formes, stroke-widths, viewBox par SVG |
| 3.2 | Créer une bibliothèque de formes de base (path, circle, rect, etc.)             | P1       | ⬜     | Composants réutilisables                                                      |
| 3.3 | Implémenter un système de DSL graphique intermédiaire (JSON → SVG)              | P1       | ⬜     | Représentation structurée avant conversion                                    |
| 3.4 | Implémenter un mapping concept → formes sémantiques                             | P1       | ⬜     | Ex: "sécurité" → bouclier, cadenas, clé                                       |
| 3.5 | Implémenter un système de composition (superposition, alignement)               | P1       | ⬜     | Assembler les formes en icône cohérente                                       |
| 3.6 | Tester avec des concepts secrets maison (ex: "musique", "cuisine", "transport") | P1       | ⬜     | Vérifier la généralisation                                                    |
| 3.7 | Tester avec une charte variante (nouvelles couleurs, nouveaux SVG)              | P1       | ✅     | Test `test_generalization_to_unknown_charte` couvre ce cas                    |

---

## Phase 4 — Cohérence de collection (P1)

> Objectif : les icônes d'une même collection partagent un langage visuel commun.

| #   | Tâche                                                                                               | Priorité | Statut | Notes                                                                       |
| --- | --------------------------------------------------------------------------------------------------- | -------- | ------ | --------------------------------------------------------------------------- |
| 4.1 | Extraire les métriques de chaque icône (couleurs utilisées, nombre de formes, surface jaune/orange) | P1       | ✅     | `measure_svg()` extrait strokes, primitives, shape_vocab                    |
| 4.2 | Calculer un score de cohérence intra-collection                                                     | P1       | ✅     | `collection_consistency()` avec `_homogeneity()` (coefficient de variation) |
| 4.3 | Ajuster les icônes pour réduire la variance                                                         | P2       | ⬜     | Normaliser les proportions                                                  |
| 4.4 | Valider la cohérence visuellement (comparaison par paires)                                          | P2       | ⬜     | Test humain                                                                 |

---

## Phase 5 — Validation déterministe complète (P1)

> Objectif : passer toutes les vérifications du validateur du jury.

| #   | Tâche                                                            | Priorité | Statut | Notes                                                                             |
| --- | ---------------------------------------------------------------- | -------- | ------ | --------------------------------------------------------------------------------- |
| 5.1 | Installer Inkscape et tester la validation complète              | P1       | ⬜     | `python tools/validate_svg.py outputs/ --requests benchmark/public-concepts.json` |
| 5.2 | Corriger les SVG qui dépassent la zone utile                     | P1       | ⬜     | Vérifier x=5..59, y=5..59                                                         |
| 5.3 | Tester avec un profil personnalisé (`--profile`)                 | P2       | ⬜     | Simuler une charte secrète                                                        |
| 5.4 | Valider que le validateur fonctionne sans profil (défaut public) | P1       | ⬜     | Cas du jury                                                                       |
| 5.5 | Générer un rapport JSON complet (`--json`)                       | P2       | ⬜     | Pour documentation                                                                |

---

## Phase 6 — Documentation et livrables (P1)

> Objectif : README complet et conforme au canevas.

| #    | Tâche                                                       | Priorité | Statut | Notes                                          |
| ---- | ----------------------------------------------------------- | -------- | ------ | ---------------------------------------------- |
| 6.1  | Compléter la section "Problématique" du README              | P1       | ⬜     | 2-3 phrases                                    |
| 6.2  | Compléter la section "Approche adoptée"                     | P1       | ⬜     | Chaîne complète                                |
| 6.3  | Compléter la section "Résultats obtenus"                    | P1       | ⬜     | Scores sur concepts publics                    |
| 6.4  | Compléter la section "Installation"                         | P1       | ⬜     | Prérequis + commandes                          |
| 6.5  | Compléter la section "Exécution"                            | P1       | ⬜     | Exemple reproductible                          |
| 6.6  | Compléter la section "Architecture du système"              | P1       | ⬜     | Schéma des composants                          |
| 6.7  | Compléter la section "Formalisation de la charte graphique" | P1       | ⬜     | Palette, géométrie, traits, etc.               |
| 6.8  | Compléter la section "Stratégie de génération"              | P1       | ⬜     | Concept → SVG                                  |
| 6.9  | Compléter la section "Évaluation et boucle d'amélioration"  | P1       | ⬜     | Contraintes hard/soft, cohérence, boucle G-E-R |
| 6.10 | Compléter la section "Résultats et expériences"             | P1       | ⬜     | Tous les tests requis                          |
| 6.11 | Compléter la section "Manifeste de remise"                  | P1       | ⬜     | `manifest.json` conforme                       |
| 6.12 | Compléter la section "Vidéo de présentation"                | P1       | ⬜     | 3-5 minutes                                    |
| 6.13 | Compléter la section "Transparence sur les outils IA"       | P1       | ⬜     | Déclarer tous les outils utilisés              |
| 6.14 | Compléter la section "Contributions individuelles"          | P1       | ⬜     | Rôles de chaque membre                         |
| 6.15 | Compléter la section "Limites et améliorations"             | P2       | ⬜     |                                                |
| 6.16 | Compléter la section "Licence et propriété"                 | P2       | ⬜     |                                                |
| 6.17 | Remplir `manifest.json` avec les vraies infos d'équipe      | P1       | ⬜     | Min 2 membres                                  |

---

## Phase 7 — Manifeste et soumission (P0)

> Objectif : tout est prêt pour le commit final.

| #   | Tâche                                                                                  | Priorité | Statut | Notes                                                                                |
| --- | -------------------------------------------------------------------------------------- | -------- | ------ | ------------------------------------------------------------------------------------ |
| 7.1 | Vérifier que `manifest.json` est conforme à `submission-template/manifest.schema.json` | P0       | ⬜     |                                                                                      |
| 7.2 | Vérifier que tous les SVG sont dans `outputs/public/`                                  | P0       | ⬜     | Un `<id>.svg` par requête                                                            |
| 7.3 | Vérifier que `generate.py` fonctionne depuis la racine du dépôt                        | P0       | ⬜     | `python generate.py --input benchmark/public-concepts.json --output outputs/public/` |
| 7.4 | Vérifier que `run.sh` fonctionne                                                       | P0       | ⬜     | `bash run.sh --input ... --output ...`                                               |
| 7.5 | Vérifier que le dépôt cloné dans un dossier vierge produit les bons SVG                | P0       | ⬜     | Test de reproductibilité                                                             |
| 7.6 | Fixer les graines aléatoires si applicable                                             | P0       | ⬜     | Reproductibilité                                                                     |
| 7.7 | Supprimer les fichiers `.pyc` et `__pycache__`                                         | P1       | ✅     | Retirés du tracking git + .gitignore configuré                                       |
| 7.8 | Ajouter un `.gitignore` propre                                                         | P1       | ✅     | Exclut `.venv/`, `__pycache__/`, `*.pyc`, `.env`, etc.                               |

---

## Phase 8 — Vidéo de présentation (P1)

> Objectif : vidéo de 3-5 minutes couvrant tous les points requis.

| #   | Tâche                                              | Priorité | Statut | Notes |
| --- | -------------------------------------------------- | -------- | ------ | ----- |
| 8.1 | Filmer la présentation de l'équipe                 | P1       | ⬜     |       |
| 8.2 | Présenter le langage visuel extrait                | P1       | ⬜     |       |
| 8.3 | Présenter l'architecture du système                | P1       | ⬜     |       |
| 8.4 | Présenter la stratégie d'évaluation                | P1       | ⬜     |       |
| 8.5 | Montrer un échec instructif                        | P1       | ⬜     |       |
| 8.6 | Expliquer ce qu'on ferait avec une journée de plus | P1       | ⬜     |       |
| 8.7 | Vérifier le lien de la vidéo                       | P1       | ⬜     |       |

---

## Résumé par priorité

| Priorité  | Total  | Fait   | Reste  |
| --------- | ------ | ------ | ------ |
| P0 | 21 | 11 | 10 |
| P1        | 33     | 11     | 22     |
| P2        | 9      | 0      | 9      |
| P3        | 0      | 0      | 0      |
| **Total** | **63** | **22** | **41** |

---

## Jalon critique

```
08h00 - 09h00  → Phase 1 (chaîne minimale)
09h00 - 10h30  → Phase 3 (génération intelligente)
10h30 - 11h30  → Phase 5 (validation déterministe)
11h30 - 13h00  → Phase 2 + Phase 4 (boucle G-E-R + cohérence)
13h00 - 14h30  → Phase 6 (documentation README)
14h30 - 15h15  → Phase 7 (manifeste + soumission)
15h15 - 15h45  → Phase 8 (vidéo)
15h45 - 16h00  → Vérifications finales + dernier commit
```
