# Validateur SVG paramétrable

Le contrôle complet utilise **Inkscape**, logiciel libre, pour mesurer l’emprise visuelle réelle, contours compris. Sans option supplémentaire, ce validateur applique uniquement le profil de la charte publique de développement.

## Validation d’un dossier

```bash
python tools/validate_svg.py outputs/public/ \
  --requests benchmark/public-concepts.json
```

Le validateur contrôle notamment :

- XML et `viewBox` ;
- couleurs explicites et palette ;
- maximum quatre couleurs ;
- attributs de contour ;
- scripts, CSS, liens, images et effets interdits ;
- zone utile stricte `5…59` ;
- nombre et noms des fichiers attendus.

Réussir ce contrôle ne démontre pas l’adaptation à une nouvelle charte. Lors de l’évaluation, le jury utilisera le même outil avec un profil confidentiel via `--profile`.

Vous pouvez créer votre propre profil de contrôle pour tester une charte variante :

```bash
python tools/validate_svg.py outputs/variant/ \
  --requests benchmark/public-concepts.json \
  --profile chemin/vers/votre-profil.json
```

## Contrôle préliminaire sans Inkscape

```bash
python tools/validate_svg.py outputs/public/ --xml-only
```

Ce mode ignore la zone utile et ne constitue donc pas une validation finale.
