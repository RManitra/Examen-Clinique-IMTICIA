# Barème public — 100 points

| Dimension | Points | Principaux éléments observés |
|---|---:|---|
| Conformité technique | 20 | validation déterministe sous la charte de remplacement |
| Fidélité sémantique et lisibilité | 20 | concept identifiable et lisibilité à petite taille |
| Généralisation aux concepts secrets | 15 | qualité sur les concepts secrets et dégradation contrôlée |
| Généralisation à une charte secrète | 10 | extraction à l’exécution et fidélité au nouveau langage visuel |
| Architecture et boucle d’évaluation | 10 | conception, mesures et boucle d’amélioration |
| Cohérence de collection | 10 | langage visuel commun au set complet |
| Qualité du code et reproductibilité | 5 | exécution, documentation et traçabilité |
| Présentation vidéo | 10 | clarté, synthèse et analyse critique en 3 à 5 minutes |
| **Total** | **100** | |

## Règles importantes

- Un SVG qui échoue aux contrôles déterministes est compté comme non produit pour le concept concerné.
- Une collection dessinée manuellement sans système génératif automatisé est hors sujet.
- L’utilisation d’une API payante n’accorde aucun point supplémentaire.
- La cohérence est évaluée sur le set complet, et non comme simple moyenne d’icônes indépendantes.
- Les quatre premiers critères sont établis après exécution du dépôt sur des concepts secrets et avec une charte de remplacement.
- Le système doit lire `brand-guidelines.md` et `references/` à chaque exécution. Les valeurs figées dans le code constituent un échec de généralisation à la charte.

## Protocole public des deux axes de généralisation

Le jury utilise une matrice 2 × 2 sans modifier le code :

| Code | Concepts | Charte et références | Fonction |
|---|---|---|---|
| PP | publics | publiques | référence de développement |
| PS | publics | secrètes | contrôle sous la charte de remplacement |
| SP | secrets | publiques | contrôle sur les concepts secrets |
| SS | secrets | secrètes | test final combiné |

Le scénario SS sert aussi à établir les scores de conformité technique et de fidélité sémantique. Les fichiers exacts de la charte secrète et les concepts secrets restent confidentiels.

## Généralisation aux concepts secrets

Pour PS et SS, on calcule :

$$
Q_X = 0{,}5\,T_X + 0{,}5\,S_X,
$$

où $T_X$ est la conformité technique et $S_X$ la fidélité sémantique et la lisibilité, normalisées dans $[0,1]$.

Avec $D_c = \max(0, Q_{PS} - Q_{SS})$, le score sur 15 est :

$$
G_c = 15\,Q_{SS}\,(1 - 0{,}5D_c).
$$

## Généralisation à une charte secrète

Pour SP et SS, on calcule :

$$
R_X = 0{,}5\,T_X + 0{,}5\,V_X,
$$

où $V_X$ mesure la fidélité stylistique et la cohérence avec la charte active, normalisées dans $[0,1]$.

Avec $D_b = \max(0, R_{SP} - R_{SS})$, le score sur 10 est :

$$
G_b = 10\,R_{SS}\,(1 - 0{,}5D_b).
$$

Ces formules combinent la qualité sur la condition secrète et l’écart avec la condition de référence. Un système médiocre dans les deux conditions ne peut donc pas obtenir un bon score grâce à un écart artificiellement faible.

## Indicateurs possibles

Le jury et les équipes peuvent combiner contrôles XML/SVG, statistiques de palette et de complexité, rendu à plusieurs tailles, évaluation humaine en aveugle, modèle vision-langage local ou accessible gratuitement, comparaison par paires et métriques de cohérence intra-set.
