import torch
from diffusers import StableDiffusionPipeline
import os
from PIL import Image

champions = {
  "Aatrox": {
    "trait": "inspired by aatrox, ",
    "pose": "engaging in dynamic action stance reflecting aatrox's style"
  },
  "Ahri": {
    "trait": "inspired by ahri, ",
    "pose": "engaging in dynamic action stance reflecting ahri's style"
  },
  "Akali": {
    "trait": "inspired by akali, ",
    "pose": "engaging in dynamic action stance reflecting akali's style"
  },
  "Alistar": {
    "trait": "inspired by alistar, ",
    "pose": "engaging in dynamic action stance reflecting alistar's style"
  },
  "Amumu": {
    "trait": "inspired by amumu, ",
    "pose": "engaging in dynamic action stance reflecting amumu's style"
  },
  "Anivia": {
    "trait": "inspired by anivia, ",
    "pose": "engaging in dynamic action stance reflecting anivia's style"
  },
  "Annie": {
    "trait": "inspired by annie, ",
    "pose": "engaging in dynamic action stance reflecting annie's style"
  },
  "Aphelios": {
    "trait": "inspired by aphelios, ",
    "pose": "engaging in dynamic action stance reflecting aphelios's style"
  },
  "Ashe": {
    "trait": "inspired by ashe, ",
    "pose": "engaging in dynamic action stance reflecting ashe's style"
  },
  "Aurelion Sol": {
    "trait": "inspired by aurelion sol, ",
    "pose": "engaging in dynamic action stance reflecting aurelion sol's style"
  },
  "Azir": {
    "trait": "inspired by azir, ",
    "pose": "engaging in dynamic action stance reflecting azir's style"
  },
  "Bard": {
    "trait": "inspired by bard, ",
    "pose": "engaging in dynamic action stance reflecting bard's style"
  },
  "Bel'Veth": {
    "trait": "inspired by bel'veth, ",
    "pose": "engaging in dynamic action stance reflecting bel'veth's style"
  },
  "Blitzcrank": {
    "trait": "inspired by blitzcrank, ",
    "pose": "engaging in dynamic action stance reflecting blitzcrank's style"
  },
  "Brand": {
    "trait": "inspired by brand, ",
    "pose": "engaging in dynamic action stance reflecting brand's style"
  },
  "Braum": {
    "trait": "inspired by braum, ",
    "pose": "engaging in dynamic action stance reflecting braum's style"
  },
  "Caitlyn": {
    "trait": "inspired by caitlyn, ",
    "pose": "engaging in dynamic action stance reflecting caitlyn's style"
  },
  "Camille": {
    "trait": "inspired by camille, ",
    "pose": "engaging in dynamic action stance reflecting camille's style"
  },
  "Cassiopeia": {
    "trait": "inspired by cassiopeia, ",
    "pose": "engaging in dynamic action stance reflecting cassiopeia's style"
  },
  "Cho'Gath": {
    "trait": "inspired by cho'gath, ",
    "pose": "engaging in dynamic action stance reflecting cho'gath's style"
  },
  "Corki": {
    "trait": "inspired by corki, ",
    "pose": "engaging in dynamic action stance reflecting corki's style"
  },
  "Darius": {
    "trait": "inspired by darius, ",
    "pose": "engaging in dynamic action stance reflecting darius's style"
  },
  "Diana": {
    "trait": "inspired by diana, ",
    "pose": "engaging in dynamic action stance reflecting diana's style"
  },
  "Dr. Mundo": {
    "trait": "inspired by dr. mundo, ",
    "pose": "engaging in dynamic action stance reflecting dr. mundo's style"
  },
  "Draven": {
    "trait": "inspired by draven, ",
    "pose": "engaging in dynamic action stance reflecting draven's style"
  },
  "Ekko": {
    "trait": "inspired by ekko, ",
    "pose": "engaging in dynamic action stance reflecting ekko's style"
  },
  "Elise": {
    "trait": "inspired by elise, ",
    "pose": "engaging in dynamic action stance reflecting elise's style"
  },
  "Evelynn": {
    "trait": "inspired by evelynn, ",
    "pose": "engaging in dynamic action stance reflecting evelynn's style"
  },
  "Ezreal": {
    "trait": "inspired by ezreal, ",
    "pose": "engaging in dynamic action stance reflecting ezreal's style"
  },
  "Fiddlesticks": {
    "trait": "inspired by fiddlesticks, ",
    "pose": "engaging in dynamic action stance reflecting fiddlesticks's style"
  },
  "Fiora": {
    "trait": "inspired by fiora, ",
    "pose": "engaging in dynamic action stance reflecting fiora's style"
  },
  "Fizz": {
    "trait": "inspired by fizz, ",
    "pose": "engaging in dynamic action stance reflecting fizz's style"
  },
  "Galio": {
    "trait": "inspired by galio, ",
    "pose": "engaging in dynamic action stance reflecting galio's style"
  },
  "Gangplank": {
    "trait": "inspired by gangplank, ",
    "pose": "engaging in dynamic action stance reflecting gangplank's style"
  },
  "Garen": {
    "trait": "inspired by garen, ",
    "pose": "engaging in dynamic action stance reflecting garen's style"
  },
  "Gnar": {
    "trait": "inspired by gnar, ",
    "pose": "engaging in dynamic action stance reflecting gnar's style"
  },
  "Gragas": {
    "trait": "inspired by gragas, ",
    "pose": "engaging in dynamic action stance reflecting gragas's style"
  },
  "Graves": {
    "trait": "inspired by graves, ",
    "pose": "engaging in dynamic action stance reflecting graves's style"
  },
  "Gwen": {
    "trait": "inspired by gwen, ",
    "pose": "engaging in dynamic action stance reflecting gwen's style"
  },
  "Hecarim": {
    "trait": "inspired by hecarim, ",
    "pose": "engaging in dynamic action stance reflecting hecarim's style"
  },
  "Heimerdinger": {
    "trait": "inspired by heimerdinger, ",
    "pose": "engaging in dynamic action stance reflecting heimerdinger's style"
  },
  "Illaoi": {
    "trait": "inspired by illaoi, ",
    "pose": "engaging in dynamic action stance reflecting illaoi's style"
  },
  "Irelia": {
    "trait": "inspired by irelia, ",
    "pose": "engaging in dynamic action stance reflecting irelia's style"
  },
  "Ivern": {
    "trait": "inspired by ivern, ",
    "pose": "engaging in dynamic action stance reflecting ivern's style"
  },
  "Janna": {
    "trait": "inspired by janna, ",
    "pose": "engaging in dynamic action stance reflecting janna's style"
  },
  "Jarvan IV": {
    "trait": "inspired by jarvan iv, ",
    "pose": "engaging in dynamic action stance reflecting jarvan iv's style"
  },
  "Jax": {
    "trait": "inspired by jax, ",
    "pose": "engaging in dynamic action stance reflecting jax's style"
  },
  "Jayce": {
    "trait": "inspired by jayce, ",
    "pose": "engaging in dynamic action stance reflecting jayce's style"
  },
  "Jhin": {
    "trait": "inspired by jhin, ",
    "pose": "engaging in dynamic action stance reflecting jhin's style"
  },
  "Jinx": {
    "trait": "inspired by jinx, ",
    "pose": "engaging in dynamic action stance reflecting jinx's style"
  },
  "K'Sante": {
    "trait": "inspired by k'sante, ",
    "pose": "engaging in dynamic action stance reflecting k'sante's style"
  },
  "Kai'Sa": {
    "trait": "inspired by kai'sa, ",
    "pose": "engaging in dynamic action stance reflecting kai'sa's style"
  },
  "Kalista": {
    "trait": "inspired by kalista, ",
    "pose": "engaging in dynamic action stance reflecting kalista's style"
  },
  "Karma": {
    "trait": "inspired by karma, ",
    "pose": "engaging in dynamic action stance reflecting karma's style"
  },
  "Karthus": {
    "trait": "inspired by karthus, ",
    "pose": "engaging in dynamic action stance reflecting karthus's style"
  },
  "Kassadin": {
    "trait": "inspired by kassadin, ",
    "pose": "engaging in dynamic action stance reflecting kassadin's style"
  },
  "Katarina": {
    "trait": "inspired by katarina, ",
    "pose": "engaging in dynamic action stance reflecting katarina's style"
  },
  "Kayle": {
    "trait": "inspired by kayle, ",
    "pose": "engaging in dynamic action stance reflecting kayle's style"
  },
  "Kayn": {
    "trait": "inspired by kayn, ",
    "pose": "engaging in dynamic action stance reflecting kayn's style"
  },
  "Kennen": {
    "trait": "inspired by kennen, ",
    "pose": "engaging in dynamic action stance reflecting kennen's style"
  },
  "Kha'Zix": {
    "trait": "inspired by kha'zix, ",
    "pose": "engaging in dynamic action stance reflecting kha'zix's style"
  },
  "Kindred": {
    "trait": "inspired by kindred, ",
    "pose": "engaging in dynamic action stance reflecting kindred's style"
  },
  "Kled": {
    "trait": "inspired by kled, ",
    "pose": "engaging in dynamic action stance reflecting kled's style"
  },
  "Kog'Maw": {
    "trait": "inspired by kog'maw, ",
    "pose": "engaging in dynamic action stance reflecting kog'maw's style"
  },
  "LeBlanc": {
    "trait": "inspired by leblanc, ",
    "pose": "engaging in dynamic action stance reflecting leblanc's style"
  },
  "Lee Sin": {
    "trait": "inspired by lee sin, ",
    "pose": "engaging in dynamic action stance reflecting lee sin's style"
  },
  "Leona": {
    "trait": "inspired by leona, ",
    "pose": "engaging in dynamic action stance reflecting leona's style"
  },
  "Lillia": {
    "trait": "inspired by lillia, ",
    "pose": "engaging in dynamic action stance reflecting lillia's style"
  },
  "Lissandra": {
    "trait": "inspired by lissandra, ",
    "pose": "engaging in dynamic action stance reflecting lissandra's style"
  },
  "Lucian": {
    "trait": "inspired by lucian, ",
    "pose": "engaging in dynamic action stance reflecting lucian's style"
  },
  "Lulu": {
    "trait": "inspired by lulu, ",
    "pose": "engaging in dynamic action stance reflecting lulu's style"
  },
  "Lux": {
    "trait": "inspired by lux, ",
    "pose": "engaging in dynamic action stance reflecting lux's style"
  },
  "Malphite": {
    "trait": "inspired by malphite, ",
    "pose": "engaging in dynamic action stance reflecting malphite's style"
  },
  "Malzahar": {
    "trait": "inspired by malzahar, ",
    "pose": "engaging in dynamic action stance reflecting malzahar's style"
  },
  "Maokai": {
    "trait": "inspired by maokai, ",
    "pose": "engaging in dynamic action stance reflecting maokai's style"
  },
  "Master Yi": {
    "trait": "inspired by master yi, ",
    "pose": "engaging in dynamic action stance reflecting master yi's style"
  },
  "Milio": {
    "trait": "inspired by milio, ",
    "pose": "engaging in dynamic action stance reflecting milio's style"
  },
  "Miss Fortune": {
    "trait": "inspired by miss fortune, ",
    "pose": "engaging in dynamic action stance reflecting miss fortune's style"
  },
  "Mordekaiser": {
    "trait": "inspired by mordekaiser, ",
    "pose": "engaging in dynamic action stance reflecting mordekaiser's style"
  },
  "Morgana": {
    "trait": "inspired by morgana, ",
    "pose": "engaging in dynamic action stance reflecting morgana's style"
  },
  "Naafiri": {
    "trait": "inspired by naafiri, ",
    "pose": "engaging in dynamic action stance reflecting naafiri's style"
  },
  "Nami": {
    "trait": "inspired by nami, ",
    "pose": "engaging in dynamic action stance reflecting nami's style"
  },
  "Nasus": {
    "trait": "inspired by nasus, ",
    "pose": "engaging in dynamic action stance reflecting nasus's style"
  },
  "Nautilus": {
    "trait": "inspired by nautilus, ",
    "pose": "engaging in dynamic action stance reflecting nautilus's style"
  },
  "Neeko": {
    "trait": "inspired by neeko, ",
    "pose": "engaging in dynamic action stance reflecting neeko's style"
  },
  "Nidalee": {
    "trait": "inspired by nidalee, ",
    "pose": "engaging in dynamic action stance reflecting nidalee's style"
  },
  "Nilah": {
    "trait": "inspired by nilah, ",
    "pose": "engaging in dynamic action stance reflecting nilah's style"
  },
  "Nocturne": {
    "trait": "inspired by nocturne, ",
    "pose": "engaging in dynamic action stance reflecting nocturne's style"
  },
  "Nunu & Willump": {
    "trait": "inspired by nunu & willump, ",
    "pose": "engaging in dynamic action stance reflecting nunu & willump's style"
  },
  "Olaf": {
    "trait": "inspired by olaf, ",
    "pose": "engaging in dynamic action stance reflecting olaf's style"
  },
  "Orianna": {
    "trait": "inspired by orianna, ",
    "pose": "engaging in dynamic action stance reflecting orianna's style"
  },
  "Ornn": {
    "trait": "inspired by ornn, ",
    "pose": "engaging in dynamic action stance reflecting ornn's style"
  },
  "Pantheon": {
    "trait": "inspired by pantheon, ",
    "pose": "engaging in dynamic action stance reflecting pantheon's style"
  },
  "Poppy": {
    "trait": "inspired by poppy, ",
    "pose": "engaging in dynamic action stance reflecting poppy's style"
  },
  "Pyke": {
    "trait": "inspired by pyke, ",
    "pose": "engaging in dynamic action stance reflecting pyke's style"
  },
  "Qiyana": {
    "trait": "inspired by qiyana, ",
    "pose": "engaging in dynamic action stance reflecting qiyana's style"
  },
  "Quinn": {
    "trait": "inspired by quinn, ",
    "pose": "engaging in dynamic action stance reflecting quinn's style"
  },
  "Rakan": {
    "trait": "inspired by rakan, ",
    "pose": "engaging in dynamic action stance reflecting rakan's style"
  },
  "Rammus": {
    "trait": "inspired by rammus, ",
    "pose": "engaging in dynamic action stance reflecting rammus's style"
  },
  "Rek'Sai": {
    "trait": "inspired by rek'sai, ",
    "pose": "engaging in dynamic action stance reflecting rek'sai's style"
  },
  "Rell": {
    "trait": "inspired by rell, ",
    "pose": "engaging in dynamic action stance reflecting rell's style"
  },
  "Renata Glasc": {
    "trait": "inspired by renata glasc, ",
    "pose": "engaging in dynamic action stance reflecting renata glasc's style"
  },
  "Renekton": {
    "trait": "inspired by renekton, ",
    "pose": "engaging in dynamic action stance reflecting renekton's style"
  },
  "Rengar": {
    "trait": "inspired by rengar, ",
    "pose": "engaging in dynamic action stance reflecting rengar's style"
  },
  "Riven": {
    "trait": "inspired by riven, ",
    "pose": "engaging in dynamic action stance reflecting riven's style"
  },
  "Rumble": {
    "trait": "inspired by rumble, ",
    "pose": "engaging in dynamic action stance reflecting rumble's style"
  },
  "Ryze": {
    "trait": "inspired by ryze, ",
    "pose": "engaging in dynamic action stance reflecting ryze's style"
  },
  "Samira": {
    "trait": "inspired by samira, ",
    "pose": "engaging in dynamic action stance reflecting samira's style"
  },
  "Sejuani": {
    "trait": "inspired by sejuani, ",
    "pose": "engaging in dynamic action stance reflecting sejuani's style"
  },
  "Senna": {
    "trait": "inspired by senna, ",
    "pose": "engaging in dynamic action stance reflecting senna's style"
  },
  "Seraphine": {
    "trait": "inspired by seraphine, ",
    "pose": "engaging in dynamic action stance reflecting seraphine's style"
  },
  "Sett": {
    "trait": "inspired by sett, ",
    "pose": "engaging in dynamic action stance reflecting sett's style"
  },
  "Shaco": {
    "trait": "inspired by shaco, ",
    "pose": "engaging in dynamic action stance reflecting shaco's style"
  },
  "Shen": {
    "trait": "inspired by shen, ",
    "pose": "engaging in dynamic action stance reflecting shen's style"
  },
  "Shyvana": {
    "trait": "inspired by shyvana, ",
    "pose": "engaging in dynamic action stance reflecting shyvana's style"
  },
  "Singed": {
    "trait": "inspired by singed, ",
    "pose": "engaging in dynamic action stance reflecting singed's style"
  },
  "Sion": {
    "trait": "inspired by sion, ",
    "pose": "engaging in dynamic action stance reflecting sion's style"
  },
  "Sivir": {
    "trait": "inspired by sivir, ",
    "pose": "engaging in dynamic action stance reflecting sivir's style"
  },
  "Skarner": {
    "trait": "inspired by skarner, ",
    "pose": "engaging in dynamic action stance reflecting skarner's style"
  },
  "Smolder": {
    "trait": "inspired by smolder, ",
    "pose": "engaging in dynamic action stance reflecting smolder's style"
  },
  "Sona": {
    "trait": "inspired by sona, ",
    "pose": "engaging in dynamic action stance reflecting sona's style"
  },
  "Soraka": {
    "trait": "inspired by soraka, ",
    "pose": "engaging in dynamic action stance reflecting soraka's style"
  },
  "Swain": {
    "trait": "inspired by swain, ",
    "pose": "engaging in dynamic action stance reflecting swain's style"
  },
  "Sylas": {
    "trait": "inspired by sylas, ",
    "pose": "engaging in dynamic action stance reflecting sylas's style"
  },
  "Syndra": {
    "trait": "inspired by syndra, ",
    "pose": "engaging in dynamic action stance reflecting syndra's style"
  },
  "Tahm Kench": {
    "trait": "inspired by tahm kench, ",
    "pose": "engaging in dynamic action stance reflecting tahm kench's style"
  },
  "Taliyah": {
    "trait": "inspired by taliyah, ",
    "pose": "engaging in dynamic action stance reflecting taliyah's style"
  },
  "Talon": {
    "trait": "inspired by talon, ",
    "pose": "engaging in dynamic action stance reflecting talon's style"
  },
  "Taric": {
    "trait": "inspired by taric, ",
    "pose": "engaging in dynamic action stance reflecting taric's style"
  },
  "Teemo": {
    "trait": "inspired by teemo, ",
    "pose": "engaging in dynamic action stance reflecting teemo's style"
  },
  "Thresh": {
    "trait": "inspired by thresh, ",
    "pose": "engaging in dynamic action stance reflecting thresh's style"
  },
  "Tristana": {
    "trait": "inspired by tristana, ",
    "pose": "engaging in dynamic action stance reflecting tristana's style"
  },
  "Trundle": {
    "trait": "inspired by trundle, ",
    "pose": "engaging in dynamic action stance reflecting trundle's style"
  },
  "Tryndamere": {
    "trait": "inspired by tryndamere, ",
    "pose": "engaging in dynamic action stance reflecting tryndamere's style"
  },
  "Twisted Fate": {
    "trait": "inspired by twisted fate, ",
    "pose": "engaging in dynamic action stance reflecting twisted fate's style"
  },
  "Twitch": {
    "trait": "inspired by twitch, ",
    "pose": "engaging in dynamic action stance reflecting twitch's style"
  },
  "Udyr": {
    "trait": "inspired by udyr, ",
    "pose": "engaging in dynamic action stance reflecting udyr's style"
  },
  "Urgot": {
    "trait": "inspired by urgot, ",
    "pose": "engaging in dynamic action stance reflecting urgot's style"
  },
  "Varus": {
    "trait": "inspired by varus, ",
    "pose": "engaging in dynamic action stance reflecting varus's style"
  },
  "Vayne": {
    "trait": "inspired by vayne, ",
    "pose": "engaging in dynamic action stance reflecting vayne's style"
  },
  "Veigar": {
    "trait": "inspired by veigar, ",
    "pose": "engaging in dynamic action stance reflecting veigar's style"
  },
  "Vel'Koz": {
    "trait": "inspired by vel'koz, ",
    "pose": "engaging in dynamic action stance reflecting vel'koz's style"
  },
  "Vex": {
    "trait": "inspired by vex, ",
    "pose": "engaging in dynamic action stance reflecting vex's style"
  },
  "Vi": {
    "trait": "inspired by vi, ",
    "pose": "engaging in dynamic action stance reflecting vi's style"
  },
  "Viego": {
    "trait": "inspired by viego, ",
    "pose": "engaging in dynamic action stance reflecting viego's style"
  },
  "Viktor": {
    "trait": "inspired by viktor, ",
    "pose": "engaging in dynamic action stance reflecting viktor's style"
  },
  "Vladimir": {
    "trait": "inspired by vladimir, ",
    "pose": "engaging in dynamic action stance reflecting vladimir's style"
  },
  "Volibear": {
    "trait": "inspired by volibear, ",
    "pose": "engaging in dynamic action stance reflecting volibear's style"
  },
  "Warwick": {
    "trait": "inspired by warwick, ",
    "pose": "engaging in dynamic action stance reflecting warwick's style"
  },
  "Wukong": {
    "trait": "inspired by wukong, ",
    "pose": "engaging in dynamic action stance reflecting wukong's style"
  },
  "Xayah": {
    "trait": "inspired by xayah, ",
    "pose": "engaging in dynamic action stance reflecting xayah's style"
  },
  "Xerath": {
    "trait": "inspired by xerath, ",
    "pose": "engaging in dynamic action stance reflecting xerath's style"
  },
  "Xin Zhao": {
    "trait": "inspired by xin zhao, ",
    "pose": "engaging in dynamic action stance reflecting xin zhao's style"
  },
  "Yasuo": {
    "trait": "inspired by yasuo, ",
    "pose": "engaging in dynamic action stance reflecting yasuo's style"
  },
  "Yone": {
    "trait": "inspired by yone, ",
    "pose": "engaging in dynamic action stance reflecting yone's style"
  },
  "Yorick": {
    "trait": "inspired by yorick, ",
    "pose": "engaging in dynamic action stance reflecting yorick's style"
  },
  "Yuumi": {
    "trait": "inspired by yuumi, ",
    "pose": "engaging in dynamic action stance reflecting yuumi's style"
  },
  "Zac": {
    "trait": "inspired by zac, ",
    "pose": "engaging in dynamic action stance reflecting zac's style"
  },
  "Zed": {
    "trait": "inspired by zed, ",
    "pose": "engaging in dynamic action stance reflecting zed's style"
  },
  "Zeri": {
    "trait": "inspired by zeri, ",
    "pose": "engaging in dynamic action stance reflecting zeri's style"
  },
  "Ziggs": {
    "trait": "inspired by ziggs, ",
    "pose": "engaging in dynamic action stance reflecting ziggs's style"
  },
  "Zilean": {
    "trait": "inspired by zilean, ",
    "pose": "engaging in dynamic action stance reflecting zilean's style"
  },
  "Zoe": {
    "trait": "inspired by zoe, ",
    "pose": "engaging in dynamic action stance reflecting zoe's style"
  },
  "Zyra": {
    "trait": "inspired by zyra, ",
    "pose": "engaging in dynamic action stance reflecting zyra's style"
  }
}

# 고정된 스타일 및 색상 조합
style = "A full-body shot of one single realistic detailed humanoid  . The mech is equipped with tactical armor plating . The scene is set in a desert asphalt  under natural sunlight at 3pm, casting sharp shadows. The mech features a two-tone color scheme of gray and brown. "

# "runwayml/stable-diffusion-v1-5",
pipe = StableDiffusionPipeline.from_pretrained(
    "Lykon/dreamshaper-8",
    torch_dtype=torch.float16
).to("cuda")

os.makedirs("outputs", exist_ok=True)

for name, desc in champions.items():
    prompt = f"{name}, {desc['trait']}, {style}"
    print(f"🎨 Generating {name}...")
    image = pipe(prompt, width=720, height=1280).images[0]
    image.save(f"outputs/{name}.png")

print("✅ All champion portraits saved in /outputs")
