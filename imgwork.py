import torch
from diffusers import StableDiffusionPipeline
import os
from PIL import Image


{
  "Akali": {
    "trait": "a stealth mecha-ninja equipped with cloaking systems and high-speed blades",
    "skin": "sleek black armor with neon green highlights, retractable face visor",
    "pose": "emerging from energy mist with dual plasma kunai extended"
  },
  "Anivia": {
    "trait": "a frost-based aerial mech with crystalline wings and cryo-core engine",
    "skin": "transparent blue plating, glowing snowflake emblems, mist exhaust vents",
    "pose": "soaring in flight with wings fully deployed"
  },
  "Aurelion Sol": {
    "trait": "a celestial dragon-class battleship with orbital weapons and star core",
    "skin": "gold-trimmed hull, floating constellation rings, shimmering energy trails",
    "pose": "hovering in deep space with stars circling its chassis"
  },
  "Ashe": {
    "trait": "a long-range artillery mech with precision-guided frost missiles",
    "skin": "white and blue armor, glowing ice bow module on forearm",
    "pose": "drawing energy bow with a frozen targeting arc"
  },
  "Draven": {
    "trait": "a high-agility executioner mech with rotating blade launchers",
    "skin": "muscle-toned plating, red lights, chain-linked spinning axes",
    "pose": "spinning blade arms mid-throw with aggressive stance"
  },
  "Fizz": {
    "trait": "an amphibious scout mech with trident-jump capability",
    "skin": "slimy metallic fins, underwater boosters, agile frame",
    "pose": "mid-leap with trident charged for thrust"
  },
  "Gnar": {
    "trait": "a transformation-capable mech shifting between scout and berserker forms",
    "skin": "prehistoric rusted panels, dual-mode hydraulics, glowing transformation core",
    "pose": "mid-shift with energy lines cracking across armor"
  },
  "Graves": {
    "trait": "a heavy-armored vanguard mech with smoke-cannon launcher",
    "skin": "bronze exo-plating, cigar-like exhaust pipe, reinforced gauntlets",
    "pose": "cocking arm-cannon with thick smoke venting behind"
  },
  "Heimerdinger": {
    "trait": "a genius support mech deploying autonomous turrets",
    "skin": "brass and chrome body, exposed gears, back-mounted mini-drones",
    "pose": "projecting holographic turret schematics from wrist console"
  },
  "Illaoi": {
    "trait": "a divine mech priest powered by oceanic kinetic cores",
    "skin": "coral-styled armor, gold tentacle arms, glowing blue energy glyphs",
    "pose": "slamming down energy totem with hydraulic arms extended"
  }
  
}




style = "Robot Style, full body, Natural lighting, 3D illustration"

pipe = StableDiffusionPipeline.from_pretrained(
    "Lykon/dreamshaper-8",  # 또는 현실 스타일용 "runwayml/stable-diffusion-v1-5"
    torch_dtype=torch.float16
).to("cuda")

os.makedirs("outputs", exist_ok=True)

for name, desc in champions.items():
    prompt = f"{name}, {desc['trait']}, {desc['skin']}, {desc['pose']}, {style}"
    print(f"🎨 Generating {name}...")
    image = pipe(prompt, width=720, height=1080).images[0]
    image.show()
    image.save(f"outputs/{name}.png")

print("✅ All champion portraits saved in /outputs")
