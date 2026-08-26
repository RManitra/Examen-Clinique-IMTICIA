"""Bibliothèque de formes SVG réutilisables — tâche 3.2.

Chaque forme est une fonction qui retourne une chaîne SVG.
Toutes les coordonnées sont sur une grille interne 64×64.
Les couleurs sont passées en paramètre (jamais hardcodées).
"""

from typing import Optional


def circle(cx: float, cy: float, r: float,
           fill: str = "none", stroke: Optional[str] = None,
           stroke_width: Optional[float] = None) -> str:
    attrs = f'cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"'
    if stroke:
        sw = f' stroke-width="{stroke_width}"' if stroke_width else ""
        return f'<circle {attrs} stroke="{stroke}"{sw}/>'
    return f'<circle {attrs} stroke="none"/>'


def rect(x: float, y: float, w: float, h: float, rx: float = 0,
         fill: str = "none", stroke: Optional[str] = None,
         stroke_width: Optional[float] = None) -> str:
    attrs = f'x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'
    if rx:
        attrs += f' rx="{rx}"'
    if stroke:
        sw = f' stroke-width="{stroke_width}"' if stroke_width else ""
        return f'<rect {attrs} stroke="{stroke}"{sw}/>'
    return f'<rect {attrs} stroke="none"/>'


def ellipse(cx: float, cy: float, rx: float, ry: float,
            fill: str = "none", stroke: Optional[str] = None) -> str:
    attrs = f'cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"'
    if stroke:
        return f'<ellipse {attrs} stroke="{stroke}"/>'
    return f'<ellipse {attrs} stroke="none"/>'


def line(x1: float, y1: float, x2: float, y2: float,
         fill: str = "none") -> str:
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="{fill}"/>'


def path(d: str, fill: str = "none") -> str:
    return f'<path d="{d}" fill="{fill}"/>'


# ── Formes sémantiques pré-composées ──

def shield(cx: float = 32, cy: float = 32, size: float = 26,
           fill: str = "#FFD21E") -> str:
    """Bouclier de sécurité."""
    top = cy - size * 0.7
    bot = cy + size * 0.5
    return path(
        f'M{cx} {top} L{cx - size} {top + size * 0.3} '
        f'v{size * 0.6} c0 {size * 0.8} {size * 0.6} {size} {size} {size * 1.1} '
        f'c{size * 0.4} -{size * 0.1} {size} -{size * 0.3} {size} -{size * 1.1} '
        f'v-{size * 0.6} z',
        fill=fill,
    )


def lock(cx: float = 32, cy: float = 37, w: float = 22, h: float = 16,
         fill: str = "#FF9D00") -> str:
    """Cadenas de sécurité."""
    body = rect(cx - w / 2, cy, w, h, rx=3, fill=fill)
    arch_r = w * 0.3
    arch = path(
        f'M{cx - arch_r} {cy} v-{h * 0.5} a{arch_r} {h * 0.5} 0 0 1 {arch_r * 2} 0',
        fill="none",
    )
    return f'{body}\n    {arch}'


def note_music(cx: float = 32, cy: float = 32, size: float = 18,
               fill: str = "#FFD21E") -> str:
    """Note de musique (note simple avec hampe)."""
    head = ellipse(cx - size * 0.3, cy + size * 0.3, size * 0.35, size * 0.25, fill=fill)
    stem = path(
        f'M{cx + size * 0.05} {cy + size * 0.3} v-{size * 1.1}',
        fill="none",
    )
    return f'{head}\n    {stem}'


def cloud_shape(cx: float = 32, cy: float = 30, size: float = 22,
                fill: str = "#FFD21E") -> str:
    """Nuage stylisé."""
    r = size * 0.35
    return (
        f'<circle cx="{cx - r}" cy="{cy}" r="{r}" fill="{fill}"/> '
        f'<circle cx="{cx}" cy="{cy - r * 0.6}" r="{r * 1.2}" fill="{fill}"/> '
        f'<circle cx="{cx + r}" cy="{cy}" r="{r * 0.9}" fill="{fill}"/> '
        f'<rect x="{cx - r * 1.5}" y="{cy}" width="{r * 3}" height="{r * 1.2}" '
        f'rx="{r * 0.3}" fill="{fill}"/>'
    )


