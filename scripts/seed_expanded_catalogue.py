"""Author the reproducible discovery plan. Proposed names need independent evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'research/catalogue-v0.5'

# These are discovery targets, not unverified claims about a product's identity.
# Live Steam metadata is checked before an appid can enter the published library.
SEEDS = '''
10|反恐精英|Counter-Strike|fps|CS1.6;CS 1.6;CS16
80|反恐精英：零点行动|Counter-Strike: Condition Zero|fps|CS零点行动
240|反恐精英：起源|Counter-Strike: Source|fps|CSS;CS起源
570|刀塔2|Dota 2|moba|DOTA2;刀塔;刀塔二
578080|绝地求生|PUBG: BATTLEGROUNDS|fps,battle_royale|PUBG;吃鸡
1172470|Apex英雄|Apex Legends|fps,battle_royale|APEX;顶点英雄
2357570|守望先锋|Overwatch|fps|OW;守望先锋2;OW2
359550|彩虹六号：围攻|Tom Clancy's Rainbow Six Siege|fps|R6;彩六;R6S
2507950|三角洲行动|Delta Force|fps,extraction_shooter|三角洲;DeltaForce
1203220|永劫无间|NARAKA: BLADEPOINT|battle_royale,action_rpg|NARAKA
1085660|命运2|Destiny 2|fps,online_rpg|D2;命运二
440|军团要塞2|Team Fortress 2|fps|TF2;军团要塞
1938090|使命召唤|Call of Duty|fps|COD;战区;Warzone
10180|使命召唤：现代战争2|Call of Duty: Modern Warfare 2|fps|COD6
10190|使命召唤：现代战争2多人模式|Call of Duty: Modern Warfare 2 - Multiplayer|fps|COD6多人
7940|使命召唤4：现代战争|Call of Duty 4: Modern Warfare|fps|COD4
10090|使命召唤：战争世界|Call of Duty: World at War|fps|COD5
42700|使命召唤：黑色行动|Call of Duty: Black Ops|fps|COD7
42680|使命召唤：现代战争3|Call of Duty: Modern Warfare 3|fps|COD8
202970|使命召唤：黑色行动2|Call of Duty: Black Ops II|fps|COD9
209160|使命召唤：幽灵|Call of Duty: Ghosts|fps|COD10
209650|使命召唤：高级战争|Call of Duty: Advanced Warfare|fps|COD11
311210|使命召唤：黑色行动3|Call of Duty: Black Ops III|fps|COD12
292730|使命召唤：无限战争|Call of Duty: Infinite Warfare|fps|COD13
476600|使命召唤：二战|Call of Duty: WWII|fps|COD14
1238810|战地5|Battlefield V|fps|BF5;战地五
1238840|战地1|Battlefield 1|fps|BF1;战地一
1238860|战地4|Battlefield 4|fps|BF4
1238820|战地3|Battlefield 3|fps|BF3
1517290|战地2042|Battlefield 2042|fps|BF2042
24960|战地：叛逆连队2|Battlefield: Bad Company 2|fps|叛逆连队2
221380|帝国时代2高清版|Age of Empires II HD|rts|帝国时代2HD
266840|神话时代：扩展版|Age of Mythology: Extended Edition|rts|神话时代
1934680|神话时代：重述版|Age of Mythology: Retold|rts|神话时代重制版
1213210|命令与征服：重制版合集|Command & Conquer Remastered Collection|rts|CNC重制
17480|命令与征服：红色警戒3|Command & Conquer: Red Alert 3|rts|红警3;RA3
24790|命令与征服3：泰伯利亚战争|Command & Conquer 3 Tiberium Wars|rts|CNC3
4770|罗马：全面战争|Rome: Total War|rts,grand_strategy_4x|罗马全战
4700|中世纪2：全面战争|Medieval II: Total War|rts,grand_strategy_4x|中世纪2全战
10500|帝国：全面战争|Empire: Total War|grand_strategy_4x|帝国全战
34030|拿破仑：全面战争|Napoleon: Total War|grand_strategy_4x|拿战
364360|全面战争：战锤|Total War: WARHAMMER|grand_strategy_4x|战锤全战1
594570|全面战争：战锤2|Total War: WARHAMMER II|grand_strategy_4x|战锤全战2
325610|全面战争：阿提拉|Total War: ATTILA|grand_strategy_4x|阿提拉全战
1099410|全面战争传奇：特洛伊|A Total War Saga: TROY|grand_strategy_4x|特洛伊全战
214950|全面战争：罗马2|Total War: ROME II|grand_strategy_4x|罗马2全战
39210|最终幻想14|FINAL FANTASY XIV Online|mmorpg,jrpg|FF14;狒狒14;最终幻想XIV
306130|上古卷轴OL|The Elder Scrolls Online|mmorpg|ESO;上古卷轴Online
1284210|激战2|Guild Wars 2|mmorpg|GW2
8500|星战前夜|EVE Online|mmorpg,space|EVE
1599340|失落的方舟|Lost Ark|mmorpg,action_rpg|命运方舟
582660|黑色沙漠|Black Desert|mmorpg,action_rpg|BDO
212160|洛奇英雄传|Vindictus|mmorpg,action_rpg|洛英
212180|洛奇|Mabinogi|mmorpg|玛奇
216150|冒险岛|MapleStory|mmorpg|枫之谷
109600|无冬OL|Neverwinter|mmorpg|无冬Online
206480|龙与地下城OL|Dungeons & Dragons Online|mmorpg|DDO
212500|指环王OL|The Lord of the Rings Online|mmorpg|LOTRO
761890|阿尔比恩OL|Albion Online|mmorpg|阿尔比恩
1343400|江湖|RuneScape|mmorpg|符文工坊
1343370|经典江湖|Old School RuneScape|mmorpg|OSRS
899770|最后纪元|Last Epoch|action_rpg|LE
2694490|流放之路2|Path of Exile 2|action_rpg|POE2
2344520|暗黑破坏神4|Diablo IV|action_rpg,online_rpg|暗黑4;大菠萝4;Diablo4
200710|火炬之光2|Torchlight II|action_rpg|火炬之光二
41500|火炬之光|Torchlight|action_rpg|火炬之光1
1030210|火炬之光3|Torchlight III|action_rpg|火炬之光三
475150|泰坦之旅周年版|Titan Quest Anniversary Edition|action_rpg|泰坦之旅
39190|地牢围攻|Dungeon Siege|action_rpg|地牢围攻1
39200|地牢围攻2|Dungeon Siege II|action_rpg|地牢围攻二
236430|黑暗之魂2|DARK SOULS II|action_rpg|黑魂2;黑暗之魂2原版
335300|黑暗之魂2：原罪学者|DARK SOULS II: Scholar of the First Sin|action_rpg|原罪学者;魂2原罪
22330|上古卷轴4：湮灭|The Elder Scrolls IV: Oblivion|adventure_rpg|老滚4;湮灭原版
72850|上古卷轴5：天际|The Elder Scrolls V: Skyrim|adventure_rpg|老滚5原版;天际原版
22300|辐射3|Fallout 3|adventure_rpg|FO3
22370|辐射3年度版|Fallout 3: Game of the Year Edition|adventure_rpg|辐射3GOTY
38400|辐射|Fallout|adventure_rpg|辐射1
38410|辐射2|Fallout 2|adventure_rpg|辐射二
38420|辐射战略版：钢铁兄弟会|Fallout Tactics: Brotherhood of Steel|strategy_tactical_rpg|辐射战略版
1151340|辐射76|Fallout 76|online_rpg,adventure_rpg|FO76
20900|巫师：加强版|The Witcher: Enhanced Edition|adventure_rpg|巫师1
70300|VVVVVV|VVVVVV|platformer_runner|六个V
17470|死亡空间原版|Dead Space|third_person_shooter,horror|死亡空间2008
47780|死亡空间2|Dead Space 2|third_person_shooter,horror|死亡空间二
1238060|死亡空间3|Dead Space 3|third_person_shooter,horror|死亡空间三
254700|生化危机4原版|Resident Evil 4 (2005)|third_person_shooter,horror|生化4原版;RE4原版
952060|生化危机3重制版|Resident Evil 3|third_person_shooter,horror|RE3重制
21690|生化危机5|Resident Evil 5|third_person_shooter,horror|RE5
221040|生化危机6|Resident Evil 6|third_person_shooter,horror|RE6
304590|生化危机：启示录2|Resident Evil Revelations 2|third_person_shooter,horror|启示录2
222480|生化危机：启示录|Resident Evil Revelations|third_person_shooter,horror|启示录1
339340|生化危机0高清版|Resident Evil 0|horror|生化0
7670|生化奇兵原版|BioShock|fps,scifi_cyberpunk|生化奇兵1原版
8850|生化奇兵2|BioShock 2|fps,scifi_cyberpunk|生化奇兵二
409720|生化奇兵2重制版|BioShock 2 Remastered|fps,scifi_cyberpunk|生化奇兵2高清版
70|半条命|Half-Life|fps,scifi_cyberpunk|半衰期;半条命1;HL1
50|半条命：针锋相对|Half-Life: Opposing Force|fps|针锋相对
130|半条命：蓝色行动|Half-Life: Blue Shift|fps|蓝色行动
380|半条命2：第一章|Half-Life 2: Episode One|fps|半条命2第一章
420|半条命2：第二章|Half-Life 2: Episode Two|fps|半条命2第二章
546560|半条命：爱莉克斯|Half-Life: Alyx|fps,vr|半衰期爱莉克斯;Alyx;HL:A
271590|侠盗猎车手5传承版|Grand Theft Auto V Legacy|third_person_shooter,open_world|GTA5旧版;GTA V Legacy
12110|侠盗猎车手：罪恶都市|Grand Theft Auto: Vice City|open_world|罪恶都市;GTAVC
12100|侠盗猎车手3|Grand Theft Auto III|open_world|GTA3
12120|侠盗猎车手：圣安地列斯|Grand Theft Auto: San Andreas|open_world|圣安地列斯;GTASA
12210|侠盗猎车手4|Grand Theft Auto IV|open_world|GTA4
1547000|侠盗猎车手：圣安地列斯最终版|Grand Theft Auto: San Andreas - The Definitive Edition|open_world|圣安地列斯重制
1546990|侠盗猎车手：罪恶都市最终版|Grand Theft Auto: Vice City - The Definitive Edition|open_world|罪恶都市重制
1546970|侠盗猎车手3最终版|Grand Theft Auto III - The Definitive Edition|open_world|GTA3重制
2668510|荒野大镖客：救赎|Red Dead Redemption|open_world|荒野大镖客1;RDR1;大表哥1
55230|黑道圣徒3|Saints Row: The Third|open_world|黑道圣徒三
206420|黑道圣徒4|Saints Row IV|open_world|黑道圣徒四
7420|杀手：血钱|Hitman: Blood Money|life_immersive_sim|杀手4;血钱
203140|杀手：赦免|Hitman: Absolution|life_immersive_sim|赦免
236870|杀手|HITMAN|life_immersive_sim|杀手2016
40990|黑手党原版|Mafia|open_world,third_person_shooter|四海兄弟原版
1030840|四海兄弟：最终版|Mafia: Definitive Edition|open_world,third_person_shooter|黑手党重制版
50130|黑手党2|Mafia II|open_world,third_person_shooter|四海兄弟2原版
1030830|四海兄弟2：最终版|Mafia II: Definitive Edition|open_world,third_person_shooter|黑手党2最终版
360430|四海兄弟3|Mafia III|open_world,third_person_shooter|黑手党3
552520|孤岛惊魂5|Far Cry 5|fps,open_world|远哭5;FC5
220240|孤岛惊魂3|Far Cry 3|fps,open_world|远哭3;FC3
298110|孤岛惊魂4|Far Cry 4|fps,open_world|远哭4;FC4
2369390|孤岛惊魂6|Far Cry 6|fps,open_world|远哭6;FC6
939960|孤岛惊魂：新曙光|Far Cry New Dawn|fps,open_world|新曙光
371660|孤岛惊魂：原始杀戮|Far Cry Primal|fps,open_world|原始杀戮
19680|爱丽丝：疯狂回归|Alice: Madness Returns|adventure_rpg,platformer_runner|爱丽丝疯狂回归
17300|孤岛危机|Crysis|fps|显卡危机
17330|孤岛危机：弹头|Crysis Warhead|fps|弹头
108800|孤岛危机2极限版|Crysis 2 Maximum Edition|fps|孤岛危机2
1282690|孤岛危机3|Crysis 3|fps|孤岛危机三
1715130|孤岛危机重制版|Crysis Remastered|fps|孤岛危机1重制
230410|星际战甲|Warframe|third_person_shooter,online_rpg|战争框架
252490|腐蚀|Rust|survival|RUST
381210|黎明杀机|Dead by Daylight|horror,party_multiplayer|DBD;黎明杀鸡
438100|虚拟现实社交平台|VRChat|party_multiplayer,vr|VRC;VR聊天
291550|英灵乱战|Brawlhalla|fighting_martial_arts|Brawlhalla
813780|帝国时代2决定版|Age of Empires II: Definitive Edition|rts|帝国2决定版
24010|模拟火车经典版|Train Simulator Classic|hobby_job_sim|火车模拟
359320|精英：危险|Elite Dangerous|space_flight_sim|精英危险
275850|无人深空|No Man's Sky|space,survival|NMS
892970|英灵神殿|Valheim|survival|瓦尔海姆
1623730|幻兽帕鲁|Palworld|survival,open_world|帕鲁;PalWorld
1144200|严阵以待|Ready or Not|fps|RON
594650|猎杀：对决|Hunt: Showdown 1896|fps,extraction_shooter|猎杀对决;猎杀1896
393380|战术小队|Squad|fps,military_strategy|SQUAD
736220|战术小队44|Squad 44|fps|Post Scriptum
686810|人间地狱|Hell Let Loose|fps|HLL
581320|叛乱：沙漠风暴|Insurgency: Sandstorm|fps|沙漠风暴
222880|叛乱|Insurgency|fps|叛乱1
107410|武装突袭3|Arma 3|fps,military_strategy|ARMA3;武装突袭三
1874880|武装突袭：重铸者|Arma Reforger|fps|ARMA重铸
236390|战争雷霆|War Thunder|military_strategy|WT;战争之雷
444200|坦克世界闪击战|World of Tanks Blitz|military_strategy|WOTB
552990|战舰世界|World of Warships|military_strategy|WOWS;窝窝屎
1407200|坦克世界|World of Tanks|military_strategy|WOT
1172620|盗贼之海|Sea of Thieves|adventure_rpg,party_multiplayer|SOT
252950|火箭联盟|Rocket League|team_sports,racing|RL
1097150|糖豆人|Fall Guys|party_multiplayer|糖豆人终极淘汰赛
945360|太空狼人杀|Among Us|social_deduction|在我们之中
1568590|鹅鸭杀|Goose Goose Duck|social_deduction|GGD
1966720|致命公司|Lethal Company|horror,party_multiplayer|LC
739630|恐鬼症|Phasmophobia|horror,party_multiplayer|抓鬼
2881650|内容警告|Content Warning|horror,party_multiplayer|警告内容
3241660|R.E.P.O.|R.E.P.O.|horror,party_multiplayer|REPO
1217060|枪火重生|Gunfire Reborn|fps,roguelike_roguelite|枪火
692890|机械守护者|Roboquest|fps,roguelike_roguelite|机器守护者
611790|家庭派对|House Party|life_immersive_sim|家庭聚会
322330|饥荒联机版|Don't Starve Together|survival|DST
648800|木筏求生|Raft|survival|木筏
264710|深海迷航|Subnautica|survival|美丽水世界
383120|帝国霸业：银河生存|Empyrion - Galactic Survival|survival,space|帝国霸业
304930|未转变者|Unturned|survival|未转变
346110|方舟：生存进化|ARK: Survival Evolved|survival|方舟生存进化;ARK
2399830|方舟：生存飞升|ARK: Survival Ascended|survival|方舟重制
440900|流放者柯南|Conan Exiles|survival|柯南流亡
834910|阿特拉斯|ATLAS|survival|阿特拉斯海盗
1604030|夜族崛起|V Rising|survival|吸血鬼崛起
1203620|雾锁王国|Enshrouded|survival|雾锁
1928980|夜莺传说|Nightingale|survival|夜莺
294100|环世界|RimWorld|management,city_settlement|边缘世界;RIMWORLD
233450|监狱建筑师|Prison Architect|management,city_settlement|监狱设计师
219740|饥荒|Don't Starve|survival|单机饥荒
367520|空洞骑士|Hollow Knight|metroidvania|HK
1151640|地平线：零之曙光完全版|Horizon Zero Dawn Complete Edition|open_world|地平线黎明时分
1150690|奥莫里|OMORI|turn_based_rpg,horror|OMORI
1426210|双人成行|It Takes Two|platformer_runner|双人成行正式版
2001120|双影奇境|Split Fiction|platformer_runner,party_multiplayer|分裂奇境
1222700|逃出生天|A Way Out|adventure_rpg,party_multiplayer|逃出升天
448510|胡闹厨房|Overcooked|party_multiplayer|煮糊了;分手厨房1
728880|胡闹厨房2|Overcooked! 2|party_multiplayer|分手厨房2;煮糊了2
1243830|胡闹厨房：全都好吃|Overcooked! All You Can Eat|party_multiplayer|分手厨房全都好吃
477160|人类一败涂地|Human Fall Flat|sandbox_physics,party_multiplayer|HFF
1260320|猛兽派对|Party Animals|party_multiplayer|动物派对
285900|帮派野兽|Gang Beasts|party_multiplayer|基佬大乱斗
252950|火箭联盟|Rocket League|sports|火箭联盟PC
291860|坑人|Pit People|strategy_tactical_rpg|坑人游戏
238460|战斗砖块剧场|BattleBlock Theater|platformer_runner|方块剧场
204360|城堡破坏者|Castle Crashers|hack_and_slash,party_multiplayer|城堡毁灭者
218620|收获日2|PAYDAY 2|fps|劫薪日2
1272080|收获日3|PAYDAY 3|fps|劫薪日3
22380|辐射：新维加斯|Fallout: New Vegas|adventure_rpg|FNV
933110|帝国时代3决定版|Age of Empires III: Definitive Edition|rts|帝国3决定版
489830|上古卷轴5天际特别版|The Elder Scrolls V: Skyrim Special Edition|adventure_rpg|老滚5;天际特别版
17460|质量效应|Mass Effect|adventure_rpg,space|质量效应1
24980|质量效应2|Mass Effect 2|adventure_rpg,space|质量效应二
1238020|质量效应3|Mass Effect 3|adventure_rpg,space|质量效应三
1328670|质量效应传奇版|Mass Effect Legendary Edition|adventure_rpg|质量效应合集
1173770|最终幻想1像素重制版|FINAL FANTASY|jrpg,turn_based_rpg|FF1
1173780|最终幻想2像素重制版|FINAL FANTASY II|jrpg,turn_based_rpg|FF2
1173790|最终幻想3像素重制版|FINAL FANTASY III|jrpg,turn_based_rpg|FF3
1173800|最终幻想4像素重制版|FINAL FANTASY IV|jrpg,turn_based_rpg|FF4
1173810|最终幻想5像素重制版|FINAL FANTASY V|jrpg,turn_based_rpg|FF5
1173820|最终幻想6像素重制版|FINAL FANTASY VI|jrpg,turn_based_rpg|FF6
39150|最终幻想8|FINAL FANTASY VIII|jrpg,turn_based_rpg|FF8
1026680|最终幻想8重制版|FINAL FANTASY VIII - REMASTERED|jrpg,turn_based_rpg|FF8重制
377840|最终幻想9|FINAL FANTASY IX|jrpg,turn_based_rpg|FF9
292120|最终幻想13|FINAL FANTASY XIII|jrpg|FF13
292140|最终幻想13-2|FINAL FANTASY XIII-2|jrpg|FF13-2
345350|雷霆归来：最终幻想13|LIGHTNING RETURNS: FINAL FANTASY XIII|jrpg|雷霆归来
637650|最终幻想15|FINAL FANTASY XV WINDOWS EDITION|jrpg,action_rpg|FF15
1809700|女神异闻录3携带版|Persona 3 Portable|jrpg,turn_based_rpg|P3P
1809700|女神异闻录3携带版|Persona 3 Portable|jrpg,turn_based_rpg|女神异闻录3P
1205520|女神异闻录5乱战：魅影攻手|Persona 5 Strikers|jrpg,hack_and_slash|P5S
2254740|女神异闻录5战略版|Persona 5 Tactica|strategy_tactical_rpg|P5T
1113000|女神异闻录4黄金版|Persona 4 Golden|jrpg|P4G
1687950|女神异闻录5皇家版|Persona 5 Royal|jrpg|P5R
2161700|女神异闻录3Reload|Persona 3 Reload|jrpg|P3R
311560|刺客信条：叛变|Assassin's Creed Rogue|open_world|AC叛变
15100|刺客信条|Assassin's Creed|open_world|AC1
33230|刺客信条2|Assassin's Creed II|open_world|AC2
48190|刺客信条：兄弟会|Assassin's Creed Brotherhood|open_world|AC兄弟会
201870|刺客信条：启示录|Assassin's Creed Revelations|open_world|AC启示录
208480|刺客信条3|Assassin's Creed III|open_world|AC3
242050|刺客信条4：黑旗|Assassin's Creed IV Black Flag|open_world|黑旗;AC4
289650|刺客信条：大革命|Assassin's Creed Unity|open_world|ACU
368500|刺客信条：枭雄|Assassin's Creed Syndicate|open_world|ACS
2208920|刺客信条：英灵殿|Assassin's Creed Valhalla|open_world|AC英灵殿
3035570|刺客信条：幻景|Assassin's Creed Mirage|open_world|AC幻景
3159330|刺客信条：影|Assassin's Creed Shadows|open_world|AC影
447040|看门狗2|Watch_Dogs 2|open_world|WD2
243470|看门狗|Watch_Dogs|open_world|WD1
2239550|看门狗：军团|Watch Dogs: Legion|open_world|WD军团
928600|F1赛车2019|F1 2019|racing|F12019
1080110|F1赛车2020|F1 2020|racing|F12020
2108330|F1赛车23|F1 23|racing|F123
1551360|极限竞速地平线5|Forza Horizon 5|racing|FH5;地平线5
1293830|极限竞速地平线4|Forza Horizon 4|racing|FH4;地平线4
1846380|极品飞车：不羁|Need for Speed Unbound|racing|NFS不羁
1262600|极品飞车：热力追踪重制版|Need for Speed Hot Pursuit Remastered|racing|NFS热力追踪
1262560|极品飞车：最高通缉|Need for Speed Most Wanted|racing|NFS17;最高通缉2012
1262580|极品飞车：热度|Need for Speed Heat|racing|NFS21
1262540|极品飞车|Need for Speed|racing|NFS19
1222680|极品飞车：复仇|Need for Speed Payback|racing|NFS20
35014|极品飞车：变速|Need for Speed SHIFT|racing|NFS13
47870|极品飞车：热力追踪|Need for Speed: Hot Pursuit|racing|NFS14
415480|实况足球2016|Pro Evolution Soccer 2016|team_sports|PES2016
592580|实况足球2018|PRO EVOLUTION SOCCER 2018|team_sports|PES2018
770240|实况足球2019|PRO EVOLUTION SOCCER 2019|team_sports|PES2019
996470|实况足球2020|eFootball PES 2020|team_sports|PES2020
230410|星际战甲|Warframe|online_rpg|WarframePC
632360|雨中冒险2|Risk of Rain 2|roguelike_roguelite|ROR2
311690|挺进地牢|Enter the Gungeon|roguelike_roguelite|ETG
813230|动物井|ANIMAL WELL|metroidvania|动物之井
1145360|哈迪斯|Hades|roguelike_roguelite|黑帝斯;哈迪斯1
892970|英灵神殿|Valheim|survival|英灵神殿PC
1326470|森林之子|Sons Of The Forest|survival|森林2
413150|星露谷物语|Stardew Valley|farming_crafting|星露谷;SDV
400|传送门|Portal|puzzle|传送门1
620|传送门2|Portal 2|puzzle|传送门二
105600|泰拉瑞亚|Terraria|survival|泰拉;TerrariaPC
457140|缺氧|Oxygen Not Included|building_automation|ONI
427520|异星工厂|Factorio|building_automation|工厂异星
292030|巫师3狂猎|The Witcher 3: Wild Hunt|adventure_rpg|巫师三
814380|只狼影逝二度|Sekiro: Shadows Die Twice|action_rpg|只狼;SEKIRO
1245620|艾尔登法环|ELDEN RING|action_rpg|老头环;法环;ER
2622380|艾尔登法环：黑夜君临|ELDEN RING NIGHTREIGN|action_rpg|黑夜君临
440520|恐龙生存游戏|ARK Park|vr|方舟公园
238960|流放之路|Path of Exile|action_rpg|POE;流放1
240720|和班尼特福迪一起攻克难关|Getting Over It with Bennett Foddy|platformer_runner|掘地求升;罐子人
274170|迈阿密热线2：空号|Hotline Miami 2: Wrong Number|action_rpg|迈阿密热线2
219150|迈阿密热线|Hotline Miami|action_rpg|迈阿密热线1
115320|虐杀原形2|PROTOTYPE 2|open_world,action_rpg|虐杀2
10150|虐杀原形|Prototype|open_world,action_rpg|虐杀1
464060|RUINER|RUINER|action|RUINER
418240|影子战术：将军之刃|Shadow Tactics: Blades of the Shogun|rts|影子战术
610370|赏金奇兵3|Desperados III|rts|赏金奇兵三
1545560|影子诡局：被诅咒的海盗|Shadow Gambit: The Cursed Crew|rts|影子诡局
379430|天国：拯救|Kingdom Come: Deliverance|adventure_rpg|KCD1
990080|霍格沃茨之遗|Hogwarts Legacy|adventure_rpg,open_world|霍格沃兹之遗
1919590|NBA2K23篮球|NBA 2K23|team_sports|NBA2K23
1644960|NBA2K22篮球|NBA 2K22|team_sports|NBA2022
1089350|NBA2K20篮球|NBA 2K20|team_sports|NBA2K20
370240|NBA2K16篮球|NBA 2K16|team_sports|NBA2K16
257350|博德之门2增强版|Baldur's Gate II: Enhanced Edition|adventure_rpg|BG2
228280|博德之门增强版|Baldur's Gate: Enhanced Edition|adventure_rpg|BG1
1086940|博德之门3|Baldur's Gate 3|turn_based_rpg|BG3;博德3
435150|神界原罪2|Divinity: Original Sin 2|turn_based_rpg|DOS2
113200|以撒的结合原版|The Binding of Isaac|roguelike_roguelite|以撒原版
250900|以撒的结合重生|The Binding of Isaac: Rebirth|roguelike_roguelite|以撒重生
65800|地牢守护者|Dungeon Defenders|tower_defense|地牢守护者1
236850|欧陆风云4|Europa Universalis IV|grand_strategy_4x|EU4;欧陆4
281990|群星|Stellaris|grand_strategy_4x|群星PC
203770|十字军之王2|Crusader Kings II|grand_strategy_4x|CK2;王国风云2
1158310|十字军之王3|Crusader Kings III|grand_strategy_4x|CK3;王国风云3
394360|钢铁雄心4|Hearts of Iron IV|grand_strategy_4x|HOI4;钢4
42960|维多利亚2|Victoria II|grand_strategy_4x|维多利亚二;VIC2
529340|维多利亚3|Victoria 3|grand_strategy_4x|VIC3
203160|古墓丽影2013|Tomb Raider|adventure_rpg|古墓丽影9
391220|古墓丽影：崛起|Rise of the Tomb Raider|adventure_rpg|古墓丽影10
750920|古墓丽影：暗影|Shadow of the Tomb Raider|adventure_rpg|古墓丽影11
200260|蝙蝠侠：阿卡姆之城|Batman: Arkham City|action_rpg|阿卡姆城
35140|蝙蝠侠：阿卡姆疯人院|Batman: Arkham Asylum|action_rpg|阿卡姆疯人院
209000|蝙蝠侠：阿卡姆起源|Batman: Arkham Origins|action_rpg|阿卡姆起源
208650|蝙蝠侠：阿卡姆骑士|Batman: Arkham Knight|action_rpg|阿卡姆骑士
1817070|漫威蜘蛛侠重制版|Marvel's Spider-Man Remastered|open_world,action_rpg|蜘蛛侠重制
1817190|漫威蜘蛛侠：迈尔斯莫拉莱斯|Marvel's Spider-Man: Miles Morales|open_world,action_rpg|迈尔斯
2651280|漫威蜘蛛侠2|Marvel's Spider-Man 2|open_world,action_rpg|蜘蛛侠2
1091500|赛博朋克2077|Cyberpunk 2077|adventure_rpg|2077;CP2077
242760|森林|The Forest|survival|森林1
322170|几何冲刺|Geometry Dash|arcade_rhythm|GD
223470|喋血街头2|POSTAL 2|fps|邮差2
232090|杀戮空间2|Killing Floor 2|fps|KF2
1250|杀戮空间|Killing Floor|fps|KF1
312660|狙击精英4|Sniper Elite 4|third_person_shooter|狙击精英四
227300|欧洲卡车模拟2|Euro Truck Simulator 2|hobby_job_sim|欧卡2;ETS2
270880|美国卡车模拟|American Truck Simulator|hobby_job_sim|美卡;ATS
255710|城市天际线|Cities: Skylines|city_settlement|天际线1
949230|城市天际线2|Cities: Skylines II|city_settlement|天际线2;都市天际线2
703080|动物园之星|Planet Zoo|management|动物园
493340|过山车之星|Planet Coaster|management|过山车之星1
1643310|地下城4|Dungeons 4|management|地下城四
1644320|铁路帝国2|Railway Empire 2|management|铁路帝国二
503940|铁路帝国|Railway Empire|management|铁路帝国1
33830|铁路大亨3|Railroad Tycoon 3|management|铁路大亨三
285310|过山车大亨豪华版|RollerCoaster Tycoon: Deluxe|management|RCT1
285330|过山车大亨2|RollerCoaster Tycoon 2|management|RCT2
500370|铁路大亨2白金版|Railroad Tycoon II Platinum|management|铁路大亨2
273070|行会2文艺复兴|The Guild II Renaissance|life_immersive_sim|行会2
311290|咒语力量3|SpellForce 3|rts,action_rpg|咒语力量三
270150|奔跑吧步兵|RUNNING WITH RIFLES|third_person_shooter|小兵步枪
602960|潜渊症|Barotrauma|survival|潜渊
387990|废品机械师|Scrap Mechanic|sandbox_physics|废品机械师PC
374320|黑暗之魂3|DARK SOULS III|action_rpg|黑魂3;魂3;DS3
570940|黑暗之魂重制版|DARK SOULS: REMASTERED|action_rpg|黑魂1;魂1重制
960090|气球塔防6|Bloons TD 6|tower_defense|BTD6
646570|杀戮尖塔|Slay the Spire|card_board|STS;杀戮尖塔1
2379780|小丑牌|Balatro|card_board|巴拉特罗
2868840|杀戮尖塔2|Slay the Spire 2|card_board|STS2;杀戮尖塔二
306020|气球塔防5|Bloons TD 5|tower_defense|BTD5
431240|友尽高尔夫|Golf With Your Friends|individual_sports,party_multiplayer|高尔夫好友
1599600|速速上菜|PlateUp!|party_multiplayer|餐厅模拟
714010|瞄准实验室|Aimlabs|fps|Aim Lab;练枪
300|胜利之日：起源|Day of Defeat: Source|fps|DODS
22320|上古卷轴3晨风|The Elder Scrolls III: Morrowind|adventure_rpg|老滚3;晨风
261550|骑马与砍杀2霸主|Mount & Blade II: Bannerlord|action_rpg|骑砍2;霸主;MB2
48700|骑马与砍杀：战团|Mount & Blade: Warband|action_rpg|骑砍战团;战团
22100|骑马与砍杀|Mount & Blade|action_rpg|骑砍1
65530|黑道圣徒3|Saints Row: The Third|open_world|黑道圣徒
302510|罗马之子|Ryse: Son of Rome|hack_and_slash|Ryse
393080|使命召唤：现代战争重制版|Call of Duty: Modern Warfare Remastered|fps|COD4重制
359870|最终幻想10高清重制版|FINAL FANTASY X/X-2 HD Remaster|jrpg|FF10;FFX
256290|光之子|Child of Light|turn_based_rpg|光之子PC
391540|传说之下|UNDERTALE|turn_based_rpg|UT;地下传说
1671210|三角符文|DELTARUNE|turn_based_rpg|三角符文PC
368230|王国经典版|Kingdom: Classic|strategy|王国1
496300|王国：新大陆|Kingdom: New Lands|strategy|王国新大陆
701160|王国：两位君主|Kingdom Two Crowns|strategy|王国双冠
573170|尤库的小岛速递|Yoku's Island Express|platformer_runner|尤库
238320|失忆症：猪猡的机器|Amnesia: A Machine for Pigs|horror|猪猡的机器
239200|逃生|Outlast|horror|逃生1
1304930|逃生：试炼|The Outlast Trials|horror,party_multiplayer|逃生试炼
883710|生化危机2重制版|Resident Evil 2|horror|生化2重制
2050650|生化危机4重制版|Resident Evil 4|horror|生化4重制
1253920|盗贼遗产2|Rogue Legacy 2|roguelike_roguelite|盗贼遗产二
241600|盗贼遗产|Rogue Legacy|roguelike_roguelite|盗贼遗产1
588650|死亡细胞|Dead Cells|roguelike_roguelite|DC
233740|组织派对|Organ Trail: Director's Cut|survival|器官之路
274520|阴暗森林|Darkwood|horror|黑暗森林
774171|喵斯快跑|Muse Dash|arcade_rhythm|MD;暮色快跑
400910|拉比哩比|Rabi-Ribi|metroidvania|兔子弹幕
2230650|TEVI|TEVI|metroidvania|提薇
1637320|穹顶守护者|Dome Keeper|roguelike_roguelite|穹顶
793460|112接线员|112 Operator|management|112报警中心
503560|911接线员|911 Operator|management|911报警中心
282070|这是我的战争|This War of Mine|survival|我的战争
1174180|荒野大镖客2|Red Dead Redemption 2|open_world|大表哥2;RDR2
976730|光环：士官长合集|Halo: The Master Chief Collection|fps|光环合集;MCC
1240440|光环：无限|Halo Infinite|fps|光环无限
1672970|我的世界：地下城|Minecraft Dungeons|action_rpg|MC地下城
1928870|我的世界：传奇|Minecraft Legends|rts|MC传奇
534380|消逝的光芒2|Dying Light 2|open_world,survival|消光2;DL2
239140|消逝的光芒|Dying Light|open_world,survival|消光1;DL1
356190|中土世界：战争之影|Middle-earth: Shadow of War|action_rpg,open_world|战争之影
241930|中土世界：暗影魔多|Middle-earth: Shadow of Mordor|action_rpg,open_world|暗影魔多
1201230|了不起的修仙模拟器|Amazing Cultivation Simulator|management|修仙模拟器
1468810|鬼谷八荒|Tale of Immortal|adventure_rpg|鬼谷
1094520|部落与弯刀|Sands of Salzaar|adventure_rpg|部落弯刀
1948980|大侠立志传|Hero's Adventure: Road to Passion|adventure_rpg|大侠立志
1876890|逸剑风云决|Wandering Sword|adventure_rpg|逸剑
838350|太吾绘卷|The Scroll Of Taiwu|adventure_rpg|太吾
377530|侠客风云传|Tale of Wuxia|adventure_rpg|侠客风云传本传
650760|侠客风云传前传|Tale of Wuxia: The Pre-Sequel|adventure_rpg|侠客前传
1097420|侠隐阁|Path Of Wuxia|adventure_rpg|侠之道
1407450|仙剑奇侠传7|Sword and Fairy 7|adventure_rpg|仙剑7;仙七
994280|古剑奇谭3|Gujian3|adventure_rpg|古剑3;古三
1161120|古剑奇谭2|Gujian2|adventure_rpg|古剑2;古二
570780|轩辕剑外传：穹之扉|Xuan-Yuan Sword: The Gate of Firmament|adventure_rpg|穹之扉
1249800|轩辕剑7|Xuan-Yuan Sword VII|adventure_rpg|轩辕剑七
1189630|轩辕剑3外传：天之痕|Xuan-Yuan Sword III: The Scar of the Sky|adventure_rpg|天之痕
1722410|天命奇御2|Fate Seeker II|adventure_rpg|天命2
882790|天命奇御|Fate Seeker|adventure_rpg|天命1
1147560|小骨：英雄杀手|Skul: The Hero Slayer|roguelike_roguelite|小骨
588430|辐射避难所|Fallout Shelter|management|避难所
1084600|沙石镇时光|My Time at Sandrock|farming_crafting|沙石镇
666140|波西亚时光|My Time At Portia|farming_crafting|波西亚
1248130|模拟农场22|Farming Simulator 22|farming_crafting|FS22
787860|模拟农场19|Farming Simulator 19|farming_crafting|FS19
2300320|模拟农场25|Farming Simulator 25|farming_crafting|FS25
220|半条命2|Half-Life 2|fps|半条命二
1716740|星空|Starfield|adventure_rpg,space|星空PC
1063730|新世界|New World|mmorpg|新世界PC
2138710|师父|Sifu|fighting_martial_arts|师傅
2420110|地平线西之绝境|Horizon Forbidden West|open_world|西之绝境
9900|星际迷航OL|Star Trek Online|mmorpg,space|STO
223750|DCS世界|DCS World Steam Edition|space_flight_sim|DCS模拟飞行
288470|神鬼寓言：周年纪念版|Fable Anniversary|adventure_rpg|神鬼寓言重制
204030|神鬼寓言：失落之章|Fable - The Lost Chapters|adventure_rpg|神鬼寓言1
1286830|星球大战：旧共和国|STAR WARS: The Old Republic|mmorpg,space|SWTOR
255220|超级房车赛：汽车运动|GRID Autosport|racing|GRIDAS
703080|动物园之星|Planet Zoo|management|动物园之星PC
212680|超越光速|FTL: Faster Than Light|roguelike_roguelite|FTL
237990|旗帜的传说|The Banner Saga|strategy_tactical_rpg|旗帜传说1
774361|渎神|Blasphemous|metroidvania|神之亵渎
1366540|戴森球计划|Dyson Sphere Program|building_automation|戴森球;DSP
1366540|戴森球计划|Dyson Sphere Program|building_automation|DSP
632470|极乐迪斯科|Disco Elysium|adventure_rpg|极乐
1235140|如龙7|Yakuza: Like a Dragon|jrpg|人中之龙7
638970|如龙0|Yakuza 0|action_rpg|人中之龙0
834530|如龙极|Yakuza Kiwami|action_rpg|人中之龙极
927380|如龙极2|Yakuza Kiwami 2|action_rpg|人中之龙极2
1088710|如龙3重制版|Yakuza 3 Remastered|action_rpg|人中之龙3
1105500|如龙4重制版|Yakuza 4 Remastered|action_rpg|人中之龙4
1105510|如龙5重制版|Yakuza 5 Remastered|action_rpg|人中之龙5
1388590|如龙6生命诗篇|Yakuza 6: The Song of Life|action_rpg|人中之龙6
2058180|审判之眼：死神的遗言|Judgment|action_rpg,mystery_detective|审判之眼
2058190|审判之逝：湮灭的记忆|Lost Judgment|action_rpg,mystery_detective|审判之逝
2375550|如龙7外传：无名之龙|Like a Dragon Gaiden|action_rpg|无名之龙
1805480|如龙：维新极|Like a Dragon: Ishin!|action_rpg|人中之龙维新极
2072450|如龙8|Like a Dragon: Infinite Wealth|jrpg|人中之龙8
2909400|最终幻想7重生|FINAL FANTASY VII REBIRTH|jrpg|FF7重生
1462040|最终幻想7重制版|FINAL FANTASY VII REMAKE INTERGRADE|jrpg|FF7RE
1113560|尼尔：人工生命升级版|NieR Replicant ver.1.22474487139...|action_rpg|尼尔伪装者;尼尔人工生命
1233570|镜之边缘：催化剂|Mirror's Edge Catalyst|platformer_runner|镜之边缘2
17410|镜之边缘|Mirror's Edge|platformer_runner|镜之边缘1
1250410|微软模拟飞行|Microsoft Flight Simulator|space_flight_sim|MSFS2020
2537590|微软模拟飞行2024|Microsoft Flight Simulator 2024|space_flight_sim|MSFS2024
227300|欧洲卡车模拟2|Euro Truck Simulator 2|hobby_job_sim|欧卡
289070|文明6|Sid Meier's Civilization VI|turn_based_strategy|文明六;CIV6
1295660|文明7|Sid Meier's Civilization VII|turn_based_strategy|文明七;CIV7
4000|盖瑞模组|Garry's Mod|sandbox_physics|GMod;盖瑞;GMOD
223100|国土防线：革命|Homefront: The Revolution|fps|国土防线2
55110|红色派系：末日审判|Red Faction: Armageddon|third_person_shooter|红色派系4
20500|红色派系：游击战|Red Faction: Guerrilla|third_person_shooter|红色派系3
1506830|FIFA22足球|FIFA 22|team_sports|FIFA22
1313860|FIFA21足球|FIFA 21|team_sports|FIFA21
450540|热狗马蹄和手榴弹|Hot Dogs, Horseshoes & Hand Grenades|vr,fps|H3VR
805550|神力科莎：竞速|Assetto Corsa Competizione|racing_sim|ACC
244210|神力科莎|Assetto Corsa|racing_sim|AC赛车
228380|撞车嘉年华|Wreckfest|racing|撞车嘉年华1
280790|创造世界|Creativerse|sandbox_physics|创造宇宙
433340|史莱姆牧场|Slime Rancher|farming_crafting|史莱姆农场
1057090|奥日与萤火意志|Ori and the Will of the Wisps|metroidvania|精灵与萤火意志;奥日2
261570|奥日与黑暗森林|Ori and the Blind Forest|metroidvania|奥日原版;奥日1原版
387290|奥日与黑暗森林终极版|Ori and the Blind Forest: Definitive Edition|metroidvania|奥日1;精灵与森林
1361510|忍者神龟：施莱德的复仇|Teenage Mutant Ninja Turtles: Shredder's Revenge|hack_and_slash|忍者神龟复仇
985890|怒之铁拳4|Streets of Rage 4|hack_and_slash|SOR4
1959200|铁血联盟3|Jagged Alliance 3|strategy_tactical_rpg|JA3
12360|铁血联盟2|Jagged Alliance 2|strategy_tactical_rpg|JA2
55150|战锤40K：星际战士|Warhammer 40,000: Space Marine|third_person_shooter|星际战士原版
2183900|战锤40K：星际战士2|Warhammer 40,000: Space Marine 2|third_person_shooter|星际战士2
285160|乐高霍比特人|LEGO The Hobbit|adventure_rpg|乐高霍比特
214510|乐高指环王|LEGO The Lord of the Rings|adventure_rpg|乐高魔戒
920210|乐高星球大战：天行者传奇|LEGO Star Wars: The Skywalker Saga|adventure_rpg|乐高天行者
1172380|星球大战绝地：陨落的武士团|STAR WARS Jedi: Fallen Order|action_rpg|绝地陨落
1774580|星球大战绝地：幸存者|STAR WARS Jedi: Survivor|action_rpg|绝地幸存者
1794680|吸血鬼幸存者|Vampire Survivors|roguelike_roguelite|VS
1942280|土豆兄弟|Brotato|roguelike_roguelite|土豆
2321470|深岩银河：幸存者|Deep Rock Galactic: Survivor|roguelike_roguelite|深岩幸存者
2420510|全网公敌2：新世界|Cyber Manhunt 2: New World|mystery_detective|全网公敌2
1216710|全网公敌|Cyber Manhunt|mystery_detective|全网公敌1
1229900|无尽旅图|Carto|puzzle|卡朵
756800|缉私警察|Contraband Police|hobby_job_sim|边境警察
1509510|部落幸存者|Settlement Survival|city_settlement|部落幸存
1158310|十字军之王3|Crusader Kings III|grand_strategy_4x|十字军3
1687060|游戏王大师决斗|Yu-Gi-Oh! Master Duel|card_board|大师决斗;MD游戏王
601510|游戏王决斗链接|Yu-Gi-Oh! Duel Links|card_board|决斗链接
700330|SCP秘密实验室|SCP: Secret Laboratory|fps,horror|SCP SL;秘密实验室
251570|七日杀|7 Days to Die|survival|7DTD
108600|僵尸毁灭工程|Project Zomboid|survival|PZ;僵毁
1142710|全面战争战锤3|Total War: WARHAMMER III|grand_strategy_4x|战锤3全战
1154840|影子帝国|Shadow Empire|grand_strategy_4x|暗影帝国
1217060|枪火重生|Gunfire Reborn|fps,roguelike_roguelite|枪火重生PC
1003590|俄罗斯方块效应：连接|Tetris Effect: Connected|arcade_rhythm|俄罗斯方块效应
356190|中土世界战争之影|Middle-earth: Shadow of War|action_rpg|中土战争之影
1363080|庄园领主|Manor Lords|city_settlement|领主庄园
620|传送门2|Portal 2|puzzle|PORTAL2
1206560|世界盒子：上帝模拟器|WorldBox - God Simulator|sandbox_physics|世界盒子
1426210|双人成行|It Takes Two|party_multiplayer|双人游戏双人成行
367450|桥梁建筑师|Poly Bridge|puzzle|桥梁构造师
1549970|异形：火力小队|Aliens: Fireteam Elite|third_person_shooter|异形火力小队
1150530|死亡之屋重制版|The House of the Dead: Remake|fps|死亡之屋1重制
239030|请出示文件|Papers, Please|hobby_job_sim|请出示证件;请出示文件
234650|暗影狂奔：归来|Shadowrun Returns|strategy_tactical_rpg|暗影狂奔归来
300550|暗影狂奔：龙陨导演剪辑版|Shadowrun: Dragonfall - Director's Cut|strategy_tactical_rpg|暗影狂奔龙陨
1476970|放置传说|IdleOn - The Idle RPG|online_rpg|IdleOn
39140|最终幻想7原版|FINAL FANTASY VII|jrpg|FF7
225540|正当防卫3|Just Cause 3|open_world|JC3
8190|正当防卫2|Just Cause 2|open_world|JC2
517630|正当防卫4|Just Cause 4|open_world|JC4
208400|耻辱|Dishonored|life_immersive_sim|羞辱1
403640|耻辱2|Dishonored 2|life_immersive_sim|羞辱2
614570|耻辱：界外魔之死|Dishonored: Death of the Outsider|life_immersive_sim|界外魔之死
482400|网络奇兵重制版|System Shock|fps,scifi_cyberpunk|网络奇兵1重制
238210|网络奇兵2|System Shock 2|fps,scifi_cyberpunk|网络奇兵二
410710|网络奇兵增强版|System Shock: Enhanced Edition|fps,scifi_cyberpunk|网络奇兵原版
12110|侠盗猎车手罪恶都市|Grand Theft Auto: Vice City|open_world|罪城
205100|耻辱|Dishonored|life_immersive_sim|羞辱
201810|德军总部：新秩序|Wolfenstein: The New Order|fps|德军新秩序
350080|德军总部：旧血脉|Wolfenstein: The Old Blood|fps|德军旧血脉
612880|德军总部2：新巨像|Wolfenstein II: The New Colossus|fps|德军新巨像
1290000|冲就完事模拟器|PowerWash Simulator|hobby_job_sim|高压水枪模拟器
883710|生化危机2重制版|Resident Evil 2|horror|RE2重制
285010|汽车大亨|Automation - The Car Company Tycoon Game|hobby_job_sim|汽车公司大亨
346010|围攻|Besiege|sandbox_physics|围攻PC
588670|女巫来了|Witch It|party_multiplayer|Witch It
1435790|密室逃脱模拟器|Escape Simulator|puzzle|逃脱模拟器
105600|泰拉瑞亚|Terraria|survival|泰拉瑞亚PC
312520|雨世界|Rain World|platformer_runner|雨中世界
1119980|In Sound Mind|In Sound Mind|horror|In Sound Mind
620980|节奏光剑|Beat Saber|arcade_rhythm,vr|BS
1307890|王国重生|Kingdoms Reborn|city_settlement|王国重生PC
266510|上帝之手|Hand of Fate|card_board|命运之手
456670|命运之手2|Hand of Fate 2|card_board|命运之手二
2050650|生化危机4重制|Resident Evil 4|horror|RE4R
620|传送门2|Portal 2|puzzle|传送门II
960170|DJMAX致敬V|DJMAX RESPECT V|arcade_rhythm|DJMAX;DJMAX致敬
221910|史丹利的寓言|The Stanley Parable|story_rich|史丹利寓言
1703340|史丹利的寓言终极豪华版|The Stanley Parable: Ultra Deluxe|story_rich|史丹利终极版
319630|奇异人生|Life is Strange|story_rich|奇异人生1
532210|奇异人生2|Life is Strange 2|story_rich|奇异人生二
554620|奇异人生：暴风前夕|Life is Strange: Before the Storm|story_rich|暴风前夕
936790|奇异人生：本色|Life is Strange: True Colors|story_rich|奇异人生本色
1265920|奇异人生重制版|Life is Strange Remastered|story_rich|奇异人生1重制
239160|神偷|Thief|life_immersive_sim|神偷2014
211600|神偷黄金版|Thief Gold|life_immersive_sim|神偷1
211740|神偷2|Thief II: The Metal Age|life_immersive_sim|神偷二
6980|神偷3：致命暗影|Thief: Deadly Shadows|life_immersive_sim|神偷3
237850|梦陨|Dreamfall Chapters|story_rich|梦陨章节
207170|魔岩山传说|Legend of Grimrock|adventure_rpg|格林洛克传奇
251730|魔岩山传说2|Legend of Grimrock 2|adventure_rpg|格林洛克传奇2
405900|魔界战记|Disgaea PC|strategy_tactical_rpg|魔界战记1
495280|魔界战记2|Disgaea 2 PC|strategy_tactical_rpg|魔界战记二
1233880|魔界战记4完整版|Disgaea 4 Complete+|strategy_tactical_rpg|魔界战记四
1740720|见习死神|Have a Nice Death|roguelike_roguelite|祝你好死
673750|超级兔子人|Super Bunny Man|party_multiplayer|兔子人
1229490|究极杀戮|ULTRAKILL|fps|终极杀戮
519860|黄昏|DUSK|fps|Dusk黄昏
359870|最终幻想10高清合集|FINAL FANTASY X/X-2 HD Remaster|jrpg|FFXHD
1046930|刀塔霸业|Dota Underlords|auto_battler|自走棋刀塔
993780|多多自走棋|Auto Chess|auto_battler|自走棋
8930|文明5|Sid Meier's Civilization V|turn_based_strategy|文明五;CIV5
3900|文明4|Sid Meier's Civilization IV|turn_based_strategy|文明四;CIV4
1207650|宗主国|Suzerain|story_rich|Suzerain
3117820|苏丹的游戏|Sultan's Game|card_board,story_rich|苏丹
250760|铲子骑士|Shovel Knight: Treasure Trove|platformer_runner|铲子骑士宝藏
1794680|吸血鬼幸存者|Vampire Survivors|roguelike_roguelite|吸血鬼幸存者PC
588650|死亡细胞|Dead Cells|metroidvania|死亡细胞PC
205100|耻辱|Dishonored|life_immersive_sim|羞辱PC
236090|尘埃：幸福的轨迹|Dust: An Elysian Tail|metroidvania|尘埃幸福轨迹
107100|堡垒|Bastion|action_rpg|堡垒PC
237930|晶体管|Transistor|action_rpg|晶体管PC
462770|柴堆|Pyre|story_rich|火堆
504230|蔚蓝|Celeste|platformer_runner|蔚蓝山
40800|超级食肉男孩|Super Meat Boy|platformer_runner|超级肉肉哥
264200|一个人影|One Finger Death Punch|fighting_martial_arts|一指神功
980300|一指神功2|One Finger Death Punch 2|fighting_martial_arts|一指死亡拳2
224760|菲斯|FEZ|puzzle,platformer_runner|菲兹
250180|合金弹头3|METAL SLUG 3|shmup|合金弹头三
312610|合金弹头X|METAL SLUG X|shmup|合金弹头叉
366250|合金弹头|METAL SLUG|shmup|合金弹头1
250180|合金弹头3|METAL SLUG 3|shmup|MS3
310950|街头霸王5|Street Fighter V|fighting_martial_arts|SF5
1364780|街头霸王6|Street Fighter 6|fighting_martial_arts|SF6;街霸6
1498570|拳皇15|THE KING OF FIGHTERS XV|fighting_martial_arts|KOF15
222420|拳皇98终极之战|THE KING OF FIGHTERS '98 ULTIMATE MATCH FINAL EDITION|fighting_martial_arts|拳皇98;KOF98
222440|拳皇2002无限之战|THE KING OF FIGHTERS 2002 UNLIMITED MATCH|fighting_martial_arts|拳皇2002;KOF2002
222940|拳皇13|THE KING OF FIGHTERS XIII STEAM EDITION|fighting_martial_arts|KOF13
838380|死或生6|DEAD OR ALIVE 6|fighting_martial_arts|DOA6
311730|死或生5最后一战|Dead or Alive 5 Last Round|fighting_martial_arts|DOA5
544750|灵魂能力6|SOULCALIBUR VI|fighting_martial_arts|刀魂6;剑魂6
1716740|星空|Starfield|adventure_rpg|STARFIELD
42700|使命召唤黑色行动|Call of Duty: Black Ops|fps|黑色行动1
3830|脑航员|Psychonauts|platformer_runner|脑航员1
409710|生化奇兵重制版|BioShock Remastered|fps|生化奇兵1高清
703080|动物园之星|Planet Zoo|management|动物园之星
249130|乐高漫威超级英雄|LEGO Marvel Super Heroes|adventure_rpg|乐高漫威
647830|乐高漫威超级英雄2|LEGO Marvel Super Heroes 2|adventure_rpg|乐高漫威2
730|反恐精英2|Counter-Strike 2|fps|CS2
4465480|反恐精英：全球攻势|Counter-Strike: Global Offensive|fps|CSGO;CS:GO
570|刀塔2|Dota 2|moba|Dota2
431960|壁纸引擎|Wallpaper Engine|casual|壁纸软件候选不入游戏库
'''

QUERIES = '''
仙剑奇侠传|adventure_rpg
轩辕剑|adventure_rpg
古剑奇谭|adventure_rpg
侠客风云传|adventure_rpg
天命奇御|adventure_rpg
河洛|adventure_rpg
三国志|turn_based_strategy
三国群英传|rts
大富翁|card_board
幻想三国志|jrpg
圣女之歌|jrpg
双星物语|jrpg
伊苏|jrpg
轨迹|jrpg
东方|shmup
Touhou|shmup
逆转裁判|visual_novel
弹丸论破|visual_novel
STEINS|visual_novel
CLANNAD|visual_novel
Key|visual_novel
Fate|visual_novel
传颂之物|visual_novel
真三国无双|hack_and_slash
战国无双|hack_and_slash
无双大蛇|hack_and_slash
信长之野望|grand_strategy_4x
太阁立志传|life_immersive_sim
三国杀|card_board
铁甲雄兵|online_rpg
流星蝴蝶剑|fighting_martial_arts
小小梦魇|horror
生化危机|horror
寂静岭|horror
零|horror
Resident Evil|horror
Silent Hill|horror
FINAL FANTASY|jrpg
DRAGON QUEST|jrpg
Tales of|jrpg
Ys|jrpg
Trails|jrpg
Yakuza|action_rpg
Like a Dragon|action_rpg
Call of Duty|fps
Battlefield|fps
Medal of Honor|fps
Quake|fps
DOOM|fps
Wolfenstein|fps
S.T.A.L.K.E.R.|fps
Metro|fps
Hitman|life_immersive_sim
Splinter Cell|life_immersive_sim
Prince of Persia|platformer_runner
Tomb Raider|adventure_rpg
Need for Speed|racing
Forza|racing
Test Drive|racing
Colin McRae|racing
F1|racing
NBA 2K|team_sports
Football Manager|sports_sim_management
FIFA|team_sports
eFootball|team_sports
PES|team_sports
Dark Souls|action_rpg
Armored Core|action_rpg
Nioh|action_rpg
Monster Hunter|action_rpg
Dragon Age|adventure_rpg
Divinity|adventure_rpg
Dungeon Siege|action_rpg
Gothic|adventure_rpg
Risen|adventure_rpg
King's Bounty|strategy_tactical_rpg
Heroes of Might|turn_based_strategy
Might and Magic|turn_based_rpg
Age of Empires|rts
Command and Conquer|rts
Total War|grand_strategy_4x
Civilization|turn_based_strategy
LEGO|adventure_rpg
Sonic|platformer_runner
Rayman|platformer_runner
Mega Man|platformer_runner
Castlevania|metroidvania
Metal Slug|shmup
The King of Fighters|fighting_martial_arts
Samurai Shodown|fighting_martial_arts
Guilty Gear|fighting_martial_arts
BlazBlue|fighting_martial_arts
The Sims|life_immersive_sim
SimCity|city_settlement
Anno|city_settlement
RollerCoaster Tycoon|hobby_job_sim
Tropico|city_settlement
Zoo Tycoon|hobby_job_sim
Stronghold|rts
Settlers|city_settlement
Warhammer|strategy_tactical_rpg
Warcraft|rts
StarCraft|rts
Counter-Strike|fps
Out of the Park Baseball|sports_sim_management
Dragon Nest|mmorpg
LaTale|mmorpg
'''


def main():
    seeds = []
    for row in SEEDS.strip().splitlines():
        appid, zh, original, categories, aliases = row.split('|')
        seeds.append({'appid': int(appid), 'proposed_title': zh, 'expected_title': original,
                      'category_ids': categories.split(','), 'proposed_aliases': aliases.split(';')})
    queries = [{'term': row.split('|')[0], 'category_ids': [row.split('|')[1]]}
               for row in QUERIES.strip().splitlines()]
    # Overlapping snapshots deliberately combine recent reach with older franchises.
    queries = [{'key': f'global-top-sellers-{page}', 'term': '', 'filter': 'globaltopsellers',
                'start': page * 50, 'category_ids': []} for page in range(12)] + queries
    output = {'version': '0.5.0', 'checked_at': '2026-10-28',
              'scope': 'native PC first; notable console games retained; no mobile-only or emulator-only additions',
              'chinese_review_minimum': 50, 'steam_seeds': seeds, 'queries': queries}
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / 'manifest.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Discovery plan: {len(seeds)} seed references, {len(queries)} searches')


if __name__ == '__main__':
    main()
