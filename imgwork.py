import torch
from diffusers import StableDiffusionPipeline
import os
from PIL import Image

champions = {
  "Aatrox": {
    "trait": "a themed battle mech inspired by aatrox, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting aatrox's style"
  },
  "Ahri": {
    "trait": "a themed battle mech inspired by ahri, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ahri's style"
  },
  "Akali": {
    "trait": "a themed battle mech inspired by akali, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting akali's style"
  },
  "Alistar": {
    "trait": "a themed battle mech inspired by alistar, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting alistar's style"
  },
  "Amumu": {
    "trait": "a themed battle mech inspired by amumu, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting amumu's style"
  },
  "Anivia": {
    "trait": "a themed battle mech inspired by anivia, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting anivia's style"
  },
  "Annie": {
    "trait": "a themed battle mech inspired by annie, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting annie's style"
  },
  "Aphelios": {
    "trait": "a themed battle mech inspired by aphelios, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting aphelios's style"
  },
  "Ashe": {
    "trait": "a themed battle mech inspired by ashe, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ashe's style"
  },
  "Aurelion Sol": {
    "trait": "a themed battle mech inspired by aurelion sol, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting aurelion sol's style"
  },
  "Azir": {
    "trait": "a themed battle mech inspired by azir, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting azir's style"
  },
  "Bard": {
    "trait": "a themed battle mech inspired by bard, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting bard's style"
  },
  "Bel'Veth": {
    "trait": "a themed battle mech inspired by bel'veth, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting bel'veth's style"
  },
  "Blitzcrank": {
    "trait": "a themed battle mech inspired by blitzcrank, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting blitzcrank's style"
  },
  "Brand": {
    "trait": "a themed battle mech inspired by brand, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting brand's style"
  },
  "Braum": {
    "trait": "a themed battle mech inspired by braum, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting braum's style"
  },
  "Caitlyn": {
    "trait": "a themed battle mech inspired by caitlyn, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting caitlyn's style"
  },
  "Camille": {
    "trait": "a themed battle mech inspired by camille, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting camille's style"
  },
  "Cassiopeia": {
    "trait": "a themed battle mech inspired by cassiopeia, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting cassiopeia's style"
  },
  "Cho'Gath": {
    "trait": "a themed battle mech inspired by cho'gath, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting cho'gath's style"
  },
  "Corki": {
    "trait": "a themed battle mech inspired by corki, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting corki's style"
  },
  "Darius": {
    "trait": "a themed battle mech inspired by darius, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting darius's style"
  },
  "Diana": {
    "trait": "a themed battle mech inspired by diana, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting diana's style"
  },
  "Dr. Mundo": {
    "trait": "a themed battle mech inspired by dr. mundo, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting dr. mundo's style"
  },
  "Draven": {
    "trait": "a themed battle mech inspired by draven, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting draven's style"
  },
  "Ekko": {
    "trait": "a themed battle mech inspired by ekko, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ekko's style"
  },
  "Elise": {
    "trait": "a themed battle mech inspired by elise, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting elise's style"
  },
  "Evelynn": {
    "trait": "a themed battle mech inspired by evelynn, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting evelynn's style"
  },
  "Ezreal": {
    "trait": "a themed battle mech inspired by ezreal, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ezreal's style"
  },
  "Fiddlesticks": {
    "trait": "a themed battle mech inspired by fiddlesticks, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting fiddlesticks's style"
  },
  "Fiora": {
    "trait": "a themed battle mech inspired by fiora, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting fiora's style"
  },
  "Fizz": {
    "trait": "a themed battle mech inspired by fizz, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting fizz's style"
  },
  "Galio": {
    "trait": "a themed battle mech inspired by galio, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting galio's style"
  },
  "Gangplank": {
    "trait": "a themed battle mech inspired by gangplank, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting gangplank's style"
  },
  "Garen": {
    "trait": "a themed battle mech inspired by garen, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting garen's style"
  },
  "Gnar": {
    "trait": "a themed battle mech inspired by gnar, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting gnar's style"
  },
  "Gragas": {
    "trait": "a themed battle mech inspired by gragas, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting gragas's style"
  },
  "Graves": {
    "trait": "a themed battle mech inspired by graves, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting graves's style"
  },
  "Gwen": {
    "trait": "a themed battle mech inspired by gwen, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting gwen's style"
  },
  "Hecarim": {
    "trait": "a themed battle mech inspired by hecarim, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting hecarim's style"
  },
  "Heimerdinger": {
    "trait": "a themed battle mech inspired by heimerdinger, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting heimerdinger's style"
  },
  "Illaoi": {
    "trait": "a themed battle mech inspired by illaoi, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting illaoi's style"
  },
  "Irelia": {
    "trait": "a themed battle mech inspired by irelia, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting irelia's style"
  },
  "Ivern": {
    "trait": "a themed battle mech inspired by ivern, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ivern's style"
  },
  "Janna": {
    "trait": "a themed battle mech inspired by janna, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting janna's style"
  },
  "Jarvan IV": {
    "trait": "a themed battle mech inspired by jarvan iv, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting jarvan iv's style"
  },
  "Jax": {
    "trait": "a themed battle mech inspired by jax, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting jax's style"
  },
  "Jayce": {
    "trait": "a themed battle mech inspired by jayce, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting jayce's style"
  },
  "Jhin": {
    "trait": "a themed battle mech inspired by jhin, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting jhin's style"
  },
  "Jinx": {
    "trait": "a themed battle mech inspired by jinx, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting jinx's style"
  },
  "K'Sante": {
    "trait": "a themed battle mech inspired by k'sante, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting k'sante's style"
  },
  "Kai'Sa": {
    "trait": "a themed battle mech inspired by kai'sa, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kai'sa's style"
  },
  "Kalista": {
    "trait": "a themed battle mech inspired by kalista, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kalista's style"
  },
  "Karma": {
    "trait": "a themed battle mech inspired by karma, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting karma's style"
  },
  "Karthus": {
    "trait": "a themed battle mech inspired by karthus, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting karthus's style"
  },
  "Kassadin": {
    "trait": "a themed battle mech inspired by kassadin, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kassadin's style"
  },
  "Katarina": {
    "trait": "a themed battle mech inspired by katarina, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting katarina's style"
  },
  "Kayle": {
    "trait": "a themed battle mech inspired by kayle, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kayle's style"
  },
  "Kayn": {
    "trait": "a themed battle mech inspired by kayn, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kayn's style"
  },
  "Kennen": {
    "trait": "a themed battle mech inspired by kennen, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kennen's style"
  },
  "Kha'Zix": {
    "trait": "a themed battle mech inspired by kha'zix, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kha'zix's style"
  },
  "Kindred": {
    "trait": "a themed battle mech inspired by kindred, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kindred's style"
  },
  "Kled": {
    "trait": "a themed battle mech inspired by kled, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kled's style"
  },
  "Kog'Maw": {
    "trait": "a themed battle mech inspired by kog'maw, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting kog'maw's style"
  },
  "LeBlanc": {
    "trait": "a themed battle mech inspired by leblanc, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting leblanc's style"
  },
  "Lee Sin": {
    "trait": "a themed battle mech inspired by lee sin, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting lee sin's style"
  },
  "Leona": {
    "trait": "a themed battle mech inspired by leona, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting leona's style"
  },
  "Lillia": {
    "trait": "a themed battle mech inspired by lillia, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting lillia's style"
  },
  "Lissandra": {
    "trait": "a themed battle mech inspired by lissandra, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting lissandra's style"
  },
  "Lucian": {
    "trait": "a themed battle mech inspired by lucian, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting lucian's style"
  },
  "Lulu": {
    "trait": "a themed battle mech inspired by lulu, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting lulu's style"
  },
  "Lux": {
    "trait": "a themed battle mech inspired by lux, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting lux's style"
  },
  "Malphite": {
    "trait": "a themed battle mech inspired by malphite, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting malphite's style"
  },
  "Malzahar": {
    "trait": "a themed battle mech inspired by malzahar, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting malzahar's style"
  },
  "Maokai": {
    "trait": "a themed battle mech inspired by maokai, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting maokai's style"
  },
  "Master Yi": {
    "trait": "a themed battle mech inspired by master yi, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting master yi's style"
  },
  "Milio": {
    "trait": "a themed battle mech inspired by milio, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting milio's style"
  },
  "Miss Fortune": {
    "trait": "a themed battle mech inspired by miss fortune, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting miss fortune's style"
  },
  "Mordekaiser": {
    "trait": "a themed battle mech inspired by mordekaiser, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting mordekaiser's style"
  },
  "Morgana": {
    "trait": "a themed battle mech inspired by morgana, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting morgana's style"
  },
  "Naafiri": {
    "trait": "a themed battle mech inspired by naafiri, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting naafiri's style"
  },
  "Nami": {
    "trait": "a themed battle mech inspired by nami, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nami's style"
  },
  "Nasus": {
    "trait": "a themed battle mech inspired by nasus, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nasus's style"
  },
  "Nautilus": {
    "trait": "a themed battle mech inspired by nautilus, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nautilus's style"
  },
  "Neeko": {
    "trait": "a themed battle mech inspired by neeko, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting neeko's style"
  },
  "Nidalee": {
    "trait": "a themed battle mech inspired by nidalee, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nidalee's style"
  },
  "Nilah": {
    "trait": "a themed battle mech inspired by nilah, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nilah's style"
  },
  "Nocturne": {
    "trait": "a themed battle mech inspired by nocturne, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nocturne's style"
  },
  "Nunu & Willump": {
    "trait": "a themed battle mech inspired by nunu & willump, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting nunu & willump's style"
  },
  "Olaf": {
    "trait": "a themed battle mech inspired by olaf, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting olaf's style"
  },
  "Orianna": {
    "trait": "a themed battle mech inspired by orianna, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting orianna's style"
  },
  "Ornn": {
    "trait": "a themed battle mech inspired by ornn, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ornn's style"
  },
  "Pantheon": {
    "trait": "a themed battle mech inspired by pantheon, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting pantheon's style"
  },
  "Poppy": {
    "trait": "a themed battle mech inspired by poppy, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting poppy's style"
  },
  "Pyke": {
    "trait": "a themed battle mech inspired by pyke, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting pyke's style"
  },
  "Qiyana": {
    "trait": "a themed battle mech inspired by qiyana, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting qiyana's style"
  },
  "Quinn": {
    "trait": "a themed battle mech inspired by quinn, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting quinn's style"
  },
  "Rakan": {
    "trait": "a themed battle mech inspired by rakan, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting rakan's style"
  },
  "Rammus": {
    "trait": "a themed battle mech inspired by rammus, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting rammus's style"
  },
  "Rek'Sai": {
    "trait": "a themed battle mech inspired by rek'sai, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting rek'sai's style"
  },
  "Rell": {
    "trait": "a themed battle mech inspired by rell, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting rell's style"
  },
  "Renata Glasc": {
    "trait": "a themed battle mech inspired by renata glasc, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting renata glasc's style"
  },
  "Renekton": {
    "trait": "a themed battle mech inspired by renekton, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting renekton's style"
  },
  "Rengar": {
    "trait": "a themed battle mech inspired by rengar, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting rengar's style"
  },
  "Riven": {
    "trait": "a themed battle mech inspired by riven, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting riven's style"
  },
  "Rumble": {
    "trait": "a themed battle mech inspired by rumble, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting rumble's style"
  },
  "Ryze": {
    "trait": "a themed battle mech inspired by ryze, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ryze's style"
  },
  "Samira": {
    "trait": "a themed battle mech inspired by samira, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting samira's style"
  },
  "Sejuani": {
    "trait": "a themed battle mech inspired by sejuani, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting sejuani's style"
  },
  "Senna": {
    "trait": "a themed battle mech inspired by senna, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting senna's style"
  },
  "Seraphine": {
    "trait": "a themed battle mech inspired by seraphine, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting seraphine's style"
  },
  "Sett": {
    "trait": "a themed battle mech inspired by sett, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting sett's style"
  },
  "Shaco": {
    "trait": "a themed battle mech inspired by shaco, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting shaco's style"
  },
  "Shen": {
    "trait": "a themed battle mech inspired by shen, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting shen's style"
  },
  "Shyvana": {
    "trait": "a themed battle mech inspired by shyvana, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting shyvana's style"
  },
  "Singed": {
    "trait": "a themed battle mech inspired by singed, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting singed's style"
  },
  "Sion": {
    "trait": "a themed battle mech inspired by sion, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting sion's style"
  },
  "Sivir": {
    "trait": "a themed battle mech inspired by sivir, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting sivir's style"
  },
  "Skarner": {
    "trait": "a themed battle mech inspired by skarner, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting skarner's style"
  },
  "Smolder": {
    "trait": "a themed battle mech inspired by smolder, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting smolder's style"
  },
  "Sona": {
    "trait": "a themed battle mech inspired by sona, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting sona's style"
  },
  "Soraka": {
    "trait": "a themed battle mech inspired by soraka, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting soraka's style"
  },
  "Swain": {
    "trait": "a themed battle mech inspired by swain, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting swain's style"
  },
  "Sylas": {
    "trait": "a themed battle mech inspired by sylas, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting sylas's style"
  },
  "Syndra": {
    "trait": "a themed battle mech inspired by syndra, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting syndra's style"
  },
  "Tahm Kench": {
    "trait": "a themed battle mech inspired by tahm kench, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting tahm kench's style"
  },
  "Taliyah": {
    "trait": "a themed battle mech inspired by taliyah, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting taliyah's style"
  },
  "Talon": {
    "trait": "a themed battle mech inspired by talon, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting talon's style"
  },
  "Taric": {
    "trait": "a themed battle mech inspired by taric, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting taric's style"
  },
  "Teemo": {
    "trait": "a themed battle mech inspired by teemo, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting teemo's style"
  },
  "Thresh": {
    "trait": "a themed battle mech inspired by thresh, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting thresh's style"
  },
  "Tristana": {
    "trait": "a themed battle mech inspired by tristana, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting tristana's style"
  },
  "Trundle": {
    "trait": "a themed battle mech inspired by trundle, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting trundle's style"
  },
  "Tryndamere": {
    "trait": "a themed battle mech inspired by tryndamere, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting tryndamere's style"
  },
  "Twisted Fate": {
    "trait": "a themed battle mech inspired by twisted fate, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting twisted fate's style"
  },
  "Twitch": {
    "trait": "a themed battle mech inspired by twitch, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting twitch's style"
  },
  "Udyr": {
    "trait": "a themed battle mech inspired by udyr, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting udyr's style"
  },
  "Urgot": {
    "trait": "a themed battle mech inspired by urgot, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting urgot's style"
  },
  "Varus": {
    "trait": "a themed battle mech inspired by varus, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting varus's style"
  },
  "Vayne": {
    "trait": "a themed battle mech inspired by vayne, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting vayne's style"
  },
  "Veigar": {
    "trait": "a themed battle mech inspired by veigar, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting veigar's style"
  },
  "Vel'Koz": {
    "trait": "a themed battle mech inspired by vel'koz, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting vel'koz's style"
  },
  "Vex": {
    "trait": "a themed battle mech inspired by vex, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting vex's style"
  },
  "Vi": {
    "trait": "a themed battle mech inspired by vi, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting vi's style"
  },
  "Viego": {
    "trait": "a themed battle mech inspired by viego, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting viego's style"
  },
  "Viktor": {
    "trait": "a themed battle mech inspired by viktor, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting viktor's style"
  },
  "Vladimir": {
    "trait": "a themed battle mech inspired by vladimir, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting vladimir's style"
  },
  "Volibear": {
    "trait": "a themed battle mech inspired by volibear, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting volibear's style"
  },
  "Warwick": {
    "trait": "a themed battle mech inspired by warwick, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting warwick's style"
  },
  "Wukong": {
    "trait": "a themed battle mech inspired by wukong, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting wukong's style"
  },
  "Xayah": {
    "trait": "a themed battle mech inspired by xayah, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting xayah's style"
  },
  "Xerath": {
    "trait": "a themed battle mech inspired by xerath, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting xerath's style"
  },
  "Xin Zhao": {
    "trait": "a themed battle mech inspired by xin zhao, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting xin zhao's style"
  },
  "Yasuo": {
    "trait": "a themed battle mech inspired by yasuo, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting yasuo's style"
  },
  "Yone": {
    "trait": "a themed battle mech inspired by yone, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting yone's style"
  },
  "Yorick": {
    "trait": "a themed battle mech inspired by yorick, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting yorick's style"
  },
  "Yuumi": {
    "trait": "a themed battle mech inspired by yuumi, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting yuumi's style"
  },
  "Zac": {
    "trait": "a themed battle mech inspired by zac, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting zac's style"
  },
  "Zed": {
    "trait": "a themed battle mech inspired by zed, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting zed's style"
  },
  "Zeri": {
    "trait": "a themed battle mech inspired by zeri, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting zeri's style"
  },
  "Ziggs": {
    "trait": "a themed battle mech inspired by ziggs, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting ziggs's style"
  },
  "Zilean": {
    "trait": "a themed battle mech inspired by zilean, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting zilean's style"
  },
  "Zoe": {
    "trait": "a themed battle mech inspired by zoe, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting zoe's style"
  },
  "Zyra": {
    "trait": "a themed battle mech inspired by zyra, featuring tactical armor and signature weapon",
    "pose": "engaging in dynamic action stance reflecting zyra's style"
  }
}

# 고정된 스타일 및 색상 조합
style = "Robot style, full body, desert asphalt plaza at 3pm, natural lighting, 3D illustration, two-tone color scheme: dark gray and light brown"

pipe = StableDiffusionPipeline.from_pretrained(
    "Lykon/dreamshaper-8",
    torch_dtype=torch.float16
).to("cuda")

os.makedirs("outputs", exist_ok=True)

for name, desc in champions.items():
    prompt = f"{name}, {desc['trait']}, {desc['pose']}, {style}"
    print(f"🎨 Generating {name}...")
    image = pipe(prompt, width=720, height=1280).images[0]
    image.save(f"outputs/{name}.png")

print("✅ All champion portraits saved in /outputs")