def arrow_up(cx: float = 32, cy: float = 32, size: float = 20,
             fill: str = "#FF9D00") -> str:
    """Flèche vers le haut (déploiement, upload)."""
    s = size / 2
    return path(
        f'M{cx} {cy - s} L{cx - s * 0.7} {cy + s * 0.2} '
        f'L{cx - s * 0.3} {cy + s * 0.2} L{cx - s * 0.3} {cy + s} '
        f'L{cx + s * 0.3} {cy + s} L{cx + s * 0.3} {cy + s * 0.2} '
        f'L{cx + s * 0.7} {cy + s * 0.2} z',
        fill=fill,
    )


def gear(cx: float = 32, cy: float = 32, r: float = 18,
         fill: str = "#FFD21E") -> str:
    """Engrenage / configuration / settings."""
    teeth = 8
    inner_r = r * 0.6
    tooth_h = r * 0.25
    d = ""
    import math
    for i in range(teeth):
        a1 = (2 * math.pi * i) / teeth
        a2 = (2 * math.pi * (i + 0.3)) / teeth
        a3 = (2 * math.pi * (i + 0.5)) / teeth
        a4 = (2 * math.pi * (i + 0.8)) / teeth
        x1, y1 = cx + inner_r * math.cos(a1), cy + inner_r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        x3, y3 = cx + r * math.cos(a3), cy + r * math.sin(a3)
        x4, y4 = cx + inner_r * math.cos(a4), cy + inner_r * math.sin(a4)
        if i == 0:
            d += f'M{x1:.1f} {y1:.1f} '
        d += f'L{x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} L{x4:.1f} {y4:.1f} '
    d += "z"
    return path(d, fill=fill)


def star(cx: float = 32, cy: float = 32, r: float = 20,
         fill: str = "#FFD21E") -> str:
    """Étoile / favoris / excellence."""
    import math
    inner = r * 0.45
    points = []
    for i in range(10):
        a = math.pi / 2 + (2 * math.pi * i) / 10
        radius = r if i % 2 == 0 else inner
        points.append(f'{cx + radius * math.cos(a):.1f} {cy - radius * math.sin(a):.1f}')
    return path(f'M{" L".join(points)} z', fill=fill)


def heart(cx: float = 32, cy: float = 32, size: float = 16,
          fill: str = "#FFD21E") -> str:
    """Cœur / favoris / amour."""
    return path(
        f'M{cx} {cy + size * 0.6} '
        f'C{cx - size * 1.2} {cy - size * 0.1} {cx - size * 0.6} {cy - size * 0.9} {cx} {cy - size * 0.4} '
        f'C{cx + size * 0.6} {cy - size * 0.9} {cx + size * 1.2} {cy - size * 0.1} {cx} {cy + size * 0.6} z',
        fill=fill,
    )


def magnifier(cx: float = 32, cy: float = 32, r: float = 14,
              fill: str = "none", stroke: str = "#111827") -> str:
    """Loupe / recherche / analytics."""
    lens = circle(cx - r * 0.2, cy - r * 0.2, r, fill=fill, stroke=stroke)
    handle = path(
        f'M{cx + r * 0.5} {cy + r * 0.5} L{cx + r * 1.2} {cy + r * 1.2}',
        fill="none",
    )
    return f'{lens}\n    {handle}'


def bar_chart(cx: float = 32, cy: float = 32, size: float = 24,
              fill: str = "#FFD21E") -> str:
    """Graphique en barres / analytics / tendance."""
    bars = [
        (cx - size * 0.4, cy + size * 0.3, size * 0.2, size * 0.5),
        (cx - size * 0.1, cy - size * 0.1, size * 0.2, size * 0.9),
        (cx + size * 0.2, cy + size * 0.1, size * 0.2, size * 0.7),
    ]
    rects = []
    for x, y, w, h in bars:
        rects.append(rect(x, y - h, w, h, rx=2, fill=fill))
    base = line(cx - size * 0.5, cy + size * 0.3, cx + size * 0.5, cy + size * 0.3)
    return f'{base}\n    ' + '\n    '.join(rects)


