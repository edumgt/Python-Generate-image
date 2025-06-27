import torch
from diffusers import StableDiffusionPipeline
import os
os.environ["DISABLE_FLASH_ATTN"] = "1"
from PIL import Image
from transformers import CLIPImageProcessor
processor = CLIPImageProcessor.from_pretrained("openai/clip-vit-base-patch32")
# prompt = "Full-body female humanoid robot, 25-year-old Japanese appearance, working as a McDonald's crew member, wearing red and yellow uniform with a name tag, realistic chrome and ceramic body with soft joint covers, standing behind a cashier counter, warm fast food restaurant interior, cinematic lighting, soft focus, photorealistic, elegant pose, 9:16 portrait"
# prompt = "Full-body female humanoid robot, 25-year-old Japanese appearance, working as a nurse in a modern hospital, wearing a white and pink nurse uniform with a name tag and stethoscope, realistic chrome and ceramic body with soft joint covers, standing beside a hospital bed with medical equipment in the background, bright clinical lighting, soft focus, photorealistic, gentle and caring pose, 9:16 portrait"
champions= {
  "Tracer": {
    "prompt": "Robotics Slim female hero with short brown spiky hair, orange chronal jumpsuit, yellow-tinted visor, dual pulse pistols, dynamic pose with time trail effect, futuristic London backdrop",
    "style": "Overwatch 2 style"
  },
  "Sojourn": {
    "prompt": "Robotics Athletic black female with white mohawk, red glowing cybernetic eye, sleek blue combat suit, railgun raised, cyberpunk trainyard setting, high-fidelity detail",
    "style": "Overwatch 2 style"
  },
  "Junker Queen": {
    "prompt": "Robotics Tall punk-style female warlord with mohawk, face paint, spiked armor, wielding shotgun and magnetic axe, dystopian gladiator arena background",
    "style": "Overwatch 2 style"
  },
  "Ramattra": {
    "prompt": "Robotics Ominous omnic monk with angular black-purple armor, flowing scarf, glowing nanite effects surrounding hands, destroyed monastery in background",
    "style": "Overwatch 2 style"
  },
  "Kiriko": {
    "prompt": "Robotics Young Japanese healer with fox mask on head, red and white modern shrine outfit, holding kunai, blue spirit fox and cherry blossom shrine behind her",
    "style": "Overwatch 2 style"
  },
  "Reinhardt": {
    "prompt": "Robotics Towering knight in silver-gray rocket armor, lion-emblazoned shoulder plate, holding massive hammer, blue energy shield, castle ruins battlefield",
    "style": "Overwatch 2 style"
  },
  "Sigma": {
    "prompt": "Robotics Floating scientist in blue gravity suit, bald with glowing scars, rocks orbiting around him, distorted gravity field in laboratory background",
    "style": "Overwatch 2 style"
  },
  "Cassidy": {
    "prompt": "Robotics Cowboy with red serape, cybernetic right arm, revolver in spinning motion, cigar in mouth, golden desert town at sunset",
    "style": "Overwatch 2 style"
  },
  "Genji": {
    "prompt": "Robotics Cyborg ninja in green-accented silver armor, glowing dragon emblem on chest, katana unsheathed, Japanese rooftop background",
    "style": "Overwatch 2 style"
  },
  "Hanzo": {
    "prompt": "Robotics Japanese archer with tattoos, tied-up hair, traditional blue robe, spirit dragon coiling behind him, ancient temple battlefield",
    "style": "Overwatch 2 style"
  },
  "Echo": {
    "prompt": "Robotics Futuristic female android with white-blue armor, glowing wings, soft robotic features, floating in digital sky background",
    "style": "Overwatch 2 style"
  },
  "Sombra": {
    "prompt": "Robotics Stealthy hacker with undercut purple hair, digital cloak, neon circuits glowing, disappearing into glitching urban alleyway",
    "style": "Overwatch 2 style"
  },
  "Widowmaker": {
    "prompt": "Robotics Purple-skinned sniper with long ponytail, red visor eye, tight blue bodysuit, perched on tower with sniper rifle, nighttime city view",
    "style": "Overwatch 2 style"
  },
  "Bastion": {
    "prompt": "Robotics Robotic unit with moss and rust details, bird on shoulder, transforming between turret and recon mode, peaceful forest background",
    "style": "Overwatch 2 style"
  },
  "Torbj\u00f6rn": {
    "prompt": "Robotics Short engineer with red beard, mechanical arm, turret on back, welding goggles, industrial forge setting",
    "style": "Overwatch 2 style"
  },
  "Zenyatta": {
    "prompt": "Robotics Floating omnic monk with bronze plating, glowing orbs circling head, meditative pose, tranquil temple background",
    "style": "Overwatch 2 style"
  },
  "Lucio": {
    "prompt": "Robotics Brazilian DJ with green visor, dreadlocks, glowing sonic amplifier, wall-riding across neon city arena",
    "style": "Overwatch 2 style"
  },
  "Moira": {
    "prompt": "Robotics Pale scientist with red and black coat, glowing purple and yellow hands, biotic mist swirling, lab corridor behind",
    "style": "Overwatch 2 style"
  },
  "Mercy": {
    "prompt": "Robotics Swiss healer with white armor and gold halo wings, holding Caduceus staff, glowing light from behind in futuristic hospital",
    "style": "Overwatch 2 style"
  },
  "Ana": {
    "prompt": "Robotics Elder Egyptian sniper with hooded cloak, eye patch, tactical rifle glowing blue, desert ruins in background",
    "style": "Overwatch 2 style"
  },
  "D.Va": {
    "prompt": "Robotics Korean gamer pilot with long brown hair, bubblegum, wearing pink-blue jumpsuit, standing in front of massive pink mech in hangar",
    "style": "Overwatch 2 style"
  },
  "Orisa": {
    "prompt": "Robotics Four-legged centaur-like omnic with gold-green armor, energy spear charged, defending Numbani streets",
    "style": "Overwatch 2 style"
  },
  "Roadhog": {
    "prompt": "Robotics Large masked brawler with tattoos, gas mask, hook and scrap gun, standing in grimy alley with graffiti walls",
    "style": "Overwatch 2 style"
  },
  "Junkrat": {
    "prompt": "Robotics Wild demolitionist with spiked hair, missing tooth, grenades and trap gear, laughing maniacally in desert junkyard",
    "style": "Overwatch 2 style"
  },
  "Symmetra": {
    "prompt": "Robotics Indian architect in sleek light-blue armor, creating hard-light construct with her fingers, high-tech city background",
    "style": "Overwatch 2 style"
  },
  "Pharah": {
    "prompt": "Robotics Egyptian woman in heavy blue Raptora armor, rocket launcher aimed, wings igniting mid-air over battlefield",
    "style": "Overwatch 2 style"
  },
  "Mei": {
    "prompt": "Robotics Scientist with blue parka, snow goggles, cryo-blaster in hand, snowy arctic base setting, small Snowball robot floating beside",
    "style": "Overwatch 2 style"
  },
  "Winston": {
    "prompt": "Robotics Gorilla scientist in white armor, glasses, jumping with Tesla cannon charged, lab background with broken machinery",
    "style": "Overwatch 2 style"
  },
  "Reaper": {
    "prompt": "Robotics Dark wraith-like figure in black hooded coat, white skull mask, dual shotguns, smoke and shadows swirling around him",
    "style": "Overwatch 2 style"
  },
  "Soldier: 76": {
    "prompt": "Robotics Veteran soldier with blue armor and red visor mask, pulse rifle firing, sprinting across destroyed street, military debris",
    "style": "Overwatch 2 style"
  },
  "Zarya": {
    "prompt": "Robotics Muscular Russian woman with pink hair, power armor and glowing particle cannon, energy shield surrounding her in urban battlefield",
    "style": "Overwatch 2 style"
  },
  "Brigitte": {
    "prompt": "Robotics Young female squire in yellow armor, brown ponytail, holding energy shield and flail, standing confidently in castle courtyard",
    "style": "Overwatch 2 style"
  },
  "Ashe": {
    "prompt": "Robotics White-haired outlaw with black vest, red lipstick, lever-action rifle resting on shoulder, dynamite belt, omnic butler behind her",
    "style": "Overwatch 2 style"
  },
  "Baptiste": {
    "prompt": "Robotics Combat medic with teal-orange armor, visor goggles, biotic launcher and healing field generator, futuristic city plaza",
    "style": "Overwatch 2 style"
  },
  "Lifeweaver": {
    "prompt": "Robotics Elegant man with long hair, pink-gold floral tech armor, glowing petal platform in hand, standing in garden with cherry blossoms",
    "style": "Overwatch 2 style"
  },
  "Illari": {
    "prompt": "Robotics Solar-powered warrior with glowing yellow markings, golden armor and energy rifle, sunset background with Incan temple",
    "style": "Overwatch 2 style"
  },
  "Mauga": {
    "prompt": "Robotics Massive Samoan tank with tribal tattoos, dual chainguns, red power armor, glowing eyes, volcanic battlefield with smoke and lava",
    "style": "Overwatch 2 style"
  },
  "Wrecking Ball": {
    "prompt": "Robotics Spherical orange mech with hamster cockpit open, small pilot with headset inside, transforming legs extended, scrapyard setting",
    "style": "Overwatch 2 style"
  },
  "Doomfist": {
    "prompt": "Robotics Powerful brawler with cybernetic golden gauntlet, bald head, red markings, shirtless upper body, charging through collapsed building",
    "style": "Overwatch 2 style"
  }
}




# prompt = "A cute fluffy puppy playing joyfully in a sunny green field, chasing a colorful butterfly. The dog has big round eyes, floppy ears, and a happy expression. The background is filled with blooming flowers, soft sunlight, and blue sky. Wholesome, heartwarming, Pixar-style illustration, highly detailed, 4K resolution."
# champions= {

#     "1": {
#       "prompt": prompt
#     },
#     "2": {
#       "prompt": prompt
#     },
#     "3": {
      
#       "prompt": prompt
#     },

#     "4": {
#       "prompt": prompt
#     },
    

#     "5": {
#       "prompt": prompt
#     },

#     "6": {
#       "prompt": prompt
#     },
    

#     "7": {
#       "prompt": prompt
#     }

# }





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
