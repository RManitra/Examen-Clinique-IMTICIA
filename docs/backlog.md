# Backlog produit - IconForge AI

## 1. Contexte du projet

Le projet IconForge AI vise à produire automatiquement une famille cohérente d’icônes SVG à partir de concepts exprimés en langage naturel. L’objectif principal est de générer des symboles visuellement harmonisés, conformes à une charte graphique précise, tout en restant techniquement validés et reproductibles.

Le système s’appuie sur trois piliers essentiels :

- la lecture dynamique des règles d’une charte graphique (palette, zone utile, viewBox, épaisseur de trait, marges, formes, finitions);
- l’analyse des fichiers SVG de référence du dossier `references/`;
- une boucle de génération, validation et raffinement appelée Generate-Evaluate-Refine.

Le projet est présenté comme un hackathon de fin d’études et repose sur une logique d’AI Engineering orientée produit, avec une forte exigence de qualité visuelle et de validation déterministe.

---

## 2. Problématique métier

La génération d’icônes individuelles via intelligence artificielle présente plusieurs risques :

- incohérence d’épaisseur de trait entre icônes;
- dérive chromatique dans la palette;
- variance de proportions visuelles et de mise à l’échelle;
- non-respect des contraintes de composition et d’espaces vides;
- ICônes non conformes aux exigences techniques du format SVG.

Le vrai défi n’est pas seulement de générer des icônes, mais de garantir une cohérence d’ensemble sur une collection complète, en respectant une identité visuelle unique.

---

## 3. Vision produit

Créer un système autonome capable de :

1. lire et interpréter une charte graphique fournie au moment de l’exécution;
2. synthétiser une famille cohérente d’icônes SVG à partir d’un ensemble de concepts;
3. valider automatiquement la conformité structurale et visuelle;
4. corriger les défauts par une boucle itérative de raffinement ;
5. produire des résultats exploitables en production ou pour une validation académique.

---

## 4. Objectifs du projet

### Objectifs fonctionnels

- Générer plusieurs icônes SVG cohérentes à partir de concepts texte.
- Extraire automatiquement les contraintes graphiques depuis `brand-guidelines.md`.
- Analyser les références existantes pour inférer les règles visuelles communes.
- Respecter le standard technique du projet, notamment :
  - `viewBox = 0 0 64 64` ;
  - zone utile restreinte à `x=5..59, y=5..59` ;
  - palette très limitée ;
  - cohérence des traits, des formes et des proportions.

### Objectifs non fonctionnels

- Fiabilité de la génération.
- Validation déterministe et reproductible.
- Robustesse face à des écarts visuels ou des erreurs de composition.
- Traçabilité des règles appliquées.
- facilité d’ajout de nouveaux concepts et d’évolution de la charte.

---

## 5. Acteurs et utilisateurs

### 5.1 Utilisateur final / demandeur

- souhaite obtenir une famille d’icônes cohérente et prêtes à l’emploi ;
- attend des résultats conformes aux normes visuelles et techniques.

### 5.2 Développeur / AI Engineer

- conçoit le pipeline de génération ;
- gère l’analyse de la charte et des références ;
- implémente et ajuste le moteur de validation.

### 5.3 Validateur technique

- vérifie la conformité SVG déterministe via un script de validation ;
- détecte les écarts par rapport aux contraintes.

---

## 6. Périmètre fonctionnel du produit

### In

- fichier de charte visuelle (`brand-guidelines.md`);
- dossiers de références SVG ;
- concepts d’icônes sous forme de JSON ou autres structures de données ;
- exigences de benchmark et schéma de validation.

### Out

- fichiers SVG individuels générés ;
- famille cohérente d’icônes ;
- validation technique et visuelle ;
- résultats de remédiation ou de raffinement.

---

## 7. Règles métier et contraintes techniques

Le projet impose plusieurs exigences strictes :

- respect absolu du `viewBox` ;
- occupation de la zone utile dans des limites précises ;
- palette limitée et maîtrisée : Jaune, Orange, Encre sombre, Blanc ;
- contrôle des lignes et épaisseurs de traits ;
- conformité avec la structure SVG attendue ;
- génération d’icônes de qualité visuelle uniforme.

Ces contraintes doivent être appliquées dynamiquement, sans codage figé pour chaque icône.

---

## 8. Architecture fonctionnelle prévue

