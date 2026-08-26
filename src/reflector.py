"""Module d'évaluation et de raffinement itératif (Generate-Evaluate-Refine)."""

from pathlib import Path
from src.generator import IconGenerator
from src.validator_bridge import ValidatorBridge

class ReflectorPipeline:
    def __init__(self, brand_style: dict, validator_bridge: ValidatorBridge):
        self.brand_style = brand_style
        self.validator = validator_bridge
        self.generator = IconGenerator(brand_style)

    def process_requests(self, requests: list[dict], output_dir: Path) -> list[dict]:
        output_dir.mkdir(parents=True, exist_ok=True)
        results = []

        for req in requests:
            req_id = req["id"]
            svg_content = self.generator.generate_icon(req)
            out_file = output_dir / f"{req_id}.svg"
            out_file.write_text(svg_content, encoding="utf-8")

            report = self.validator.validate(out_file, xml_only=True)
            results.append({
                "id": req_id,
                "file": str(out_file),
                "valid": report["valid"],
                "errors": report.get("errors", []),
                "warnings": report.get("warnings", [])
            })

        return results
