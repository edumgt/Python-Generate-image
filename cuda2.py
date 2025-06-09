from diffusers import StableDiffusionImg2ImgPipeline
import torch
import os
import cv2
from PIL import Image
import subprocess
import time

# === 설정 ===
prompt = (
    "a young woman wearing shorts and a light jogging outfit, jogging by the riverside "
    "at 5am, soft dawn lighting, peaceful atmosphere, motion blur, dynamic pose"
)
output_dir = "jogging_frames"
os.makedirs(output_dir, exist_ok=True)

num_frames = 150   # 5초 × 30fps
fps = 30
width, height = 512, 768
guidance_scale = 7.5
strength = 0.75  # 이미지 왜곡도 (조절 가능)
mp3_file = "background.mp3"  # 선택: 배경음악
temp_video = "temp_no_audio.mp4"
final_video = "jogging_with_audio.mp4"

# === 모델 로드 ===
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "Lykon/dreamshaper-8", torch_dtype=torch.float16
).to("cuda")
pipe.enable_attention_slicing()

# === 첫 이미지용 흰 배경
init_image = Image.new("RGB", (width, height), "white")

# === 프레임 생성 ===
print(f"🚀 {num_frames}프레임 생성 시작...")
start_time = time.time()
for i in range(num_frames):
    image = pipe(prompt=prompt, image=init_image,
                 strength=strength, guidance_scale=guidance_scale).images[0]
    image.save(f"{output_dir}/frame_{i:03}.png")
    print(f"✅ frame_{i:03}.png 생성 완료")
print(f"🖼️ 전체 프레임 생성 완료! ⏱️ {time.time() - start_time:.2f}초")

# === 영상 생성 (OpenCV)
frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
sample_frame = cv2.imread(os.path.join(output_dir, frame_files[0]))
height, width, _ = sample_frame.shape
out = cv2.VideoWriter(temp_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for f in frame_files:
    path = os.path.join(output_dir, f)
    img = cv2.imread(path)
    out.write(img)
out.release()
print(f"🎬 영상 생성 완료: {temp_video}")

# === 배경 음악 병합
if os.path.exists(mp3_file):
    print("🎵 오디오 병합 중...")
    cmd = [
        "ffmpeg", "-y",
        "-i", temp_video,
        "-i", mp3_file,
        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", final_video
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"✅ 최종 영상 완료: {final_video}")
else:
    print("⚠️ MP3 없음. 오디오 없이 저장됨.")