Le système s’organise autour des composants suivants :

- `brand-guidelines.md` : source des règles de design ;
- `references/` : fichiers SVG utilisés comme référence visuelle ;
- `src/parser.py` : extraction des contraintes graphiques ;
- `src/generator.py` : génération de la structure SVG ;
- `src/validator_bridge.py` : interface de validation déterministe ;
- `src/reflector.py` : boucle de correction et d’amélioration ;
- `generate.py` : orchestrateur principal ;
- `tools/validate_svg.py` : validation strictement déterministe des SVG ;
- `benchmark/public-concepts.json` : jeux de concepts publics.

---

## 9. Épopées et backlog fonctionnel

## Épique 1 - Mise en place du projet et des fondations

### US-01 : Initialiser le projet de génération d’icônes

- Type : fonctionnel
- Priorité : Haute
- Estimation : 3 points

Description :
Le système doit être initialisé avec la structure du projet, les dépendances et les fichiers de configuration nécessaires pour générer des icônes SVG à partir d’un concept texte.

Critères d’acceptation :
- le dépôt contient la structure attendue ;
- les dépendances Python sont listées ;
- le script principal peut être exécuté ;
- le projet est documenté de manière minimale mais exploitable.

Sous-tâches :
- créer l’arborescence du projet ;
- ajouter les dépendances ;
- configurer l’exécution ;
- vérifier le lancement du pipeline.

---

### US-02 : Documenter la charte visuelle et les contraintes de production

- Type : fonctionnel / documentation
- Priorité : Haute
- Estimation : 2 points

Description :
Le projet doit formaliser la charte graphique, en spécifiant les couleurs, l’échelle, le viewBox, les marges et les règles d’usage.

Critères d’acceptation :
- le document de charte est exploitable par un script ;
- les règles sont lisibles et structurées ;
- les contraintes sont cohérentes avec les références.

Sous-tâches :
- lire la charte graphique ;
- identifier les éléments structurants ;
- définir les paramètres de génération ;
- vérifier la compatibilité avec les références.

---

## Épique 2 - Analyse dynamique des règles visuelles

### US-03 : Extraire les règles graphiques depuis la charte

- Type : fonctionnel
- Priorité : Haute
- Estimation : 5 points

Description :
Le système doit pouvoir lire une charte graphique externe et en extraire les éléments importants : palette, viewBox, zone utile, marges, épaisseur de trait, styles, finitions.

Critères d’acceptation :
- les règles sont détectées automatiquement ;
- aucun paramètre n’est en dur dans le code pour les concepts publics ;
- les données extraites sont utilisables pour générer les icônes.

Sous-tâches :
- parser le document de charte ;
- normaliser les règles ;
- construire un modèle de contraintes ;
- valider le modèle par rapport aux références.

---

### US-04 : Déduire les paramètres visuels à partir des icônes de référence

- Type : fonctionnel
- Priorité : Haute
- Estimation : 5 points

Description :
Les fichiers SVG de référence doivent servir d’entrée pour inférer la cohérence visuelle commune de la famille d’icônes.

Critères d’acceptation :
- les références sont analysées automatiquement ;
- la palette et les traits sont identifiés ;
- les proportions et dimensions sont interprétables ;
- les paramètres dérivés sont typés et exploités par le moteur de génération.

Sous-tâches :
- lire les SVG de référence ;
- extraire les attributs clés ;
- calculer des statistiques visuelles ;
- comparer les références entre elles.

---

## Épique 3 - Génération de la famille d’icônes SVG

### US-05 : Produire une structure SVG conforme

- Type : fonctionnel
- Priorité : Haute
- Estimation : 8 points

Description :
Le générateur doit produire des SVG respectant la structure attendue, notamment le `viewBox`, les limites de composition et les conventions de style de la charte.

Critères d’acceptation :
- chaque SVG contient les attributs requis ;
- les dimensions sont conformes ;
- les éléments vectoriels sont bien structurés ;
- le rendu est cohérent avec les références.

Sous-tâches :
- créer la structure SVG de base ;
- définir les éléments visuels ;
- injecter les règles de style ;
- générer un lot d’icônes test.

---

### US-06 : Générer des icônes cohérentes à partir des concepts

- Type : fonctionnel
- Priorité : Haute
- Estimation : 8 points

Description :
Le système doit transformer un concept exprimé en langage naturel en une représentation visuelle compatible avec la charte de marque.

