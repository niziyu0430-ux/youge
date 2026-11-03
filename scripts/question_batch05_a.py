"""Hand-authored Gears 5, Max Payne 3 and GTAV Enhanced mode paths.

Every mode has its own twelve initial scenes and twelve written alternatives.
No runtime version or integration metadata is assigned in this source module.
"""
from question_authoring import question as Q, pack, source

SOURCES = [
 source('g5v5_store','官方｜Gears 5 Steam 本体与模式说明',
  'https://store.steampowered.com/app/1097840/Gears_5/','official',
  '本体战役与三人合作|Versus|Horde与Escape区别|角色与职业分别选择',
  '正文可读；只采用Gears 5本体模式，不把同页Hivebusters、重玩修改器或其他Gears作品写进基础前提。'),
 source('g5v5_op5','官方｜Xbox Wire Operation 5：角色与PvE职业解耦',
  'https://news.xbox.com/en-us/2020/11/17/gears-5-operation-5/','official',
  'PvE角色与职业独立|角色外观不决定职业|既有多人内容边界',
  '官方历史更新正文与索引可读；用于确认持续沿用的职业解耦，不采用当年数值、商店内容或活跃轮换。'),
 source('g5v5_jackflight','官方｜Xbox Wire：Gears 5的Jack飞行支援',
  'https://news.xbox.com/en-us/2019/08/19/gears-5-at-gamescom-2019/','official',
  'Jack为可操控飞行支援机器人|Jack不依赖人类掩体动作|Horde的Tap与设施防守',
  '公开正文已读；只取Jack移动与掩体差异。发布时角色与职业绑定的叙述以Operation 5解耦资料覆盖，不采用当年配表或数值。'),
 source('g5v5_jack','攻略｜Shacknews：战役Jack组件与配置',
  'https://www.shacknews.com/article/113753/how-to-upgrade-jack-in-gears-5','editorial_guide',
  '战役Jack主动与被动能力|组件与本存档成长|可选路径与升级|收藏品和组件统计',
  '正文可读；只使用组件、能力和战役路径结构，不采用升级费用、总量或攻略推荐。合作客人不强制亲手修改主机存档。'),
 source('g5v5_abilities','攻略｜Stevivor：Jack能力与终极升级',
  'https://stevivor.com/guides/gears-5-jack-abilities-ultimate-upgrades-guide/','editorial_guide',
  'Flash与电击支援|战役能力逐步开放|可选任务的能力升级',
  '公开索引核对能力及开放阶段；不把后期Barrier、Cloak、Hijack当成开局必有，也不把战役Jack技能树移入Versus。'),
 source('g5v5_campaign','攻略｜Cultured Vultures：战役、Skiff与合作Jack',
  'https://culturedvultures.com/gears-5-beginners-tips-campaign-escape-horde/','editorial_guide',
  '合作玩家可操控Jack|掩体射击|Skiff半开放区域|遗物武器与支线',
  '公开正文及索引可核对；只取玩法存在性。人类持枪题另给Jack行动路径；不把攻略中的最优建议变成正确答案。'),
 source('g5v5_horde','社区｜Gears Wiki：Gears 5 Horde',
  'https://gearsofwar.fandom.com/wiki/Horde_(Gears_5)','community_wiki',
  '波次与间歇|Energy共享与存入|Fabricator设施|Energy Tap|职业与技能卡|局外职业成长',
  '本轮曾取得正文，复访受限；采用可交叉核对的基础结构。旧版角色绑定职业已被Operation 5官方资料覆盖；不引用职业强度、价格或波数。经典规则缺少系统时用独立替代。'),
 source('g5v5_fabricator','社区｜Gears Wiki：Fabricator的Gears 5小节',
  'https://gearsofwar.fandom.com/wiki/Fabricator','community_wiki',
  'Fabricator初始搬运|Energy购买武器和设施|设施布置与维护',
  '直接访问受限，核对公开索引中明确标为Gears 5的小节；不采用页面前段Gears 4的制造机等级解锁规则。'),
 source('g5v5_versus','社区｜Gears 5玩家说明：自定义Versus电脑对手',
  'https://www.reddit.com/r/GearsOfWar/comments/d5y48q/','community_discussion',
  '自定义Versus可选地图与电脑对手|真人与电脑对手的路径区别',
  '公开讨论索引可读；仅确认自定义电脑练习入口，不采用高手建议、脚本、排名机制或当前匹配人口。'),
 source('g5v5_control','官方｜Gears 5 Steam开发者公告：Control与据点规则',
  'https://store.steampowered.com/news/posts/?appids=1097840&enddate=1615235906&feed=steam_community_announcements','official',
  'Control占领区域与转点|常规Versus武器拾取与个人重生的规则区别',
  '公开公告索引可读；Control只是已体验者的一条情境，不保证当前轮换开放。死亡竞赛或电脑自定义给独立替代，不引用赛制数值。'),
 source('mp3v5_manual','官方｜Max Payne 3 PC操作手册',
  'https://media.rockstargames.com/rockstargames-newsite/img/manuals/en_us/MP3_PC_Manual_M01.pdf','official_manual',
  'Bullet Time有限资源|Shootdodge与倒地射击|掩体会受损与侧翼|止痛药|双持会放下双手武器|单人HUD与武器轮',
  '官方PDF直接打开因文件过大失败；通过公开索引逐条核对相关手册段落，不声称通读全册。不采用多人Adrenaline/Burst、精确数量或默认键位。'),
 source('mp3v5_rockstar','官方｜Rockstar Design and Technology：瞄准与武器',
  'https://www.rockstargames.com/newswire/article/o349k55254a3o1/watch-the-new-max-payne-3-design-and-technology-series-video-tar.html','official_developer',
  '动作与枪械反馈|掩体和移动射击|Max的身体动作与瞄准衔接',
  '官网正文呈现受限，公开索引可核对开发者视频介绍；不据此捏造可改变剧情的选择或额外技能树。'),
 source('mp3v5_story','官方｜Rockstar Asked & Answered：Max Payne 3',
  'https://www.rockstargames.com/newswire/article/ak14o88381o725/asked-answered-max-payne-3-la-noire-red-dead-and-more.html','official_developer',
  '纽约旧警察与圣保罗保镖身份|独白叙事|Shootdodge表现',
  '公开索引核对开发者叙事与动作说明；身份选项只决定玩家在可控场面的行动风格，不改变固定剧情。'),
 source('mp3v5_collect','攻略｜PowerPyx：金枪零件、线索与章节检查点',
  'https://www.powerpyx.com/guides/max_payne_3.html','editorial_guide',
  '金枪零件收集|可调查线索|已完成章节检查点重玩|剧情固定演出与可操作射击区别',
  '正文可读；只采用系统与地点类型，不把奖杯精确击杀、难度或通关限制写成动机题。只问战役，不含Score Attack、New York Minute和多人。'),
 source('gtavev5_store','官方｜GTA V Enhanced Steam版本与内容说明',
  'https://store.steampowered.com/app/3240220/Grand_Theft_Auto_V_Enhanced/','official',
  'PC Enhanced入口|故事三位主角|GTA Online独立体验|洛圣都与布莱恩郡',
  '正文可读；仅映射3240220增强版，不把Legacy的271590重复接入；不要求GTA+、近期DLC资产或迁移存档。'),
 source('gtavev5_manual','官方｜Rockstar GTA V Game Help基础玩法手册',
  'https://dlassets-ssl.xboxlive.com/public/content/4f0a3089-ba2c-4f3d-9e38-102a41cbd885/GameManual/9dfeb637-1cb0-46c8-b7d7-0c58cf990494/en-GB/index.html','official_manual',
  '故事主角切换与各自能力|Franklin驾驶特殊能力|个人能力值随使用增长|抢劫准备与NPC队员|Los Santos Customs|手机与Snapmatic|自由活动|Online基础任务竞速与RP',
  '官方旧版手册正文可读，仅用于仍存在的基础系统，与当前增强版商店及支持页交叉核对。忽略旧转移流程、Social Club分享流程、精确数值和陈旧通缉文案。'),
 source('gtavev5_migrate','官方｜Rockstar Support：Legacy到Enhanced迁移说明',
  'https://support.rockstargames.com/articles/259ZyI1It8EACcCuOk5u4z/migrating-your-online-profile-from-gtav-legacy-to-gtav-enhanced-on-pc','official_support',
  'PC增强版与传承版分属不同入口|Online版本边界',
  '公开支持正文可读；只确认版本边界，不要求玩家执行迁移，不把一次性迁移或账号资产视为动机。'),
 source('gtavev5_photo','官方｜Rockstar Support：Snapmatic与头像支持变更',
  'https://support.rockstargames.com/articles/1KLoJrhjvC14GciaNoEHfD/changes-in-support-for-snapmatic-selfies-and-mugshots-as-player-avatars','official_support',
  '故事与Online均有Snapmatic|拍摄与外部头像服务的区别',
  '2026年公开支持索引可读；只问游戏内取景或本地截图，不假定仍能用旧社交网站流程上传、设头像或外部发布。'),
 source('gtavev5_range','攻略｜GTABase：故事射击场与Online射击场',
  'https://www.gtabase.com/grand-theft-auto-v/side-missions/shooting-range-challenges','editorial_guide',
  '指定射击挑战|成绩与奖牌|练习操作和能力值成长的区别',
  '公开索引核对既有射击场项目；未参加者可用早期驾驶替代。不采用当前武器伤害、价格或必须夺金的攻略。'),
 source('gtavev5_completion','攻略｜PowerPyx：GTA V补全项目',
  'https://www.powerpyx.com/gta-v-100-completion-checklist-guide/','editorial_guide',
  '故事收集与陌生人活动|射击场与其他消遣|完成清单和探索的区别',
  '公开攻略与索引核对项目种类，不采用100%精确门槛、剧透解答或把未解锁项目当作人人可做。Online不沿用故事100%清单。'),
]

PACKS = []

