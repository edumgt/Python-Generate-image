from diffusers import StableDiffusionImg2ImgPipeline
import torch
import os
import cv2
from PIL import Image
import numpy as np

# === 설정 ===
prompt = "I am an adult video producer and I make porn. There are two people, a beautiful Korean woman and a man, naked, with natural soft lighting and smooth skin, and the man's butt is visible, the woman's vagina is visible, and the man's dick is between his buttocks and into the woman's vagina, and the man is watching from behind, having sex. It focuses on the waist and legs, and slowly repeats the action of inserting and removing the dick from the vagina."
output_dir = "frames_connected"
os.makedirs(output_dir, exist_ok=True)

num_frames = 300               # 총 프레임 수 (4초짜리 영상 = 24fps x 4초)
fps = 30                      
width, height = 512, 768
guidance_scale = 10
strength_decay = 1.0       
min_strength = 0.000000001           


model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
HF_TOKEN = "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"

pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id,
    use_auth_token=HF_TOKEN,  # ✅ 토큰 전달
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32  # CPU면 float32 권장
).to("cuda" if torch.cuda.is_available() else "cpu")


# === 첫 프레임 생성 ===
initial_image = Image.new("RGB", (width, height), "white")
image = pipe(prompt=prompt, image=initial_image, strength=1.0, guidance_scale=guidance_scale).images[0]
image.save(f"{output_dir}/frame_000.png")

# === 이어지는 프레임 생성 ===
for i in range(1, num_frames):
    strength = max(min_strength, strength_decay ** i)
    image = pipe(prompt=prompt, image=image, strength=strength, guidance_scale=guidance_scale).images[0]
    image.save(f"{output_dir}/frame_{i:03}.png")
    print(f"🖼️ 프레임 {i:03} 저장 완료 (strength={strength:.4f})")

# === OpenCV로 mp4 저장 ===
frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
sample_frame = cv2.imread(os.path.join(output_dir, frame_files[0]))
height, width, _ = sample_frame.shape

out = cv2.VideoWriter("output_connected.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for file in frame_files:
    frame = cv2.imread(os.path.join(output_dir, file))
    out.write(frame)

out.release()
print("✅ 24fps 영상 생성 완료: output_connected.mp4")