Critères d’acceptation :
- chaque concept produit une icône unique et cohérente ;
- la forme correspond au sens du concept ;
- les proportions sont alignées avec la charte ;
- les couleurs restent maîtrisées.

Sous-tâches :
- normaliser les concepts ;
- mapper le concept vers un schéma visuel ;
- construire les formes vectorielles ;
- appliquer la palette correcte.

---

### US-07 : Assurer l’harmonie visuelle de la collection

- Type : fonctionnel / qualité
- Priorité : Haute
- Estimation : 5 points

Description :
La famille complète d’icônes doit présenter un langage visuel cohérent et harmonieux, sans rupture de style entre les éléments.

Critères d’acceptation :
- les épaisseurs de trait restent cohérentes ;
- les couleurs sont conformes à la palette ;
- les proportions entre icônes sont cohérentes ;
- les formes sont homogènes malgré la diversité des concepts.

Sous-tâches :
- comparer les résultats entre icônes ;
- normaliser les attributs visuels ;
- corriger les écarts majeurs ;
- établir un barème de cohérence visuelle.

---

## Épique 4 - Validation déterministe des SVG

### US-08 : Implémenter un validateur SVG strict

- Type : technique / qualité
- Priorité : Haute
- Estimation : 8 points

Description :
Le projet doit disposer d’un moteur de validation technique capable de vérifier la conformité des fichiers SVG produits aux règles imposées.

Critères d’acceptation :
- la validation est déterministe ;
- les erreurs de structure sont détectées ;
- la conformité visuelle est contrôlée par des règles explicites ;
- la commande de validation fonctionne sur un dossier complet.

Sous-tâches :
- définir les règles de validation ;
- implémenter le validateur ;
- utiliser les benchmarks pour tester les cas ;
- corriger les écarts de conformité.

---

### US-09 : Vérifier la conformité des dimensions et de la zone utile

- Type : technique
- Priorité : Haute
- Estimation : 3 points

Description :
Le validateur doit s’assurer que le `viewBox` et la zone utile répondent précisément aux exigences du projet.

Critères d’acceptation :
- `0 0 64 64` est respecté ;
- `x=5..59, y=5..59` est respecté ;
- les éléments visuels restent dans les limites autorisées ;
- des échecs explicites sont renvoyés si la zone utile est violée.

Sous-tâches :
- intégrer les contrôles de zone utile ;
- ajouter des messages de diagnostic ;
- valider sur des cas conformes et non conformes.

---

### US-10 : Contrôler la palette et les styles graphiques

- Type : technique / qualité
- Priorité : Haute
- Estimation : 3 points

Description :
Un moteur de validation doit vérifier que les couleurs, les traits et les styles respectent strictement la palette et les conventions graphiques.

Critères d’acceptation :
- la palette autorisée est vérifiée ;
- les éléments de même catégorie utilisent le bon style ;
- les couleurs inconsistantes sont signalées ;
- l’écart visuel est détecté avant publication.

Sous-tâches :
- comparer les couleurs utilisées aux règles de la charte ;
- vérifier les épaisseurs ;
- détecter les écarts majeurs de style.

---

## Épique 5 - Boucle Generate-Evaluate-Refine

### US-11 : Implémenter la boucle d’itération de correction

- Type : fonctionnel / technique
- Priorité : Haute
- Estimation : 8 points

Description :
Le système doit produire une première version, la valider, identifier les défauts et appliquer un raffinement jusqu’à ce que le résultat soit conforme.

Critères d’acceptation :
- la boucle est executable en séquence ;
- chaque itération améliore le SVG ;
- le nombre d’itérations est maîtrisé ;
- le résultat final est conforme sans intervention manuelle.

Sous-tâches :
- définir le cycle de génération ;
- créer une phase d’évaluation ;
- mettre en place le mécanisme de correction ;
- limiter les boucles inutiles.

---

### US-12 : Corriger automatiquement les défauts de structure

- Type : technique
- Priorité : Moyenne
- Estimation : 5 points

Description :
Les défauts les plus fréquents doivent être corrigés automatiquement après validation.

Critères d’acceptation :
- les erreurs de trait sont corrigées ;
- les problèmes de zone utile sont réduits ;
- les éléments visuellement incohérents sont ajustés ;
- la génération reste stable sur plusieurs exécutions.

