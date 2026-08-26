from pathlib import Path

from src.parser import BrandParser

ROOT = Path(__file__).resolve().parent.parent


def test_parse_guidelines():
    parser = BrandParser(ROOT / "brand-guidelines.md", ROOT / "references")
    guidelines = parser.parse_guidelines()

    assert guidelines["allowed_colors"]
    assert guidelines["view_box"]
    assert guidelines["safe_zone"] is not None


def test_parse_references():
    parser = BrandParser(ROOT / "brand-guidelines.md", ROOT / "references")
    references = parser.parse_references()

    assert len(references) > 0
    for reference in references:
        assert "filename" in reference
        assert "colors" in reference
        assert "shape_count" in reference


def test_full_analysis():
    parser = BrandParser(ROOT / "brand-guidelines.md", ROOT / "references")
    result = parser.analyze()

    assert "guidelines" in result
    assert "references" in result
    assert "reference_summary" in result


def test_generalization_to_unknown_charte(tmp_path):
    variant = tmp_path / "brand-guidelines-variant.md"
    variant.write_text(
        """# Charte variante (simulateur de charte secrète)

## Palette
- #0000FF
- #FF0000
- #000000

maximum 3 couleurs visibles

## Géométrie
viewBox="0 0 128 128"

Marge de sécurité : 10px

## Traits
stroke-width="4"
stroke-linecap="square"
stroke-linejoin="bevel"

## Éléments interdits
- filter
- text
""",
        encoding="utf-8",
    )

    parser = BrandParser(variant, ROOT / "references")
    guidelines = parser.parse_guidelines()

    assert guidelines["allowed_colors"] == ["#000000", "#0000FF", "#FF0000"]
    assert guidelines["view_box"] == "0 0 128 128"
    assert guidelines["stroke_width"] == 4.0
    assert guidelines["stroke_linecap"] == "square"
    assert guidelines["stroke_linejoin"] == "bevel"
    assert guidelines["max_colors"] == 3
    assert guidelines["safe_zone"] == {
        "x_min": 10.0,
        "x_max": 118.0,
        "y_min": 10.0,
        "y_max": 118.0,
    }

def test_analyze_reconciles_stroke_width_from_references(tmp_path):
   
    # Valeur de référence calculée dynamiquement depuis vos VRAIS SVG,
    # jamais codée en dur : le test reste valable quel que soit le chiffre.
    ref_parser = BrandParser(ROOT / "brand-guidelines.md", ROOT / "references")
    ref_widths = ref_parser.summarize_references(ref_parser.parse_references())["stroke_widths"]
    assert len(ref_widths) == 1, "les références doivent partager UNE seule épaisseur"
    expected_width = ref_widths[0]

    guidelines_file = tmp_path / "brand-guidelines.md"
    guidelines_file.write_text(
        """# Charte (épaisseur qualitative uniquement, comme dans le vrai sujet)

## Palette
- #1F6F54

## Géométrie
viewBox="0 0 24 24"

## Traits
Le style impose une épaisseur optique stable, sans qu'un chiffre ne soit donné ici.

## Éléments interdits
- filter
- text
""",
        encoding="utf-8",
    )

    parser = BrandParser(guidelines_file, ROOT / "references")

    # Sans reconciliation : parse_guidelines() seul renvoie bien None (attendu).
    assert parser.parse_guidelines()["stroke_width"] is None

    # Avec reconciliation : analyze() va chercher dans les références.
    result = parser.analyze()
    assert result["guidelines"]["stroke_width"] == expected_width
    assert result["value_sources"]["stroke_width"] == "references"

def test_missing_guidelines_file_raises(tmp_path):
    parser = BrandParser(tmp_path / "does-not-exist.md", ROOT / "references")
    try:
        parser.parse_guidelines()
        assert False, "devait lever FileNotFoundError"
    except FileNotFoundError:
        pass