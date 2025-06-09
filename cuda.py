from diffusers import StableDiffusionImg2ImgPipeline
import torch
import os
import cv2
from PIL import Image
import numpy as np

# === 설정 ===
prompt = "Just two orange, cinematic lighting"
output_dir = "frames_connected"
os.makedirs(output_dir, exist_ok=True)
num_frames = 48
width, height = 512, 768
strength_decay = 0.98  # 점진적 변화 비율

# === 모델 로드 ===
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# === 1. 첫 이미지 생성 (기준 프레임)
image = pipe(prompt=prompt, strength=1.0, guidance_scale=7.5,
             image=Image.new("RGB", (width, height), "white")).images[0]
image.save(f"{output_dir}/frame_000.png")

# === 2. 이후 프레임은 img2img로 이어서 생성
for i in range(1, num_frames):
    strength = max(0.3, strength_decay ** i)  # 점점 적게 변화
    image = pipe(prompt=prompt, image=image, strength=strength, guidance_scale=7.5).images[0]
    image.save(f"{output_dir}/frame_{i:03}.png")

# === 3. OpenCV로 mp4로 저장
frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
sample_frame = cv2.imread(os.path.join(output_dir, frame_files[0]))
height, width, _ = sample_frame.shape
out = cv2.VideoWriter("output_connected.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

for file in frame_files:
    frame = cv2.imread(os.path.join(output_dir, file))
    out.write(frame)

out.release()
print("✅ 연결된 영상 생성 완료: output_connected.mp4")