def wrench(cx: float = 32, cy: float = 32, size: float = 20,
           fill: str = "#FFD21E") -> str:
    """Clé / maintenance / outils."""
    s = size
    return path(
        f'M{cx - s * 0.4} {cy + s * 0.4} l{s * 0.6} -{s * 0.6} '
        f'a{s * 0.3} {s * 0.3} 0 0 1 {s * 0.15} -{s * 0.1} '
        f'a{s * 0.3} {s * 0.3} 0 0 1 {s * 0.1} {s * 0.15} '
        f'l-{s * 0.6} {s * 0.6}',
        fill="none",
    )


def eye(cx: float = 32, cy: float = 32, size: float = 22,
        fill: str = "#FFD21E") -> str:
    """Œil / surveillance / vision."""
    outer = path(
        f'M{cx - size} {cy} '
        f'Q{cx} {cy - size * 0.8} {cx + size} {cy} '
        f'Q{cx} {cy + size * 0.8} {cx - size} {cy} z',
        fill=fill,
    )
    pupil = circle(cx, cy, size * 0.25, fill="#111827")
    return f'{outer}\n    {pupil}'


def users(cx: float = 32, cy: float = 32, size: float = 20,
          fill: str = "#FFD21E") -> str:
    """Utilisateurs / équipe / personnes."""
    s = size
    head1 = circle(cx - s * 0.4, cy - s * 0.3, s * 0.25, fill=fill)
    head2 = circle(cx + s * 0.4, cy - s * 0.3, s * 0.25, fill=fill)
    body1 = path(
        f'M{cx - s * 0.65} {cy + s * 0.5} '
        f'Q{cx - s * 0.4} {cy} {cx - s * 0.15} {cy + s * 0.5}',
        fill=fill,
    )
    body2 = path(
        f'M{cx + s * 0.15} {cy + s * 0.5} '
        f'Q{cx + s * 0.4} {cy} {cx + s * 0.65} {cy + s * 0.5}',
        fill=fill,
    )
    return f'{head1}\n    {head2}\n    {body1}\n    {body2}'


def globe(cx: float = 32, cy: float = 32, r: float = 20,
          fill: str = "#FFD21E") -> str:
    """Globe / réseau / international."""
    circle_main = circle(cx, cy, r, fill="none")
    meridian1 = path(
        f'M{cx} {cy - r} a{r * 0.4} {r} 0 0 1 0 {r * 2}',
        fill="none",
    )
    meridian2 = path(
        f'M{cx - r} {cy} a{r} {r * 0.4} 0 0 0 {r * 2} 0',
        fill="none",
    )
    return f'{circle_main}\n    {meridian1}\n    {meridian2}'


def rocket(cx: float = 32, cy: float = 32, size: float = 20,
           fill: str = "#FFD21E") -> str:
    """Fusée / lancement / speed."""
    s = size
    body = path(
        f'M{cx} {cy - s} '
        f'Q{cx + s * 0.5} {cy - s * 0.5} {cx + s * 0.4} {cy + s * 0.3} '
        f'L{cx - s * 0.4} {cy + s * 0.3} '
        f'Q{cx - s * 0.5} {cy - s * 0.5} {cx} {cy - s} z',
        fill=fill,
    )
    window = circle(cx, cy - s * 0.2, s * 0.15, fill="#FFFFFF")
    return f'{body}\n    {window}'


def database_icon(cx: float = 32, cy: float = 32, size: float = 22,
                  fill: str = "#FFD21E") -> str:
    """Base de données / stockage."""
    s = size
    top_ellipse = ellipse(cx, cy - s * 0.5, s, s * 0.35, fill=fill)
    body_rect = rect(cx - s, cy - s * 0.5, s * 2, s, fill=fill)
    bottom_ellipse = ellipse(cx, cy + s * 0.5, s, s * 0.35, fill=fill)
    line1 = path(f'M{cx - s} {cy} a{s} {s * 0.35} 0 0 0 {s * 2} 0', fill="none")
    line2 = path(f'M{cx - s} {cy + s * 0.35} a{s} {s * 0.35} 0 0 0 {s * 2} 0', fill="none")
    return f'{body_rect}\n    {line1}\n    {line2}\n    {top_ellipse}\n    {bottom_ellipse}'