gears = pack('g5v5','战争机器5',['steam-1097840'],
 '本体战役／持久战Horde／常规对战Versus分别作答，不含Hivebusters与Escape',[
 Q(1,'人类士兵的掩体间隙','你操控持枪角色，眼前两个掩体之间留着可穿行的空隙，敌人暂时没有逼近。现在先做什么？',
  '在这段距离练一次进出掩体，让移动停得更稳|把贴墙、探身射击和退回接起来，找连贯的触感|看清两个掩体之间哪条视线会暴露，再选位置|换一条平时不用的侧路接敌，看看场面怎样变化',
  'practice_seeker feedback_engine puzzle_breaker route_choice','01持枪换侧和Jack换支援侧都只是当前枪械接近路线，i降route_choice；其余t/f/p不推能力。','g5v5_campaign g5v5_abilities',
  ('你在合作战役中只操控Jack。队友正从两个掩体之间向前，附近有你已经会电击的敌人。你先做什么？', '反复练靠近、电击和退开的距离，让这套动作稳定|跟着一次电击的命中反馈移动，享受支援接上交火|观察敌人面向与队友位置，再选切入电击的方向|绕到自己平时不去的一侧，试试另一种支援路线', 'practice_seeker feedback_engine puzzle_breaker route_choice')),
 Q(2,'手里的枪与Jack的支援','你操控人类角色，当前已能带不同距离的枪，也已经会让Jack用Flash干扰掩体后的敌人。面对这段交火，你先调整什么？',
  '用Flash干扰掩体后的敌人，再让远枪接露出的枪位、近枪接逼近者，调整这套互补|先理顺换枪、补弹和等Jack能力可用的次序|拿常用武器专练Flash之后探身的一次时机|换上当前可用但平时少带的一套枪械与支援配置，实际打过这段看看',
  'build_alchemist mission_preparation_plan practice_seeker try_available_setup','02普通少用枪械支援配置降try_available_setup，Jack换侧仅route_choice；原有换枪/补弹/能力等待先后忠实保留，y降mission_preparation_plan，不改成练习。保b前明确远近火力与Flash/电击打断互补。','g5v5_jack g5v5_abilities',
  ('你只操控Jack，当前会基础电击，正陪持枪队友推进。面对掩体两侧的敌人，你先做什么？', '用自己的近身电击打断靠近的敌人，让队友枪线接住更远目标，比较两者互补|安排靠近、支援和撤回的次序，别让动作挤在一起|选一个敌人专练电击后退开的时机|改从不常走的一侧靠近，试一次新的支援办法', 'build_alchemist mission_preparation_plan practice_seeker route_choice')),
 Q(3,'组件已经装进箱子','在可继续走动的区域，你们发现一箱Jack组件；当前存档已有几种可选能力配置，也留有未解锁升级。没有新敌人催促，你先做什么？',
  '把这次组件投入选定的Jack成长方向，留下后续还能用的提升|从当前已开放的能力配置中换上一套平时少用的配置，再实际交火体验|看本章组件记录，回头补一个已经知道位置的缺口|先走进箱子后面没看过的侧室，看看还藏着什么',
  'growth_keeper try_available_setup collector wanderer','03Jack持久组件成长g与真实章节缺项c可保留；泛泛能力搭配没有互补目的，降试当前配置。ALT谨慎侦察称号只是门口路线习惯，改route_variant。','g5v5_jack',
  ('还没用过组件菜单，只在战役早期一片已清场的区域移动。前方有主路，旁边还有能走进的小房间。你先做什么？', '检查刚才未明白的掩体和入口关系，弄清交火为何从那里展开|顺着可走的侧室看看，不先查里面有没有奖励|停步把小队刚才的话与眼前设施联系起来，想清为何来到这里|沿门口与已能走通的房间边缘绕一圈，体验另一种经过方向后再回主路', 'puzzle_breaker wanderer story_keeper route_variant')),
 Q(4,'Skiff停在岔路口','你已玩到能乘Skiff自由选路的一段。地图上有当前目标，也有尚未去过的可疑建筑，Skiff此刻停在岔路口。你先怎么走？',
  '先去没探过的建筑，不预先确认有没有奖励|把已知地点连成顺路的一圈，再把Skiff开出去|在空旷处练一次转向与停车，让操控更稳|有精力继续追目标，也想主动把Skiff沿喜欢的熟路从容开一段',
  'wanderer mission_preparation_plan practice_seeker cozy_resident','04Skiff与早期步行的地点、补给先后只当次准备，y降mission_preparation_plan，保留原计划含义；两h已有精力和可推进前提。','g5v5_campaign g5v5_jackflight',
  ('还没开过Skiff，只在早期清场后的小队行进路段；你可以操控人类角色或Jack移动，主路与可回头的一条通道都能经过。你先做什么？', '进入未看过的通道，看看这一区域还连到哪里|按已知补给位置安排一小圈，确认完再回主路|选通道里两个位置，练一次靠近、停住再退回，让自己的移动更稳定|自己仍有精神也能跟上主路，仍想沿刚熟悉的通道从容移动', 'wanderer mission_preparation_plan practice_seeker cozy_resident')),
 Q(5,'可选地点和能力奖励','你已经知道眼前这个可选地点能带来Jack的一项升级，入口也已能进入；当前并不需要马上走主线。先做什么？',
  '为这项会留在存档里的提升进入，把Jack继续养起来|先看自己缺的升级记录，确认这一处能补上哪格|读升级说明并对照现有能力的实际效果，先解释它会改变哪一处支援反应，再在取得后验证|先绕建筑外侧走走，更想发现它还有哪些可进入的角落',
  'growth_keeper collector puzzle_breaker wanderer','05已知持久升级g、真实缺项c和未知角落w成立；泛泛比较升级不算构筑，改具体说明与实际支援反应的p验证。','g5v5_jack g5v5_abilities',
  ('还没到能力支线，只在一个已经清场的早期房间。你看见可查看的收藏品，旁边有一条未走过的支路。先做什么？', '查看收藏品内容，弄清这里的人经历了什么|拿起这个已知收藏品，补入本章收藏记录|回看门口与掩体的位置，解释刚才敌人怎样过来|先走那条支路，即使不确定有任何东西可拿', 'story_keeper collector puzzle_breaker wanderer')),
 Q(6,'真人合作的一次停步','你正与真人同伴玩本体战役，大家刚停在下一片交火区域前，手头确有另一套可选枪械或支援配置，持枪角色与Jack都能讨论安排。你先做什么？',
  '问清谁先接敌、谁何时支援，把这次共同推进安排明白|接上同伴刚才的玩笑，边聊边一起走进去|和同伴说好试一套当前可选但平时少用的枪械与支援配置，再实际交火体验|和同伴商定改从另一条已可达侧路接敌，实际试这次进入方向',
  'quest_board social_spark try_available_setup route_choice','06真人q/o真实；普通换枪械支援配置降try_available_setup，换接敌方向降route_choice。单人ALT不假设能指挥AI Jack近身电击，原泛b实义改已会持枪动作换序的try_action_variant，无真人前提。','g5v5_store g5v5_campaign',
  ('你单人推进，其他小队成员是NPC。下一片交火区已经看得见，当前可以从两边掩体靠近。你先做什么？', '观察入口、掩体与敌人位置，判断各方向的视线|只用当下已会的持枪动作，把移动、换枪和探身出手换个先后，实际试这段交火|选一条路线专练一次探身与回位|换到自己平时不用的那边，认真试一次不同打法', 'puzzle_breaker try_action_variant practice_seeker route_choice')),
 Q(7,'人物留下的可读痕迹','在战役中一间仍可走动的房间，你刚拾起一件带文字的收藏品，小队对当前任务也已有自己的说法。现在先做什么？',
  '打开文字，把它和刚才的人物对话联系起来|确认收藏记录收下了它，再找这一区域已知漏项|沿房间已走通的出入口与物件位置换一圈经过方向，再回出口|走进没仔细看过的相邻空间，看看那里是什么样',
  'story_keeper collector route_variant wanderer','07已取得文字s、章节真实缺项c成立；调查者/侦察者称号只是路线，去r；ALT补给/出口原先后保留为mission_preparation_plan，不把它改成路线试用。','g5v5_jack g5v5_store',
  ('还没有调查收藏品，只记得开场小队交谈。现在交火结束，当前区域仍可自由走动。你先做什么？', '在可停留处，理一理刚才不同人物为何这样回应|把眼前可取补给与出口的顺序排好，实际沿这一圈走完|沿出口两侧已可达的通道绕一圈，体验不同经过方向后再出发|绕去此前没走到的一侧，认识这块战场的空间', 'story_keeper mission_preparation_plan route_variant wanderer')),
 Q(8,'清场后的当前画面','战役清场后，当前位置安全且能自行停留，你操控的角色或Jack都能移动并调整当前视角。你先做什么？',
  '挑一处背景，移动到合意位置，用普通截图做一张自己的战地取景|自己有精神且能跟小队继续，仍想沿熟悉掩体慢慢走一遍，享受这段自在行进|把自己已经会的穿过空隙、停步和转向换个先后，实际走一遍体会差别|沿已走通的入口一侧绕过这片熟悉区域，再从另一侧跟上小队',
  'style_director cozy_resident try_action_variant route_variant','08清场截图是a、主动停留h前提齐；普通戒备巡查不算r，普通移动先后不算i，分别改route_variant与try_action_variant。','g5v5_campaign g5v5_store',
  ('只玩过战役很早的一小段，现在刚清掉一间有数处掩体的房间，暂时不用触发下一步。你先做什么？', '用当前位置和镜头安排前景掩体与远处出口，截出自己想要的画面|自己有精神，也能跟小队继续，仍想沿已经走熟的小圈从容绕一遍|把已经会的移动、停住与转向换个先后，实际做一遍体验差别|沿出口边缘一条已经能走通的路绕一圈，再接回主路', 'style_director cozy_resident try_action_variant route_variant')),
 Q(9,'枪线真正连起来的那次','回想一次你操控持枪角色完成的战役交火，哪段自己实际做出的事最值得记住？',
  '进掩体、探身与射击连起来，反馈一直跟着手上的动作|原来总卡住的换位时机，经过几次尝试终于稳定|远枪处理对面枪位、近枪应付逼近者，Jack干扰又留下探身空档，工具在那次确实互补|从不同方向进入同一场交火，试出了自己没用过的办法',
  'feedback_engine practice_seeker build_alchemist route_choice','09两种枪与Jack支援b写明远近目标和干扰空档，换进入方向只记route_choice；全部为真实过去。','g5v5_campaign g5v5_abilities',
  ('只操控过合作战役的Jack。回想一次你真正完成的支援，最记得什么？', '电击、移动和队友火力接上时那段直接反馈|从靠得太近到能稳定电击后退开的练习过程|自己的电击打断了靠近的敌人，队友枪线接住更远目标，两种工具在那次确实互补|改走不常用的靠近路线，真的试出另一种支援方法', 'feedback_engine practice_seeker build_alchemist route_choice')),
 Q(10,'离开主路留下了什么','回想一次你在Skiff章节主动离开当前目标路线，真正让这趟绕行留下印象的是哪件事？',
  '先不知道那里有什么，自己走进去才发现了新地点|取回了选定的Jack升级，之后的存档里仍能继续用|补上了一处事先知道的收藏或升级缺口|停下来查看文字与环境，把人物经历连得更完整',
  'w g c s','半开放章节专属回顾另给早期回顾；成长不是当场补给。','g5v5_campaign g5v5_jack',
  ('还没到Skiff章节。回想开场清场后自己真正多停留的一小段，哪件事最有吸引力？',
   '走进主路旁没看过的房间，发现那里原来可以去|练了一次掩体转换，之后相同动作比原先稳定|拿到了一件已知漏掉的收藏品，记录少了一个缺口|读了一条已找到的说明，让刚才的事件多了来由',
   'w t c s')),
 Q(11,'Jack改变战役的过程','回想你在当前战役存档中使用或指挥Jack的经历，哪件已经发生的事最让投入有了意义？',
  '逐步收集组件并升级，Jack留下了持续可用的成长|自己调过已开放能力与枪械的搭配，让支援干扰留下的空档接上远近火力，实际感到了互补|反复练一次能力与移动的衔接，后来真的更稳|比较敌人的掩体与能力反应，弄明白了其中的关系',
  'growth_keeper build_alchemist practice_seeker puzzle_breaker','11V1真实组件升级g与可选能力/枪械配置b可保；ALT未保证哪种Jack帮助，不硬b、不默认人类可指挥AI电击，实义改过去已会支援与移动换序的0分动作行为。','g5v5_jack g5v5_abilities',
  ('只记得早期用过Jack的基础帮助，还没做升级。回想当时真正做出的操作，最记得哪一段？', '试了几次靠近和退开，终于能稳定做出那次支援|自己把当时已会的Jack支援与移动换过一次先后，实际体验了那段动作交接|支援命中与随后移动连起来，反馈很痛快|观察过敌人位置后再行动，验证了自己对视线的判断', 'practice_seeker try_action_variant feedback_engine puzzle_breaker')),
 Q(12,'战役里自己选择停留的事','回想已经玩过的本体战役，哪件你主动做过的事最能说明自己为何投入？',
  '为读懂人物动机，停下来把对话和已找到的文字对照|自己沿熟悉出入口选择过另一条已可达的经过路线，实际走出了不同的路段先后|移动角色与当前镜头，按个人主题截过一组战地画面|当时精力足且还能推进，自己仍在熟悉安全路段从容走过，享受自主停留',
  'story_keeper route_variant style_director cozy_resident','12h已有精力与进度可做、s文本联系、a实拍成立；谨慎侦察者称号只有熟路巡查，去r改过去真实路线变体。','g5v5_store g5v5_campaign',
  ('只回想最初玩过的一小段本体战役，你确实主动做过、也最在意的是哪件事？', '把小队的一段对话与刚发生的事件联系起来，想清人物为何这样说|自己沿已走通的门口边缘绕过一圈，再接回主路，实际体验了不同经过方向|用普通镜头调整掩体与角色的位置，截出一张自己安排的画面|当时小队还能继续、自己也有精神，仍在已清场的熟悉区域慢待过一阵', 'story_keeper route_variant style_director cozy_resident')),
], notes=[
 '战役、Horde、Versus各有独立的12道初始题与12道替代题。模式由玩家选择玩过哪些；未体验情境可换题。',
 '战役持枪题均有合作Jack能直接作答的替代，不把玩家Jack当AI，也不把NPC当真人。',
 '只问Gears 5本体；Hivebusters和Escape不包含在已声明模式中。',
])

