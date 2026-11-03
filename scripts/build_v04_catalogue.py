"""Reproduce the frozen historical 0.4 baseline (47 x 20).

Current catalogue maintenance uses build_expanded_catalogue.py, without quotas.
"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'research/catalogue-v0.4'
spec=importlib.util.spec_from_file_location('research_catalogue',ROOT/'scripts/research_catalogue_v04.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

STEAM_FIXES={'Returnal':1649240,'HELLDIVERS 2':553850,'ENDLESS Legend':289130,'ENDLESS Space 2':392110,'Anno 2070':48240,'STAR WARS: Knights of the Old Republic':32370,'STAR WARS Knights of the Old Republic II: The Sith Lords':208580,'SimCity 4 Deluxe':24780,'Monument Valley: Panoramic Edition':1927720,'TOEM':1307580,'Amnesia: Memories':359390,'Crash Bandicoot 4: It\'s About Time':1378990,'EA SPORTS FC 24':2195250,'NBA 2K Playgrounds 2':726590,'Nightmares from the Deep: The Cursed Heart':259740,'Rayman Legends':242550,'Sonic Generations Collection':71340,'Tales of Berseria':429660,'Rocket League':252950,'DiRT Rally':310560,'HUMANKIND':1124300,'DEATH STRANDING':1190460}

STEAM_FIXES.update({'Castlevania: Lords of Shadow - Ultimate Edition':234080,"Raiden V: Director's Cut":570050,'Mortal Kombat 11':976310,'Mortal Kombat 1':1971870,'NARUTO SHIPPUDEN: Ultimate Ninja STORM 4':349040,'The Witcher 3: Wild Hunt':292030,'Valkyria Chronicles':294860,'Sea of Stars':1244090})
STEAM_FIXES.update({'Satisfactory':526870,'shapez 2':2162800,'Graveyard Keeper':599140,'Microsoft Flight Simulator':1250410,'X-Plane 12':2014780,'The Sims 3':47890,'Shenmue I & II':758330,'Warhammer 40,000: Dawn of War - Anniversary Edition':4570,'Warhammer 40,000: Dawn of War II - Anniversary Edition':15620,'Stronghold Crusader HD':40970,'Northgard':466560,'Defense Grid 2':221540,'Eastside Hockey Manager':301120,'Skater XL':962730,'PGA TOUR 2K23':1588010,'SOMA':282140,'Resident Evil HD REMASTER':304240})

CONSOLE={
'METAL GEAR RISING: REVENGEANCE':('合金装备崛起 复仇','https://www.konami.com/games/eu/en/products/mgr/',['PC','PlayStation 3','Xbox 360']),
'NINJA GAIDEN: Master Collection':('忍者龙剑传 大师合集','https://teamninja-studio.com/ngmc/us/',['PC','PlayStation','Xbox','Nintendo Switch']),
'Super Mario Odyssey':('超级马力欧 奥德赛','https://www.nintendo.com/us/store/products/super-mario-odyssey-switch/',['Nintendo Switch']),
'Super Mario Bros. Wonder':('超级马力欧兄弟 惊奇','https://www.nintendo.com/us/store/products/super-mario-bros-wonder-switch/',['Nintendo Switch']),
'ASTRO BOT':('宇宙机器人','https://www.playstation.com/en-us/games/astro-bot/',['PlayStation 5']),
"Astro's Playroom":('宇宙机器人 无线控制器使用指南','https://www.playstation.com/en-us/games/astros-playroom/',['PlayStation 5']),
'Donkey Kong Country: Tropical Freeze':('森喜刚国度 热带寒流','https://www.nintendo.com/us/store/products/donkey-kong-country-tropical-freeze-switch/',['Nintendo Switch']),
'Super Smash Bros. Ultimate':('任天堂明星大乱斗 特别版','https://www.nintendo.com/us/store/products/super-smash-bros-ultimate-switch/',['Nintendo Switch']),
'Animal Crossing: New Horizons':('集合啦！动物森友会','https://www.nintendo.com/us/store/products/animal-crossing-new-horizons-switch/',['Nintendo Switch']),
'Metroid Dread':('密特罗德 生存恐惧','https://www.nintendo.com/us/store/products/metroid-dread-switch/',['Nintendo Switch']),
'Metroid Prime Remastered':('密特罗德 究极 复刻版','https://www.nintendo.com/us/store/products/metroid-prime-remastered-switch/',['Nintendo Switch']),
'13 Sentinels: Aegis Rim':('十三机兵防卫圈','https://atlus.com/13sentinels/',['PlayStation 4','Nintendo Switch']),
'Fire Emblem: Three Houses':('火焰之纹章 风花雪月','https://www.nintendo.com/us/store/products/fire-emblem-three-houses-switch/',['Nintendo Switch']),
'Fire Emblem Engage':('火焰之纹章 Engage','https://www.nintendo.com/us/store/products/fire-emblem-engage-switch/',['Nintendo Switch']),
'Unicorn Overlord':('圣兽之王','https://unicornoverlord.atlus.com/',['Nintendo Switch','PlayStation','Xbox']),
'Xenoblade Chronicles: Definitive Edition':('异度神剑 决定版','https://www.nintendo.com/us/store/products/xenoblade-chronicles-definitive-edition-switch/',['Nintendo Switch']),
'Xenoblade Chronicles 2':('异度神剑2','https://www.nintendo.com/us/store/products/xenoblade-chronicles-2-switch/',['Nintendo Switch']),
'Xenoblade Chronicles 3':('异度神剑3','https://www.nintendo.com/us/store/products/xenoblade-chronicles-3-switch/',['Nintendo Switch']),
'Collar X Malice':('项圈×恶意','https://www.aksysgames.com/collar-malice/',['Nintendo Switch','PlayStation Vita']),
'Code: Realize - Guardian of Rebirth':('Code: Realize 创世的公主','https://www.aksysgames.com/code-realize/',['Nintendo Switch','PlayStation']),
'Cupid Parasite':('丘比特寄生','https://ideafintl.com/cupid-parasite/',['Nintendo Switch']),
'Piofiore: Fated Memories':('虔诚之花的晚钟','https://www.aksysgames.com/piofiore/',['Nintendo Switch','PlayStation Vita']),
'Birushana: Rising Flower of Genpei':('毗卢遮那战姬 源平飞花梦想','https://ideafintl.com/birushana/',['Nintendo Switch']),
'Jack Jeanne':('杰克贞德','https://www.aksysgames.com/jackjeanne/',['Nintendo Switch']),
'Minecraft':('我的世界','https://www.minecraft.net/en-us/about-minecraft',['PC','console']),
'Advance Wars 1+2: Re-Boot Camp':('高级战争1+2 重制营地','https://www.nintendo.com/us/store/products/advance-wars-1-plus-2-re-boot-camp-switch/',['Nintendo Switch']),
'StarCraft: Remastered':('星际争霸 重制版','https://starcraft.blizzard.com/',['PC']),
'StarCraft II':('星际争霸2','https://starcraft2.blizzard.com/',['PC']),
'Warcraft III':('魔兽争霸3','https://warcraft3.blizzard.com/',['PC']),
'Gran Turismo 7':('GT赛车7','https://www.playstation.com/en-us/games/gran-turismo-7/',['PlayStation 4','PlayStation 5']),
'Gran Turismo Sport':('GT Sport','https://www.gran-turismo.com/us/products/gtsport/',['PlayStation 4']),
'Mario Kart 8 Deluxe':('马力欧卡丁车8 豪华版','https://www.nintendo.com/us/store/products/mario-kart-8-deluxe-switch/',['Nintendo Switch']),
'Live for Speed':('Live for Speed','https://www.lfs.net/',['PC']),
'Richard Burns Rally':('理查德·伯恩斯拉力赛','https://www.mobygames.com/game/13913/richard-burns-rally/',['PC','PlayStation 2','Xbox']),
'MLB The Show 25':('MLB The Show 25','https://theshow.com/games/the-show-25/',['PlayStation','Xbox','Nintendo Switch']),
'MLB The Show 24':('MLB The Show 24','https://theshow.com/games/the-show-24/',['PlayStation','Xbox','Nintendo Switch']),
'NHL 25':('NHL 25','https://www.ea.com/games/nhl/nhl-25',['PlayStation','Xbox']),
'NHL 24':('NHL 24','https://www.ea.com/games/nhl/nhl-24',['PlayStation','Xbox']),
'skate 3':('滑板3','https://www.ea.com/games/skate/skate-3',['PlayStation 3','Xbox 360']),
'Mario Tennis Aces':('马力欧网球 王牌','https://www.nintendo.com/us/store/products/mario-tennis-aces-switch/',['Nintendo Switch']),
'Mario Golf: Super Rush':('马力欧高尔夫 超级冲冲冲','https://www.nintendo.com/us/store/products/mario-golf-super-rush-switch/',['Nintendo Switch']),
'Nintendo Switch Sports':('Nintendo Switch 运动','https://www.nintendo.com/us/store/products/nintendo-switch-sports-switch/',['Nintendo Switch']),
'Ring Fit Adventure':('健身环大冒险','https://www.nintendo.com/us/store/products/ring-fit-adventure-switch/',['Nintendo Switch']),
'The Legend of Zelda: Breath of the Wild':('塞尔达传说 旷野之息','https://www.nintendo.com/us/store/products/the-legend-of-zelda-breath-of-the-wild-switch/',['Nintendo Switch','Wii U']),
'The Legend of Zelda: Tears of the Kingdom':('塞尔达传说 王国之泪','https://www.nintendo.com/us/store/products/the-legend-of-zelda-tears-of-the-kingdom-switch/',['Nintendo Switch']),
'Alan Wake 2':('心灵杀手2','https://www.alanwake.com/',['PC','PlayStation 5','Xbox Series'])
}

# Chinese search aliases are editorial labels; they are not advertised as official localizations.
ZH={
'Counter-Strike 2':'反恐精英2|CS2|CSGO','DOOM Eternal':'毁灭战士 永恒','DOOM':'毁灭战士2016','Half-Life 2':'半条命2','Black Mesa':'黑山','Metro Exodus':'地铁 离去','Metro 2033 Redux':'地铁2033 重制版','Metro: Last Light Redux':'地铁 最后的曙光 重制版','Titanfall 2':'泰坦陨落2','ULTRAKILL':'究极杀戮','Deep Rock Galactic':'深岩银河','Left 4 Dead 2':'求生之路2','BioShock Remastered':'生化奇兵 重制版','BioShock Infinite':'生化奇兵 无限','Borderlands 2':'无主之地2','Borderlands 3':'无主之地3','Ready or Not':'严阵以待','Wolfenstein: The New Order':'德军总部 新秩序',
'Resident Evil 4':'生化危机4 重制版','Resident Evil 2':'生化危机2 重制版','Dead Space':'死亡空间 重制版','Control Ultimate Edition':'控制 终极版','Returnal':'死亡回归','Gears 5':'战争机器5','Max Payne 3':'马克思佩恩3','Grand Theft Auto V Enhanced':'侠盗猎车手5 增强版|GTA5|给他爱5','Red Dead Redemption 2':'荒野大镖客2|大表哥2|RDR2','HELLDIVERS 2':'绝地潜兵2|地狱潜者2','Risk of Rain 2':'雨中冒险2','Warframe':'星际战甲','Remnant: From the Ashes':'遗迹 灰烬重生','Remnant II':'遗迹2','Sniper Elite 4':'狙击精英4','Sniper Elite 5':'狙击精英5','Vanquish':'绝对征服','UNCHARTED: Legacy of Thieves Collection':'神秘海域 盗贼传奇合辑','The Last of Us Part I':'最后生还者 第一部|美国末日','Days Gone':'往日不再',
'Devil May Cry 5':'鬼泣5','Devil May Cry 4 Special Edition':'鬼泣4 特别版','Devil May Cry HD Collection':'鬼泣 高清合集','Bayonetta':'猎天使魔女','God of War':'战神2018','God of War Ragnarok':'战神 诸神黄昏','METAL GEAR RISING: REVENGEANCE':'合金装备崛起 复仇','Hi-Fi RUSH':'完美音浪','NieR:Automata':'尼尔 机械纪元','Darksiders Warmastered Edition':'暗黑血统 战神版','Darksiders II Deathinitive Edition':'暗黑血统2 终极版','Darksiders III':'暗黑血统3','DYNASTY WARRIORS: ORIGINS':'真三国无双 起源','Sifu':'师父',
'Crypt of the NecroDancer':'节奏地牢','Just Shapes & Beats':'形状节奏','Geometry Dash':'几何冲刺','Muse Dash':'喵斯快跑','Hatsune Miku: Project DIVA Mega Mix+':'初音未来 歌姬计划 Mega39s+','Rhythm Doctor':'节奏医生','A Dance of Fire and Ice':'冰与火之舞','Beat Saber':'节奏光剑','Metal: Hellsinger':'重金属 地狱歌手','Rayman Legends':'雷曼 传奇','Rayman Origins':'雷曼 起源','Celeste':'蔚蓝','Super Meat Boy':'超级食肉男孩','Shovel Knight: Treasure Trove':'铲子骑士','Sonic Mania':'索尼克 狂欢','Sonic Generations Collection':'索尼克 世代','Crash Bandicoot N. Sane Trilogy':'古惑狼 疯狂三部曲','Crash Bandicoot 4: It\'s About Time':'古惑狼4 时机已到','A Hat in Time':'时光之帽','It Takes Two':'双人成行','Sackboy: A Big Adventure':'麻布仔大冒险','Ori and the Blind Forest: Definitive Edition':'奥日与黑暗森林 终极版','Ori and the Will of the Wisps':'奥日与萤火意志','Psychonauts 2':'脑航员2',
'Ikaruga':'斑鸠','DoDonPachi Resurrection':'怒首领蜂大复活','Mushihimesama':'虫姬','Deathsmiles':'死亡微笑','Enter the Gungeon':'挺进地牢','Street Fighter 6':'街头霸王6','Street Fighter V':'街头霸王5','Ultra Street Fighter IV':'终极街头霸王4','TEKKEN 8':'铁拳8','TEKKEN 7':'铁拳7','Mortal Kombat 11':'真人快打11','Mortal Kombat 1':'真人快打1','GUILTY GEAR -STRIVE-':'罪恶装备 奋战','DRAGON BALL FighterZ':'龙珠斗士Z','Granblue Fantasy Versus: Rising':'碧蓝幻想Versus Rising','THE KING OF FIGHTERS XV':'拳皇15','BlazBlue Centralfiction':'苍翼默示录 神观之梦','NARUTO SHIPPUDEN: Ultimate Ninja STORM 4':'火影忍者疾风传 究极忍者风暴4','Absolver':'赦免者',
'Hidden Folks':'隐藏的家伙','Hidden Through Time':'穿越时空的隐藏物体','Tiny Lands':'小小世界','Stardew Valley':'星露谷物语','Unpacking':'拆箱','PowerWash Simulator':'冲就完事模拟器','A Short Hike':'短途徒步旅行','Dorfromantik':'多边形造物主','Mini Metro':'迷你地铁','Mini Motorways':'迷你高速公路','Townscaper':'城镇叠叠乐','Monument Valley: Panoramic Edition':'纪念碑谷','DAVE THE DIVER':'潜水员戴夫|戴夫','Balatro':'小丑牌','Plants vs. Zombies GOTY Edition':'植物大战僵尸 年度版','Bejeweled 3':'宝石迷阵3','Peggle Deluxe':'幻幻球','Katamari Damacy REROLL':'块魂 重制版','Untitled Goose Game':'捣蛋鹅','Donut County':'甜甜圈都市','TOEM':'TOEM 摄影冒险',
'Hollow Knight':'空洞骑士','Hollow Knight: Silksong':'空洞骑士 丝之歌','Dead Cells':'死亡细胞|重生细胞','Blasphemous':'渎神','Blasphemous 2':'渎神2','Bloodstained: Ritual of the Night':'赤痕 夜之仪式','ENDER LILIES: Quietus of the Knights':'终焉之莉莉 骑士寂夜','ENDER MAGNOLIA: Bloom in the Mist':'终焉之玛格诺利亚 雾中绽放','Prince of Persia The Lost Crown':'波斯王子 失落的王冠','ANIMAL WELL':'动物井','Nine Sols':'九日','Portal':'传送门','Portal 2':'传送门2','The Talos Principle':'塔罗斯的法则','The Talos Principle 2':'塔罗斯的法则2','The Witness':'见证者','Baba Is You':'巴巴是你','Patrick\'s Parabox':'帕特里克的箱子','Return of the Obra Dinn':'奥伯拉丁的回归','The Case of the Golden Idol':'黄金偶像案','The Rise of the Golden Idol':'黄金偶像崛起','Chants of Sennaar':'巴别塔圣歌','COCOON':'茧','Outer Wilds':'星际拓荒','Opus Magnum':'巨著','Human Resource Machine':'人力资源机器','World of Goo':'粘粘世界','The Room 4: Old Sins':'未上锁的房间4 旧罪',
'The Elder Scrolls V: Skyrim Special Edition':'上古卷轴5 天际 特别版','The Elder Scrolls IV: Oblivion Remastered':'上古卷轴4 湮灭 重制版','The Elder Scrolls III: Morrowind':'上古卷轴3 晨风','Kingdom Come: Deliverance':'天国 拯救','Kingdom Come: Deliverance II':'天国 拯救2|天国拯救2|KCD2','The Witcher 3: Wild Hunt':'巫师3 狂猎','The Witcher 2: Assassins of Kings Enhanced Edition':'巫师2 国王刺客','Cyberpunk 2077':'赛博朋克2077','Disco Elysium - The Final Cut':'极乐迪斯科 最终剪辑版','Baldur\'s Gate 3':'博德之门3','Divinity: Original Sin 2 - Definitive Edition':'神界 原罪2 终极版','Mass Effect Legendary Edition':'质量效应 传奇版','Dragon Age: Origins - Ultimate Edition':'龙腾世纪 起源','Dragon Age: Inquisition':'龙腾世纪 审判','The Outer Worlds':'天外世界','Fallout: New Vegas':'辐射 新维加斯','Fallout 4':'辐射4','GreedFall':'贪婪之秋',
'STEINS;GATE':'命运石之门','STEINS;GATE 0':'命运石之门0','CLANNAD':'CLANNAD 团子大家族','Summer Pockets':'夏日口袋','Raging Loop':'人狼村之谜','Danganronpa: Trigger Happy Havoc':'弹丸论破 希望的学园和绝望的高中生','Danganronpa 2: Goodbye Despair':'超级弹丸论破2','Danganronpa V3: Killing Harmony':'新弹丸论破V3','AI: The Somnium Files':'AI 梦境档案','AI: THE SOMNIUM FILES - nirvanA Initiative':'AI 梦境档案 涅槃肇始','The Great Ace Attorney Chronicles':'大逆转裁判 编年史','Phoenix Wright: Ace Attorney Trilogy':'逆转裁判123 成步堂精选集','WITCH ON THE HOLY NIGHT':'魔法使之夜','Fate/stay night REMASTERED':'Fate stay night 重制版','Slay the Princess - The Pristine Cut':'杀戮公主','Doki Doki Literature Club Plus!':'心跳文学部 Plus',
'The Last of Us Part II Remastered':'最后生还者 第二部 复刻版','What Remains of Edith Finch':'艾迪芬奇的记忆','Firewatch':'看火人','Life is Strange':'奇异人生','Detroit: Become Human':'底特律 变人','Heavy Rain':'暴雨','A Plague Tale: Innocence':'瘟疫传说 无罪','A Plague Tale: Requiem':'瘟疫传说 安魂曲','Hellblade: Senua\'s Sacrifice':'地狱之刃 塞娜的献祭','To the Moon':'去月球','Finding Paradise':'寻找天堂','Spiritfarer: Farewell Edition':'灵魂摆渡人 告别版',
'ELDEN RING':'艾尔登法环|老头环','DARK SOULS III':'黑暗之魂3|黑魂3','DARK SOULS: REMASTERED':'黑暗之魂 重制版','Sekiro: Shadows Die Twice - GOTY Edition':'只狼 影逝二度','Monster Hunter: World':'怪物猎人 世界','MONSTER HUNTER RISE':'怪物猎人 崛起','Grim Dawn':'恐怖黎明','Path of Exile':'流放之路','Titan Quest Anniversary Edition':'泰坦之旅 周年纪念版','Dragon\'s Dogma: Dark Arisen':'龙之信条 黑暗觉者','Nioh 2 - The Complete Edition':'仁王2 完全版','Lies of P':'匹诺曹的谎言','Black Myth: Wukong':'黑神话 悟空','Tales of Arise':'破晓传说','Tales of Berseria':'狂战传说','Mount & Blade II: Bannerlord':'骑马与砍杀2 霸主|骑马与砍杀|骑砍2|霸主',
'Tactics Ogre: Reborn':'皇家骑士团 重生','TRIANGLE STRATEGY':'三角战略','Disgaea 5 Complete':'魔界战记5','Disgaea 7: Vows of the Virtueless':'魔界战记7','Valkyria Chronicles':'战场女武神','The Banner Saga':'旗帜的传说','Wasteland 3':'废土3','Shadowrun: Dragonfall - Director\'s Cut':'暗影狂奔 龙陨','Wartales':'战争传说','Battle Brothers':'战场兄弟','Persona 5 Royal':'女神异闻录5 皇家版','Persona 4 Golden':'女神异闻录4 黄金版','Persona 3 Reload':'女神异闻录3 Reload','DRAGON QUEST XI S: Echoes of an Elusive Age - Definitive Edition':'勇者斗恶龙11S','FINAL FANTASY VII':'最终幻想7 原版','FINAL FANTASY VII REMAKE INTERGRADE':'最终幻想7 重制版 Intergrade','FINAL FANTASY VII REBIRTH':'最终幻想7 重生','FINAL FANTASY X/X-2 HD Remaster':'最终幻想10 高清合集','FINAL FANTASY XII THE ZODIAC AGE':'最终幻想12 黄道时代','FINAL FANTASY XVI':'最终幻想16','CHRONO TRIGGER':'时空之轮','OCTOPATH TRAVELER II':'八方旅人2','BRAVELY DEFAULT II':'勇气默示录2','Yakuza: Like a Dragon':'如龙7 光与暗的去向','Like a Dragon: Infinite Wealth':'如龙8','Hades':'哈迪斯','Hades II':'哈迪斯2','Slay the Spire':'杀戮尖塔|爬塔','The Binding of Isaac: Rebirth':'以撒的结合 重生','FTL: Faster Than Light':'超越光速','Into the Breach':'陷阵之志','Spelunky':'洞穴探险','Spelunky 2':'洞穴探险2','Noita':'女巫','Rogue Legacy 2':'盗贼遗产2','Darkest Dungeon':'暗黑地牢','Inscryption':'邪恶冥刻','Loop Hero':'循环英雄','Vampire Survivors':'吸血鬼幸存者','Clair Obscur: Expedition 33':'光与影 33号远征队','UNDERTALE':'传说之下','DELTARUNE':'三角符文',
'Factorio':'异星工厂','Satisfactory':'幸福工厂','Dyson Sphere Program':'戴森球计划','shapez 2':'异形工厂2','Mindustry':'像素工厂','Captain of Industry':'工业之都','Hydroneer':'淘金热','Big Pharma':'制药公司','Timberborn':'海狸浮生记','Oxygen Not Included':'缺氧','Euro Truck Simulator 2':'欧洲卡车模拟2','American Truck Simulator':'美国卡车模拟','House Flipper':'房产达人','House Flipper 2':'房产达人2','PC Building Simulator':'装机模拟器','Hardspace: Shipbreaker':'迷走深空 碎舰师','Supermarket Simulator':'超市模拟器','TCG Card Shop Simulator':'TCG卡牌店模拟器','Papers, Please':'请出示文件','Not Tonight':'今夜没门','Potion Craft: Alchemist Simulator':'药剂工艺 炼金模拟器','Potionomics':'魔药经济学',
'My Time at Portia':'波西亚时光','My Time at Sandrock':'沙石镇时光','Roots of Pacha':'帕夏时代','Sun Haven':'太阳港','Fields of Mistria':'米斯特里亚牧场','Coral Island':'珊瑚岛','Slime Rancher':'史莱姆牧场','Slime Rancher 2':'史莱姆牧场2','Graveyard Keeper':'守墓人','Microsoft Flight Simulator':'微软模拟飞行','Elite Dangerous':'精英 危险','X4: Foundations':'X4 基石','Kerbal Space Program':'坎巴拉太空计划','Universe Sandbox':'宇宙沙盘','No Man\'s Sky':'无人深空','EVERSPACE 2':'永恒空间2','The Sims 4':'模拟人生4','The Sims 3':'模拟人生3','Disney Dreamlight Valley':'迪士尼梦幻星谷','Prey':'掠食','Dishonored':'耻辱','Dishonored 2':'耻辱2','System Shock':'网络奇兵 重制版','HITMAN World of Assassination':'杀手 暗杀世界','Shadows of Doubt':'Shadows of Doubt','Terraria':'泰拉瑞亚','Garry\'s Mod':'盖瑞模组','Teardown':'拆迁','BeamNG.drive':'车祸模拟器','People Playground':'人类游乐场','Totally Accurate Battle Simulator':'全面战争模拟器','Besiege':'围攻','Scrap Mechanic':'废品机械师','Space Engineers':'太空工程师','Human Fall Flat':'人类一败涂地','Goat Simulator 3':'模拟山羊3',
'Sid Meier\'s Civilization VI':'文明6|文明VI','Sid Meier\'s Civilization V':'文明5|文明V','Sid Meier\'s Civilization IV':'文明4|文明IV','Old World':'旧世界','HUMANKIND':'人类','Age of Wonders 4':'奇迹时代4','Total War: WARHAMMER III':'全面战争 战锤3','Total War: SHOGUN 2':'全面战争 幕府将军2','Total War: THREE KINGDOMS':'全面战争 三国','XCOM 2':'幽浮2','XCOM: Enemy Unknown':'幽浮 未知敌人','Age of Empires II: Definitive Edition':'帝国时代2 决定版','Age of Empires IV: Anniversary Edition':'帝国时代4','Age of Empires III: Definitive Edition':'帝国时代3 决定版','Company of Heroes':'英雄连','Company of Heroes 2':'英雄连2','They Are Billions':'亿万僵尸','Northgard':'北境之地','Bloons TD 6':'气球塔防6','Bloons TD 5':'气球塔防5','Kingdom Rush - Tower Defense':'王国保卫战','Kingdom Rush Frontiers - Tower Defense':'王国保卫战 前线','Kingdom Rush Origins - Tower Defense':'王国保卫战 起源','Kingdom Rush Vengeance - Tower Defense':'王国保卫战 复仇','Kingdom Rush 5: Alliance TD':'王国保卫战5 联盟','Orcs Must Die!':'兽人必须死','Orcs Must Die! 2':'兽人必须死2','Orcs Must Die! 3':'兽人必须死3','Monster Train':'怪物火车','Monster Train 2':'怪物火车2','Wildfrost':'雪居之地','Gloomhaven':'幽港迷城','Wingspan':'展翅翱翔','Tabletop Simulator':'桌游模拟器','For The King':'为了吾王','For The King II':'为了吾王2','Root':'茂林源记','Spirit Island':'灵迹岛','Terraforming Mars':'殖民火星',
'Cities: Skylines':'城市 天际线','SimCity 4 Deluxe':'模拟城市4 豪华版','Anno 1800':'纪元1800','Anno 1404 - History Edition':'纪元1404 历史版','Anno 2070':'纪元2070','Tropico 6':'海岛大亨6','Frostpunk':'冰汽时代','Frostpunk 2':'冰汽时代2','Banished':'放逐之城','Foundation':'奠基','Manor Lords':'庄园领主','Farthest Frontier':'最远的边陲','Against the Storm':'风暴之城','Dawn of Man':'人类黎明','Kingdoms and Castles':'王国与城堡','Settlement Survival':'部落幸存者','Workers & Resources: Soviet Republic':'工人与资源 苏维埃共和国','Stellaris':'群星','Europa Universalis IV':'欧陆风云4','Crusader Kings III':'十字军之王3','Crusader Kings II':'十字军之王2','Hearts of Iron IV':'钢铁雄心4','Victoria 3':'维多利亚3','Football Manager 2024':'足球经理2024','Football Manager 2023':'足球经理2023','Motorsport Manager':'赛车经理','Forza Horizon 5':'极限竞速 地平线5','Forza Horizon 4':'极限竞速 地平线4','Assetto Corsa':'神力科莎','Assetto Corsa Competizione':'神力科莎 竞速','DiRT Rally 2.0':'尘埃 拉力赛2.0','EA SPORTS WRC':'世界拉力锦标赛 EA WRC','Project CARS 2':'赛车计划2','Need for Speed Heat':'极品飞车 热度','Need for Speed Hot Pursuit Remastered':'极品飞车 热力追踪 重制版','GRID Legends':'超级房车赛 传奇','Wreckfest':'撞车嘉年华','Burnout Paradise Remastered':'火爆狂飙 天堂 重制版','Rocket League':'火箭联盟',
'Resident Evil 7 Biohazard':'生化危机7','Resident Evil Village':'生化危机8 村庄','SILENT HILL 2':'寂静岭2 重制版','Alien: Isolation':'异形 隔离','SOMA':'活体脑细胞','Outlast':'逃生','Outlast 2':'逃生2','SIGNALIS':'信号','Little Nightmares':'小小梦魇','Little Nightmares II':'小小梦魇2','Detention':'返校','Visage':'面容','Darkwood':'阴暗森林','Stray':'迷失','Horizon Zero Dawn Remastered':'地平线 零之曙光 复刻版','Horizon Forbidden West Complete Edition':'地平线 西之绝境 完整版','DEATH STRANDING':'死亡搁浅','DEATH STRANDING DIRECTOR\'S CUT':'死亡搁浅 导演剪辑版','Ghost of Tsushima DIRECTOR\'S CUT':'对马岛之魂 导演剪辑版','Assassin\'s Creed Odyssey':'刺客信条 奥德赛','Assassin\'s Creed Origins':'刺客信条 起源','Subnautica':'深海迷航','Subnautica: Below Zero':'深海迷航 冰点之下','Don\'t Starve Together':'饥荒 联机版','Don\'t Starve':'饥荒','The Long Dark':'漫漫长夜','Green Hell':'绿色地狱','The Forest':'森林','Sons Of The Forest':'森林之子','Valheim':'英灵神殿','Raft':'木筏求生','Project Zomboid':'僵尸毁灭工程','Rust':'腐蚀','7 Days to Die':'七日杀','V Rising':'夜族崛起','Grounded':'禁闭求生','This War of Mine':'这是我的战争','Pacific Drive':'超自然车旅','Ghost Trick: Phantom Detective':'幽灵诡计','Paradise Killer':'天堂杀手','The Painscreek Killings':'潘克里克案件','The Sinking City':'沉没之城','L.A. Noire':'黑色洛城'
}

FAMILY_BY_CATEGORY={'fps':'shooter','third_person_shooter':'shooter','hack_and_slash':'action','fighting_martial_arts':'action','arcade_rhythm':'rhythm','platformer_runner':'action','shmup':'action','hidden_object':'hidden','metroidvania':'action','puzzle':'puzzle','adventure_rpg':'adventure','visual_novel':'story','story_rich':'story','action_rpg':'adventure','strategy_tactical_rpg':'strategy','jrpg':'adventure','roguelike_roguelite':'rogue','turn_based_rpg':'strategy','party_based_rpg':'adventure','building_automation':'management','hobby_job_sim':'management','dating_sim':'story','farming_crafting':'life','space_flight_sim':'flight','life_immersive_sim':'life','sandbox_physics':'creative','turn_based_strategy':'strategy','rts':'strategy','tower_defense':'strategy','card_board':'cards','city_settlement':'management','grand_strategy_4x':'strategy','military_strategy':'strategy','sports_sim_management':'management','racing':'racing','racing_sim':'racing','team_sports':'sports','individual_sports':'sports','sports':'sports'}
PACK_BY_APP={289070:'civ6',1174180:'rdr2',1190460:'ds1',1850570:'ds1',588650:'dc',646570:'sts',261550:'bannerlord',1771300:'kcd2',1868140:'dave'}
FEATURED=[289070,1174180,1190460,588650,646570,261550,1771300,1868140]


def choose_family(cats,tags):
    joined='|'.join(tags)
    for words,family in [('视觉小说|恋爱模拟','story'),('隐藏物体','hidden'),('节奏','rhythm'),('牌组构建','cards'),('农场模拟','life'),('自动化','management')]:
        if any(w in joined for w in words.split('|')):return family
    for cat in cats:
        if cat in FAMILY_BY_CATEGORY:return FAMILY_BY_CATEGORY[cat]
    if '解谜' in joined:return 'puzzle'
    if '第一人称射击' in joined or '第三人称射击' in joined:return 'shooter'
    if '剧情丰富' in joined:return 'story'
    return 'adventure'


def main():
    shortlist=json.loads((BASE/'shortlist.json').read_text(encoding='utf-8'));taxonomy=json.loads((BASE/'taxonomy.json').read_text(encoding='utf-8'))
    awards=json.loads((BASE/'awards.json').read_text(encoding='utf-8'));award_map={}
    for year in awards['years']:
        for name,award in year['winners'].items():award_map.setdefault(helper.key(name),[]).append({'organizer':'The Game Awards','year':year['year'],'award':award,'status':'winner','source_url':year['source_url'],'scope':'original game; not a claim about later port quality','checked_at':awards['checked_at']})
    names=list(dict.fromkeys(n for group in shortlist.values() for n in group));games=[];by_name={};pending=[]
    for name in names:
        path=BASE/'records'/(helper.slug(name)+'.json');record=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        appid=record.get('steam_appid') or STEAM_FIXES.get(name)
        cats=[cat for cat,group in shortlist.items() if name in group]
        special=CONSOLE.get(name)
        aliases=ZH.get(name,'').split('|') if name in ZH else []
        title=aliases[0] if aliases else record.get('store_title_zh') or record.get('original_title') or name
        if special:title=special[0]
        identifier=f'steam-{appid}' if appid else helper.slug(name)
        source=record.get('store_url') or (f'https://store.steampowered.com/app/{appid}/' if appid else special[1] if special else None)
        if not source:pending.append(name)
        game={'id':identifier,'title':title,'original_title':name,'aliases':list(dict.fromkeys(aliases+[name,record.get('original_title',name),record.get('store_title_zh',title)])),'category_ids':cats,'mechanic_family':choose_family(cats,record.get('store_tags_zh',[])),'question_pack':PACK_BY_APP.get(appid),'platforms':special[2] if special else ['PC'],'source_url':source,'review_snapshot':record.get('review_snapshot'),'review_checked_at':record.get('checked_at'),'source_status':record.get('verification_status','publisher_reference' if special else 'needs_source'),'store_tags':record.get('store_tags_zh',[]),'award_evidence':[],'inclusion_rationale':'从用户指定分类中整理的知名作品或类内代表作；口碑数据与奖项分别保留，不将未核对的奖项作为事实。'}
        game['award_evidence']=award_map.get(helper.key(name),[])
        if special:game['source_status']='official_publisher_reference'
        elif name in STEAM_FIXES and not game['source_status'].startswith('verified_steam'):
            game['source_status']='official_store_reference_checked'
            game['identity_checked_at']='2026-10-27'
        elif appid and game['source_status']=='pending':
            game['source_status']='matched_store_reference_review_pending'
        if name=='Shadows of Doubt':
            game['title']='Shadows of Doubt';game['aliases']=['Shadows of Doubt']
        if game.get('review_snapshot') and (game['review_snapshot'].get('positive_percent') or 0)<70:
            game['inclusion_rationale']='知名系列或类内代表作；Steam口碑可能偏低或混合，保留实际快照，不称为全库一致好评。'
        existing=next((g for g in games if g['id']==identifier),None)
        if existing:
            existing['category_ids']=list(dict.fromkeys(existing['category_ids']+cats));existing['aliases']=list(dict.fromkeys(existing['aliases']+game['aliases']))
        else:games.append(game)
        by_name[name]=identifier
    categories=[]
    for cat in taxonomy['categories']:
        ids=[by_name[n] for n in shortlist[cat['id']]]
        if len(ids)!=20 or len(set(ids))!=20:raise ValueError('Category must contain 20 distinct games: '+cat['id'])
        categories.append({'id':cat['id'],'name':cat['name'],'kind':cat['kind'],'game_ids':ids,'image_positions':cat['image_positions']})
    output={'version':'0.4.0','source_taxonomy':'user_supplied_48_entries_47_unique_categories','category_count':47,'category_assignment_count':940,'game_count':len(games),'selection_policy':'PC and console; recognition and reputation prioritized; awards preferred but not required','categories':categories,'games':games,'featured':[f'steam-{i}' for i in FEATURED],'provenance':{'reviews_api':'https://partner.steamgames.com/doc/webapi/IUserReviewsService','review_scope':'all languages, Steam purchases, off-topic filtered; frozen snapshot','console_sources':'official publisher/platform pages, historical reference where original publisher page unavailable','game_name_never_scores':True}}
    (ROOT/'config/games.v0.4.0.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (BASE/'unresolved-sources.json').write_text(json.dumps(pending,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Catalogue: {len(games)} games, 47 categories, 940 assignments; sources still needed: {len(pending)}')
    if pending:print(json.dumps(pending,ensure_ascii=False))


if __name__=='__main__':main()
