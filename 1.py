from diffusers import StableDiffusionPipeline
import torch
import os
import cv2
from PIL import Image

# 모델 로드 (CPU 전용)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# 폴더 준비
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

# 프레임 생성
prompt = "A fantasy landscape with castles and mountains"
for i in range(30):
    image = pipe(prompt).images[0]  # PIL.Image
    image.save(f"{output_dir}/frame_{i:03}.png")

# OpenCV로 동영상 생성
frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
sample_frame = cv2.imread(os.path.join(output_dir, frame_files[0]))
height, width, _ = sample_frame.shape

out = cv2.VideoWriter("output_video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))
for file in frame_files:
    frame = cv2.imread(os.path.join(output_dir, file))
    out.write(frame)
out.release()
print("🎞️ 동영상 생성 완료: output_video.mp4")
