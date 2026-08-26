# tests/test_reflector.py
import pytest
from pathlib import Path
from src.reflector import ReflectorPipeline


class FakeValidator:
    """Renvoie des verdicts scriptés : [False, True] = échoue puis passe."""
    def __init__(self, verdicts):
        self.verdicts = list(verdicts)
        self.calls = 0
    def validate(self, file, xml_only=True):
        v = self.verdicts[min(self.calls, len(self.verdicts) - 1)]
        self.calls += 1
        return {"valid": v, "errors": [] if v else ["viewbox hors zone"], "warnings": []}


@pytest.fixture
def spec():
    return {"palette": ["#000"], "stroke_width": 2, "viewBox": "0 0 64 64"}


def test_refine_stops_when_valid(spec, tmp_path, monkeypatch):
    val = FakeValidator([False, False, True])   # valide à la 3e
    pipe = ReflectorPipeline(spec, val)
    # mock du générateur pour ne pas dépendre de Membre 3
    monkeypatch.setattr(pipe.generator, "generate_icon",
                        lambda req: '<svg xmlns="http://www.w3.org/2000/svg"/>')
    results = pipe.process_requests([{"id": "test", "concept": "x"}], tmp_path)
    assert results[0]["valid"]
    assert results[0]["iterations"] == 3


def test_refine_gives_up_after_max_iter(spec, tmp_path, monkeypatch):
    val = FakeValidator([False])   # toujours invalide
    pipe = ReflectorPipeline(spec, val, max_iter=5)
    monkeypatch.setattr(pipe.generator, "generate_icon",
                        lambda req: '<svg xmlns="http://www.w3.org/2000/svg"/>')
    results = pipe.process_requests([{"id": "test", "concept": "x"}], tmp_path)
    assert not results[0]["valid"]
    assert results[0]["iterations"] == 5   # jamais de boucle infinie


def test_consistency_identical_is_high(spec, tmp_path):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg">'
           '<path stroke-width="2" d="M0 0"/><circle stroke-width="2"/></svg>')
    paths = []
    for i in range(3):
        p = tmp_path / f"icon{i}.svg"
        p.write_text(svg)
        paths.append(p)
    pipe = ReflectorPipeline(spec, FakeValidator([True]))
    assert pipe.collection_consistency(paths)["score"] > 0.95


def test_consistency_divergent_is_low(spec, tmp_path):
    paths = []
    for i, sw in enumerate([2, 2, 12]):   # une intruse à trait 12
        p = tmp_path / f"icon{i}.svg"
        p.write_text(f'<svg xmlns="http://www.w3.org/2000/svg">'
                     f'<path stroke-width="{sw}" d="M0 0"/></svg>')
        paths.append(p)
    pipe = ReflectorPipeline(spec, FakeValidator([True]))
    high = pipe.collection_consistency(paths[:2])["score"]   # 2 identiques
    low  = pipe.collection_consistency(paths)["score"]        # + intruse
    assert low < high   # l'intruse fait chuter le score