horde = pack('g5hordev5','战争机器5持久战情境',['steam-1097840'],
 'Horde标准／Frenzy及可用的基础波次玩法；不含Escape',[
 Q(1,'Fabricator还没有落位','这局使用Fabricator，当前Energy够布置基础屏障；你正选第一片防守区域，制造机尚未落定。眼前开阔地、窄口和侧路都能选，先做什么？',
  '理顺补给、退路与设施的工作范围，安排一套能持续运转的防区|沿各入口观察视线，推敌人可能怎样绕进来|把将用屏障拖慢近敌与职业攻击接住停留的作用配好，再据此选防守落位|从一处自己平时不守、当前可达的位置接敌，实际体验这次防守方向',
  'systems_builder puzzle_breaker build_alchemist route_choice','01设施供给与维护能持续运转的防区才y，屏障拖敌与职业攻击互补才b并写实；只换防守位置i降route_choice，两ALT同理。','g5v5_horde g5v5_fabricator',
  ('这局没有你用过的制造机或设施，你已能在出生区域移动，前面有低墙与两条可接敌通道。你先做什么？', '观察入口、低墙和退路，判断敌人从哪边能看见自己|选一段从低墙出入的距离，练稳攻击或支援后退回的动作|把移动与手中射击、或Jack电击的反馈连成一段|从平时不守的一侧接敌，实际试一种新的守法', 'puzzle_breaker practice_seeker feedback_engine route_choice')),
 Q(2,'这一波结束后的Energy','这一波结束，你与真人同伴都有Energy，队伍正在考虑存入制造机、补给和设施维护。你先做什么？',
  '把Energy分给补给、设施维修和下一波保留，再按每波损耗复核，让防线持续运转|问清大家这轮要投入哪处，把不同人的花费与工作接好|边收拾防区边与同伴聊刚才那一幕，一起待着就很有意思|让现有屏障拖慢近敌，自己当前武器或Jack电击接住这段停留，比较两者互补',
  'systems_builder quest_board social_spark build_alchemist','02真人预算协调q、同游o成立；Energy跨波补给维修储备是真持续资源流y，设施拖敌与攻击互补保b。ALT普通动作换序只try_action_variant，原取补给/掉落/回位先后保留为mission_preparation_plan。','g5v5_horde g5v5_fabricator',
  ('你单人或和AI打波次，下一波尚未开始；地图上能看见敌人刚才留下的枪，自己的接敌点与补给点也已认得。你先做什么？', '把取补给、检查掉落物与回接敌点排成一圈，实际走顺|观察敌人刚才走过的通道，弄清为何能绕到防区侧面|在原接敌点练一次靠近、攻击和退回的时机；Jack就练电击后退开|把自己已会的靠近、攻击和退回换个先后，在下一波实际试出手交接的差别', 'mission_preparation_plan puzzle_breaker practice_seeker try_action_variant')),
 Q(3,'职业与技能卡不必绑外观','在使用职业和技能卡的Horde大厅，你已有几个可选职业；所选职业能装两张卡，一张可增强常用能力、另一张可补当前防守短板，且都已获得。现在先定什么？',
  '把这两张卡一起装进当前职业，检验能力增强与防守补缺能否互相补上|继续使用自己在培养的职业，让经验和卡解锁留下长期积累|沿用一套熟悉配置，专门练一种能力的使用时机|换一个平时不用的职业思路，体验不同的波次玩法',
  'build_alchemist growth_keeper practice_seeker try_available_setup','03普通换可用职业i降try_available_setup；b补明确已持两卡、可装两槽和增强能力/补防守两种互补效果。g是跨局经验及卡解锁，ALT无卡完整可答且换侧只route_choice。','g5v5_op5 g5v5_horde',
  ('还没用过职业卡，或只玩不采用它的基础波次。你已站在熟悉低墙旁，持枪角色或Jack都能用当前基础攻击接敌。先做什么？', '定一个从墙边出入的距离，反复练稳攻击与回位|沿一次移动和射击、或电击的连续反馈接战|看敌人路线与低墙视线，判断自己该从哪侧出现|给自己换一条与上波不同的接近和退出路线', 'practice_seeker feedback_engine puzzle_breaker route_choice')),
 Q(4,'Energy Tap与原防线之间','这局已启用Energy Tap，你和真人同伴正在两波之间行动。Tap与原防线并不在同一处，眼前都能前往。你先做什么？',
  '看看Tap周围的入口和视线，推下一波敌人怎样靠近|安排本轮取Energy、回补给与回防的路线|与同伴说清谁去取、谁留守、什么时候会合|试着换一个自己过去没守过的接应位置',
  'puzzle_breaker mission_preparation_plan quest_board route_choice','04Tap换守点i降route_choice；单次取Energy/补给/回防路径y降mission_preparation_plan。ALT明确每次攻击后须换位、换位完成前禁再出手，是真约束保i；原补给先后只记当次准备。','g5v5_horde',
  ('没遇过Energy Tap。现在两波之间，下一波还没开始，你已记得上波敌人分别出现在哪条通道。手边补给点与原接敌位置都能走到，先做什么？', '实际沿两处出敌通道查看，验证哪条路能绕到防区背后|安排这次取补给、回到接敌处与留一条退路的先后|在原接敌点重复练一次攻击后退开的距离|这一波每次完成攻击都先换到另一处已可达接敌位置，换位完成前不再次出手，实际试这条自选限制', 'puzzle_breaker mission_preparation_plan practice_seeker play_inventor')),
 Q(5,'设施之间怎样留出路','这局你能布置已有的屏障或其他设施，当前两波之间可以移动它们；没有真人同伴的既有布置需要改动。你先怎样安排？',
  '安排补给余量、设施维护与回防通路，下一波后再按损耗调整，让防区持续运转|用屏障拖慢近敌，让手中武器或Jack电击接这段被拖住的时间，比较两种工具互补|观察拐角和侧路，验证屏障放在哪里会改变接近关系|把已有屏障与其他可用设施换个当前可行的摆放配置，打一波体验',
  'systems_builder build_alchemist puzzle_breaker try_available_setup','05实际设施维护与波次损耗运营可y，屏障拖敌接攻击保真实b；只试摆放配置降try_available_setup。ALT原取补给/掉落/回位顺序只记mission_preparation_plan，整波禁用一条撤回通道是真自限i。','g5v5_horde g5v5_fabricator',
  ('没有可布置设施。波次间歇里，地上还有上波掉落的武器，你原来使用的接敌点和补给处都能返回。你先做什么？', '把检查掉落物、取补给与回原位的先后排顺，实际走完|观察掉落物所在位置与两条入口，推刚才的敌人怎样走到这里|绕墙移动后接上手中枪的射击、或Jack电击，投入动作连续回应的触感|给下一波保留一条自选禁用约束：整波不走刚才那条撤回通道，遇敌也改用另一条可达路线', 'mission_preparation_plan puzzle_breaker feedback_engine play_inventor')),
 Q(6,'真人同伴倒在低墙旁','真人同伴倒在附近低墙旁，仍能交谈，场面允许选择不同接近方式。你已决定去拉起他，先怎样做？',
  '与他和其他真人说清谁掩护、自己从哪里过去|回应他对刚才险情的吐槽，边过去边一起把这幕玩下去|观察敌人枪线与低墙角度，选一条接近路径|把接近、拉起和退回连起来，享受这段动作接上的反馈',
  'quest_board social_spark puzzle_breaker feedback_engine','06真人倒地时q/o只对人，动作反馈f与路径解释p成立；ALT枪械/电击换侧仅route_choice，AI不社交。','g5v5_horde g5v5_store',
  ('本局只有自己或AI同伴。你刚绕过一段低墙，眼前有敌人，退路仍在。现在先做什么？', '观察敌人面向与低墙两侧视线，再选接近方向|反复练一次从墙边出现、使用当前攻击再退回的动作|把移动与射击或Jack电击接起来，体验连续反馈|从刚才没用过的侧路靠近，试另一种接敌路线', 'puzzle_breaker practice_seeker feedback_engine route_choice')),
 Q(7,'一波中途的第二个方向','一波还没结束，原先只看正面的低墙，现在侧面的通道也有敌人出现；你仍有可移动的余地。当前先做什么？',
  '看清两个方向怎样互相遮挡，先解出自己还能站在哪里|沿熟悉的掩体动作移动，让射击或电击接上换位|选一段不太稳的侧向出入动作，专门把它练清楚|改用此前没试的绕行次序，看看能否形成不同接敌方式',
  'puzzle_breaker feedback_engine practice_seeker route_choice','07两变体都只是普通绕墙或反向进入，i降route_choice，不添加伪规则；t/f/p对应原有具体动作。','g5v5_horde g5v5_campaign',
  ('刚开始玩波次，只记得出生区低墙与身旁一条侧路；这次敌人正从那边接近，退路没有封住。你先做什么？', '看低墙与敌人方向，判断换到哪一侧还能观察到他|把绕墙移动与当前射击、或Jack电击连成一段|重复一次出墙后回位的距离，让动作稳定|反着走一遍自己原来的接近路线，试个不同办法', 'puzzle_breaker feedback_engine practice_seeker route_choice')),
 Q(8,'开局前的个人选择','你和真人同伴正准备再开一局Horde，当前职业已经选好，外观可用默认或自己已拥有的造型。先做什么？',
  '选角色和武器外观的色调，配出一套自己想呈现的样子|改选平时少玩的可用职业，给这一局试一种不同支援方式|约同伴继续刚才没聊完的话题，一起进熟悉地图|精力充足并能继续推进波次，仍提议在熟悉设定里从容重温守波',
  'style_director try_available_setup social_spark cozy_resident','08普通换已有职业i降try_available_setup；ALT谨慎守卫称号不证r，实义改成入口视线预测并用下一波来路核对的p；开局绕圈仅route_variant。h已有精力与可推进前提。','g5v5_store g5v5_op5',
  ('你单人或和AI开一局熟悉的Horde，当前已经选好可用角色，默认外观也可以。进场后尚能自行走动，你先做什么？', '移动到合意背景，安排角色与低墙的位置，用普通截图做自己的取景|先据入口与低墙视线判断敌人会从哪条线接近，再在下一波用实际来路核对|把熟悉防区换一条已可达的开局绕行路线，实际走一圈体验|自己仍有精力且波次可推进，也想先沿熟悉防区从容移动一圈', 'style_director puzzle_breaker route_variant cozy_resident')),
 Q(9,'一轮防守怎样接上','回想一次已经完成的Horde波次，哪件自己实际做过的事最有吸引力？',
  '自己按每波损耗分配过Energy给补给与维护，也复核过保留量，防线在后续波次持续运转|自己让屏障拖慢近敌，职业攻击接住那段停留，已持卡补上防守短板，实际体验过互补|把攻击与出入掩体接起来，反馈一路跟着动作|看懂了敌人绕行与防区视线的关系，验证了判断',
  'systems_builder build_alchemist feedback_engine puzzle_breaker','09跨波Energy按损耗分配与维护才y，屏障/职业攻击/已持卡互补b写实；ALT个人取补给回低墙原顺序保留为mission_preparation_plan，不强改目的。全部真实过去。','g5v5_horde g5v5_fabricator',
  ('没有设施或技能卡经历。回想一次自己打过的基础波次，最记得哪件事？', '把取补给和回到低墙的次序走顺，下一轮仍能照着运转|反复练过从低墙旁出现、攻击再退回的时机，自己的动作后来更稳|移动与攻击接上时那段连续反馈|发现敌人为何能从侧面绕到低墙后，想清了空间关系', 'mission_preparation_plan practice_seeker feedback_engine puzzle_breaker')),
 Q(10,'局外留下的积累','回想你在Horde长期使用职业的过程，哪件已经发生的事最让投入留下印记？',
  '持续使用同一职业，经验与卡解锁在不同场次间留下成长|自己换用过几套当时已获得的技能卡配置，实际体验了能力发动与守波的差别|为一项能力反复练时机，后来自己的动作明显更稳|改用过少用的职业思路，真的体验到一套新守法',
  'growth_keeper try_available_setup practice_seeker try_available_setup','10跨局职业经验与卡解锁g成立；普通换技能卡和少用职业都降try_available_setup，ALT换防守路线降route_choice。','g5v5_horde g5v5_op5',
  ('只玩过早期波次，还没有职业卡或等级成长的印象。回想那几局自己真正做过的事，最在意什么？', '把一次出入低墙的距离反复练过，后来不再仓促|对照敌人来路与低墙两侧视线，验证了从何处能看见自己|攻击命中、转身和移动接上时的直接反馈|换了自己平时不走的防守路线，发现另一种打法', 'practice_seeker puzzle_breaker feedback_engine route_choice')),
 Q(11,'一起守波的那一段','回想一次与真人同伴玩Horde，哪件已经发生的事最让你愿意记住这局？',
  '聊清了各自的投入与守点，让不同人的推进接到一起|同伴的聊天、玩笑和险情，成了大家共同经历的一段|自己和同伴试过另一套当时可用的职业与设施配置，实际体验了守波差别|为了自己的战地主题，在局间选位置和镜头截了大家所在的画面',
  'quest_board social_spark try_available_setup style_director','11真人q/o与真实截图a成立，泛泛换职业和设施没有互补目的，b降try_available_setup；ALT独自或AI无真人点。','g5v5_store g5v5_horde',
  ('你只与AI或独自玩过Horde。回想一次真实波次，最让你记住的是哪件事？', '看清侧路、敌人位置与低墙的联系，弄明白一次绕行|一个出入掩体的动作经过练习终于能稳定做出|移动与射击、或Jack电击连起来时很有反馈|在局间移动到选好的位置，用普通镜头截出自己安排的防区画面', 'puzzle_breaker practice_seeker feedback_engine style_director')),
 Q(12,'熟悉地图里的主动停留','回想已经玩过的Horde，你确实主动做过、也最在意的是哪件事？',
  '走到防区之外没看过的通道，认识了地图新的去处|当时还有精神继续打波次，自己主动选了熟悉设定，安稳重温了已经会用的守波过程|自己沿一条平时少用、当时可达的侧路进入接敌位置，实际体验过不同防守方向|移动角色与镜头，把防区截图整理成自己选定的视觉主题',
  'wanderer cozy_resident route_choice style_director','12过去h有精力与下一波可做，a是实际视觉主题，w为未知通道；普通守卫称号只是枪械接敌路线，r降route_choice。','g5v5_horde g5v5_store',
  ('只回想最早几轮Horde，哪件自己真正做出的事最值得留下？', '绕进起点旁没走过的通道，发现另一处可去的空间|当时有精力也能接下一波，自己仍沿熟悉低墙和退路从容移动过，过程本身就很合意|自己从熟悉低墙另一侧的可达通道接敌，实际试过不同进入方向|选择低墙与远处入口的相对位置，用普通截图呈现自己的防线取景', 'wanderer cozy_resident route_choice style_director')),
])

