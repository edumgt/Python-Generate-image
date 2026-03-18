#!/usr/bin/env python3
"""moon_test.py — 우주에 달 하나 떠 있는 이미지 생성 테스트

HuggingFace diffusers 가 설치되어 있으면 실제 Stable Diffusion 모델을 사용하고,
설치되어 있지 않으면 PNG 형태의 SVG 대체 이미지를 생성합니다.

사용법:
    # 온라인 환경 (처음 실행 시 모델 자동 다운로드)
    python3 moon_test.py

    # 오프라인/폐쇄망 환경 (사전에 scripts/preload-models.py 실행 필요)
    HF_HOME=/home/vagrant/hf_cache TRANSFORMERS_OFFLINE=1 python3 moon_test.py

결과 이미지: moon_output.png (현재 디렉터리에 저장)
"""

import os
import sys
from pathlib import Path

PROMPT = "a single bright moon floating in outer space, deep cosmos, stars, photorealistic, 4K"
OUTPUT_FILE = Path("moon_output.png")
WIDTH = 512
HEIGHT = 512
MODEL_ID = "runwayml/stable-diffusion-v1-5"


def generate_with_diffusers() -> None:
    import torch
    from diffusers import StableDiffusionPipeline

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    print(f"Device : {device}")
    print(f"Model  : {MODEL_ID}")
    print(f"Prompt : {PROMPT}")
    print("Loading pipeline … (this may take a few minutes on first run)")

    pipe = StableDiffusionPipeline.from_pretrained(
        MODEL_ID,
        torch_dtype=dtype,
        safety_checker=None,
        requires_safety_checker=False,
    ).to(device)
    pipe.set_progress_bar_config(disable=False)

    print("Generating image …")
    result = pipe(
        prompt=PROMPT,
        width=WIDTH,
        height=HEIGHT,
        num_inference_steps=20,
    )
    image = result.images[0]
    image.save(str(OUTPUT_FILE))
    print(f"\n✓ Image saved: {OUTPUT_FILE.resolve()}")


def generate_placeholder() -> None:
    """Fallback: create a simple PNG placeholder without AI libraries."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        # Ultra-minimal fallback: write a 1×1 black PNG
        _write_minimal_png()
        return

    img = Image.new("RGB", (WIDTH, HEIGHT), color=(5, 5, 20))
    draw = ImageDraw.Draw(img)

    # Draw a simple "moon"
    cx, cy, r = WIDTH // 2, HEIGHT // 2, 80
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(240, 240, 200))

    # Stars
    import random
    rng = random.Random(42)
    for _ in range(200):
        x = rng.randint(0, WIDTH - 1)
        y = rng.randint(0, HEIGHT - 1)
        draw.point((x, y), fill=(255, 255, 255))

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    note = "[placeholder — install diffusers for AI generation]"
    draw.text((10, 10), note, fill=(180, 180, 180), font=font)

    img.save(str(OUTPUT_FILE))
    print(f"✓ Placeholder image saved: {OUTPUT_FILE.resolve()}")
    print("  Install diffusers+torch to generate a real AI image.")


def _write_minimal_png() -> None:
    """Write a valid 1×1 black PNG without any third-party libraries."""
    import struct
    import zlib

    def chunk(name: bytes, data: bytes) -> bytes:
        c = name + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    raw = b"\x00\x00\x00\x00"
    idat = chunk(b"IDAT", zlib.compress(raw))
    iend = chunk(b"IEND", b"")
    OUTPUT_FILE.write_bytes(signature + ihdr + idat + iend)
    print(f"✓ Minimal placeholder saved: {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    try:
        import torch  # noqa: F401
        import diffusers  # noqa: F401
        generate_with_diffusers()
    except ImportError:
        print("diffusers or torch not found — generating placeholder image.")
        generate_placeholder()
    except Exception as exc:
        print(f"Error during AI generation: {exc}", file=sys.stderr)
        print("Falling back to placeholder …")
        generate_placeholder()
