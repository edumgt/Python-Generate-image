import torch
from diffusers import StableDiffusionPipeline
import os
os.environ["DISABLE_FLASH_ATTN"] = "1"
from PIL import Image
from transformers import CLIPImageProcessor
processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")
# prompt = "Full-body female humanoid robot, 25-year-old Japanese appearance, working as a McDonald's crew member, wearing red and yellow uniform with a name tag, realistic chrome and ceramic body with soft joint covers, standing behind a cashier counter, warm fast food restaurant interior, cinematic lighting, soft focus, photorealistic, elegant pose, 9:16 portrait"
# prompt = "Full-body female humanoid robot, 25-year-old Japanese appearance, working as a nurse in a modern hospital, wearing a white and pink nurse uniform with a name tag and stethoscope, realistic chrome and ceramic body with soft joint covers, standing beside a hospital bed with medical equipment in the background, bright clinical lighting, soft focus, photorealistic, gentle and caring pose, 9:16 portrait"
# champions= {

# "3": {
#     "prompt": 
#     "Elite futuristic SWAT officer wearing black exoskeleton armor with glowing HUD visor, holding a high-tech railgun or plasma rifle, posing tactically in a ruined urban combat zone, sparks and smoke in background, gritty and hyper-realistic"
#   },

#   "4": {
#     "prompt": 
#     "Heavy-duty futuristic police armored vehicle with mounted plasma turrets and bulletproof smart glass, hovering slightly above the ground, parked near a neon-lit police headquarters in a dystopian city, rain and steam effects, cinematic lighting"  }
# ,"5": {
#     "prompt": 
#     "Futuristic robotic police dog with armored titanium plating, glowing blue sensors, hydraulic legs, patrolling a cyberpunk city street at night, neon signs reflecting on wet pavement, shot from low angle, photorealistic, 4K"  }


# }

prompt = "A cheerful YouTube creator playing with a cute 2-month-old white robot puppy, about the size of two fists, in a cozy studio. The puppy robot has big round eyes, a soft fur-like texture, and reacts with adorable gestures and electronic sounds. It fits perfectly in the creator's hands. High-resolution, warm cinematic lighting, kawaii aesthetic, futuristic toy design, ultra-detailed, 16:9 YouTube frame."
champions= {

    "1": {
      "prompt": prompt
    },
    "2": {
      "prompt": prompt
    },
    "3": {
      
      "prompt": prompt
    },

    "4": {
      "prompt": prompt
    },
    

    "5": {
      "prompt": prompt
    },

    "6": {
      "prompt": prompt
    },
    

    "7": {
      "prompt": prompt
    }

}





model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
# model_id = "DeepFloyd/IF-I-M-v1.0"
# model_id = "stabilityai/stable-diffusion-xl-base-1.0"
# model_id = "Lykon/dreamshaper-8"
# model_id = "rinna/japanese-stable-diffusion"
# model_id = "lllyasviel/control_v11p_sd15_openpose"
HF_TOKEN = "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"

# === 모델 로드 ===
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    use_auth_token=HF_TOKEN,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
).to("cuda" if torch.cuda.is_available() else "cpu")



os.makedirs("outputs", exist_ok=True)

for name, desc in champions.items():
    prompt = desc['prompt']  # ✅ 프롬프트 앞에 숫자 제거
    print(f"🎨 Generating {name}...")
    image = pipe(
    prompt=desc['prompt'],
    negative_prompt = "multiple people, extra bodies, extra limbs, twin faces, duplicate humans, crowd, more than one person",
    width=720,
    height=1024).images[0]
    image.save(f"outputs/{name}.png")


print("✅ All champion portraits saved in /outputs")