Sous-tâches :
- identifier les défauts récurrents ;
- définir des règles de correction ;
- enchaîner les corrections de manière séquentielle ;
- vérifier l’amélioration du score de conformité.

---

### US-13 : Mesurer la qualité de la boucle de refinement

- Type : qualité / monitoring
- Priorité : Moyenne
- Estimation : 3 points

Description :
Le système doit fournir des indicateurs qui permettent de mesurer l’efficacité du raffinement.

Critères d’acceptation :
- des scores ou des diagnostics sont calculés ;
- l’évolution de la conformité est visible ;
- les boucles de correction peuvent être analysées.

Sous-tâches :
- définir un indicateur de conformité ;
- enregistrer les résultats d’évaluation ;
- comparer les versions successives.

---

## Épique 6 - Benchmarks, validation publique et démonstration

### US-14 : Exécuter le jeu de concepts publics

- Type : fonctionnel
- Priorité : Haute
- Estimation : 3 points

Description :
Le système doit être testé sur les concepts publics du benchmark afin de montrer sa capacité à générer des icônes conformes dans un cas représentatif.

Critères d’acceptation :
- les concepts du benchmark sont traités ;
- les SVG générés sont validés ;
- le taux de conformité est calculé ;
- la sortie est exploitable dans le dossier d’output.

Sous-tâches :
- préparer la liste de concepts ;
- exécuter le pipeline ;
- lancer la validation ;
- corriger les écarts observés.

---

### US-15 : Garantir 100 % de conformité déterministe sur les concepts publics

- Type : qualité / produit
- Priorité : Haute
- Estimation : 5 points

Description :
Le projet prétend à un niveau de conformité élevé et déterministe, et doit démontrer cette capacité sur les cas publics.

Critères d’acceptation :
- 100 % des concepts publics passent la validation ;
- les erreurs sont nulles ou réduites à zéro ;
- la famille générée est stable et cohérente ;
- les résultats sont reproductibles.

Sous-tâches :
- identifier les causes de non-conformité ;
- corriger les défauts récurrents ;
- relancer les validations ;
- documenter le niveau de qualité final.

---

## 10. Backlog technique détaillé

### Tâches transverses

#### BT-01 - Structuration du pipeline

- orchestrer `generate.py` ;
- définir la séquence d’exécution ;
- contrôler les entrées et sorties ;
- préparer le traitement de lots.

#### BT-02 - Gestion des fichiers de référence

- lire les SVG de référence ;
- standardiser l’analyse ;
- détecter les règles communes.

#### BT-03 - Extraction de données visuelles

- parser la charte ;
- calculer palette et marges ;
- repérer les conventions de trait et de composition.

#### BT-04 - Génération paramétrique

- créer des primitives visuelles réutilisables ;
- transformer les concepts en schéma visuel ;
- faire évoluer la génération selon les contraintes dynamiques.

#### BT-05 - Contrôle des sorties SVG

- vérifier les attributs XML/SVG ;
- valider le `viewBox`, la palette, la zone utile ;
- contrôler le rendu final.

#### BT-06 - Résilience et amélioration

- corriger automatiquement les défauts ;
- éviter les boucles infinies ;
- limiter les retouches inutiles.

---

## 11. User stories priorisées

### Priorité 1 - Critiques

- En tant que demandeur, je veux générer une famille d’icônes cohérente afin d’avoir une identité visuelle uniforme.
- En tant que développeur, je veux extraire dynamiquement la charte afin d’éviter de coder en dur les contraintes.
- En tant que validateur, je veux obtenir une conformité déterministe afin de garantir la qualité technique.
- En tant qu’utilisateur, je veux que les icônes respectent strictement les limites du canvas afin d’éviter les déformations visuelles.

### Priorité 2 - Importantes

- En tant que product owner, je veux une boucle de correction automatisée afin de réduire les écarts visuels.
- En tant que développeur, je veux analyser les références afin d’inférer les bonnes conventions de design.
- En tant que testeur, je veux valider le benchmark public afin de confirmer la robustesse du système.

### Priorité 3 - Complémentaires

- En tant que mainteneur, je veux documenter le code afin de faciliter la reprise et l’évolution.
- En tant que chef de projet, je veux suivre les performances de génération afin de vérifier la qualité produit.

---

## 12. Critères de finition (Definition of Done)

Un item de backlog est considéré terminé si :