def code_brackets(cx: float = 32, cy: float = 32, size: float = 20,
                  fill: str = "#FFD21E") -> str:
    """Code / développement / programme."""
    s = size
    left = path(f'M{cx - s * 0.6} {cy - s * 0.5} L{cx - s * 0.1} {cy} L{cx - s * 0.6} {cy + s * 0.5}', fill="none")
    right = path(f'M{cx + s * 0.6} {cy - s * 0.5} L{cx + s * 0.1} {cy} L{cx + s * 0.6} {cy + s * 0.5}', fill="none")
    return f'{left}\n    {right}'


def lightning(cx: float = 32, cy: float = 32, size: float = 22,
              fill: str = "#FFD21E") -> str:
    """Éclair / énergie / vitesse / performance."""
    s = size
    return path(
        f'M{cx + s * 0.1} {cy - s} L{cx - s * 0.4} {cy + s * 0.1} '
        f'L{cx + s * 0.05} {cy + s * 0.1} L{cx - s * 0.1} {cy + s} '
        f'L{cx + s * 0.4} {cy - s * 0.1} L{cx - s * 0.05} {cy - s * 0.1} z',
        fill=fill,
    )


def bell(cx: float = 32, cy: float = 32, size: float = 18,
         fill: str = "#FFD21E") -> str:
    """Cloche / notification / alerte."""
    s = size
    body = path(
        f'M{cx} {cy - s * 0.9} '
        f'Q{cx - s * 0.8} {cy - s * 0.7} {cx - s * 0.8} {cy + s * 0.2} '
        f'L{cx - s} {cy + s * 0.5} '
        f'L{cx + s} {cy + s * 0.5} '
        f'L{cx + s * 0.8} {cy + s * 0.2} '
        f'Q{cx + s * 0.8} {cy - s * 0.7} {cx} {cy - s * 0.9} z',
        fill=fill,
    )
    dot = circle(cx, cy + s * 0.7, s * 0.15, fill=fill)
    return f'{body}\n    {dot}'


def pen(cx: float = 32, cy: float = 32, size: float = 20,
        fill: str = "#FFD21E") -> str:
    """Stylus / édition / création."""
    s = size
    return path(
        f'M{cx + s * 0.6} {cy - s * 0.6} '
        f'L{cx - s * 0.6} {cy + s * 0.6} '
        f'L{cx - s * 0.45} {cy + s * 0.75} '
        f'L{cx + s * 0.75} {cy - s * 0.45} z',
        fill=fill,
    )


def map_pin(cx: float = 32, cy: float = 32, size: float = 20,
            fill: str = "#FFD21E") -> str:
    """Localisation / carte / géolocalisation."""
    s = size
    head = circle(cx, cy - s * 0.3, s * 0.45, fill=fill)
    point = path(
        f'M{cx} {cy + s * 0.6} L{cx - s * 0.2} {cy + s * 0.05} '
        f'L{cx + s * 0.2} {cy + s * 0.05} z',
        fill=fill,
    )
    inner = circle(cx, cy - s * 0.3, s * 0.18, fill="#FFFFFF")
    return f'{head}\n    {point}\n    {inner}'


def calendar(cx: float = 32, cy: float = 32, size: float = 20,
             fill: str = "#FFD21E") -> str:
    """Calendrier / planification / date."""
    s = size
    cal = rect(cx - s, cy - s * 0.6, s * 2, s * 1.4, rx=3, fill=fill)
    bar = rect(cx - s, cy - s * 0.6, s * 2, s * 0.35, rx=3, fill="#111827")
    dot1 = circle(cx - s * 0.4, cy + s * 0.2, s * 0.12, fill="#FFFFFF")
    dot2 = circle(cx, cy + s * 0.2, s * 0.12, fill="#FFFFFF")
    dot3 = circle(cx + s * 0.4, cy + s * 0.2, s * 0.12, fill="#FFFFFF")
    return f'{cal}\n    {bar}\n    {dot1}\n    {dot2}\n    {dot3}'


def refresh(cx: float = 32, cy: float = 32, r: float = 16,
            fill: str = "#FFD21E") -> str:
    """Rafraîchissement / synchronisation / cycle."""
    import math
    arc = path(
        f'M{cx} {cy - r} a{r} {r} 0 1 1 -{r * 0.3} {r * 0.2}',
        fill="none",
    )
    head = path(
        f'M{cx - r * 0.3} {cy - r - r * 0.3} l{r * 0.3} {r * 0.3} l-{r * 0.3} {r * 0.3}',
        fill=fill,
    )
    return f'{arc}\n    {head}'
