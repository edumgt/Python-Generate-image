from diffusers import StableDiffusionImg2ImgPipeline
import torch
import os
import cv2
from PIL import Image
import subprocess

# === 설정 ===
prompt_start = "a girl in natural lighting"
prompt_end = "a girl in futuristic sci-fi armor, neon lights"
output_dir = "frames_connected"
os.makedirs(output_dir, exist_ok=True)

num_frames = 120              # 원래 방향 프레임 수
fps = 30
width, height = 512, 768
guidance_scale = 7.5
strength_decay = 0.995
min_strength = 0.3
mp3_file = "background.mp3"
final_video = "output_connected_with_audio.mp4"

# === 모델 로드 ===
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "Lykon/dreamshaper-8",
    torch_dtype=torch.float16
).to("cuda")

# === 첫 프레임 생성 ===
image = pipe(prompt=prompt_start, image=Image.new("RGB", (width, height), "white"),
             strength=1.0, guidance_scale=guidance_scale).images[0]
image.save(f"{output_dir}/frame_000.png")

# === 프레임 생성 ===
for i in range(1, num_frames):
    # 프롬프트 점진적 전환
    ratio = i / (num_frames - 1)
    prompt = f"{prompt_start} AND ({prompt_end})^{ratio:.2f}"
    
    strength = max(min_strength, strength_decay ** i)
    image = pipe(prompt=prompt, image=image, strength=strength, guidance_scale=guidance_scale).images[0]
    image.save(f"{output_dir}/frame_{i:03}.png")
    print(f"🖼️ frame_{i:03}.png saved (strength={strength:.4f}, ratio={ratio:.2f})")

# === 🔁 프레임 루프 (정방향 + 역방향)
frame_files = sorted([f for f in os.listdir(output_dir) if f.endswith(".png")])
reverse_files = frame_files[-2:0:-1]  # 첫 프레임 중복 제외
all_files = frame_files + reverse_files

# === OpenCV로 영상 생성
sample_frame = cv2.imread(os.path.join(output_dir, all_files[0]))
height, width, _ = sample_frame.shape
temp_video = "temp_no_audio.mp4"

out = cv2.VideoWriter(temp_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
for file in all_files:
    frame = cv2.imread(os.path.join(output_dir, file))
    out.write(frame)
out.release()

print(f"🎬 mp4 생성 완료: {temp_video}")

# === 🎵 MP3 병합 (ffmpeg 필요)
if os.path.exists(mp3_file):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", temp_video,
        "-i", mp3_file,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        final_video
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"✅ 최종 영상 생성 완료: {final_video}")
else:
    print("⚠️ 배경 음악 파일이 없습니다. 오디오 없이 저장됨.")
