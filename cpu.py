from diffusers import StableDiffusionImg2ImgPipeline
import torch
import os
import cv2
from PIL import Image
import numpy as np

# === 설정 ===
prompt = "The video is mainly made with scenes of Sex scene between Korean woman and Korean man"
sample_image_path = "sample.png"  # 미리 준비된 레퍼런스 이미지
output_dir = "frames_connected"
os.makedirs(output_dir, exist_ok=True)

num_frames = 300
fps = 30
guidance_scale = 7.5
strength_decay = 0.85
min_strength = 0.27

model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
HF_TOKEN = "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"

# === 모델 로드 ===
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id,
    use_auth_token=HF_TOKEN,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to("cuda" if torch.cuda.is_available() else "cpu")

# === 첫 이미지 로드 ===
initial_image = Image.open(sample_image_path).convert("RGB").resize((512, 768))
image = pipe(prompt=prompt, image=initial_image, strength=1.0, guidance_scale=guidance_scale).images[0]
image.save(f"{output_dir}/frame_000.png")

# === 이어지는 프레임 생성 ===
for i in range(1, num_frames):
    strength = max(min_strength, strength_decay ** i)
    image = pipe(prompt=prompt, image=image, strength=strength, guidance_scale=guidance_scale).images[0]
    image.save(f"{output_dir}/frame_{i:03}.png")
    print(f"🖼️ 프레임 {i:03} 저장 완료 (strength={strength:.4f})")

# === 영상으로 저장 ===
frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
sample_frame = cv2.imread(os.path.join(output_dir, frame_files[0]))
height, width, _ = sample_frame.shape

out = cv2.VideoWriter("output_connected.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
for file in frame_files:
    frame = cv2.imread(os.path.join(output_dir, file))
    out.write(frame)
out.release()
print("✅ 영상 저장 완료: output_connected.mp4")