versus = pack('g5versusv5','战争机器5常规对战情境',['steam-1097840'],
 '常规Versus真人对战或自定义电脑对手；不把Horde职业、技能卡带入',[
 Q(1,'霰弹枪与低墙转角','你已用过Gnasher，在一张熟悉地图里靠近低墙转角，真人对手也在附近，当前还能选择接近方式。先做什么？',
  '专门练一遍贴墙后出手的距离，让动作更稳定|把贴靠、转向和射击接起来，享受即时反馈|先看转角视线和对手位置，推他可能怎样出现|围绕这局要赢下来的目标，选择自己最有把握的接战安排',
  'practice_seeker feedback_engine puzzle_breaker rank_worker','01真人胜负k与具体Gnasher动作t/f/p成立；电脑ALT普通换接近路线i降route_choice。','g5v5_store g5v5_versus',
  ('你只和电脑打过自定义Versus。现在拿常用枪靠近一处熟悉低墙，电脑对手在另一侧。你先做什么？', '固定一段出入低墙的距离，反复把动作练稳|把移动、探身和射击接成自己喜欢的节奏|看低墙与对手方向，判断他从哪里能看见自己|换一条平时不用的接近路线，试试另一种交火方式', 'practice_seeker feedback_engine puzzle_breaker route_choice')),
 Q(2,'地图拾取武器的岔路','这一局与真人对抗，采用地图武器拾取；你知道一件可拾取武器的位置，手里也有基础枪。眼前既可去取，也可留在原路线，先做什么？',
  '对照拾取武器与基础枪的用途，让一件接另一件不便处理的局面，再决定是否去取|安排接近、拾取和回到可接敌位置的步骤|围绕这局真人对抗的胜负，去争取自己准备使用的那件武器|改试一次自己平时不拿的地图武器，看看熟图能有何变化',
  'compare_available_setup mission_preparation_plan rank_worker try_available_setup','02单次武器拾取步骤不是运营，忠实保留原计划并降mission_preparation_plan；少用地图武器i降try_available_setup，b强调工具用途补缺，ALT已有两枪近远分工写实。 仅比较可选方案、尚未实际装配的选项只记配置比较；一次解锁未说明具体互动的选项只记购买，不强计构筑或成长动机。','g5v5_store g5v5_versus',
  ('没用过地图拾取，只在自定义Versus带基础枪行动。当前常用的两件枪都在手里，前面有开阔地与低墙。先做什么？', '让一件枪接开阔距离、另一件接低墙近身，实际检验两种射程互补|练稳从当前枪切到另一件再出手的动作|把一次移动、换枪与命中反馈连起来|观察开阔地与低墙之间的视线，再选择接敌位置', 'build_alchemist practice_seeker feedback_engine puzzle_breaker')),
 Q(3,'Control区域即将更换','你玩过Control，这局正与真人队友围绕占领区域交战，下一处区域已经能辨认。现在你先做什么？',
  '观察区域之间的入口与掩体，判断转过去会遇到什么视线|和真人队友说清谁留、谁先过去，把转点接上|围绕这局胜负与区域分数，先执行自己准备好的争夺路线|把跑动、进掩体与出手接起来，投入这段连续交锋',
  'puzzle_breaker quest_board rank_worker feedback_engine','03Control真人转点协调q和胜负目标k真实；ALT死亡竞赛/CPU换侧路线仅route_choice，不强制Control。','g5v5_control g5v5_store',
  ('只玩过死亡竞赛或电脑自定义。你刚重新进场，眼前一条路通向熟悉低墙，另一条通向地图侧边。现在先做什么？', '看两条路与正在交火位置的视线，推从哪里能接上场面|走熟悉低墙那条路，专门练一次进墙与出手的时机|把跑动、贴靠和射击连成自己喜欢的节奏|走平时不用的侧路，认真试一次不同的进场办法', 'puzzle_breaker practice_seeker feedback_engine route_choice')),
 Q(4,'真人小队开局前','你与真人组成的小队正在开一局Versus，当前可以讨论第一段接敌。你先做什么？',
  '问清大家首段要去哪里、谁看哪条线，把共同目标接好|继续接上同伴刚才的笑话，一起进场的经历最有意思|围绕赢下这局，提醒自己执行已准备的对抗安排|提议让不同枪械覆盖不同距离，试一套小队组合',
  'quest_board social_spark rank_worker build_alchemist','04真人不同枪械覆盖不同距离的b有互补，q/o与胜负独立；ALT补远近两基础枪前提并写明分工，普通换路线i降route_choice。','g5v5_store g5v5_versus',
  ('你独自进入自定义Versus，其他角色由电脑控制。当前已带远近两件基础枪出生，前面有两条能到交火区的路线。你先做什么？', '观察入口与掩体关系，推自己从哪边能看见交火|拿熟悉枪练一次进掩体后出手的时机|让远枪处理开阔射线、近枪接低墙转角，按当前两段距离检验互补|换一条平时不走的路线，看看会形成怎样的交火', 'puzzle_breaker practice_seeker build_alchemist route_choice')),
 Q(5,'主动装填的这一段间隙','这一局与真人对抗，你正使用带主动装填判定的枪，当前退在掩体后，有一次可自行控制的换弹间隙。先把注意力放在哪里？',
  '反复练按下第二次装填的时机，让这项动作稳定|把退回、装填与再次出手连起来，找顺手的反馈|理顺剩余弹药、装填和换位次序，让接敌流程不断开|围绕这局真人较量的结果，用已熟悉的装填安排接回交锋',
  'practice_seeker feedback_engine mission_preparation_plan rank_worker','05主动装填可专练且连续反馈真实；个人余弹检查/装填/换位顺序y降mission_preparation_plan，ALT同理，换出墙侧仅route_choice。','g5v5_versus g5v5_store',
  ('你只在电脑自定义里用普通装填，刚退回熟悉低墙后。补弹和绕到另一边都可做，你先做什么？', '练稳一次补弹后重新探身的时机|把补弹、移动和射击接成顺畅动作|按现有弹药与下一段移动安排补给和出手顺序|换一侧出墙，试一次与上一轮不同的接敌方式', 'practice_seeker feedback_engine mission_preparation_plan route_choice')),
 Q(6,'重新出生后还能换路','这一局与真人对抗，采用可再次出生的规则。你刚回到场上，知道上次交火在哪，眼前也能走另一条路线。当前先做什么？',
  '回看入口与交火位置，解释上次为何从侧面被看到|只抓住上次没做稳的一次移动，沿熟路重新练|围绕这局与真人的胜负，执行自己调整过的争夺安排|改从另一条路进入，试试熟悉地图的不同可能',
  'puzzle_breaker practice_seeker rank_worker route_choice','06重生后换通道是普通枪械接近路线，两个i均降route_choice；解释上次视线、练习和真实胜负目标可保留。','g5v5_control g5v5_versus',
  ('只和电脑在可重生自定义中玩。你刚出生，上一段常走低墙路，眼前的地图侧道也能走。先做什么？', '看侧道怎样连到交火区，验证自己的空间判断|沿低墙专练一次自己上次仓促的出入动作|连着跑动、贴靠与射击，重温手上顺畅的反馈|选侧道进入，让自己实际试一次不同路线', 'puzzle_breaker practice_seeker feedback_engine route_choice')),
 Q(7,'熟悉地图上的准备动作','你即将与真人打熟悉的Versus地图，现在已进入场内，首段接敌还未发生。你先做什么？',
  '沿一小段低墙练一次出入动作，重点是自己能否更稳|围绕这局胜负确认首段路线，把准备落实到较量|让跑动、贴靠与转向连成一段，找手感|走一条与自己惯常相反的路线，认真试一个新开局',
  'practice_seeker rank_worker feedback_engine route_choice','07反向路线/不同经过顺序都未新增约束，i降route_choice，去自定规则措辞；h有精神与可认真接敌前提。','g5v5_store g5v5_versus',
  ('你主动开了熟悉地图的电脑自定义，现在已经进场，也没有另设成绩要求。先做什么？', '选一处低墙，反复练一次进出距离|沿熟悉路线移动与射击，享受连贯反馈|沿一条与自己平时不同的已可达路线进入交火区，实际试这次方向|自己精神充足，也能继续认真接敌，仍想按舒服的熟路从容玩一段', 'practice_seeker feedback_engine route_choice cozy_resident')),
 Q(8,'角色外观与进场风格','你正与真人同伴在Versus大厅里，队伍一侧已经确定，可使用默认或自己已有的角色与武器外观。你先做什么？',
  '按自己选定的色调搭配可用角色和枪械外观|提议与同伴改走另一条当前可达的进入路线，实际体验熟图上的不同接敌方向|和真人同伴约好一起进场，继续刚才的聊天|查看自己已记录的上一场对抗结果，明确本场要争取的成绩目标',
  'style_director route_choice social_spark rank_worker','08真人大厅特殊经过路线没有新规则，i降route_choice；ALT谨慎守线者称号和开局顺序都只是路线，r/i降route_choice。默认外观截图a成立。','g5v5_store g5v5_op5',
  ('你只打电脑自定义，当前已经进场，角色和枪械可以都是默认外观，敌人尚未靠近。先做什么？', '移动到低墙旁调整当前镜头，截出自己安排的角色与地图画面|先根据低墙出口与电脑位置判断哪条枪线会看见自己，再到相应位置实际核对|改走一条自己平时少用的可达开局路线，实际试不同接敌方向|有精神也能去接敌，仍愿按自己的慢节奏沿熟悉低墙路线进入', 'style_director puzzle_breaker route_choice cozy_resident')),
 Q(9,'近距离交锋的记忆','回想一次你确实打过的真人Versus近距离交锋，哪件事最让你记住？',
  '贴靠、转向和射击一气接上，动作反馈很直接|一个原来不稳定的出手距离，经过练习终于掌握|这场较量的胜负或自己对抗成绩达到了设下的目标|看懂了低墙两侧的视线，验证了对手会怎样出现',
  'feedback_engine practice_seeker rank_worker puzzle_breaker','09两变体都是实际过去交锋，t/f/p和明确对抗成绩k可保留；CPUALT换熟路之外通道只是route_choice。','g5v5_store g5v5_versus',
  ('你只和电脑玩过自定义。回想一次真正打出的近距离交锋，最记得什么？', '移动、进墙和射击接上时那段畅快反馈|从仓促出墙到能稳定做出动作的练习过程|观察低墙与对手方向后，实际验证了自己的判断|改走惯常路线之外的通道，真的试出另一种打法', 'feedback_engine practice_seeker puzzle_breaker route_choice')),
 Q(10,'地图与武器关系变清楚','回想已玩过的一张Versus地图，哪件自己实际做过的事最有吸引力？',
  '自己让基础枪与拾取武器分别接不同距离和开火空档，实际体验了两者互补|看懂入口、低墙与开阔地怎样形成不同视线|主动走入先前没去过的支路，认识了地图新一侧|换过一条非惯常路线，让熟悉交火出现不同可能',
  'build_alchemist puzzle_breaker wanderer route_choice','10真实未知通道w与视线解释p成立，普通换/反向路线i降route_choice；b补基础枪与拾取武器接距离和开火空档的互补。','g5v5_versus g5v5_store',
  ('从没取过地图武器，只记得手中远近两件基础枪和起点旁一段低墙。回想自己真正做过的尝试，最在意什么？', '让手中两件基础枪与不同距离互相接应，形成合意打法|弄清低墙两边为什么能从不同方向看到自己|走入低墙旁未看过的通道，发现另一处可去的空间|用反向经过低墙的顺序打过一次，体验到了不同场面', 'build_alchemist puzzle_breaker wanderer route_choice')),
 Q(11,'与真人一起进入那一局','回想一次与真人同伴玩Versus，哪段已经发生的事最想留下？',
  '把首段目标、守线与转点说清，不同人的行动接上了|边玩边聊留下了共同的笑料和险情|围绕一场胜负准备并完成了自己设定的竞争目标|亲自选角色色调或画面取景，留下有自己主题的对战记录',
  'q o k a','协调与关系都要求真人；普通比赛胜负不自动等同努力目标。','g5v5_store g5v5_versus',
  ('你只和电脑玩过自定义。回想一次真正在场内做过的事，最在意哪一段？',
   '移动与射击接上时一直有畅快反馈|反复练的一次进出掩体，后来确实更稳定|看过侧道与低墙后，验证了自己对空间的解释|用已有外观与当前镜头安排过一张有个人主题的画面',
   'f t p a')),
 Q(12,'对战里自己主动做的事','回想已玩过的Versus，哪件确实做过的事最能说明自己当时的投入？',
  '围绕一场真人胜负或自己记录的对抗成绩准备并较量|反复练一段低墙出入动作，直到比之前稳定|按个人色调选过可用外观，或安排当前镜头留下主题截图|当时精力充足且有新交锋可接，自己仍主动选熟悉设定打了电脑自定义，喜欢其中安稳自主的节奏',
  'k t a h','真实过去的竞技、练习、表达或自主舒缓；没有对应经历可继续换题。','g5v5_store g5v5_versus',
  ('只回想最早玩过的电脑自定义，哪件自己真正做出的事最有吸引力？',
   '在低墙旁重复过一次时机，后来自己做得更稳|把移动和射击接起来，重温了喜欢的即时反馈|用普通镜头安排角色与低墙的位置，截出自己想呈现的画面|当时精神足，也有交火可接，自己仍沿熟悉路线从容玩过，享受自主掌握节奏',
   't f a h')),
])

