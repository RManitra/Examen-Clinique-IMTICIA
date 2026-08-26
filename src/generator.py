"""Module de génération vectorielle SVG sémantique et paramétrique."""

from pathlib import Path

class IconGenerator:
    def __init__(self, brand_style: dict):
        self.brand_style = brand_style
        self.yellow = "#FFD21E"
        self.orange = "#FF9D00"
        self.dark = "#111827"
        self.white = "#FFFFFF"

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
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <g stroke="{self.dark}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M18 46h28a12 12 0 0 0 2-23.8 14 14 0 0 0-26.4-4.2A11 11 0 0 0 18 46z" fill="{self.yellow}"/>
    <path d="M26 35h12M32 29v12" fill="none"/>
    <circle cx="48" cy="22" r="3" fill="{self.orange}" stroke="none"/>
  </g>
</svg>'''

    def _generate_security(self, title: str, desc: str) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <g stroke="{self.dark}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M32 7 12 15v16c0 14.5 9.8 23 20 26 10.2-3 20-11.5 20-26V15z" fill="{self.yellow}"/>
    <rect x="23" y="27" width="18" height="15" rx="3" fill="{self.orange}"/>
    <path d="M27 27v-5a5 5 0 0 1 10 0v5" fill="none"/>
    <circle cx="32" cy="33.5" r="1.5" fill="{self.white}" stroke="none"/>
  </g>
</svg>'''

    def _generate_database(self, title: str, desc: str) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <g stroke="{self.dark}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 16c0-4.4 9-8 20-8s20 3.6 20 8v32c0 4.4-9 8-20 8s-20-3.6-20-8z" fill="{self.yellow}"/>
    <path d="M12 24c0 4.4 9 8 20 8s20-3.6 20-8" fill="none"/>
    <path d="M12 36c0 4.4 9 8 20 8s20-3.6 20-8" fill="none"/>
    <ellipse cx="32" cy="16" rx="20" ry="8" fill="{self.orange}"/>
  </g>
</svg>'''

    def _generate_collaboration(self, title: str, desc: str) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <g stroke="{self.dark}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="21" cy="20" r="7" fill="{self.yellow}"/>
    <circle cx="43" cy="20" r="7" fill="{self.yellow}"/>
    <path d="M9 49c0-8 6-13 14-13h3" fill="{self.yellow}"/>
    <path d="M55 49c0-8-6-13-14-13h-3" fill="{self.yellow}"/>
    <circle cx="32" cy="32" r="8" fill="{self.orange}"/>
    <path d="M28 32l3 3 5-5" fill="none"/>
  </g>
</svg>'''

    def _generate_deployment(self, title: str, desc: str) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <g stroke="{self.dark}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <path d="M32 7c-9 0-16 10-16 22 0 8 4 14 7 17l9 9 9-9c3-3 7-9 7-17 0-12-7-22-16-22z" fill="{self.yellow}"/>
    <circle cx="32" cy="25" r="6" fill="{self.white}"/>
    <path d="M26 50l6 8 6-8" fill="{self.orange}"/>
  </g>
</svg>'''

    def _generate_generic(self, concept_id: str, title: str, desc: str) -> str:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <g stroke="{self.dark}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="12" y="12" width="40" height="40" rx="10" fill="{self.yellow}"/>
    <circle cx="32" cy="32" r="12" fill="{self.orange}"/>
    <path d="M26 32h12M32 26v12" fill="none"/>
  </g>
</svg>'''
