import torch
from diffusers import StableDiffusionPipeline
import os
from PIL import Image


champions = {
    "Akali": {
        "trait": "a rogue ninja with smoke bombs and kunai",
        "skin": "urban assassin outfit, green tattoos, masked face",
        "pose": "emerging from smoke with blades in hand"
    },
    "Anivia": {
        "trait": "a majestic frost phoenix with crystalline feathers",
        "skin": "ice-covered wings, glowing blue core, snow effects",
        "pose": "soaring with wings wide open"
    },
    "Aurelion Sol": {
        "trait": "a celestial dragon with a star core",
        "skin": "glowing constellation skin, golden horns, star rings",
        "pose": "circling in the sky with stars orbiting"
    },
    "Ashe": {
        "trait": "an ice archer with a glowing blue bow",
        "skin": "fur-lined cloak, ice crown, snowy mist",
        "pose": "drawing an arrow with icy trail behind"
    },
    "Draven": {
        "trait": "a flamboyant executioner with spinning axes",
        "skin": "gladiator outfit, leather straps, confident smirk",
        "pose": "twirling axes with one hand while shouting"
    },
    "Fizz": {
        "trait": "a mischievous amphibian with a trident",
        "skin": "coral fins, bubble effects, sea creature charm",
        "pose": "mid-leap with trident ready to stab"
    },
    "Gnar": {
        "trait": "a cute yordle that transforms into a giant beast",
        "skin": "prehistoric outfit, bone weapons, two forms",
        "pose": "small Gnar mid-transformation into big Gnar"
    },
    "Graves": {
        "trait": "a rugged outlaw with a cigar and shotgun",
        "skin": "long coat, bandolier belt, smoky effects",
        "pose": "cocking his shotgun with a smirk"
    },
    "Heimerdinger": {
        "trait": "a genius yordle inventor with crazy hair",
        "skin": "goggles, steampunk tools, floating turrets",
        "pose": "gesturing toward a tiny turret beside him"
    },
    "Illaoi": {
        "trait": "a powerful priestess with a glowing idol",
        "skin": "tribal markings, giant golden totem, ocean energy",
        "pose": "slamming idol into ground with tentacles behind"
    },
    "Kayle": {
        "trait": "an ascended angel in radiant armor",
        "skin": "golden wings, glowing sword, divine light",
        "pose": "hovering with sword raised to the heavens"
    },
    "Lissandra": {
        "trait": "an ice witch with jagged shards and pale skin",
        "skin": "frozen cloak, glacial crown, frosty breath",
        "pose": "rising from frozen ground with arms lifted"
    },
    "Malzahar": {
        "trait": "a void prophet with glowing sigils",
        "skin": "dark robes, hovering symbols, void mist",
        "pose": "raising hands to summon the void"
    },
    "Nami": {
        "trait": "a mermaid sorceress wielding tidal magic",
        "skin": "shimmering scales, coral staff, ocean glow",
        "pose": "riding a wave with staff raised"
    },
    "Neeko": {
        "trait": "a curious chameleon girl with colorful markings",
        "skin": "leafy dress, jungle flora, shimmering tail",
        "pose": "peeking from behind a plant with smile"
    },
    "Nocturne": {
        "trait": "a nightmare wraith with shadowy blades",
        "skin": "wispy dark form, glowing red eyes, ethereal mist",
        "pose": "emerging from darkness with claws extended"
    },
    "Ornn": {
        "trait": "a forge god with a giant hammer and volcanic beard",
        "skin": "molten runes, stone armor, glowing forge effects",
        "pose": "standing at an anvil mid-strike"
    },
    "Rakan": {
        "trait": "a flamboyant dancer with feathered cloak",
        "skin": "shimmering gold and red fabrics, dazzling light trail",
        "pose": "striking a dramatic dance pose"
    },
    "Rumble": {
        "trait": "a yordle inventor inside a mech suit with flamethrowers",
        "skin": "rusted plating, exhaust vents, cartoonish flair",
        "pose": "launching a rocket with grin on face"
    },
    "Ryze": {
        "trait": "a battle mage covered in glowing scrolls",
        "skin": "rune tattoos, blue lightning, magical scrolls",
        "pose": "channeling runes while floating scrolls spin"
    },
    "Sejuani": {
        "trait": "a fierce warrior riding a boar with a flail",
        "skin": "fur cloak, icy armor, snow-covered helm",
        "pose": "swinging her flail while boar charges forward"
    },
    "Shaco": {
        "trait": "a demonic jester with a killer smile",
        "skin": "red and black harlequin outfit, daggers in both hands",
        "pose": "crouched behind victim with sinister grin"
    },
    "Singed": {
        "trait": "a mad chemist with poison trail",
        "skin": "gas mask, alchemist coat, green flasks",
        "pose": "running with poison trail behind him"
    },
    "Sivir": {
        "trait": "a battle-hardened mercenary wielding a giant chakram",
        "skin": "desert armor, tribal patterns, golden accents",
        "pose": "throwing her chakram with determination"
    },
    "Sylas": {
        "trait": "a rebellious mage with heavy chains",
        "skin": "shirtless, glowing shackles, magical tattoos",
        "pose": "swinging chains with rage in his eyes"
    },
    "Taric": {
        "trait": "a radiant gem knight with crystal armor",
        "skin": "glittering shoulder pads, hair blowing, gemstones glowing",
        "pose": "channeling cosmic energy through palms"
    },
    "Tryndamere": {
        "trait": "a barbarian king with a giant sword and wild eyes",
        "skin": "fur cape, savage armor, blood-red blade",
        "pose": "charging with sword above head"
    },
    "Vel'Koz": {
        "trait": "a void creature with glowing eyes and laser tendrils",
        "skin": "alien skin, pulsating veins, geometric patterns",
        "pose": "floating with one tentacle charging a beam"
    },
    "Viego": {
        "trait": "a tormented king with spectral blade",
        "skin": "ghostly crown, corrupted armor, mist trail",
        "pose": "reaching out as if to possess the viewer"
    },
    "Xayah": {
        "trait": "a rebellious Vastaya with feather daggers",
        "skin": "dark leather with magenta highlights, long feathery hair",
        "pose": "throwing feathers in a fan-shaped arc"
    },
    "Zoe": {
        "trait": "a cosmic trickster with a flowing scarf and playful eyes",
        "skin": "starlight particles, rainbow hair, floating orbs",
        "pose": "leaping through a portal mid-spin"
    }
}



style = "Robot Style, full body, Natural lighting, 3D illustration"

pipe = StableDiffusionPipeline.from_pretrained(
    "Lykon/dreamshaper-8",  # 또는 현실 스타일용 "runwayml/stable-diffusion-v1-5"
    torch_dtype=torch.float32
).to("cpu")

os.makedirs("outputs", exist_ok=True)

for name, desc in champions.items():
    prompt = f"{name}, {desc['trait']}, {desc['skin']}, {desc['pose']}, {style}"
    print(f"🎨 Generating {name}...")
    image = pipe(prompt, width=720, height=1080).images[0]
    image.show()
    image.save(f"outputs/{name}.png")

print("✅ All champion portraits saved in /outputs")