# Extra mode objects only supply authored variants; one published pack owns all slots.
for slot in gears['slots']:
    for variant in slot['variants']:
        variant['modes'] = ['campaign']
for mode_id, suffix, authored in [('horde','HORDE',horde), ('versus','VERSUS',versus)]:
    for main_slot, mode_slot in zip(gears['slots'], authored['slots']):
        for variant in mode_slot['variants']:
            variant['id'] = main_slot['id'] + '.' + suffix + '.' + variant['id'].rsplit('.',1)[1]
            variant['modes'] = [mode_id]
            main_slot['variants'].append(variant)
gears['modes'] = [
 {'id':'campaign','label':'本体战役（含单人、人类合作角色与玩家Jack）','initial_variants':{}},
 {'id':'horde','label':'持久战Horde（标准／Frenzy与基础波次）',
  'initial_variants':{s['id']:s['id']+'.HORDE.V1' for s in gears['slots']}},
 {'id':'versus','label':'常规对战Versus（真人或自定义电脑）',
  'initial_variants':{s['id']:s['id']+'.VERSUS.V1' for s in gears['slots']}},
]
PACKS.append(gears)

maxpayne = pack('mp3v5','马克思佩恩3',['steam-204100'],
 '本体单人战役与已完成章节的战役重玩；不含街机、New York Minute与多人',[
 Q(1,'手动慢动作与眼前掩体','战役中你在掩体后，手动Bullet Time仍有余量，前方敌人和另一处掩体都已看得见。现在先做什么？',
  '选一次探身开慢动作的时机，专门把它练稳|把探身、慢动作射击和退回接成连贯反馈|先看敌人与两处掩体的视线，弄清移动时会暴露在哪里|从自己平时少用的一侧飞扑接近，实际体验那一边的交火方向',
  'practice_seeker feedback_engine puzzle_breaker route_choice','01换飞扑侧只为另一进入方向，不是新玩法，i降route_choice；ALT同样普通换出墙侧。t/f/p保留具体交火行为。','mp3v5_manual mp3v5_rockstar',
  ('只玩过开场。现在Max已经能在一处掩体边移动，敌人在另一侧，旁边仍能退出。你先做什么？', '重复一次探身和回位的动作，让时机稳定|把移动、开枪与退回连起来，投入直接的动作反馈|观察掩体高度与敌人方向，判断哪段能被看见|从另一侧出掩体，认真试一种不同的接敌路线', 'practice_seeker feedback_engine puzzle_breaker route_choice')),
 Q(2,'双持会放下长枪','你手里已有两把单手枪和一件双手长枪，当前在清场后能自由换武器。知道改双持会把长枪放到地上，你先怎样安排？',
  '保留单手枪与长枪，让各自在适合距离和对方装填空档接手，检验两种用途互补|安排携带、取回与补弹的次序，让下一段工具不断档|选自己当前喜欢的持枪方式，接着体验动作与枪械反馈|把长枪暂时放下，认真试一次平时不用的双持玩法',
  'build_alchemist mission_preparation_plan feedback_engine try_available_setup','02双持会放下长枪，普通改双持i降try_available_setup；b明确保留单手+长枪、各接适合距离与装填空档，不虚构三者同时持有。原个人携带/取回/补弹先后保留为mission_preparation_plan。','mp3v5_manual',
  ('还没同时带过这些枪，只用开场单手枪。现在在一处已清场的房间，枪里与备弹都有余量，下一段出口就在前面。你先做什么？', '专门练一次装填后重新瞄向门口的动作|把补弹、离开掩体和走向出口的步骤理顺|移动着重新举枪，体验动作与瞄准接上的反馈|回看门口与刚才敌人的位置，解释这段交火的视线关系', 'practice_seeker mission_preparation_plan feedback_engine puzzle_breaker')),
 Q(3,'正在受损的遮挡物','Max正靠在一处会被打坏的掩体后，已经能看到它受损，旁边还有能移动过去的遮挡。现在先做什么？',
  '观察受损掩体与敌人方向，判断哪些角度还挡得住|安排当前弹药、慢动作余量与转移顺序，再接下一段交火|专门练一次离开掩体后进入另一处的衔接|换一条平时不用的转移方向，试出不同接敌场面',
  'puzzle_breaker mission_preparation_plan practice_seeker route_choice','03受损掩体可转移，普通换方向i降route_choice；原弹药、慢动作余量与转移顺序只是当次准备，两y降mission_preparation_plan，保留计划含义不强改练习。','mp3v5_manual',
  ('还没注意过掩体损坏，只在早期一个房间靠着低矮遮挡物，另一处掩体也能到达。你先做什么？', '看敌人和两处掩体的方向，判断哪段移动会暴露|理顺补弹、离开和重新出手的次序|重复练一次从这处掩体移到另一处的动作|沿另一条已可达的方向从这处掩体转到下一处，实际试交火路线', 'puzzle_breaker mission_preparation_plan practice_seeker route_choice')),
 Q(4,'飞扑落地之后','你刚完成一次Shootdodge，Max已经落地但仍能转向、开枪或装填，起身移动也可做。附近有可返回的掩体，你先做什么？',
  '保持倒地姿态转向瞄准，练清这个角度怎样出手|把落地、射击与起身接起来，体验身体动作的连续反馈|看当前身位与敌人视线，判断倒地和起身各会露在哪里|把已经会的落地瞄准、装填与起身换个先后，实际试这次动作交接',
  'practice_seeker feedback_engine puzzle_breaker try_action_variant','04Shootdodge落地后换动作先后只是try_action_variant；ALT换出墙侧是route_choice。瞄准练习、反馈和视线解释不推能力。','mp3v5_manual mp3v5_rockstar',
  ('还没用过飞扑，只在开场掩体边结束一轮射击，当前可以装填、换一侧探身或移动。你先做什么？', '反复练一次装填后重新探身的时机|把回掩体、装填与再次射击连成顺手的节奏|观察敌人方向和掩体边缘，判断哪侧仍能看到他|从惯常探身另一侧的可达位置接敌，实际体验这次进入方向', 'practice_seeker feedback_engine puzzle_breaker route_choice')),
 Q(5,'止痛药与下一间房','你刚清掉一段战役交火，眼前能取的止痛药已经看见，手动慢动作条与备弹也能查看；下一扇门尚未触发。现在先做什么？',
  '理顺补给、补弹和走向门口的步骤，安排下一段资源使用|回看交火留下的入口与枪线，解释刚才哪里造成暴露|拿当前余量练一次探身后退回的动作，重点是自己的稳定|让补弹、举枪与移动一气接上，继续体会动作反馈',
  'mission_preparation_plan puzzle_breaker practice_seeker feedback_engine','05止痛药/弹药/慢动作都是当前资源，原出门整备顺序忠实保留并降mission_preparation_plan，不计运营或回血成长。','mp3v5_manual',
  ('还没遇到止痛药选择。早期一间房已经清场，Max可以装填并在两处掩体间移动，出口尚未触发。你先做什么？', '把装填、走位与出门步骤理顺再走|回看两处掩体与敌人出现的位置，弄清刚才的交火关系|重复练一次从墙边举枪后回到掩体的动作|连着走位、举枪与转向，享受手上反馈', 'mission_preparation_plan puzzle_breaker practice_seeker feedback_engine')),
 Q(6,'线索与金枪零件都看得见','你在一片仍可自由走动的已清场区域，已经发现可调查的线索，也看见一件金枪零件。没有必须立刻推进的事件，你先做什么？',
  '调查线索，听Max怎样解释它与刚才事件的联系|取下已知的金枪零件，补上章节收集记录的一格|走进旁边还没看过的角落，先看看那里究竟有什么|移动Max和当前镜头，以场景物件为主题截一张自己的构图',
  'story_keeper collector wanderer style_director','06真实未有金枪零件取得c、未见角落w、构图a、线索独白s成立；ALT戒备旧警探称号只是清场巡路，去r改route_variant。','mp3v5_collect mp3v5_story',
  ('还没找过线索或金枪零件。Max在最早一间已清场的房内，仍能移动、举枪和调整当前镜头，出口尚未触发。先做什么？', '用当前枪练一次探身、收枪和退回掩体的衔接|把举枪、转向与走动接起来，体会Max身体动作的连续反馈|回看敌人来路与现有掩体，解释刚才哪里会被侧面看见|沿已可达门口与熟悉掩体边缘换一圈经过路线，再回出口前', 'practice_seeker feedback_engine puzzle_breaker route_variant')),
 Q(7,'旧警察与现任保镖','一段独白刚结束，Max暂时停在已清场且仍可走动的房间；你不能改写剧情，但能决定如何走向出口。现在先做什么？',
  '判断门边哪处能看见房内另一入口，再走到那里实际核对视线|留在可停步处，把刚才独白与自己已见过的事件联系清楚|在现有两处掩体间重复一次转移，把自己的动作练稳|把房间里已能走通的门口与掩体换一条经过路线，实际走一遍',
  'puzzle_breaker story_keeper practice_seeker route_variant','07房内普通经过顺序i降route_variant；旧警探/保镖称号不支持r，C实义改成门口是否能看见另一入口的现场预测验证p，避免两个近义绕路选项；s只联系已见独白。','mp3v5_story mp3v5_manual',
  ('只记得开场独白，现在最初一间房刚清场，Max能在出口前停留与移动。你先做什么？', '先判断门边哪处能看见房里另一入口，再走到那里实际核对视线|把开场独白与眼前刚发生的事联系一下，再继续|利用房间现有遮挡，反复练一次进出掩体|换一条房内已可达的绕行路线，实际走过掩体与门口', 'puzzle_breaker story_keeper practice_seeker route_variant')),
  Q(8,'已经打开的战役检查点','你通过章节选择重玩已完成检查点的自由交火段，当前已有两种可用持枪方式，其中有已知未取的线索或金枪零件；这次不采用街机计分。现在先做什么？',
   '只练一处飞扑落地后的瞄准与起身，让它比上次稳|重温慢动作、枪械与身体动作连续接上的感觉|回到一个自己已知漏掉的线索或金枪零件位置，把缺口补上|换用当前已经可用、平时少用的持枪配置，实际打过这段体验差别',
   'practice_seeker feedback_engine collector try_available_setup','08重玩自由交火段补两种可用持枪方式前提，普通试持枪i降try_available_setup；ALT当前检查点换进入方向降route_choice，c为已知未取物。','mp3v5_collect mp3v5_manual',
   ('没有重玩过章节，只在首次战役的当前检查点开始，前面的掩体路线已能看清。现在先做什么？', '挑一次出掩体再回位的动作，认真练稳|让移动、举枪与射击连成顺畅反馈|观察门口与两处掩体的联系，弄清各自看得见哪里|换一个与自己平时相反的接近方向，实际试一遍', 'practice_seeker feedback_engine puzzle_breaker route_choice')),
 Q(9,'慢动作没有停在画面里','回想一次你确实用过Shootdodge、落地后继续射击的战役交火，哪段自己实际做出的事最值得记住？',
  '落地、转向、射击与起身连在一起，反馈很痛快|原来仓促的一次瞄准或起身，反复试后终于稳定|观察掩体、落地点与敌人方向后，验证了自己的判断|自己从平时少用的一侧飞扑接近，实际体验过那条交火方向',
  'feedback_engine practice_seeker puzzle_breaker route_choice','09两个换飞扑侧/绕侧只记route_choice，t/f/p均已发生操作，不以落地次数推能力。','mp3v5_manual mp3v5_rockstar',
  ('只玩过开场掩体射击，还没用过飞扑。回想当时自己真正做出的动作，最记得什么？', '探身、射击和退回连起来时的直接反馈|一次原先乱掉的探身时机，后来能稳定做出来|看过掩体和敌人方向后，弄明白了为什么那侧会暴露|换过另一侧接近，体验到了与惯常不同的交火', 'feedback_engine practice_seeker puzzle_breaker route_choice')),
 Q(10,'调查之后留下的东西','回想一次自己在清场后停步调查或取景的经历，哪件已经发生的事最有吸引力？',
  '调查一件线索后，Max的独白让人物经历多了联系|取到一件已知缺少的金枪零件，章节记录少了一格空白|走进未看过的角落，发现这个房间还有另一面|移动Max与镜头，按自己的光线或物件主题截出了画面',
  's c w a','表达来自自己的取景动作，不能仅凭喜欢视觉风格计a。','mp3v5_collect mp3v5_story',
  ('没有调查物或取景经历，只回想最早一段开场独白与掩体交火，哪件自己真正经历过的事最在意？',
   '听清Max的独白，把自己刚见到的场面连进他的经历|举枪、转向与射击连续接上，身体动作很快给出回应|看懂入口和遮挡物的关系，弄明白敌人为什么从那里出现|一次原来仓促的探身回位，经过尝试后终于变稳',
   's f p t')),
 Q(11,'手里工具与房间连上以后','回想已经打过的一段战役，哪件真正发生过的变化最让投入有意义？',
  '自己比较过双持会放下长枪的取舍，最后让单手枪与长枪分别接适合距离和装填空档，实际体验了互补|把止痛药、弹药与手动慢动作的使用步骤理顺，后续交火接得上|反复练一次掩体转移，自己后来做得更稳定|从敌人的侧翼与受损掩体看出原因，解开了之前没明白的局面',
  'build_alchemist mission_preparation_plan practice_seeker puzzle_breaker','11单手与长枪互补写实，不暗示双持仍带长枪；ALT慢动作接初始枪只是核心反馈，b降f。两处原药量/弹药/出手先后保留为mission_preparation_plan，不强改练习。','mp3v5_manual',
  ('只用过开场枪械。回想自己真打过的一间房，哪件事最让你记住？', '自己手动开慢动作接上初始枪瞄准命中，投入时间变慢与开火连续回应的感觉|安排好补弹、离开遮挡和再次出手，让动作流程接上|原来仓促的一次探身回位，经过练习真的稳了|观察入口与掩体后，弄清了敌人为什么能从侧面出现', 'feedback_engine mission_preparation_plan practice_seeker puzzle_breaker')),
 Q(12,'这段Max经历中的主动行动','回想已玩的本体战役，哪件自己确实做过的事最说明当时的投入？',
  '为理解Max的处境，停下来把独白与已调查线索对照|自己沿已清场房间的另一侧门口与掩体边缘走过，再接回可达出口前|用普通镜头安排Max与场景物，截过一组自己选定主题的画面|自己曾在能全程普通瞄准的自由交火段，禁用手动Bullet Time与Shootdodge，只用普通掩体射击实际打过',
  'story_keeper route_variant style_director play_inventor','12V1泛规则具体为自由交火段禁手动Bullet Time和Shootdodge，只用普通掩体射击，保真实禁用i；ALT普通经过route_variant，C实义改过去门口视线预测验证p，两个近义巡路分开。','mp3v5_story mp3v5_manual mp3v5_collect',
  ('只回想最初玩过的一小段，哪件自己真正做出的事最有吸引力？', '听过独白后停步，把它和刚才眼前的事连起来|自己曾判断门边哪处能看见房内另一入口，再走到那里实际验证过视线|移动角色与镜头，截出了自己安排的前景和出口画面|自己换过最早清场房内一条已可达的经过路线，实际走出了不同路段先后', 'story_keeper puzzle_breaker style_director route_variant')),
], notes=[
 '仅单人战役；无街机或多人专属题，因此首次游玩与只玩战役者可完整作答。',
 'Bullet Time、Shootdodge、倒地操作、双持携带和线索调查分别形成具体情境，不使用精确资源数值。',
 '全卷无真人社交、永久技能树或普通击杀成绩的强行映射；黄金零件按收藏解释，不把普通枪械写成可升级角色。',
])
for slot in maxpayne['slots']:
    for variant in slot['variants']:
        variant['modes'] = ['campaign']