- la fonctionnalité est implémentée et intégrée au pipeline ;
- la sortie produit des fichiers SVG conformes ;
- la validation passe avec succès sur les cas de test pertinents ;
- les contraintes visuelles et techniques sont respectées ;
- le comportement est documenté de manière claire ;
- le résultat est reproductible et ne dépend pas de données non maîtrisées.

---

## 13. Risques et points de vigilance

### Risques fonctionnels

- mauvaises interprétations de la charte visuelle ;
- incohérence entre les références et la charte ;
- génération d’icônes trop éloignées du concept initial ;
- difficulté à maintenir une cohérence visuelle sur un grand ensemble.

### Risques techniques

- validation trop stricte, générant des faux négatifs ;
- génération de SVG non standard ;
- manque de robustesse de la boucle d’itération ;
- difficulté d’automatisation sur des cas complexes.

### Risques de qualité

- dérive chromatique ;
- variation d’épaisseur de trait ;
- erreurs dans la composition ou la ratio visuel ;
- résultats non reproductibles d’une exécution à l’autre.

---

## 14. Plan de livraison proposé

### Sprint 1 - Fondations et analyse

- mise en place du projet ;
- étude de la charte graphique ;
- extraction des contraintes ;
- analyse des références ;
- préparation des règles de validation.

### Sprint 2 - Génération et contrôle

- implémentation du générateur SVG ;
- création des structures vectorielles ;
- validation technique des sorties ;
- correction des erreurs de structure.

### Sprint 3 - Raffinement et qualité

- boucle Generate-Evaluate-Refine ;
- amélioration de la cohérence visuelle ;
- ajustement des palettes et traits ;
- validation sur les concepts publics.

### Sprint 4 - Stabilisation et remise

- tests finaux ;
- documentation finale ;
- contrôle du niveau de conformité ;
- préparation de la remise et du manifeste.

---

## 15. Backlog synthétique (tableau de priorisation)

| ID | Titre | Priorité | Estimation | Type |
|---|---|---:|---:|---|
| US-01 | Initialiser le projet | Haute | 3 | Fonctionnel |
| US-02 | Documenter la charte visuelle | Haute | 2 | Documentation |
| US-03 | Extraire les règles graphiques | Haute | 5 | Fonctionnel |
| US-04 | Analyser les références SVG | Haute | 5 | Fonctionnel |
| US-05 | Produire une structure SVG conforme | Haute | 8 | Fonctionnel |
| US-06 | Générer des icônes cohérentes | Haute | 8 | Fonctionnel |
| US-07 | Assurer l’harmonie visuelle | Haute | 5 | Qualité |
| US-08 | Implémenter le validateur SVG | Haute | 8 | Technique |
| US-09 | Vérifier viewBox et zone utile | Haute | 3 | Technique |
| US-10 | Contrôler la palette et styles | Haute | 3 | Technique |
| US-11 | Implémenter la boucle Generate-Evaluate-Refine | Haute | 8 | Fonctionnel |
| US-12 | Corriger les défauts automatiquement | Moyenne | 5 | Technique |
| US-13 | Mesurer la qualité du raffinement | Moyenne | 3 | Qualité |
| US-14 | Exécuter le benchmark public | Haute | 3 | Fonctionnel |
| US-15 | Garantir 100 % de conformité | Haute | 5 | Qualité |

---

## 16. Conclusion

Le backlog montre que le projet IconForge AI est avant tout un projet de génération visuelle assistée par IA, mais avec une exigence de discipline technique forte. Son cœur de valeur réside dans la capacité à combiner :

- extraction dynamique des contraintes,
- interprétation des références visuelles,
- génération SVG structurée,
- validation déterministe,
- auto-correction et raffinement itératif.

Le produit final ne doit pas se limiter à la génération d’une icône isolée, mais à une famille cohérente, homogène, conforme et reproductible, répondant à une charte de marque précise.

---

## 17. Recommandation finale

Pour une livraison performante, il est conseillé de traiter le projet en priorité selon l’ordre suivant :

1. charte visuelle + extraction de règles ;
2. validation déterministe ;
3. génération SVG conforme ;
4. boucle de raffinage ;
5. validation sur benchmark public ;
6. documentation et remise finale.

Cela permet de sécuriser le socle technique avant de viser la qualité visuelle, qui est le cœur du projet.
