#!/usr/bin/env python3
"""scripts/preload-models.py

Downloads the HuggingFace models required for offline / air-gapped use.
Run this script once (with internet access) to populate HF_HOME.
After that, set TRANSFORMERS_OFFLINE=1 and HF_DATASETS_OFFLINE=1 so the
application never tries to reach the internet.

Usage (with internet access):
    HF_HOME=/home/vagrant/hf_cache python3 scripts/preload-models.py

The script also works inside the VM via setup-vm.sh.
"""
import os
import sys

HF_HOME = os.environ.get("HF_HOME", os.path.expanduser("~/hf_cache"))
os.environ["HF_HOME"] = HF_HOME
os.makedirs(HF_HOME, exist_ok=True)

print(f"HF_HOME = {HF_HOME}")

# Models to pre-load (only the default / lightest one is downloaded here;
# add more if desired — each is several GB).
MODELS = [
    "runwayml/stable-diffusion-v1-5",
]


def download_model(model_id: str) -> None:
    print(f"\n--- Downloading model: {model_id} ---")
    try:
        from diffusers import StableDiffusionPipeline
        import torch

        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float32,  # float32 for CPU
            safety_checker=None,
            requires_safety_checker=False,
        )
        print(f"  ✓ {model_id} cached to {HF_HOME}")
        del pipe
    except Exception as exc:
        print(f"  ✗ Failed to download {model_id}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    for model in MODELS:
        download_model(model)
    print("\nAll models pre-loaded successfully. Air-gapped operation is ready.")