maxpayne['modes'] = [
 {'id':'campaign','label':'本体单人战役（含战役章节重玩）','initial_variants':{}}
]
PACKS.append(maxpayne)

gtav = pack('gtavev5','GTA5增强版',['steam-3240220'],
 'PC Enhanced：故事模式与GTA Online分别作答；不混Legacy、FiveM或近期DLC资产前提',[
 Q(1,'Franklin的自由驾驶路口','故事模式里你已能让Franklin自由活动，当前驾车停在路口，熟悉街道与没走过的支路都能选，也没有通缉或任务倒计时。先做什么？',
  '在熟悉拐角反复练一次刹车和转向，让动作稳定|沿街开起来，体验转向、车身和加速接上的反馈|转进没开过的支路，看看会到城市哪一面|自己此刻有精神，车也能继续往新处开，仍想沿熟悉的一小圈从容驾驶，享受自在节奏',
  'practice_seeker feedback_engine wanderer cozy_resident','Franklin驾驶能力不移给其他主角或Online；此题不要求已用特殊能力。','gtavev5_manual gtavev5_store',
  ('还没自由开过车，只记得能让角色在城市街边走动的一段，旁边有熟路与可进入的小巷，没有紧迫任务。现在先做什么？', '在街边练一次走动、转向与停步的衔接|让走动和转动镜头接起来，体验操控的连续反馈|走进没看过的小巷，先看看它通到哪里|精力充足且还有街区可探索，仍想沿熟悉街段慢走，自己掌握停留节奏', 'practice_seeker feedback_engine wanderer cozy_resident')),
 Q(2,'洛圣都改车王里的现有车辆','故事模式里，你把当前可改装的自用车开进Los Santos Customs；想看的外观、发动机与刹车改项都已可选，资金够做本次所选改装。现在先做什么？',
  '比较发动机加速改动与刹车效果，让加速和进弯减速互相补上，再选能负担的一套|按自己选定的配色和轮毂主题，把车做成想呈现的样子|保留熟悉配置，出去专练一次转弯和停车|换一套当前可用但平时少用的车辆改装配置，实际开出店体验',
  'compare_available_setup style_director practice_seeker try_available_setup','02普通改另一已有车辆配置不算i，降try_available_setup；ALT普通绕街i降route_variant。V1补可用且负担得起的发动机/刹车，并以加速与减速互补支持b。 仅比较可选方案、尚未实际装配的选项只记配置比较；一次解锁未说明具体互动的选项只记购买，不强计构筑或成长动机。','gtavev5_manual',
  ('还没改过车。你已在故事自由活动中开着一辆普通车，街边能安全停下，前方一段熟路也能继续开。现在先做什么？', '停在选好的背景前，调整普通镜头，截出自己安排的车辆构图|在熟悉路口练一次刹车与转向的衔接|开一段熟路，感受车身和方向输入接上的反馈|给自己定一条平时不走的绕街次序，实际开一圈', 'style_director practice_seeker feedback_engine route_variant')),
 Q(3,'抢劫规划板上的实际选择','故事已推进到一场能同时选择方案与NPC队员的抢劫准备，规划板当前就能操作。你先围绕什么作决定？',
  '把已有准备步骤和资源先后理清，再选接下来的安排|把当前可选NPC的岗位特长与方案所需的驾驶、枪械或技术任务对上，按岗位互补选组合|先看已有简报与人物交代，弄清他们为什么接下这次行动|从原先打算的方案换到当前另一套可选方案与NPC配置，亲手准备并实玩体验',
  'mission_preparation_plan build_alchemist story_keeper try_available_setup','03谨慎策划者称号不支持r，改为实试当前另一方案/NPC配置的try_available_setup；任务资源步骤仅mission_preparation_plan。b明确NPC岗位特长与方案分工互补；ALT街区司机只是驾驶路线，去r。','gtavev5_manual',
  ('还没到抢劫规划。当前故事自由活动中，地图上已有一个可去的主线标记与一个陌生人标记，手机里也有刚收到的人物消息。先做什么？', '把补给、出发点与目标顺序排好，实际开始这一圈|打开现有消息，把人物刚才的要求与已知事件接起来|取当前自用车，换一条已可达的街区接事路线，实际开过去体验|先绕进目标旁边没去过的街段，看看那里是什么样', 'mission_preparation_plan story_keeper route_variant wanderer')),
 Q(4,'三位主角当前都能切换','你已解锁多位故事主角，当前自由活动没有锁定切换，地图与各自状态都能查看。你先让谁做什么？',
  '切到最想继续追踪人物处境的那位，去看他当前已开放的任务|切到一位当前能自由活动的主角，沿所在街区另一条已可达路线步行或驾车，实际体验|切到一位能力值尚未达到自己培养目标的主角，开始可用的训练活动|切到另一位所在区域，走一条自己还没见过的街路',
  'story_keeper route_variant growth_keeper wanderer','04泛生活身份与街区司机取车未足证角色扮演，保守降实际route_variant；人物任务s、未知区域w及保留能力值g成立。','gtavev5_manual',
  ('只玩到Franklin自由活动，当前还不用切换。手机、附近街路和已开放活动都能使用，先做什么？', '查看他刚收到的消息，去接最想了解的一段人物事件|取当前自用车，沿一条不同于惯常的可达街路去接事，实际体验路线|选一段驾驶活动，继续培养他自己会保留的驾驶能力值|转进还没看过的小路，发现这个街区的新去处', 'story_keeper route_variant growth_keeper wanderer')),
 Q(5,'射击场同一个已开放项目','你在故事射击场已经选到一个可重复的项目，当前主角射击能力值尚有成长空间，能直接开始。现在为这一轮选什么重点？',
  '固定练一次瞄准与换目标的动作，重点是自己能否更稳|持续培养当前主角会保留的射击能力值|冲自己已经记下的项目成绩或更高奖牌结果|享受射击、靶面反馈与换目标连续发生的节奏',
  't g k f','成长、练习与个人成绩分开；没有参加射击场不推能力。','gtavev5_range gtavev5_manual',
  ('没参加过射击场。故事自由活动中，Franklin驾驶能力值尚可培养，已在普通车上，眼前一段熟悉道路可重复经过。现在先做什么？',
   '重复练一个拐角的刹车和转向，让自己的动作稳定|继续驾驶，培养Franklin自己会保留的驾驶能力值|让连续转弯和加速接起来，体验车身与操控反馈|驶入那条还没看过的分支道路，先看看它通向哪里',
   't g f w')),
 Q(6,'通缉搜索中的下一段路','故事自由活动中，你已离开直接追逐，警察正在搜索，当前车还能走普通路与一条侧街。没有必须走的任务路线，现在先做什么？',
  '结合小地图搜索范围与街道视线，判断哪里会再被发现|理顺转入侧街、等待和再次出发的步骤，安排这段脱离搜索的流程|把转向、刹车与避开街头障碍接成连贯驾驶|试一条自己没用过的侧路，看看这片街区还允许怎样绕行',
  'puzzle_breaker mission_preparation_plan feedback_engine route_variant','06脱离搜索的个人步骤不是经营，y降mission_preparation_plan；普通试侧街i降route_variant，不套枪械route_choice；搜索范围推视线p及早期ALT无警察机制可答。','gtavev5_manual',
  ('还没留意过搜索机制。故事自由活动中你在街边步行，附近有熟悉街段、可进入的小巷和一个能停步的路口。现在先做什么？', '观察街道、围墙与小巷的连通关系，验证另一侧能否走到|走进自己没去过的小巷，看看那里是什么|移动到路口选好前景与远处建筑，用普通截图做一张个人取景|自己有精力且还能沿小巷往新处走，仍愿在已熟悉街段从容绕一圈', 'puzzle_breaker wanderer style_director cozy_resident')),
 Q(7,'已知碎片与尚未见过的街区','你已经开始收集故事中的信件碎片，也知道眼前一条支路上有自己尚未取的那一片；当前在自由活动，旁边街区也能逛。先做什么？',
  '去取这个已知缺项，把收集记录补上一格|转入另一条没走过的路，更在意城市还有什么未见|查看手机里一条现有的人物消息，接着了解那段人物事件|先选碎片附近建筑作背景，移动角色与镜头截自己的城市主题画面',
  'c w s a','不说每片碎片都能读出完整信件；故事收集不移入Online清单。','gtavev5_completion gtavev5_manual',
  ('还没收集过碎片。当前故事自由活动中，一个已开放的陌生人标记就在附近，街边还有你没走过的通道。现在先做什么？',
   '去接触标记对应的人，了解他这次究竟遇到了什么事|先走那条陌生通道，即使不知道会不会有任务或奖励|精力充足，也能接触眼前的陌生人事件，仍想在熟悉街段慢转一圈|把角色与街角背景安排好，用普通镜头截出自己的街区画面',
   's w h a')),
 Q(8,'一次由自己安排的城市停留','故事自由活动中，当前主角能在街边走动、使用已有衣装与手机，也没有任务催促。你先做什么？',
  '选择街景与人物位置，用Snapmatic或普通截图做一张自己主题的取景|沿已有步道反复练一次跑动、转向与停步的交接，让自己的角色控制更稳定|沿一条当前已经可达、平时少走的步道与楼梯穿过街区，实际体验不同经过方向|精神充足且可接已开放活动，仍愿去熟悉海边或街区慢走，享受自主停留',
  'style_director practice_seeker route_variant cozy_resident','08跑者称号不计r，专项虚拟跑动转向停步练习计t；主替代步道与楼梯普通换路均只作route_variant，不后加禁用条款包装i。h有精力且仍有进度可做，a为实际自主取景。','gtavev5_manual gtavev5_photo',
  ('还没用过Snapmatic或衣柜。当前主角已能在街边自由走动，普通镜头可调整。先做什么？', '移动到合意背景，用普通镜头安排前景、角色与远处建筑，留下主题截图|在已有步道反复练一次跑动转向后停住的位置，让自己的控制更稳定|给自己定一条不同于刚才的步行经过顺序，实际走一遍|有精神且有未去街段或已开放活动可做，仍愿在熟悉小段街路从容停停走走', 'style_director practice_seeker route_variant cozy_resident')),
 Q(9,'驾驶里真正连起来的动作','回想一次自己在故事模式实际驾车的经历，最让你记住的是哪件事？',
  '刹车、转向与再加速一气接上，车身反馈很有感觉|一个原本不稳定的拐角，反复练后终于做稳|主动走了一条陌生支路，发现了城市新的去处|那次自己还有精力和可去的目标，仍选熟悉路线从容开过，安稳驾驶的过程本身就喜欢',
  'f t w h','只问故事已有驾驶体验，不由车速或撞车推能力。','gtavev5_manual',
  ('只回想故事最初开过的那一小段车，哪件真正发生的事最有吸引力？',
   '转动方向、车身回应和继续前进连起来很顺手|一次停车或转弯从仓促变得较稳定|多开进一条此前没看过的街路，认识了新地方|当时有精神，车也能继续往新处开，自己仍沿熟悉的一段路从容驾驶，掌握了舒服的节奏')),
 Q(10,'人物与自己扮演的方式','回想一次故事主角自由活动或任务准备，哪件已经发生的事最让投入留下印记？',
  '停下来查看消息、简报与对话，把人物动机连得更清楚|自己沿一条不同于惯常的已可达城市路线步行或驾车，实际体验过那段经过|理顺了抢劫准备或出发补给的步骤，流程终于接上|持续培养同一主角的驾驶或其他能力值，投入留在了这位角色身上',
  'story_keeper route_variant mission_preparation_plan growth_keeper','10泛生活身份/街区司机的动作仍是路线，去r降route_variant；个人抢劫准备和出发步骤y降mission_preparation_plan，角色保留能力值g与人物动机s成立。','gtavev5_manual',
  ('还没到抢劫，也只玩过Franklin。回想自己确实做过的事，最在意什么？', '打开消息或听完对话，把他接下这件事的缘由弄清|自己取过当时可用的车，沿一条非惯常但可达的接事路线实际开过|把出发前补给、找车与到目标的先后理顺|继续驾驶来培养Franklin自己的能力值，看到了能保留的积累', 'story_keeper route_variant mission_preparation_plan growth_keeper')),
 Q(11,'城市留下了自己的痕迹','回想一次故事自由活动里主动做过的事，最有吸引力的是哪件？',
  '按个人配色改过自用车，或移动人物与镜头拍出主题画面|取回了一件事先知道缺少的故事收集物，补上记录|走进原本没去过的街区，发现城市还有新地方|安排过主角能力值培养，投入在后续仍能保留',
  'a c w g','表达必须有修改或构图动作，不把欣赏城市画面自动计a。','gtavev5_manual gtavev5_completion gtavev5_photo',
  ('没改车、没做收集，只回想早期故事自由活动。哪件你真正做过的事最在意？',
   '用普通镜头安排角色与街景，截出自己想表达的城市画面|在熟悉拐角反复练过操作，后来自己做得更稳定|走入先前没去过的小巷，发现了另一处可去空间|继续驾驶或跑动，培养了当前主角自己会保留的能力值',
   'a t w g')),
 Q(12,'自由活动时已经作出的选择','回想故事模式里你主动安排过的一段活动，哪件事最能解释当时的投入？',
  '重复练射击或驾驶动作，直到自己比原来稳定|围绕已经记下的射击场或其他现有项目成绩，完成了一次争取纪录的尝试|自己沿一条平时少走、当时已可达的街区步道与楼梯路线走过，实际体验了不同经过方向|当时精神充足且有已开放新活动可做，自己仍选择熟悉一小圈，实际享受过安稳自主的停留',
  'practice_seeker rank_worker route_variant cozy_resident','12主替代普通街区经过路线均只作route_variant，去掉普通步行后加禁用规则的i包装；h有精神且仍有活动可做。四项均是实际过去经历，k有明确项目纪录目标。','gtavev5_manual gtavev5_range',
  ('没有消遣项目成绩的经历，只回想早期故事街区自由活动。哪件自己真做过的事最有吸引力？', '把一处转弯、停步或进出掩体的动作练得比之前稳|沿街移动与驾驶接起来，重温了顺手的反馈|实际按自己另定的街区经过顺序走完一圈，试了新的玩法|当时精力足且有已开放的事可做，自己仍沿熟悉街段从容玩过，安稳的过程本身就合意', 'practice_seeker feedback_engine route_variant cozy_resident')),
], notes=[
 '只挂PC Enhanced的3240220；故事与Online各自12道初始题和12道替代题，不要求Legacy经历或账号迁移。',
 '故事的主角切换、特殊能力、能力值、NPC抢劫队员与收集清单均不移作Online默认前提。',
 'Online只采用基础城市、常规联系任务、竞速和已拥有或可用物件，不强制任何近期DLC产业、GTA+或高价载具。',
 '摄影只需游戏内取景或本地普通截图；不要求对外上传、发布或使用旧版头像服务。',
])

