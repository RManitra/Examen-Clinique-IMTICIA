"""Module de génération vectorielle SVG sémantique et paramétrique."""

from pathlib import Path


class IconGenerator:
    def __init__(self, brand_style: dict):
        self.brand_style = brand_style

        colors = brand_style.get("allowed_colors") or ["#111827"]
        required = brand_style.get("required_colors") or []
        accents = brand_style.get("accent_colors") or []

        # stroke_color = la couleur la plus sombre pour les traits
        self.stroke_color = colors[0]

        # primary = couleur requise (ex: jaune dominant) ou sinon la 2e de la palette
        if required:
            self.primary = required[0]
        else:
            self.primary = colors[min(1, len(colors) - 1)]

        # accent = couleur d'accent depuis la charte, ou sinon la 1re non-stroke non-primary
        if accents:
            self.accent = accents[0]
        else:
            self.accent = None
            for c in colors:
                if c != self.stroke_color and c != self.primary:
                    self.accent = c
                    break
            if self.accent is None:
                self.accent = colors[min(2, len(colors) - 1)]

        self.white = "#FFFFFF" if "#FFFFFF" in colors else colors[-1]

        self.view_box = brand_style.get("view_box") or "0 0 24 24"
        self.stroke_width = brand_style.get("stroke_width") or 1.5
        self.linecap = brand_style.get("stroke_linecap") or "round"
        self.linejoin = brand_style.get("stroke_linejoin") or "round"

        # Toutes les formes ci-dessous sont dessinées sur une grille interne
        # fixe de 64x64 (plus simple à composer). On calcule le facteur
        # d'échelle nécessaire pour que ce dessin tienne exactement dans le
        # viewBox réel de la charte, quel qu'il soit (24x24, 128x128, ...).
        self._INTERNAL_SIZE = 64.0
        try:
            _, _, vb_w, vb_h = (float(v) for v in self.view_box.split())
        except (ValueError, AttributeError):
            vb_w = vb_h = self._INTERNAL_SIZE
        self._scale = min(vb_w, vb_h) / self._INTERNAL_SIZE

    def _svg_open(self, title: str, desc: str) -> str:
        compensated_stroke = self.stroke_width / self._scale if self._scale else self.stroke_width
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{self.view_box}" '
            f'role="img" aria-labelledby="title desc">\n'
            f'  <title id="title">{title}</title>\n'
            f'  <desc id="desc">{desc}</desc>\n'
            f'  <g transform="scale({self._scale})" '
            f'stroke="{self.stroke_color}" stroke-width="{compensated_stroke:.3f}" '
            f'stroke-linecap="{self.linecap}" stroke-linejoin="{self.linejoin}">'
        )

    def generate_icon(self, request: dict) -> str:
        concept_id = request.get("id", "").lower()
        concept_title = request.get("concept", "Concept")
        context = request.get("context", "")

        if concept_id == "cloud":
            return self._generate_cloud(concept_title, context)
        elif concept_id == "security":
            return self._generate_security(concept_title, context)
        elif concept_id == "database":
            return self._generate_database(concept_title, context)
        elif concept_id == "collaboration":
            return self._generate_collaboration(concept_title, context)
        elif concept_id == "deployment":
            return self._generate_deployment(concept_title, context)
        else:
            return self._generate_generic(concept_id, concept_title, context)

    def _generate_cloud(self, title: str, desc: str) -> str:
        return f'''{self._svg_open(title, desc)}
    <path d="M18 46h28a12 12 0 0 0 2-23.8 14 14 0 0 0-26.4-4.2A11 11 0 0 0 18 46z" fill="{self.primary}"/>
    <path d="M26 35h12M32 29v12" fill="none"/>
    <circle cx="48" cy="22" r="3" fill="{self.accent}" stroke="none"/>
  </g>
</svg>'''

    def _generate_security(self, title: str, desc: str) -> str:
        return f'''{self._svg_open(title, desc)}
    <path d="M32 7 12 15v16c0 14.5 9.8 23 20 26 10.2-3 20-11.5 20-26V15z" fill="{self.primary}"/>
    <rect x="23" y="27" width="18" height="15" rx="3" fill="{self.accent}"/>
    <path d="M27 27v-5a5 5 0 0 1 10 0v5" fill="none"/>
    <circle cx="32" cy="33.5" r="1.5" fill="{self.white}" stroke="none"/>
  </g>
</svg>'''

    def _generate_database(self, title: str, desc: str) -> str:
        return f'''{self._svg_open(title, desc)}
    <path d="M12 16c0-4.4 9-8 20-8s20 3.6 20 8v32c0 4.4-9 8-20 8s-20-3.6-20-8z" fill="{self.primary}"/>
    <path d="M12 24c0 4.4 9 8 20 8s20-3.6 20-8" fill="none"/>
    <path d="M12 36c0 4.4 9 8 20 8s20-3.6 20-8" fill="none"/>
    <ellipse cx="32" cy="16" rx="20" ry="8" fill="{self.accent}"/>
  </g>
</svg>'''

    def _generate_collaboration(self, title: str, desc: str) -> str:
        return f'''{self._svg_open(title, desc)}
    <circle cx="21" cy="20" r="7" fill="{self.primary}"/>
    <circle cx="43" cy="20" r="7" fill="{self.primary}"/>
    <path d="M9 49c0-8 6-13 14-13h3" fill="{self.primary}"/>
    <path d="M55 49c0-8-6-13-14-13h-3" fill="{self.primary}"/>
    <circle cx="32" cy="32" r="8" fill="{self.accent}"/>
    <path d="M28 32l3 3 5-5" fill="none"/>
  </g>
</svg>'''

    def _generate_deployment(self, title: str, desc: str) -> str:
        return f'''{self._svg_open(title, desc)}
    <path d="M32 7c-9 0-16 10-16 22 0 8 4 14 7 17l9 9 9-9c3-3 7-9 7-17 0-12-7-22-16-22z" fill="{self.primary}"/>
    <circle cx="32" cy="25" r="6" fill="{self.white}"/>
    <path d="M26 50l6 8 6-8" fill="{self.accent}"/>
  </g>
</svg>'''

    def _generate_generic(self, concept_id: str, title: str, desc: str) -> str:
        safe = self.brand_style.get("safe_zone") or {"x_min": 5, "x_max": 59, "y_min": 5, "y_max": 59}
        cx = (safe["x_min"] + safe["x_max"]) / 2
        cy = (safe["y_min"] + safe["y_max"]) / 2
        r = min(safe["x_max"] - safe["x_min"], safe["y_max"] - safe["y_min"]) / 4
        return f'''{self._svg_open(title, desc)}
    <rect x="{safe['x_min']}" y="{safe['y_min']}" width="{safe['x_max']-safe['x_min']}" height="{safe['y_max']-safe['y_min']}" fill="{self.primary}" rx="8"/>
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{self.accent}" stroke="none"/>
  </g>
</svg>'''