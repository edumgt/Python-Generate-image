import torch
from diffusers import StableDiffusionPipeline
import os

# ✅ Hugging Face 토큰이 필요 없는 공개 모델 사용 (runwayml)
model_id = "Lykon/dreamshaper-8"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32  # CPU면 float32 권장
).to("cuda" if torch.cuda.is_available() else "cpu")


# ✅ 새로운 챔피언들
champions = {
    "Katarina": {
        "trait": "a deadly assassin with flowing red hair and dual daggers",
        "skin": "battle scarred leather armor, deep shadows, gothic punk elements",
        "pose": "standing confidently with one dagger pointed down"
    },
    "Thresh": {
        "trait": "a ghostly warden with chains and a glowing lantern",
        "skin": "dark spectral armor, green mist and eerie lighting",
        "pose": "looming forward with lantern held out"
    },
    "Miss Fortune": {
        "trait": "a stylish bounty hunter with twin pistols and a pirate hat",
        "skin": "tight red corset, flowing coat, golden accents",
        "pose": "one leg raised on a treasure chest, pistols drawn"
    },
    "Yasuo": {
        "trait": "a wind-swept swordsman with a torn cape and glowing eyes",
        "skin": "samurai-style armor, swirling wind and falling leaves",
        "pose": "battle stance with katana mid-swing"
    },
    "Irelia": {
        "trait": "a graceful warrior with levitating blades",
        "skin": "eastern silk armor, glowing runes, moonlight reflections",
        "pose": "suspended mid-air in a spinning motion with blades circling"
    }
}

# ✅ 리얼리즘 강화 스타일
# style = (
#     "Robot style, full body,  2:3 portrait, desert asphalt plaza at 3pm, "
#     "natural lighting, 3D illustration, two-tone color scheme: dark gray and light brown, "
#     "high resolution, dynamic pose, volumetric lighting, fabric texture, "
#     "hyper detailed hands and face, cinematic shading, highly detailed armor"
# )

style = "Robot style, full body,  2:3 portrait, desert asphalt plaza at 3pm, "
style += "natural lighting, 3D illustration, two-tone color scheme: dark gray and light brown"
style += "high resolution, dynamic pose, volumetric lighting, fabric texture, "
style += "hyper detailed hands and face, cinematic shading, highly detailed armor"

# ✅ 출력 디렉토리 생성
os.makedirs("outputs", exist_ok=True)

# ✅ 챔피언 이미지 생성
for name, desc in champions.items():
    prompt = f"{name}, {desc['trait']}, {desc['skin']}, {desc['pose']}, {style}"
    print(f"🎨 Generating {name}...")
    image = pipe(prompt, width=720, height=1280).images[0]
    image.save(f"outputs/{name}.png")

print("✅ New champion portraits saved in /outputs")