online = pack('gtaveonlinev5','GTA5增强版Online情境',['steam-3240220'],
 'GTA Online基础城市、联系任务、常规竞速与当前可用物件；不含FiveM',[
 Q(1,'Online城市里已经能自由活动','你已经进入GTA Online，当前不在差事或追逐中，身旁有普通车辆与可走街路，手机也能打开现有差事入口。现在先做什么？',
  '把取车、到任务入口和途中补给的顺序安排好，实际开始这一圈|走进自己还没去过的街段，先发现城市有什么|用可重复的基础活动继续培养自己角色会保留的能力值或等级|自己精力充足且有现成差事可接，仍想去熟悉街区慢转一圈，享受自主从容的节奏',
  'mission_preparation_plan wanderer growth_keeper cozy_resident','01个人取车/补给/任务入口先后y降mission_preparation_plan，未知w、角色保留能力等级g和有新地方可去时的h成立。','gtavev5_store gtavev5_manual',
  ('刚开始Online，只在街边自由走动，还没接过差事；普通镜头能调整，近旁有熟路与小巷。先做什么？', '看街道与巷口的连接，实际验证能从哪里走到另一边|走进未去过的小巷，不先查有没有奖励|在一段路反复练走动、转向与停步的衔接|自己有精神、街区也有新地方可去，仍想沿熟悉街段从容走一遍', 'puzzle_breaker wanderer practice_seeker cozy_resident')),
 Q(2,'Online自己的车与已有改项','你在Online已有一辆可长期保留的自用车，当前开进改车店；外观、发动机与刹车改项都已可用，资金够做本次所选改装。现在先做什么？',
  '按自己的车身配色、轮毂与细节主题做一套外观|让发动机加速改动与刹车效果补上彼此的进弯短板，选一套想实际检验的组合|为这辆长期保留的自用车装上已开放且负担得起的性能升级，让持续投入留下可保留的车辆性能提升|换用一套当前可装、自己平时少用的车辆改项，实际开出去跑选定路线',
  'style_director compare_available_setup growth_keeper try_available_setup','02自用车升级必须可用且负担得起、保留性能提升，g保留；b明确发动机加速与刹车效果互补。街头巡游司机称号不证r，改试已有配置try_available_setup；ALT绕街仅route_variant。 仅比较可选方案、尚未实际装配的选项只记配置比较；一次解锁未说明具体互动的选项只记购买，不强计构筑或成长动机。','gtavev5_manual',
  ('还没有可改装车辆。当前Online自由活动中，你能使用一辆普通车，街边可停车，前面有熟悉路口。现在先做什么？', '把车停在选定背景前，调整普通镜头，留下个人主题构图|给自己换一条不常经过的街道次序，实际开一圈|在熟悉路口练稳一次刹车与转向|把转弯、车身回应和继续加速连起来，投入驾驶反馈', 'style_director route_variant practice_seeker feedback_engine')),
 Q(3,'真人合作联系任务的准备','你与真人同伴已进入一项大家能玩的联系任务准备阶段，当前可以讨论工具与进场。你先做什么？',
  '问清任务目标、谁走哪条线与何时会合，把大家的推进接上|接着聊刚才的事，能一起做这一单本身就很有意思|比较大家当前可用的枪械与进场距离，组成一套互补配置|提议与同伴改从另一条当前可达的侧路进场，实际体验这次交火方向',
  'quest_board social_spark build_alchemist route_choice','03真人分路与会合q、共同经历o成立，枪械不同距离互补可b；普通换进场路i降route_choice，单人ALT任务步骤y降mission_preparation_plan。','gtavev5_manual gtavev5_store',
  ('你只单人玩过允许单人进入的基础联系任务。当前已到任务区域外，知道目标在里面，附近有掩体与两条接近路线。先做什么？', '把补弹、接近与完成目标后离开的次序排好|观察入口、掩体和可见敌人的关系，判断各侧视线|沿一条熟路练稳一次进掩体与探身出手|让移动、射击与退回接起来，投入这段即时反馈', 'mission_preparation_plan puzzle_breaker practice_seeker feedback_engine')),
 Q(4,'已参加过的一项陆地竞速','你已经参加过一项普通陆地竞速，现在又到同类项目的准备阶段，允许使用的车型与路线都已明确。你先围绕什么进入这一轮？',
  '把一个不稳的弯角当练习点，重复练刹车与转向|冲自己记下的完成时间，或与本场真人争一次名次|比较弯角、出弯距离与熟悉车辆的反应，提出一条走线判断并实跑验证|从当前允许的可用车型里换一种自己平时少开的，实际跑过这项竞速体验',
  'practice_seeker rank_worker puzzle_breaker try_available_setup','04普通换当前允许车型不算i，降try_available_setup；ALT普通绕街不算规则，降route_variant。k有真实用时/真人名次目标，p已有走线判断和实跑验证，h补有其他活动可做。','gtavev5_manual',
  ('没参加过竞速。Online自由活动中你已在一辆普通车里，前面一条熟悉街路没有任务或追逐要求。现在先做什么？', '把熟悉路口的一次刹车与转向练稳|让转弯、加速与车身回应连起来，享受驾驶反馈|换一条当前已可达的绕街路线，实际开一圈体验不同经过方向|自己仍有精力，且能去未到街段或已开放活动，仍愿无成绩目标地从容驾驶熟悉小圈', 'practice_seeker feedback_engine route_variant cozy_resident')),
 Q(5,'差事列表与自己的积累','你已用过Online基础差事列表，当前几项已开放任务或竞速可选；也已查明一枚游戏内基础奖章或成就的缺项，这次可选活动确能做它的条件。现在先做什么？',
  '继续一项自己熟悉的活动，为角色下一段可保留的等级或能力成长积累|把接差事、返回与补给的先后安排成可重复运行的一圈|专为取得这枚游戏内列表尚未有的基础奖章或成就，进入可做条件的活动实际争取|先不进差事，开到旁边自己没去过的街段，看看那边有什么',
  'growth_keeper mission_preparation_plan collector wanderer','05个人差事补给循环y降mission_preparation_plan；c改明确游戏内未得奖章/成就与当前可做条件，不是个人记录。ALT补体力尚可成长前提，个人绕圈步骤也只当次计划。','gtavev5_manual',
  ('还没用过差事列表。Online街边能自由走动，前面有熟路、小巷与可停路口；当前角色体力能力值仍有成长空间。你先做什么？', '沿街继续跑动，培养自己角色会保留的体力能力值|把路口、取车处和返回点排成一圈，实际走顺|用普通镜头选择前景与远处建筑，留一张自己的取景|走进还没去过的小巷，即使不知道会发现什么', 'growth_keeper mission_preparation_plan style_director wanderer')),
 Q(6,'本次任务前的现有工具','你在Online已有一把支持瞄具与扩容弹匣的基础步枪，两个配件都已可装且资金够所选配置；正准备进入熟悉联系任务。现在先调整什么？',
  '用瞄具接远处定位、扩容弹匣减少连续交火中的装填中断，比较两个部件的互补|安排弹药、进场、换枪与退出的次序，让任务流程连上|保留熟悉工具，专练一次进掩体后探身的时机|换用当前已经可用、自己平时少用的一套步枪配件配置，实际进任务体验',
  'build_alchemist mission_preparation_plan practice_seeker try_available_setup','06普通试已有枪械/配件配置i降try_available_setup；b补支持且已可装、负担得起的瞄具与扩容弹匣，分别接定位和持续火力。任务次序y降mission_preparation_plan，ALT换枪线只route_choice。','gtavev5_manual',
  ('只有早期默认工具，也只玩过一小段联系任务。现在已到目标区附近，眼前有遮挡物和可退回的路。先做什么？', '观察敌人、遮挡与入口的视线，判断哪里还能接近|固定练一次出掩体射击再退回的动作|把移动、举枪与命中反馈连成一段|换到自己平时不用的那一侧，试另一种进场路线', 'puzzle_breaker practice_seeker feedback_engine route_choice')),
 Q(7,'车库里的已有收藏','Online里你已有车库、几辆自用车和一个可用车位；已确认一辆尚未有、当前可购买存入的普通车型，也有一辆自用车可升级，钱够作本次所选投入。现在先做什么？',
  '专为补齐那辆已知还没有的普通车型，现在购入并存进现有空位|开出自己持续培养的那辆车，去装可选性能升级，让这份长期投入继续留下可保留的车辆性能提升|按自己的色调主题选车开出去，在合意背景前取景|取一辆平时少开的车，实际换一种城市驾驶体验',
  'collector growth_keeper style_director try_available_setup','07普通试少开的已持车i降try_available_setup；收藏改真实尚未有且现在能买、能存的普通车型，补资金与空位前提。g是持久可用升级。ALT避开惯常拐角只是route_variant。','gtavev5_manual',
  ('没有车库收藏。Online自由活动中你可以用一辆普通车，眼前是已熟悉的街口与尚未去过的侧路。现在先做什么？', '驶入还没去过的侧路，发现城市新的去处|停在选好的街景前，调整普通镜头，截一张自己安排的车辆画面|自己有精神且车还能继续探索，仍想沿熟悉街路从容开一圈，自主掌握节奏|换一条当前已走通、避开惯常拐角的绕街路线，实际开过体验', 'wanderer style_director cozy_resident route_variant')),
 Q(8,'角色衣装与城市身份','Online自由活动中，你可以使用默认或自己已有的衣装、手机和街区空间。当前不在任务里，先做什么？',
  '按个人色调搭配已有衣装，再选街角背景拍一张自己的造型取景|在已有步道反复练一次跑动、转向与停步的交接，让自己的角色控制更稳定|换一条当前已可达、平时少走的步道与楼梯路线，实际走一圈体验不同经过方向|精力充足且有已开放活动或新街段可去，仍愿在熟悉街区从容停停走走，重温自主节奏',
  'style_director practice_seeker route_variant cozy_resident','08跑者称号不计r，虚拟跑动转向停步的专项练习计t；主替代普通步道楼梯路线均只作route_variant，不后加禁用条款保i。h明确精力与可做内容，a有实际形象表达。','gtavev5_manual gtavev5_photo',
  ('还没换过衣装或用过Snapmatic。Online角色已能在街边自由走动，普通镜头可调整。你先做什么？', '移动角色与镜头，把街边物件安排成自己想呈现的主题画面|沿现有步道反复练一次跑动转向后停住的位置，让自己的角色控制更稳定|换一条街区里当前已经可达的穿行路线，实际走过体验不同经过方向|精力足、也能继续在城市探索，仍想在已经走熟的街路从容转转', 'style_director practice_seeker route_variant cozy_resident')),
 Q(9,'已经跑过或打过的一段','你既打过Online联系任务，也参加过陆地竞速。回想这些真实经历，哪件自己实际做过的事最让你记住？',
  '一处进掩体或转弯的动作反复练过，后来真的稳了|移动、出手或转向接起来时，有连续而直接的反馈|围绕竞速用时或真人名次目标，完成了一次争取成绩的较量|同一角色的等级或能力值持续积累，投入之后还能保留',
  'practice_seeker feedback_engine rank_worker growth_keeper','09V1明确联系任务与竞速都体验过，避免任务玩家被迫承认竞速名次；ALT早期自由驾驶的换路线i降route_variant，角色保留能力g真实。','gtavev5_manual',
  ('只回想最初Online自由驾驶，还没做过差事。哪件自己真正做过的事最在意？', '反复练了一处刹车与转向，后来动作比原来稳定|连贯转弯和加速时，车身反馈一直跟着操作|实际换一条不同经过顺序，发现熟路还能有别的玩法|继续驾驶，让自己角色会保留的驾驶能力值积累起来', 'practice_seeker feedback_engine route_variant growth_keeper')),
 Q(10,'城市里留下的个人痕迹','回想Online里一次自己主动安排的自由活动，哪件已经发生的事最有吸引力？',
  '修改已有衣装或车的色调，或选位置拍出了自己主题的画面|自己取得过一辆事先未有的车型或一枚游戏内已知未得奖章，实际补齐了那个缺项|驶入此前没去过的街段，发现了城市另一面|当时精神足且已有活动可接，自己仍沿熟悉路线从容玩过一段，喜欢安稳自主的过程',
  'style_director collector wanderer cozy_resident','10c只指真的取得未有车型或游戏内未得奖章，不含记账；ALT普通街区经过顺序仅route_variant。h有精力及已有活动或未逛完街区，a为真实构图。','gtavev5_manual gtavev5_photo',
  ('没有收藏或改装经历，只回想早期Online街边走动。哪件自己真正做出的事最有吸引力？', '移动角色与普通镜头，截出自己安排的街景构图|给街区穿行定了新的经过顺序，实际试完了一小圈|走进自己没看过的小巷，认识了另一处空间|当时有精力且街区还未逛完，自己仍在熟悉街段从容停留过，喜欢能掌握的节奏', 'style_director route_variant wanderer cozy_resident')),
 Q(11,'真人同伴一起做过的一单','回想与真人同伴实际做过的一次熟悉联系任务：当时全队有可用爆炸物，任务也可只用普通枪械完成。哪件自己实际参与的事最让你记住？',
  '把目标、分路与会合说清，不同人的行动真的接上了|同伴的闲聊、笑料和临场插曲，成了一段共同经历|大家本来有可用爆炸物，却商定整段禁用爆炸武器和手榴弹，只用当时可用普通枪械，确实按限制打过|亲自选择镜头与站位，把这次相处拍成了自己主题的画面',
  'quest_board social_spark play_inventor style_director','11V1泛非常规路线工具改成有可用爆炸物却整段禁用的真实团队限制i，题干说明任务能纯枪完成；q/o只真人。ALT巡游司机称号只是实际驾车路线，r降route_variant。','gtavev5_manual gtavev5_photo',
  ('没有真人合作或联系任务经历，只回想自己单人在Online自由驾车的一小段，哪件真正做过的事最有吸引力？', '对照街道、围墙与转角，实际验证了另一条路怎样绕到目的地|反复练一次路口刹车与转向，自己后来比原先稳定|转向、车身回应与加速连起来时，反馈很直接|自己取过当时可用的车，沿一条非惯常但已可达的街区路线实际开完一圈', 'puzzle_breaker practice_seeker feedback_engine route_variant')),
 Q(12,'长期角色里已经留下的事','回想你已玩过的GTA Online，哪件确实做过的事最能说明当时的投入？',
  '持续培养同一角色的等级或能力，积累在后续仍能保留|把接基础差事、补给与返回的步骤排成可重复运行的一圈|自己换用过当时已经可用的一套枪械、配件或车辆改项配置，实际体验了那套工具|查看NPC联系人已有消息与任务交代，理解了这次事件的来由',
  'growth_keeper mission_preparation_plan try_available_setup story_keeper','12个人基础差事/补给/返回圈和早期取车步骤y降mission_preparation_plan；泛配置比较没有真实组件互补，b降try_available_setup。s是NPC事件文本，g是角色跨活动保留成长。','gtavev5_manual',
  ('只玩过Online最初一小段，没有产业或丰富装备。回想自己真做过的事，最在意哪一件？', '继续驾驶或跑动，让当前角色的基础能力值留下积累|把取车、到目标与返回的先后理顺，形成了自己的一小圈流程|把一处转弯或出入掩体的动作反复练得更稳定|查看过现有手机消息或人物交代，把眼前这件事听得更清楚', 'growth_keeper mission_preparation_plan practice_seeker story_keeper')),
])
for main_slot, online_slot in zip(gtav['slots'], online['slots']):
    for variant in main_slot['variants']:
        variant['modes'] = ['story']
    for variant in online_slot['variants']:
        variant['id'] = main_slot['id'] + '.ONLINE.' + variant['id'].rsplit('.',1)[1]
        variant['modes'] = ['online']
        main_slot['variants'].append(variant)
gtav['modes'] = [
 {'id':'story','label':'故事模式（Michael／Franklin／Trevor）','initial_variants':{}},
 {'id':'online','label':'GTA Online（增强版基础玩法，单人或真人合作）',
  'initial_variants':{s['id']:s['id']+'.ONLINE.V1' for s in gtav['slots']}},
]
PACKS.append(gtav)
