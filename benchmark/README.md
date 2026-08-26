# Contrat du benchmark

## Entrée

Le système reçoit un fichier JSON conforme à `request.schema.json`.

Chaque requête contient :

- `id` : identifiant stable utilisé comme nom de fichier ;
- `concept` : concept principal à représenter ;
- `context` : précision sémantique facultative ;
- `keywords` : indices facultatifs, jamais des instructions graphiques exhaustives.

## Sortie

Pour chaque requête, créer exactement un SVG :

```text
outputs/<id>.svg
```

Le SVG doit être autonome et respecter la version de `brand-guidelines.md` présente au moment de l’exécution, ainsi que les références présentes dans `references/`.

## Exemple

```bash
python generate.py \
  --input benchmark/public-concepts.json \
  --output outputs/public/
```

Le jury utilisera le même contrat avec un fichier de concepts non communiqué aux équipes. Il remplacera également `brand-guidelines.md` et `references/` aux mêmes emplacements avant certaines exécutions.

L’adaptateur doit donc lire ces ressources à l’exécution. Une copie de palette, de `viewBox`, de largeur de trait ou de règles stylistiques intégrée au code ne respecte pas le contrat.

## Reproductibilité

Si la méthode est stochastique, le système doit accepter ou documenter une graine. Le jury peut exécuter plusieurs générations pour observer la stabilité du langage visuel.
