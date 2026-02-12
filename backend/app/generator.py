from __future__ import annotations

import html
import base64
import textwrap
import uuid
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class GenerateRequest(BaseModel):
    model_config = {"protected_namespaces": ()}
    model_id: str = Field(min_length=1)
    output_type: str = Field(pattern="^(image|video)$")
    prompt: str = Field(min_length=1, max_length=1000)
    width: int = Field(default=768, ge=256, le=1536)
    height: int = Field(default=768, ge=256, le=1536)
    video_size: str = Field(default="square")

    @field_validator("video_size")
    @classmethod
    def validate_video_size(cls, value: str) -> str:
        allowed = {"square", "landscape", "portrait"}
        if value not in allowed:
            raise ValueError(f"video_size must be one of {sorted(allowed)}")
        return value


class GenerationResult(BaseModel):
    model_config = {"protected_namespaces": ()}
    file_url: str
    media_type: str
    width: int
    height: int
    model_id: str
    prompt: str
    data_url: str | None = None


class GeneratorService:
    VIDEO_SIZES = {
        "square": (768, 768),
        "landscape": (1024, 576),
        "portrait": (576, 1024),
    }

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def available_models() -> list[str]:
        return [
            "runwayml/stable-diffusion-v1-5",
            "stabilityai/sdxl-turbo",
            "stabilityai/stable-diffusion-3-medium-diffusers",
        ]

    def generate(self, request: GenerateRequest) -> GenerationResult:
        width, height = request.width, request.height
        label = "IMAGE"

        if request.output_type == "video":
            width, height = self.VIDEO_SIZES[request.video_size]
            label = f"VIDEO PREVIEW ({request.video_size})"

        output_path, svg_content = self._create_preview_svg(
            model_id=request.model_id,
            prompt=request.prompt,
            width=width,
            height=height,
            label=label,
        )
        encoded_svg = base64.b64encode(svg_content.encode("utf-8")).decode("ascii")
        return GenerationResult(
            file_url=f"/outputs/{output_path.name}",
            media_type="image/svg+xml",
            width=width,
            height=height,
            model_id=request.model_id,
            prompt=request.prompt,
            data_url=f"data:image/svg+xml;base64,{encoded_svg}",
        )

    def _create_preview_svg(self, model_id: str, prompt: str, width: int, height: int, label: str) -> tuple[Path, str]:
        escaped_lines = textwrap.wrap(f"Prompt: {prompt}", width=60)
        text_lines = [
            label,
            f"Model: {model_id}",
            *escaped_lines,
        ]

        text_nodes = []
        y = 80
        for line in text_lines:
            safe_line = html.escape(line)
            text_nodes.append(
                f'<text x="36" y="{y}" fill="#e5e7eb" font-size="24" font-family="Arial">{safe_line}</text>'
            )
            y += 36

        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#0f172a" />
  <rect x="12" y="12" width="{width - 24}" height="{height - 24}" fill="none" stroke="#22d3ee" stroke-width="4" rx="10" />
  {"".join(text_nodes)}
</svg>
'''
        file_name = f"asset_{uuid.uuid4().hex[:8]}.svg"
        path = self.output_dir / file_name
        path.write_text(svg, encoding="utf-8")
        return path, svg
