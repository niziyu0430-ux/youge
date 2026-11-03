"""Handwritten PC survival games, private in-progress author draft.





Do not register or build until source research, independent editing and parent


acceptance have completed. No player trial or psychometric validity claim.


"""


from copy import deepcopy


from question_authoring import question as Q, pack, source, SIGNALS








def _extra(scene, text, labels, signals, purpose, sources, boundary, reflection=False):


    words = labels.split('|')


    assigned = [SIGNALS.get(s, s) for s in signals.split()]


    assert len(words) == len(set(words)) == len(assigned) == 4


    return {'key': 'ALT2', 'text': text, 'scene': scene,


            'question_type': 'experience_reflection' if reflection else 'situational_action',


            'source_ids': sources.split(), 'modes': [],


            'options': [{'id': chr(65+i), 'label': label, 'signal': signal}


                        for i, (label, signal) in enumerate(zip(words, assigned))],


            'design_purpose': purpose, 'interpretation_boundary': boundary}








def _paths(identifier, title, game_id, scope, written, notes):


    result = pack(identifier, title, [game_id], scope, written[0][2], notes)


    result['modes'] = []


    for slot in result['slots']:


        slot['variants'] = []


    for mode_id, label, questions in written:


        serialized = pack(identifier, title, [game_id], scope, questions)


        initial = {}


        for dest, src in zip(result['slots'], serialized['slots']):


            for variant in deepcopy(src['variants']):


                suffix = variant['id'].rsplit('.', 1)[1]


                if suffix == 'ALT2':


                    # Keep every authored label and signal coupled, matching the


                    # explicit Q serializer's per-slot rotation for V1/ALT1.


                    offset = (dest['number'] - 1) % 4


                    choices = variant['options']


                    choices = choices[offset:] + choices[:offset]


                    variant['options'] = [choice | {'id': chr(65 + i)}


                                          for i, choice in enumerate(choices)]


                variant['id'] = dest['id'] + '.' + mode_id.upper() + '.' + suffix


                variant['modes'] = [mode_id]


                dest['variants'].append(variant)


                if suffix == 'V1':


                    initial[dest['id']] = variant['id']


        result['modes'].append({'id': mode_id, 'label': label, 'initial_variants': initial})


    return result








SOURCES = [


    source('VAL9L_STORE', 'Iron Gate：英灵神殿当前PC简体中文商店正文',


        'https://store.steampowered.com/app/892970/Valheim/', 'developer_current_pc_store_body',


        '食物影响生命耐力而非饥饿惩罚|新材料解锁配方|不同生态群落|建筑结构与装饰|可单人及真人合作|武器动作与首领推进',


        '2026-10-31实际读官方appdetails简中完整详细介绍。仅原作本体，不借MOD自动取箱、飞行或规划蓝图；支持范围不证明人格。'),


    source('VAL9L_GENERAL', 'Iron Gate：Valheim FAQ玩法与多人正文',


        'https://valheim.com/faq/', 'developer_current_page_mixed_age_faq_body',


        '食物不吃不会饿死但影响生命耐力|窑炉冶炼炉风车等加工|长屋地板墙顶家具|耕作和驯养|船与传送门|共识PvP|真人聊天',


        '2026-10-31直接HTTP200，两段完整正文实际读完。页面混有旧信息；不采用Sandbox不存在、三种船、发型后期独占等旧回答，也不承诺任意物品必可传送或默认有语音。'),


    source('VAL9L_10', 'Iron Gate：1.0正式发布完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1843481262688942',


        'developer_official_news_api_released_body',


        '2026-09-09正式1.0|DeepNorth已实装|所有发型起始可选|现有世界及新物品边界|新库存和建材',


        '2026-10-31已实际读官方SteamNewsAPI完整13094字符；只作当前版本和排除过时回答的依据。题包不要求到DeepNorth、不要求新增首领或器械；内嵌媒体未看。'),


    source('VAL9L_CURRENT', 'Iron Gate：Patch 1.0.21完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847920302230913',


        'developer_official_news_api_current_patch_body',


        '当前1.0.21已发布|成就与部分工具维护|风暴不再吹进屋内的修复',


        '2026-10-31实际读完整4028字符。只按已发布的PC版本，不把稍后跨平台上传时间误作PC未来功能；不将修复项、数值、未完成修复写成问卷门槛。'),


    source('VAL9L_10FAQ', 'Iron Gate：Valheim 1.0 FAQ完整正文',


        'https://valheim.com/support/valheim-1-0-faq/', 'developer_released_version_boundary_body',


        '旧存档可继续|新生态只生成于未探索区域|成就从1.0起记录|Hammer阻止部分成就|无官方MOD支持|单人和最多10人合作',


        '先web仅实际返回部分行，后直接HTTP200完整5938字符解析正文实际读完。价格与下载大小不用于题目；不承诺旧首领成就自动补发，不要求开作弊或改玩家设置。'),


    source('VAL9L_MODIFIERS', 'Iron Gate：Dedicated Servers指南中的原生世界修正项',


        'https://valheim.com/support/a-guide-to-dedicated-servers/', 'developer_actual_world_modifier_reference_body',


        'Normal等预设与Hammer|Resources和Portals独立修正|nobuildcost和nomap|passivemobs与raids',


        '2026-10-31HTTP200全文10271字符实际读完；只取末尾真实预设与修正项，不让玩家配置服务器。Hammer题只用已解锁且当前可放的构件，不推所有配方/装备免费、无结构限制、飞行或地图必开。'),


    source('VAL9L_PLAYER', '原作者Advanced tips for Valheim：亲自建造、交手与装饰经验',


        'https://steamcommunity.com/sharedfiles/filedetails/?id=2418823677', 'community_firsthand_historical_full_guide_body',


        '按时格挡与翻滚|锄头平地当前站位|炉窑投料与收取|物品架装饰与木构件旋转|长屋烟与排烟设计|同名传送门配对|多人自订玩法',


        '2026-10-31HTTP200完整19580字符4段实际读完，不看外链图或视频。旧攻略中Lox不能繁育、夜狼、地形无敌、FPS实例、控制台、备份路径、数值和最优打法全部排除；只采用当前题面给足可用条件的基本动作。个人经验不等于当前开发者承诺。'),


    source('VAL9L_HUGIN', 'Iron Gate：Hugin提示开关已实装的官方说明选段',


        'https://store.steampowered.com/news/posts/?appids=892970&enddate=1680697960&feed=steam_community_announcements',


        'developer_historical_search_returned_selected_body',


        'Hugin乌鸦提示确实存在且可关闭|最早文字不当每位玩家必读',


        '2026-10-31实际读web搜索返回的2023-02-15开发日志主体选段；未通读聚合页、图片或所有历史新闻。只核提示存在及非强制，不采用尚在开发Ashlands或当时未来计划。'),


    source('VAL9L_STONE', '原作者Valheim: A Guide：最早石器时代实玩段落',


        'https://steamcommunity.com/sharedfiles/filedetails/?id=2399948064', 'community_firsthand_historical_selected_body',


        '最早锤子与工作台|屋顶和烟排出|营火上的烹饪架|石斧修理|木盾与弓|建造和材料',


        '2026-10-31HTTP200，实际读Introduction起首6000字符及TheStoneAge、TheStoneAgePt2两节全文7377/4354字符；没有通读12万字符整篇。作者明确未更新HearthAndHome，故不采用食物数值、装备/配方数值、死亡轻惩罚、金属必禁传送、全部首领上限、建议优先级或未来羽毛设施。只取当前可用条件明示的基础工具/烹饪/建筑操作；不看图片。')


]








SOURCES += [


    source('RAFT9L_STORE', 'Redbeet：Raft当前原生PC商店详细介绍',


        'https://store.steampowered.com/app/648800/Raft/', 'developer_current_pc_store_body',


        '钩取漂流物|研究台|扩建木筏|登岛与潜水|航行和故事|作物烹饪动物|单人或真人合作',


        '2026-10-31实际读官方API完整详细介绍，返回英文正文；中文名采用现有库已核通称。当前原生Windows，不挪用主机专用按键或MOD。'),


    source('RAFT9L_CURRENT', 'Redbeet：Raft1.1跨平台进入默认分支',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1826362059932435',


        'developer_official_news_api_current_release_body',


        '2026-03-10默认分支1.1|原生跨平台|完整手柄与游戏内语音|旧分支可选',


        '2026-10-31实际读2236字符完整正文。当前PC不再说跨平台仅Beta；题目不要求跨平台、语音或回退分支。'),


    source('RAFT9L_HOTFIX', 'Redbeet：Raft1.1.01默认分支修复',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1826992588592889',


        'developer_official_news_api_patch_body',


        '新用户PlayFab语音默认关闭|保存名称和社交界面修复',


        '2026-10-31实际读392字符完整正文；不将已实装语音等同默认开启，不以聊天方式推社交人格。'),


    source('RAFT9L_NAV', 'Redbeet Support：How do I navigate完整正文',


        'https://support.redbeetinteractive.com/hc/en-us/articles/360013265259-How-do-I-navigate',


        'developer_navigation_help_body',


        '接收器绿色/蓝色/已选频率目标|地点随航行重生|飘带显示自然漂流方向|引擎与方向盘作用',


        '2026-10-31HTTP200实际读完整短正文。2020文章；只用题面当前可用装置，不用地图固定坐标、无引擎必能逆风、颜色辅助必开或岛屿永不消失等推断。'),


    source('RAFT9L_RESEARCH', 'Redbeet Support：研究台与新配方',


        'https://support.redbeetinteractive.com/hc/en-us/articles/360007305832-How-can-I-learn-new-recipes-and-get-new-items',


        'developer_research_help_body',


        '研究台放材料研究|部分配方需要已找到蓝图|岛屿箱桶可有蓝图',


        '2026-10-31HTTP200完整短正文实际读；不把研究一项材料直接等同所有配方已开，也不承诺每一岛或箱都给蓝图。'),


    source('RAFT9L_CREATIVE', 'Redbeet Support：创意模式木筏保持静止',


        'https://support.redbeetinteractive.com/hc/en-us/articles/360017725239-My-raft-is-not-moving-in-creative-game-mode',


        'developer_native_creative_rule_body',


        '创意木筏故意不移动|静止为大型建造提供性能空间',


        '2026-10-31HTTP200完整短正文实际读；创意题不出海、不靠漂流物来流、不登故事岛、不假造引擎能推动。不是玩家卡住/故障情境。'),


    source('RAFT9L_SAILS', 'Redbeet Support：帆的数量与速度',


        'https://support.redbeetinteractive.com/hc/en-us/articles/360007241132-Will-more-than-one-sail-make-my-raft-go-faster',


        'developer_sailing_rule_body',


        '多放帆不叠加航速|划桨与引擎是其他操纵方式',


        '2026-10-31HTTP200完整短正文实际读。题目不许诺堆帆加速，不采用任何固定速度。'),


    source('RAFT9L_ENGINES', 'Redbeet Support：引擎与筏体关系的历史说明',


        'https://support.redbeetinteractive.com/hc/en-us/articles/360013792659-Do-multiple-engines-make-the-raft-faster',


        'developer_historical_engine_help_body',


        '引擎作用与筏体规模相关|多引擎非无限叠速度',


        '2026-10-31HTTP200完整2462字符解析正文实际读；原文2020，不采用其承载数、速度数、慢速区间、六引擎之外规律等固定公式。内嵌图未看，题目不用数值解题。'),


    source('RAFT9L_FINAL', 'Redbeet：VERSION1.0 The Final Chapter完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/6214419350719481990',


        'developer_official_news_api_released_full_body',


        '故事笔记重写与Notebook回听|回收机垃圾块与贸易币不同来源|交易站和稀有鱼|榨汁机增益|横柱和可伸缩旋转细节木板|部分装置需电',


        '2026-10-31实际读完整15581字符3段；只用已发布功能，不强制终章地点、特殊装备或交易等级。内嵌媒体未看；配方、产出与价格不记固定数。'),


    source('RAFT9L_RENOVATION', 'Redbeet：Renovation Update完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/4056035920069792385',


        'developer_official_news_api_released_building_full_body',


        '新的建筑形状和装饰包|墙两面分别上色|图案双色与颜色预览|取色和构件选取|拆除高亮|引擎控制|部分建筑可镜像',


        '2026-10-31实际读完整10191字符2段。原文提未来Chapter3为2021历史语境，现终章已另证实装；只采用当前可用涂装/建造工具，不把所有物件都可双色或免支撑当通则。'),


    source('RAFT9L_PLAYER', '原作者How to Raft：最早钩取、料理、建造与创意经历',


        'https://steamcommunity.com/sharedfiles/filedetails/?id=2840337010', 'community_firsthand_original_guide_full_body',


        '蓄力抛钩与收线|淡水杯和净水器|鱼竿与简易烤架|研究材料与配方|装饰包和收纳|创意免费物品与自由观察视角|真人合作',


        '2026-10-31HTTP200完整17932字符3段实际读。不采用其错误/过时的净水器配方、种植格数、动物会饿死、引擎吃电池、死亡一律掉光、鲨鱼诱饵固定分钟、岛屿必有店或漂流物必指向岛。推荐打法与效率意见不当唯一答案；只采用交叉官方已证的基本动作和当前界面确有的创意工具。')


]





SOURCES += [


    source('GH9L_STORE', 'Creepy Jar：绿色地狱当前PC商店完整中文正文',


        'https://store.steampowered.com/app/815370/Green_Hell/', 'developer_current_pc_store_body',


        '身体检查与生存制作|本体Mia故事和无尽生存|免费SoA前传|木竹泥建造|当前装饰与养殖|可单人或真人合作',


        '2026-10-31实际读appdetails完整中文详细介绍。本体815370，不是GreenHellVR；不把宣传游玩小时、内容数或现实生存说法作玩家考核。'),


    source('GH9L_CURRENT', 'Creepy Jar：2.9.5已发布维护完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1823825466493672',


        'developer_official_news_api_current_patch_body',


        '当前PC2.9.5|SteamDeck文字和控制维护',


        '2026-10-31实际读完整819字符；不从补丁未提的机制推不存在，也不强制手柄或特定按键。'),


    source('GH9L_BUILD', 'Creepy Jar：Building Update正式发布全文',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5035621474425830268',


        'developer_official_news_api_released_building_body',


        '木竹墙顶和三角框|树上/水上建造|爬绳与浮动框|Notebook分类|清理大棕榈等地面物',


        '2026-10-31实际读完整4001字符。只用已开放且题面已有材料构件；不假定随时有最大树或把三层水屋当所有建筑上限。'),


    source('GH9L_TRANSPORT', 'Creepy Jar：Storage & Transportation正式发布全文',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5141475722341803976',


        'developer_official_news_api_released_transport_body',


        '雪橇可放不同重物|升降机运输重料|普通和悬挂架|篮与木竹通用架|可选快速拾取动画|单次实际取放',


        '2026-10-31实际读完整10325字符。武器与建材不能都塞普通小物架；不把木竹架材料对应当旧限制，不将关闭拾取动画推身体条件。'),


    source('GH9L_DECOR', 'Creepy Jar：免费更新21 Decorations全文',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/6240387642472530526',


        'developer_official_news_api_released_decoration_body',


        '画刷与颜料|工作台制作家具|盔甲箭架|火把架仍需维护|已造装饰可移位|最终内容更新',


        '2026-10-31实际读完整6746字符；不将最后内容更新等同停止维护。画刷、颜料、家具只在当前已取得前提下用；无付费装饰必需。'),


    source('GH9L_ANIMALS', 'Creepy Jar：Animal Husbandry正式发布全文',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/4587497456695844129',


        'developer_official_news_api_released_husbandry_body',


        '水豚貘猯圈养|吹管麻醉与动物圈|喂水喂食和清理|信任后可抚摸|蜂箱与蜂蜜',


        '2026-10-31实际读完整2442字符。初版三种不是当前全部可养动物；不采用精确饲料量、信任速度、成功率或无条件抓幼崽。'),


    source('GH9L_ANTEATER', 'Creepy Jar：更新20 Anteater完整正文',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5762994032387187553',


        'developer_official_news_api_released_husbandry_extension_body',


        '食蚁兽和两类犰狳可养|堆肥器及昆虫饲料槽|可拆蚁丘会另处生成|鹦鹉巢和羽毛蛋',


        '2026-10-31实际读完整5706字符；不采用新物品一定已解锁、不设饲料或产出固定数字。只与当前About共同核对养殖边界。'),


    source('GH9L_FLAME', 'Creepy Jar：更新19 Flamekeeper完整正文',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5510784213116250902',


        'developer_official_news_api_released_optional_combat_activity_body',


        'Waraha村中永恒火图腾|收材料启仪式|守护火焰抵御波次|合作可选|特殊挑战奖励',


        '2026-10-31实际读完整3443字符。作为普通世界可选活动，不与主菜单七项Challenges或VR挑战混名；题面需活动已可开且有实际波次，不预告固定敌人、必胜或奖励已拥有。'),


    source('GH9L_FLAME_BOUNDARY', 'Creepy Jar：2.7.1正式修复中的仪式模式边界',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5589599109279911865',


        'developer_official_news_api_released_mode_boundary_body',


        '本体Story不能制作Ritual of Flame Herbs|永恒火焰合作界面与重载状态|仪式属可存档世界活动而非七项限时挑战',


        '2026-10-31C独立实读后，root另从自己的官方100篇缓存取出完整正文并实际读完。仅按原文模式边界限定活动，不把Story的低理智敌人与仪式混同；不以修复内容证明某个未点名模式的所有可用性。'),


    source('GH9L_SOA2', 'Creepy Jar：SoA Part2正式发布完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/4056035920073577164',


        'developer_official_news_api_released_prequel_body',


        '前传部落与新传奇活动|与正篇不同地图区域|hard已开放|SoA和Challenges不同修复项',


        '2026-10-31实际读完整1683字符；不采用仍在公测的旧先行公告或将SoA地图照搬正篇，未定固定敌人数量。'),


    source('GH9L_LAUNCH', 'Creepy Jar：Green Hell 1.0发布完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/2413288973188808850',


        'developer_official_news_api_released_original_mode_body',


        '本体故事已发布|各基础难度|Custom可调设置|真实生存机制',


        '2026-10-31从C独立历史缓存另存root缓存后实际读完整3867字符。不把2019版本选项当当前完整菜单；只确认Custom并非必有同样营养/危险，题面另给当前已可用条件。'),


    source('GH9L_SOA1', 'Creepy Jar：Spirits of Amazonia Part1正式发布完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/4050393736338918307',


        'developer_official_news_api_released_prequel_initial_body',


        '独立前传故事|部落信任|传奇与新区域|手表坐标南西标记',


        '2026-10-31实际读完整2777字符。初版hard暂不可用已被Part2后续公告替代，不沿用旧限制；不假定每人已有地图、不编地图自动玩家标记。'),


    source('GH9L_NOTEBOOK', 'Creepy Jar：2.5.2完整修复中的Notebook和SoA存档边界',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5211283418277590805',


        'developer_official_news_api_released_notebook_boundary_body',


        'Survival Guide解锁Notebook|SoA修船后Save and Quit修复',


        '2026-10-31实际读完整1040字符。只确认Notebook并非无需经历便当然已开，题面均明确当前可用；修复不是保证任意旧存档无问题。'),


    source('GH9L_SOA_UI', 'Green Hell社区Wiki：前传信任页、猎人检查和渔民蓝图的定向返回正文',


        'https://greenhell.fandom.com/wiki/Spirits_of_Amazonia_Game_Mode',


        'community_wiki_targeted_search_returned_sections',


        '见并交谈村长后才可查看信任页|传奇任务需先读齐该传奇线索|猎人须实际检查状态而非显示精确材料单|渔民旁蓝图显示所需工具',


        '2026-10-31root实际读两次定向web返回的GameMode、InjuredHunters和HelpFishermen段落；不是通读三篇全页或实际运行客户端。原作者SoA实玩指南已独立全文读。第二次返回完整存soa-ui-targeted-second-search.json；仅使用上述限定段落，不采用坐标、数量、命中、治疗配方或控制台，也不将Wiki标题Official当开发者官方正文。'),


    source('GH9L_SOA3', 'Creepy Jar：SoA Part3已发布全文与官方介绍',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/4258723269526706288',


        'developer_official_news_api_released_prequel_finale_body',


        '免费前传三部已完整|第三捕鱼部落|三类仪式场|传奇与制陶|独立于正篇的Jake经历',


        '2026-10-31实际读完整1472字符，另读官方greenhell-game.com/656/正文6018字符；后者3月9日是发布前介绍，采用3月29日已实装公告确认。未看预告片、外链图。'),


    source('GH9L_SOA_PLAYER', '原作者Green Hell The Spirits of Amazonia Achievement Guide',


        'https://steamcommunity.com/sharedfiles/filedetails/?id=2872280445', 'community_firsthand_prequel_guide_full_body',


        '村长信任与传奇石画线索|救猎人带孩子回村|清污水和重建图腾|渔民需求|三种不同仪式|SoA船上无线电',


        '2026-10-31HTTP200完整6844字符两段实际读。作者Habbacu某些需求标问号、最终Yabahuaca仪式仍MoreInfoSoon，均不作为已核细节；固定坐标、信任/数量、成就全达成及外链攻略未采用。'),


    source('GH9L_CHALLENGE_PLAYER', 'Kasiornis亲自尝试七项挑战：I am not afraid of any work',


        'https://steamcommunity.com/sharedfiles/filedetails/?id=2189945462', 'community_firsthand_historical_challenge_full_body',


        'Campfire/Raft/MightyCamp/Hunter/Fisherman/Radio/Blacksmith各有预设目标|本局材料与路线|计时挑战|冶炼与建造不同循环',


        '2026-10-31HTTP200完整19075字符四段实际读。原稿2020，固定刷新、坐标、数量、最佳路线、一击击杀、蛇伤处理、蛙肉汤、存档/计时可忽略建议不当当前保证；不采用其人身语气。不声称亲自运行挑战。')


]





SOURCES += [


    source('PZ9L_STORE', 'The Indie Stone：Project Zomboid当前PC商店正文',


        'https://store.steampowered.com/app/108600/Project_Zomboid/', 'developer_current_pc_store_body',


        'Knox隔离区探索|搜刮与防御|饥渴情绪和疾病|制作烹饪耕作捕鱼|角色技能随实际活动发展|原生在线和分屏',


        '2026-10-31实际读完整appdetails英文详细介绍，当前Apocalypse/Outbreak/Rising/Extinction已在正文。PlannedFeatures中的Kate/Baldspot、深入NPC生存者和Steam成就均未来，不作为已实装题面；不用MOD、必中、感染治愈或不死保证。'),


    source('PZ9L_42', 'The Indie Stone：Build42.20官方功能总览完整正文',


        'https://projectzomboid.com/blog/features-overview-build-42-20/', 'developer_current_stable_feature_overview_body',


        '地下室和新地点|动物照料和追踪|季节作物|交互捕鱼和噪声|可选配方输入和工作站|武器头柄独立状态|服装和3D摆放|环境文字叙事|原生多人',


        '2026-10-31HTTP200完整17638字符三段实际读完，并在进入PZ写题前再次实际读完。正文是42.20功能，页头当前稳定42.21、预发布42.22；不借预发布新功能，不固定地图面积、楼层、作物月份或数值。概述含41已有3D摆放等共通功能，不能把标题里的new直接当41不存在。'),


    source('PZ9L_CURRENT', 'The Indie Stone：42.21稳定版完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1844751498231307',


        'developer_official_news_api_current_stable_body',


        '42.21已到稳定分支|区别Unstable/PreRelease|现有42存档边界',


        '2026-10-31实际读完整3957字符。只确认当前已稳定，不让用户安装预发布、改MOD或迁移存档来答题；不推所有旧存档无问题。'),


    source('PZ9L_LEGACY', 'The Indie Stone：41.78.21 legacy与42维护完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1842212951296601',


        'developer_official_news_api_legacy_availability_body',


        '41.78.21 Legacy仍有官方分支|42.20.4与42.19.2分开维护',


        '2026-10-31实际读完整1121字符并复读。安全修复细节不写进产品题目；不让玩家执行外部代码，不承诺41/42人物、地图或MOD兼容。'),


    source('PZ9L_41', 'The Indie Stone：Build41正式发布完整公告',


        'https://projectzomboid.com/blog/news/2021/12/project-zomboid-build-41-released/',


        'developer_historical_released_feature_body',


        '41时代Apocalypse/Survivor/Builder|潜行战斗和衣物防护|地图|环境死亡场景叙事|衣物修补锻炼VHS|3D物品与人台|原生联机',


        '2026-10-31HTTP200完整11043字符三段实际读完；2021当时稳定不等于当前默认41，当前分支另证。41已有3D摆物不误排除；不往41加入42动物、季节耕作、交互捕鱼、武器头柄或新工作站；旧宣传稳定/无丢车不当保证。'),


    source('PZ9L_GAME', 'The Indie Stone：The Game当前功能与计划分栏',


        'https://projectzomboid.com/blog/the-game/', 'developer_current_feature_and_planned_boundary_body',


        '当前生存搜刮建筑防御|技能随游戏发展|原生在线和分屏|NPC与剧情故事在Planned分栏',


        '2026-10-31HTTP200完整5878字符实际读完。犬、NPC生存者和Kate/Baldspot均计划，不写已实装。另下载并实际读ReturningtoPZ页面5318字符，只是早期购者找回密钥说明，不用作玩法来源。')


]





SOURCES += [


    source('SEV9L_STORE', 'The Fun Pimps：七日杀当前原生PC商店完整介绍',


        'https://store.steampowered.com/app/251570/7_Days_to_Die/', 'developer_current_pc_store_body',


        '采集制作搜刮采矿|建筑形状涂装与结构倒塌|电力陷阱炮塔|技能点与书籍|贸易商NPC任务|载具耕种|真人合作或竞争|原生创建和自定义角色外观',


        '2026-10-31实际读完整appdetails简中正文并在进入本作写题前复读。不采用宣传物品数、配方数、楼面积、敌人数或销量；不将所有Sandbox世界都推为有血月、地图、任务、修理和同样解锁。'),


    source('SEV9L_CURRENT', 'The Fun Pimps：V3.4.0 Stable-b9完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1847286114045870',


        'developer_official_news_api_current_patch_body',


        '3.4Stable-b9|背包和容器搜索筛选|锁定栏位修复|真人任务分享修复|营火直接食用已知问题',


        '2026-10-31完整3371字符已读并复读。营火食物题只用已取进背包且当前可用物品，不假装可直接在营火食用；不拿修复当无条件数据兼容或客户端实测保证。'),


    source('SEV9L_33', 'The Fun Pimps：V3.3.0 Stable完整公告',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1845383656394144',


        'developer_official_news_api_released_inventory_editor_body',


        '可装备背包扩容|部分负重格|PrefabEditor原生多工具栏页仍在维护|营火物品先转背包',


        '2026-10-31完整3281字符已读并复读。只当前角色实际能用的背包/工具栏，不固定格数、品质或容量；官方确认编辑器存在，不据此宣称旧攻略每个按钮和快捷键当前都相同。'),


    source('SEV9L_30', 'The Fun Pimps：Dead Hot Summer3.0完整发布说明',


        'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1835236783562323',


        'developer_official_news_api_feature_release_body',


        'Sandbox预设和可关闭机制|Magnitude与CombineStation|维修和衰退设置|编辑器SignTech文本形状颜色层|新POI|原生准星设置',


        '2026-10-31完整19525字符4段已实际读，写题前复读01/02及03/04定向设置段。最初标题EXP，已另读1836506165560649完整415字符确认3.0Stable已发布；当前3.4另证。不把AlmostCreative名当CreativeMenu全物品权限，不假定地图、任务、修理、最高科技或血月必开；不采用固定增益、品质上限、代码/服务器指令或付费外观必须。'),


    source('SEV9L_CREATIVE', '7DaysWiki：CreativeMenu当前定向返回正文',


        'https://7daystodie.wiki.gg/wiki/Creative_Menu', 'community_wiki_targeted_search_returned_body',


        '原生物品构件取用菜单|需要单独启用的世界设置或权限|选择当前显示物品与类别',


        '2026-10-31实际读搜索返回的开头正文，未通读全页或运行客户端；社区Wiki标题Official不当开发者正文。只题面当前已启用且菜单确实显示的普通物件，不推飞行、无敌、无结构规则、全开发者物品或AlmostCreative自动开菜单。避开旧网格大小、按键、XML和成就承诺。'),


    source('SEV9L_PREFAB', 'Naz：PrefabEditorOverview原作者实作说明选段',


        'https://7dac.net/prefab-editor-overview-guide/', 'community_firsthand_historical_browser_returned_sections',


        '编辑器选区复制旋转镜像|单独保存prefab|另开空世界Playtest|当前预览时间|本地PrefabBrowser与工具栏',


        '2026-10-31直接HTTP412保留失败，另web实际读返回27-203行，不声称全325行或图片视频。2020/2022原作者历史说明，3.3官方另证编辑器存在；不固定当前按键、路径、网格、全操作可撤销、预览进度自动保存、旧灯光/性能或远景网格覆盖规则。所有细节仍须题面当前确实可用并经独立审阅。'),


    source('SEV9L_PREFAB_START', 'Naz：PrefabEditorGettingStarted原作者实作选段',


        'https://7dac.net/prefab-editor-getting-started-basics/', 'community_firsthand_historical_browser_returned_sections',


        '创建命名保存单个prefab|当前构件菜单|选区复制|sleeper位置与volume分开|门与触发器|单独试玩',


        '2026-10-31直接HTTP412保留失败，另web实际读30-196行，不声称全331行或看图片视频。排除旧尺寸、敌人数量、键位、路径、Trader图标、自动进RWG、EAC或服务器步骤；当前3.4精确面板未实测，不把另一个未复核3.4的ModdingWiki当终审。')


]





VAL_SURVIVAL = [


    Q(1, '食物空位与草甸出门前',


        '在草甸长屋准备出门，食物栏还有空位，现有熟肉、莓果和蘑菇可选；木斧与熟路也可用。你先怎样投入这一段？',


        '比较两种可吃的食物组合，带一组出门检验生命、耐力与挥斧的配合|留在熟路反复练挥斧与停手的节奏，专门把耐力控制练熟|只先看当前食物剩余时间与身体状态，再决定出门安排|先在熟悉火边吃点东西、慢慢收拾，享受回家的安稳感',


        'b t survival_status_review h',


        '食物与已有动作的具体取舍：组合效用b、刻意练习t、当前状态核对0、熟悉停留h。食物不是饥饿惩罚；不要求最优组合、满血或任何成功。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_PLAYER',


        ('只经历过最早拾木石也可答：手边已有木石、能做石斧，附近还有未走过的草甸与熟悉火堆。你想先做什么？',


         '去还没踏过的草甸看看那边有什么，暂不为指定产物而走|在一棵可砍的树旁反复练挥斧与退步，专门熟悉动作节奏|先核对已带木石和当前耐力，再决定这趟活动|回熟悉火堆边拾几块近处木石，享受这段已经熟悉的日常',


         'w t survival_status_review h')),


    Q(2, '窑炉、煤与原矿的周转',


        '窑炉与冶炼炉已能用，现有木材、煤、原矿与空箱；你还没想好这段时间怎样安排加工。更愿意先做哪件事？',


        '把木材补给、煤产出、投矿与成品存放连成几轮周转，持续调整让供给接得上|怀疑停产是煤跟不上，保持投矿方式不变，只补煤检验自己的猜想|先看炉内已有燃料、原矿和箱中成品，核对当前情况|排清这一次取木、投料和收成品的先后，亲手按顺序做一轮',


        'y p production_state_review physical_tool_action_sequence',


        '连续供给与产出的安排才是y；p明确是本人尚未确认原因的单项试验。查看已有状态和单次工具流程均0，不伪造自动物流或因果答案。',


        'VAL9L_GENERAL VAL9L_PLAYER',


        ('尚未冶炼，只有最早的木石制作经历也可答：已会做的石斧当前材料够，火堆与木料箱可用。你先怎样安排？',


         '排清从箱取石、制作石斧和收回余料的顺序，再亲手做一轮|先看手头材料及已开放配方，核对这一把能否制作|实际做出这一把已能制作的石斧，体验它怎样出现在手里|用斧头敲一段木头，留意按下动作与木块掉落紧接着发生的感觉',


         'physical_tool_action_sequence compare_production_options available_operation_trial f')),


    Q(3, '长屋伸出去的屋顶',


        '一段木屋顶伸出去后放不稳，你还不确定是哪处支撑影响它；锤子与现有木构件可用。你更想先怎样处理？',


        '猜是悬出太远，保留其他连接，只加一处已有立柱，观察这次是否改变|把屋顶轮廓改成自己喜欢的长屋样子，优先表达这一栋的风格|先排清拆哪块、加哪段连接、再放屋顶的步骤，按这一轮流程试|只移动一块当前可调整的木构件，亲手看改动后的样子',


        'p a construction_action_plan creative_edit_trial',


        'p是未核实支撑关系的可失败单项测试；a要有本人想表达的风格。施工先后和一项编辑不自动等于机制研究、练习或发明。',


        'VAL9L_STORE VAL9L_PLAYER',


        ('还没造长屋也可答：最早的工作台已提示需要屋顶，你已有锤子、木材与可放的茅草顶。你先做什么？',


         '按照提示补上当前能放的屋顶，重点是把这项眼前要求推进|先核对已有建筑操作说明，再继续搭这片顶|把这一小处做成自己选定的屋形，表达想让它呈现的感觉|排清先放连接再补顶的顺序，照这一轮施工安排动手',


         'stated_objective_progress tool_reference_first a construction_action_plan')),


    Q(4, '船首之外的陌生海岸',


        '当前已在一艘能操纵的船上，海况与补给允许短途活动；一边是熟悉停靠点，一边是没去过的海岸。你想先怎样玩？',


        '驶近没去过的海岸，想亲眼知道那边有什么|亲手拉帆、转向，留意输入之后船身和海面反应的直接感觉|只看当前可用地图上的位置与已有标记，再决定这段往哪走|先排清已有食物、停靠点和返程的先后，再按这趟安排行动',


        'w f navigation_information_review mission_preparation_plan',


        '陌生海岸的发现w与驾驶反馈f分开；读已开放地图0与本次资源/目的地安排0，不假定无地图预设也有地图或任意逆风皆可达。',


        'VAL9L_GENERAL VAL9L_MODIFIERS',


        ('没有地图、还没航船也可答：草甸里有一条已经能走、但你没去过的林缘，身后是熟悉营火。你先怎样继续？',


         '走近陌生林缘，想看看地形转过去会露出什么|在可走的小坡上跑跳，留意步伐、落地与环境回应的感觉|先核对带着的食物与当前体力，再决定这段活动|回熟悉火边走一圈，让自己待在已经安心的地方',


         'w f survival_status_review h')),


    Q(5, '已有小盾的格挡时点',


        '眼前是一只已能接近的普通灰矮人；当前小盾、单手武器与耐力可用，还没有进入必须获胜的首领战。你想把这次交手用在哪里？',


        '反复练看起手再举盾的时点，专门把格挡手感练熟|比较手头两组确实可换的盾与武器，实际检验组合效果|亲手打一轮，享受举盾、命中与敌人反应接连发生的反馈|先排清举盾、出手与停手恢复耐力的循环，再照着尝试',


        't b f combat_resource_cycle',


        't必须有专门反复练时点的目的；b必须比较现有两种组合并检验效用，f是即时反馈。只理本轮资源循环0；不预告格挡成功、固定伤害或无敌帧数。',


        'VAL9L_STORE VAL9L_PLAYER',


        ('没有小盾或不想交战可换这个情境：石斧当前可用，眼前有一棵可以砍的树，附近有停手恢复耐力的空间。你先怎样投入？',


         '反复练砍一下再退步的时点，专门让这一套动作更熟|亲手挥斧，留意砍击声音、树身晃动与输入相连的反馈|先排清挥斧、退到旁边恢复与再靠近的先后，再照安排砍这一轮|只先看当前耐力与已带补给，再决定怎样动手',


         't f tool_operation_plan survival_status_review')),


    Q(6, '已经重生且仍在的墓碑',


        '这一次你已重生，旧装备确实还留在当前可返回的墓碑里；眼前有基础食物与备用工具。你更想怎样继续？',


        '先回去取这一份仍可取回的旧物，把当前最惦记的事处理完|排清备用食物、可走路段与接近墓碑的先后，按这趟安排返回|暂时改去一处可达但没走过的地方，先看看新的东西|回熟悉长屋慢慢整理，让这次返回家里的停留先安定下来',


        'runes_retrieve_first mission_preparation_plan w h',


        '只用于已重生且墓碑实存的当次经历；不向Hardcore永久死亡、全物品销毁或未死过的玩家保证可复活取回。恢复物品本身0，不计长期养成或竞争。',


        'VAL9L_MODIFIERS VAL9L_PLAYER VAL9L_STONE',


        ('没有这类死亡经历可答：最早一把石斧耐久已低，当前已有能修它的工作台，附近木材也够。你先怎样继续？',


         '在当前可用工作台把这把斧头修好，先接回惦记的这段工作|排清取出石斧、在台前修好和收回手边工具的先后，再照顺序做|修好后去没走过的草甸边看看，想知道那里还有什么|留在熟悉营火与小屋之间慢慢收整，享受已经熟悉的地方',


         'available_operation_trial physical_tool_action_sequence w h')),


    Q(7, '已拿到的不同战利品',


        '你已有几种实际拾到的战利品和一个能用的物品架；不要求再打任何首领。眼前这段空闲，你更愿意做什么？',


        '把已见过的种类列成自己的收藏目标，想为还缺的那一类继续找|从现有战利品里选一件配合梁柱和桌面，做出自己想表达的长屋风格|只把已经拿到的物品与地点补记下来，保留这段经历的记录|按这一存档里给维京人的性格设定，选择他会郑重摆放的那一件',


        'c a game_recording r',


        'c明确在意种类缺口而非掉落强弱；a是展示风格，r由本人角色设定决定行动，不从战利品外观推现实身份。补记已有物品0，不凭空造官方全藏品列表。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_PLAYER',


        ('没有物品架也可答：刚拾过木石、莓果与第一批材料，当前有一个能放物品的箱子。你更愿意先怎样收整？',


         '把已经见过的材料种类当作自己的收藏，惦记还没见到的那一类|只调整这批已有物品的存放，再继续自己的活动|补记这几件已经拿到的东西和发现地点，留下一份记录|按自己给这个维京人设定的习惯，只留下他此刻愿意带走的物件',


         'c item_handling_action game_recording r')),


    Q(8, '读完一段可达符文石',


        '一块已经可达的符文石刚读完，附近没有必须立刻打的仗。文字和眼前地形都在这里；你更愿意把下一段时间给什么？',


        '再读一遍，把其中的人物经历或世界线索与之前看过的内容接起来|照自己给这名维京人设定的信念，决定他读完后要回长屋还是继续走|不为线索答案而走，去看看符文石后还没踏过的林子|只为这段已经读到的文字与地点补上自己的记录',


        's r w game_recording',


        '故事s关注叙事联系；角色r要本人以身份作行动决定，符文石没有被编成真正分支任务。未知地形w与补记0分别解释，不强迫玩家认同某个叙事解读。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_HUGIN',


        ('还没留意符文石也可答：最初见过乌鸦提示后，你正站在已经能走动的草甸里。接下来的可选时间，想怎样过？',


         '再看已出现的文字，想理解这个维京人为何来到这里以及正在经历什么|按自己给这名维京人设定的处事方式，决定先搭住所还是出发|往还没走过的小坡后面看看，想知道眼前之外有什么|先核对已经出现的玩法说明，再继续自己的实际尝试',


         's r w game_reference_first')),


    Q(9, '真实经营过的田地或圈养',


        '回想你实际照料过的菜地或圈养：在那些已经玩过的时段里，哪种投入最贴近你愿意保留的体验？',


        '持续回到同一片田地或同一群动物身边，看前几次投入慢慢留下变化|把播种、留种、食物产出和下一轮补给衔接起来，多轮调整它们的供给|在自己已见过的作物或动物种类中留意缺口，想把种类慢慢补齐|只是先查看当时实际可见的作物或动物状态，再决定那轮怎样处理',


        'g y c production_state_review',


        '真实过去，g看同一对象持续积累，y看多轮投入产出衔接，c看种类缺口；普通查看0。不要求高星繁育成功、指定作物产量或到过某个生物群落。',


        'VAL9L_GENERAL VAL9L_PLAYER',


        ('没有耕作或圈养经历，回想真实最早的草甸活动：已有火堆、小屋或第一批工具时，你做过且愿意保留的投入是什么？',


         '多次回到同一间小屋逐步添东西，喜欢看早先投入一直留在这个住所里|亲手拾木、挥斧或放下构件，喜欢动作之后马上发生的回应|留意已见材料的种类，想慢慢收进还没拿过的那一类|只是按当时现有物品，实际调整了一轮携带与存放',


         'g f c item_handling_action')),


    Q(10, '真实搭过的小屋里',


        '回想一间你真实搭过或改过的小屋：哪种已经做过的动作，更接近你愿意再次经历的那种投入？',


        '反复调整梁柱、屋顶和摆设，直到它表达了自己想要的长屋气质|明明有别处可去，还是回到熟悉火边、床旁慢慢待一阵|按自己赋予维京人的经历与习惯，决定屋内要留下哪些物件|只是为已经搭过的建筑与连接补记过程，保留这一轮建设记录',


        'a h r construction_process_recording',


        '反思真实已发生的建造/停留，风格表达、熟悉栖居与角色一致性各有明确动机；记录0。不从装修审美、床的朝向或角色身体推现实人格。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_PLAYER',


        ('若只造过最简单的火堆与几块木构件，回想当时实际发生过的投入：哪一项最贴近你愿意保留的部分？',


         '把当前几块构件摆成自己想表达的样子，即使只是很小一角|在已经熟悉的火光附近慢慢走动，喜欢那段安定的停留|照自己对这名维京人的设定，选一个他此刻会愿意留下来的位置|只把已经放过的构件与步骤补记下来，保留这次建设记录',


         'a h r construction_process_recording')),


    Q(11, '已经用过的装备与熟路',


        '回想一次真实用已有武器或工具活动的经历：哪种已经做过的投入，最接近你愿意留住的部分？',


        '围绕同一套已拥有装备安排过持续升级，喜欢前几次投入在它上面留下积累|专门重复过一小段挥砍、举盾或退步，目的就是把动作练得更熟|比较过自己当时确实拥有的两组搭配，再实际检验它们带来的不同效果|只是先比较当时可选的现有配置，再决定下一步怎么安排',


        'g t b compare_available_setup',


        '真实过去；长期积累g与刻意动作训练t分开，比较并检验组合效用才b，单纯浏览配置0。无装备高低、效率、技术水平或特定升级数值要求。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_PLAYER VAL9L_STONE',


        ('尚未升级或换配装，可以回想真实在最早烹饪架上放过肉的经历：哪种已经做过的投入最接近你愿意保留的体验？',


         '专门重复观察烹饪变化与取下时点，想把亲手料理这件事练熟|亲手挂肉、取肉，喜欢火声、食物变化与输入接连发生的反馈|待在熟悉营火旁慢慢等这一轮料理，喜欢这段安稳的停留|只是先查看当时架上与手边实际已有的食物状态，再决定那轮怎样处理',


         't f h production_state_review')),


    Q(12, '真实同游时的共同安排',


        '回想一次确实有其他真人同玩的时段：长屋未收尾，有人想继续搭建，有人想出门。哪种你实际做过的动作最贴近愿意保留的体验？',


        '先谈清这轮共同想完成什么，商量谁留家、谁出门以及何时再集合|先陪同伴走走、聊眼前的事，喜欢一起待在这个世界里的陪伴|和愿意参加的人约定一个临时自订规则，例如这一轮只用木构件搭一间小屋|只为自己已经参与的那段建设补记过程，保留发生过的步骤',


        'q o i construction_process_recording',


        '仅真实真人经历；q是协商共同目标与分工，o是陪伴，i是明确自订且参与者同意的玩法，不当官方模式。无真人用单人ALT，不以NPC或想象中的人补证。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_PLAYER',


        ('没有联机经历就回想真实单人玩过的草甸：哪种已经做过的动作，最贴近你愿意留住的部分？',


         '从一条没走过的林缘绕出去，想亲自看看那边是什么|给这一轮加一个自己的小规则，例如只在河边拾取，再按这个规则玩|回到熟悉火堆与小屋间走走，享受一个人安稳停留的感觉|只为已经拿到的物品和已体验地点补上记录',


         'w i h game_recording')),


]





VAL_SURVIVAL[0]['variants'].append({


    'key': 'ALT2',


    'text': '还没经历食物搭配或反复练动作，也可答草甸里的一处小废屋：入口能走到，锤子、够用木料与此处可用工作台都具备，可修整已开放木构件。你先怎样投入？',


    'scene': '草甸已可进入的小废屋',


    'question_type': 'situational_action',


    'source_ids': ['VAL9L_STORE', 'VAL9L_GENERAL', 'VAL9L_PLAYER', 'VAL9L_STONE'],


    'modes': [],


    'options': [


        {'id': 'A', 'label': '走进还没看过的小废屋，想亲眼知道里面和屋后有什么', 'signal': 'wanderer'},


        {'id': 'B', 'label': '用当前能修整的木构件布置这一角，让它表达自己选定的住处风格', 'signal': 'style_director'},


        {'id': 'C', 'label': '沿用我给他设定的流浪者身份，收起修屋工具，继续走这段路', 'signal': 'role_player'},


        {'id': 'D', 'label': '先查看已经能走到的入口与屋内现场，再决定这一段怎样继续', 'signal': 'scene_inspection'},


    ],


    'design_purpose': '两个原情境均未体验后提供不同前提的真实早期场景。未知发现w、风格表达a、角色设定影响行动r分别明确；仅查看可达入口和现场0。',


    'interpretation_boundary': '仅当前确实可进入和可修整的已有木废屋；不假定每一废屋都安全、必有宝物、可招NPC或是剧情任务。换题本身不计分，只有实际四选一进入证据；本稿仍待完整逐项编辑验收。',


})





VAL_SURVIVAL[1]['variants'].append(_extra(


    '只有随身材料与小木箱的一轮收整',


    '还没做过冶炼或石斧制作，也可答最早的收整：已拾到木石，当前小木箱可用，眼前还有能取的小树枝。你先怎样处理？',


    '先查看眼前实际已有的木石与存量，核对这一轮的物料|实际把一部分已有木石放入箱中，调整随身携带|亲手拾起树枝，留意输入之后物件进入手里的即时回应|给已拿到的材料和发现位置补上一份记录',


    'material_stock_review item_handling_action f game_recording',


    '在未经历两种制作情境时用基础取放；物料查看、实际存放和补记均精确0，只有明确即时反馈f。',


    'VAL9L_STORE VAL9L_STONE',


    '箱子当前确实可用，不假定已造冶炼设备或全新工具；普通存放不当长期养成，已有材料记录不直接当收藏齐全。'))


VAL_SURVIVAL[2]['variants'].append(_extra(


    '第一处木地板与转向',


    '还没试屋顶或修工作台，也可答最初铺地板：锤子、够用木料与已开放地板当前可用，草甸上有可放的位置。你先怎样玩？',


    '把这几块排成自己想表达的小屋轮廓|亲手转向并放下一块地板，喜欢构件随输入立刻出现的反馈|给这一轮定只沿一条折线放地板的小规则，再照规则尝试|排清先选位置、再转向和落位的编辑步骤，亲手照顺序做',


    'a f i creative_workflow_plan',


    '另用基础地板前提，风格a、即时反馈f与明确自订规则i分开，单轮编辑流程0。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_STONE',


    '只当前已开放且能放的木地板，不造全构件解锁、免费木料或自订规则必定能完成的保证。'))


VAL_SURVIVAL[3]['variants'].append(_extra(


    '草甸水边的燧石',


    '没有航船、也没走林缘的经历，可以答草甸水边：浅岸当前能步行，眼前有已见的燧石与树枝，河湾后还没看过。你先怎样继续？',


    '沿能走的浅岸绕到河湾后，想亲眼看看那边是什么|先核对眼前实际可见的燧石与树枝，再决定这一轮取什么|沿用我给他设定的沿水旅人身份，顺着已熟悉的河岸继续赶路|回到已经熟悉的岸边慢慢走一阵，享受这个地方的安定感',


    'w material_stock_review r h',


    '以真实草甸燧石岸替代航船/林缘，w为未知发现，r有本人角色习惯影响行动，已见物料查看0。',


    'VAL9L_STORE VAL9L_STONE',


    '只给定当前能步行的浅岸，不要求游泳、造船、地图或水中必有资源，也不把找指定材料计探索动机。'))


VAL_SURVIVAL[4]['variants'].append(_extra(


    '不用交战或砍树的锤子操作',


    '没经历小盾交手或挥斧砍树，也可答最早锤子：当前已能放普通木墙与地板，木料够，这里可以调整一个转角。你先怎样投入？',


    '反复练选择木墙、转向与落位，专门把这一项工具操作练熟|亲手放下或转动一块构件，喜欢输入和眼前变化相连的反馈|只改一块当前木墙的朝向，亲手看看这一项编辑结果|先核对当前已可用的旋转与放置说明，再继续自己的尝试',


    't f creative_edit_trial tool_reference_first',


    '无战斗、砍树前提的工具场景；刻意重复t、即时反馈f与普通改动/读说明0分开。',


    'VAL9L_STORE VAL9L_PLAYER VAL9L_STONE',


    '当前构件与材料给足，不评价技术、建成速度或成功率；普通换方向不直接解释为练习或发明。'))


VAL_SURVIVAL[5]['variants'].append(_extra(


    '不涉及死亡和坏工具的携带调整',


    '没遇过墓碑或坏斧，可以答最早一次收纳：已有木石和食物，小木箱当前可用；只是想调整这一段随身带什么。你先怎样做？',


    '实际把一部分已有物品放入箱中，再带其余物件继续活动|先核对当前已带的食物与补给，再决定这一趟怎样存取|照我给他设定的定居者身份，把现有木石留在箱中，把这里当作这轮落脚处|先核对已经可用的物品取放说明，再继续实际收整',


    'item_handling_action survival_status_review r game_reference_first',


    '不靠受挫经历的替代；实际存取、查看已带食物补给与读说明0，r须角色习惯影响物件取舍。',


    'VAL9L_STORE VAL9L_STONE',


    '只已持有物品与可用箱子，不造自动取箱、死亡掉落或携带上限规则，不以留下食物多少推人格。'))


VAL_SURVIVAL[6]['variants'].append(_extra(


    '不需要物品架或箱子的草甸口粮',


    '没用过物品架或箱子，也可答最早带着草甸口粮的一段：莓果与蘑菇确实已拾到，当前能吃或继续携带。你先怎样安排？',


    '把已见口粮种类当作自己的小收藏目标，惦记还没收进的那一类|只核对当前食物状态与已带补给，再决定这一轮怎么活动|照我给他设定的赶路习惯，吃一点现有口粮，带着余下的继续沿岸走|补记这批已经取得的口粮与发现地点，保留真实经历',


    'c survival_status_review r game_recording',


    '用随身口粮替代展示/箱中收集，c明确种类缺口；身体补给核对和补记0，r有角色习惯影响行动。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_STONE',


    '不要求吃满食物栏、最优属性或任何特定未见品种；普通带食物不自动计收藏或角色代入。'))


VAL_SURVIVAL[7]['variants'].append(_extra(


    '未读剧情提示时的第一处停步',


    '没留意符文石或乌鸦提示，也可以只答最早踏进草甸后的一段：这里有能停留的空地和可拾木石，也有一条可走但没去过的方向。你先怎样继续？',


    '沿用我给他设定的定居者身份，留在空地拾起现有木石，为第一处住所准备|走向没去过的那边，想亲眼知道地形转过去是什么样|先在已熟悉的小空地慢慢走走，享受这段已经安稳的停留|先核对眼前实际可见的木石与当前已知存量，再决定这一轮怎样处理',


    'r w h material_stock_review',


    '不需要阅读特定故事或提示，角色行动r、未知发现w与熟悉停留h分别明示，现场物料查看0，不要求任何说明曾经出现。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_HUGIN VAL9L_STONE',


    '不要求Hugin提示开启，不把自设角色生活方式冒充游戏剧情分支；不能由默认角色外观推代入。'))


VAL_SURVIVAL[8]['variants'].append(_extra(


    '真实最初沿草甸拾物的一段',


    '没有田地、圈养或小屋经历，就回想最早沿草甸走动和拾物的真实一段：哪种已经发生的投入最贴近你愿意保留的体验？',


    '走到还没看过的草甸岸边，想亲眼知道那边有什么|亲手拾起木石，喜欢输入之后物件立刻被取起的反馈|在已经熟悉的一小片地方慢慢走一阵，享受安定停留|只是先核对当时眼前实际已有的材料，再决定那一轮取什么',


    'w f h material_stock_review',


    '无养殖/建造前提的真实早期回顾，未知发现、即时反馈与熟悉停留有不同动机；物料查看0。',


    'VAL9L_STORE VAL9L_STONE',


    '只问实际过去，不要求之后照做；拾物不直接计收藏，资源自然刷新不计长期养成。', reflection=True))


VAL_SURVIVAL[9]['variants'].append(_extra(


    '真实建人物并踏进草甸的开头',


    '如果还没搭过小屋或火堆，就回想真实建人物并踏进草甸的开头：哪种已经做过的动作更接近你愿意保留的投入？',


    '选择过发型或其他可用外观，让维京形象表达自己想要的风格|给他设定过流浪者身份，入场后照这份设定先赶路，暂不搭住处|进入后就走向一处没看过的方向，想亲眼知道那里是什么样|只是先查看当时已开放的外观方案，再决定采用哪种',


    'a r w creative_option_review',


    '无房屋/火堆前提的真实开头：外观表达a、身份设定确实影响后续行动r、未知发现w与普通浏览0分开。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_10',


    '不根据身体、性别、肤色或所选发型直接推现实身份；r不是仅选一个外观。所有发型起始可选按1.0正文，不要求BarberStation。', reflection=True))


VAL_SURVIVAL[10]['variants'].append(_extra(


    '真实拿到新材料后的配方提示',


    '没有升级装备、练石斧或烹饪经历，就回想最早拾到新材料、看到配方提示的真实一段：哪种已经做过的动作最接近你愿意保留的体验？',


    '留意已经见过的材料或配方种类缺口，想慢慢补进还没收齐的那一类|接着走到一处没去过的草甸边，想亲眼发现那边是什么|沿用我给他设定的流浪者身份，带上刚拾的东西继续走，暂不制作|只是先核对当时已经出现的玩法说明，再继续实际尝试',


    'c w r game_reference_first',


    '资源触发新配方是本作真实机制；种类齐全c不等于照配方做物品，未知发现和角色影响行动各自明示，读说明0。',


    'VAL9L_STORE VAL9L_STONE',


    '不要求记住某配方或取得后期材料，不把已有提示复述计因果解谜，也不把任何解锁都自动计养成。', reflection=True))


VAL_SURVIVAL[11]['variants'].append(_extra(


    '真实给最早营火添木的一段',


    '没有同游或独自加规则的经历，也可回想最早给已有营火添过木的一段：哪种真实做过的动作最接近你愿意留住的体验？',


    '实际给当时可添木的营火添入一份已有木材，亲手体验这项操作|回到已经熟悉的火边慢慢待一阵，享受安定停留|照我给他设定的守屋习惯，补火后仍留在火边收整已有物品，暂不远行|先核对当时已有的营火交互说明，再继续实际添木',


    'available_operation_trial h r game_reference_first',


    '无真人或自订规则前提的真实营火操作；普通添木操作0与熟悉停留h、角色影响下一步r分开，核对已有交互说明0。',


    'VAL9L_GENERAL VAL9L_STONE',


    '只已有能用营火与木材，不借用绿色地狱手钻/引火草，不要求等待时间、Rested数值、吃满口粮或成功通关。', reflection=True))





VAL_HAMMER = [


    Q(1, '已解锁木构件的第一间长屋',


        '世界当前启用Hammer/No Build Cost，你已解锁的木墙、地板与屋顶可直接放置；不需要为这些构件先砍树。空地已经能建，你先做什么？',


        '先选一个自己想表达的长屋样子，用这批构件把风格摆出来|按自己给维京人设定的经历，决定这间屋应当留下怎样的入口与火边位置|给这一轮加一个自己的小规则，例如只能沿弯曲边界搭屋，再照规则玩|先看当前已开放的墙、地板和屋顶样式，再决定采用哪一种',


        'a r i creative_option_review',


        '仅已解锁且当前可放的建筑构件免材料，不能推全配方、装备、物品无限。风格a、角色身份影响行动r、自订玩法i分开，浏览创作选项0。',


        'VAL9L_STORE VAL9L_MODIFIERS VAL9L_10FAQ',


        ('只放过最早几块地板也可答：这些已解锁木构件当前无建造材料消耗，锤子可用，眼前还有一点空地。你先怎样玩？',


         '把这几块木地板排成自己想要的小屋轮廓，表达这一角的感觉|按给这名维京人设定的习惯，决定他会把第一块地板落在哪里|自己规定这轮只搭一个转角，然后看用现有构件能怎样玩|先浏览当前已经能用的木构件，再决定这一轮采用哪种',


         'a r i creative_option_review')),


    Q(2, '免材料仍要解决的支撑',


        '当前建造不耗这些已解锁构件的材料，但悬出去的木屋顶仍有一段放不稳。你不知道是哪处连接影响它，先怎样试？',


        '先猜一个支撑原因，保持其他连接不变，只加一段已有立柱，检验这次结果|排清先拆哪块、再补哪段连接、最后放屋顶，按这一轮施工顺序做|只移动一块当前可调整的构件，亲手看这次改动后的样子|把这处改成自己更想表达的轮廓，先照顾整栋长屋的风格',


        'p construction_action_plan creative_edit_trial a',


        '免材料不等于免支撑；p是本人尚未确认规则的单项可失败测试，普通移动和施工顺序0。无固定颜色阈值、承重公式或必定成功要求。',


        'VAL9L_STORE VAL9L_MODIFIERS VAL9L_PLAYER',


        ('还没搭悬屋顶也可答：最初几块木地板与墙已能放，当前这些构件不耗材料；你正调整一处小转角。你先怎样继续？',


         '只转动一块已有墙，亲手看看改变后的转角|排清先放地板、接墙和最后调整位置的先后，再照这轮施工顺序做|把这个转角做成自己喜欢的轮廓，重视它表达的样子|先核对当前已经能用的旋转与放置说明，再亲手继续',


         'creative_edit_trial construction_action_plan a tool_reference_first')),


    Q(3, '有燃料却反复熄灭的室内火',


        '你这间已造好的屋里，火堆当前有燃料却反复熄灭，原因还没弄清；锤子与已有屋顶构件可调整。你先怎样处理？',


        '怀疑烟排不出去，保持火堆位置和燃料不变，只改一个排烟开口，再观察|先核对已有建筑或火堆操作说明，再继续自己的改动|排清这轮拆顶、留开口和补回周边构件的先后，亲手照顺序试|先回到另一处已经能安稳停留的熟悉火边，享受待一阵的感觉',


        'p tool_reference_first construction_action_plan h',


        'p明示未知原因和单项检验，不把正确答案藏在已给原因里；不承诺开口必修好。仍以实际可用火堆与建材为前提，无材料成本不推无烟伤或免天气。',


        'VAL9L_MODIFIERS VAL9L_STONE VAL9L_PLAYER',


        ('只经历过最早露天营火也可答：它当前确实能烧，你可以在旁边放已解锁的几块木构件，不耗这些构件的建造材料。想先怎样用这段时间？',


         '给火边搭一个自己想表达的小小轮廓，优先让它有自己选定的气质|亲手放下、转动一块木构件，留意输入与眼前变化紧接着发生的感觉|先排清这轮放哪块、转哪块和怎样收尾，再照顺序动手|留在熟悉火光附近慢慢待一阵，享受这处已经安稳的地方',


         'a f construction_action_plan h')),


    Q(4, '已能用锄头的地面',


        '当前锄头已经制作好并可用，你正给长屋门前整一小片地。建造构件免材料，但这把工具仍按当前已有条件使用。你先怎样玩？',


        '猜平地结果会随自己站位变化，保持目标小片地不变，换一次站位检验|亲手抬落锄头，享受动作之后地面立即回应的感觉|把门前修成自己选定的坡线和轮廓，重视这一角的风格表达|排清这一轮走到哪、整哪片、何时停手恢复耐力，再照安排试',


        'p f a tool_operation_plan',


        '锄头确实已拥有；p是未知作用关系的比较，不保证地面变平，f不是技术评价。路线/操作/恢复都明示才用工具流程0，无飞行、无限耐力或自动平地MOD。',


        'VAL9L_MODIFIERS VAL9L_PLAYER',


        ('还没做锄头就换这里：最初的锤子与已解锁木地板可用，这些构件不耗建造材料；你站在草甸空地。先做什么？',


         '亲手旋转、放下一块地板，留意输入与构件落下相连的反馈|把地板边缘排成自己想表达的小屋形状|只移动一块已经放下的地板，亲手看改动后的样子|先排清这次放置、转向与收尾的编辑步骤，再照顺序做',


         'f a creative_edit_trial creative_workflow_plan')),


    Q(5, '物品架旁的实有物件',


        '你已解锁并放好物品架，手边确实有能放上去的战利品、工具或食物；建造免材料没有替你生成这些物件。你想先怎样摆？',


        '选现有物件配合梁柱和桌边，表达自己想要的大厅气质|按自己已见过的种类留出展示位置，惦记慢慢补齐缺的那一类|只调整一件现有摆设的位置，亲手看看这次编辑结果|把已经取得过的这些物件和来处补记下来，保留经历记录',


        'a c creative_edit_trial game_recording',


        '展示风格a与补种类c有不同目的；一项普通编辑或记录0。架上物必须实际持有且可放，不从NoBuildCost生成无限食物、工具或稀有战利品。',


        'VAL9L_STORE VAL9L_MODIFIERS VAL9L_PLAYER',


        ('没有物品架也可答：你最早已有小木屋与一个能用的箱子，手边是真实拾过的木石和莓果；当前这些已解锁建筑不耗建造材料。先怎样收整？',


         '把箱子与木墙摆成自己喜欢的角落，重视表达这一间的风格|以已经见过的材料种类作自己的收藏目标，惦记还缺哪一类|只调整眼前这批已有物品的携带与存放，再继续自己的安排|补记这几件已拿到的物品和发现地点，留下经历记录',


         'a c item_handling_action game_recording')),


    Q(6, '这轮自行加的建造限制',


        '当前已解锁的木构件可免材料放置，你想再做一小间能走进去的屋子。还没有规定要怎样搭，先把时间用在哪里？',


        '自己规定这一间只用已有墙与顶、不落中间立柱，再按这条自订限制尝试|比较一处自己还没弄清的连接关系，只改一项支撑检验猜想|先定一套自己想表达的轮廓，再围绕这份风格调整墙顶|只先移动一块当前可调整的构件，亲手看这一项编辑的结果',


        'i p a creative_edit_trial',


        'i明确增设自订限制，不把普通试建都计发明；p是本人未知支撑问题而非已知解法。只承诺可以尝试，不保证无柱屋顶可成，也不添加官方竞赛或排行榜。',


        'VAL9L_STORE VAL9L_MODIFIERS VAL9L_PLAYER',


        ('还只会最早木地板也可答：已能放的几块木构件当前不耗材料，眼前有一处小空地。你先怎样玩？',


         '自己给这一轮定只沿一条弯边搭的规则，再照这个小玩法动手|只转动一块现有地板，亲手看看这项改动|选择自己想表达的转角形状，让这小块地方有自己的样子|先浏览当前已经开放的木构件，再决定采用哪一种',


         'i creative_edit_trial a creative_option_review')),


    Q(7, '免建筑材料的加工院',


        '冶炼炉、窑炉与储物箱当前已能使用，实际木材、煤和矿也够做一轮；这些建筑构件可免材料放置。你想先怎样安排这处院子？',


        '把木材补给、制煤、投矿和成品存放按多轮周转来安排，持续调整供给衔接|排清这一次搬动箱子、补一段地板与调整炉边位置的先后，再照这轮施工步骤做|把加工院外观做成自己想表达的样子，让它与长屋气质相合|只移动一只当前可调整的箱子，亲手看这一项布局改动的结果',


        'y construction_action_plan a creative_edit_trial',


        'y是持续多轮的手动供给与加工系统，不假造箱到炉自动物流。单轮搬动与布局编辑0；建筑免材料不代表矿、煤、装备或物品无限。',


        'VAL9L_GENERAL VAL9L_MODIFIERS VAL9L_PLAYER',


        ('没用过冶炼炉可答这里：最早木屋的地板、墙和箱子当前已解锁可放，不耗这些建筑构件的材料；你正调整一处储物角。先做什么？',


         '先排清这一次移动箱子、补地板和接墙的先后，再亲手照顺序做|把储物角摆成自己选定的风格，重视它表达的感觉|只移动一只当前可调整的箱子，亲手看看这次布局变化|先看当前已能选的地板、墙与箱子样式，再决定采用哪种',


         'construction_action_plan a creative_edit_trial creative_option_review')),


    Q(8, '确有同伴在同一处搭屋',


        '当前确有其他真人和你在这处免建筑材料的长屋旁活动；有人想继续搭顶，有人想走一圈。你先怎样参与？',


        '先谈清大家这轮共同想做什么，商量搭建、出门与再集合的安排|先陪他们走走聊聊，喜欢一起待在这片世界里的感觉|问过愿意参加的人，约定这轮只用一组木构件搭角落的自订规则|先调整自己这一角的梁柱和屋顶，让它表达想要的风格',


        'q o i a',


        'q是有真人且协商的共同目标，o是陪伴，i是实际同意的自订玩法。未联机者有独立单人ALT；不假定语音、共同钱包或每人进度一致。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS VAL9L_PLAYER',


        ('没有联机经历就答单人小屋：已解锁的木构件当前不耗材料，熟悉火边还有一处可建的角落。你先怎样过这一段？',


         '按自己给维京人的生活习惯，决定这个角落要留给什么|自己规定这一轮只能搭一个弯角，再照这个限制玩|回熟悉火边慢慢待一阵，享受已经安稳的停留|只调整一块现有构件的位置，亲手看看这一项编辑结果',


         'r i h creative_edit_trial')),


    Q(9, '真实多次回来的同一栋屋',


        '回想你在免建筑材料设置下真实改过的一栋屋：哪种已经发生的投入，最贴近你愿意留住的体验？',


        '多次回来给同一栋屋添东西，喜欢看前几次投入逐渐留在它身上|围绕自己选定的大厅气质调整梁柱与摆设，让它表达想要的风格|明明有别处可去，还是回到熟悉火边慢慢待着|只是为已搭过的构件、连接和改造步骤补记过程',


        'g a h construction_process_recording',


        '真实过去，g明确同一对象多次积累，不把一次修屋或免材料优势直接计养成。风格、栖居与过程记录分开，无规模、总时长或完工要求。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS',


        ('若只在这个设置下搭过最简单的小木屋，回想真实已经发生的投入：哪一种最贴近你愿意保留的部分？',


         '后来又回到同一处慢慢添墙补顶，喜欢看前一次投入留下来|把最早几块木构件摆成自己想表达的小小样子|在已经熟悉的小屋与火边慢慢待一阵，享受安定的感觉|只给当时已经放过的构件和步骤补上一份记录',


         'g a h construction_process_recording')),


    Q(10, '真实处理过的一处木构件问题',


        '回想免建筑材料时一次真实摆墙、接顶或处理支撑的经历：哪种实际做过的动作，最接近你愿意保留的体验？',


        '提出过一个自己尚未核实的支撑猜想，只改一项连接来检验|专门重复过一个转角的旋转与吸附操作，目的是把这一套动作练熟|给那轮搭建加过自己的构件限制，再按自订规则玩|只是为已经经历过的搭建和连接改动补记过程',


        'p t i construction_process_recording',


        '真实过去的原因检验p、刻意操作练习t、自订规则i都必须在行为里明确出现。只是记过程0；反复失败本身不证明坚持、能力或练习动机。',


        'VAL9L_STORE VAL9L_MODIFIERS VAL9L_PLAYER',


        ('尚未处理复杂屋顶，就回想最早在该设置下放几块木构件的经历：哪种已经做过的动作更贴近愿意保留的投入？',


         '反复练过把一块木墙旋转并接到地板边，目的就是让操作更熟|给这一轮定过只搭一段弯边的小规则，然后照着玩|只实际改动过一块现有构件的位置，亲手看那一次变化|只把已经放过的构件和步骤补记下来，保留那段记录',


         't i creative_edit_trial construction_process_recording')),


    Q(11, '真实发现材料与保留物件',


        '回想这个存档里真实探索或拾取过的经历：即使已有建筑不耗材料，哪种已经做过的投入仍最接近你愿意留住的部分？',


        '不为指定产物而走近一处未知海岸或林缘，想亲眼知道那边是什么|留意自己已见物件的种类缺口，惦记收进还没有的那一类|只为已经拿到的物品和实际到过的地点补上记录|只按已有物品与当前可用操作，调整了一轮携带和存放',


        'w c game_recording item_handling_action',


        '免建筑材料不抹去探索与真实物品；w是未知发现，c是种类目标，普通记录/存取0。新材料解锁配方不意味着问卷要求所有配方已开或去过后期群落。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS',


        ('没有出海或后期探索，就回想最早在草甸里实际走过和拾过东西的那段：哪种动作最贴近你愿意保留的体验？',


         '绕到一块还没走过的草甸后面，想亲眼看看那边有什么|把已见过的木石与其他小物当自己的收藏，惦记未收进的种类|只是为已经拾到的那批物件补上记录|只调整了当时现有物品的携带与存放，再继续自己的活动',


         'w c game_recording item_handling_action')),


    Q(12, '真实留在自己造的世界里',


        '回想一次你在该设置下真实自由搭建或停留的时段：哪种已经做过的动作，最接近你愿意再次保留的体验？',


        '按照自己给维京人赋予的经历，决定他会在这栋屋里怎样生活与行动|给这一轮另定一个自己的搭建规则，再照这个小玩法尝试|亲手旋转、放置木构件，喜欢输入之后它立刻出现在眼前的反馈|只为已经完成的那段建设补记过程，留下当时发生的步骤',


        'r i f construction_process_recording',


        '真实过去，r须本人角色设定影响行动，i须新加自己的规则，f是即时操作反馈；普通记录0。不从屋形、角色外观或所选预设推现实身份。',


        'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS VAL9L_PLAYER',


        ('只经历过最早放地板、接木墙也可答：回想真实发生过的动作，哪一种更贴近你愿意保留的投入？',


         '按自己对这名维京人的处事设定，决定第一处住所要落在哪里|给那一轮定一个只搭弯角的小规则，再按这个规则玩|亲手把一块构件放到眼前，喜欢输入与出现连在一起的反馈|只是给已经放过的构件和步骤补记过程，留下那一轮记录',


         'r i f construction_process_recording')),


]





VAL_HAMMER[0]['variants'].append(_extra(


    '还没建屋时的Hammer草甸活动',


    '还没在免材料设置下搭过屋或地板，可以答草甸上的一段：当前一条小路能走，前面还没看过，身后有熟悉停步处。你先怎样继续？',


    '往没看过的那段走，想亲眼知道它通到什么地方|沿用我给他设定的定居者身份，留在熟地查看一处可以落脚的位置|回到已经熟悉的停步处慢慢待一阵，享受安定感|先核对当前已带补给与身体状态，再决定这段活动',


    'w r h survival_status_review',


    '无建屋/地板前提；Hammer没有取消真实世界探索。未知发现、身份影响行动与熟悉栖居分开，当前状态0。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS',


    '不假定地图、食物或装备无限；只当前已可步行的一段，不造飞行或故事任务。'))


VAL_HAMMER[1]['variants'].append(_extra(


    '没有支撑问题时的新材料提示',


    '还没碰过悬屋顶或木转角，可以答最早取得木石的一段：新材料让部分配方出现，现有材料已够做石斧或木锤。你先做什么？',


    '以自己已经见到的配方种类作一个小收藏目标，惦记还没补进的那类|先比较当前已经可做的基础工具与材料条件，再决定采用哪项|给已经取得的这份材料与发现地点补记记录|先核对已经出现的基础玩法说明，再继续自己的尝试',


    'c compare_production_options game_recording game_reference_first',


    '不同于支撑测试和转角编辑的真实解锁前提；c明确种类目标，比较、补记、读说明0。',


    'VAL9L_STORE VAL9L_MODIFIERS VAL9L_STONE',


    'NoBuildCost仍只用已发现配方，工具另给材料足够的前提；不把提示复述当解谜，不把所有解锁都当养成或全配方已开。'))


VAL_HAMMER[2]['variants'].append(_extra(


    '不需营火的最初文字提示',


    '还没有室内或露天营火经历，可以答最早实际读过的一段文字：它谈到维京人来到这里的处境，你当前仍能在草甸自由走动，脚边有确实可取的木石。你先怎样继续？',


    '回想文字中的处境，想把这个人来到此地的原因与接下来经历接起来|沿用我给他设定的流浪者身份，读完便继续沿可走方向赶路，暂不搭住处|直接拾起眼前一件当前可取木石，亲手体验这项操作|给这段已经读到的人物信息补记自己的记录',


    's r available_operation_trial game_recording',


    '无营火前提的已读文字情境；故事理解s、身份影响行动r与普通拾取/记录0分开，不假设叙事文字兼有操作教程。',


    'VAL9L_GENERAL VAL9L_HUGIN VAL9L_STORE VAL9L_STONE',


    '仅自己确实读过的文字，不要求Hugin提示开着，也不编具体台词、官方分支或与NPC协商的真人证据。'))


VAL_HAMMER[3]['variants'].append(_extra(


    '还没做过地面和地板编辑的木斧',


    '还没用过锄头或铺地板，也可答这个存档最早拿着斧头的一段：斧头当前已拥有，树木能砍，旁边有停手空间。你先怎样投入？',


    '反复练挥斧和退步的时点，专门让这一套动作更熟|亲手砍一轮，喜欢声音、树身变化与输入紧接着发生的反馈|只先看当前已带补给和耐力状态，再决定怎样继续|排清挥斧、退到旁边恢复与再靠近的先后，再亲手按安排试',


    't f survival_status_review tool_operation_plan',


    '无锄头/地板经历的实有工具情境；t刻意重复、f即时反馈，查看补给与路线/恢复流程0。',


    'VAL9L_STORE VAL9L_PLAYER VAL9L_MODIFIERS',


    '斧头明确已有，不从免建筑材料推装备或工具免费，也不要求砍倒、效率或某个耐力数。'))


VAL_HAMMER[4]['variants'].append(_extra(


    '不用物品架与木箱的随身食物',


    '还没用物品架或箱子，可答最早拾到草甸口粮的一段：现有莓果与蘑菇能吃或继续携带，食物栏也有可用空位。你先怎样安排？',


    '先核对已有食物说明，确认莓果与蘑菇怎样占用食物栏，再继续吃用|把已见口粮种类作自己的小收藏目标，惦记缺的那一类|只核对当前食物与已带补给的状态，再决定这一轮怎样行动|照我给他设定的沿岸旅人身份，吃一点现有莓果，带着余粮继续走',


    'game_reference_first c survival_status_review r',


    '无展示/木箱前提；普通核对食物说明0，不从两种食物泛泛比较推组件配合b；种类齐全c、角色影响行动r与查看补给0分开。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS',


    '只当前持有、可吃且食物栏有位；不承诺同种食物能重复叠，不强迫最佳属性或满格。'))


VAL_HAMMER[5]['variants'].append(_extra(


    '还没有搭建时的自订步行规则',


    '还没在这里搭过小屋或木地板，可以只答草甸行走的一段：当前河边与另一处小坡都能走，身后有熟悉停留处。你先怎样玩？',


    '给这轮加只沿河边行进的小规则，再照自己的玩法尝试|沿用我给他设定的沿河旅人身份，先顺河岸走，暂不攀那处小坡|回到已经熟悉的地方慢慢走一阵，享受安稳停留|排清现有补给、这一小段去向与回程，再照这趟准备行动',


    'i r h mission_preparation_plan',


    '无建造前提的明确自订玩法i与身份行动r、熟悉栖居h分开；一趟资源去向安排0。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS',


    '自订规则不冒充官方挑战，不要求地图、船、飞行或只沿河必到某地点。'))


VAL_HAMMER[6]['variants'].append(_extra(


    '没有加工院或木箱时的基础工具',


    '还没用冶炼炉或收纳角，可以答最早制作工具的一段：你已选定这轮要做石斧，现有木石够做石斧或木锤，两项配方都已开放。你先怎样继续？',


    '直接制作这把当前可做的石斧，亲手体验这项操作|先比较当前已能做的石斧和木锤与材料条件，再决定采用哪项|排清这次取料、制作与收回余料的先后，再亲手照顺序做|按已选定的石斧需求核对条件并制作，重点是推进自己这轮工具目标',


    'available_operation_trial compare_production_options physical_tool_action_sequence stated_objective_progress',


    '无冶炼/收纳前提的真实制作；普通操作、比较、单轮流程与既定目标均精确0。',


    'VAL9L_STORE VAL9L_STONE VAL9L_MODIFIERS',


    '工具制作明示真实材料足够，不能以免建筑材料推此处装备或物品无需资源；不造科研或NPC协作人格。'))


VAL_HAMMER[7]['variants'].append(_extra(


    '没有同游和编辑经历的营火添木',


    '没有真人同游，也还没调整过小屋，可以只答最早营火的一段：它当前可添木，手头木材确实已有，旁边是熟悉停步处。你先怎样继续？',


    '实际给这处可用营火添入一份已有木材，亲手体验这项操作|在熟悉的火边慢慢待一阵，享受安定停留|沿用我给他设定的守屋身份，补火后仍在熟地慢走，留在营火附近|先核对已有营火交互说明，再继续实际添木',


    'available_operation_trial h r game_reference_first',


    '无真人/编辑前提；普通添木与读说明0，熟悉栖居h和角色影响行动r分别明确。',


    'VAL9L_STONE VAL9L_MODIFIERS',


    '只已有木材与当前可交互营火，不造添木必有光声变化，不借用其他游戏手钻引火，也不计NPC为真人。'))


VAL_HAMMER[8]['variants'].append(_extra(


    '真实人物外观与入场的最早一段',


    '还没有反复扩建或搭小屋的经历，就回想真实创建维京人并踏进草甸的最早一段：哪种已经发生的动作最贴近愿意保留的投入？',


    '用当时可选的发型或其他外观表达自己想要的维京形象|给他设定过流浪者身份，入场后照这份设定先沿可走方向赶路，暂不搭住处|走向没看过的草甸方向，想亲眼知道那边是什么|只是先查看当时已开放的外观方案，再决定采用哪种',


    'a r w creative_option_review',


    '无扩建前提的真实开头，风格a、身份影响后续行动r、未知发现w与浏览外观0分开。',


    'VAL9L_GENERAL VAL9L_10 VAL9L_MODIFIERS',


    '不由身体/性别/肤色/发型直接推现实身份；r须设定真实影响后续行动。1.0起始外观按已发布正文，不要求后期BarberStation。', reflection=True))


VAL_HAMMER[9]['variants'].append(_extra(


    '真实最早在草甸走跑的时段',


    '没有复杂支撑或基础地板编辑经历，就回想在这个存档最早走跑过的一段：哪种已经做过的动作最贴近愿意保留的体验？',


    '专门重复过一小段起跑、停步或跳落的操作，目的是让动作更熟|亲手在能走的地面上跑跳，喜欢步伐与落地随输入回应的感觉|走到一处没看过的小坡后，想亲眼知道那边是什么|只是先核对当时已显示的身体状态与携带补给，再决定那轮活动',


    't f w survival_status_review',


    '无编辑/承重问题前提的真实移动；刻意练习、即时反馈、未知发现各有动机，查看状态0。',


    'VAL9L_STORE VAL9L_GENERAL VAL9L_MODIFIERS',


    '只当前实际能走的草甸，不造跑跳计时关卡、排行榜或Hammer无限耐力；不问现实运动能力。', reflection=True))


VAL_HAMMER[10]['variants'].append(_extra(


    '真实最早打开制作菜单的时段',


    '没有较多探索或收集经历，可以回想在这个存档最早打开制作菜单、选定一项基础工具目标的一段：哪种真实动作更贴近愿意保留的投入？',


    '留意已见配方或材料的种类缺口，惦记慢慢补进还没有的那类|先查看当时已选工具列出的材料要求，核对已有材料是否够用|只是给已取得的材料与发现位置补上一份记录|只是先核对当时已出现的基础玩法说明，再继续实际尝试',


    'c objective_requirement_review game_recording game_reference_first',


    '无远行前提的真实制作菜单；c是明确种类目标，已选工具要求核对/补记/读说明0。不把仅已开放等同当前做得起，也不把看菜单都计收藏。',


    'VAL9L_STORE VAL9L_MODIFIERS VAL9L_STONE',


    'NoBuildCost不自动全解锁；不用未知配方当知识考查，不要求获得某一种后期材料。', reflection=True))


VAL_HAMMER[11]['variants'].append(_extra(


    '真实在工作台修过工具的一段',


    '没有自己加建造规则或放地板的经历，也可回想在可用工作台修过已有工具的真实一段：哪种动作最贴近愿意保留的投入？',


    '实际操作过当前可用的修理，把一件能修的工具接回手边继续用|按我给他设定的惜物工匠身份，修好后继续使用原工具，暂不制作替代品|回到已熟悉的工作台附近慢慢收整，喜欢这处已经安稳的停留|先核对当时已有的修理交互说明，再继续实际操作',


    'available_operation_trial r h game_reference_first',


    '无特殊建造经历的真实工作台修理；普通操作/读说明0，r须身份影响行动，h是熟悉舒缓停留。',


    'VAL9L_STONE VAL9L_MODIFIERS',


    '当前工作台、可修工具及操作条件都实际具备，不把普通修一次计长期养成，也不假造NoBuildCost自动恢复耐久。', reflection=True))





RAFT_SURVIVAL = [


    Q(1, '钩子蓄力与漂来的桶',


        '最早的塑料钩当前还能用，木板、塑料和一只桶正从可钩到的范围漂过；食水暂时够这一小段。你先怎样投入？',


        '反复练瞄准与松手的时点，专门把抛钩落点练得更熟|亲手抛出再收线，享受钩子拉回漂流物的声音与即时反馈|先核对已带补给和当前饥渴状态，再决定这一轮怎样活动|排清这次先取哪一件、怎样抛收与收整物品，再亲手按顺序做',


        't f survival_status_review physical_tool_action_sequence',


        't有专门重复练落点的目的，f是抛收反馈；当前状态和一轮实体工具顺序0。不以钩中率、速度或木桶必掉某物评能力，不要求下水追桶。',


        'RAFT9L_STORE RAFT9L_PLAYER',


        ('没追过桶，最早只钩过近处木板也可答：钩子仍可用，木板当前在范围内。你先怎样玩？',


         '专门重复练近处抛钩与收线的时点，想把这项操作练熟|亲手抛收这一钩，留意输入与物件靠近眼前相连的感觉|只先看当前饥渴状态和手边补给，再决定怎样活动|排清取钩、抛出、收回和收整木板的先后，再照顺序动手',


         't f survival_status_review physical_tool_action_sequence')),


    Q(2, '净水器与烤架共用木板',


        '简易净水器、杯子和简易烤架已能用，现有木板、海水与可烤食物；你想给接下来的活动留些食水。先怎样安排？',


        '把取水、添木、净水、料理和补回储备连成几轮周转，持续调配两边供给|只先查看当前食物、淡水与燃料的已有状态，再决定这一轮怎样处理|排清这一次取海水、添木、接淡水与放食物的先后，亲手照顺序做|先把眼前已经列明的一份淡水或食物做出来，以推进当前目标为重点',


        'y production_state_review physical_tool_action_sequence stated_objective_progress',


        '持续多轮投入产出衔接才y；普通查看、一次流程和已知目标0。给足已有器具，不给错误材料配方、饥渴满值或料理时间作门槛。',


        'RAFT9L_STORE RAFT9L_PLAYER',


        ('还没用烤架，最早只做过净水也可答：杯子、简易净水器和木板当前可用，能取海水。你先做什么？',


         '把接水、添木、接回淡水和下一轮补水接成循环，持续调整手头储备|只先看已有水和木板，核对当前补给情况|排清这一杯取水、添木和接回淡水的先后，再亲手照顺序做|先按当前明确的需求做出这一杯淡水，把眼前目标推进',


         'y survival_status_review physical_tool_action_sequence stated_objective_progress')),


    Q(3, '研究台里尚缺的材料',


        '研究台当前能用，界面显示一项你想学的普通配方还有材料未研究；所缺材料此刻手边也有。你先怎样继续？',


        '先看界面已经列出的材料条件，核对这次还差哪一项|把自己已研究的材料与可学配方当作种类目标，惦记慢慢补齐缺口|按当前已显示的要求推进这项配方，重点是把眼前目标接上|实际放入一份当前可研究材料，亲手体验这次研究操作',


        'objective_requirement_review c stated_objective_progress available_operation_trial',


        '已列明材料不是谜题；核对和普通研究0，c明确在意种类齐全。不把NPC功能或独自解锁配方计真人共同目标，也不声称研究一份即全解锁。',


        'RAFT9L_RESEARCH RAFT9L_PLAYER',


        ('还没造研究台可答：最早的制作菜单里有一项已开放基础器具，当前材料够，物品栏也有空位。你先做什么？',


         '先查看菜单已显示的材料要求，核对这次条件|比较当前已能做的几项基础器具与材料条件，再决定做哪种|按已有目标做出当前这项器具，重视把眼前需求推进|直接制作这一件当前可做的器具，亲手体验操作发生',


         'objective_requirement_review compare_production_options stated_objective_progress available_operation_trial')),


    Q(4, '飘带与这次航向',


        '当前帆、飘带与划桨可用，补给允许短途活动；你想试着靠近一处确实可接近、但还没去过的小岛。你先怎样玩？',


        '往那处没去过的小岛靠近，想亲眼知道岛上是什么样|还不懂这段风与帆向的关系，保持划桨不参与，只调一次帆向检验自己的猜想|亲手调帆或划桨，留意输入之后筏体与海面的即时回应|先排清已有食水、靠近方向与回到筏上的安排，再照这趟准备行动',


        'w p f mission_preparation_plan',


        'w是未知地点发现，p是尚未确认航行关系的可失败单项试验；f是操纵反馈，单次准备0。不写加第二面帆必提速，也不保证帆能朝任意方向逆风去。',


        'RAFT9L_STORE RAFT9L_NAV RAFT9L_SAILS RAFT9L_PLAYER',


        ('还没有帆，只有最早已做好的划桨也可答：当前筏边有一处可以划动的空间，近处小岛确实能靠近，食水暂够。你先怎样继续？',


         '朝没去过的小岛靠近，想亲眼看看那边有什么|亲手划这一段，留意每次输入后木筏和水面接着变化的感觉|先核对已有食水与当前饥渴状态，再决定活动安排|排清取用划桨、划这一段和收整手头物品的先后，再亲手照顺序做',


         'w f survival_status_review physical_tool_action_sequence')),


    Q(5, '下锚之后的礁石边',


        '当前已在一处小岛旁下好锚，钩子、食水与一次短潜的条件具备；水下有可到达却没仔细看过的礁石。你先怎样投入？',


        '沿没看过的礁石边看看，想知道遮住的水下轮廓后面有什么|专门重复一小段下潜、取物与上浮时点，想把操作练得更熟|先核对当前氧气、食水与携带补给，再决定这轮是否下潜|排清这次下潜路线、可取资源与返回筏上的先后，再按安排行动',


        'w t survival_status_review mission_preparation_plan',


        '给定已经下锚和实际可短潜；未知发现、刻意练操作与核对/准备0分开。无鲨鱼必不攻击、诱饵固定安全时长、无限氧气或固定矿物保证。',


        'RAFT9L_STORE RAFT9L_PLAYER',


        ('没有潜水经历可以答最早站在筏上的一段：钩子当前可用，近处漂流物可取，食水暂够。你先怎样继续？',


         '反复练抛出与收回的时点，想让这一项操作更熟|亲手抛收这一钩，留意水声、钩子与物件靠近的直接反馈|只先核对当前饥渴状态与已带补给，再决定怎么活动|排清取钩、抛出、收回与收整这轮物品的先后，再亲手做',


         't f survival_status_review physical_tool_action_sequence')),


    Q(6, '回收机与两种交易货币',


        '你已有能用的回收机，也到过当前可交易的站点；已有可回收材料，货架列着想要物品的垃圾块或贸易币要求。你先怎样安排？',


        '把剩余材料、回收产物与稀有鱼交易分成多轮供给，持续调整两种货币的来源|只先看当前货架已经列出的支付条件和已有货币，核对这次能换什么|把当前已见装饰或其他物件列成自己的种类收藏，想补进缺的那一类|先推进一项当前确实付得起的既定购买，把已经选定的目标接上',


        'y objective_requirement_review c stated_objective_progress',


        'y是持续安排不同来源而非单次点交易；垃圾块回收、贸易币卖稀有鱼不能互换。NPC店不是协商共同目标q；价格、等级与自动生产效率不定值。',


        'RAFT9L_FINAL',


        ('尚未交易或回收，可以答最早把漂来的材料带回筏上：手边已有木板、塑料、叶子与可用小箱，食水暂够。你先怎样收整？',


         '先按现有物品调整携带与箱中存放，再继续自己的安排|把已见材料种类当作自己的收藏，惦记还缺哪一类|比较当前开放且材料够的制作选项，再决定先做什么|按已经选定的一项基础制作需求，推进这轮眼前目标',


         'item_handling_action c compare_production_options stated_objective_progress')),


    Q(7, '已有画刷与两面木墙',


        '画刷、当前颜料与可涂的一面木墙已经可用，另一面也能分别处理。你先想怎样用这点空闲？',


        '选一套自己想表达的颜色与图案，让这片甲板有自己的风格|按自己给这名漂流者设定的生活习惯，决定他会怎样布置这一角|先在熟悉筏上慢慢走走，喜欢已经安稳生活过的这片地方|只改一处当前可涂的颜色设置，亲手看看这项编辑结果',


        'a r h creative_edit_trial',


        'a明确表达风格，r由本人角色习惯决定行动，h是熟悉停留；一项普通涂装试用0。不将选色当现实性格，也不假定所有物件都能双色涂。',


        'RAFT9L_RENOVATION',


        ('还没有画刷可答：最早已有建筑锤、够用木板塑料，当前一小段筏边能扩建。你先想怎样做？',


         '把这一小段排成自己选定的轮廓，让筏子表达想要的样子|按自己给漂流者设定的习惯，决定这一角留给什么生活用途|先沿熟悉甲板慢慢走一圈，享受已有小小住处的安稳感|只实际放下一块当前可建的地基，亲手体验这一项操作',


         'a r h available_operation_trial')),


    Q(8, '已拿到的故事笔记与频率',


        '已到过一个故事地点并拿到笔记，当前Notebook能回看或回听；接收器也已能用。没有必须立刻离开的期限，你先做什么？',


        '回看这些人留下的笔记，把他们的经历与之前听过的线索接起来|按自己给当前漂流者设定的立场，决定他读完后要先留一阵还是继续航程|只先查看当前接收器实际显示的目标与位置，核对导航信息|只为已经拿到的笔记与实际体验过的地点补记自己的记录',


        's r navigation_information_review game_recording',


        's是故事联系，r是本人角色立场影响行动而非官方分支；导航阅读与补记0。仅已取得笔记回放，不让未到RadioTower者先答后期人物，也不要求打开已关自动朗读。',


        'RAFT9L_FINAL RAFT9L_NAV',


        ('没有故事地点经历，可以答最早筏上的空闲：钩子、杯子与已做好的净水器当前可用，食水暂够。你先怎样过这段？',


         '先核对已经出现的玩法说明，再继续自己的实际尝试|亲手抛收一钩，享受声音与物件拉近的即时反馈|先回熟悉的器具旁慢慢走走，享受小小筏上安稳停留的感觉|排清这一杯取水、接回淡水和收整杯子的先后，再亲手照顺序做',


         'game_reference_first f h physical_tool_action_sequence')),


    Q(9, '真实钓过或照料过的食物',


        '回想真实在筏上钓鱼、种植或料理过的时段：哪种已经做过的投入，最接近你愿意留住的体验？',


        '多次回到同一片菜圃照料，喜欢前几轮投入在这处作物上留下变化|把补水、种植、收成与料理接成多轮周转，持续调配供给|留意已经见过的鱼种或可种作物，惦记自己的种类收藏还有哪项缺口|亲手抛竿、提线或取下料理，喜欢输入之后紧接着发生的反馈',


        'g y c f',


        '真实过去；对象持续养成g、供给系统y、种类c、即时反馈f分开。不推动物饥饿死亡、固定格数、配方或食物奖励数值，也不以每次重新种下等于同株永久成长。',


        'RAFT9L_STORE RAFT9L_PLAYER',


        ('没有种植或钓鱼经历，就回想最早实际做过的一杯净水：哪种已经发生的投入，更接近愿意保留的体验？',


         '后来把接水、添木与补回淡水接成几轮循环，喜欢持续调配手头供给|亲手接入海水、拿回淡水，喜欢输入与器具回应相连的反馈|留在已经熟悉的净水器旁慢慢待一段，享受小小住处的安稳感|只是先看当时已经有的水、木板和身体状态，再决定那轮怎么做',


         'y f h survival_status_review')),


    Q(10, '真实扩起来的同一张筏',


        '回想你真实扩建或布置过的这张木筏：哪种已经做过的动作，最贴近你愿意留住的投入？',


        '几次回来都接着完善同一张筏，喜欢早先投入逐渐留在这个家上面|围绕自己选定的轮廓、配色或摆设调整，让它表达想要的风格|按自己赋予漂流者的经历与习惯，决定甲板上哪些地方要怎样生活|只是为已扩过的地基、连接和器具布局补记过程',


        'g a r construction_process_recording',


        '真实过去，同一筏持续投入g不同于一轮普通维修；风格a和角色身份r需要明确目的。只记过程0，不看规模、航行天数或终章进度。',


        'RAFT9L_STORE RAFT9L_RENOVATION',


        ('如果只扩过最早几格地基，回想当时真实做过的动作：哪一项最贴近你愿意保留的体验？',


         '后来又回来给同一小块筏添东西，喜欢先前投入一直留在这里|把最早几格地基排成自己想表达的样子|按照自己对这名漂流者的设定，决定最早这角留给怎样的生活|只为已建过的地基与步骤补记过程，留下一份建设记录',


         'g a r construction_process_recording')),


    Q(11, '真实尝试过的工具或装备',


        '回想真实使用过潜水装备或手头工具的一段：哪种已经做过的投入，最接近你愿意留住的体验？',


        '比较过当时确实可用的两组潜水装备搭配，再下水检验它们带来的不同效果|专门重复过一小段抛钩、取物或上浮时点，目的是让自己的操作更熟|亲手使用工具，喜欢声音、动作与眼前变化紧接着发生的反馈|只是先比较当时已有的装备与组件，再决定那段怎么安排',


        'b t f compare_available_setup',


        '真实过去，b是比较并检验组合效用，不是戴上单件装备；t是刻意重复，f是即时反馈，普通浏览0。不假造角色技能树或武器经验等级。',


        'RAFT9L_STORE RAFT9L_FINAL RAFT9L_PLAYER',


        ('还没潜过水或换过装备，就回想真实用第一只塑料钩收近处漂流物的那段：哪种动作最贴近愿意保留的体验？',


         '反复练过近处抛钩与收回的时点，目的就是把这一项操作练熟|亲手拉回木板，喜欢钩子、声音与物件靠近相连的反馈|只是排清当时取钩、抛收与收整物件的先后，再亲手照顺序做|只是先核对当时饥渴状态与已有补给，再决定这一轮怎么活动',


         't f physical_tool_action_sequence survival_status_review')),


    Q(12, '真实同游时留筏还是登岛',


        '回想一次确实有其他真人一起玩的时段：有人想留筏整理，有人想登岛；当前都可以商量。哪种你实际做过的动作最贴近愿意保留的投入？',


        '先谈清这轮共同目标，商量谁照料筏上器具、谁登岛以及何时再集合|先陪同伴待一段、聊眼前漂来的东西，喜欢一起漂流的陪伴|问过愿意参加的人，约定这轮只用钩取物、不登岛的临时自订玩法|只为已经参与的筏上建设与器具布局补记过程',


        'q o i construction_process_recording',


        '仅真实真人，q协商推进、o陪伴、i明确同意的自订规则。NPC解锁角色不当真人；单人ALT无假同伴、语音默认开启或必定救援承诺。',


        'RAFT9L_STORE RAFT9L_CURRENT RAFT9L_HOTFIX',


        ('没有联机经历，就回想真实一个人在最早木筏上的时段：哪种已经做过的动作，最贴近你愿意留住的体验？',


         '给那轮定过只钩近处木板的一条小规则，再照自己的玩法尝试|亲手抛收一钩，喜欢水声、钩子与物件回到眼前的即时反馈|在熟悉的净水器和甲板边慢慢待一阵，享受已经安稳的地方|只为已经拿到的物品补记记录，留下真实发生过的经历',


         'i f h game_recording')),


]





RAFT_CREATIVE = [


    Q(1, '静止木筏的第一层甲板',


        '当前是原生Creative，木筏保持静止；建筑锤和菜单里当前可取的基础构件可用，不必等漂流材料。你先怎样开始这层甲板？',


        '先选一个自己想表达的轮廓，把这张筏做成有个人风格的样子|按自己给船主设定的生活习惯，决定入口和活动区该落在哪里|给这一轮定一个自己的规则，例如所有房间都沿一条弯曲走廊接起来|先浏览当前已能用的地基、墙与楼梯方案，再决定采用哪种',


        'a r i creative_option_review',


        'Creative木筏静止，所有情境只用当前菜单已有构件；不编出海、采流、登故事岛。风格、角色行动与自订玩法目的明确，浏览0，不说几乎所有等于所有物件必可得。',


        'RAFT9L_CREATIVE RAFT9L_PLAYER RAFT9L_RENOVATION',


        ('如果只在Creative放过最早几块地基也可答：基础构件当前可取，木筏不航行。你先怎样玩这小片空间？',


         '把这几块排成自己想表达的小筏轮廓|按自己对这名船主的设定，决定第一处生活角落落在哪里|自己规定这轮只沿一条折线放地基，再照这个小规则玩|先看看当前已开放的基础构件方案，再决定用哪种',


         'a r i creative_option_review')),


    Q(2, '二层地板与横向支撑',


        '当前Creative里，已有二层地板的一段放不成，你还不知道哪处支撑影响它；横柱、立柱与现有构件此刻可用。先怎样处理？',


        '猜是这一侧连接不够，保持别处不变，只加一段当前横柱，检验这次结果|排清先补哪段支撑、再接哪块地板与最后收尾的顺序，照这轮施工安排做|优先把楼层外形改成自己想表达的轮廓|只实际换掉一块当前可调整的构件，亲手看这项编辑结果',


        'p construction_action_plan a creative_edit_trial',


        '支撑原因尚未知，单项试验可失败才p；Creative不等于免支撑。横柱已实装另有原始公告，不保证加任意一段就能成功，普通施工/编辑0。',


        'RAFT9L_FINAL RAFT9L_CREATIVE',


        ('还只建过第一层，可以答当前Creative最初的转角：已有地基、墙和建筑锤可用。你先怎样继续？',


         '把这一处排成自己想表达的转角形状|只转动一块当前可调整的墙，亲手看这项变化|排清这轮先接哪块地基、放哪面墙再收尾，亲手按顺序做|先核对已经可用的旋转和建造说明，再继续自己的试用',


         'a creative_edit_trial construction_action_plan tool_reference_first')),


    Q(3, '墙两面的颜色与图案',


        'Creative的画刷与当前可用颜色、图案已取好，一面木墙的内外两侧都能分别上色。你先怎样处理？',


        '选一组自己想表达的内外配色，让室内和外观各有想要的风格|只改其中一侧当前可用的颜色设置，亲手看这一项编辑结果|专门反复练取色、瞄准与换面的操作，目的是把工具用得更熟|先浏览当前颜色与图案预览，再决定采用哪一种',


        'a creative_edit_trial t creative_option_review',


        '风格a须本人想表达，反复工具练习须明确t动机；普通一项编辑或浏览0。只可涂的木墙，不推全部物件必可涂或任意面共用颜色。',


        'RAFT9L_RENOVATION RAFT9L_CREATIVE',


        ('没有用过画刷就答Creative最初的基础搭建：建筑锤与地基、木墙当前能用。你先怎样投入？',


         '把几块构件排成自己选定的轮廓，表达这一角的感觉|只实际放下一块当前可建的地基，亲手体验操作发生|反复练选择构件、转向和落位，专门让这一项操作更熟|先看菜单里当前已经能选的基础构件，再决定用哪种',


         'a available_operation_trial t creative_option_review')),


    Q(4, '能旋转拉伸的细节木板',


        '当前Creative已取到Detail Plank，能自由调整它的长度与朝向；你想给舱口添一小处细节。先怎样做？',


        '用这一段木板做出自己想表达的舱口轮廓，重视这艘筏的风格|自己给这一轮定只能用细节木板围出一个通行框的规则，再按规则玩|只实际改变这一段木板的长度或角度，亲手看编辑结果|先排清这一轮选位、调长短和转角度的步骤，再照顺序完成',


        'a i creative_edit_trial creative_workflow_plan',


        '自由伸缩旋转只属于已实装DetailPlank，不挪给所有建筑。i是本人新加的构件限制，普通拉伸和流程0；无需做出精美或能通行成品。',


        'RAFT9L_FINAL RAFT9L_CREATIVE',


        ('还没用细节木板，可以答Creative最早几块普通木构件：当前能选地基、墙与转向。你先怎样玩？',


         '把这个小转角摆成自己想表达的外形|自己规定这轮只围出一小段折线通道，再按这个限制玩|只旋转一块当前可调的木墙，亲手看看这项编辑|先排清这轮放地基、接墙和转向的编辑步骤，再照顺序做',


         'a i creative_edit_trial creative_workflow_plan')),


    Q(5, '桌子旁的一条过道',


        'Creative里已有一张桌子、储物箱与可走的甲板；经过桌边时有一处绕不开，你还没弄清是哪件摆设卡住。先怎样处理？',


        '猜是这只箱子挡住，保持桌子和其他东西不变，只搬箱子，再亲自走一次检验|排清这次收起箱子、换位摆回和补一段通道的先后，再照安排施工|把桌边与储物角做成自己想表达的样子，优先照顾这一角的风格|只先实际调整一只当前可移动箱子的位置，亲手看这项编辑结果',


        'p construction_action_plan a creative_edit_trial',


        'p明确未知通行原因与一次只改一件的验证，不把已给原因复述当推理；普通移箱和单轮流程0。已有可移动箱子先收起再放回，不编造自由拖拽所有物件。',


        'RAFT9L_STORE RAFT9L_RENOVATION RAFT9L_PLAYER',


        ('没有家具或通行问题就答最初空甲板：当前Creative能取基础构件，你正给一处角落接木墙。先怎样做？',


         '把这一处摆成自己想表达的小屋风格|只改变一块当前木墙的朝向，亲手查看这一项编辑结果|排清这一轮先补地基、再接墙与最后收尾的先后，再照顺序做|先浏览当前已可用的木墙与地基样式，再决定采用哪种',


         'a creative_edit_trial construction_action_plan creative_option_review')),


    Q(6, '餐桌、柜子与自己的生活角',


        '当前Creative已能取用一组桌椅和柜子，旁边还有可放的基础地板；这里不需要靠吃喝维持本轮活动。你先怎样布置？',


        '把桌椅与柜子配成自己选定的氛围，让这个生活角表达自己的风格|按自己给船主设定的生活习惯，决定他会把座位与储物角怎样安排|给这一轮定只用这一组家具搭一个小场景的规则，再照这个小玩法尝试|只先改一件当前可调整家具的位置，亲手看这项编辑结果',


        'a r i creative_edit_trial',


        'Creative不假造食水生存压力；风格、角色身份影响摆设与明确自订规则各有动机。只用当前菜单确有家具，不把普通搭场景自动计i。',


        'RAFT9L_CREATIVE RAFT9L_RENOVATION RAFT9L_PLAYER',


        ('如果只搭过第一层木筏，桌椅还没用过，就答当前能放的几块地基与木墙：你先怎样用这小片空间？',


         '把这几块拼成自己想表达的小小外形|按自己给船主的设定，决定他最早要在哪里留一个生活角|自订这一轮只用地基与木墙围一处角落的规则，再照规则玩|只实际调整一块现有构件的位置，亲手看这一次变化',


         'a r i creative_edit_trial')),


    Q(7, '自由观察视角与整张筏',


        'Creative里你已能用原生自由观察视角，筏上有自己当前已搭的地板、墙与楼梯。先想怎样使用这段观察时间？',


        '绕着看整张筏，再调整一处轮廓，让它表达自己想要的外形|专门反复练视角移动与靠近的操作，目的就是让这一套工具使用更熟|先查看已经可达的楼梯入口与通道现场，再决定下一步怎样继续|亲手切换、移动视角，留意输入之后眼前景物立刻变化的感觉',


        'a t scene_inspection f',


        '仅该模式当前已可用原生自由观察，不向生存模式添加飞行或相机。查看可达入口/通道0，t须刻意重复练工具，a须风格表达；不要求截图或发布。',


        'RAFT9L_CREATIVE RAFT9L_PLAYER',


        ('还没用过自由观察，也可站在最早甲板上答：当前基础构件已可取，木筏保持静止。你先怎样投入？',


         '站在甲板边看看再调整一个转角，让它表达自己选定的形状|反复练选择、转向与放置同一种构件，专门把操作练熟|只先查看已经能走到的甲板边和入口，再决定这一轮怎样继续|亲手放下一块构件，喜欢输入之后它马上出现在眼前的反馈',


         'a t scene_inspection f')),


    Q(8, '确有真人一起搭的Creative木筏',


        '当前确有其他真人和你一起在这张静止的Creative木筏上搭建；有人想加楼层，有人想先做生活角。你怎样参与？',


        '先谈清这轮大家共同想完成什么，商量谁改哪片、哪些地方留着一起决定|先陪他们逛逛已有甲板、聊正在搭的东西，喜欢同处这里的陪伴|问过愿意参加的人，约定这轮只用一套基础构件的小规则再一起玩|先把自己这一角调整成想表达的轮廓与摆设风格',


        'q o i a',


        '真人参与及同意明示；q协商共同目标、o陪伴、i自订玩法与a个人风格分开。无真人者换单人ALT；不要求上传、社区评比、竞赛或语音。',


        'RAFT9L_STORE RAFT9L_CURRENT RAFT9L_CREATIVE',


        ('没有联机经历就答单人Creative：当前能取基础木构件，已有一片熟悉甲板。你先怎样过这一段？',


         '按自己给船主设定的生活习惯，决定这一角该怎样安排|自己给这轮加只沿一条折线搭建的小规则，再照规则玩|在熟悉的甲板边慢慢走一阵，享受安稳停留的感觉|只调整一块当前可用木构件的位置，亲手看编辑结果',


         'r i h creative_edit_trial')),


    Q(9, '真实逐次扩起来的创意筏',


        '回想在Creative里真实扩过或改过的同一张筏：哪种已经发生的投入，最接近你愿意保留的体验？',


        '多次回来接着添楼层或改甲板，喜欢先前投入逐渐留在同一张筏上|围绕自己选定的整体形状与配色调整，让它表达想要的风格|明明还能继续建，也会回到熟悉角落慢慢待一阵|只是为已扩过的构件与布局改动补记过程',


        'g a h construction_process_recording',


        '真实过去，持续同一对象的积累g与风格a、熟悉停留h分开；普通记录0。没有材料消耗也不预先否定养成，但一次放置不直接计g。',


        'RAFT9L_STORE RAFT9L_CREATIVE RAFT9L_RENOVATION',


        ('若只在Creative扩过最早几格地基，回想当时真实做过的动作：哪种更贴近愿意保留的投入？',


         '后来又回来接着完善同一小块筏，喜欢早先投入留在这里|把最早几格地基摆成自己想表达的轮廓|在已熟悉的甲板边慢慢待一阵，享受这个小住处的安定|只给已经搭过的构件和步骤补记过程，留下一份建设记录',


         'g a h construction_process_recording')),


    Q(10, '真实试过的一处建造问题',


        '回想Creative里一次真实处理楼层支撑、家具通道或构件转角的经历：哪种已经做过的投入，最接近你愿意保留的部分？',


        '提出过一个自己未核实的原因，只改一项连接或摆设再检验|专门反复练过选取、旋转与放置同一类构件，目的是把工具操作练熟|给那轮搭建另定过自己的构件限制，再按这条小规则玩|只是实际改过一项当前构件的位置或朝向，亲手查看这次编辑',


        'p t i creative_edit_trial',


        '真实过去的单项原因检验、刻意操作训练、自订规则都有明确目的；一项普通编辑0。失败、重复或造大建筑都不自动证明p/t/i。',


        'RAFT9L_FINAL RAFT9L_RENOVATION RAFT9L_CREATIVE',


        ('没有复杂楼层或家具，就回想Creative最初几块地基与墙：哪种真实做过的动作最接近你愿意保留的体验？',


         '反复练同一块木墙的选择、旋转与落位，想把这一项操作练熟|给那轮定过只搭一条折线的小规则，再照自己的玩法做|只实际调整过一块当前木墙的位置或朝向，亲手看那一次变化|只为已经放过的构件与步骤补记过程，保留真实记录',


         't i creative_edit_trial construction_process_recording')),


    Q(11, '真实浏览和摆过的装饰种类',


        '回想你在Creative里真实看过或用过的装饰：哪种已经做过的投入，最接近你愿意保留的体验？',


        '按自己已见过的装饰类目留意缺口，惦记把想要的一套种类摆齐|选过一组家具、颜色或图案，让那一角表达自己想要的风格|只是先查看当时已开放的装饰与外观方案，再决定用哪种|只为已经用过的物件与实际体验过的位置补记记录',


        'c a creative_option_review game_recording',


        'c是实际自选种类齐全目标，不编成就或难找掉落；a是表达风格，浏览/补记0。Creative不靠搜装饰包解锁，不要求某一付费/隐藏物件存在。',


        'RAFT9L_CREATIVE RAFT9L_RENOVATION RAFT9L_PLAYER',


        ('尚未摆装饰，可以回想Creative最早真实浏览过的基础构件：哪种已经做过的动作，更贴近愿意保留的投入？',


         '以自己已见构件种类作一个小收藏目标，惦记想要的一套还缺哪种|选几块基础构件摆出自己想表达的轮廓|只是先看当时已开放的基础构件样式，再决定用哪种|只给已经用过的构件与位置补记记录，留下真实经历',


         'c a creative_option_review game_recording')),


    Q(12, '真实按自己的方式搭船',


        '回想一次真实在Creative里自由搭建的时段：哪种已经做过的动作，最接近你愿意留住的体验？',


        '按自己赋予船主的经历与习惯，决定他在这片甲板上怎样生活|给当轮搭建加过一个自己的规则，再按这个小玩法尝试|亲手旋转、放置构件，喜欢它随输入立刻出现在眼前的反馈|只是为已经完成的那段甲板与房间布局补记过程',


        'r i f construction_process_recording',


        '真实过去，身份影响行动r、自订规则i与即时反馈f分别明示；普通记录0。不从角色外形、建筑题材或Creative预设推现实身份，也不把自订玩法冒充官方模式。',


        'RAFT9L_CREATIVE RAFT9L_RENOVATION RAFT9L_PLAYER',


        ('只在Creative搭过最初几格地基也可答：回想真实发生过的动作，哪种更贴近你愿意保留的部分？',


         '按自己对船主的设定，决定最早这个生活角该摆在哪里|给这一轮定过只沿一条折线放地基的小规则，再按规则玩|亲手放下一块地基，喜欢输入与构件出现连在一起的反馈|只为已经放过的构件和步骤补记过程，保留真实记录',


         'r i f construction_process_recording')),


]





# Each ALT2 below is handwritten around another verified native interaction.


# These additions remain private pending complete-context and independent review.


RAFT_SURVIVAL[0]['variants'].append(_extra(


    '未用钩时的实际钓竿操作',


    '钩取的两种情境都不适用，可以答确实用过钓竿的一段：当前鱼竿仍可用，筏边可以下竿，食水暂够。你先怎样投入？',


    '专门重复练抛竿和收线的时点，想把这一项操作练熟|亲手抛出再提线，留意输入、水声与竿线回应相连的感觉|先核对当前身体状态与已带补给，再决定这段活动|排清这次取竿、下竿、提线与收整物品的先后，再亲手做',


    't f survival_status_review physical_tool_action_sequence',


    '用另一件原生实体工具替代钩取经历；刻意练习t、即时反馈f与查看/单轮动作0分开。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '只用于实际用过钓竿；不承诺必钓中、稀有鱼、固定等待时间或贸易币来源。'))


RAFT_SURVIVAL[1]['variants'].append(_extra(


    '未料理时的小种植槽',


    '前两种料理、净水情境都没经历过，可以答实际用过的小种植槽：已有能种的种子、空槽与可用淡水。你先怎样安排？',


    '把留种、补淡水、种植和之后收成接成几轮周转，持续调整作物供给|只先看当前种子、淡水与作物状态，再决定这一轮怎么处理|排清这一轮取种、种下、浇水和收整杯子的先后，再亲手照顺序做|直接种下当前这一份可种种子，亲手体验这次操作',


    'y production_state_review physical_tool_action_sequence available_operation_trial',


    '另一个真实食物生产前提；y须持续多轮供给，单轮种植不计系统经营；已有状态/实际操作0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '不用错误槽位数量，不保证鸥鸟不来、某作物产量、自动灌溉或收获必留够下一轮种子。'))


RAFT_SURVIVAL[2]['variants'].append(_extra(


    '未研究制作时的随身材料',


    '研究台和制作都还没体验过，可以答实际拿到材料的一段：物品栏已有木板、塑料或叶子，眼前近处仍有可取漂流物。你先留意什么？',


    '把自己已经见过的材料种类作一个收藏目标，惦记还缺哪一类|先核对眼前可见材料与当前已知存量，再决定这一轮怎样处理|给已经拿到的这批物品补记自己的记录|按现有物品实际调整一次携带、存放或丢弃，再继续这段活动',


    'c material_stock_review game_recording item_handling_action',


    '无需研究台、配方、木箱或制作成功；明确种类目标才c，现场物料、补记和已有物品处理0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '不编自动识别全部配方或隐藏官方收集清单；物品处理仅用当前实际开放的操作，不要求丢掉有用材料。'))


RAFT_SURVIVAL[3]['variants'].append(_extra(


    '未操船时的实际登岛步行',


    '两种操船情境都不适用，可以答真实登过小岛的一段：木筏已经停稳，你当前能走到岛上一条没看过的坡后，食水暂够返回。你先做什么？',


    '走过没看过的坡后，想亲眼知道遮住的地方是什么|先核对当前食水与已带工具，再决定这一轮怎样活动|排清已有补给、这一小段去向与返回停筏处的安排，再照这趟准备行动|按自己给漂流者设定的沿岸观察者身份，沿近岸走完这一段便回筏，暂不往岛内走',


    'w survival_status_review mission_preparation_plan r',


    '实际步行登岛与两种船具操作有不同前提；未知发现w、角色身份落实行动r，状态/本次准备0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '明确木筏停稳与路段可走，不让未下锚者跳海，不保证每岛有商店、故事或指定资源。'))


RAFT_SURVIVAL[4]['variants'].append(_extra(


    '未潜水抛钩时的岛上砍木',


    '潜水与抛钩情境都没体验过，可以答实际在岛上用斧的一段：斧头和可砍树当前具备，能停手退开，食水暂够返回筏上。你先怎样投入？',


    '专门重复练靠近、挥斧和退开的时点，想把这一项操作练熟|亲手挥这一斧，留意声音、动作与树上变化接着发生的反馈|先核对当前身体与已带补给，再决定这一轮怎样活动|排清取斧、砍这棵树与把已有材料带回筏上的先后，再按这轮安排行动',


    't f survival_status_review physical_tool_action_sequence',


    '第三种确实可用的取物工具；t/f动机明示，单轮工具顺序和查看0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '只用于真实已有斧且树可砍的经历；不保证树种、掉落数、耐久无限或危险全部关闭。'))


RAFT_SURVIVAL[5]['variants'].append(_extra(


    '没有回收或木箱时的已选基础器具',


    '回收交易和木箱收整都没经历过，可以答最早制作菜单的一段：你已选定这一轮做杯子，所需材料已够，物品栏能容纳它。你先怎样继续？',


    '先看杯子已经列出的材料要求，核对这次条件|比较当前材料确实够做的几项基础器具，再决定采用哪项|按已经选定的杯子需求实际制作，以推进这轮目标为重点|直接制作这件当前可做的杯子，亲手体验操作发生',


    'objective_requirement_review compare_production_options stated_objective_progress available_operation_trial',


    '无需木箱、贸易站或回收机；已选目标核对、可做方案比较、推进和普通操作精确0。',


    'RAFT9L_PLAYER RAFT9L_STORE',


    '题面明示实际够做，不能仅用配方已开代替材料足够；不把制作杯子自动推资源经营或收集人格。'))


RAFT_SURVIVAL[6]['variants'].append(_extra(


    '没有涂装搭建时的现成筏上角落',


    '画刷和扩建都没体验过，可以答真实待过的最早甲板：已有的一处角落可以站立，附近的漂流物当前也能取。你先怎样过这一段？',


    '在这处已经熟悉的甲板角慢慢待一阵，喜欢眼前小小住处的安稳感|照我给漂流者设定的惜物习惯，先拾取眼前可拿的一件材料并留在手边|先核对眼前可见漂流物与当前已知材料存量，再决定这一轮怎样处理|给自己已经拿到的物品和当时所在位置补记记录',


    'h r material_stock_review game_recording',


    '不要求建造或上色；熟悉栖居h与身份落实拾取r明示，现场物料/记录0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '只眼前可取的一件，不要求下水；没有凭现成筏的样式推审美，也不假定物资无限。'))


RAFT_SURVIVAL[7]['variants'].append(_extra(


    '没有笔记与净水器时的起始漂流',


    '故事笔记与净水器旁停留都没经历过，可以答真实拿到第一批材料的一段：你仍站在起始木筏，手边已有能存留的物品。你先怎样继续？',


    '先核对已出现的基础玩法说明，再继续自己的实际尝试|照我给漂流者设定的记录员身份，先补记刚拿到的东西，再继续眼前收取|在这片已经熟悉的甲板边慢慢待一阵，享受安稳停留的感觉|只是为已经取得的物品与当时位置补记一份记录',


    'game_reference_first r h game_recording',


    '第三前提不要求任何故事进度或净水器；身份影响先记录再收取才r，普通补记0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '不凭空造开场台词、必须自动出现的任务或Notebook未知笔记；没有叙事经历时不强行计故事偏好。'))


RAFT_SURVIVAL[8]['variants'].append(_extra(


    '真实最早收到的一批漂流材料',


    '料理、净水循环都没有经历过，就回想真实最早拿到木板、叶子或塑料的时段：哪种已经做过的动作更贴近愿意保留的体验？',


    '按自己已见过的材料种类留意缺口，惦记慢慢补进还没有的那类|亲手拿回一份漂流物，喜欢输入与物件靠近眼前相连的反馈|只先看当时眼前可见材料与当前已知存量，再决定那轮怎样处理|只为当时已经拿到的物品补记记录，留下真实经历',


    'c f material_stock_review game_recording',


    '真实过去，无食物生产前提；c明确种类动机，f为亲手取回反馈，物料查看/记录0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '不能把一批漂流物变多算同一对象长期成长，不要求真实钓过任何鱼种。', reflection=True))


RAFT_SURVIVAL[9]['variants'].append(_extra(


    '真实未扩建时留在起始筏上的时段',


    '没有扩建过地基，就回想真实停留在起始甲板上的一段：哪种已经做过的动作更贴近你愿意保留的体验？',


    '在同一处熟悉筏边慢慢待着，喜欢这片小住处的安稳感|按我给漂流者设定的惜物习惯，把已有材料留在手边，暂不制作|只是先核对当时身体状态与已带补给，再决定那轮活动|只是为已经拿到的物品与当时位置补记记录',


    'h r survival_status_review game_recording',


    '无任何扩建前提的真实过去；身份具体影响留料行为r，熟悉停留h，状态/记录0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '不因住在同一张筏便自动推持续养成g，不从开局预制筏形推风格a。', reflection=True))


RAFT_SURVIVAL[10]['variants'].append(_extra(


    '真实未潜水抛钩时的垂钓工具',


    '没有潜水装备或塑料钩经历，就回想真实用过钓竿的一段：哪种已经做过的动作更贴近愿意保留的投入？',


    '反复练过下竿、观察与提线的时点，目的是把这一项操作练熟|亲手提线，喜欢动作、竿线与水声相连的即时反馈|只是排清当时取竿、抛出、提线与收整这轮物品的先后，再亲手做|只是先核对当时身体状态与已带补给，再决定那轮怎样活动',


    't f physical_tool_action_sequence survival_status_review',


    '真实另一工具经历；反复训练与即时感觉各自明示，单轮工具流程和查看0。',


    'RAFT9L_STORE RAFT9L_PLAYER',


    '不以渔获数量、稀有鱼或成功率计能力，也不编套装加成、角色钓鱼技能树。', reflection=True))


RAFT_SURVIVAL[11]['variants'].append(_extra(


    '真实单人用过的研究菜单',


    '联机与独自抛钩的两种情境都不适用，可以回想真实使用研究台的一段：你已有可研究材料，界面也显示过相应条件。哪种真实动作最贴近愿意保留的体验？',


    '以已研究过的材料和已见配方作自己的种类目标，惦记慢慢补缺|按自己给漂流者设定的研究员身份，先把当前能研究的一份材料放入，再继续原来安排|只是核对当时已选配方列出的材料条件，再决定是否推进|只是实际研究一份当时可研究的材料，亲手体验那次操作',


    'c r objective_requirement_review available_operation_trial',


    '第三单人经历无需真人、净水器或抛钩；c和具体身份影响操作r明确，条件查看/普通操作0。',


    'RAFT9L_RESEARCH RAFT9L_PLAYER',


    '不把研究台当真人协作或因果谜题，不承诺一份材料使全部配方开启。', reflection=True))





RAFT_CREATIVE[0]['variants'].append(_extra(


    '尚未放地基时浏览创意构件',


    '两种甲板搭建都没经历过，可以答实际打开过的Creative建造菜单：木筏静止，当前能查看基础地基与墙的样式。你先怎样投入？',


    '挑一组想表达的小屋轮廓与样式，为这张筏定自己的风格|按我给船主设定的独居习惯，先选一处面向外侧的入口再开始搭建|给这一轮定只用地基和木墙的小规则，再照规则尝试|先浏览当前确实开放的构件样式，再决定采用哪种',


    'a r i creative_option_review',


    '不要求已经放置地基；风格、身份落实选入口、自订规则与普通菜单浏览0分开。',


    'RAFT9L_CREATIVE RAFT9L_RENOVATION RAFT9L_PLAYER',


    '只当前菜单确有构件，不许诺所有物品任取、实际能航海或场景已建成。'))


RAFT_CREATIVE[1]['variants'].append(_extra(


    '没有支撑转角经历时的画刷预览',


    '楼层支撑与墙角都没经历过，可以答实际用过的Creative画刷：已取得画刷，当前能查看颜色与图案预览，一处木面确实可涂。你先怎样继续？',


    '选一组自己想表达的颜色与图案，让这个木面有想要的风格|只试改这个木面一项当前可用颜色，亲手看编辑结果|先排清取画刷、选色与涂这一面的顺序，再照这轮流程做|先浏览当前能用的颜色和图案预览，再决定采用哪一种',


    'a creative_edit_trial creative_workflow_plan creative_option_review',


    '另一个真实工具前提，避免重复未经历的支撑与墙角；普通流程、浏览、编辑精确0。',


    'RAFT9L_RENOVATION RAFT9L_CREATIVE',


    '仅实际取得画刷和可涂木面，不把涂色冒充未知支撑原因的检验，也不推所有物体必可涂。'))


RAFT_CREATIVE[2]['variants'].append(_extra(


    '未涂色搭地基时的已有小家具',


    '画刷与基础搭建都没体验过，可以答Creative里实际取过的一件小家具：它当前可放，甲板上有可用位置。你先怎样处理？',


    '为它选一个和自己想表达的生活角风格相合的位置|只实际放下这件当前可放家具，亲手体验操作发生|专门反复练取出、选位与落下同一件家具，把这项工具操作练熟|先浏览当前已开放的家具方案，再决定采用哪种',


    'a available_operation_trial t creative_option_review',


    '第三种原生创意操作；有风格动机才a，有专门反复练操作目的才t，浏览与一项放置0。',


    'RAFT9L_CREATIVE RAFT9L_RENOVATION RAFT9L_PLAYER',


    '只当前可放家具，不造全部物件自由拖动、任意碰撞穿过或创意模式靠装饰包才能解锁。'))


RAFT_CREATIVE[3]['variants'].append(_extra(


    '确实支持镜像的一块建筑构件',


    '前两种木板搭建都不适用，可以答实际用过的Creative镜像构件：当前建筑锤已选中一块确实支持镜像的构件，落点可建。你先怎样玩？',


    '选一个自己想表达的左右轮廓，让这一处带上想要的风格|自己规定这轮只用这块构件与它的镜像接一小段，再按规则玩|只切换这一块当前支持的镜像状态，亲手看预览变化|先排清选构件、切镜像与确认落点的先后，再照这轮流程做',


    'a i creative_edit_trial creative_workflow_plan',


    '原生部分建筑支持镜像；i是自己额外加的构件限制，不是每次切换镜像；普通编辑/流程0。',


    'RAFT9L_RENOVATION RAFT9L_CREATIVE',


    '仅这块题面已明示支持镜像的构件，不把部分支持扩成所有物件，也不承诺新奇形状一定能接成闭环。'))


RAFT_CREATIVE[4]['variants'].append(_extra(


    '没有家具通道或木墙时的斧头拆除高亮',


    '家具通道和木墙转角都没经历过，可以答实际用过的斧头拆除预览：眼前已有一块当前可拆的构件，装备斧头瞄准时会高亮目标。你先怎样继续？',


    '先核对已经可见的高亮目标与拆除说明，再继续自己的尝试|只实际拆下这块当前可拆构件，亲手体验这项操作|排清这次确认目标、拆下与补回当前可用构件的先后，再照这轮施工安排做|按我给船主设定的惜旧习惯，暂留这块旧构件，改到旁边已可建处继续搭',


    'tool_reference_first available_operation_trial construction_action_plan r',


    '拆除高亮有官方更新依据；查看、普通操作、单轮流程0，身份落实保留旧构件r。',


    'RAFT9L_RENOVATION RAFT9L_CREATIVE',


    '目标可拆、旁边可建明示，不保证拆一块不会连带别处，不诱导测试承重或整张筏消失。'))


RAFT_CREATIVE[5]['variants'].append(_extra(


    '创意菜单里确有的物件变体',


    '前两种生活角搭建都不适用，可以答实际浏览过的Creative物件：当前选中物件确有几个可选变体，菜单里已能预览。你先怎样选择？',


    '选一个和自己想表达的筏上风格相合的变体|按我给船主设定的简朴习惯，选最接近原样的一款，暂不添别的装饰|自订这一轮只从这组已开放变体里搭一个小场景，再按规则尝试|只实际切换一个当前可选变体，亲手看预览结果',


    'a r i creative_edit_trial',


    '官方仅部分物件有变体，题面给当前确有；角色落实选简朴款r、自订范围i，普通预览切换0。',


    'RAFT9L_RENOVATION RAFT9L_CREATIVE',


    '不把部分物件变体扩成每件都有，不从所选款式直接推现实性格，不编免费模式仍需搜装饰包。'))


RAFT_CREATIVE[6]['variants'].append(_extra(


    '画刷瞄准已有配色的取色操作',


    '自由观察与基础搭建都不适用，可以答实际用过的Creative取色：画刷已在手，眼前一处已涂木面当前可以瞄准选取颜色组合。你先怎样投入？',


    '取眼前配色再调整一处颜色，让下一面表达自己想要的风格|反复练瞄准、取色与切回预览，专门把这一套工具操作练熟|先浏览当前已能用的配色预览，再决定采用哪种|亲手取这次颜色，留意输入后当前配色马上变化的感觉',


    'a t creative_option_review f',


    '原生Aim-n-Select取色，不是单纯再涂同一面；风格、刻意练习、即时感觉和浏览0分开。',


    'RAFT9L_RENOVATION RAFT9L_CREATIVE',


    '只选取当前已有木面配色，不编图片取色导入、取走别人的颜料或任意面都可涂；一次取色不算t。'))


RAFT_CREATIVE[7]['variants'].append(_extra(


    '单人自由视角里绕现有木筏',


    '真人合作和基础木构件搭建都不适用，可以答真实单人用过的Creative自由视角：已有筏体可以绕着观察，当前不要求你继续添构件。你先怎样过这段？',


    '按我给船主设定的巡看习惯，先绕到入口和舷边看一圈，再回甲板|自订这一轮只从船侧绕看一圈的小规则，再照自己的玩法走完|在熟悉的筏边慢慢看一阵，享受已经安稳的地方|只先查看当前可达入口与通道的现场，再决定怎样继续',


    'r i h scene_inspection',


    '另一原生观察工具前提，身份落实巡看行动r、自订限制i、熟悉停留h，现场查看0。',


    'RAFT9L_CREATIVE RAFT9L_PLAYER',


    '题面限定当前可用自由视角，不能向资源生存强加飞行，不造真人共同目标或地图发布功能。'))


RAFT_CREATIVE[8]['variants'].append(_extra(


    '真实未扩建时的同一面涂装',


    '没有扩过地基，可以回想Creative里真实反复涂过的同一处木面：哪种已经做过的动作更贴近愿意保留的体验？',


    '几次回来接着完善同一面，喜欢先前投入逐渐留在这处布置上|选过自己想表达的颜色与图案，让这一面有想要的风格|明明还能继续改，也会回到这个熟悉角落慢慢待着|只是为已经涂过的颜色与实际步骤补记过程',


    'g a h construction_process_recording',


    '真实同一布置持续完善才g，不要求扩建规模；风格和熟悉停留分开，已有建设步骤记录0。',


    'RAFT9L_CREATIVE RAFT9L_RENOVATION',


    '不以单次换颜色或筏随时间存在算长期积累；不强迫曾用过未开放物件。', reflection=True))


RAFT_CREATIVE[9]['variants'].append(_extra(


    '真实用过可镜像构件的操作',


    '没有处理过支撑或通道，也可以回想Creative里真实用过支持镜像的构件：哪种已经做过的动作更贴近愿意保留的投入？',


    '反复练过选取、切镜像与确认落点的操作，目的就是把工具使用练熟|给那轮自订过只用一块构件及其镜像的限制，再按这个玩法尝试|只是切换过一次当时可用的镜像状态，亲手看那次预览变化|只是先看当时已开放的构件方案，再决定采用哪种',


    't i creative_edit_trial creative_option_review',


    '真实原生镜像操作替代另外两种场景；刻意训练、自订规则与普通编辑/浏览0分开。',


    'RAFT9L_CREATIVE RAFT9L_RENOVATION',


    '不从失败、反复或切换镜像本身推t/i，仅当时确实支持镜像的构件；不让玩家解释虚构物理原因。', reflection=True))


RAFT_CREATIVE[10]['variants'].append(_extra(


    '真实未用装饰构件时的颜色预览',


    '装饰与基础构件菜单都没体验过，可以回想Creative里真实用过的颜色与图案预览：哪种已经做过的动作更贴近愿意保留的体验？',


    '按自己已见的图案种类留意缺口，惦记把想要的一套种类都试过|选过一组自己想表达的颜色，让当前可涂木面呈现想要的风格|只是先浏览当时已可用的图案预览，再决定用哪种|只是给已经用过的图案与位置补记自己的记录',


    'c a creative_option_review game_recording',


    '实际自选图案种类目标才c，表达风格才a；不要求收掉落包，普通浏览/记录0。',


    'RAFT9L_RENOVATION RAFT9L_CREATIVE',


    'Creative预览现成图案不变成稀有掉落；无官方全图案收集奖或全部必可用保证。', reflection=True))


RAFT_CREATIVE[11]['variants'].append(_extra(


    '真实未搭建时的一次自由视角观察',


    '没有自由搭建或最初地基经历，就回想Creative里真实用自由视角看现有木筏的一段：哪种已经做过的动作更贴近愿意保留的投入？',


    '照我给船主设定的巡看习惯，先绕入口和舷边看一圈，再回甲板|给那轮观察定过只从船侧绕一圈的小规则，再照自己的玩法尝试|亲手切换和移动视角，喜欢输入后眼前景物立刻变化的反馈|只是先核对当时已经出现的视角操作说明，再继续自己的尝试',


    'r i f tool_reference_first',


    '另一种真实原生工具经历；身份落实巡看行动r、自订观察限制i、即时感觉f，普通说明核对0。',


    'RAFT9L_CREATIVE RAFT9L_PLAYER',


    '只有当前Creative原生自由视角；不假造资源生存飞行、无人机录像或游戏内上传地图。', reflection=True))





GH_SURVIVAL = [


    Q(1, '动身前的身体与一日补给',


        '当前身体状态与手头食水都能查看，附近有已熟悉的营地与一条没走过的林间去向；没有必须立刻触发的仪式。你先怎样过这一段？',


        '走近没去过的那条林间去向，想亲眼看看转过去是什么|先核对已经显示的身体与食水状态，再决定这一轮怎样活动|排清已有食水、可走路段与回营的先后，再按这趟准备行动|留在熟悉营地慢慢收拾，享受这里已经安稳下来的感觉',


        'w survival_status_review mission_preparation_plan h',


        '真实当前身体与携带补给，不因查看状态就推系统研究或谨慎人格。Tourist/Custom不假定必有营养消耗；未知发现w和熟悉停留h目的明确。',


        'GH9L_STORE',


        ('只经历过最早捡木石也可答：手边已有小木棍和石头，熟悉营地与附近没去过的小路当前都能走。你先怎样继续？',


         '去看看没走过的小路后面是什么，暂不为指定产物而走|只先看当前身体与已带物品的实际状态，再决定这轮怎样活动|排清这一趟带什么、走哪一小段和怎样回营的先后，再按安排行动|留在已经熟悉的地方慢慢待一阵，享受安稳停留的感觉',


         'w survival_status_review mission_preparation_plan h')),


    Q(2, '身体检查里的一只水蛭',


        '这次身体检查已能打开，你在转动肢体时确实看到一只附着水蛭；没有要求判断别的伤口。你先怎样处理？',


        '先核对当前身体上已经可见的状态，再决定这轮怎样处理|实际使用当前可用的移除操作，把这只已见水蛭拿掉|按自己给这次Jake设定的野外工作习惯，决定先处理身体再接哪段活动|先核对已有身体检查与移除操作说明，再亲手继续',


        'survival_status_review available_operation_trial r game_reference_first',


        '明确已见水蛭，普通查看/移除0，不伪装成猜疾病谜题；r须本人赋予角色的习惯影响后续行动。只限游戏实际可用身体检查，不给现实医学建议或猜病能力判断。',


        'GH9L_STORE',


        ('没有遇过水蛭，最早打开身体检查也可答：当前可以转动已显示的手臂或腿查看，不预设你受伤。先怎样做？',


         '先转动肢体查看当前实际显示的身体状态，再决定之后怎么行动|实际尝试这项当前能用的检查操作，亲手体验它怎样发生|按自己给这个Jake设定的检查习惯，决定他接下来怎样安排这一段|先核对已有的检查操作说明，再继续自己的尝试',


         'survival_status_review available_operation_trial r game_reference_first')),


    Q(3, '火边的椰碗与料理',


        '当前营火已经能用，手边有可放的椰碗、可用水与确实能料理的食材；你想给之后一小段活动备些东西。先怎样安排？',


        '把取水、料理、补回食材与下一轮储备接成周转，持续调整食水供给|排清这一次取碗、放水与食材、料理和收回的先后，再亲手照顺序做|只先看手边水与食材的现有状态，再决定这轮怎么处理|亲手放进、拿回一份当前可料理食物，留意火声与器具回应的即时感觉',


        'y physical_tool_action_sequence production_state_review f',


        '持续多轮供给y不同于一次料理顺序0；只采用当前确实可放的水和食材，不造净化效果、药用配方、营养数或有毒食材可放心吃的保证。',


        'GH9L_STORE GH9L_CHALLENGE_PLAYER',


        ('只做过最早营火也可答：当前能用的点火工具、干燥引火物和火堆都具备。你先怎样投入？',


         '排清取工具、放引火物与开始点火的先后，再亲手按顺序做|只先查看当前引火物与手头材料状态，再决定这次怎么处理|先核对已经可用的点火操作说明，再继续自己的尝试|亲手做这次已可进行的点火，留意动作与火光出现紧接着发生的反馈',


         'physical_tool_action_sequence production_state_review tool_reference_first f')),


    Q(4, 'Notebook里已列出的基础制作',


        '你正想制作一项普通工具或构件，Notebook已经显示它的材料要求，现有材料够做，操作当前可用。你先怎样继续？',


        '先核对已经列出的配方与手边材料，确认这次条件|实际制作这一件当前可做的东西，亲手体验这次操作|排清这一轮取料、制作与收回余料的先后，亲手照顺序做|按当前已选的一项工具或构件目标推进，重视把眼前需求接上',


        'objective_requirement_review available_operation_trial physical_tool_action_sequence stated_objective_progress',


        '已列明配方不计p；普通核对、制作、一次流程和既定目标都用精确0。无假配方数、跳过解锁、VR手势或现实制作知识要求。',


        'GH9L_STORE GH9L_BUILD GH9L_CHALLENGE_PLAYER',


        ('只有最早的石与木棍也可答：当前确实已能制作一项基础工具，所需材料手边够。你先怎样做？',


         '先查看当前已开放的基础配方与材料条件，再决定这次采用哪一项|直接制作这件当前可做的基础工具，亲手体验操作发生|排清这次取料、制作与收回手头物品的先后，再照顺序做|按当前已选定的这一项工具需求推进，把眼前目标接上',


         'compare_production_options available_operation_trial physical_tool_action_sequence stated_objective_progress')),


    Q(5, '雪橇、木料与上层平台',


        '当前已有能用的雪橇、材料架和升降机，下方有确实能取的重料，上层平台也已能到达。你先怎样安排这处运输？',


        '把取料、雪橇往返、上送与存放接成多轮供给，持续调整上下层周转|排清这一次装料、拉到升降机、上送与收整的先后，再亲手照顺序做|只先看当前已有木料与架上库存，核对这一轮实际状态|亲手装卸、拉动一趟雪橇，留意输入与重物移动紧接着发生的感觉',


        'y physical_tool_action_sequence material_stock_review f',


        'y需持续多轮资源供给，不把一次搬重物当经营人格。当前设备全部给足才使用；架与雪橇不假定能装任意东西，升降机不是自动全基地物流。',


        'GH9L_TRANSPORT',


        ('没用过雪橇或升降机，可答最早用手搬营地木料：眼前木料能取，已有一处能放的空位。你先怎样处理？',


         '排清这次取起、搬到空位与放下的先后，再亲手照顺序做|只先看眼前已有木料与空位状态，再决定这轮怎样处理|实际搬起并放下一份当前能取的木料，亲手体验这次操作|亲手搬动，留意重物随输入移动与落下的即时反馈',


         'physical_tool_action_sequence material_stock_review available_operation_trial f')),


    Q(6, '工作台后的第一组装饰',


        '当前已有装饰工作台、能用的画刷与颜料，也有可制作或移动的家具；这段时间不急着出门。你先怎样安排营地这一角？',


        '选一组自己想表达的颜色与摆设，让这个营地有自己的风格|按自己给Jake设定的生活与工作习惯，决定桌椅和物件该怎样安放|只移动一件当前可调整的家具，亲手看看这次编辑结果|回熟悉火边慢慢待一阵，享受已经安稳生活过的这片地方',


        'a r creative_edit_trial h',


        '只当前已有工作台、颜料和家具，不要求后期大屋。风格a、身份影响行动r、普通移位0与熟悉栖居h分开，不从配色推现实人格。',


        'GH9L_DECOR',


        ('还没有这些装饰，只有最早已能搭的小庇护所也可答：当前几段构件与材料可用，能调整这一小处位置。你先怎样玩？',


         '把这一小处搭成自己想表达的形状，让营地有自己选定的感觉|按自己对Jake的习惯设定，决定他第一处住处要落在哪里|只实际调整一项当前可放构件的位置，亲手查看这次变化|留在已经熟悉的小营地慢慢待一阵，享受安稳停留',


         'a r creative_edit_trial h')),


    Q(7, '永恒火焰的可选波次',


        '只限你实际玩过的无尽生存世界：永恒火图腾当前已能开，所需材料齐备，仪式已启动，确有敌人波次接近。你想把这一轮用在哪里？',


        '专门反复练已有武器的瞄准、投掷或退步时点，想把操作练熟|比较手头两组确实可换的武器与护具搭配，在本轮检验组合效果|排清这轮接敌、出手、停手恢复与再次接近的循环，再照安排尝试|按当前已经出现的守火目标行动，以推进这一轮目标为重点',


        't b combat_resource_cycle stated_objective_progress',


        '只问无尽生存实际已可启动且出现波次的原生活动；本体Story不可制作仪式草药，Story玩家或未触发者换早期ALT。t是刻意练，b比较检验两组，准备/已列目标0；不要求50阶段、奖励武器或必胜。',


        'GH9L_FLAME GH9L_STORE GH9L_FLAME_BOUNDARY',


        ('没有参加守火活动，最早用工具砍营地旁的木料也可答：当前斧头可用，周围有停手与退步空间。你先怎样投入？',


         '反复练一小段挥斧与退步时点，专门把这项操作练熟|亲手砍一轮，喜欢声音、木料变化与输入接连发生的反馈|排清这一轮挥斧、退到旁边恢复与再靠近的先后，再照安排尝试|先推进已选定的一份营地木料需求，把眼前目标接上',


         't f tool_operation_plan stated_objective_progress')),


    Q(8, '本体中刚听过的Mia通话',


        '本体故事里你刚实际听过一段与Mia的通话，当前可以先留在已有营地，也可以接着走；这里没有要你猜正确剧情答案。你先想做什么？',


        '回想刚听过的话，把人物关系与之前经历的线索接起来，想理解Jake正在经历什么|按自己给这次Jake赋予的立场，决定他听完后要先照顾营地还是继续寻找|离开熟路去看一处当前可达但没走过的林间去向，想亲眼发现那边是什么|先给这段已经实际听到的人物信息与地点补记记录',


        's r w game_recording',


        '仅实际经历过的本体通话；不把SoA或无尽玩家假设已听Mia，不造可回放界面或额外剧情分支。故事理解、本人角色行动与未知发现分开，补记0。',


        'GH9L_STORE',


        ('只玩无尽、或没留意通话，可以答最早营地的一段：手头木石能做一项已开放小工具，熟悉火边可停留。你先怎样过这段？',


         '直接做这件当前可做的小工具，亲手体验这次操作|按自己给Jake设定的野外生活习惯，决定先收整哪些手头物件|回熟悉火边慢慢待一阵，享受这个小营地已经安稳的感觉|先查看当前已开放配方与手边材料条件，再决定采用哪种',


         'available_operation_trial r h compare_production_options')),


    Q(9, '真实照料过的动物圈',


        '回想你真实照料过的动物圈或种植处：哪种已经做过的投入，最接近你愿意保留的体验？',


        '多次回到同一群动物身边喂水、添食与清理，喜欢信任和先前投入慢慢留下变化|把饲料、水、清理和产出接成多轮周转，持续调整营地供给|按自己已见过的可养或可种种类留意缺口，惦记慢慢补进未留住的那一类|只是先核对当时实际可见的动物、作物或材料状态，再决定那轮怎样处理',


        'g y c production_state_review',


        '真实过去，持续同一对象g、周转系统y、种类c与查看0分开。更新20已扩动物，不将最初三种误作全部；不要求繁育成功、投喂数量或刷信任。',


        'GH9L_ANIMALS GH9L_ANTEATER GH9L_STORE',


        ('还没有养殖或种植，就回想真实最早搭过的小营地：哪种已经发生的投入，最接近愿意保留的体验？',


         '后来多次回来接着添东西，喜欢先前投入逐渐留在同一处营地|把取水、料理与补回储备接成几轮周转，喜欢持续调配生活供给|按自己已见材料的种类留意缺口，惦记慢慢补进还没有的那一类|只是先看当时手头材料与可见存量，再决定那一轮怎么处理',


         'g y c production_state_review')),


    Q(10, '真实留在营地里的时段',


        '回想一次你真实搭建或停留过的营地时段：哪种已经做过的动作，最接近你愿意留住的体验？',


        '调整过构件、家具或颜料，让它表达自己想要的营地风格|明明还有别处可去，仍回到熟悉火边慢慢待着|按自己给Jake设定的经历和生活习惯，决定营地里要怎样安放物件|只是为已经搭过的构件与连接补记过程，保留建设记录',


        'a h r construction_process_recording',


        '真实过去的风格、熟悉栖居与身份影响行动；普通记录0。小庇护所也可，不用树屋、水上大屋、审美好坏或现实野外身份作考核。',


        'GH9L_STORE GH9L_BUILD GH9L_DECOR',


        ('只搭过最早的小庇护所，就回想当时真实发生过的动作：哪种最贴近你愿意保留的投入？',


         '把这几段构件摆成自己想表达的小小形状|在已经熟悉的火边与小庇护所之间慢慢待一阵|照自己给Jake设定的习惯，决定第一处住处要怎样安排|只给已经放过的构件与步骤补上一份记录',


         'a h r construction_process_recording')),


    Q(11, '真实练过或比较过的出手',


        '回想你真实用过已有矛、弓或工具的一段：哪种已经做过的投入，最接近你愿意留住的体验？',


        '专门重复过一小段瞄准、投掷或退步，目的是把这一项操作练熟|比较过当时确实可换的两组武器与护具搭配，再检验组合带来的差异|亲手使用工具或武器，喜欢动作、声音与眼前变化接连发生的反馈|只是先比较当时已经拥有的装备与组件，再决定那段怎么安排',


        't b f compare_available_setup',


        '真实过去的刻意练习与组合效用各自明示，普通浏览0；不凭武器种类推现实偏好，不把固定一击击杀、装备品质或实际技术作为证据。',


        'GH9L_STORE GH9L_CHALLENGE_PLAYER',


        ('没有矛或弓经历，就回想真实用最早斧头砍木的一段：哪种已经做过的投入，更贴近你愿意保留的体验？',


         '反复练过挥斧与退步的时点，想把这一项操作练熟|亲手砍木，喜欢声音、材料变化与输入相连的即时反馈|只是排清当时取斧、砍木与收整材料的先后，再亲手做那一轮|只是先核对当时身体与已带补给的实际状态，再决定怎么活动',


         't f physical_tool_action_sequence survival_status_review')),


    Q(12, '真实同游时的林间安排',


        '回想一次确有其他真人同玩的时段：有人想先补营地，有人想继续探索。哪种你真实做过的动作，最接近愿意保留的体验？',


        '先谈清大家这轮共同想完成什么，商量留营、探索与再集合的安排|先陪同伴走走、聊眼前看到的东西，喜欢一起待在丛林里的陪伴|问过愿意参加的人，约定这一轮只在河边收集的一条自订规则再一起玩|只为已经参与的营地建设与实际步骤补记过程',


        'q o i construction_process_recording',


        '仅真人实际经历；q协商共同目标，o陪伴，i自订且同意。单人有独立ALT，不拿部落NPC当真人，也不保证各玩家剧情/物品进度同属。',


        'GH9L_STORE',


        ('只有单人经历，就回想真实一个人在最早营地旁活动的时段：哪种已经做过的动作更贴近愿意保留的部分？',


         '去没走过的林缘看看，想亲眼知道那边是什么|给那一轮加过只在河边拾取的小规则，再按自己的玩法尝试|回到熟悉火边与小庇护所慢慢待一阵，享受安稳停留|只为已经拿到的物品与实际走过的地点补记记录',


         'w i h game_recording')),


]





GH_SURVIVAL[0]['variants'].append(_extra(


    '当前可用手表与已经取得的地图',


    '营地出门和最早拾物两种情境都不适用，可以答实际导航的一段：手表已能用，一张当前区域地图已取得，眼前有可走但没看过的林间支路。你先怎样继续？',


    '先核对地图与手表当前实际显示的位置资料，再决定这一段往哪里走|走近没看过的支路，想亲眼知道转过去有什么|按我给Jake设定的记录员习惯，先记下已显示坐标，再沿可走方向继续|只为自己已经走过的位置补记一份记录',


    'navigation_information_review w r game_recording',


    '第三前提是实际取得地图与手表，不默认开局地图或自动玩家标记；未知发现和身份落实记坐标行动分开，导航/记录0。',


    'GH9L_STORE GH9L_SOA1',


    '仅当前物品实际显示的信息；不借Mia剧情、部落地图或保证任何固定坐标有资源。'))


GH_SURVIVAL[1]['variants'].append(_extra(


    '没做身体检查时的背包取放',


    '有水蛭和无伤检查都没经历过，可以答真实打开背包的一段：手头已有可存取的小物件，当前无须判断身体伤口。你先怎样继续？',


    '先核对当前身体与已带补给的实际状态，再决定这轮怎样活动|实际取出再收回一件当前可存取物品，亲手体验这项操作|按我给Jake设定的收整习惯，先把眼前小物件收回背包，再继续可走路段|先核对已经出现的物品操作说明，再继续自己的尝试',


    'survival_status_review available_operation_trial r game_reference_first',


    '另一种实际界面操作，不强求身体检查；身份落实先收整再动身r，普通查看/取放/说明0。',


    'GH9L_STORE',


    '不造自动整理按钮、无限容量或背包免重量，不从检查或整理推现实人格。'))


GH_SURVIVAL[2]['variants'].append(_extra(


    '没有料理点火经历时的石制小工具',


    '料理和点火都还没经历过，可以答实际用过的基础制作：当前已有木棍、石头与够用材料，一项已开放小工具确实可做。你先怎样投入？',


    '排清这次取料、制作与收回余料的先后，再亲手照顺序做|只先看当前制作材料与已有存量，再决定这轮怎样处理|直接做这件当前可做工具，亲手体验操作发生|先核对当前已经出现的制作说明，再继续自己的尝试',


    'physical_tool_action_sequence production_state_review available_operation_trial tool_reference_first',


    '第三前提不用营火、椰碗；单轮实体工具流程、制作状态、操作、说明均精确0。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '不编精确配方数量或默认所有工具已解锁，材料足够与当前可做由题面明确。'))


GH_SURVIVAL[3]['variants'].append(_extra(


    '没有制作经历时的散落小材料',


    'Notebook制作与最早石器都没经历过，可以答实际收集的一段：眼前小木棍或石头可取，手头已有部分材料，背包能容纳这次拾取。你先怎样处理？',


    '先核对眼前实际可见的材料与当前已知存量，再决定这一轮怎样处理|实际拿起一件当前能取的小材料，亲手体验这次操作|把自己已见材料种类作一个小收藏目标，惦记还缺哪一类|只给已经拿到的这件材料与发现位置补记记录',


    'material_stock_review available_operation_trial c game_recording',


    '不要求制作或Notebook已解锁；明确种类动机c才计收集，物料查看、拾取、补记0。',


    'GH9L_STORE GH9L_NOTEBOOK',


    '没有把现成拾取变成谜题、生产系统或成长，没有猜未显示配方要求。'))


GH_SURVIVAL[4]['variants'].append(_extra(


    '未搬重木时的背包小物件',


    '雪橇升降机和手搬重木都没经历过，可以答实际收整背包的一段：已有可存取的小木棍或石头，当前不需搬运重料。你先怎样处理？',


    '按现有物品实际调整这一轮携带、存放或丢弃，再继续自己的安排|先核对眼前可见材料与当前已知存量，再决定这一轮怎样处理|排清这次取出、处理与收回手头物件的先后，再亲手照顺序做|亲手取出或收回一件已有物品，留意输入与它移动相连的反馈',


    'item_handling_action material_stock_review physical_tool_action_sequence f',


    '不同负载与操作前提的背包取放；普通处理、物料与单轮流程0，仅明确即时反馈f。',


    'GH9L_STORE GH9L_TRANSPORT',


    '不承诺重物进普通背包，不造自动全营地物流，不把一次取放计持续系统经营。'))


GH_SURVIVAL[5]['variants'].append(_extra(


    '没有家具庇护所时的一处小火堆',


    '家具和小庇护所都没体验过，可以答实际放过的营火蓝图：当前已开放这项构件、材料够，地面上有确实可放的位置。你先怎样安排？',


    '选一个和自己想表达的营地轮廓相合的位置，先把这一小角做出想要的感觉|按我给Jake设定的营地习惯，把火堆留在当前可放的角落，先收整近处工具|只试调一项当前可用蓝图的位置，亲手看这项编辑结果|在自己已熟悉的落脚处慢慢待一阵，享受安稳停留',


    'a r creative_edit_trial h',


    '只用确实开放且可放的基础蓝图，不要求房屋家具；风格、角色具体行动、普通编辑0与熟悉停留分开。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '不编任意角落都可点火、无雨水影响或具体地形必能建造；这是一项当前可放条件。'))


GH_SURVIVAL[6]['variants'].append(_extra(


    '没有波次砍木经历时的制作菜单',


    '守火波次和砍木都没体验过，可以答真实制作过的一件小工具：当前工具配方已开，已有材料够用，本轮目标也已选定。你先怎样继续？',


    '先看当前工具列出的材料要求，核对这次条件|直接制作这一件当前可做工具，亲手体验操作发生|排清取料、制作与收回手头物件的先后，再按这一轮顺序做|按已选工具目标实际制作，以推进眼前目标为重点',


    'objective_requirement_review available_operation_trial physical_tool_action_sequence stated_objective_progress',


    '无战斗要求的第三前提；已知条件下四种普通动作均精确0，不借未体验战斗推练习/组合或竞争。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '不把主菜单七项Challenges、无尽世界仪式与Story混为同一规则；仅当前实际可制作的一件。'))


GH_SURVIVAL[7]['variants'].append(_extra(


    '没有通话制作经历时的地图路口',


    'Mia通话和基础制作都没经历过，可以答真实用过地图的一段：地图已取得，手表当前可看，附近有一条能走却没看过的去向。你先怎样过这段？',


    '先核对地图和手表当前实际显示的位置资料，再决定下一段往哪里走|去看看没走过的去向后面是什么，暂不为指定材料而走|按我给Jake设定的记录员身份，先记下已显示坐标，再沿可走方向继续|只是给已经走过的地点补记记录，留下这段真实经历',


    'navigation_information_review w r game_recording',


    '无剧情通话、配方或营火前提；未知发现、身份具体行动与导航/记录0分开。',


    'GH9L_STORE GH9L_SOA1',


    '只题面已取得地图和当前真实可看手表，不编自动地图定位、Mia台词或保证NPC所在坐标。'))


GH_SURVIVAL[8]['variants'].append(_extra(


    '真实没有营地经营时的最早拾物',


    '没有养殖种植或反复完善营地的经历，就回想真实最早拾到木棍或石头的一段：哪种已经做过的动作更贴近愿意保留的体验？',


    '把自己已经见过的材料种类作一个收藏目标，惦记慢慢补进缺的那类|亲手拿回一件材料，喜欢物件与输入相连的即时反馈|只是先核对当时眼前可见物料与当前已知存量，再决定那轮怎样处理|只是实际调整过已有物品的一轮携带、存放或丢弃，再继续活动',


    'c f material_stock_review item_handling_action',


    '真实过去，不要求养殖或住所；无同一对象持续投入就不硬计g，无多轮周转就不硬计y。',


    'GH9L_STORE',


    '种类目标必须由玩家明确选项表达，不从拿东西多或背包满推收集人格。', reflection=True))


GH_SURVIVAL[9]['variants'].append(_extra(


    '真实还没有住处时的丛林停留',


    '没有搭营地或庇护所，就回想真实最早能自由走动的一段：哪种已经做过的动作更贴近愿意保留的体验？',


    '沿着还没看过的林缘走一小段，想亲眼知道那边是什么|在自己已经走熟的一小处慢慢停留，喜欢熟悉地方的安稳感|按我给Jake设定的野外记录习惯，先记下已走到的位置，再继续可走路段|只是先核对当时身体状态与已带补给，再决定那轮活动',


    'w h r survival_status_review',


    '无住处要求的真实移动经历；未知发现w、熟悉停留h、身份落实记录再动身r，状态0。',


    'GH9L_STORE',


    '不凭预制地形推风格，不编Jake自动生成日志或有额外职业；角色设定由玩家本人赋予。', reflection=True))


GH_SURVIVAL[10]['variants'].append(_extra(


    '真实没用武器斧头时的背包操作',


    '没用过矛弓或斧头，就回想真实打开背包取放物品的一段：哪种已经做过的动作更贴近愿意保留的投入？',


    '反复练过取出、选位和收回同类物件的操作，目的就是把工具界面用熟|亲手取出与收回物件，喜欢输入与眼前移动相连的反馈|只是排清当时取出、处理和收回的先后，再照这一轮顺序做|只是先核对当时已经出现的物品操作说明，再继续尝试',


    't f physical_tool_action_sequence tool_reference_first',


    '真实另一操作前提，无战斗或砍木；刻意练习须明确，普通顺序/说明0，不凭普通重复自动推练习。',


    'GH9L_STORE',


    '仅当前实际可用背包操作，不编自动整理、无限空间或物品随意旋转的功能。', reflection=True))


GH_SURVIVAL[11]['variants'].append(_extra(


    '真实单人未建营时的开头收集',


    '没有联机或营地活动，就回想真实最早一个人在丛林拾材料的一段：哪种已经做过的动作更贴近愿意保留的体验？',


    '给那轮定过只在眼前这段河岸拾取的小规则，再照自己的玩法尝试|亲手拿起当时可取的一件小材料，喜欢动作与物件靠近相连的反馈|按我给Jake设定的惜物习惯，先把眼前可拿的一件小材料收进背包，再继续走|只是为已经拿到的物件与当时位置补记记录',


    'i f r game_recording',


    '第三单人前提无需建营或火堆；自订范围、身份落实收物与即时反馈明示，普通补记0。',


    'GH9L_STORE',


    '不造同伴、NPC商量或可保证全部河岸安全；自订规则不是官方挑战模式。', reflection=True))





GH_SOA = [


    Q(1, '村长信任与眼前两项援助',


        '《亚马逊之魂》中你已见并交谈过Mu’agi村长，当前已能查看这支部落的信任进度；附近一名猎人的状态已经实际检查过、所需物件当前已有，旁边也有还没看过的路段。手头补给够短途返回。你先做什么？',


        '先回看当前已显示的部落任务与信任进度，核对自己已经做到哪一步，再决定这轮怎样继续|先去看看没走过的路段，想亲眼知道那里是什么|按我给Jake设定的部落援助者身份，带当前已有的所需物件先去猎人那里|排清已有补给、去猎人处与返回落脚点的安排，再照这趟准备行动',


        'quest_progress_review w r mission_preparation_plan',


        '专属于前传的信任/援助与未知探索取舍。NPC援助不是与真人协商q，角色身份落实带物先救助r；目标要求与一次准备0。',


        'GH9L_SOA1 GH9L_SOA2 GH9L_SOA_PLAYER GH9L_SOA_UI',


        ('还没见村长，可答前传实际最早自由活动的一段：当前林缘有没走过的去向，手边已有能携带的小材料。你先怎样继续？',


         '去看看还没走过的林缘，想知道转过去会出现什么|先核对当前身体状态与已有补给，再决定这轮活动|按我给Jake设定的记录习惯，先记下已走到的位置再继续|只为已经拿到的材料与实际走过的位置补记记录',


         'w survival_status_review r game_recording'),


        '仅本次当前可援助且所需物件已有的猎人，不规定治疗配方、信任数字、解锁阈值或现实医疗动作。'),


    Q(2, '传奇石画与Notebook线索',


        '一个部落传奇所需的石画线索你已全部读到，Notebook能回看，但传奇还未完成；你对解法有一个尚未验证的解读，附近确有能尝试的行动。你先怎样投入？',


        '把自己的解读当作可能出错的猜想，只试一项对应行动，再核对传奇是否有变化|回看已经读到的传奇，把它讲的人和事件与前后线索接起来|沿石画旁没走过的小路看看，不为这次传奇答案而走|只为已经读过的传奇与位置补记记录',


        'p s w game_recording',


        '真实传奇的线索解读与可失败验证p，叙事联系s、未知发现w与补记0分开；不是把已列材料复述当谜题。',


        'GH9L_SOA1 GH9L_SOA2 GH9L_SOA_PLAYER GH9L_SOA_UI',


        ('还没凑到多段线索，实际只读过一块传奇石画也可答：文字能回看，旁边有可走但没看过的林间去向。你先做什么？',


         '再读已见文字，想理解这段传奇中的人和事件|去看看没走过的林间去向，暂不为找指定石画而走|按我给Jake设定的记录员身份，先记下已见石画的位置再继续|只是给这段已读文字与位置补上一份记录',


         's w r game_recording'),


        '不编某传奇的隐藏解法、必须获得的物品或必成功结果；没有足够线索时ALT不硬计p。'),


    Q(3, '已找到的孩子与回村一段路',


        '你在前传确实遇到可带回村的孩子，当前已经能抱起，回去的路段可走，身上补给够这一趟。你先怎样继续？',


        '排清抱起前的已有补给、这段回村去向与到村后的收尾，再照这趟准备行动|实际抱起这个当前可带走的孩子，亲手体验这项操作|按我给Jake设定的护送者身份，先把孩子带回已知村落，暂不绕去探索|只先核对当前已经显示的援助目标与条件，再决定这轮怎样推进',


        'mission_preparation_plan available_operation_trial r quest_progress_review',


        '前传带孩子回村的真实具体目标；护送角色影响路线取舍r，普通目标、操作、单次准备0。',


        'GH9L_SOA_PLAYER GH9L_SOA1 GH9L_SOA_UI',


        ('没有带过孩子，可以答实际先找到受伤猎人的一段：你已经实际检查过他这次的状态，并选定一份确实可用的游戏物品，物件当前在手边。你先怎样继续？',


         '先看自己当前身体状态与已带补给，再决定这一轮怎样活动|实际给出当前这份可用物件，亲手体验一次游戏内援助操作|按我给Jake设定的援助者身份，先完成眼前这次帮助，暂不去下一条路|按已经出现的这次援助目标给出选定物件，把眼前目标推进',


         'survival_status_review available_operation_trial r stated_objective_progress'),


        '孩子和猎人都是NPC；没有协商真人共同目标证据，不计q/o，不虚构无敌护送或数值奖励。'),


    Q(4, '第二片区域的污染水源',


        '前传第二片区域里你已找到实际污染水源；当前可取的废弃瓶子已看见，清理与焚烧所需材料够，相关操作已开放。你先怎样安排？',


        '排清这一次收集废弃物、补齐当前火堆与点燃的先后，再按这轮流程做|亲手取起一件当前能取的废弃物，留意输入与眼前变化相连的反馈|按我给Jake设定的河岸照料者身份，先清理这处已见废弃物，暂不往下一段走|先查看已显示的清理要求与已有材料，核对这轮条件',


        'physical_tool_action_sequence f r objective_requirement_review',


        '真实前传污染水源活动；普通实体工具流程0、反馈f与角色身份落实先清理r明确。不是把官方已说明的焚烧流程当因果谜题。',


        'GH9L_SOA2 GH9L_SOA_PLAYER',


        ('还没到污染水源，可以答第一片区域实际发现部落遗体的一段：当前已有可用刃具，已有能完成当前处理的材料与操作。你先怎样安排？',


         '先核对已列材料要求与现有物品，再决定这一轮是否推进|排清这次使用刃具、收取当前材料与完成处理的先后，再亲手做|按我给Jake设定的尊重部落习俗身份，先完成这次处理，暂不继续赶路|按已经显示的这次处理目标行动，以推进眼前目标为重点',


         'objective_requirement_review physical_tool_action_sequence r stated_objective_progress'),


        '只游戏内已开放且当前确实可做的清理/遗体活动；不输出真实污染处理方法，不保证具体耗时或水必能直接喝。'),


    Q(5, '捕鱼部落的破损图腾',


        '你已到前传捕鱼部落所在区域，发现一座确实可修的破损图腾；所需材料已显示，手边有能交进这一轮的一部分。你先怎样继续？',


        '先核对图腾列出的材料与现有存量，再决定这一轮怎样推进|排清这次取料、带到图腾与交进构件的先后，再亲手照顺序做|按我给Jake设定的修复者身份，先把已有材料交进这座图腾，暂不去别的活动|直接交入一份当前可用材料，亲手体验这次操作',


        'objective_requirement_review physical_tool_action_sequence r available_operation_trial',


        '专属前传修图腾，未说材料全齐或任意图腾可改外观；身份具体影响先修r，普通要求/一次流程/交入0。',


        'GH9L_SOA3 GH9L_SOA_PLAYER',


        ('还没修图腾，可以答实际遇到捕鱼部落渔民的一段：他需要的游戏物品已可查看，你当前有一份确实可交的物件。你先怎样继续？',


         '先查看当前显示的渔民需要与已有物品，再决定这轮交什么|实际交出当前这份合用物件，亲手体验游戏内援助操作|按我给Jake设定的沿河援助者身份，先完成眼前这次交付，暂不去新地点|按已经列出的渔民需要交付，把当前这次目标推进',


         'objective_requirement_review available_operation_trial r stated_objective_progress'),


        '只实际已显示的物品要求，不给未确认的伤者活动全区域存在保证，不将NPC交付当真人协作。'),


    Q(6, 'Mu’agi仪式里的水滴与猎人',


        'Mu’agi仪式已经解锁并开始，你实际能拾取大水滴、带到植物处，场内也有需要守护的受伤猎人。你先怎样投入这一轮？',


        '反复练拾水、移动与交水的操作时点，专门把这一项练熟|排清这一轮取水、送到植物与再看猎人处境的先后，再照当轮流程做|亲手搬送这滴水，留意动作、场景与输入相连的反馈|按当前已显示的仪式目标行动，以推进这一轮目标为重点',


        't physical_tool_action_sequence f stated_objective_progress',


        '前传真正的仪式动作，不拿无尽守火波次代替；刻意训练、即时反馈与单轮顺序/目标0分开。',


        'GH9L_SOA3 GH9L_SOA_PLAYER',


        ('没有进过仪式，可以答实际回看村长与部落进度的一段：Notebook当前可用，已有几项你真实做过的援助。你先怎样投入？',


         '回看已经听过的部落人物与事件，想把这段经历接起来|先核对当前已经显示的部落任务与进度，确认已经做到哪一步，再决定这轮怎样继续|按我给Jake设定的援助者身份，先去完成一项当前能做的已列援助|只为已经做过的援助与见过的人物补记记录',


         's quest_progress_review r game_recording'),


        '仪式已解锁才问；不用信任阈值、植物生长必成功或猎人无敌保证，不从一局浇植物推长期养成。'),


    Q(7, 'Un’garaca仪式的动物与指定武器',


        'Un’garaca仪式已经解锁并开始，当前石上显示了目标动物与对应武器类型，你也已拿到这一轮可用武器。你先怎样投入？',


        '先核对眼前已显示的动物与武器要求，再决定这轮怎样执行|专门反复练这一种武器的瞄准与出手时点，想把操作练熟|亲手完成当前一次可用出手，喜欢动作、声音与场景回应紧接着发生|排清接近、出手、退开和恢复后再接近的循环，再按当轮安排尝试',


        'objective_requirement_review t f combat_resource_cycle',


        '真实仪式有指定类型，不编自由两套build对比；明确练习t、反馈f，要求核对与本轮资源循环0。',


        'GH9L_SOA3 GH9L_SOA_PLAYER',


        ('没有进过仪式，可以答前传里实际用过的最早斧头：斧头当前能用，眼前木料可砍，周围有退开和恢复的空间。你先怎样投入？',


         '反复练挥斧和退步的时点，专门把这一项操作练熟|亲手砍这一轮，喜欢声音与木料变化接着发生的反馈|排清靠近、挥斧、退开恢复与再靠近的先后，再照安排尝试|先核对当前身体与已带补给，再决定这轮怎样活动',


         't f tool_operation_plan survival_status_review'),


        '没有强行要求狩猎成功、固定伤害、猎物刷新或所有难度都有敌人；未进仪式有日常工具替代。'),


    Q(8, 'Habbacu仪式里的鱼群与气泡',


        'Habbacu仪式已经解锁并开始，你实际能在水下取目标颜色的神秘鱼，场内也看得到危险鱼群和可用气泡。你先怎样投入？',


        '反复练接近、取鱼与利用气泡的操作时点，想把这一段操作练熟|排清这一轮靠近目标、避开已见鱼群与回到可用气泡的先后，再照安排尝试|亲手游这一段，留意移动、声音与水下场景紧接着发生的反馈|先核对当前已显示的氧气与自身状态，再决定这一轮行动',


        't mission_preparation_plan f survival_status_review',


        '前传具体水下仪式，不与普通捕鱼或VR混用；刻意训练、反馈和单次路线/状态0分开。',


        'GH9L_SOA3 GH9L_SOA_PLAYER',


        ('没有进过水下仪式，可以答前传实际用过的手表和地图：地图已取得，当前显示的位置信息可查看，附近有尚未走过的可达林缘。你先怎样继续？',


         '先核对当前地图和手表实际显示的位置资料，再决定往哪里走|走近没看过的林缘，想亲眼知道那边是什么|按我给Jake设定的记录习惯，先记下已显示坐标再继续可走路段|只为已经走到的位置补记一份记录',


         'navigation_information_review w r game_recording'),


        '仅已经可用气泡和已显示氧气，不规定颜色数量、游法最优或保证不会被咬；地图不假定开局自带。'),


    Q(9, '真实修过的船上无线电',


        '回想前传里真实发现船、找回天线或修好无线电后报告基地的一段：哪种已经做过的投入更贴近愿意保留的体验？',


        '回听或回想已经听到的报告，把Jake这趟早期经历与后来知道的事接起来|按我给Jake设定的记录员身份，先整理已见船与报告信息，再继续这次旅程|只是先核对当时已经显示的修复要求与已有物件，再决定是否推进|只是为实际见过的地点、已取得物件和听到的信息补记记录',


        's r objective_requirement_review game_recording',


        '真实前传天线/船无线电，非本体Mia通话也非主菜单Radio挑战；叙事联系s、身份落实记录再走r与要求/补记0分开。',


        'GH9L_SOA_PLAYER GH9L_NOTEBOOK',


        ('没有船上无线电经历，可以回想前传实际听过的村长或读过的传奇文字：哪种真实投入更贴近愿意保留的体验？',


         '回看已读文字，把它讲的人和事件与前后经历接起来|按我给Jake设定的记录习惯，先记下已读传奇与所在位置，再继续这段活动|只是先核对当时已出现的基础玩法说明，再继续自己的实际尝试|只是为已读文字、已见人物和位置补记记录',


         's r game_reference_first game_recording'),


        '不编具体对话台词、最终剧情解释、基地承诺或自动记录功能，只回想自己实际听读过的内容。'),


    Q(10, '真实一点点留下的部落信任',


        '回想你在同一前传存档里多次回到同一支部落、做援助并看到信任进度留下变化的时段：哪种真实投入更贴近愿意保留的体验？',


        '几次回来接着帮助同一支部落，喜欢先前投入逐渐留在这段信任进度上|按自己已见传奇或援助类别留意缺口，惦记慢慢补完想要的一套种类|只是先看当时已显示的部落任务与进度，确认已经做到哪一步，再决定那轮怎样继续|只是为已经完成的援助和见过的人物补记记录',


        'g c quest_progress_review game_recording',


        '真实同一存档/部落进度持续积累才g，明确种类补齐才c；并非每次交付自动养成，不凭NPC功能计真人社交。',


        'GH9L_SOA1 GH9L_SOA_PLAYER',


        ('只有最早一次援助、尚无反复回村经历，就回想前传实际收集材料的一段：哪种真实动作更贴近愿意保留的体验？',


         '以自己已见材料的种类留意缺口，惦记还没补进的那类|亲手拿到一件小材料，喜欢输入与物件靠近相连的即时反馈|只是核对当时眼前可见材料与当前已知存量，再决定那轮怎样处理|只是实际调整过一轮已有物品的携带、存放或丢弃，再继续活动',


         'c f material_stock_review item_handling_action'),


        '没有持续积累经历时替代不硬计g；不要求信任满值、所有部落、全部成就或最终解锁。'),


    Q(11, '真实拿到的地图与去过的区域',


        '回想前传里真实找到地图、对照手表或走到新区域的时段：哪种已经做过的投入更贴近愿意保留的体验？',


        '把自己实际见过的地图种类作收集目标，惦记还缺哪张|走进并非为指定材料而去的陌生区域，想亲眼发现那里是什么|只是对照已取得地图与手表实际显示的信息，再决定那段往哪里走|只是为已经走过的区域与取得的地图补记记录',


        'c w navigation_information_review game_recording',


        '前传地图取得点不同于本体；种类目标c、未知发现w、导航与补记0清楚。',


        'GH9L_SOA_PLAYER GH9L_SOA1',


        ('没拿过地图，可以回想真实最早走过的前传林间路段：哪种已经做过的动作更贴近愿意保留的体验？',


         '走近没看过的林缘，想亲眼知道转过去是什么|按我给Jake设定的野外记录习惯，先记下已走到的位置再继续|只是先核对当时身体与已带补给的实际状态，再决定那轮活动|只是为已经走过的位置补记记录',


         'w r survival_status_review game_recording'),


        '不要求全五张地图、固定坐标、自动玩家点或强制到过机场；未取得地图者不猜地图知识。'),


    Q(12, '真实同游时先援助还是找传奇',


        '回想前传里确实与其他真人同游的一段：有人想先完成眼前援助，有人想继续找传奇石画。哪种你真实做过的动作更贴近愿意保留的投入？',


        '先谈清这轮共同想完成什么，商量谁带现有物品、谁走哪段以及何时再集合|先陪同伴走走聊眼前看到的东西，喜欢一起待在这段丛林的陪伴|问过愿意参加的人，约定这轮只在眼前这一段河岸活动的小规则再一起玩|只是为已经参与的援助、已读传奇与去过位置补记记录',


        'q o i game_recording',


        'SoA原生真人联机与NPC部落信任分开；协商共同目标q、陪伴o、自订且同意i明确。',


        'GH9L_SOA2 GH9L_STORE',


        ('只有单人前传经历，就回想真实最早在部落区域旁活动的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '给那轮定过只沿这一小段河岸活动的规则，再照自己的玩法尝试|按我给Jake设定的援助者身份，先交出眼前已能交的一份物品，再继续走|在自己已熟悉的落脚处慢慢停留，享受安稳的地方|只是给已经拿到的物品与实际走过的位置补记记录',


         'i r h game_recording'),


        '只真人实际同游，不让未联机者假想队伍，不承诺各人任务解锁、物品、信任或存档进度必同步。'),


]





GH_SOA[0]['variants'].append(_extra(


    '前传船上已有天线的修复',


    '前两种部落或林缘情境都不适用，可以答前传实际修船上无线电的一段：你已找到天线并带回船，当前修复交互确实能用。你先怎样继续？',


    '先核对已经显示的修复要求与手头天线，确认这次条件|实际交入这根当前可用天线，亲手体验修复操作|照我给Jake设定的联络员身份，先修好这次无线电，再继续原来的旅程|只是给已经找到的天线与船的位置补记记录',


    'objective_requirement_review available_operation_trial r game_recording',


    '另一真实前传目标，不要求见村长或探索林缘；交付条件/普通操作/记录0，身份落实先修r。',


    'GH9L_SOA_PLAYER GH9L_NOTEBOOK',


    '前传天线修船，不是本体Story无线电或主菜单Radio挑战；不保证已听到所有后续对话。'))


GH_SOA[1]['variants'].append(_extra(


    '还没读传奇时的前传基础制作',


    '多段和单块传奇都没读过，可以答前传实际制作过的最早小工具：当前基础配方已开、材料够，物品栏能容纳它。你先怎样继续？',


    '先核对当前已经出现的基础制作说明，再继续自己的实际尝试|排清这次取料、制作与收回余料的先后，再亲手照顺序做|按我给Jake设定的自备工具习惯，先做这件当前可用小工具，再继续原来的路段|直接制作这件当前可做工具，亲手体验操作发生',


    'game_reference_first physical_tool_action_sequence r available_operation_trial',


    '完全未读传奇者不用猜剧情或线索；明确普通说明/单轮制作/操作0，身份具体影响先制作r。',


    'GH9L_STORE GH9L_SOA1 GH9L_CHALLENGE_PLAYER',


    '只当前可做的基础物件，不从提示现成配方推机制解谜，也不借本体Mia故事。'))


GH_SOA[2]['variants'].append(_extra(


    '没有护送治疗时的渔民工具蓝图',


    '孩子护送与猎人治疗都没经历过，可以答实际帮助过的Habbacu渔民：他旁边的工具蓝图已显示需要，手边已有一份确实可交的物件。你先怎样继续？',


    '先查看蓝图实际显示的工具要求与手头物件，核对这次条件|实际给这份当前可交物件，亲手体验一次游戏内援助|按我给Jake设定的沿河援助者身份，先完成眼前这次交付，暂不继续赶路|按这次已显示的渔民需要给出当前物件，把眼前目标推进',


    'objective_requirement_review available_operation_trial r stated_objective_progress',


    '真实渔民蓝图不同于需检查伤情的猎人；目标条件可看有独立依据，NPC援助不计真人q/o。',


    'GH9L_SOA3 GH9L_SOA_PLAYER GH9L_SOA_UI',


    '不要求所有工具齐全、规定数量或假设每位渔民要同一物件；只当前一份合用物件。'))


GH_SOA[3]['variants'].append(_extra(


    '未清污染处理遗体时的图腾材料',


    '污染水源与遗体处理都没经历过，可以答实际修过的部落图腾：当前破损图腾能修，材料要求可看，手边有一份能交入的材料。你先怎样处理？',


    '先核对已列材料要求与已有物件，再决定这一轮怎样推进|排清这次取料、带到图腾与交入的先后，再亲手照顺序做|按我给Jake设定的修复者身份，先把已有这一份交进图腾，暂不往新区域走|直接交入当前这一份可用材料，亲手体验这项操作',


    'objective_requirement_review physical_tool_action_sequence r available_operation_trial',


    '不同于清水或火堆的真实前传修复活动；普通材料核对、单轮动作、交入0，身份影响先修r。',


    'GH9L_SOA3 GH9L_SOA_PLAYER',


    '只题面已能修的图腾，不造随意更改部落图案、重复刷奖励或全材料已齐。'))


GH_SOA[4]['variants'].append(_extra(


    '没有图腾渔民经历时的开笼援助',


    '修图腾与帮助渔民都没经历过，可以答前传实际救过被囚部落成员的一段：这次看守已处理，笼门当前确实可交互打开。你先怎样继续？',


    '直接打开这扇当前可开的笼门，亲手体验这次援助操作|按我给Jake设定的援助者身份，先打开眼前笼门，再继续原来的路段|先核对当前已经显示的这项援助目标与进度，确认做到哪一步|只为已经见过的部落成员与这个地点补记记录',


    'available_operation_trial r quest_progress_review game_recording',


    '另一真实前传NPC援助；前提明确无须再打看守，普通操作、进度查看、补记0，身份落实先开门r。',


    'GH9L_SOA1 GH9L_SOA_PLAYER',


    '不保证所有难度都有同样敌人，不编谈判选项或强迫杀敌；NPC并非其他真人。'))


GH_SOA[5]['variants'].append(_extra(


    '还没进仪式回村时的前传身体检查',


    'Mu’agi仪式与部落进度回看都没经历过，可以答前传实际身体检查的一段：当前能打开检查、转动已显示肢体，未必受伤。你先怎样继续？',


    '先查看当前实际显示的身体状态，再决定这轮活动|实际转动这条当前可检查的手臂，亲手体验这项操作|按我给Jake设定的野外检查习惯，先查完当前肢体再继续可走路段|先核对已经出现的检查操作说明，再继续自己的尝试',


    'survival_status_review available_operation_trial r game_reference_first',


    '前传原生生存操作，不要求仪式或村长；普通状态/操作/说明0，身份落实检查再走r。',


    'GH9L_STORE GH9L_SOA1',


    '只自己当前显示的游戏身体，不要求辨认疾病、医药配方或现实医学判断。'))


GH_SOA[6]['variants'].append(_extra(


    '没有狩猎砍木时的前传点火工具',


    '仪式狩猎和斧头砍木都没经历过，可以答前传实际点火的一段：当前手钻、干燥引火物与已可点的火堆具备。你先怎样投入？',


    '反复练取工具、放引火物与开始点火的操作，专门把这一项练熟|亲手尝试这次可进行的点火，留意动作与火光相连的反馈|排清取工具、用引火物与点燃这一轮的先后，再亲手照顺序做|先核对当前身体状态与手头补给，再决定这轮怎样活动',


    't f physical_tool_action_sequence survival_status_review',


    '不同工具的真实基本动作；明确刻意训练t、即时反馈f，单轮流程/状态0。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '题面给当前能点，不固定能量门槛或材料配方，不保证雨中火堆不灭，不推广真实野外点火。'))


GH_SOA[7]['variants'].append(_extra(


    '未进水下仪式也没地图时的已读传奇',


    'Habbacu仪式和地图导航都没经历过，可以答前传实际读过的一块传奇石画：文字当前能回看，附近也有可走但没看过的小路。你先怎样继续？',


    '再读已见文字，想理解传奇中的人和事件|去看看没走过的小路，想亲眼知道转过去是什么|按我给Jake设定的记录员习惯，先记下这块已读石画的位置再继续|只给这段已读文字与位置补上一份记录',


    's w r game_recording',


    '无地图或仪式前提的前传叙事/探索；故事联系、未知发现、身份落实记录再走与普通记录0分开。',


    'GH9L_SOA1 GH9L_SOA_PLAYER',


    '只有一块线索不要求传奇解法已触发，不编官方对话分支或保证路上还有石画。'))


GH_SOA[8]['variants'].append(_extra(


    '真实尚未接触前传叙事时的取水工具',


    '没有无线电、村长或传奇经历，就回想前传真实用椰碗取水或料理过的一段：当时器具与物品确实可用。哪种已经做过的动作更贴近愿意保留的体验？',


    '亲手取放椰碗与水，喜欢动作、器具和输入相连的反馈|只是排清当时取碗、放水与收回器具的先后，再亲手做那一轮|按我给Jake设定的营地照料习惯，先把当时可用的一碗收好，再继续别的活动|只是先核对当时身体状态与已带补给，再决定那轮活动',


    'f physical_tool_action_sequence r survival_status_review',


    '真实前传日常，未读听叙事不硬计s；身份落实收好器具r，普通顺序/状态0。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '只当时实际能用的水和器具，不保证水净化、药效、固定营养或任何可食材料安全。', reflection=True))


GH_SOA[9]['variants'].append(_extra(


    '真实尚无部落积累时的同一落脚点',


    '没有反复援助部落，也不以拾材料为主要体验，可以回想前传真实逐次完善同一落脚点的一段：哪种已经做过的动作更贴近愿意保留的投入？',


    '几次回来给同一小营地添东西，喜欢先前投入逐渐留在这处住所上|调整过构件位置，让它表达自己想要的营地风格|明明还有路可走，仍会在已经熟悉的落脚处慢慢待一阵|只是给已经搭过的构件与步骤补记过程',


    'g a h construction_process_recording',


    '第三种真实同一对象积累，不要求村落信任；风格、熟悉停留与普通建设记录0分开。',


    'GH9L_STORE GH9L_BUILD GH9L_SOA1',


    '必须真有多次完善才可选g，不把一次放火堆或小营地存在很久就计积累。', reflection=True))


GH_SOA[10]['variants'].append(_extra(


    '真实没有地图远行时的已有物品',


    '没有地图或林间远行经历，就回想前传真实拿到过的小木棍、石头或其他材料：哪种已经做过的动作更贴近愿意保留的体验？',


    '以自己已见过的材料种类留意缺口，惦记慢慢补进想要的一套|亲手拿回一件小物件，喜欢输入与它靠近眼前相连的反馈|只是先核对当时实际可见物料与当前已知存量，再决定那轮怎样处理|只是为已经拿到的物品与当时位置补记记录',


    'c f material_stock_review game_recording',


    '另一种真实收取经历，无地图或探索门槛；种类动机c、即时反馈f与物料/补记0。',


    'GH9L_STORE GH9L_SOA1',


    '不从材料数量或背包满推收集，不造官方材料图鉴或全部补齐奖励。', reflection=True))


GH_SOA[11]['variants'].append(_extra(


    '真实单人尚未援助时的已有蓝图',


    '没有同游或部落援助经历，就回想前传真实放过的一项基础营地蓝图：当时配方已开、材料够，位置确实可放。哪种已经做过的动作更贴近愿意保留的投入？',


    '照我给Jake设定的野外生活习惯，先把可用蓝图放在当时选好的角落，再收整近处工具|给那轮搭建定过只在眼前一小片空地活动的规则，再照自己的玩法尝试|亲手放过这一处蓝图，喜欢输入后轮廓立刻出现在眼前的反馈|只是实际调过一次当时可用蓝图的位置，亲手看那次编辑结果',


    'r i f creative_edit_trial',


    '第三单人前提；身份落实放蓝图再收整r、自订范围i与即时反馈f，普通位置编辑0。',


    'GH9L_STORE GH9L_BUILD GH9L_SOA1',


    '原生已开放蓝图，不造全配方、免材料、NPC帮建或玩家共享进度保证。', reflection=True))





GH_CHALLENGES = [


    Q(1, 'Campfire挑战的原木与点火',


        '当前是主菜单的单人Campfire挑战，目标火堆已有构架，仍在计时；周围有可砍木料，斧头可用，还没凑齐全部材料。你先怎样继续？',


        '先核对目标构架已经显示的材料与手头存量，再决定这轮怎样推进|排清这次取斧、砍木、搬到构架与交入材料的先后，再亲手照顺序做|按已经列出的火堆目标交入当前能交的材料，把眼前目标推进|按自己已确定的完成用时目标，实际尝试推进这一轮',


        'objective_requirement_review physical_tool_action_sequence stated_objective_progress score_goal_attempt',


        '真实Campfire搭建并点燃目标，不问虚构合作或排名。目标核对、单轮搬运、推进和个人用时均精确0。',


        'GH9L_CHALLENGE_PLAYER',


        ('没玩过Campfire，可以答实际玩过的Raft挑战：目标木筏已显示材料需求，手边有一份当前能交的材料，仍在计时。你先怎样继续？',


         '先看木筏目标已经列出的材料要求，核对手头物品|排清这次取料、带到木筏与交入的先后，再亲手照顺序做|按已经列出的木筏目标交入这一份材料，把当前需求推进|按自己已经确定的完成用时目标，实际尝试推进这一轮',


         'objective_requirement_review physical_tool_action_sequence stated_objective_progress score_goal_attempt'),


        '这是绿色地狱的Raft挑战，不是另一个游戏《木筏求生》；不用固定材料量、坐标、时间或中途保存保证。'),


    Q(2, 'Blacksmith挑战的木炭与熔炉',


        '当前是Blacksmith挑战，你已让木炭炉和泥熔炉可用，手边有木料、可熔材料与当前能用的模具；计时仍在。你想先怎样安排？',


        '把补木、烧炭、熔炼、模具处理与下一轮补给连成周转，持续调整两边供给|只先看当前炉中燃料、可熔材料与已出产物，核对这一轮制作状态|排清这一轮取料、投炉、处理模具与收回产物的先后，再亲手照顺序做|按已经显示的金属装备目标推进，把本轮当前可做的一项接上',


        'y production_state_review physical_tool_action_sequence stated_objective_progress',


        '实际Blacksmith连续投入产出才y，单轮顺序、已有状态与目标推进0；不把一轮投炉都称资源经营。',


        'GH9L_CHALLENGE_PLAYER',


        ('没玩过Blacksmith，可以答Mighty Camp里实际烧过木炭的一段：火堆、木材和后续目标所需木炭当前都已明确，计时仍在。你先怎样安排？',


         '把补木、烧炭、回收与下一轮补给接成周转，持续调配材料来源|只先核对当前木材、燃烧与已产木炭的状态，再决定这一轮怎样处理|排清这一轮取木、添入、收回产物与收整余料的先后，再亲手做|按当前目标已经列出的木炭需求，推进这一轮可做的部分',


         'y production_state_review physical_tool_action_sequence stated_objective_progress'),


        '炉型与当前材料均给足，不要求指定炉数、必有罐头、精确烧成时间、熔炼数值或金属装备必不受损。'),


    Q(3, 'Hunter挑战清单中的猎物种类',


        '当前是Hunter挑战，目标清单还缺几种；你已实际见过一只当前可接近的目标，手头武器可用，也有退开空间。你先怎样投入？',


        '把这份猎物种类作为自己想补齐的一套，惦记还缺的那一类|专门重复练当前武器的瞄准与出手时点，想把这一项操作练熟|亲手出这一手，留意声音、动作与目标反应相连的反馈|先核对已经显示的猎物清单与当前完成进度，再决定这轮怎样继续',


        'c t f quest_progress_review',


        'c须明确在意种类补全，不把按任务取肉自动计收集；t/f动机明确，清单查看0。不采用一击击杀或固定刷新。',


        'GH9L_CHALLENGE_PLAYER',


        ('没玩过Hunter，可以答Fisherman里真实接近目标鱼的一段：当前鱼类清单可看，已有能用的捕鱼工具，眼前这段水边可操作。你先怎样投入？',


         '把这套已见鱼类作自己的种类目标，惦记补进还缺的那类|反复练这一项下竿或出矛的操作时点，专门把手头工具练熟|亲手操作这一轮，留意竿线或水面与输入相连的反馈|先核对已经显示的鱼类清单与当前进度，再决定这轮怎样继续',


         'c t f quest_progress_review'),


        '只当前实际看见且能操作的目标，不规定猎物总数、陷阱必抓到、鱼必上钩或危险全部关闭。'),


    Q(4, 'Radio挑战已发现的守卫营地',


        '当前是Radio挑战，所需无线电部件所在营地已找到；有实际守卫，你手头武器与退开空间可用，补给也够这段活动。你先怎样投入？',


        '专门反复练手头武器的瞄准、出手与退步时点，想把操作练熟|排清已有补给、这段接近方式与取到部件后的返回安排，再照这趟准备行动|按已经显示的部件目标行动，把当前可完成的一段推进|按自己已确定的完成用时目标，实际尝试推进这一轮',


        't mission_preparation_plan stated_objective_progress score_goal_attempt',


        '真实Radio有部件和守卫，但不预告人数或击杀顺序；训练须明确动机，单次准备、既定目标和个人用时0。',


        'GH9L_CHALLENGE_PLAYER',


        ('没玩过Radio，可以答Hunter里真实用武器的一段：目标当前可接近，武器与退开空间确实可用。你先怎样投入？',


         '反复练瞄准与出手的时点，专门把这一项操作练熟|亲手出手，喜欢动作与眼前反应紧接着发生的反馈|排清接近、出手、退开恢复与再接近的循环，再照这一轮安排尝试|只先核对当前身体状态与已有补给，再决定这一轮怎样行动',


         't f combat_resource_cycle survival_status_review'),


        '不编撤回守卫后其必不追、固定解绳秒数、部件可无敌抢走或NPC队友；未进交手者可继续换。'),


    Q(5, '熔炉没有继续工作时的一个猜想',


        '在Blacksmith挑战中，当前泥熔炉没有继续产出，你还没确认原因；有可用木炭、已投入的可熔材料，计时仍在。你先怎样处理？',


        '猜是燃料没接上，保留其他投入不变，只补一份当前可用木炭，检验这次是否改变|只先查看当前已显示燃料、原料与产物状态，再决定这一轮怎样处理|排清这一轮取炭、投料与收回当前产物的先后，再亲手照顺序做|先核对已经可用的熔炼操作说明，再继续自己的尝试',


        'p production_state_review physical_tool_action_sequence tool_reference_first',


        '原因未给定且单项可失败检验才p；并不保证缺煤就是答案。普通状态、一次操作安排和说明0。',


        'GH9L_CHALLENGE_PLAYER',


        ('没有熔炉经历，可以答Campfire最早已有斧头、木料可砍的一段：你当前能动手，也能停下退开。你先怎样继续？',


         '亲手挥这一斧，留意声音、木料变化与输入相连的反馈|排清这次取斧、砍木与收整材料的先后，再亲手照顺序做|先核对当前已经出现的工具操作说明，再继续实际尝试|只先查看当前身体状态与已带补给，再决定这一轮怎样行动',


         'f physical_tool_action_sequence tool_reference_first survival_status_review'),


        '不把燃料数量、冷却时间或材料一定已熔当答案；别把简单投料照指示都计机制研究。'),


    Q(6, 'Fisherman挑战的竿、矛与已有目标',


        '当前是Fisherman挑战，手头已有当前能用的钓竿或捕鱼矛，眼前水边可以操作，目标清单还未完成。你先怎样投入？',


        '反复练当前这件捕鱼工具的出手与收回时点，专门把操作练熟|亲手操作这一轮，留意竿线、水声或鱼的反应接着发生的反馈|排清这一轮取工具、靠近水边、操作与收整手头物品的先后，再亲手做|先核对已经显示的鱼类目标与当前进度，再决定这一轮怎样继续',


        't f physical_tool_action_sequence quest_progress_review',


        '真实Fisherman工具操作，不造自动捕全；刻意训练、即时反馈与单轮流程/清单0分开。',


        'GH9L_CHALLENGE_PLAYER',


        ('没用过捕鱼工具，可以答挑战中最早点火的一段：当前点火工具、干燥引火物和可点火堆具备，计时仍在。你先怎样投入？',


         '反复练取工具、放引火物与点火的操作，专门把这一项练熟|亲手点这次已能点的火，留意动作和火光相连的反馈|排清这轮取工具、放引火物与点火的先后，再亲手照顺序做|先核对当前身体状态与已有补给，再决定这一轮怎样行动',


         't f physical_tool_action_sequence survival_status_review'),


        '不采用鱼饵、陷阱无需饵、固定鱼点或危险一击致命等旧攻略结论，不输出真实野外操作建议。'),


    Q(7, 'Mighty Camp剩余构件与手头材料',


        '当前是Mighty Camp挑战，预放目标构件还没全部完成，手边有一批能交入的木竹材料，仍在计时。你先怎样安排？',


        '先查看目标构件已经列出的材料要求，核对当前库存|排清这一轮取料、带到构件与交入的先后，再亲手照顺序做|按当前已选的一处目标构件交料，把眼前建设目标推进|只先核对现场实际可见物料与当前已知存量，再决定这一轮怎样处理',


        'objective_requirement_review physical_tool_action_sequence stated_objective_progress material_stock_review',


        '预放建设目标不假造任意位置编辑；四项普通目标/流程/物料行为均精确0。',


        'GH9L_CHALLENGE_PLAYER',


        ('没玩过Mighty Camp，可以答Campfire里实际搬木的一段：目标构架可交料，眼前一份木料可取，当前还有完成目标的时间。你先怎样处理？',


         '先看目标构架已列的材料要求，核对手头这一份|排清这次取木、搬到构架与交入的先后，再亲手照顺序做|实际交入当前这份可用材料，以推进已经选定的火堆目标为重点|只先看眼前实际可见木料与当前已知存量，再决定这一轮怎样处理',


         'objective_requirement_review physical_tool_action_sequence stated_objective_progress material_stock_review'),


        '不把固定目标工地当自由装饰，不要求哪一构件优先、固定竹林坐标或所有材料必须齐备才可答。'),


    Q(8, '计时仍在的本轮自订小玩法',


        '你正在一项真实玩过的单人挑战里，当前已有斧头和眼前可砍木料，计时仍在；这段操作不要求你立刻结束挑战。你更想怎样用这一小段？',


        '给这一小段另加只在眼前一小处取木的规则，再照自己的小玩法尝试|反复练挥斧和退步时点，专门把这一项操作练熟|按自己已确定的完成用时目标，实际尝试推进这一轮|亲手挥这一斧，留意声音、木料变化与输入相连的反馈',


        'i t score_goal_attempt f',


        '七项Challenges都是单人，不造合作规则；i是玩家额外自订小段限制，t为练习、f为反馈，个人用时0。',


        'GH9L_CHALLENGE_PLAYER',


        ('没用过斧头，可以答挑战中实际拾过小材料的一段：眼前木棍或石头当前可取，背包也有这次空间，计时仍在。你先怎样投入？',


         '给这一小段定只在眼前这处拾取的小规则，再照自己的玩法尝试|亲手拿回一件材料，留意输入与物件移动相连的反馈|按自己已确定的完成用时目标，实际尝试推进这一轮|只先核对当前可见物料与已知存量，再决定这一轮怎样处理',


         'i f score_goal_attempt material_stock_review'),


        '不说计时暂停、不承诺小规则不影响通关；个人计时目标不是对手排名或官方自订挑战编辑器。'),


    Q(9, '真实处理过的一轮挑战供给',


        '回想Blacksmith或Mighty Camp中真实多轮烧炭、补木或接续制作的时段：哪种已经做过的投入更贴近愿意保留的体验？',


        '持续调整补木、烧炭、制作与下一轮储备，让几轮供给接得上|只是先看当时已经可见的材料、炉中状态和产物，再决定那轮怎样处理|只是排清当时一轮取料、加工与收回产物的先后，再亲手做|只是为当时已经拿到的材料与实际走过位置补记记录',


        'y production_state_review physical_tool_action_sequence game_recording',


        '真实持续供给y，不把一个挑战中所有劳动自动算y；普通状态、单轮流程、补记0。',


        'GH9L_CHALLENGE_PLAYER',


        ('没做过多轮加工，可以回想挑战最早取放已有物件的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '亲手拿回或收起物件，喜欢输入与眼前移动相连的反馈|只是先查看当时可见物料与当前已知存量，再决定那轮怎样处理|只是按当时已有物品实际调整一轮携带、存放或丢弃，再继续活动|只是先核对当时身体状态与已带补给，再决定那轮活动',


         'f material_stock_review item_handling_action survival_status_review'),


        '不要求造出多座炉、产量最优、挑战成功或全程没受伤，没有持续周转就不硬计y。'),


    Q(10, '真实惦记过的挑战物品缺口',


        '回想Hunter或Fisherman里真实回看目标种类清单的一段：哪种已经做过的投入更贴近愿意保留的体验？',


        '把这套自己已经见过的种类当作想补齐的一套，惦记还缺的那类|只是核对当时已经显示的清单与完成进度，再决定那轮怎样继续|只是按自己已经确定的完成用时目标，实际尝试推进那一轮|只是为已经取得的物品与发现位置补记记录',


        'c quest_progress_review score_goal_attempt game_recording',


        '真实清单中明确种类补全才c，普通进度查看、个人时间目标与补记0；不凭通关或拿肉判收集人格。',


        'GH9L_CHALLENGE_PLAYER',


        ('没玩过这两项，可以回想Campfire、Raft或Mighty Camp里真实看目标材料的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '只是先核对目标当时已列的材料要求与手头物件，再决定那轮怎样推进|只是按当前已经选定的一项构件目标交料，把那轮需求推进|只是按自己已确定的完成用时目标，实际尝试推进那一轮|只是为已经参与的构件建设和步骤补记过程',


         'objective_requirement_review stated_objective_progress score_goal_attempt construction_process_recording'),


        '没有种类收藏动机的材料建设替代全为精确0；不虚构排行榜、其他真人竞争或全挑战奖杯门槛。'),


    Q(11, '真实练过的Radio出手',


        '回想Radio或Hunter中真实交手、投掷过的一段：哪种已经做过的动作更贴近愿意保留的投入？',


        '专门重复练过瞄准、出手与退步时点，想把这一项操作练熟|比较过当时确实可换的两组武器与护具搭配，再检验组合效果|亲手出手，喜欢声音、动作与目标反应接连发生的反馈|只是先比较当时确实已有的装备与组件，再决定那轮怎样安排',


        't b f compare_available_setup',


        '真实刻意训练与实际检验组合才t/b，普通装备浏览0；不从成功、最优武器或固定击杀数推能力。',


        'GH9L_CHALLENGE_PLAYER GH9L_STORE',


        ('没有交手经历，可以回想挑战里真实使用最早斧头的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '反复练过挥斧、退步与再靠近的时点，专门把工具操作练熟|亲手砍木，喜欢声音与木料变化紧接着发生的反馈|只是排清当时取斧、砍木与收整材料的先后，再亲手做那一轮|只是先核对当时身体状态与已带补给，再决定那轮活动',


         't f physical_tool_action_sequence survival_status_review'),


        '不保证所有挑战起手有装备、角色技能树或护具耐久；只回想自己当时真正有的两组。'),


    Q(12, '真实走过的单人挑战路段',


        '回想一项真实玩过的单人挑战：你曾站在可走但还没去过的林间去向旁，计时仍在。哪种已经做过的动作更贴近愿意保留的投入？',


        '走近那段未知去向，想亲眼看看遮住的地方是什么，暂不为指定材料而走|给当时那一小段另定过只沿眼前河岸活动的规则，再照自己的玩法尝试|照我给Jake设定的记录员习惯，先记下当时所在位置，再继续可走路段|只是先核对当时身体状态与已带补给，再决定那轮活动',


        'w i r survival_status_review',


        '真实未知发现w与自订玩法i、身份落实记录再走r明确，补给查看0；单人挑战无真人q/o。',


        'GH9L_CHALLENGE_PLAYER GH9L_STORE',


        ('没有走过未知路段，可以回想挑战最早站在熟悉起点处理已有物件的一段：哪种真实动作更贴近愿意保留的体验？',


         '给当时那一小段加过只在眼前空地收集的规则，再照自己的玩法尝试|亲手拿起当时可取的一件物品，喜欢输入与眼前移动相连的反馈|按我给Jake设定的惜物习惯，先把眼前可拿的小材料收好，再继续原来安排|只是为已经拿到的物品与当时位置补记记录',


         'i f r game_recording'),


        '不保证额外探索或小规则仍能按时完成，不编原生多人、自由改挑战规则或中途保存功能。'),


]





GH_CHALLENGES[0]['variants'].append(_extra(


    'Mighty Camp当前已有的一处目标构件',


    'Campfire和Raft都没玩过，可以答实际玩过的Mighty Camp：一处预放目标构件仍缺材料，当前有一份能交入的物件，计时仍在。你先怎样继续？',


    '先核对构件列出的材料要求与手头物件，再决定这轮怎样推进|排清这次取料、带到目标与交入的先后，再亲手照顺序做|按当前已经选定的构件交入材料，把眼前需求推进|按自己已确定的完成用时目标，实际尝试推进这一轮',


    'objective_requirement_review physical_tool_action_sequence stated_objective_progress score_goal_attempt',


    '第三项真实建设挑战；目标要求、单轮流程、推进与个人用时目标精确0。',


    'GH9L_CHALLENGE_PLAYER',


    '目标构件预放，不编可任意换形、免材料或部落NPC帮忙，个人用时不是排名。'))


GH_CHALLENGES[1]['variants'].append(_extra(


    '没有烧炭经历时的基础工具制作',


    'Blacksmith和Mighty Camp烧炭都没经历过，可以答实际玩过挑战中的最早制作：当前已有够用木石，一项基础工具确实已能做，计时仍在。你先怎样安排？',


    '只先核对当前制作材料与已有存量，再决定这一轮怎样处理|排清取料、制作与收回余料的先后，再亲手照这轮顺序做|直接制作这件当前可做小工具，亲手体验操作发生|先核对已经出现的制作说明，再继续自己的实际尝试',


    'production_state_review physical_tool_action_sequence available_operation_trial tool_reference_first',


    '未做持续加工就不硬计系统经营y；另一基础制作前提的状态、单轮流程、操作、说明均0。',


    'GH9L_CHALLENGE_PLAYER GH9L_STORE',


    '只当前材料足够且配方已开的工具，不推所有挑战自动全解锁或有相同初始装备。'))


GH_CHALLENGES[2]['variants'].append(_extra(


    '没做猎鱼清单时的Radio目标部件',


    'Hunter和Fisherman都没玩过，可以答Radio里实际拿到一件目标部件之后：你已回到能停留的位置，当前目标进度可查看，计时仍在。你先怎样继续？',


    '先核对已经显示的无线电部件目标与当前进度，确认做到哪一步|按自己已确定的完成用时目标，实际尝试推进这一轮|只为已经取得的这件部件与发现位置补记记录|按我给Jake设定的记录员身份，先记下刚取得的部件，再继续原来安排',


    'quest_progress_review score_goal_attempt game_recording r',


    '不要求猎物或鱼种收藏；普通任务进度、个人用时、记录0，身份落实记录后继续r。',


    'GH9L_CHALLENGE_PLAYER',


    '仅实际已取得的Radio部件，不造Mia对话、前传天线或对手排行榜，也不把部件数量当收藏动机。'))


GH_CHALLENGES[3]['variants'].append(_extra(


    '没有Radio或猎物交手时的已选制作',


    'Radio与Hunter交手都没经历过，可以答实际挑战中的最早工具：这一轮已选定一件基础工具，当前材料够、配方已开。你先怎样继续？',


    '先核对这件已选工具列出的材料要求，确认这次条件|实际制作这件当前可做工具，亲手体验操作发生|排清这次取料、制作与收回余料的先后，再亲手照顺序做|按已选工具需求实际制作，把眼前目标推进',


    'objective_requirement_review available_operation_trial physical_tool_action_sequence stated_objective_progress',


    '无战斗前提的第三情境；已选工具的要求查看/操作/单轮流程/既定目标均精确0。',


    'GH9L_CHALLENGE_PLAYER GH9L_STORE',


    '不把只是做工具当战斗组合或专门练习；不能以配方已开替代材料确实足够。'))


GH_CHALLENGES[4]['variants'].append(_extra(


    '没有熔炉或斧头经历时的Raft交料',


    '熔炉与Campfire砍木都没经历过，可以答实际Raft挑战中的材料交入：木筏目标当前已能交料，手边有一份确实可用物件。你先怎样继续？',


    '先核对目标已列的材料要求与手头物件，再决定这一轮怎样推进|直接交入当前这份材料，亲手体验这项操作|排清这次取料、带到木筏与交入的先后，再亲手照顺序做|只先查看现场实际可见物料与当前已知存量，再决定这一轮怎样处理',


    'objective_requirement_review available_operation_trial physical_tool_action_sequence material_stock_review',


    '真实另一挑战的已知建设过程；没有未知因果，不硬计p；四项普通行为精确0。',


    'GH9L_CHALLENGE_PLAYER',


    '不编木筏能在这个挑战里自由出海、固定椰子数、蓝图全解锁或中途保存。'))


GH_CHALLENGES[5]['variants'].append(_extra(


    '没捕鱼点火时的背包取放',


    '捕鱼工具与点火都没经历过，可以答实际挑战中用过的背包：已有可存取小物件，当前能取出再收回，计时仍在。你先怎样投入？',


    '反复练取出、选位与收回的操作，专门把这一套界面用熟|亲手取出或收回一件小物件，留意输入与眼前移动相连的反馈|排清这一轮取出、处理与收回的先后，再亲手照顺序做|先核对已经出现的物品操作说明，再继续自己的实际尝试',


    't f physical_tool_action_sequence tool_reference_first',


    '第三种实际工具操作，不要求捕鱼或火堆；刻意训练、反馈与单轮流程/说明0分开。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '只当前可用背包操作，不造自动整理、无限空间或必须丢弃物品。'))


GH_CHALLENGES[6]['variants'].append(_extra(


    '第三种目标构架的材料需求',


    'Mighty Camp和Campfire都没玩过，可以答实际Raft挑战：目标构架已显示本轮材料要求，当前有一份能交入的物件。你先怎样安排？',


    '先核对构架已列要求与已有物件，再决定这一轮怎样推进|排清取料、搬到构架与交入这一轮的先后，再亲手照顺序做|按已经选定的这处木筏目标交料，把当前需求推进|只先核对眼前实际可见材料与当前已知存量，再决定这一轮怎样处理',


    'objective_requirement_review physical_tool_action_sequence stated_objective_progress material_stock_review',


    '真实第三项建设挑战，不从建造目标或材料查看强行计长期成长或经营；四项0。',


    'GH9L_CHALLENGE_PLAYER',


    '这是绿色地狱原生挑战构架，不是Raft游戏创意建造，不规定固定材料数或交料优先级。'))


GH_CHALLENGES[7]['variants'].append(_extra(


    '没砍木拾物时的挑战手表',


    '斧头与拾物都没经历过，可以答实际挑战中看过的手表：当前能查看时间、方向或坐标，人物仍能在这小段可走区域活动。你先怎样投入？',


    '给这一小段自订先看一次手表再只沿当前可走河岸走一段的规则，然后照规则尝试|按我给Jake设定的记录员身份，先记下手表实际显示的坐标，再继续可走路段|只先核对当前手表实际显示的位置资料，再决定这一段往哪里走|先核对当前已经显示的任务目标与进度，确认做到哪一步',


    'i r navigation_information_review quest_progress_review',


    '另一种实际原生工具；自订活动顺序和范围i，角色落实记坐标再走r，导航/任务查看0。',


    'GH9L_SOA1 GH9L_CHALLENGE_PLAYER',


    '只当前手表实际能显示的信息，不说地图必已取得、钟表能暂停计时或自订规则被官方计分。'))


GH_CHALLENGES[8]['variants'].append(_extra(


    '真实没有加工取放经历时的身体检查',


    '没有多轮加工或物品收整经历，可以回想挑战中真实打开身体检查的一段：当时能转动已显示肢体，不预设受伤。哪种已经做过的动作更贴近愿意保留的体验？',


    '只是先查看当时身体实际显示的状态，再决定那轮活动|只是实际转动一次当时可检查的手臂，亲手体验那次操作|按我给Jake设定的检查习惯，先查完当时肢体再继续可走路段|只是先核对当时已经出现的检查操作说明，再继续尝试',


    'survival_status_review available_operation_trial r game_reference_first',


    '真实另一生存操作，不要求加工供给或建设；身份具体影响先检查r，普通状态/操作/说明0。',


    'GH9L_STORE GH9L_CHALLENGE_PLAYER',


    '没有长周期生产就不硬计y，没有真实伤情不要求猜疾病、治疗配方或现实生存能力。', reflection=True))


GH_CHALLENGES[9]['variants'].append(_extra(


    '真实Radio里取得部件后的进度',


    '没有猎鱼清单或目标构件建设经历，可以回想Radio里真实取得一件部件的一段：哪种已经做过的动作更贴近愿意保留的投入？',


    '只是先核对当时已经显示的部件目标与当前进度，再决定那轮怎样继续|只是按自己已确定的完成用时目标，实际尝试推进那一轮|按我给Jake设定的记录员身份，先记下已取得部件，再继续当时安排|只是为已经取得物件与发现位置补记记录',


    'quest_progress_review score_goal_attempt r game_recording',


    '另一真实挑战目标，不把少数任务部件硬当收藏；普通进度、个人用时与补记0，身份落实记录后继续r。',


    'GH9L_CHALLENGE_PLAYER',


    '不编对手、部件固定数量或官方最佳时间纪录；只玩家本人既有时间目标。', reflection=True))


GH_CHALLENGES[10]['variants'].append(_extra(


    '真实没有交手砍木时的捕鱼工具',


    '没有Radio交手或斧头经历，可以回想Fisherman里真实用过的捕鱼工具：哪种已经做过的动作更贴近愿意保留的投入？',


    '反复练过下竿、提线或出矛时点，专门把这一项工具操作练熟|亲手操作，喜欢竿线、水面与输入紧接着变化的反馈|只是排清当时取工具、靠近水边、操作与收整的先后，再亲手做那一轮|只是先核对当时身体状态与已带补给，再决定那轮活动',


    't f physical_tool_action_sequence survival_status_review',


    '真实第三工具前提，无武器组合或砍木要求；刻意练习t、即时反馈f与普通流程/状态0。',


    'GH9L_CHALLENGE_PLAYER',


    '不要求某鱼必出现、鱼饵配方或命中率，不从挑战成功推技术能力。', reflection=True))


GH_CHALLENGES[11]['variants'].append(_extra(


    '真实没有远行收集时的制作菜单',


    '没有未知路段或起点拾物经历，可以回想实际挑战里最早制作工具的一段：当时配方已开、材料够、已选定这轮工具需求。哪种真实动作更贴近愿意保留的投入？',


    '按我给Jake设定的自备工具习惯，先做当时可做的小工具，再继续原来活动|只是先核对当时已选工具列出的材料要求，确认条件后再决定是否推进|只是实际制作当时这一件可做工具，亲手体验那次操作|只是排清当时取料、制作与收回余料的先后，再亲手做那一轮',


    'r objective_requirement_review available_operation_trial physical_tool_action_sequence',


    '真实第三种基本制作经历，身份落实先做工具r，普通要求/操作/流程0；无真人社交或未知探索硬计。',


    'GH9L_CHALLENGE_PLAYER GH9L_STORE',


    '只当时确实可做的工具，不编所有挑战全配方、定制模式或中途存档能力。', reflection=True))





PZ_42 = [


    Q(1, 'Knox住处门外的下一段街区',


        'Build42里你暂时待在已经熟悉的住处，当前身体和随身食水能查看；门外有一段能接近但还没看过的街区。没有必须立刻完成的系统任务。你先怎样过这一段？',


        '走近没看过的街区，想亲眼知道那些建筑里外是什么|先核对当前身体状态与已带食水，再决定这轮怎样活动|排清已有补给、这一小段去向与回住处的安排，再照这趟准备行动|留在熟悉屋内慢慢收拾，享受这里暂时安稳的感觉',


        'w survival_status_review mission_preparation_plan h',


        '本作自由生存的探索/落脚取舍，不造NPC派任务；未知发现w、熟悉栖居h与状态/一次准备0分开。',


        'PZ9L_STORE PZ9L_42',


        ('尚无自己的住处，可答42最早实际搜过的一栋屋：一只容器已打开，手边物品可取，门外小路当前也能走。你先怎样继续？',


         '去看看还没看过的下一处屋外，想亲眼发现那里是什么|只先核对当前身体与随身补给，再决定这轮活动|按现有物品调整这次携带、存放或丢弃，再继续眼前搜取|排清这一趟带什么、走哪段与回已知落脚点的安排，再照准备行动',


         'w survival_status_review item_handling_action mission_preparation_plan'),


        '可走不等于无僵尸或绝对安全，身体设置按当前实有，不固定感染、水电关闭日或出生房无敌。'),


    Q(2, '工作站配方的可选输入',


        '42的当前工作站已经可用，一项已选配方允许指定输入材料；手边有几份确实合用材料，制作条件满足。你先怎样继续？',


        '先核对这项配方已显示的输入与手头材料，确认这次条件|比较当前材料确实够做的配方或输入选项，再决定采用哪项|排清这一轮取料、指定输入、制作与收回产物的先后，再亲手照顺序做|直接用一份当前合用材料制作，亲手体验这次操作',


        'objective_requirement_review compare_production_options physical_tool_action_sequence available_operation_trial',


        '42真实配方输入选择与工作站；查看已列条件不是未知机制研究，四项普通制作行为精确0。',


        'PZ9L_42',


        ('还没用过工作站，可答当前可做的最早一项制作：配方已开、材料够、已选定本轮工具需求，不要求特殊台面。你先怎样继续？',


         '先核对已选工具列出的材料要求与当前物品，再决定怎样推进|比较当前已开放且材料够做的基础配方，再决定采用哪项|排清取料、制作与收回余料的先后，再亲手做这一轮|直接做这一件当前可制作工具，亲手体验操作发生',


         'objective_requirement_review compare_production_options physical_tool_action_sequence available_operation_trial'),


        '只题面已可用的工作站与合用材料，不推全部配方已开、不同输入必改变属性或材料被自动取到。'),


    Q(3, '42季节耕作中的下一轮种植',


        '你已有实际照料过的地块、当前能种的种子与用具；这轮种植的季节条件已经确认合用，现有食水允许继续活动。你先怎样投入？',


        '接着完善同一片地，喜欢前几轮照料逐渐留在这里的变化|把留种、种植、补水、收成与之后食物储备连成几轮周转，持续调整供给|以自己实际见过的作物种类留意缺口，惦记补进还没种过的那类|只先查看当前地块、作物和已有材料状态，再决定这一轮怎样处理',


        'g y c production_state_review',


        '42真实季节耕作给足当前可种条件；同一对象积累g、多轮供给y、明确种类c与普通查看0分开。',


        'PZ9L_42 PZ9L_STORE',


        ('没种过地，可答42实际整理过的料理材料：当前炉具能用，已有一份确实能料理的食物和可用容器。你先怎样安排？',


         '把食材取得、料理与之后补回储备接成几轮周转，持续调整生活供给|只先核对当前食材、容器与已有产物状态，再决定这一轮怎样处理|排清这次取食材、放入容器、料理与收整的先后，再亲手做|直接料理当前这份可用食物，亲手体验这项操作',


         'y production_state_review physical_tool_action_sequence available_operation_trial'),


        '不固定月份、成长天数、农药或产量；季节不合用时不能拿本题要求玩家实际播种，也不造现实食物安全保证。'),


    Q(4, '鸡群、水与同一处饲养点',


        '42里你已实际照料过这群鸡，当前能查看它们并补给已有饲料与水；附近也是你走熟的落脚处。你先怎样投入？',


        '继续回来照料同一群鸡，喜欢先前投入慢慢留在这处饲养点上|把饲料、水和产出接成几轮周转，持续调整这片地方的供给|先在已经熟悉的饲养点与住所旁慢慢待一段，享受暂时安稳的地方|只先查看当前鸡群、饲料与水的实际状态，再决定这一轮怎样处理',


        'g y h production_state_review',


        '仅42原生动物照料，明确持续积累/多轮周转才g/y；普通动物状态核对0，熟悉停留h。',


        'PZ9L_42',


        ('没有动物，可答实际种过或照料过的42地块：当前有能处理的作物与材料，附近已有熟悉落脚处。你先怎样投入？',


         '接着照料同一片地，喜欢前几轮投入留下的变化|把留种、补水、收成与之后储备接成多轮周转，持续调配供给|先回熟悉地块与屋边慢慢待一阵，享受暂时安稳的地方|只先查看当前作物、地块与材料状态，再决定这一轮怎样处理',


         'g y h production_state_review'),


        '不把动物当真人共同目标，不给鸡数量、繁育成功、必产蛋、疫病规则或41同样有鸡群的保证。'),


    Q(5, '42水面动静与这次捕鱼',


        '42里当前捕鱼工具能用，水边可操作；你已看过这一处水面动静，但还没确认自己活动的噪声是否影响这一段的鱼。你先怎样投入？',


        '把减少这段自身噪声当作未核实的猜想，保持其他用具不变，试一段后比较实际动静|反复练当前捕鱼工具的操作时点，专门把这一项练熟|亲手操作这一轮，留意输入、竿线与水面相连的反馈|先核对当前身体状态与已带补给，再决定这一轮怎样活动',


        'p t f survival_status_review',


        '42官方确有鱼对噪声反应；p是本人尚未确认的单项试验，不预告结果。刻意操作训练和即时反馈明确，状态0。',


        'PZ9L_42',


        ('还没捕鱼，可答实际用过的最早近战武器：当前武器可用，眼前一只僵尸可接近，周围能退开恢复。你先怎样投入？',


         '反复练瞄准、推击或退步的时点，专门把这一项操作练熟|亲手打一轮，留意动作、声音与目标反应相连的反馈|排清接近、出手、退开恢复与再次接近的循环，再照安排尝试|只先核对当前身体状态与已有补给，再决定怎样行动',


         't f combat_resource_cycle survival_status_review'),


        '不承诺声音降低必有鱼、固定鱼数、必能近战获胜或僵尸绝不会奔跑；只本次实际可用条件。'),


    Q(6, '已可进入的地下室与一份传单',


        '42里你已找到一个当前能进入的地下室入口，附近还拿到一份可读传单；不要求立刻搬家或交战。你先怎样用这一段时间？',


        '走进还没看过的地下空间，想亲眼知道里面是什么|读已拿到的传单，把它讲的人和事件与这处地方前后经历接起来|按我给这个幸存者设定的记录员身份，先记下已见入口，再继续查看当前可达空间|只为已经取得传单与看过的入口补记记录',


        'w s r game_recording',


        '42真实地下室与环境文字叙事；未知发现、故事联系、身份落实记录再查看与普通补记0分开。',


        'PZ9L_42',


        ('没有地下室经历，可答42实际遇过的屋内场景：你已看过一处留下物件或尸体的现场，当前还可回看，外面有一段能走但没看过的路。你先怎样继续？',


         '再看已经见过的物件与现场，想理解这里的人之前经历了什么|去看看没走过的小路，想亲眼知道转过去有什么|按我给幸存者设定的记录习惯，先记下已见现场再继续可走路段|只是给已见地点与实际体验过的人物线索补记记录',


         's w r game_recording'),


        '不保证每栋屋都有地下室、不编新NPC任务、传单具体台词或现场唯一正确解释；旧41不借此新增地下层。'),


    Q(7, '当前武器的头部与柄部状态',


        '42里你当前持有一把确实支持部件状态的武器，界面能查看它的头部、柄部或刃部信息；身旁另有当前可用的备用武器。你先怎样继续？',


        '先比较当前已有的武器与组件，再决定这一轮采用哪件|先核对已经出现的部件状态与使用说明，再继续实际尝试|直接换用这一件当前可装备的备用武器，亲手体验这项操作|按我给幸存者设定的惜物习惯，先把旧武器收好，再用当前备用武器继续',


        'compare_available_setup tool_reference_first available_operation_trial r',


        '仅42确有独立部件的武器，不推所有武器都有头柄或任意部件能换；普通比较/说明/装备0，身份落实收旧换备r。',


        'PZ9L_42',


        ('没用过部件武器，可答实际拥有两件衣物的一段：当前两件都能穿，已有外观或防护信息可看。你先怎样继续？',


         '只先比较当前确实已有的衣物与装备信息，再决定这轮穿哪件|选一套自己想表达的颜色和轮廓，让幸存者带上想要的风格|按我给幸存者设定的旧制服习惯，穿回这件当前可穿旧衣，再继续原来路段|实际换上当前这件可穿衣物，亲手体验这项操作',


         'compare_available_setup a r available_operation_trial'),


        '不保证任意衣物防咬、旧物可修、头必会掉或部件替换配方已开，不从制服或性别推现实人格。'),


    Q(8, '人台旁的已有衣物与小摆件',


        '42里当前人台可用，你已有可穿戴的衣物和可摆的一件小物；这处屋内暂时能停留。你先怎样布置？',


        '选一组自己想表达的衣物与摆件位置，让这个角落带上自己的风格|以自己已见过的衣物或小摆件种类留意缺口，惦记想要的一套还缺哪类|只实际改一件当前可摆物品的位置，亲手看这次编辑结果|按我给幸存者设定的旧制服习惯，把现有这件制服留在人台上，暂不拿去别处',


        'a c creative_edit_trial r',


        '原生3D摆物和人台，风格/种类动机明示；身份落实留制服r，普通位置编辑0。',


        'PZ9L_42 PZ9L_41',


        ('没用过人台，可答实际最早拿到的小物件：当前屋内有可放位置，一件已有物品确实能摆。你先怎样处理？',


         '选一个和自己想表达的住处风格相合的位置|把已见过的小物件种类作自己的收藏目标，惦记还缺哪类|只实际摆下这件当前能放物件，亲手看这次位置变化|照我给幸存者设定的念旧习惯，把这件已有小物留在当前落脚处，再继续原来安排',


         'a c creative_edit_trial r'),


        '41也已有3D摆物，不错误排除旧版本；只当前可摆物件，不造任意体积缩放、自绘纹理或一键房屋复制。'),


    Q(9, '真实逐次留下来的同一处住所',


        '回想42里真实多次回来改过或住过的同一处住所：哪种已经做过的投入更贴近愿意保留的体验？',


        '接着给同一处住所添防御、储物或生活物件，喜欢先前投入逐渐留在这里|调整过已有摆件与外观，让它表达自己想要的居所风格|明明还有路可走，仍会在熟悉屋内慢慢待一阵|只是为已经搭过的构件与实际步骤补记建设过程',


        'g a h construction_process_recording',


        '真实同一对象持续完善g，不由生存天数自动推养成；风格、熟悉栖居与普通建设记录0分开。',


        'PZ9L_STORE PZ9L_42',


        ('没有反复改住所，可以回想42真实最早拿到与摆过一件物品的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '为它选过一个自己想表达的摆放位置，让小角落有想要的感觉|按我给幸存者设定的念旧习惯，把这件已有物品留在当时落脚处，再继续原来安排|只是实际调整过这件当时可摆物件的位置，亲手看那次变化|只是为已经取得物件与当时位置补记记录',


         'a r creative_edit_trial game_recording'),


        '不要求大基地、固定水电设施、无敌防御或角色一直没死；没有多次完善经历时不硬计g。'),


    Q(10, '真实同一幸存者的技能与亲手练习',


        '回想42里同一名幸存者真实练过的制作、耕作或其他已有技能：哪种已经做过的投入更贴近愿意保留的体验？',


        '多次回来继续练同一角色已有技能，喜欢先前投入逐渐留在等级或可做内容上|专门重复一小段实际工具操作，目的就是把自己的操作练熟|把材料取得、制作、产出与之后补给接成多轮周转，持续调配供给|只是先核对当时已出现的玩法说明，再继续自己的实际尝试',


        'g t y game_reference_first',


        '角色数值持续积累g与玩家本人刻意练操作t区分，持续供给才y；普通说明0，不凭角色职业或等级推玩家能力。',


        'PZ9L_STORE PZ9L_42',


        ('还没有技能积累，可以回想42真实最早近战或用工具的一段：哪种已经做过的动作更贴近愿意保留的投入？',


         '反复练过瞄准、出手或退步时点，专门让这一项操作更熟|亲手使用工具或武器，喜欢声音与眼前变化相连的反馈|只是先核对当时身体状态与已带补给，再决定那轮活动|只是先比较当时已有装备与组件，再决定那轮怎样安排',


         't f survival_status_review compare_available_setup'),


        '不要求技能到某级、录像课必有、所有服务器经验倍率相同或角色死后数值必继承。'),


    Q(11, '真实按幸存者身份走过的路',


        '回想42里真实给这名幸存者设过生活方式的一段：你当时有能用的工具与可走区域。哪种已经做过的动作更贴近愿意保留的体验？',


        '照我给他设定的惜物工匠身份，先收好可留的旧工具，再带备用工具继续|给那轮另定过只在眼前这一段街区找物的小规则，再按自己的玩法尝试|走近一处并非为指定材料而去的陌生地方，想亲眼发现那里是什么|只是为已经取得物件与实际去过的位置补记记录',


        'r i w game_recording',


        '真实身份落实收旧工具行动r、自订街区范围i、未知发现w与普通补记0分开；不由角色职业选择直接定现实人格。',


        'PZ9L_STORE PZ9L_42',


        ('没有自订生活方式，可以回想42实际读过的一份传单或报纸：哪种已经做过的动作更贴近愿意保留的体验？',


         '回看已读文字，把它讲的人和事件与前后经历接起来|按我给幸存者设定的记录习惯，先记下已读内容与地点，再继续可走路段|只是先核对当时已经出现的基础玩法说明，再继续自己的实际尝试|只是为已读信息与当时位置补记记录',


         's r game_reference_first game_recording'),


        '只已经实际读过的文字，不造可招募NPC、Kate/Baldspot任务、狗伙伴或官方剧情分支。'),


    Q(12, '真实同游时先搜街还是补住处',


        '回想42里确有其他真人同游的一段：有人想去下一段街区，有人想先补已知住处。哪种你真实做过的动作更贴近愿意保留的投入？',


        '先谈清这轮共同想完成什么，商量谁带哪些已有物品、谁走哪段与何时再集合|先陪同伴在落脚处走走聊天，喜欢大家一起待着的陪伴|问过愿意参加的人，约定这轮只搜眼前一个街区的小规则再一起玩|只是为已经参与的住处建设与实际步骤补记过程',


        'q o i construction_process_recording',


        '原生在线或分屏的实际真人，协商共同目标、陪伴与自订且同意分别有证据；NPC计划功能不能当已实装同伴。',


        'PZ9L_STORE PZ9L_42 PZ9L_GAME',


        ('只有单人经历，可以回想42真实最早在一处落脚点处理已有物品的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '给那轮另定过只在眼前屋内收整的小规则，再照自己的玩法尝试|按我给幸存者设定的念旧习惯，先把当时可留的一件物品存好，再继续原来安排|在自己已熟悉的地方慢慢待一阵，享受暂时安稳的感觉|只是按当时已有物品调整一轮携带、存放或丢弃，再继续活动',


         'i r h item_handling_action'),


        '不保证世界进度、死亡后人物、物品或MOD跨版本兼容，不要求语音、公共服务器或竞技排行。'),


]





PZ_41 = [


    Q(1, '旧41存档里的落脚屋与下一条街',


        '你玩的是原生Build41或legacy41：已经有一处走熟的落脚屋，当前食水可查看，门外有一段能接近但没看过的街道。你先怎样过这一段？',


        '走近没去过的街道，想亲眼知道那边的建筑与路口是什么|先核对当前身体状态与已带食水，再决定这一轮怎样活动|排清已有补给、这段去向与回落脚屋的安排，再照这趟准备行动|留在熟悉屋内慢慢收拾，享受这里暂时安稳的感觉',


        'w survival_status_review mission_preparation_plan h',


        '旧41自由生存的发现与栖居取舍，不套42新地下室、动物或预设名称；状态和一次准备0。',


        'PZ9L_STORE PZ9L_41 PZ9L_LEGACY',


        ('没有自己的落脚屋，可答41最早实际打开容器搜取的一段：眼前已有能取物品，背包当前有这次空间。你先怎样处理？',


         '先核对身体状态与已有补给，再决定这轮怎样活动|实际调整这一轮已有物品的携带、存放或丢弃，再继续搜取|以自己已见过的物品种类留意缺口，惦记慢慢补进想要的一套|只为已经拿到的物品与发现地点补记记录',


         'survival_status_review item_handling_action c game_recording'),


        '41的Apocalypse/Survivor/Builder为当时预设，不把当前42预设套过来；具体僵尸、水电与死亡规则仍以本次存档为准。'),


    Q(2, '41窗边已有工具的一次加固',


        '旧41存档里一扇窗当前可加固，你已选定这轮要处理它，所需工具与材料手边够，附近也能动手。你先怎样安排？',


        '先核对当前已列的加固材料与已有物件，确认这次条件|排清这一轮取料、带到窗边与逐步装上的先后，再亲手照顺序做|按已经选定的这扇窗目标实际加固，把眼前建设需求推进|直接进行一项当前可做的加固操作，亲手体验它怎样发生',


        'objective_requirement_review physical_tool_action_sequence stated_objective_progress available_operation_trial',


        '真实41防御建设，四项普通条件/单轮流程/既定目标/操作精确0；不把按已知配方封窗当解谜或系统经营。',


        'PZ9L_STORE PZ9L_41',


        ('还没加固窗户，可答41最早已有工具的一项制作：配方已开、材料够，你已选定本轮工具需求。先怎样继续？',


         '先核对这项已选工具列出的材料要求与手头物件|排清取料、制作与收回余料的先后，再亲手做这一轮|按已经选定的工具目标制作，把眼前需求推进|直接做这一件当前可做工具，亲手体验操作发生',


         'objective_requirement_review physical_tool_action_sequence stated_objective_progress available_operation_trial'),


        '不给固定木板/钉子数、不保证绝对防僵尸；不给41安排42工作站、全新材料输入界面或全配方解锁。'),


    Q(3, '41已经种过的地块与留种',


        '旧41里你已实际种过这片地，当前作物与水能查看，手边也有当前可用种子和用具。你先怎样投入？',


        '继续回到同一片地照料，喜欢前几轮投入逐渐留下的变化|把留种、种植、补水、收成与后续食物储备接成几轮周转，持续调配供给|以自己实际见过的作物种类留意缺口，惦记补进还没种过的那类|只先核对当前地块、作物与已有材料状态，再决定这一轮怎样处理',


        'g y c production_state_review',


        '41原生耕作，持续同一对象、多轮供给和种类动机分别明确；普通状态查看0，不借42季节新作物。',


        'PZ9L_STORE PZ9L_41',


        ('没有种过地，可以答41实际料理过的食材：当前炉具能用，已有一份确实可料理的食物与容器。你先怎样安排？',


         '把食材取得、料理和后续储备接成几轮周转，持续调配生活供给|只先核对当前食材、容器与已有产物状态，再决定这一轮怎样处理|排清这次取食材、放入容器、料理与收整的先后，再亲手做|直接料理当前这一份可用食物，亲手体验操作发生',


         'y production_state_review physical_tool_action_sequence available_operation_trial'),


        '不用42最佳播种月份、食草动物产出、固定收成天数或现实可食安全保证；只当时真实可种可做的内容。'),


    Q(4, '41衣物修补与手边备用衣',


        '旧41里你已有一件能修补的衣物，这次所需针线与材料确实具备；另有一件当前可穿备用衣，已有防护信息能查看。你先怎样继续？',


        '只先比较当前已有衣物和装备信息，再决定这一轮穿哪件|排清这次取材料、修补与收回手边物件的先后，再亲手照顺序做|直接修补这一件当前能修的衣物，亲手体验这项操作|按我给幸存者设定的惜旧习惯，先修好并穿回这件旧衣，再继续原来安排',


        'compare_available_setup physical_tool_action_sequence available_operation_trial r',


        '41已实装Tailoring，当前确能修补才问；普通比较/单轮手工/操作0，身份落实修旧再穿r。',


        'PZ9L_41',


        ('没修过衣物，可答41最早实际换过衣服的一段：当前已有可穿衣物，界面能查看已有外观与防护信息。你先怎样继续？',


         '只先比较当前确实已有衣物与装备信息，再决定这轮穿什么|实际换上这一件当前可穿衣物，亲手体验这次操作|按我给幸存者设定的旧制服习惯，穿回当前这件旧衣再继续原来路段|先核对已经出现的穿戴操作说明，再继续自己的尝试',


         'compare_available_setup available_operation_trial r tool_reference_first'),


        '不保证补料免疫咬伤、不把所有衣物都说成可补洞，也不要求织物数值或现实缝纫知识。'),


    Q(5, '41目标描边与一次实际出手',


        '旧41里当前枪械、对应弹药和瞄准操作确实可用，你能看到一只可接近目标；周围也有退开空间。你想怎样用这一段？',


        '反复练进入瞄准、观察描边与出手的时点，专门把这一项操作练熟|亲手打一轮，喜欢动作、声音与目标反应接连发生的反馈|排清接近、瞄准出手、退开恢复与再次接近的循环，再照当轮安排尝试|只先比较当前已有枪械与装备信息，再决定这一轮采用哪件',


        't f combat_resource_cycle compare_available_setup',


        '41已有瞄准目标描边，不借42精确身体部位新瞄准系统；明确练习/反馈，与本轮循环/装备浏览0分开。',


        'PZ9L_41',


        ('没用过枪，可以答41实际用过的最早近战武器：当前武器能用，眼前一只僵尸可接近，周围能退开。你先怎样投入？',


         '反复练推击、挥击和退步的时点，专门把这一项操作练熟|亲手打一轮，喜欢动作、声音与目标反应相连的反馈|排清接近、出手、退开恢复与再次接近的循环，再照安排尝试|只先核对当前身体状态与已有补给，再决定这一轮怎样行动',


         't f combat_resource_cycle survival_status_review'),


        '不保证绿描边必中、不固定感染或击杀数、不称武器自动静音；只玩家真实已有的工具和场景。'),


    Q(6, '41屋内留下的聚会现场',


        '旧41里你已实际见过一处像是人们曾一起看球、聚会或生活过的屋内现场，相关物件当前仍能查看；屋外也有没看过但可走的一段路。你先怎样继续？',


        '回看已经见到的物件和摆设，想理解这里的人之前经历了什么|走近没看过的路段，想亲眼知道那边是什么|按我给幸存者设定的记录员身份，先记下已见现场，再继续可走路段|只为已经体验的地点与人物线索补记记录',


        's w r game_recording',


        '41真实随机环境叙事，不是已实装NPC支线；故事联系、未知发现、身份落实记录再走与普通补记0分开。',


        'PZ9L_41',


        ('没遇过聚会现场，可以答41实际看过的车辆残骸或路障：当前位置可停留，附近另有能走但没看过的小路。你先怎样继续？',


         '再看已见车辆与路障，把这里的人之前发生的事与已见线索接起来|去看看没走过的小路，暂不为指定物资而走|按我给幸存者设定的记录习惯，先记下当前已见路口，再继续可走路段|只为已见地点与实际取得物品补记记录',


         's w r game_recording'),


        '只已有现场，不造唯一真相、必触发事件、NPC委托或42新增地下室；停留不等于保证安全。'),


    Q(7, '41实际能开的车与短途移动',


        '旧41里你已有一辆当前确实能发动、能操纵的车，眼前一小段路可走，手头补给够短途返回。你先怎样投入？',


        '反复练这辆车的起步、转向与停下，专门把驾驶操作练熟|亲手开这一段，留意转向、车声与道路变化接着发生的反馈|驶近还没看过的下一段路，想亲眼知道那边是什么|排清已有补给、这一小段去向与返回停靠点的安排，再照这趟准备行动',


        't f w mission_preparation_plan',


        '原生41车辆，当前可开条件给足；刻意驾驶训练、即时反馈、未知发现与单次准备0分开。',


        'PZ9L_STORE PZ9L_41',


        ('没有开过车，可答41实际走过的短途街道：前方有能走但没看过的路口，身后有熟悉落脚处。你先怎样继续？',


         '去看看陌生路口那边是什么，暂不为指定物品而走|先核对当前身体状态与已带补给，再决定这一轮怎样活动|排清已有补给、这一小段去向与回落脚点的安排，再照准备行动|回熟悉落脚处慢慢待一阵，享受暂时安稳的地方',


         'w survival_status_review mission_preparation_plan h'),


        '不考钥匙、油量或热接线技能门槛，当前可开不表示无碰撞、无僵尸、车不耗油或跨版本车库兼容。'),


    Q(8, '41已取得的录像带与能用的设备',


        '旧41里你已有一盘实际取得的VHS，当前电视与播放设备能用；这盘你看过的内容确实有人物或事件可回看。你先怎样用这一段时间？',


        '再看已看过的内容，把其中的人和事件前后接起来|以自己已见过的录像种类留意缺口，惦记补进想要的一套|按我给幸存者设定的记录习惯，先记下这盘已看录像的信息，再继续原来安排|直接进行一次当前可用的播放操作，亲手体验它怎样发生',


        's c r available_operation_trial',


        '41原生VHS不是每盘都必涨技能；叙事联系和种类动机明确，身份落实记录再行动r，普通播放0。',


        'PZ9L_41',


        ('没有播过录像，可以答41最早实际看过的地图：地图当前能打开，已显示这片区域的一些位置或标记。你先怎样继续？',


         '先核对已能用地图实际显示的位置与标记，再决定这一段往哪里走|去看看地图附近尚未走过的可达去向，想亲眼知道那边是什么|按我给幸存者设定的记录员习惯，先记下当前已见标记，再继续可走路段|只为自己已经体验过的位置补记记录',


         'navigation_information_review w r game_recording'),


        '只已取得录像与当前可用设备，不保证全图鉴、技能奖励、供电持续或地图显示未知资源。'),


    Q(9, '真实逐次补起来的41落脚屋',


        '回想旧41里真实多次回来完善过的同一处落脚屋：哪种已经做过的投入更贴近愿意保留的体验？',


        '接着给同一处屋添防御或生活物件，喜欢早先投入逐渐留在这里|调整过已有摆件与位置，让住处表达自己想要的风格|明明还有地方可去，仍会回熟悉屋内慢慢待一阵|只是为已经做过的构件与实际步骤补记建设过程',


        'g a h construction_process_recording',


        '旧41同一对象持续投入g，不要求豪宅或幸存天数；表达风格a、熟悉停留h与普通记录0分开。',


        'PZ9L_STORE PZ9L_41',


        ('没有反复完善屋子，可以回想41真实最早摆过一件已有物品的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '为它选过一个和自己想表达的住处风格相合的位置|按我给幸存者设定的念旧习惯，把这件旧物留在当时落脚处再继续|只是实际调整过这件当时可摆物件的位置，亲手看那次变化|只是为已经取得物件与当时位置补记记录',


         'a r creative_edit_trial game_recording'),


        '41已有3D摆物，不强加42新建筑、新动物或头柄系统，没有多次完善时不硬计g。'),


    Q(10, '真实同一角色的修补制作技能',


        '回想旧41里同一幸存者真实多次修补衣物、制作或做其他已有技能活动的一段：哪种已经做过的投入更贴近愿意保留的体验？',


        '继续练同一角色已有技能，喜欢早先投入逐渐留在等级与可做内容上|专门重复一小段亲手工具操作，目的是把自己的操作练熟|把材料取得、制作、产出与后续补给接成多轮周转，持续调配供给|只是先核对当时已经出现的玩法说明，再继续自己的实际尝试',


        'g t y game_reference_first',


        '角色成长g与玩家刻意操作训练t分开；连续供给才y，说明0，不从职业或数值断定玩家能力。',


        'PZ9L_STORE PZ9L_41',


        ('没有技能积累，可以回想41真实最早用过的近战工具：哪种已经做过的动作更贴近愿意保留的体验？',


         '反复练过推击、出手或退步时点，专门让这一项操作更熟|亲手使用工具或武器，喜欢声音与目标变化相连的反馈|只是先核对当时身体状态与已带补给，再决定那轮活动|只是先比较当时已有装备与组件，再决定那轮怎样安排',


         't f survival_status_review compare_available_setup'),


        '不保证任何录像都加经验、固定升级速度、角色死亡后技能继承或41/42存档兼容。'),


    Q(11, '真实穿过旧衣、摆过人台的41时段',


        '回想旧41里真实使用已有衣物或人台的一段：哪种已经做过的动作更贴近愿意保留的投入？',


        '选过一组自己想表达的衣物颜色和轮廓，让幸存者或角落有想要的风格|按我给幸存者设定的旧制服习惯，穿回当时可穿的旧衣再继续原来路段|以自己已见衣物种类留意缺口，惦记补进想要的一套|只是实际换过一件当时可穿衣物，亲手体验那次操作',


        'a r c available_operation_trial',


        '41真实衣物、人台功能；表达风格、身份影响穿旧再出发、明确种类目标与普通换装0分开。',


        'PZ9L_41',


        ('没用过衣物或人台，可以回想41真实给一小段活动加过规则、或最早取物的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '给那轮另定过只在眼前这一栋屋里取物的规则，再照自己的玩法尝试|亲手拿回一件小物品，喜欢输入与物件移动相连的反馈|按我给幸存者设定的惜物习惯，先收好当时可留的一件旧物，再继续原来安排|只是按当时已有物品调整一轮携带、存放或丢弃，再继续活动',


         'i f r item_handling_action'),


        '不从性别、制服、职业或衣物好坏推现实身份；没有编官方外观排行榜、付费服装必需或42新防具配方。'),


    Q(12, '真实41同游时的一段安排',


        '回想旧41里确有其他真人同游的一段：有人想继续搜物，有人想先补落脚屋。哪种你真实做过的动作更贴近愿意保留的投入？',


        '先谈清这轮共同想完成什么，商量谁带已有物资、谁走哪段与何时再集合|先陪同伴走走、聊眼前看到的东西，喜欢大家一起待着的陪伴|问过愿意参加的人，约定只搜眼前一栋屋的小规则再一起玩|只是为已经参与的住处建设与实际步骤补记过程',


        'q o i construction_process_recording',


        '41原生多人实际真人，不拿计划NPC当队友；协商目标、陪伴、自订且同意分别有证据，普通记录0。',


        'PZ9L_41 PZ9L_STORE',


        ('只有单人41经历，就回想真实最早在熟悉落脚处处理已有物品的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '给那轮另定过只在眼前屋内收整的小规则，再照自己的玩法尝试|按我给幸存者设定的念旧习惯，先存好当时可留的一件物品再继续|在已经熟悉的地方慢慢待一阵，享受暂时安稳的感觉|只是按当时已有物品调整一轮携带、存放或丢弃，再继续活动',


         'i r h item_handling_action'),


        '不要求公共服务器、语音或跨版本好友同游，不保证角色技能、存档、物资或MOD随切分支继承。'),


]





PZ_42[0]['variants'].append(_extra(


    '42最早已有的一件小物品',


    '住处与开容器两种情境都不适用，可以答42实际拿到第一件小物品的一段：当前物品已经在手边，可以存取，附近小路也确实能走。你先怎样继续？',


    '只先核对当前身体状态与已带补给，再决定这一轮活动|以自己已经见过的物品种类留意缺口，惦记慢慢补进想要的一套|按我给幸存者设定的惜物习惯，先收好当前这件旧物，再继续可走路段|只给已经取得的这件物品与发现位置补记记录',


    'survival_status_review c r game_recording',


    '第三种最早取物前提不要求住所或容器；种类动机、身份落实存旧再走与状态/补记0分开。',


    'PZ9L_STORE PZ9L_42',


    '不编自动整理、物品无重量、绝对安全或NPC援助；只当前可存取物件。'))


PZ_42[1]['variants'].append(_extra(


    '没制作时的42背包取放',


    '工作站与基础制作都没体验过，可以答42实际打开背包的一段：已有可取出再收回的小物件，当前不需要制作。你先怎样处理？',


    '按已有物品实际调整一轮携带、存放或丢弃，再继续自己的安排|排清这次取出、处理与收回的先后，再亲手照顺序做|直接取出再收回这一件当前可用物品，亲手体验操作发生|先核对已经出现的物品操作说明，再继续自己的尝试',


    'item_handling_action physical_tool_action_sequence available_operation_trial tool_reference_first',


    '不需要任何配方或工作站的另一真实界面操作，四种普通行为精确0。',


    'PZ9L_STORE PZ9L_42',


    '不从背包整理推系统研究、经营或成长；没有臆造某个排序按钮、自动全箱取料或跨服务器共享物品。'))


PZ_42[2]['variants'].append(_extra(


    '没耕作料理时的随身食水',


    '耕作和料理都没体验过，可以答42实际拿到食水的一段：补给已经在当前物品中，身体状态也能查看。你先怎样安排？',


    '先核对当前身体状态与已带食水，再决定这一轮活动|按现有物品实际调整一次携带或存放，再继续自己的安排|以自己实际见过的食物种类留意缺口，惦记补进还没有的那类|只给已经拿到的食物与发现位置补记记录',


    'survival_status_review item_handling_action c game_recording',


    '没有生产经历不硬计y/g；补给查看和已有物品处理/记录0，种类动机明确才c。',


    'PZ9L_STORE',


    '不让未料理者猜配方、食品保质期或疾病；只已取得游戏物品，不保证现实可食安全。'))


PZ_42[3]['variants'].append(_extra(


    '没照料动物作物时的同一住所',


    '动物和作物都没照料过，可以答42实际多次补过的同一处住所：当前还有已开放且材料够做的小构件，附近也是走熟的地方。你先怎样投入？',


    '接着给同一处住所添东西，喜欢早先投入逐渐留在这里|把已有材料取得、制作与下一轮补给接成几轮周转，持续调配建设供给|回熟悉屋内慢慢待一阵，享受暂时安稳的地方|只先核对眼前可见物料与当前已知存量，再决定这一轮怎样处理',


    'g y h material_stock_review',


    '另一真实持续积累对象，不要求42动物或地块；多轮建设供给才y，现场物料0。',


    'PZ9L_STORE PZ9L_42',


    '必须真有多次完善经历才适用，不由房屋大小、生存天数或小构件一次放置推g。'))


PZ_42[4]['variants'].append(_extra(


    '没捕鱼交手时的3D摆物工具',


    '捕鱼和近战都没体验过，可以答42实际用过的3D物品摆放：当前一件小物确实可摆，眼前有可放位置。你先怎样投入？',


    '反复练取出、选位和确认摆放，专门把这一项工具操作练熟|亲手摆这一件，留意输入与物件在眼前出现相连的反馈|只实际改这一件当前可摆物品的位置，亲手看这次编辑结果|先核对已经出现的摆放操作说明，再继续自己的尝试',


    't f creative_edit_trial tool_reference_first',


    '第三种原生操作前提，刻意训练与反馈明确；普通一次编辑和说明0，无未知原因不硬计p。',


    'PZ9L_42 PZ9L_41',


    '41也有3D摆物，不推任意缩放、穿模、全物件悬空或MOD功能；一次摆物不算专门训练。'))


PZ_42[5]['variants'].append(_extra(


    '没见地下现场时的已读报纸',


    '地下室和屋内现场都没经历过，可以答42实际读过的一份报纸：文字当前能回看，附近有可走但尚未看过的去向。你先怎样继续？',


    '再读已见文字，把其中的人和事件与前后经历接起来|走近没看过的去向，想亲眼知道那边是什么|按我给幸存者设定的记录员身份，先记下已读报纸与位置，再继续可走路段|只给这份已读信息与当前位置补记记录',


    's w r game_recording',


    '当前42明确有可读报纸的环境叙事；身份落实记录后行动，普通补记0。',


    'PZ9L_42',


    '只真实已读文字，不编NPC支线、某一期内容、唯一谜底、地图位置或未发布故事。'))


PZ_42[6]['variants'].append(_extra(


    '没用部件衣物时的一件旧工具',


    '部件武器和衣物比较都没体验过，可以答42实际取放过的一件旧工具：当前能取出、收回，附近还可以继续走动。你先怎样处理？',


    '直接取出再收回这件当前可用工具，亲手体验这项操作|按我给幸存者设定的惜物习惯，先把旧工具收好，再继续可走路段|只是按已有物品调整这一轮携带、存放或丢弃，再继续安排|先核对已经出现的物品操作说明，再继续自己的尝试',


    'available_operation_trial r item_handling_action tool_reference_first',


    '不要求装备比较或部件界面；身份落实收旧工具再走r，普通操作/取放/说明0。',


    'PZ9L_STORE PZ9L_42',


    '不保证旧工具可维修、部件可拆、同种能叠或跨版本可用；没有比较组合不硬计b。'))


PZ_42[7]['variants'].append(_extra(


    '没摆物时的已有衣物外观',


    '人台与摆放小物都没体验过，可以答42实际换过的已有衣物：当前可穿，已有外观能查看。你先怎样继续？',


    '选一套自己想表达的颜色与轮廓，让幸存者带上想要的风格|以自己已见过的衣物种类留意缺口，惦记补进想要的一套|只实际换上这一件当前可穿衣物，亲手体验操作发生|按我给幸存者设定的旧制服习惯，穿回这件旧衣再继续原来路段',


    'a c available_operation_trial r',


    '另一真实外观操作前提，不要求摆放；风格和种类动机明确，角色落实穿旧再行动r，普通穿戴0。',


    'PZ9L_42 PZ9L_41',


    '不凭所选衣物、性别或职业推现实身份，不要求特定稀有服装、全衣柜或付费外观。'))


PZ_42[8]['variants'].append(_extra(


    '真实没改住所时的同一角色技能',


    '没有完善住所或摆小物的经历，可以回想42里同一角色真实多次做过的制作或耕作活动：哪种已经做过的投入更贴近愿意保留的体验？',


    '接着练同一角色已有技能，喜欢早先投入逐渐留在等级与可做内容上|反复练过一小段亲手工具操作，专门把自己的操作练熟|只是先核对当时已经出现的玩法说明，再继续实际尝试|只是为已经取得的物件与实际体验过的位置补记记录',


    'g t game_reference_first game_recording',


    '另一真实持续积累对象；角色进展与玩家操作训练分别明确，说明/补记0。',


    'PZ9L_STORE PZ9L_42',


    '不把一次动作、阅读说明或角色职业本身计成长，不保证等级阈值、经验倍率或死后继承。', reflection=True))


PZ_42[9]['variants'].append(_extra(


    '真实没练技能交手时的摆放操作',


    '没有技能积累或武器经历，可以回想42真实摆过一件小物的一段：当时有确实可放的位置。哪种已经做过的动作更贴近愿意保留的体验？',


    '反复练过取出、选位与确认摆放，专门把这一项工具操作练熟|亲手摆下物件，喜欢输入与眼前位置变化相连的反馈|只是实际改过这件当时可摆物品的位置，亲手看那次编辑结果|只是先核对当时已经出现的摆放操作说明，再继续自己的尝试',


    't f creative_edit_trial tool_reference_first',


    '真实另一工具，无技能成长或交战门槛；刻意练习和反馈与普通编辑/说明0分开。',


    'PZ9L_42 PZ9L_41',


    '不从一次放置自动推训练，不编世界编辑器、物体任意缩放或同物件可无限复制。', reflection=True))


PZ_42[10]['variants'].append(_extra(


    '真实没有自订剧情经历时的地图',


    '没有自订生活方式或读报经历，可以回想42真实打开过的地图：当时位置或已有标记确实可查看，附近有能走但没看过的去向。哪种真实动作更贴近愿意保留的体验？',


    '只是先核对地图实际显示的位置与标记，再决定那段往哪里走|走近没看过的去向，想亲眼发现那边是什么|按我给幸存者设定的记录习惯，先记下已见标记，再继续可走路段|只是为实际体验过的位置补记记录',


    'navigation_information_review w r game_recording',


    '另一实际原生导航经历，未知发现与身份落实记录再走明确，地图阅读/补记0。',


    'PZ9L_42 PZ9L_41',


    '只当时已能用的地图与标记，不默认地图显示全部人物或资源，不编未发布NPC任务。', reflection=True))


PZ_42[11]['variants'].append(_extra(


    '真实单人田地旁的自由时段',


    '没有同游或屋内收整经历，可以回想42真实一个人在已有地块旁活动的一段：当时用具可用，也能在熟悉落脚点停留。哪种真实动作更贴近愿意保留的体验？',


    '几次回来接着照料同一片地，喜欢早先投入逐渐留下变化|给那一小段另定过只在当前地块旁活动的规则，再照自己的玩法尝试|先在熟悉地块与落脚处慢慢待一阵，享受暂时安稳的地方|只是先查看当时实际可见作物与材料状态，再决定那轮怎样处理',


    'g i h production_state_review',


    '第三种真实单人经历，不补造真人q/o；持续积累、自订范围、熟悉停留与状态0分开。',


    'PZ9L_STORE PZ9L_42',


    '只当时真实已种地块，不默认当前季节可种、不保证产量、无人袭击或所有服务器规则相同。', reflection=True))





PZ_41[0]['variants'].append(_extra(


    '41当前可打开的已有地图',


    '落脚屋与搜物都没经历过，可以答旧41实际打开过的地图：当前一些位置或标记可见，附近有能走但没看过的小路。你先怎样继续？',


    '先核对地图实际显示的位置与已有标记，再决定下一段往哪里走|去看看没走过的小路后面是什么，暂不为指定物品而走|按我给幸存者设定的记录员习惯，先记下当前已见标记，再继续可走路段|只给自己已经走过的位置补记记录',


    'navigation_information_review w r game_recording',


    '旧41原生地图，不要求住所或搜箱；未知发现、身份落实记录再走与地图/补记0分开。',


    'PZ9L_41',


    '不把42新地图地点、地下室或动物图标套进41，不承诺地图显示全部资源或所有道路安全。'))


PZ_41[1]['variants'].append(_extra(


    '没建设制作时的41小物件',


    '加固和制作都没体验过，可以答旧41实际取放过的小物件：当前能取出再收回，不要求配方或工具台。你先怎样处理？',


    '按已有物品实际调整这一轮携带、存放或丢弃，再继续自己的安排|排清这次取出、处理与收回的先后，再亲手照顺序做|实际取出再收回这件当前可用物件，亲手体验操作发生|先核对已经出现的物品操作说明，再继续自己的尝试',


    'item_handling_action physical_tool_action_sequence available_operation_trial tool_reference_first',


    '没有建设或配方前提的另一种真实操作，四项精确0，不凭普通背包动作推系统经营。',


    'PZ9L_STORE PZ9L_41',


    '不造42工作站输入界面、自动全箱取料、无限容量或不存在的整理按钮。'))


PZ_41[2]['variants'].append(_extra(


    '没种植料理时的41随身食物',


    '旧41耕作与料理都没经历过，可以答真实拿到过食物的一段：补给当前已经在已有物品中，身体状态也能查看。你先怎样继续？',


    '先核对当前身体状态与已带补给，再决定这一轮活动|按已有物品实际调整一次携带或存放，再继续自己的安排|把自己已见过的食物种类当作想补齐的一套，惦记还缺哪类|只给已经取得食物与发现位置补记记录',


    'survival_status_review item_handling_action c game_recording',


    '没有生产经历时不用y/g硬解释；明确种类目标c，普通补给/物品/补记0。',


    'PZ9L_STORE PZ9L_41',


    '不考42种植月份、动物产出或具体食物安全，不保证游戏物品在现实中可食用。'))


PZ_41[3]['variants'].append(_extra(


    '没修补穿戴时的旧工具取放',


    '衣物修补与换装都没经历过，可以答41实际取放过的一件旧工具：当前能取出、收回，附近还有可走路段。你先怎样继续？',


    '先核对已经出现的工具操作说明，再继续自己的实际尝试|实际取出再收回这件当前可用旧工具，亲手体验操作发生|按我给幸存者设定的惜物习惯，先收好旧工具再继续可走路段|只是按当前已有物品调整这一轮携带、存放或丢弃，再继续安排',


    'tool_reference_first available_operation_trial r item_handling_action',


    '第三种已有物品前提；角色身份落实先收旧再走，普通说明/操作/物品0，不借42头柄机制。',


    'PZ9L_STORE PZ9L_41',


    '不承诺工具必能修、任意堆叠或材料免费，不把拾到旧工具都计养成。'))


PZ_41[4]['variants'].append(_extra(


    '没用武器时的41摆物操作',


    '枪械和近战都没体验过，可以答旧41实际用过的3D物品摆放：已有一件当前可摆小物，眼前也有可放位置。你先怎样投入？',


    '反复练取出、选位与确认摆放，专门把这一项工具操作练熟|亲手摆这一件，留意输入与眼前物件位置变化相连的反馈|只实际改这一件当前可摆物品的位置，亲手看编辑结果|先核对已经出现的摆放操作说明，再继续自己的尝试',


    't f creative_edit_trial tool_reference_first',


    '41已有3D摆物，能给无战斗者另一实际工具；刻意练习、反馈、普通编辑/说明0分开。',


    'PZ9L_41',


    '不把3D摆放错排为42专属，不造自由缩放、无限复制或MOD物件编辑。'))


PZ_41[5]['variants'].append(_extra(


    '没遇环境现场时的已看录像',


    '聚会现场和路障都没经历过，可以答旧41实际看过的一盘VHS：当前设备能用，这盘已看内容确实有人物与事件可回看。你先怎样继续？',


    '再看已见内容，把其中的人和事件前后接起来|以自己实际见过的录像种类留意缺口，惦记补进想要的一套|按我给幸存者设定的记录习惯，先记下这盘已看内容，再继续原来安排|只实际进行这次当前可用的播放操作，亲手体验它怎样发生',


    's c r available_operation_trial',


    '另一真实叙事媒介，不造可招募NPC；故事、种类、身份落实记录再行动与普通播放0分开。',


    'PZ9L_41',


    '不编具体录像台词、每盘经验奖励、所有设备都有电或任意录像必有人物故事。'))


PZ_41[6]['variants'].append(_extra(


    '没驾驶远行时的41地图查看',


    '开车和短途陌生街道都没经历过，可以答旧41实际打开地图的一段：当前已显示一些位置与已有标记，你仍在当前可停留处。你先怎样继续？',


    '先核对地图实际显示的位置与标记，再决定这一段往哪里走|按我给幸存者设定的记录员身份，先记下已见标记，再继续原来安排|只先核对当前身体状态与已带补给，再决定这一轮活动|只为自己已经去过的位置补记记录',


    'navigation_information_review r survival_status_review game_recording',


    '另一种原生导航工具，不要求车辆或未知路段；身份落实记录后行动r，导航/身体/补记0。',


    'PZ9L_41',


    '不编地图必显示所有资源、道路绝对安全、自动路线规划或42新地下室。'))


PZ_41[7]['variants'].append(_extra(


    '没有录像地图时的41物品种类',


    'VHS播放与地图都没体验过，可以答旧41真实拿到的几件物品：当前物品已经在手边，有可取放的小物。你先怎样继续？',


    '把自己已见过的物品种类当作一个收藏目标，惦记还缺哪类|按我给幸存者设定的惜物习惯，先收好这件可留旧物，再继续原来安排|实际取出再收回一件当前可用小物，亲手体验这项操作|只给已经取得物品与发现位置补记记录',


    'c r available_operation_trial game_recording',


    '无媒体或地图门槛；明确种类目标才c，身份具体影响收旧再继续r，普通取放/补记0。',


    'PZ9L_STORE PZ9L_41',


    '不从背包满推收集，不造官方全物品奖励或全配方图鉴；也不让未读媒体者猜剧情。'))


PZ_41[8]['variants'].append(_extra(


    '真实没改屋摆物时的同一角色',


    '没有完善住所或摆物经历，可以回想旧41里同一角色真实多次修补、制作或做已有技能活动的一段：哪种真实投入更贴近愿意保留的体验？',


    '继续练同一角色已有技能，喜欢早先投入逐渐留在等级或可做内容上|专门重复过一小段亲手工具操作，目的就是把自己的操作练熟|只是先核对当时已经出现的玩法说明，再继续实际尝试|只是为已经取得物件与实际体验过的位置补记记录',


    'g t game_reference_first game_recording',


    '真实另一持续积累对象，角色成长与玩家操作训练分开，说明和补记0。',


    'PZ9L_STORE PZ9L_41',


    '不保证技能门槛、经验倍率或死后继承；一次普通动作或只看说明不自动计g/t。', reflection=True))


PZ_41[9]['variants'].append(_extra(


    '真实没练技能交手时的41摆放',


    '没有技能积累或近战工具经历，可以回想旧41真实摆过一件已有小物的一段：当时有确实可放位置。哪种真实动作更贴近愿意保留的投入？',


    '反复练过取出、选位与确认摆放，专门把工具操作练熟|亲手摆下物件，喜欢输入与眼前位置变化相连的反馈|只是实际改过这件当时可摆物品的位置，亲手看那次编辑结果|只是先核对当时已经出现的摆放操作说明，再继续实际尝试',


    't f creative_edit_trial tool_reference_first',


    '第三种真实操作前提，训练须专门目的、反馈须明确动机，普通位置编辑/说明0。',


    'PZ9L_41',


    '不借42新编辑功能，也不把3D摆物当42才有；一次普通放置不算训练。', reflection=True))


PZ_41[10]['variants'].append(_extra(


    '真实没穿衣收物时的熟悉路口',


    '衣物与屋内取物两种情境都不适用，可以回想旧41真实站在走熟路口的一段：当时附近有一处能走但没看过的去向。哪种真实动作更贴近愿意保留的体验？',


    '走近没看过的去向，想亲眼知道那边是什么|给那一小段另加过只沿眼前街道活动的规则，再照自己的玩法尝试|按我给幸存者设定的记录习惯，先记下当时路口再继续可走路段|只是先核对当时身体与已带补给的实际状态，再决定那轮活动',


    'w i r survival_status_review',


    '另一真实移动经历，不靠衣物测现实身份；未知发现、自订活动范围、身份落实记录再走与状态0。',


    'PZ9L_STORE PZ9L_41',


    '不保证僵尸不来、额外规则仍能达成任何目标或有NPC委托；角色设定由玩家本人赋予。', reflection=True))


PZ_41[11]['variants'].append(_extra(


    '真实单人41地块旁的时段',


    '没有联机或屋内收整经历，可以回想旧41真实一个人在已有地块旁活动的一段：用具当时可用，也能在熟悉落脚处停留。哪种真实动作更贴近愿意保留的体验？',


    '几次回来继续照料同一片地，喜欢早先投入逐渐留下变化|给那一小段另定过只在当前地块旁活动的规则，再照自己的玩法尝试|在自己已熟悉的地块与落脚处慢慢待一阵，享受暂时安稳的地方|只是先查看当时可见作物与材料状态，再决定那轮怎样处理',


    'g i h production_state_review',


    '真实第三单人情境，无真人就不补q/o；持续投入、自订范围、熟悉停留与生产查看0。',


    'PZ9L_STORE PZ9L_41',


    '不强加42季节作物、动物或全新工作站，不固定产量和生存天数，不保证无危险。', reflection=True))





SEV_SURVIVAL = [


    Q(1, '这一轮确实会到来的血月前',


        '当前世界这一轮确实有血月，你已定下这次防守位置；手头确有两组能换用的武器与适配模组搭配，材料与补给也够，敌人还没到眼前。最后这段准备时间，你先怎样投入？',


        '把材料取得、弹药或器具制作与下一轮补回储备接成周转，持续调整防守供给|用已有武器反复练一段瞄准、出手与退步，专门把这一套操作练熟|比较手头两组确实可换的武器与模组搭配，再检验这一轮的组合效果|排清已有补给、防守位置与退回已知落脚点的安排，再照这次准备行动',


        'y t b mission_preparation_plan',


        '本次确有血月而非所有世界默认；多轮供给、刻意练习、组合检验与单次准备0分开，不从血月成功推能力。',


        'SEV9L_STORE SEV9L_30',


        ('没有血月经历，可答实际最早已能用石斧或近战工具的一段：当前工具可用，眼前木料能处理，旁边能停手退开。你先怎样投入？',


         '反复练出手与退步时点，专门把这一项操作练熟|亲手处理一轮木料，喜欢声音、变化与输入紧接着发生的反馈|排清取工具、处理木料与收整材料的先后，再亲手照顺序做|先核对当前身体状态与已带补给，再决定这一轮怎样活动',


         't f physical_tool_action_sequence survival_status_review'),


        '不固定第七天、尸潮数、敌人能力或死亡掉落；设为无血月者换其他情境，不要求改存档设置。'),


    Q(2, '锻造、工作台与手头供给',


        '当前锻造与一处制作工作台确实能用，本轮原料与燃料已在手边；你也有一项已经选定的制作目标，材料要求可查看。想给之后活动做些能用的东西，先怎样安排？',


        '把原料取得、加工、制作与下一轮储备接成周转，持续调配各处供给|只先看当前燃料、制作材料与已有产物状态，再决定这一轮怎样处理|在现有制作界面排清这一轮确认配方与用料、执行制作和整理产物的先后，再亲自照顺序做|先核对已选制作目标列出的材料要求，确认这次条件',


        'y production_state_review crafting_action_sequence objective_requirement_review',


        '真实多处制作持续周转才y；普通当前状态、一轮流程与已列目标要求0。Sandbox可改制作与科技，题面给当前真实可用条件。',


        'SEV9L_STORE SEV9L_30',


        ('还没用过这些设备，可答实际最早一项基础制作：已选定一项工具需求，它和另一项基础配方都已开放、材料够，当前制作界面可用。你先怎样继续？',


         '先核对已选工具列出的材料要求与手头物件，再决定怎样推进|比较当前已开放且材料够做的基础配方，再决定采用哪项|排清这轮在制作界面确认配方与用料、执行制作和整理产物的先后，再亲自做这一轮|直接做这一件当前可制作工具，亲手体验操作发生',


         'objective_requirement_review compare_production_options crafting_action_sequence available_operation_trial'),


        '不说任意废弃工作站都能用、不强行全配方开启、不固定烧成秒数或将无制作预设当普通生存；已选目标不假造NPC要求。'),


    Q(3, '当前已接下的一项贸易商任务',


        '当前世界任务功能开启，你已经接下一项能执行的贸易商任务，已有地点说明、目标与奖励可查看；这段出行补给也已具备。你先怎样继续？',


        '先阅读已经出现的任务与地点说明，核对目标、交付条件和可去位置，再决定这一趟是否前往|排清已有补给、任务地点与返回路线的安排，再照这一趟准备行动|按当前已经接下的这项任务要求行动，以推进它的完成为重点|先去一处可达但没看过的地方，想亲眼发现那里是什么，暂不为任务奖励而走',


        'mission_briefing_review mission_preparation_plan stated_objective_progress w',


        '真实NPC任务不是与真人协商q；说明、单次准备、推进0，未知发现须有不为指定奖励的目的。',


        'SEV9L_STORE SEV9L_30',


        ('没接过任务、或当前任务关闭，可答实际看过的贸易商货架：交易当前开启，货架有一件付得起且当前能用、自己还没持有过这一类的基础工具；身上也带着一件旧工具，物件信息、价格与支付条件能看。你先怎样继续？',


         '先核对已显示的支付条件与已有货币，再决定这次买什么|直接买下当前这项可支付物件，亲手体验一次可用交易|先比较身上旧工具与当前这件可支付工具的已有装备信息，再决定这次采用哪件|先买当前这件付得起的工具，专门想补进自己这套工具还缺的一类',


         'objective_requirement_review available_operation_trial compare_available_setup c'),


        '不保证贸易商每时都开、任务和交易必启用、固定奖励或任务重置永不影响建筑；没有任务者不要求强行去接。'),


    Q(4, 'Combine Station里的现有两件装备',


        '当前Combine Station确实可用，你已持有两件界面允许合并的同类物件，实际属性能比较，这次合并操作也满足条件。你先怎样继续？',


        '先比较当前已有装备与属性，再决定这一轮采用哪件或怎样合并|排清这次取物、放入当前设备、合并与收回的先后，再亲手照顺序做|直接合并这一组当前可合物件，亲手体验操作发生|按我给幸存者设定的惜物习惯，先保留当前这件仍可用旧物，暂不把它合掉',


        'compare_available_setup physical_tool_action_sequence available_operation_trial r',


        '3.0原生CombineStation不等于每件物品都能互合；普通比较、单轮设备流程、操作0，身份落实暂留旧物r。',


        'SEV9L_30',


        ('没用过CombineStation，可答实际装过武器模组的一段：当前已有一件可用武器与两份确实适配的模组，能在可用位置轮流装入，确有两组可换搭配。你先怎样继续？',


         '比较这件武器与两份模组分别组成的当前可换搭配，再实际检验组合效果|只先比较当前已有装备与组件，再决定这一轮怎么安排|直接装入其中一份当前适配模组，亲手体验这次操作发生|先核对已经出现的装备操作说明，再继续自己的尝试',


         'b compare_available_setup available_operation_trial tool_reference_first'),


        '不固定品质、百分比或所有模组都随品质增强；维修方法可被改，不从合并站存在推所有装备可修或修后不衰退。'),


    Q(5, '已有地块里的作物与下一轮食物',


        '当前确实已能耕种，你有实际照料过的同一片作物；现有种植格有合法空位，手头有一类还没种过但现在能种的已得种子，已知种子取得途径也还能用，用具与料理条件允许接着活动。你先怎样投入？',


        '继续回到同一片地照料，喜欢先前投入逐渐留在这处作物上的变化|把已有种子来源、播种、收成和料理接成几轮周转，持续调配生活供给|先在现有空位播下这类还没种过的已得种子，想把自己惦记的作物种类补进这一套|只先查看当前作物、地块与已有材料状态，再决定这一轮怎样处理',


        'g y c production_state_review',


        '持续同一地块、连续供给和种类动机分别明确，普通查看0。种子掉落与生长可调，不假定收成必留够下一轮。',


        'SEV9L_STORE SEV9L_30',


        ('没种过地，可答实际已料理并取进背包的一份食物：当前能用，身体与已有补给可查看。你先怎样安排？',


         '先核对当前身体状态与已带补给，再决定这一轮活动|按已有物品实际调整一次携带或存放，再继续自己的安排|把自己实际见过的食物种类列成想补齐的一套，先圈出这轮惦记补进的一类|只为已经取得的食物与发现位置补记记录',


         'survival_status_review item_handling_action c game_recording'),


        '种子掉落、生长和产量按当次真实世界，不保证收成留够下一轮。替代的食物情境明确已经取进背包且当前可用，避开当前3.4营火直接食用已知问题；不考现实食物安全。'),


    Q(6, '已有建筑块与可涂的一面墙',


        '这段自己精力够，角色食水和当前建造材料也够；你在已经熟悉的住处，已有能放的建筑块、填色工具与一面确实可涂旧墙，还能继续新建造目标。没有迫近防守，先怎样过这段？',


        '选自己想表达的轮廓和表面，让这处建筑带上个人风格|按我给幸存者设定的惜旧习惯，只修当前这一小角，其他旧痕迹先留着|只给这面墙的一小块换一种当前可用纹理，让图案或配色改变，亲手看这次编辑结果|在熟悉的住处旁慢慢待一阵，享受这片已经走熟的地方',


        'a r creative_edit_trial h',


        '原生建筑形状和填色，不需要全物品自由取用或DLC。风格、角色落实只改小角与熟悉停留分开，一项普通编辑0。',


        'SEV9L_STORE',


        ('没有用过填色，可答最早放过基础建筑块的一段：当前构件与材料够用，有确实可放的位置。你先怎样投入？',


         '把这几块排成自己想表达的住处轮廓|按我给幸存者设定的朴素定居者身份，先只补当前基本门洞，暂不另加门面装饰|只实际放下一块当前可建构件，亲手体验操作发生|先核对已出现的建造操作说明，再继续自己的实际尝试',


         'a r available_operation_trial tool_reference_first'),


        '不假定全方块可涂、无材料消耗、无结构倒塌或默认飞行，身份由玩家本人设定而非职业直接给分。'),


    Q(7, '未去过的POI与现成指示牌',


        '当前你站在一处还没进入的可达POI外，眼前有实际能读的商铺或设施指示牌，也有已经能走到的入口；手头食水够短途返回。你先怎样继续？',


        '走近还没看过的内部，想亲眼知道里面的空间与东西是什么|只先查看当前已可达的入口、通道和现场，再决定这段怎样继续|排清已有补给、进入哪一小段与返回落脚点的安排，再照这趟准备行动|按我给幸存者设定的记录员身份，先记下已见招牌和入口，再继续可走部分',


        'w scene_inspection mission_preparation_plan r',


        '真实POI与3.0环境指示牌，未知发现与身份具体行动明确；现场查看和一次准备0。没有从商业牌自动编剧情任务。',


        'SEV9L_STORE SEV9L_30',


        ('还没进过POI，可答最早实际看过地图的一段：当前世界允许地图，已显示的一些位置或标记能看，附近有一段可走但没看过的路。你先怎样继续？',


         '先核对地图实际显示的位置与已有标记，再决定下一段往哪里走|去看看没走过的路后面是什么，暂不为指定产物而走|按我给幸存者设定的记录员身份，先记下已见标记，再继续当前能走的路段|只给自己已经走过的位置补记记录',


         'navigation_information_review w r game_recording'),


        '不假定地图/指南针必开、每POI必有同样敌人或任务；SignTech原生自定义牌属于另条编辑器题路，不借给普通生存玩家。'),


    Q(8, '当前允许的维修与一件旧工具',


        '当前世界这次维修方式确实允许，你有一件能修旧工具与所需物件，界面已经显示条件；身旁也有一件当前可用替代工具。你先怎样继续？',


        '先核对这次已显示的维修材料要求与手头物件，再决定是否执行|先换用旁边这件当前能用的替代工具，亲手体验它怎样发挥|直接进行这次确实可用的维修，亲手体验操作发生|按我给幸存者设定的惜物工匠身份，先修好旧工具并继续用，暂不换替代品',


        'objective_requirement_review try_available_setup available_operation_trial r',


        '维修方法与衰退可自定义，当前可修才问；条件、单轮操作与普通修理0，身份具体影响修旧再用r，不从一次修理计长期养成。',


        'SEV9L_30 SEV9L_STORE',


        ('没修过工具、或世界不允许当前维修，可答实际拿到替代工具的一段：当前已有两件确实能用，装备信息可看。你先怎样继续？',


         '先比较当前已有两件工具与已显示的装备信息，再决定这一轮采用哪件|直接换用这件当前可装备工具，亲手体验操作发生|按我给幸存者设定的惜物习惯，先把可留旧工具收好，再拿备用工具继续|先核对已经出现的装备操作说明，再继续实际尝试',


         'compare_available_setup available_operation_trial r tool_reference_first'),


        '不保证维修不降耐久、死亡掉落必可找回或任何工具都能合并；未允许维修不要求改Sandbox设置。'),


    Q(9, '真实同一幸存者的点数与读书',


        '回想同一幸存者真实多次获得点数、读过已有书籍或推进制作技能的时段：哪种已经做过的投入更贴近愿意保留的体验？',


        '接着完善同一角色已有技能，喜欢先前投入逐渐留在可做内容或角色进度上|以自己实际见过的书籍种类留意缺口，惦记想要的一套还缺哪类|用当时已有工具反复练出手和退步时点，目的就是让自己的操作更熟|只是先核对当时已经出现的玩法说明，再继续自己的实际尝试',


        'g c t game_reference_first',


        '角色持续进度g、书籍种类c、玩家刻意训练t明确区分；进度规则可调，没有读书体系不强迫虚构经历。',


        'SEV9L_STORE SEV9L_30',


        ('没有技能或书籍积累，可以回想最早真实使用石斧等基础工具的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '反复练过出手与退步时点，专门让这一项操作更熟|亲手处理木料，喜欢声音与眼前变化紧接着发生的反馈|只是先核对当时身体状态与已带补给，再决定那轮活动|只是排清当时取工具、处理材料与收整的先后，再亲手做那一轮',


         't f survival_status_review physical_tool_action_sequence'),


        '不固定杂志数量、书籍奖励、最高科技或死亡后技能保留，也不从角色职业或等级推现实能力。'),


    Q(10, '真实逐次改过的同一处基地',


        '回想你真实多次回来扩过、修过或住过的同一处基地：当时自己精力够、角色补给够，也有新地方可去或新部分可建。哪种已经做过的投入更贴近愿意保留的体验？',


        '接着给同一基地添防御或生活设施，喜欢早先投入逐渐留在这里|调整过已有构件与表面，让它表达自己想要的建筑风格|明明还有地方可去，仍会在熟悉基地里慢慢待一阵|只是为已经建过的构件、连接与实际步骤补记建设过程',


        'g a h construction_process_recording',


        '真实同一对象持续完善才g，普通修一次不算；风格、熟悉栖居与建设记录0分开，不由基地大或尸潮过关定能力。',


        'SEV9L_STORE',


        ('还没反复改基地，可以回想真实最早放过的几块基础构件：哪种已经做过的动作更贴近愿意保留的体验？',


         '把这几块排成自己想表达的住处轮廓|按我给幸存者设定的朴素定居者身份，先只补当时基本门洞，暂不另加门面装饰|只是实际放过一块当时可建构件，亲手体验那次操作|只是给已经放过的构件与步骤补记过程',


         'a r available_operation_trial construction_process_recording'),


        '不要求电网、炮塔、最高材质或无敌结构，不把AlmostCreative预设当全构件取用权限。'),


    Q(11, '真实两组武器与模组的比较',


        '回想你真实用过两组确实适配的武器与模组搭配，或反复练过一段出手的时段：哪种已经做过的投入更贴近愿意保留的体验？',


        '比较过当时确实可换的两组搭配，再出手检验组合带来的差异|专门反复练过瞄准、出手与退步时点，想把自己的操作练熟|亲手打一轮，喜欢声音、动作与目标反应接连发生的反馈|只是先比较当时已有装备与组件，再决定那轮怎样安排',


        'b t f compare_available_setup',


        '实际比较并检验组合效用才b，刻意重复才t；普通装备浏览0，不从装一件模组就推配装研究。',


        'SEV9L_STORE SEV9L_30',


        ('没有武器模组经历，可回想真实最早用近战工具处理木料的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '反复练过出手、退开与再靠近时点，专门把工具操作练熟|亲手处理木料，喜欢声音和变化与输入相连的反馈|只是排清当时靠近、出手、退开恢复与再靠近的先后，再照安排做那一轮|只是先核对当时身体状态与已带补给，再决定那轮活动',


         't f tool_operation_plan survival_status_review'),


        '不固定伤害、Magnitude百分比、模组槽数或必胜，也不让未开启战斗者想象击杀经历。'),


    Q(12, '真实同游时先做任务还是补基地',


        '回想确有其他真人同游的一段：有人想继续已有任务，有人想先补基地，当前都能商量。哪种你真实做过的动作更贴近愿意保留的投入？',


        '先谈清这轮共同想完成什么，商量谁带哪些已有物品、谁走哪段与何时再集合|先陪同伴在落脚处走走聊天，喜欢一起待在这里的陪伴|只是排清当时已有补给、这次选定的任务去向与返回基地的先后，再照那轮准备行动|只是为已经参与的基地建设与实际步骤补记过程',


        'q o mission_preparation_plan construction_process_recording',


        '真实同游的目标协商q与陪伴o分开，单趟补给去向安排和已做建设记录0；普通单个POI活动范围不计自创玩法。NPC贸易商不是其他真人。',


        'SEV9L_STORE SEV9L_CURRENT',


        ('只有单人经历，或从未一起做任务，可以回想真实在熟悉基地旁处理物品的一段：当时手头有一件仍可保留的旧工具，自己精力够、角色补给够，也还有新地方可去或新部分可做。哪种已经做过的动作更贴近愿意保留的体验？',


         '只是为当时已经取得的物品与发现位置补记记录|按我给幸存者设定的惜物习惯，先收好当时可留的一件旧工具再继续|在熟悉基地旁慢慢待一阵，享受暂时安稳的地方|只是按当时已有物品调整一轮携带、存放或丢弃，再继续安排',


         'game_recording r h item_handling_action'),


        '不要求语音、公共服、PvP或任务必开；没有对手与排名不把个人用时或角色等级计竞争人格。'),


]





SEV_SURVIVAL[0]['variants'].append(_extra(


    '没有血月和砍木时的3.4背包筛选',


    '血月准备和基础工具使用都没经历过，可以答实际用过的3.4背包搜索：包里已有几件物品，包括一件仍能保留的旧工具，搜索栏与类别筛选当前可用。你先怎样继续？',


    '直接输入一项已有物品名称或选一个当前类别，亲手体验这次筛选|先核对已经出现的背包操作说明，再继续自己的尝试|把自己已见过的物品种类列成补全清单，先圈出这轮惦记补进的一类|按我给幸存者设定的惜物习惯，先把筛出的可留旧工具收好，再继续原来安排',


    'available_operation_trial tool_reference_first c r',


    '真实当前3.4新界面功能，不需要战斗或木料；种类目标与身份具体收旧行动明确，普通筛选/说明0。',


    'SEV9L_CURRENT SEV9L_33',


    '只筛已有物品，不造自动跨箱取料、菜单生成物品或AlmostCreative权限；旧版没用过可继续换。'))


SEV_SURVIVAL[1]['variants'].append(_extra(


    '没制作时的容器中已见材料',


    '多处设备与基础制作都没体验过，可以答实际打开过的容器：里面有当前能取的材料；背包已带一份基础材料，也容得下这次再取的一份。你先怎样处理？',


    '先核对眼前实际可见物料与当前已知存量，再决定这一轮怎样处理|按已有物品实际调整一轮携带、存放或丢弃，再继续自己的安排|直接取回这一份当前能取材料，亲手体验操作发生|只给已经取得材料与发现位置补记记录',


    'material_stock_review item_handling_action available_operation_trial game_recording',


    '无配方或工作站前提，物料查看、已有物品处理、一次取物与记录精确0，没有持续加工不硬计y。',


    'SEV9L_STORE SEV9L_CURRENT',


    '不保证每个旧箱有同样物件、不推地图任务必开，也不造自由物品菜单或无限容量。'))


SEV_SURVIVAL[2]['variants'].append(_extra(


    '任务和交易都关闭时的自主路段',


    '任务和交易两种情境都不适用，可以答实际自主走过的一段：当前附近有一处可达但没看过的建筑外侧，身后有已知落脚点，补给够这一趟。你先怎样继续？',


    '去看看建筑外侧还没见过的部分，想亲眼知道那边是什么|先核对当前身体状态与已有补给，再决定这一轮活动|排清已有补给、这一小段去向与回落脚点的安排，再照这趟准备行动|按我给幸存者设定的记录员身份，先记下已见建筑外侧与返回落脚点，再继续可走路段',


    'w survival_status_review mission_preparation_plan r',


    '原生自主探索不要求NPC交易任务；未知发现、身份落实记录再走与状态/一次准备0分开。',


    'SEV9L_STORE SEV9L_30',


    '不要求改Sandbox、不保证建筑有任务或奖励，不把当前可达理解成绝对无危险。'))


SEV_SURVIVAL[3]['variants'].append(_extra(


    '没有合并装模组时的已有工具',


    'CombineStation和装模组都没经历过，可以答实际拿到两件已有工具的一段：当前都能装备，已有信息可看。你先怎样继续？',


    '先比较当前已有工具与装备信息，再决定这一轮采用哪件|实际换用这件当前可装备工具，亲手体验操作发生|按我给幸存者设定的惜物习惯，先收好当前可留旧工具，再拿备用工具继续|先核对已经出现的装备操作说明，再继续实际尝试',


    'compare_available_setup available_operation_trial r tool_reference_first',


    '无合并或模组槽要求，普通比较/装备/说明0；身份具体影响收旧换备r，不把普通浏览当组合研究b。',


    'SEV9L_STORE SEV9L_30',


    '只当前实际持有工具，不固定品质差、属性百分比、维修方法或装备一定更优。'))


SEV_SURVIVAL[4]['variants'].append(_extra(


    '没有耕种料理时的最早小材料',


    '作物和料理都没经历过，可以答实际最早收过小材料的一段：眼前木石或草料确实可取，已有物品可看，背包容得下这一份。你先怎样投入？',


    '把自己实际见过的材料种类列成补全清单，先圈出这轮惦记补进的一类|亲手拿回这一份材料，喜欢输入与眼前变化相连的反馈|只先查看眼前实际可见物料与当前已知存量，再决定这一轮怎样处理|只是按现有物品调整这一轮携带、存放或丢弃，再继续安排',


    'c f material_stock_review item_handling_action',


    '无食物生产前提，种类动机c、反馈f与物料/物品0明确；不硬计经营或成长。',


    'SEV9L_STORE',


    '只当前可取的普通材料，不让玩家凭现实经验尝草木，不造一份材料解锁全部配方。'))


SEV_SURVIVAL[5]['variants'].append(_extra(


    '还未建造时的最初外观选择',


    '涂装和基础建筑块都没体验过，可以答最初实际创建角色的一段：当前已有外观选项能看，还没确认入场。你先怎样选择？',


    '选一组自己想表达的轮廓与颜色，让幸存者有想要的风格|先浏览当前确实开放的外观方案，再决定采用哪种|只实际改一项当前可用外观设置，亲手看这次编辑结果|先核对已经出现的外观操作说明，再继续自己的尝试',


    'a creative_option_review creative_edit_trial tool_reference_first',


    '第三种原生创作前提，不要求已经放构件；明确风格a与普通浏览/一项编辑/说明0分开。',


    'SEV9L_STORE',


    '不从性别、职业、外貌推现实身份或角色代入，不要求购买新外观包、导入MOD或游戏内随时能回捏脸。'))


SEV_SURVIVAL[6]['variants'].append(_extra(


    '没有POI地图时的背包搜索结果',


    'POI和地图两种情境都不适用，可以答实际用过的3.4背包搜索：当前已有物品，筛出的类别或名称结果可看。你先怎样继续？',


    '直接对一项已有物品作当前可用的搜索，亲手体验结果怎样出现|按我给幸存者设定的记录员身份，先记下已经取得的这批物品，再继续原来安排|把自己已见过的物品种类列成补全清单，先圈出这轮惦记补进的一类|只是按现有物品调整一次携带、存放或丢弃，再继续安排',


    'available_operation_trial r c item_handling_action',


    '另一实际界面前提，不强求地图、导航或空间探索；身份落实记录后继续与种类动机明确，普通搜索/物品0。',


    'SEV9L_CURRENT',


    '不把搜索已有物品变成CreativeMenu取新物品，也不编全部容器共享、自动生成路线或隐秘人物。'))


SEV_SURVIVAL[7]['variants'].append(_extra(


    '没修理换工具时的已选基础制作',


    '维修和替代工具都没经历过，可以答最早实际制作过的小工具：当前制作界面可用，已选这项工具与另一项基础配方都已开、材料够，能查看各自要求。你先怎样继续？',


    '先核对已选工具列出的材料要求与手头物件，确认这次条件|排清这轮在制作界面确认配方与用料、执行制作和整理产物的先后，再亲自照顺序做|直接做这一件当前可制作工具，亲手体验操作发生|先比较当前已开放且材料够做的基础配方，再决定这一轮采用哪项',


    'objective_requirement_review crafting_action_sequence available_operation_trial compare_production_options',


    '无维修方式或备用装备要求的第三前提，条件/单轮流程/普通操作/既定目标精确0。',


    'SEV9L_STORE SEV9L_30',


    '不以配方已开代替材料够，不从一次制作自动推经营或成长，也不要求改世界科技上限。'))


SEV_SURVIVAL[8]['variants'].append(_extra(


    '真实没有技能工具经历时的背包筛选',


    '没有技能读书积累或基础工具经历，可以回想3.4里真实用过的背包搜索：当时已有一批物品，搜索与类别筛选可用。哪种真实动作更贴近愿意保留的体验？',


    '把自己当时已见的物品种类列成补全清单，圈出惦记补进的一类|亲手改过搜索或类别，喜欢输入与结果立即变化相连的反馈|只是实际做过一次当时可用的搜索，亲手体验那次操作|只是为已经取得物品与发现位置补记记录',


    'c f available_operation_trial game_recording',


    '真实第三种原生操作，种类目标与即时反馈明示，普通搜索和补记0；没角色积累不硬计g。',


    'SEV9L_CURRENT',


    '只已持有物品，不造虚构图鉴、自由取物权限或全物品收齐成就。', reflection=True))


SEV_SURVIVAL[9]['variants'].append(_extra(


    '真实未建基地时的同一角色进度',


    '没有基地或建筑块经历，可以回想同一幸存者真实多次获得点数、读书或推进已有技能的一段：哪种真实投入更贴近愿意保留的体验？',


    '接着完善同一角色已有技能，喜欢先前投入逐渐留在可做内容或进度上|反复练过一小段亲手操作，专门让自己的操作更熟|只是先核对当时已经出现的玩法说明，再继续实际尝试|只是为已经取得的物件与实际体验过的位置补记记录',


    'g t game_reference_first game_recording',


    '真实另一持续积累对象，角色成长与玩家操作训练分开，普通说明/记录0。',


    'SEV9L_STORE SEV9L_30',


    '只当时真实启用且发生过的技能进度，不要求书籍机制必开、固定升级量、死亡后保留或最高科技相同。', reflection=True))


SEV_SURVIVAL[10]['variants'].append(_extra(


    '真实没有武器工具时的跑跳操作',


    '没有武器模组或处理木料经历，可以回想真实最早在可走地面移动的一段：当时能走、跑或跳，也有停手空间。哪种真实动作更贴近愿意保留的投入？',


    '反复练过起跑、停步或落地时点，专门把这一项操作练熟|亲手移动，喜欢步伐、落地与眼前变化随输入回应的感觉|只是先核对当时身体状态与已带补给，再决定那轮活动|只是先核对当时已经出现的移动操作说明，再继续实际尝试',


    't f survival_status_review tool_reference_first',


    '第三种实际操作，不要求武器与战斗；刻意训练、即时反馈与普通状态/说明0分开。',


    'SEV9L_STORE SEV9L_30',


    '不固定速度、跳高、体力恢复或跑酷技能门槛，不把自我练习当对手排名。', reflection=True))


SEV_SURVIVAL[11]['variants'].append(_extra(


    '真实单人作物旁的活动',


    '没有同游或基地收物经历，可以回想真实一个人在已种地块旁活动的一段：用具可用，自己精力与角色补给充足，也还能做新目标或回熟悉落脚处。哪种真实动作更贴近愿意保留的体验？',


    '几次回来接着照料同一片地，喜欢早先投入逐渐留下变化|只是按当时已有工具和物件调整一次携带或存放，再继续安排|在已经熟悉的地块与落脚处慢慢待一阵，享受安稳停留|只是先查看当时作物与已有材料的实际状态，再决定那轮怎样处理',


    'g item_handling_action h production_state_review',


    '第三真实单人经历，不借真人q/o；持续同一作物g、精力/新内容具备时的主动熟悉停留h与当前生产查看/已有工具物品处理0分开，普通地块范围不计发明。',


    'SEV9L_STORE SEV9L_30',


    '只当时实际启用且已有作物的经历，不固定生长速度、种子掉落、产量或无敌人规则。', reflection=True))





SEV_CREATIVE = [


    Q(1, '自由取构件的一间废土小店',


        '你已在当前世界启用原生CreativeMenu，普通建筑块当前可取；街面已有一小段可保留的旧木质外观，正想给这间小店补入口和通往后院的部分，不必先为这些构件搜材料。你先怎样开始？',


        '先错开门口与屋檐，留一条穿到后院的路，让小店表达自己想要的废土气质|按我给幸存者设定的惜物店主身份，先保留当前旧木质街面外观，再只补入口这一段|排清这轮选择现有构件、确认入口位置与放下基础块的先后，再照本轮施工安排做|先浏览当前菜单确实可取的构件与形状方案，再决定采用哪种',


        'a r construction_action_plan creative_option_review',


        '真实已启用原生取物菜单；风格表达与本人幸存者身份如何改变入口布置分开，单轮施工和当前构件比较0。普通同类方块限制不计自创玩法。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没搭过小店，可以答自由取物后最早试的几块基础方块：当前菜单能取，地面有确实可放位置。你先怎样玩？',


         '把这几块排成自己想表达的入口轮廓|按我给幸存者设定的朴素工匠身份，先只补当前可放的基本门洞，暂不另加门面装饰|只改变当前待放构件的落点或朝向，再实际放下，亲手看这次编辑结果|先看看当前可取的基础块方案，再决定采用哪种',


         'a r creative_edit_trial creative_option_review'),


        '菜单启用只解决当前物件取用，不推飞行、无敌、无饥渴、无结构规则、所有开发者物件或世界无敌人。'),


    Q(2, '伸出去的混凝土边与支撑',


        '当前世界的结构规则仍在，一小段挑出的建筑块没按你预想稳定下来，你还没确认哪处连接影响它；取物菜单与当前支撑构件可用。你先怎样处理？',


        '猜是这一侧连接不足，保持别处不变，只补一根当前支撑，检验这次是否改变|先把挑出轮廓改成自己想表达的样子，重视这处外观|排清拆哪块、补哪段与再接上挑出部分的先后，再照这一轮施工安排做|只给当前待放的一块基础构件切换一种已有造型，再实际放下，亲手看这项编辑结果',


        'p a construction_action_plan creative_edit_trial',


        '本作原生结构稳定性仍适用，未知因果的单项可失败试验才p；普通施工和一项编辑0。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没遇过承重问题，可以答最初在地面接墙的一段：当前基础块能取，也有可放位置。你先怎样继续？',


         '把这一小段接成自己想表达的转角轮廓|排清这一轮先选位置、放哪块与最后收尾的先后，再照施工安排做|只实际转向并放下一块当前可用构件，亲手看这项编辑|先核对已出现的放置操作说明，再继续自己的尝试',


         'a construction_action_plan creative_edit_trial tool_reference_first'),


        '不保证补一根必能稳定、不说菜单关闭结构倒塌，也不要求玩家真毁掉已有大建筑来验证。'),


    Q(3, '同一面墙的现有涂装纹理',


        '当前填色工具与可用纹理已在手，入口和后院各有一面现在确实可涂的建筑块。你想让这两处看起来有所区别，先怎样投入？',


        '挑不同的现成纹理搭配，让街面与后院表达自己选定的生活气氛|只给其中一块当前可涂表面换一种已有纹理，让图案或配色改变，亲手看这次编辑结果|反复练选纹理、瞄准与涂面的操作，专门把这一套工具练熟|先浏览当前已开放的纹理预览，再决定采用哪种',


        'a creative_edit_trial t creative_option_review',


        '普通世界原生纹理涂装，不冒充PrefabSignTech任意RGBA图层。风格、刻意练习与普通编辑/预览0分开。',


        'SEV9L_STORE SEV9L_CREATIVE SEV9L_PREFAB',


        ('没用过填色，可以答自由取物后最早选建筑块的一段：当前形状方案能看，地面有可放位置。你先怎样投入？',


         '选几块基础构件排成自己想表达的小入口|只实际放下一块当前可用构件，亲手体验操作发生|反复练选块、转向与确认落点，专门把工具操作练熟|先浏览当前能取的构件与形状预览，再决定采用哪种',


         'a available_operation_trial t creative_option_review'),


        '不承诺任意方块可涂、自由调每种纹理RGB、导入图片或免费外观DLC；只当前实际可用表面与工具。'),


    Q(4, '基础块形状与一小段门廊',


        '当前你已取到确实有可选形状的建筑块，这一小段门廊可以施工，形状和朝向方案都已可看。你先怎样玩？',


        '选一个自己想表达的斜面与门框轮廓，让这处门廊带上个人风格|先比较当前确实可用的形状与朝向方案，再决定这一处采用哪种|只切换一项当前可用形状或朝向，亲手看这次预览结果|排清选形状、确认朝向与落位这一轮的先后，再亲手照顺序做',


        'a creative_option_review creative_edit_trial creative_workflow_plan',


        '当前可选形状的基础块，不是任意拉伸；风格表达、单轮编辑流程与当前方案比较/实际一项形状编辑0分开。只限制两种形状不计自创玩法。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没有做过门廊，可以答当前菜单里确实可取的普通基础块：有几种已开放的基础形状可看，地面也有可放位置，不需要复杂结构。你先怎样投入？',


         '把几块排成自己想表达的一小段轮廓|先比较当前已经能用的基础块方案，再决定采用哪一种|只实际放下这一块当前能建方块，亲手体验操作发生|先排清这轮选位、放块与收尾的编辑步骤，再亲手照顺序做',


         'a creative_option_review available_operation_trial creative_workflow_plan'),


        '不造任意缩放、全块都有同样形状或单一门廊必能承重，只有当前确实可选的方案。'),


    Q(5, '已经接好的门与供电线路',


        '当前你确实已搭好可用供电装置、线路和一扇原生电力门，但这次门没按预想动作，你还没确认原因；接线工具与可改连接当前可用。你先怎样处理？',


        '猜是最后这段连接有问题，保持其他供电与开关设置不变，只改这一段再检验|排清这次停下操作、核对现有连接、改线与再次试门的先后，再照这一轮流程做|先核对已经出现的接线操作说明，再继续自己的尝试|实际改这一处当前可改连接，亲手体验这项操作怎样发生',


        'p creative_workflow_plan tool_reference_first available_operation_trial',


        '本作原生电力门与未知连接原因，单项可失败检验才p；已给当前可用设备，普通流程/说明/可用操作0。连线操作不硬套只写尺寸位置造型颜色的creative_edit_trial完整copy。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没用过电力，可以答普通门旁一段旁墙的问题：门口实际不够通畅，你还没确认哪块影响经过；手头原生工具确实能拆掉这一块，也能在可放位置重建同类方块。你先怎样处理？',


         '猜是这块旁墙挡住，保持门和别处不变，只拆改这一块，再亲自走一次检验|排清这次确认位置、调整旁墙与再走一遍的步骤，再照这一轮流程做|先核对已出现的建造操作说明，再继续实际尝试|只用当前可用方式拆掉这一块，在可放位置重建同类方块，亲手看这次位置编辑结果',


         'p creative_workflow_plan tool_reference_first creative_edit_trial'),


        '不指定供电口数、电压、固定开关编号或不需要电源；不把Prefab触发组界面借给普通世界电力工具。'),


    Q(6, '当前可摆的桌椅与储物角',


        '原生取物菜单当前能给你一组确实可摆的桌椅与储物构件，建筑内有可放位置，入口旁也已有自己先前摆下的一张旧桌。你先怎样安排这处生活角？',


        '选一组自己想表达的材质和摆法，让生活角带上想要的风格|按我给幸存者设定的惜物店主身份，先保留入口旁已有旧桌，再只补一处当前可放储物角|先比较当前确实可取的桌椅与储物构件外观，再决定采用哪项|只把一件当前待放家具的落点移到可用位置再放下，亲手看这次位置编辑结果',


        'a r creative_option_review creative_edit_trial',


        '只当前可取可放的真实构件；风格、本人幸存者身份如何改变留旧桌选择与当前方案比较/待放位置编辑0分开，普通一组家具范围不计发明。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没有用过桌椅，可答最初已能取的普通建筑块：当前可以在地面接出一小段墙，形状和位置可选。你先怎样玩？',


         '把这一角做成自己想表达的住处轮廓|按我给幸存者设定的朴素定居者身份，先只做基本门洞，暂不另加门面装饰|先比较当前已经能取的基础块形状，再决定采用哪种|只改变一块当前待放构件的落点，再实际放下，亲手看这次位置编辑结果',


         'a r creative_option_review creative_edit_trial'),


        '不保证所有菜单物件可自由移动、全部物品已显示或可以任意缩放；只有本次确实可摆的物件。'),


    Q(7, '自由取物菜单里的构件种类',


        '当前CreativeMenu已启用，你已实际看过几类基础形状与装饰，能取到本轮想试的普通物件；旁边也有可摆放的空位。你先怎样投入？',


        '以已见类别作一套自己的小陈列，先取出并摆上还没摆过的一类当前可用构件，想把惦记的类别试齐|选一组当前可用构件搭出自己想表达的外观|先浏览当前菜单确实可选的构件或外观预览，再决定采用哪种|只实际取出一件当前可取物件，亲手体验这项操作',


        'c a creative_option_review available_operation_trial',


        '无资源成本也可以有本人明确的陈列种类目标c；不把任意打开目录当收集。风格表达与浏览/取物0分开。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('还没取过装饰，可以答最早浏览过的基础块菜单：当前几种确实可选形状已能看，也有能放基础块的位置。你先怎样投入？',


         '从已见基础形状中选一种这次还没摆过的，实际放下来，想把自己惦记的类别试齐|选几块排成自己想表达的入口轮廓|只是先浏览当前已开放的构件方案，再决定采用哪种|只实际取出一块当前可取方块，亲手体验操作发生',


         'c a creative_option_review available_operation_trial'),


        '不编稀有掉落、付费装饰必须、全方块成就或一键得到全部开发者物件；不是资源生存解锁题。'),


    Q(8, '真人一起用取物菜单搭基地',


        '当前确有其他真人在同一世界和你一起自由建造，大家都已有当前可用构件；有人想加楼层，有人想先做入口。你怎样参与？',


        '先谈清这轮共同想完成什么，商量谁改哪片、哪些地方留着一起决定|先陪同伴逛逛已有建筑、聊正在搭的东西，喜欢同处这里的陪伴|先比较当前确实可用的基础块与表面方案，再决定这一轮采用哪种|先把自己这一角搭成想表达的轮廓与表面风格',


        'q o creative_option_review a',


        '真实世界同游而非Prefab假协作；共同目标协商q、陪伴o、个人风格a与当前可用构件方案比较0分开，不以普通同类方块限制计发明。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('只有单人经历，可答自由取物后的最早小角落：当前普通建筑块能取，附近有走熟落脚处；此刻自己精力够、角色补给够，也还能继续搭新部分。你先怎样投入？',


         '按我给幸存者设定的朴素定居者身份，先只补基本门洞，暂不另加门面装饰|只改变一块当前待放构件的落点或朝向，再实际放下，亲手看这次编辑结果|先回熟悉落脚处慢慢待一阵，享受安稳停留|只实际放下一块当前可用构件，亲手体验操作发生',


         'r creative_edit_trial h available_operation_trial'),


        '菜单权限逐人按当前实有，不造同伴必有管理员权、全部物资共享、语音必开或任务进度必同步。'),


    Q(9, '真实逐次添起来的同一处自由建筑',


        '回想自由取物时真实多次回来完善过的同一处建筑：当时自己精力和角色补给充足，还能继续搭新部分。哪种已经做过的投入更贴近愿意保留的体验？',


        '接着给同一处添楼层、入口或生活角，喜欢早先投入逐渐留在这里|调整过已有构件和涂装纹理，让它表达自己想要的建筑风格|明明还能继续建，仍回熟悉角落慢慢待一阵|只是为已经建过的构件、连接与实际步骤补记建设过程',


        'g a h construction_process_recording',


        '资源自由取用不否定同一作品持续积累g；但一次放块不算g。风格、熟悉栖居与记录0分开。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('只搭过最初几块，也可回想当时真实的投入：自己精力和角色补给够，附近有走熟的小角落，也能接着搭新部分。哪种已经做过的动作更贴近愿意保留的体验？',


         '后来又回来完善同一小块建筑，喜欢早先投入留在这里|把这几块排成自己想表达的轮廓|在自己已走熟的小角落慢慢待一阵，享受安稳停留|只是为已经放过的构件与步骤补记过程',


         'g a h construction_process_recording'),


        '不以规模、资源数、服务器天数或建筑没倒定人格，也不保证角色、创意权限或旧世界跨版本兼容。'),


    Q(10, '真实处理过的结构或通道问题',


        '回想自由取物时真实处理建筑支撑、门口通道或连接的一段：哪种已经做过的投入更贴近愿意保留的体验？',


        '对当时尚未确认的原因提出猜想，只改一处连接或旁墙再检验|反复练过选块、转向与确认落位，专门让工具操作更熟|只是先比较当时已有的构件与可用形状方案，再决定这一轮采用哪种|只是调整过当时待放方块的落点或朝向，再实际放下，亲手看那次编辑结果',


        'p t creative_option_review creative_edit_trial',


        '真实尚未确认原因的单项检验p与刻意训练t分开，已有构件方案比较/待放位置或朝向编辑0；普通构件范围限制不计发明。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没有复杂结构问题，可以回想最初实际放基础块的一段：哪种已经做过的动作更贴近愿意保留的体验？',


         '反复练过选块、转向与落位时点，专门把工具操作练熟|只是先比较当时已经可用的基础块与形状预览，再决定采用哪种|只是调整过待放构件的落点或朝向，再实际放下，亲手看那次编辑结果|只是为已经放过的构件与步骤补记过程',


         't creative_option_review creative_edit_trial construction_process_recording'),


        '不说自由取物就忽略结构规则，不让玩家必须毁已有建筑、不编所有编辑可一键撤销。'),


    Q(11, '真实试过的涂装与形状工具',


        '回想自由取物时真实用过纹理涂装、形状选择或建筑块放置的一段：哪种已经做过的投入更贴近愿意保留的体验？',


        '专门重复一小段选纹理、转向或落位操作，想把这一项工具练熟|选过当时可用的形状或现成纹理表面，让建筑表达自己想要的风格|亲手编辑，喜欢构件或纹理随输入立刻变化的反馈|只是先浏览当时确实开放的构件与纹理预览，再决定采用哪种',


        't a f creative_option_review',


        '本作原生建筑与纹理工具，不当任意RGB图层编辑；刻意训练、风格与即时反馈明确，普通浏览0。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没涂过纹理，可以回想最早实际取过、放过一块基础块：哪种已经做过的动作更贴近愿意保留的体验？',


         '反复练过取块、选位与落下，专门把这一项操作练熟|为这一小处选过自己想表达的轮廓|亲手放下构件，喜欢输入后它马上出现在眼前的反馈|只是先看当时已开放的基础块方案，再决定采用哪种',


         't a f creative_option_review'),


        '不由作品好看、建得快或造得大判断能力；没有武器组合或对手时不强计b/k。'),


    Q(12, '真实按自己设定建的一处入口',


        '回想自由取物时真实安排过的一处入口或生活角：哪种已经做过的动作更贴近愿意保留的体验？',


        '照我给幸存者设定的惜物店主身份，先留当时已有旧构件外观，再只补这处当前能建的一小段|只是先比较当时已经可用的基础块与形状方案，再决定采用哪种|亲手放块或涂表面，喜欢输入后眼前立刻变化的反馈|只是为当时已经搭过的这处构件与实际步骤补记建设过程',


        'r creative_option_review f construction_process_recording',


        '本人赋予幸存者的身份影响已有构件与基础搭建选择r；操作反馈f与当前方案比较、已做建设过程记录0分开，普通同类方块限制不计自创玩法。',


        'SEV9L_STORE SEV9L_CREATIVE',


        ('没有入口或生活角经历，可以回想最早实际试过的几块方块：哪种已经做过的动作更贴近愿意保留的体验？',


         '按我给幸存者设定的朴素工匠身份，先用当时这类基础块做一小段实用矮墙，暂不另加装饰|只是先比较当时已经可用的基础块与形状预览，再决定采用哪种|亲手放下一块，喜欢输入与构件出现相连的反馈|只是为当时已经放过的构件与步骤补记过程',


         'r creative_option_review f construction_process_recording'),


        '角色设定由玩家本人赋予，不从形象、职业或建筑题材推现实身份；不假造NPC店主剧情或系统开店玩法。'),


]





SEV_CREATIVE[0]['variants'].append(_extra(


    '尚未搭建时的原生角色外观',


    '小店和基础块都没搭过，可以答最初实际创建角色的一段：当前已有外观方案可看，还没确认入场。你先怎样选择？',


    '选一组自己想表达的轮廓与颜色，让幸存者带上想要的风格|先浏览当前确实开放的外观方案，再决定采用哪种|只实际改一项当前可用外观设置，亲手看这次编辑结果|先核对已经出现的外观操作说明，再继续自己的尝试',


    'a creative_option_review creative_edit_trial tool_reference_first',


    '无建筑前提的另一真实创作工具，风格动机a与普通预览/一项设置/说明0分开。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '不说取物菜单允许随时捏脸、飞行或无敌，不要求付费外观或从所选身体特征推现实身份。'))


SEV_CREATIVE[1]['variants'].append(_extra(


    '没有承重接墙时的涂装工具',


    '结构支撑和基础墙都没体验过，可以答实际用过的原生填色工具：现有纹理可选，眼前有当前确实可涂的一面建筑块。你先怎样投入？',


    '选一组自己想表达的纹理，让这一面带上想要的风格|反复练选纹理、瞄准与涂面的操作，专门把工具用熟|只把这一面换成另一种现有纹理，让图案或配色改变，亲手看编辑结果|先浏览当前能用的纹理预览，再决定采用哪种',


    'a t creative_edit_trial creative_option_review',


    '另一真实工具，未遇未知支撑原因就不硬计p；明确风格、训练与普通编辑/预览0。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '原生纹理选择不是PrefabSignTech的RGBA颜色图层，不保证所有建筑面或装饰物可涂。'))


SEV_CREATIVE[2]['variants'].append(_extra(


    '没涂装搭建时的当前取物类别',


    '涂装和基础块搭建都没体验过，可以答实际打开过的CreativeMenu：当前类别筛选可用，一组普通物件确实可取。你先怎样投入？',


    '先浏览当前确实可取的构件和外观方案，再决定采用哪种|直接选择当前一类、取出一件可用物件，亲手体验这项操作|以自己已见构件种类作一套想试摆齐的小目标，惦记还缺哪类|先核对已经出现的菜单操作说明，再继续自己的实际尝试',


    'creative_option_review available_operation_trial c tool_reference_first',


    '第三种原生目录取物前提，不要求已经施工；本人明确种类目标才c，普通预览/取物/说明0。',


    'SEV9L_CREATIVE SEV9L_STORE',


    '只菜单当下确实显示的普通物件，不造全开发者物品、稀有掉落或打开目录就计收集。'))


SEV_CREATIVE[3]['variants'].append(_extra(


    '没形状搭建时的一个涂装范围',


    '形状门廊与基础块都没搭过，可以答实际用过的纹理涂装：当前工具、几种现有纹理与一面可涂墙具备。你先怎样玩？',


    '选一组自己想表达的表面，让这一面有想要的感觉|先比较当前确实可用的纹理预览，再决定这面墙采用哪种|只给这一块当前可涂表面换一种现有纹理，让图案或配色改变，亲手看编辑结果|排清这一轮选纹理、确认目标与涂面的先后，再亲手照顺序做',


    'a creative_option_review creative_edit_trial creative_workflow_plan',


    '另一原生涂装经历；风格表达与本轮编辑流程、已有预览/一项颜色图案编辑0分开，普通纹理数量限制不计自创玩法。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '不用自绘图片、任意RGB或预制件选区填满功能，不把编辑器工具混入普通世界取物菜单。'))


SEV_CREATIVE[4]['variants'].append(_extra(


    '没用电力或门口问题时的现成表面',


    '电力接线和门口通行问题都没体验过，可以答实际用过的一处原生涂装：当前有可涂建筑块与已可用纹理，不需要判断任何未知原因。你先怎样继续？',


    '只给这一面换一种当前可用纹理，让图案或配色改变，亲手看这次编辑结果|先排清这一轮选工具、选纹理与涂面的先后，再亲手照顺序做|先核对已经出现的涂装操作说明，再继续自己的尝试|选一个自己想表达的表面搭配，让这个小角落带上想要的风格',


    'creative_edit_trial creative_workflow_plan tool_reference_first a',


    '不编电路或通道谜题，普通一项编辑/流程/说明0，只有明确风格目的a。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '只有当下确实可涂的建筑块，不保证任何道具能涂、不要求电力或管理员控制台。'))


SEV_CREATIVE[5]['variants'].append(_extra(


    '没有家具方块施工时的旧墙表面',


    '桌椅与基础块施工都没经历过，可以答实际用过的纹理工具：眼前已有一面当前可涂旧墙，几种现成可用纹理能预览，工具也可用。你先怎样处理？',


    '挑一组自己想表达的表面，让旧墙这一角带上想要的风格|按我给幸存者设定的惜旧工匠身份，只涂当前旧墙这一小块，其余先留原样|先比较当前确实可用的纹理预览，再决定这次采用哪种|只给这一小块换一种现有纹理，让图案或配色改变，亲手看编辑结果',


    'a r creative_option_review creative_edit_trial',


    '另一真实涂装经历；本人角色身份落实只改小块留旧r，个人风格a与当前纹理比较/一次图案配色编辑0分开，普通纹理数量限制不计发明。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '旧墙可涂由题面明确，不保证每一种物件支持涂装，也不把墙面材质变成现实价值判断。'))


SEV_CREATIVE[6]['variants'].append(_extra(


    '没有目录类目经历时手头一件可摆物',


    '装饰目录与基础块类目都没浏览过，可以答实际用过的现成物件：当前手头已有一件能摆的小物，眼前也有可放位置。你先怎样投入？',


    '给它选一个与自己想表达的生活角风格相合的位置|只实际摆下这一件当前可放物品，亲手体验操作发生|亲手摆这一件，留意输入与物件出现在眼前相连的反馈|先核对已经出现的放置操作说明，再继续自己的尝试',


    'a available_operation_trial f tool_reference_first',


    '无需目录或种类收藏前提，风格、即时反馈明确，普通放置/说明0，没有种类目标不硬计c。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '只手头当前确实能摆物件，不保证所有拾取道具可自由移动或菜单内全部物件可见。'))


SEV_CREATIVE[7]['variants'].append(_extra(


    '没有同游搭块时的单人涂装',


    '真人合作和最早搭块都没体验过，可以答真实单人用过的纹理工具：当前已有可涂墙面、现成纹理与能用工具。你先怎样过这段？',


    '选一组自己想表达的表面搭配，让这个角落带上自己的风格|按我给幸存者设定的惜旧工匠身份，只涂当前墙面这一小块，其余先留原样|先比较当前确实可用的纹理预览，再决定这一轮采用哪种|只给这一面换一种当前可用纹理，让图案或配色改变，亲手看编辑结果',


    'a r creative_option_review creative_edit_trial',


    '第三真实单人涂装，不借真人q/o；本人身份落实留旧r、风格a与当前纹理比较/一项图案配色编辑0分开，普通单纹理限制不计发明。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '不把单人编辑器和世界同游混为一谈，也不借PrefabSignTech的文本图层或颜色工具。'))


SEV_CREATIVE[8]['variants'].append(_extra(


    '真实没施工时的同一处表面完善',


    '没有扩过建筑或最早基础块经历，可以回想真实多次涂过同一处表面的一段：当时纹理工具与可涂面确实可用，自己精力和角色补给够，也还有新的可改部分。哪种真实投入更贴近愿意保留的体验？',


    '几次回来接着完善同一角落，喜欢早先投入逐渐留在这处布置上|选过一组自己想表达的纹理，让这一处有想要的风格|明明还能继续改，仍在熟悉角落慢慢待一阵|只是为已经改过的表面与实际步骤补记过程',


    'g a h construction_process_recording',


    '真实同一布置多次完善才g，不要求施工规模或资源成本；风格、熟悉停留与过程记录0分开。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '一次换纹理不自动计长期成长，也不假造所有表面、天气或光照都可任意设置。', reflection=True))


SEV_CREATIVE[9]['variants'].append(_extra(


    '真实没碰结构时的纹理工具操作',


    '没有结构问题或基础块落位经历，可以回想真实用过的纹理涂装：哪种已经做过的动作更贴近愿意保留的体验？',


    '反复练过选纹理、瞄准与涂面的操作，专门把这一项工具练熟|只是为当时已经涂过的墙面与实际步骤补记建设过程|只是给一面当时可涂墙换一种现有纹理，让图案或配色改变，亲手看那次结果|只是先看当时已开放的纹理预览，再决定采用哪种',


    't construction_process_recording creative_edit_trial creative_option_review',


    '真实另一工具，无未知因果不硬计p；刻意工具训练t与一次预设纹理编辑、当前预览和实际建设过程补记0分开，不以两纹理限制计发明。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '不从反复换纹理或编辑失败直接推t/i，只本人明确动机；没有任意RGB或图像导入保证。', reflection=True))


SEV_CREATIVE[10]['variants'].append(_extra(


    '真实没施工时的目录取物操作',


    '没有涂装或基础块放置经历，可以回想实际打开CreativeMenu选物的一段：当时类别筛选与当前普通物件确实可取。哪种真实动作更贴近愿意保留的体验？',


    '反复练过切类别、选物与取出，专门把这一套菜单操作练熟|把自己当时已见过的构件种类列成想试齐的小清单，圈出惦记还缺的一类|亲手选择一件当时可取物品，喜欢输入后物件马上到手的反馈|只是先浏览当时确实可用的构件方案，再决定采用哪种',


    't c f creative_option_review',


    '第三种真实操作，刻意训练和种类目标明确，反馈与普通目录浏览0分开。',


    'SEV9L_CREATIVE',


    '只本人的真实菜单体验，不把一次点击算训练、不造全开发者道具或收集成就。', reflection=True))


SEV_CREATIVE[11]['variants'].append(_extra(


    '真实尚未放块时的构件领取',


    '没有入口或最初方块放置经历，可以回想真实从CreativeMenu取过物件的一段：当时可取基础构件里有旧木外观，也有另一种当前可选材质。哪种真实动作更贴近愿意保留的投入？',


    '按我给幸存者设定的惜物建造者身份，先领取当时可取的旧木外观构件备用，暂不另换新材质|只是先比较当时已经可用的基础块材质与形状方案，再决定采用哪种|亲手取出一件物品，喜欢输入后它马上到手的反馈|只是实际领取一件当时可取物品，亲手体验那次操作',


    'r creative_option_review f available_operation_trial',


    '真实目录领取，无落位前提；本人身份落实选旧木备用r与反馈f、当前构件方案比较/普通取物0分开，普通领取范围不计发明。',


    'SEV9L_STORE SEV9L_CREATIVE',


    '不造NPC店主任务、材料稀缺成本或额外权限。本人赋予角色的惜物身份不等于官方模式；普通领取同类物件不当自创玩法。', reflection=True))





SEV_PREFAB = [

    Q(1, '单独Prefab里尚未定下的入口',

      '你在原生Prefab Editor里编辑一栋单独建筑，已有可放的墙、地板和门；这次只做本地作品，不是在生存存档里赶血月。入口位置还没定，你先怎样投入？',

      '先用现有构件做出自己想表达的店面轮廓，让入口带上这栋建筑的风格|按我给建造者设定的朴素工匠身份，先只做当前可放的基本门洞，暂不加门面装饰|排清这一轮地板、门洞与墙面落位的先后，再照施工安排做|先比较当前目录里确实可放的门与墙形状，再决定这次采用哪项',

      'a r construction_action_plan creative_option_review',

      '单独作品的入口设计；风格表达与本人赋予建造者的角色设定如何改变行动分开，单轮施工和目录浏览0。不是玩家职业测量。',

      'SEV9L_33 SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没做过完整门面，可答实际第一次在单独Prefab里放方块：当前已选到一种能放的基础块，眼前有可用位置。你先怎样投入？',

       '把这几块排成自己想表达的小屋轮廓|反复练选择、转向与确认放置，专门把编辑操作练熟|亲手放下一块，留意输入与眼前方块出现相连的反馈|只实际放下这一块当前可用构件，亲手看操作发生',

       'a t f available_operation_trial'),

      '不承诺默认地形尺寸、键位、文件夹、进入生存世界或自动被随机地图采用；题面只问原生编辑器里实际可用构件。'),

    Q(2, '复制的一段墙怎样接到转角',

      '已有一段墙可以用编辑器选区复制，当前旋转和粘贴操作都可用；你刚复制出的转角没有对齐，还没确认原因。你想在同一Prefab把这一处接好，先怎样继续？',

      '猜转角不齐是选区多包含了一列，保持朝向和落点不变，只重选范围再粘一次检验|反复练选区、旋转与粘贴，专门把这套操作练熟|把现有墙段转成自己想表达的折线外观，优先表现建筑风格|排清这一轮选区、复制、转向和落位的先后，再照安排做',

      'p t a construction_action_plan',

      '确有未确认的选区猜想才p，不把复制一次计创新；刻意练习、风格与单轮施工分别表达。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没复制过墙段，可答实际转过一个基础构件：当前可选的形状与旋转预览确实能用，旁边有可放位置。你先怎样继续？',

       '反复练选形、转向与确认，专门让这一套操作更熟|亲手转一次再放下，喜欢输入和朝向变化紧接着发生的反馈|只调整这一件当前可用构件的朝向或位置，看这次编辑结果|先核对已出现的编辑操作说明，再继续自己的尝试',

       't f creative_edit_trial tool_reference_first'),

      '不固定复制快捷键、选区体积或所有物件都可镜像；猜想不预告为真实原因，不保证所有编辑可撤销。'),

    Q(3, '另开Playtest才发现的卡住处',

      '你已经保存单独Prefab并实际进入原生Playtest，试走时在自己做的门口卡住；还不确定是门洞尺寸还是旁边构件挡路。回到可编辑的作品后，你先怎样处理？',

      '保留门洞尺寸，只去掉旁边一件怀疑挡路的构件，再另开试玩检验猜想|先排清保存当前作品、只改这一处与再试玩的步骤，再照这轮安排做|把门口改成自己想表达的开阔门廊，优先追求外观感觉|只先查看当前门洞和旁边已有构件的位置，核对眼前实际结构',

      'p construction_action_plan a device_status_review',

      '未知通行原因的单变量检验才p；保存与再试玩是一次编辑流程0，静态结构查看用装置/结构状态0，不把它当因果诊断。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没用过Playtest，可答实际在编辑器里查看自己一处窄门洞：当前两侧方块和一件附近装饰都能看见，也能编辑。你先怎样处理？',

       '把入口改成自己想表达的宽门廊轮廓|只实际改变旁边这一件可编辑构件的位置，亲手看改动结果|先排清拆哪块与补哪块的先后，再照本轮安排做|只先查看门洞与旁边构件当前的实际结构，再决定怎样改',

       'a creative_edit_trial construction_action_plan device_status_review'),

      '原生Playtest与生存存档不混用；不承诺自动保留试玩改动、自由通行、结构绝对安全或猜想必对。'),

    Q(4, '同一房间的明暗预览',

      '当前编辑器里调预览时间的功能确实可用，你有同一房间及已放好的窗洞、墙面；一处角落比自己预想暗，还没确认原因。这里不要求接电或跑生存任务，先怎样看这一处？',

      '切换当前可预览的时段，挑让这间屋子呈现自己想要气氛的样子|怀疑这面墙挡住光线，保持预览时间和其他构件不变，只改墙上这一处开口，观察暗处是否变化|只先核对眼前已有窗洞与墙面的实际结构，再决定这一轮怎样处理|先比较当前已经可用的构件和表面外观，再决定采用哪种',

      'a p device_status_review creative_option_review',

      '气氛表达a与尚未知原因的单项检验p分开；查看当前结构、比较可用外观0。不把切换时间本身计创造。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没有调整预览时间的经历，可答实际给一面墙选过当前可用表面的时段：这面墙现在能编辑。你先怎样继续？',

       '选自己想表达的材质外观，让这一角带上作品风格|亲手换这一处可用表面，喜欢输入与眼前变化相连的反馈|只给这一处换一种当前可用表面纹理，让图案或配色改变，看本轮编辑结果|先比较已经可用的表面方案，再决定采用哪种',

       'a f creative_edit_trial creative_option_review'),

      '不借旧攻略断言当前具体时间滑杆、所有灯具、光照算法、性能效果或任意RGB；预览时间不是生存计时承诺。'),

    Q(5, '需要检查的Sleeper位置与区域',

      '你实际使用过Prefab Editor的Sleeper位置及区域工具；作品里有一处已放的Sleeper位置和打算让它使用的区域能查看，但尚未确定上轮试玩没出现预期表现的原因。你先怎样继续？',

      '猜那处位置在区域外，保持区域与其他配置不变，只把这个Sleeper位置重新布到同一现有区域内，再另开试玩检验|只先查看已经显示的位置、区域与连接关系，核对当前实际信息|排清这一轮重新布置这个位置、保存与再试玩的先后，再照这轮施工安排做|先核对已经出现的该工具操作说明，再继续自己的实际尝试',

      'p device_status_review construction_action_plan tool_reference_first',

      'Sleeper位置与预期使用区域分开；未知位置关系的单项试玩检验p，当前区域/结构查看76与单轮重新布置保存试玩0分开，不假造某个归属下拉字段。',

      'SEV9L_PREFAB_START SEV9L_33',

      ('没接触过Sleeper工具，可答实际在Prefab中摆过一件普通构件：当前物件有可放位置，已有放置操作说明。你先怎样继续？',

       '反复练选位、转向与确认放置，专门让工具操作更熟|亲手摆这一件，喜欢输入与位置变化相连的反馈|只实际改这一件可放构件的位置，看本轮编辑结果|先核对当前已出现的放置说明，再继续实际尝试',

       't f creative_edit_trial tool_reference_first'),

      '不固定敌人数、激活距离或每轮必刷；不借2020指南保证2026面板字段与按钮原样。没有工具经历就换题，不能用“当前可用”挽救已移除机制。'),

    Q(6, '给自制建筑写一块SignTech牌',

      '你在原生编辑器实际用过3.0已加入的SignTech；当前这块牌的文字与颜色层确实可编辑，建筑入口也已做好。你先怎样投入？',

      '安排文字与色块，让牌子表达这栋建筑想给人的风格|按我给建造者设定的惜旧工匠身份，先保留当前已有文字，只修一处色块，暂不换整牌|只实际改当前这一处色块的颜色，看这次编辑结果|先比较当前工具里实际开放的牌面方案，再决定采用哪种',

      'a r creative_edit_trial creative_option_review',

      '3.0已发布的原生牌面编辑，不要求MOD；风格与自己赋予建造者的身份落实行为分开，普通局部编辑/方案查看0。',

      'SEV9L_30 SEV9L_PREFAB_START',

      ('没用过SignTech，可答实际给Prefab选过一件现成门面构件：当前目录能取用，已有可放位置。你先怎样投入？',

       '把这件现成构件放进自己想表达的门面轮廓|按我给建造者设定的朴素工匠身份，先用当前这件构件做入口，暂不继续换造型|只实际改变当前可用构件的位置，看这次编辑结果|先比较当前目录里确实可放的门面构件，再决定采用哪项',

       'a r creative_edit_trial creative_option_review'),

      '只问实际已用原生功能，不保证任意图片导入、付费外观、NPC任务或自动文本解谜；文字含义由玩家自己赋予。'),

    Q(7, '本地PrefabBrowser里尚未看过的建筑',

      '当前本地PrefabBrowser能打开，你能选到一栋还没仔细看过的原生建筑，也有自己的本地作品可继续编辑。你先怎样投入这段？',

      '打开还没看过的建筑，想亲眼知道内部空间怎样展开，暂不为指定成品而看|先比较当前浏览器里已经可选的建筑与布景方案，再决定这一轮看哪栋|回到自己的作品，把已有构件改成想表达的建筑风格|先核对当前已出现的浏览与加载操作说明，再继续自己的实际尝试',

      'w creative_option_review a tool_reference_first',

      '未知内容的发现w需明确动机；浏览已有信息与说明0，不能把打开一条目录自动当探索。',

      'SEV9L_PREFAB SEV9L_33',

      ('没有浏览其他Prefab，可答实际打开自己一份本地作品的时段：你以前已几次回来修改过这段墙面，当前能加载并继续编辑。你先怎样投入？',

       '继续改同一份作品，喜欢以前投入逐渐留在这栋建筑上|把这段墙面的轮廓做成自己想表达的样子|只实际调整一件当前可编辑构件的位置，看本轮结果|先核对已出现的加载与编辑操作说明，再继续实际尝试',

       'g a creative_edit_trial tool_reference_first'),

      '本地浏览器不等于在线工坊，不保证条目全是未解锁可用模块或会自动进RWG；加载他人作品不等于获编辑发布授权。'),

    Q(8, '从保存作品到再试玩的一小轮',

      '你有实际保存过的单独Prefab，已经发现一处想改的小门廊；保存与原生Playtest都曾用过，今天只准备完成这一轮改动。你先怎样继续？',

      '排清这一次改门廊、保存与另开试玩核对的先后，再亲手照安排做|反复练同一段选区、复制和落位，专门把编辑操作练熟|先只改一处当前可编辑构件的位置，亲手看这次编辑结果|按我给建造者设定的惜旧工匠身份，只修入口这一小段，先留原来墙面',

      'construction_action_plan t creative_edit_trial r',

      '一次编辑-保存-试玩不是生产系统y；刻意练习、具体普通编辑与赋予建造者身份后的具体选择r分开。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('还没试玩、只保存过作品，可答实际给当前Prefab命名并保存的一段：本地保存功能已用过，这次有现成作品可存，也有已经出现的工具操作说明可核对。你先怎样继续？',

       '先核对已经出现的命名、保存与本地加载操作说明，再继续自己的实际尝试|实际把当前这份作品保存一次，亲手体验操作发生|按我给建造者设定的档案员身份，先用自己拟定的用途名称命名，再实际存好|只给已经编辑过的构件与步骤补记建设过程',

       'tool_reference_first available_operation_trial r construction_process_recording'),

      '不承诺自动保存、所有试玩改动回写、所有动作能撤销或具体存档路径；本地保存本身不算养成与创造新玩法。'),

    Q(9, '真实反复回来修改的同一份Prefab',

      '回想你真实多次打开、修改并保存同一份Prefab的一段：哪种已经做过的投入更贴近愿意保留的体验？',

      '继续完善同一栋建筑，喜欢早先投入逐渐留在房间与外观上|调整已有轮廓与表面，让作品表达自己想要的建筑风格|专门反复练选区、复制和落位，目的是把编辑操作练熟|只是给已改过的构件与实际步骤补记建设过程',

      'g a t construction_process_recording',

      '真实多轮积累g、风格a、刻意训练t与补记0分开；不靠作品大、下载量或熟练结果推信号。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没有多次保存同一作品，可回想实际第一次摆过门墙的一段：哪种已经做过的动作更贴近愿意保留的体验？',

       '把门与墙排成自己想表达的小屋门面|按我给建造者设定的朴素工匠身份，先只做当时可放的基本门洞，暂不加门面装饰|只是实际放下一件当时可用构件，亲手看操作发生|只是先核对当时已出现的放置说明，再继续实际尝试',

       'a r available_operation_trial tool_reference_first'),

      '没有持续改同一作品不逼答g；真实回顾不要求发布、第三方MOD或反复做同一错误。'),

    Q(10, '真实试玩中检验过的一处通道',

      '回想你真实保存Prefab后另开试玩，实际试走过自制通道的一段：哪种已经做过的投入更贴近愿意保留的体验？',

      '当时怀疑一件装饰挡路，保留其余结构，只改它再试玩，检验自己的猜想|反复练过走同一小段、转向和通过门洞，专门让操作更熟|亲手试走一轮，喜欢输入和眼前位置变化接连发生的反馈|只是排清改这一处、保存与另开试玩的先后，再照这轮安排做',

      'p t f construction_action_plan',

      '真实因果猜想须尚未确认并单项检验，练习须专门目的；试玩一次不自动计机制研究或训练。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没有试玩经历，可回想真实在编辑器选区复制过墙段的一段：哪种已经做过的动作更贴近愿意保留的体验？',

       '专门重复练选区、旋转与落位，想让这项工具操作更熟|亲手粘下一段墙，喜欢输入与眼前结构出现相连的反馈|只是实际调整那段当前可编辑墙的位置或朝向，看改动结果|只是先核对当时已出现的选区工具说明，再继续实际尝试',

       't f creative_edit_trial tool_reference_first'),

      '不保证某种门宽必能通过、所有物件都挡路或Playtest进度保存；不知道原因时不能事后把已知教程答案冒充p。'),

    Q(11, '真实为建筑选过的一套门面',

      '回想你真实在Prefab里为一处门面安排过构件，并编辑过SignTech牌面的一段：当时门面、牌面文字与颜色层都可用。哪种已经做过的投入更贴近愿意保留的体验？',

      '让门面轮廓与牌面颜色一起表达自己想要的建筑风格|把自己当时已见过的构件类别列成想试摆齐的一套，先圈出惦记还缺的一类|按我给建造者设定的惜旧工匠身份，先保留入口现有文字，只修一处色块，暂不换整牌|只是先比较当时实际可用的构件或牌面方案，再决定采用哪种',

      'a c r creative_option_review',

      '风格、明确类别缺口、自己赋予建造者的身份与普通方案比较分开；不造官方全构件收藏成就。',

      'SEV9L_PREFAB SEV9L_30',

      ('没有做过整套门面，可以回想真实选过、摆过最初基础构件的一段：哪种已做动作更贴近愿意保留的体验？',

       '反复练过选形、转向与放下，专门把编辑操作练熟|亲手放这一块，喜欢输入与物件出现紧接着发生的反馈|只是实际调整那块当时可编辑构件的位置，看这次结果|只是先比较当时已开放的基础形状，再决定采用哪种',

       't f creative_edit_trial creative_option_review'),

      '主情境只问确实编辑过SignTech牌面的经历；没有体验时使用基础构件替代，不把它当完成整套问卷的强制门槛。不假定所有类别无限复制、所有开发物件可取或菜单浏览就是收藏动机。'),

    Q(12, '真实回到熟悉作品里的一个下午',

      '回想你真实再次打开已做熟的Prefab的一段：当时精力够、还有新建筑可看或新部分可做。哪种真实投入更贴近愿意保留的体验？',

      '仍在熟悉房间里慢慢试走、看看旧墙面，喜欢留在这份已经熟悉的作品里|打开一栋还没看过的本地建筑，想亲眼知道内部空间怎样展开|继续给同一作品补一处已有计划的门廊，喜欢早先投入逐渐留下变化|只是给已经编辑过的构件与步骤补记建设过程',

      'h w g construction_process_recording',

      'H明确玩家精力与新去向均具备仍主动熟悉停留；探索与同一对象持续积累分开，补记0。',

      'SEV9L_PREFAB SEV9L_PREFAB_START',

      ('没有熟悉完整房间，可回想真实只在编辑器练过基础方块的一段：哪种已做动作更贴近愿意保留的体验？',

       '反复练选位、旋转和确认，专门把这项工具操作练熟|亲手放下方块，喜欢输入与形状出现相连的反馈|只是实际放下一个当时可用构件，亲手体验操作发生|只是先核对当时已经出现的基础编辑说明，再继续自己的尝试',

       't f available_operation_trial tool_reference_first'),

      '不把疲劳、没有权限、只能停留或没剩新内容时的被迫留下计H；不要求编辑器联机、NPC委托或玩家排名。'),

]



_SEV_PREFAB_THIRDS = [

    ('最早只浏览基础构件时',

     '门面与放置都没体验过，可以答实际在Prefab Editor看过构件目录的一段：当前确实显示几类可取基础块。你先怎样投入？',

     '以自己实际见过的构件类别作一套想试齐的目标，惦记还缺哪类|先比较当前确实可用的基础形状，再决定采用哪种|先核对已出现的编辑工具说明，再继续自己的实际尝试|实际从当前目录取出一件可取构件，亲手体验操作发生',

     'c creative_option_review tool_reference_first available_operation_trial',

     '真实较早目录操作，不借完整施工经历；收集须有类别缺口动机。',

     'SEV9L_PREFAB_START SEV9L_33',

     '不造类别完成奖励、任意开发物件或默认飞行；普通查看与取出0。'),

    ('没有复制旋转时的单块放置',

     '复制与旋转都没体验过，可以答真实只放过一个基础块的一段：当前能取用且有可放位置。你先怎样继续？',

     '亲手放下一块，喜欢输入与方块出现相连的反馈|只实际放下当前这块构件，亲手看操作发生|先核对当前已出现的放置说明，再继续尝试|给已经摆过的构件与实际步骤补记建设过程',

     'f available_operation_trial tool_reference_first construction_process_recording',

     '另一真实低前提操作，不让没旋转过者假答训练。',

     'SEV9L_PREFAB_START', '普通放置或补记不计发明、训练或风格表达。'),

    ('没有门洞时的一段可改墙面',

     '试玩与门洞都没体验过，可以答实际编辑过一小段墙面：当时能换一处当前可用表面。你先怎样处理？',

     '选能表达自己想要建筑感觉的表面|亲手换这一处，喜欢输入与表面变化相连的反馈|只给这一处换一种当前可用表面纹理，让图案或配色改变，亲手看这次编辑结果|先比较当前确实可用的外观方案，再决定采用哪种',

     'a f creative_edit_trial creative_option_review',

     '另一可见编辑机制，不制造未知原因或通行测试经历。',

     'SEV9L_PREFAB SEV9L_STORE', '不保证所有方块可涂、任意RGB或结果自动同步到生存世界。'),

    ('没有时间预览或表面编辑时',

     '时间预览和改表面都没经历过，可以答实际在编辑器里转着看过自己已经放好的一处墙角：当前墙角与相邻构件都能查看。你先怎样投入？',

     '先看墙角和相邻构件当前的实际结构，再决定这一轮怎样改|先核对当时已经出现的编辑操作说明，再继续尝试|只给自己已经放过的构件与步骤补记建设过程|按我给建造者设定的档案员身份，先记下这段旧墙要保留的外观，再继续自己原来的编辑安排',

     'device_status_review tool_reference_first construction_process_recording r',

     '另一现有结构查看，自己赋予建造者的身份必须具体影响保留旧墙的记录和后续安排。',

     'SEV9L_PREFAB_START', '不从观察角度推因果诊断、审美或全场自动照明。'),

    ('未布Sleeper也未摆装饰时',

     'Sleeper和摆装饰都没经历过，可以答实际在编辑器浏览过普通构件目录：当前有能取用的一类基础块。你先怎样继续？',

     '先比较当前可用的基础形状，再决定采用哪种|实际取出一件当前可取构件，亲手体验操作发生|先核对已出现的取用与放置说明，再继续尝试|以自己实际见过的构件类别作一个想试齐的目标，惦记还缺哪类',

     'creative_option_review available_operation_trial tool_reference_first c',

     '真实第三早期操作，不让未使用刷怪工具者想象触发。',

     'SEV9L_PREFAB_START', '不造全类自动图鉴或研发/生存等级门槛；类别收藏必须本人明确目标。'),

    ('只在Prefab放过最早几块时',

     '牌面与门面构件都没用过，可以答实际最初放过几块基础墙：当前方块能取用，也有可放位置。你先怎样投入？',

     '把几块墙排成自己想表达的小屋轮廓|反复练选择、转向与落位，专门让编辑操作更熟|只实际放下这一块当前可用墙块，亲手看操作发生|先核对已经出现的基础建造说明，再继续尝试',

     'a t available_operation_trial tool_reference_first',

     '第三真实基础搭建场景，风格与刻意练习明确。',

     'SEV9L_PREFAB_START', '不要求文字、特效、全配方或在线作品发布。'),

    ('没加载作品时的编辑器初次选物',

     '浏览和加载作品都没体验过，可以答实际第一次在Prefab Editor选基础构件：当前菜单可取物，尚未做完整房间。你先怎样继续？',

     '实际选出一件当前可取构件，亲手体验一次菜单操作|反复练分类、选物与取出，专门把菜单操作练熟|先比较当前已经可用的形状，再决定采用哪项|先核对已出现的选物操作说明，再继续尝试',

     'available_operation_trial t creative_option_review tool_reference_first',

     '比本地作品更早的实际工具经历，无加载门槛。',

     'SEV9L_PREFAB_START SEV9L_33', '一次普通点击不等于训练，不假造在线推荐或默认全开发物件。'),

    ('尚未保存时的一轮基础施工',

     '试玩与保存都没体验过，可以答实际只搭过一面基础墙的一段：当前构件可取用，也有可放位置。你先怎样继续？',

     '排清本轮选块、转向与落位的先后，再照这轮施工安排做|亲手摆下一块，喜欢输入与眼前形状出现相连的反馈|只实际调整一个当前可编辑构件的位置，看这次结果|先核对已出现的基础建造说明，再继续尝试',

     'construction_action_plan f creative_edit_trial tool_reference_first',

     '第三真实施工阶段，不预设保存成功或编辑器熟练度。',

     'SEV9L_PREFAB_START', '一次施工顺序0，不能借“循环”措辞计生产系统或新玩法。'),

    ('真实没搭门墙时的目录经历',

     '反复修改与搭门墙都没经历过，可以回想真实在Prefab构件目录选过、取过物件但还没搭门墙的一段：哪种已做动作更贴近愿意保留的体验？',

     '反复练过分类、选物与取出，专门把这项工具操作练熟|实际取出一件当时可取构件，喜欢输入与物件到手相连的反馈|只是先比较当时已经开放的基础形状，再决定采用哪种|只是先核对当时已经出现的选物说明，再继续实际尝试',

     't f creative_option_review tool_reference_first',

     '第三真实较早阶段，过去反复训练与普通浏览分开。',

     'SEV9L_PREFAB_START SEV9L_33', '没有持续对象不计g，结果好坏或点击次数本身不计t。'),

    ('真实没试玩复制时的单块放置',

     '试玩与复制都没体验过，可以回想实际放过最初几个基础块的一段：哪种已做动作更贴近愿意保留的体验？',

     '把几块排成自己想表达的建筑轮廓|亲手放下一块，喜欢输入与方块出现相连的反馈|只是实际放下一块当时可用构件，亲手看操作发生|只是给已放过的构件与步骤补记建设过程',

     'a f available_operation_trial construction_process_recording',

     '第三真实放置动作，无试玩或复制前提。',

     'SEV9L_PREFAB_START', '普通摆放不自动计新玩法；风格表达须本人明确目的。'),

    ('真实尚未取物时看过的工具说明',

     '门面和基础块取用都没经历过，可以回想真实在Prefab Editor看过构件目录与工具说明的一段：哪种已做动作更贴近愿意保留的体验？',

     '把自己当时实际见过的构件类别列成想试齐的目标，先圈出惦记还缺的一类|只是先比较当时已经显示可用的形状，再决定采用哪种|只是先核对当时已经出现的选物说明，再继续实际尝试|只是实际选中过当时一个已出现的构件类别，亲手体验那次菜单操作',

     'c creative_option_review tool_reference_first available_operation_trial',

     '真实目录观察与分类选择，不冒充已取物或已施工；本人明确类别补全目标c与工具说明、普通菜单选择和当前方案比较0分开。',

     'SEV9L_PREFAB_START', '没有实际取用者不冒充已施工；不凭菜单存在推全物品收集奖励。'),

    ('真实没有熟悉作品与练习时',

     '熟悉作品停留和基础方块练习都没经历过，可以回想真实首次在Prefab Editor取过一件构件的一段：哪种已做动作更贴近愿意保留的体验？',

     '亲手取出一件构件，喜欢输入与物件到手相连的反馈|只是实际取出一件当时可取物品，亲手体验操作发生|只是先比较当时已经开放的形状，再决定采用哪种|只是先核对当时已经出现的取用说明，再继续实际尝试',

     'f available_operation_trial creative_option_review tool_reference_first',

     '第三真实最早工具经历，不用早期疲劳替代熟悉栖居。',

     'SEV9L_PREFAB_START SEV9L_33', '未经历过仍可继续换已核实专属情境；三种只是草稿容量，不承诺人人可完成。'),

]

for _n, _row in enumerate(_SEV_PREFAB_THIRDS):

    SEV_PREFAB[_n]['variants'].append(_extra(*_row, reflection=_n >= 8))





SOURCES += [
    source('GR9L_STORE', 'Obsidian：Grounded原作当前PC商店About正文',
      'https://store.steampowered.com/api/appdetails?appids=962130&l=english', 'developer_current_pc_about_game_body',
      '原作后院探索建造生存|实验与缩小故事|单人及最多三位真人伙伴|SharedWorld进度|Mutations与MilkMolars|装备制作升级|MIX.R',
      '2026-10-31实际读保存appdetails中about_the_game完整5411HTML字符的纯正文。早先564字符detailed_description仅1.4预告，不冒充About全体；这次已另存grounded-actual-about-game-5411.txt并完整读。原作962130，不用Grounded2的Buggies、BrookhollowPark或续作专属Brainpower配方。'),
    source('GR9L_CURRENT', 'Obsidian：Grounded1.4.7.4815当前原作补丁完整正文',
      'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1799088287963976', 'developer_official_news_api_current_original_game_body',
      '原作1.4.7.4815|Playgrounds刷出动物自订数值|试玩时间与崩溃修复|REMIX.D已完成层选择修复',
      '2026-10-31已读完整854字符并复读；原作新闻流也有续作宣传，已逐条排除。补丁修复不承诺绝无崩溃，不采用易变伤害、耐力或宠物数值，不要求NG+或最高装备。'),
    source('GR9L_13', 'Obsidian：MakeItAndBreakIt1.3原生Playgrounds及本体更新',
      'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/5302486388013402433', 'developer_official_news_api_released_feature_body',
      'Playgrounds设计与试玩|物件按钮计时激光及逻辑|自由摆放旋转|代码下载分享|设计多人|试玩回设计重置|新BURG.L任务|篮球投掷力度|普通蒲公英绒毛改消耗品',
      '2026-10-31实际分6段读完Steam返回31993字符，并保存剩余04-06实读记录；不声称读Steam截断后官网额外说明或看视频。创意两预设全突变/FullyYoked不等于所有模式；下载玩家不假定有编辑权限。篮球与自创玩法分开，官方任务更新不沿用旧随机每日任务默认已解锁。'),
    source('GR9L_14', 'Obsidian：FullyYoked1.4完整原作更新',
      'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/6474562312199647292', 'developer_official_news_api_released_expansion_body',
      '原作免费1.4|蚁后与NG+须真实进度|Playgrounds制作与玩法选项|原作跨平台',
      '2026-10-31实际读完整16081字符，不把NG+、蚁后或后期配方作为全玩家必备。1.4发布机制和1.4.7.4815当前维护分别核；媒体没看，不借续作宣传。'),
    source('GR9L_12', 'Obsidian：SuperDuper1.2官方介绍已返回的特征段',
      'https://grounded.obsidian.net/news/grounded/update-1-2', 'developer_historical_released_feature_selected_body',
      'SuperDuper在OakLab须DuperDisc与RawScience|复制保留Smithing升级|基地舒适度与新装饰|HandyGnat可从少年旁储物建造|Creative默认助手生存须实际Custom设置|官方1.2正文189–202行：PlaceMany连续放置及结构Relocate条件，墙/地板/屋顶等不是其他建筑唯一支撑时可搬移',
      '2026-10-31实际读web返回20-82行及此前定向HandyGnat段，不冒充587行全文或视频。舒适度是游戏数值，不等于cozy_resident人格；助手名字含Gnat也不是另一个真人。；本次补读另采用189–202已返回原文，不从旧社区“墙不可移动”推断当前规则，也不把结构搬移泛化成Playground自由编辑。'),
    source('GR9L_10', 'Obsidian：1.0正式发布故事、升级与储物选段',
      'https://grounded.obsidian.net/news/grounded/grounded-1-0-release', 'developer_released_feature_selected_body',
      '完整缩小故事与实验室|原生HotDeposit附近箱子|MilkMolar强化|QuartziteMarble加工成升级料|新SCA.B外观方案',
      '2026-10-31实际读web返回35-106行，另检索返回完整HotDepositPlus、OtherAdjustments与MoreSCA.B条目；未通读436行全文。蒲公英绒毛旧饰品槽规则被1.3替换，不采用旧配装与固定数量/伤害/升级上限。'),
    source('GR9L_MODES', 'Grounded原作社区Wiki：实际返回的生存/创意/Custom规则',
      'https://grounded.wiki.gg/wiki/Game_Modes_%28Grounded%29', 'community_wiki_original_game_mode_search_returned_body',
      'Creative与CreativeWithBugs都免材料且全配方|仍需实际制作站和制作时间|两创意无本体任务生存压力|有无虫分开|Custom按实际规则|不是Grounded2',
      '2026-10-31实际读搜索返回完整相关模式表与设置段；直接robots或访问失败不当成功。Fandom是同份旧站内容，不计独立作者佐证。共同创意题不要求活虫、身体生存、任务或从已全开突变再成长。'),
    source('GR9L_ANALYZER', 'Grounded原作Wiki：ResourceAnalyzer基本操作与Brainpower开头',
      'https://grounded.wiki.gg/wiki/Resource_Analyzer', 'community_wiki_targeted_returned_opening_body',
      'FieldStation和实验室有分析仪|分析已有材料可开配方与积Brainpower|充能次数有限须等恢复|Brainpower非唯一配方途径',
      '2026-10-31实际读返回开头、Brainpower说明及表前几行，未读完整配方表。数值、恢复分钟和指定配方需求不采用；当前能分析且有充能才问。续作独占Brainpower奖励不借给原作。'),
    source('GR9L_STORAGE', 'Grounded原作Wiki：StorageChest实际取放与HotDeposit段',
      'https://grounded.wiki.gg/wiki/Storage_Chest', 'community_wiki_targeted_returned_usage_body',
      '箱子与背包实际取放|NearbyStorage可供建筑|HotDeposit只合入箱中已有同类物|箱可排除HotDeposit|标签与彩色图标',
      '2026-10-31实际读返回HowToUse、HotDeposit与Customization及配方栏，不采用容量、配方材料数、键位或范围。只有真实当前启用且匹配的同类物才能快捷合入；不把它写成全部背包自动清空。'),
    source('GR9L_WOOD', 'Obsidian：IntoTheWood历史发布的工具与生产选段',
      'https://www.obsidian.net/news/grounded/the-time-has-come-to-go-into-the-wood', 'developer_released_feature_targeted_search_body',
      'PEEP.R与已有地图航点|部分灯色强度可调|部分建筑蓝图可复制|SpinningWheelGrinderOven制作与附近存储|已发现地点记录',
      '2026-10-31实际读检索返回的PEEP.R航点、BuildingCustomization、ImprovedDataPage、HotDeposit、SpinningWheel/GrinderUI段，不声称全页。旧EA耐力/绒毛/装备合成与数值不用；目录可见不等于材料够，已开放且当前可做才比较配方。'),
    source('GR9L_STORY_FIX', 'Obsidian：原作IssueTracker返回的录音、任务和实验室边界',
      'https://grounded.obsidian.net/issue-tracker', 'developer_current_issue_tracker_selected_search_body',
      '实验室录音与资料页|BURG.L原生NPC|原作任务和实验室存在|多人修复不等于绝无连接问题',
      '2026-10-31实际读检索返回GeneralIssues、Major、Audio及1.4/1.3/1.0修复列表，不声称打开所有条目。只核录音和资料页确实存在，修复历史不当剧情原文或进度门槛。'),
]

GR_SURVIVAL = [
    Q(1, '分析仪这次还能分析一件材料',
      '你在后院一处Field Station，分析仪当前还有可用充能，操作说明已出现；包里有尚未分析的材料，也有两项已经开放、现有材料分别够做的基础配方。附近另有能走但没看过的草丛，补给够短途返回。你先做什么？',
      '先去没看过的草丛，想亲眼发现那边是什么，暂不为指定材料而走|把已见材料列成想分析齐的一套，先分析尚未分析的这一类，专门补自己的清单缺口|先核对已出现的分析仪操作说明与这件材料信息，再亲自继续分析|先比较已经开放且材料够的配方，再决定这次做哪件',
      'w c tool_reference_first compare_production_options',
      '原作分析与未知后院的具体分歧；种类缺口须本人动机，查看说明和当前可做配方0。',
      'GR9L_STORE GR9L_ANALYZER',
      ('还没用过分析仪，可答实际最初捡过植物纤维、小石块这类背包小物的一段：已有一件可收起的小物，旁边有能走但没看过的草叶间隙。你先怎样继续？',
       '走进没看过的草叶间隙，想亲眼知道里面是什么|把已见小物类别列成自己想补齐的一套，先选定这轮想补进的缺类，再去找这一类|先按已有物件实际调整一次携带或存放，再继续安排|先核对当前身体状态和已带补给，再决定这一段怎样走',
       'w c item_handling_action survival_status_review'),
      '不固定分析次数/恢复时间、指定配方解锁或要求找齐全物品；没有充能不让玩家强行分析，不用Grounded2独占配方。'),
    Q(2, '蘑菇浆、烤炉与下一轮墙砖',
      '你已用Grinder和Oven做过蘑菇墙砖；附近有此前采过且现在还能取的蘑菇，手头有浆料，设备与配方也允许继续加工。当前加工界面和操作说明能看，一份已选蓝图仍需墙砖。你先怎样投入这一段？',
      '把蘑菇取得、磨浆、烤砖与下一轮蓝图供给接成周转，持续调整几处储备|先核对已出现的磨浆、烤砖操作说明，再亲自继续这一轮加工|在现有加工界面排清这轮确认用料、执行加工与收取产物的先后，再亲自照顺序做|先核对当前原料、加工进度与已有产物状态，再决定这次怎样安排',
      'y tool_reference_first crafting_action_sequence production_state_review',
      '真实蘑菇、浆料、烤砖与蓝图供给的持续周转y，和本轮制作界面顺序、当前生产现状及操作说明0分开；没有故障现象不强造因果检验。',
      'GR9L_SHROOM GR9L_WOOD GR9L_10',
      ('没用过这两种设备，可答实际搬草板补过蓝图：当前手边有可搬草板，一处已选墙面蓝图确实还需要它。你先怎样继续？',
       '排清这轮拿草板、走到蓝图旁与补料的先后，再按本轮施工安排做|把这一处墙面排成自己想表达的基地轮廓|按当前已经选定的墙面要求实际补料，重点推进这个眼前目标|先核对蓝图已经列出的材料要求与手头物件，再决定这次怎样补',
       'construction_action_plan a stated_objective_progress objective_requirement_review'),
      '不固定配方数量、自动速度或额外燃料，不把制作界面说成手持原料逐件塞进设备。只有已开放且条件满足的配方可做；没有实际失败与未知原因就不计p。'),
    Q(3, '已有武器和突变的这一轮交手',
      '当前你能接近一只自己打过的普通后院昆虫，已有两组确实可换的武器与已开突变搭配，补给与退开空间都具备。你想把这一轮交手用在哪里？',
      '比较这两组已能用的武器与突变搭配，实际检验组合效果|反复练观察起手与格挡时点，专门把自己的操作练熟|亲手交手一轮，享受出手、声音与昆虫反应接连发生的反馈|先排清攻击、耐力消耗和退开恢复的先后，再照这轮循环尝试',
      'b t f combat_resource_cycle',
      '已有两组且亲自检验组合才b，刻意练习才t，反馈f与单次资源循环0分开；角色强化不等于玩家熟练。',
      'GR9L_STORE GR9L_13',
      ('没有昆虫交战或突变配置经历，可答实际用过斧头处理草叶的一段：工具当前可用，旁边有能停手恢复的地方。你先怎样投入？',
       '反复练挥斧与退开的时点，专门把这一套操作练熟|亲手砍这一轮，喜欢声音、草板变化与输入相连的反馈|排清靠近、出手、恢复与收板的先后，再照本轮流程做|先核对当前身体状态与已带补给，再决定这轮怎样活动',
       't f tool_operation_plan survival_status_review'),
      '不保证格挡无伤、不写固定时间窗、昆虫行为或伤害；当前世界无战斗者换题，不要求改设置或去打首领。'),
    Q(4, '橡树实验室回来的一段空闲',
      '你已经到过Oak Lab并与BURG.L交谈，当前有已读实验室录音和已显示任务目标可回看；回程补给够，也有一段可达但没看过的后院。你先做什么？',
      '再听已得录音、回看已见对话，把缩小实验里已经知道的人和事件前后接起来|按当前已显示的任务要求继续行动，先推进这一项目标|先核对任务已经显示的目标与进度，再决定这趟继续到哪一步|去没看过的后院一角，想亲眼知道那里是什么，暂不为指定任务奖励而走',
      's stated_objective_progress quest_progress_review w',
      '已见叙事联系s与当前目标推进0、进度核对0分开；机器人NPC不是与真人协作。',
      'GR9L_STORE GR9L_13 GR9L_STORY_FIX',
      ('没进Oak Lab，可答实际在最初后院看过当前任务提示的一段：已有一个能执行的目标，旁边另有没走过的草叶间隙。你先怎样继续？',
       '先核对已经显示的目标和当前进度，再决定做到哪一步|按这项已显示要求行动，重点推进眼前目标|走近没看过的草叶间隙，想亲眼发现里面是什么|先核对身体状态与已带补给，再决定这段活动',
       'quest_progress_review stated_objective_progress w survival_status_review'),
      '不编录音具体台词、未来剧情与未见角色关系；不是所有玩家都已开每日任务，当前任务状态未显示就不能借题假造。'),
    Q(5, '快捷存入后仍在背包的一件材料',
      '你实际用过Hot Deposit，附近箱里已有同类材料，也有可继续存放的空间；这次那件材料仍留在包里，你尚未确认是排除设置还是别的条件。现在箱子与材料都能查看。你先怎样处理？',
      '猜是这箱被排除快捷存入，固定位置、物品与其他设置，只检查并调整这一项，再用同样方式存入检验|先按这次已有物品实际手动存入一份，再继续原来安排|先核对当前背包和箱中同类材料的实际数量，再决定怎样处理|给箱子选择自己想表达的标签与图标颜色，让这一角收纳带上个人风格',
      'p item_handling_action material_stock_review a',
      '明确失败现象与未知原因的单项检验p；手动取放和材料存量0，个性收纳视觉a不等于物流系统。',
      'GR9L_STORAGE GR9L_10',
      ('没有Hot Deposit经历，可答实际手动往已有箱子放过材料的一段：当前箱子有空间，包里有能放进去的小物，还带着一件仍可保留的旧工具。你先怎样继续？',
       '先按已有物品实际调整一次携带或存放，再继续安排|给这一处箱子选自己想表达的可用标签或图标颜色|先核对包里与箱中已有材料，再决定本轮怎样处理|按我给少年设定的惜物习惯，先把一件仍能留的旧工具收好，再继续出门准备',
       'item_handling_action a material_stock_review r'),
      'Hot Deposit只匹配箱中已有同类物，非全包全场自动清空。设置操作不是76静态查看；位置、范围等不预告排除。未有箱子可继续换题。'),
    Q(6, '有材料也有新去向时的基地',
      '这段时间你精力够，少年补给与工具也够；基地此前由你逐次完善，已有几件已解锁能做的装饰，还有新地点可去。没有迫近的进攻，先怎样投入？',
      '留在熟悉基地慢慢走走、听听声音，享受自己已经住惯的这一角|用已有装饰与构件表达自己想要的微型家园风格|接着完善同一基地，喜欢早先投入逐渐留在这处住屋上|先比较已经开放且当前能做的装饰或构件，再决定这次采用哪项',
      'h a g compare_production_options',
      'H有玩家精力、新地点与补给仍主动享受熟悉节奏；风格a与同一基地持续积累g分开，普通可做配方比较0。游戏Coziness值不是H。',
      'GR9L_12 GR9L_STORE',
      ('没有装饰或长期基地，可答最早一处已放基础蓝图：当前材料够、有可继续施工的位置，你还没有完整家园。你先怎样投入？',
       '把几处基础构件排成自己想表达的住处轮廓|按我给少年设定的朴素定居者身份，先补眼前基本草墙，暂不另加门面装饰|排清这轮搬料、补蓝图与收整的先后，再照安排施工|先核对当前蓝图已经列出的材料要求，再决定怎样补料',
       'a r construction_action_plan objective_requirement_review'),
      '一次放置不直接算g，疲劳/躲风险/没新事可做的停留不计H；不保证基地不会遭袭或所有建材都已解锁。'),
    Q(7, 'SuperDuper前的一份已有装备',
      '你已用Duper Disc开放Super Duper，当前设备权限与Raw Science允许复制手里这件装备；此前一直在完善同一少年，也已有两组确实能换用的武器与突变搭配，能出门尝试。你先怎样继续？',
      '先核对这次复制已显示的资源要求与手头条件，再决定是否执行|实际复制这一件当前可复制装备，亲手体验操作发生|接着完善同一少年的可用装备，喜欢早先投入逐渐留在角色可做内容上|比较已有两组装备与突变搭配，再出门实际检验组合效果',
      'objective_requirement_review available_operation_trial g b',
      '当前允许复制才问；条件查看和普通复制0，持续角色完善g与两组亲测b分开。不是无限免费复制。',
      'GR9L_12 GR9L_STORE',
      ('没用过Super Duper，可答实际在Smithing设施升级过同一件常用装备的一段：此前已为它投入过几次，当前已有升级料满足要求，升级界面与操作说明都能看。你先怎样继续？',
       '继续完善这件自己反复用的装备，喜欢先前投入逐渐留在它上面|先核对本次已显示的升级要求与手头材料，再决定怎样做|先核对已经出现的升级操作说明，再亲手做这一轮升级|直接做这次当前允许的升级，亲手体验操作发生',
       'g objective_requirement_review tool_reference_first available_operation_trial'),
      '不要求后期碟片、复制最高级或固定RawScience花费；没有反复投入不因一次升级计g，不把角色数值当现实能力。'),
    Q(8, 'SCA.B已显示的一段后院路',
      '你当前的SCA.B地图已显示几个已发现位置和一个已有航点；眼前有走熟回程，也有能到但没走过的草叶下小路，补给足够短途返回。你先怎样继续？',
      '走近没看过的小路，想亲眼发现草叶后面是什么|先核对地图已显示位置与已有航点，再决定这段往哪里走|排清已有补给、这次目的地和返回熟悉落脚处的安排，再照这趟准备行动|按我给少年设定的后院记录员身份，先记下眼前已见标记，再继续能走的路段',
      'w navigation_information_review mission_preparation_plan r',
      '未知发现与具体身份行动分开；只看地图现有信息0、单趟准备0，不造全地图资源点。',
      'GR9L_WOOD GR9L_STORE',
      ('没有看过地图，可答最早在草叶间走过的一段：前方是尚未看过但能走的空隙，身后有走熟落脚处，手边有基础补给。你先怎样继续？',
       '走过去亲眼看看空隙后面是什么，暂不为指定产物而走|先核对当前身体与已带补给，再决定这段活动|按我给少年设定的后院记录员身份，先记下已见草叶与落脚处，再继续能走路段|只给已经到过的位置补记记录',
       'w survival_status_review r game_recording'),
      '不保证地图永远全开、航点自动规划安全路或随时可传送；不借Grounded2骑乘/越野车辆。'),
    Q(9, '真实逐次完善的同一少年',
      '回想原作后院里同一少年真实多次开放突变、用Milk Molar强化或完善已有装备的一段：哪种已经做过的投入更贴近愿意保留的体验？',
      '接着完善同一角色可用的配置与装备，喜欢先前投入逐渐留在角色身上|比较过两组当时确实可换的突变与装备，并实际检验组合效果|专门反复练过格挡或工具时点，目的是让自己的操作更熟|只是先核对当时已经出现的配置与强化说明，再继续实际尝试',
      'g b t game_reference_first',
      '持续角色进度、配装检验、玩家刻意训练三者不同；普通说明0，不从突变全开或数值高推现实能力。',
      'GR9L_STORE GR9L_10',
      ('没有角色强化，可回想实际几次回同一处小基地补过蓝图的一段：哪种已做投入更贴近愿意保留的体验？',
       '继续完善同一住处，喜欢以前投入逐渐留在这处基地上|用已有构件做自己想表达的家园轮廓|只是排清当时搬料、补蓝图与收整的先后，再做那一轮|只是核对当时蓝图已列要求与手头材料，再决定怎样补',
       'g a construction_action_plan objective_requirement_review'),
      '没有持续投入就不逼答g；不混Creative已全开突变的无成长压力规则，不要求最高强化、固定层数或NG+。'),
    Q(10, '真实听过的实验室录音',
      '回想你真实取得并听过实验室录音、与BURG.L交谈或看过后院实验资料的一段：哪种已做投入更贴近愿意保留的体验？',
      '再听已得内容，把已见人物、实验与缩小事件的先后接起来|把已见录音或资料类别列成自己的补全清单，专门留意并寻找还缺的一类|按我给少年设定的记录员身份，先记下已知实验线索，再继续这段旅程|只是给已经看过的资料与人物信息补上自己的记录',
      's c r game_recording',
      '叙事联系、明确资料类别缺口、自己角色落实行动与普通已见信息记录分别表达；NPC不计真人社交。',
      'GR9L_STORY_FIX GR9L_STORE GR9L_ANALYZER',
      ('没有录音或实验室经历，可回想真实在最早Field Station分析过材料的一段：哪种已做动作更贴近愿意保留的体验？',
       '列过自己想分析齐的已见材料类别，先分析其中尚未分析的一类，专门补进这套清单|亲手分析一件当时允许分析的材料，喜欢输入与结果出现相连的反馈|先核对当时已出现的分析仪操作说明，再亲手继续实际尝试|只是为已经取得的材料与发现位置补记记录',
       'c f tool_reference_first game_recording'),
      '不让未见剧情者猜未来关系，不编具体台词或未找到录音位置。普通分析、记录或推进目标本身不自动计收集与叙事。'),
    Q(11, '真实选过的SCA.B外观或箱子标记',
      '回想你真实取得并选过SCA.B外观方案，或给已有储物箱选过标签与图标颜色的一段：哪种已做投入更贴近愿意保留的体验？',
      '选择能表达自己想要后院旅途感觉的配色与标记|把已见SCA.B方案列成自己的收藏清单，专门寻找当时还没拿到的一类，想补进自己这套|专门反复练过箱子存取与快捷合入，目的是让自己的工具操作更熟|只是先比较当时已经开放的外观或标记方案，再决定采用哪种',
      'a c t creative_option_review',
      '风格表达a、明确类别收集c和刻意工具练习t分开；已有方案比较0。箱子标签不等于整个基地生产系统。',
      'GR9L_10 GR9L_STORAGE',
      ('没有SCA.B外观与箱子标记，可回想实际放过一面基础墙蓝图的一段：哪种已做动作更贴近愿意保留的体验？',
       '用几处基础构件表达自己想要的小家轮廓|按我给少年设定的朴素定居者身份，先补当时那面基本草墙，暂不另加门面装饰|只是排清当时搬料、补蓝图与收整的先后，再照本轮安排做|只是核对当时蓝图已列要求与手头材料，再决定怎样补',
       'a r construction_action_plan objective_requirement_review'),
      '不造SCA.B方案能力加成、全收藏奖励或必须收齐才会玩；反复存取须明确训练动机才t。'),
    Q(12, '真实同游时的后院安排',
      '回想确有其他真人一起玩原作后院的一段：当时有人想继续已显示实验室目标，有人想先补基地，各项当前能做；自己手里也确有两组可用装备与突变搭配。哪种真实投入更贴近愿意保留的体验？',
      '先谈清这轮共同目标，商量谁带哪些已有补给、谁补蓝图与何时再集合|陪同伴在熟悉基地边走走聊天，喜欢一起待在后院的陪伴|比较过自己手头两组可用装备与突变，再实际检验组合效果|只是为已经参与的基地建设与实际步骤补记过程',
      'q o b construction_process_recording',
      '真实共同安排q与陪伴o分开；现有配装亲测b不依赖对方角色，建设记录0。不从跨平台或好友数推社交人格。',
      'GR9L_STORE GR9L_13',
      ('只有单人经历，可回想真实待在熟悉基地的一段：此前你逐次完善过这处基地，当时自己精力够、补给够，也有新地方可走。哪种真实投入更贴近愿意保留的体验？',
       '仍在熟悉基地边慢慢走走，喜欢待在已经住惯的地方|去没看过的草叶间隙，想亲眼知道里面是什么|继续完善同一小基地，喜欢之前投入逐渐留下变化|只是按当时已有物件实际调整一次携带或存放，再继续安排',
       'h w g item_handling_action'),
      'HandyGnat、BURG.L和宠物不是其他真人；不保证所有人都有共享世界或网络必能连上。H排除疲劳、没补给、没别处可去造成的停留。'),
]

_GR_SURVIVAL_THIRDS = [
    ('没分析也没拾物时的最早走路',
     '分析与拾物两种情境都没体验过，可以答实际第一次在后院草叶间行走的一段：你能走到眼前空隙，也看得到返回处。你先怎样继续？',
     '去亲眼看看没走过的草叶空隙后面是什么|亲手走跳一小段，喜欢输入与眼前位置变化相连的反馈|先核对当前身体状态与已带补给，再决定这一段活动|只给自己已经走过的位置补记记录',
     'w f survival_status_review game_recording',
     '第三真实最早移动情境，不要求合成、实验室或战斗。',
     'GR9L_STORE', '不保证空隙安全或补给自动恢复；普通移动不能直接计探索，须有未知发现动机。'),
    ('没加工搬板时的已开基础配方',
     '磨浆烤砖与搬草板都没经历过，可以答实际做过最早基础工具的一段：当前制作界面有两项已开放、现有材料分别够做的配方，这次能选择一项制作。你先怎样继续？',
     '先核对已选工具列出的材料要求与手头物件，再决定怎样做|排清这轮在制作界面确认配方与用料、执行制作和整理产物的先后，再亲自照顺序做|直接做这一件当前能做的工具，亲手体验操作发生|先比较已经开放且材料够做的基础配方，再决定这次采用哪项',
     'objective_requirement_review crafting_action_sequence available_operation_trial compare_production_options',
     '第三早期制作动作，无高级设备门槛，四种具体行为均0。',
     'GR9L_STORE GR9L_ANALYZER', '查看配方不假定材料已够；题面明示当前可做，不从基础制作计管理系统或成长。'),
    ('没交手砍草时的一轮小物操作',
     '昆虫交手与斧头砍草都没经历过，可以答实际捡起并收过一件小物：当前这件能拾起，手边也有可放空间。你先怎样投入？',
     '亲手拾起这一件，喜欢输入与物件变化紧接着发生的反馈|先按已有物品实际调整一次携带或存放，再继续安排|把已见小物种类列成自己想补齐的一套，先选定这轮要补进的缺类，再去寻找|先核对已经出现的基础操作说明，再继续实际尝试',
     'f item_handling_action c tool_reference_first',
     '第三真实交互，无装备组合或交战前提。',
     'GR9L_STORE GR9L_STORAGE', '不能把拿到几件东西自动计收集，也不要求反复丢物造训练。'),
    ('未进实验室也未看任务时',
     '实验室与任务提示都没体验过，可以答实际在后院走过的最初一段：前方有可走但没看过的草叶空隙，你能查看自己的身体和已带物件。你先怎样继续？',
     '亲眼去看看草叶空隙后面是什么|先核对当前身体状态与已带补给，再决定这一段活动|先核对已经出现的基础玩法说明，再继续自己的实际尝试|按我给少年设定的后院记录员身份，先记下已见草叶和返回处，再继续能走的路段',
     'w survival_status_review game_reference_first r',
     '第三真实移动阶段，不靠未知剧情和任务假设填题。',
     'GR9L_STORE', '身份由本人赋予并具体影响记录后继续的行为，不把没有任务当负分。'),
    ('没箱子时整理已有背包',
     '快捷存入和箱子都没体验过，可以答实际整理过已有背包：当前有一件可取放的小物，身体与已带补给可查看。你先怎样继续？',
     '按已有物件实际调整一次携带、放下或收起，再继续安排|先核对当前身体状态与已带补给，再决定本轮活动|把已见小物种类列成自己想补齐的一套，先选定这轮想补进的缺类|只给自己已经取得的物件与发现位置补记记录',
     'item_handling_action survival_status_review c game_recording',
     '第三真实最早物品操作，不编尚未建成容器。',
     'GR9L_STORE', '不要求背包容量、拾物上限或丢弃后必可找回；种类目标需明确动机。'),
    ('没建家时的已有基础材料',
     '装饰、长期基地和蓝图都没体验过，可以答实际收起过基础材料：当前几件小物已在手边，还有能走到的草叶空隙。你先怎样继续？',
     '去没看过的草叶空隙亲眼看看是什么|把已见材料类别列成自己想补齐的一套，先选定这轮要补进的缺类|先按已有小物实际调整一次携带或存放，再继续安排|先核对身体与已带补给，再决定这一轮活动',
     'w c item_handling_action survival_status_review',
     '第三真实早期经历，不为未建家者硬造熟悉基地H或持续成长G。',
     'GR9L_STORE', '没有持续投入或熟悉安居前提就不强计H/G；未知发现须本人动机。'),
    ('还没复制升级时的已有工具',
     'SuperDuper和Smithing都没用过，可以答实际拿到一件基础工具的一段：当前工具能用，也有已经出现的操作说明。你先怎样继续？',
     '反复练出手与退开时点，专门把这项工具操作练熟|亲手用这一件，喜欢输入与声音、变化相连的反馈|先核对已有操作说明，再继续自己的实际尝试|只实际换用一件当前已有可用工具，亲手体验它怎样发挥',
     't f tool_reference_first try_available_setup',
     '第三早期工具经历，无复制或升级门槛。',
     'GR9L_STORE', '当前一项已有工具试用0，不假造第二组合或所有突变都已开。'),
    ('无地图也没穿草叶时的站内信息',
     '地图与草叶岔路都没体验过，可以答实际在Field Station看过分析说明的一段：包里已有取得的材料，当前身体、携带物和分析操作说明都能查看。你先怎样继续？',
     '先核对已显示的分析仪操作说明与材料信息，再亲手继续尝试|把已见材料类别列成自己想补齐的一套，先选定这轮要补进的缺类|只给已经取得的材料与发现位置补记记录|先核对当前身体状态与已带补给，再决定这一轮活动',
     'tool_reference_first c game_recording survival_status_review',
     '第三种已见工具信息，不依赖地图解锁或实际分析充能。',
     'GR9L_ANALYZER GR9L_STORE', '没有实际分析者不假答已解锁配方；普通核对说明与记录0。'),
    ('真实尚未成长建家时的基础操作',
     '角色强化与反复完善基地都没经历过，可以回想实际最早处理草叶的一段：哪种已做投入更贴近愿意保留的体验？',
     '反复练过挥斧与退开时点，专门让这项工具操作更熟|亲手砍草，喜欢输入与声音、草板变化相连的反馈|只是排清当时靠近、出手、恢复与收板的先后，再做那一轮|只是核对当时身体状态和已带补给，再决定那轮活动',
     't f tool_operation_plan survival_status_review',
     '第三真实操作经历，玩家训练与角色数值成长区分。',
     'GR9L_STORE', '不要求固定砍草数、突变阶段或战斗；一次普通挥斧不算刻意练习。'),
    ('真实尚未分析时见过的后院',
     '录音、实验室与材料分析都没体验过，可以回想实际在最早后院草叶旁的一段：哪种已做动作更贴近愿意保留的体验？',
     '走进当时能到但没看过的空隙，想亲眼知道里面是什么|亲手跑跳一小段，喜欢输入与位置变化相连的反馈|按我给少年设定的后院记录员身份，先记下已见草叶和返回处，再继续能走路段|只是给自己已经去过的位置补记记录',
     'w f r game_recording',
     '第三真实早期经历，不让未读资料者编故事记忆。',
     'GR9L_STORE', '记录不是自动叙事联系；未知发现与反馈须本人明确投入。'),
    ('真实尚未改外观建墙时的小物',
     '外观方案、箱子标记和墙面蓝图都没体验过，可以回想实际拿过几类小物的一段：哪种已做投入更贴近愿意保留的体验？',
     '列过自己想补齐的小物种类清单，专门去找还没拿到的一类，想补进自己这套|亲手拾一件，喜欢输入与物件变化相连的反馈|只是按当时已有物件调整一次携带或存放，再继续安排|只是给已经取得的物件与发现位置补记记录',
     'c f item_handling_action game_recording',
     '第三真实较早操作，不靠外观或施工经历强计审美。',
     'GR9L_STORE', '不凭物品数量计c，不造全收藏成就或背包满的动机。'),
    ('真实没有联机安居时的单人制作',
     '联机与熟悉基地停留都没体验过，可以回想真实单人做过基础工具的一段：当时制作界面有两项已开放、现有材料分别够做的配方。哪种已做动作更贴近愿意保留的体验？',
     '先比较当时已经开放且材料够的配方，再决定做哪件|排清过那轮在制作界面确认配方与用料、执行制作和整理产物的先后，再亲自照顺序做|亲手做一件，喜欢输入与物件出现相连的反馈|只是核对当时已选工具列出的材料要求，再决定怎样做',
     'compare_production_options crafting_action_sequence f objective_requirement_review',
     '第三真实单人制作，不让NPC助手补真人社交。',
     'GR9L_STORE GR9L_ANALYZER', '三种是当前草稿容量，不保证所有玩家必有适用项；未体验仍继续换已核实专属情境，不提供跳过。'),
]
for _n, _row in enumerate(_GR_SURVIVAL_THIRDS):
    GR_SURVIVAL[_n]['variants'].append(_extra(*_row, reflection=_n >= 8))


GR_CREATIVE = [
    Q(1, '免材料建造里最初的草墙轮廓',
      '你在原作Creative或CreativeWithBugs里建造，两者都免配方材料；眼前草墙、门和地板当前可放，不需要做生存任务。入口轮廓还没定，你先怎样投入？',
      '把现有构件排成自己想表达的微型住屋轮廓|反复练选构件、转向与落位，专门把这套建造操作练熟|排清这次先选地板、再放门洞与墙面的编辑顺序，再照顺序实际摆放|只实际放下一件当前可用构件，亲手看操作发生',
      'a t creative_workflow_plan available_operation_trial',
      '共同创意规则下的具体建造，不以材料周转或未开配方制造压力；风格、刻意操作训练与本轮流程0区分。',
      'GR9L_MODES GR9L_12 GR9L_WOOD',
      ('没搭过整间屋，可答真实只选过基础草墙并放置的一段：当前能再次选墙、转动待放预览，眼前也有能放的位置。你先怎样投入？',
       '把几块墙排成自己想表达的小屋轮廓|亲手放下这一块，喜欢输入与墙面出现紧接着发生的反馈|只调整这块待放草墙预览的位置，再实际放下查看结果|先核对当前已经出现的建造说明，再继续实际尝试',
       'a f creative_edit_trial tool_reference_first'),
      '免材料建造仍通过原生建造菜单选择、预览与放置；不写建筑物从背包领取，不强加未完工蓝图补料。制作站、加工时间与普通建造限制分别核实；共同情境不需要活昆虫，不推少年本人默认飞行。'),
    Q(2, '用HandyGnat补一段高处门廊',
      '你在原作创意模式实际使用过Handy Gnat；当前助手能操纵，高处门廊旁还有能放现有构件的位置，可以继续选件与放置。你先怎样投入？',
      '反复练助手靠近、对准与确认放置，专门把这套工具操作练熟|亲手操纵助手放下一件，喜欢输入与眼前结构变化相连的反馈|把这一段改成自己想表达的微型门廊造型|排清这一轮选件、调整朝向与落位的编辑先后，再照顺序实际完成',
      't f a creative_workflow_plan',
      '原生助手是操作工具而非真人；刻意练习、反馈、风格与单轮建设顺序0分开。',
      'GR9L_12 GR9L_MODES',
      ('没用过HandyGnat，可答实际由少年放过基础构件：当前一件草墙或地板可放，眼前有可用位置。你先怎样继续？',
       '反复练选块、转向与确认，专门把建造操作练熟|亲手放下这一件，喜欢输入与形状变化相连的反馈|只改变当前待放草墙预览的位置，再亲手放下查看结果|先核对已经出现的放置说明，再继续实际尝试',
       't f creative_edit_trial tool_reference_first'),
      '不把创意默认助手借给未转换Custom的生存玩家，不以助手飞行推少年能飞，不保证无距离限制或每块都可放。'),
    Q(3, '免材料但仍要经过制作站',
      '这次创意规则免配方材料，你已摆好需要的制作站；站内有一项加工尚未完成，另有成品可取，至少两项已开放配方当前也能加工。你先怎样继续？',
      '先查看当前站内加工进度与已有成品状态，再决定这一轮怎样处理|排清这轮在站点界面核对免材料配方与设备、执行加工和收取成品的先后，再亲自做|先比较已开放且当前制作站能做的配方，再决定这一轮采用哪项|实际取出这件已经完成物品，亲手体验操作发生',
      'production_state_review crafting_action_sequence compare_production_options available_operation_trial',
      '创意免材料不取消站点和时间；四项均为具体0行为，不为了凑人格把查看或单轮取物计系统经营。',
      'GR9L_MODES GR9L_WOOD',
      ('没用过制作站，可答实际从当前可用基础建造目录选草墙的一段：这类构件现在可放。你先怎样继续？',
       '先比较当前可用的基础墙形，再决定采用哪种|只实际放下一个当前能放的构件，亲手看操作发生|先核对已经出现的基础建造说明，再继续尝试|把几块墙排成自己想表达的住处轮廓',
       'creative_option_review available_operation_trial tool_reference_first a'),
      '不宣称全部物件都能裸手瞬间生成、配方可见就无需站点；普通一次制作不算y，多轮资源压力不强加给创意。'),
    Q(4, '已有萤火灯的一处光与颜色',
      '你已有一盏当前能调整颜色与强度的Firefly Hanging Lantern，旁边是已建草墙与家具；一处角落仍比预期暗，还没确认影响因素。这里没有任务催促，先怎样改这一角？',
      '选自己想表达的灯色，让这一角呈现想要的微型家园气氛|猜暗处与灯的强度有关，固定位置、灯色和周围构件，只改这一项强度观察差异|只实际改一个当前可用灯色，看本轮编辑结果|先比较已经开放的灯色或构件外观，再决定采用哪种',
      'a p creative_edit_trial creative_option_review',
      '灯色表达与未知亮度关系单项测试分开；只换色0、查看方案0。切换一次强度不能自动计因果研究。',
      'GR9L_WOOD GR9L_12',
      ('没用过可调灯，可答实际摆过一件现成装饰：当前装饰有可放位置，也能调整位置。你先怎样继续？',
       '把它与草墙排成自己想表达的家园风格|亲手摆下一件，喜欢输入与眼前位置变化相连的反馈|只调整这件装饰待放预览的位置，再实际放下查看结果|先比较当前目录里确实可用的装饰，再决定采用哪项',
       'a f creative_edit_trial creative_option_review'),
      '只指定已证可调的灯，不把所有灯都可改色；未知原因不预告结论，不承诺实际照明或结构绝无问题。'),
    Q(5, '从已建草墙复制一件再摆放',
      '你在原作创意后院已放好一块草墙，当前可以用原生复制建筑操作选出同类待放墙，旁边也有能放的位置。你想继续接这一小段，先怎样投入？',
      '反复练对准已有墙、复制、转向与落位，专门把这套建造操作练熟|先核对已经出现的复制建筑与放置说明，再亲手继续这一轮|排清这轮复制选件、调整朝向与落位的编辑先后，再照顺序实际完成|把接出的墙面排成自己想表达的开敞门廊轮廓',
      'practice_seeker tool_reference_first creative_workflow_plan a',
      '原生复制建筑与放置预览的真实操作，刻意工具练习t、视觉表达a和本轮编辑顺序/操作说明0分开；不凭空添加创意支撑故障。',
      'GR9L_WOOD GR9L_12 GR9L_MODES',
      ('没用过复制建筑，可答实际只摆过地板的一段：当前能再次选取地板、调整待放预览，眼前也有可放的位置。你先怎样继续？',
       '把几块地板排成自己想表达的平台轮廓|只改一块待放地板预览的位置，再实际放下查看结果|排清这轮选地板、转向与落位的编辑先后，再照顺序实际完成|先核对已经出现的基础建造说明，再继续实际尝试',
       'a creative_edit_trial creative_workflow_plan tool_reference_first'),
      '不要求免材料模式留下待补料蓝图，不把普通复制建筑算发明。移动已建结构另受原生Relocate条件限制；复制不等于自由拖动任意现有物。'),
    Q(6, '空后院里还没看过的一角',
      '你在创意后院一处已经熟悉的小屋旁，这段精力够，也有一处能到但没看过的草叶下空隙；当前地图已有位置与标记可看，不必做任务或处理食水。你先怎样投入？',
      '走近没看过的空隙，想亲眼知道草叶背后是什么|仍在熟悉小屋旁慢慢走走，喜欢待在已经住惯的这一角|把已有墙面和家具改成自己想表达的家园风格|只先核对当前地图已经显示的位置与标记，再决定这段往哪里走',
      'w h a navigation_information_review',
      '共同创意路径无活虫前提；未知发现、主动熟悉栖居、视觉风格与已显示导航信息0区分。',
      'GR9L_MODES GR9L_STORE GR9L_WOOD',
      ('没有熟悉小屋，可答实际第一次走进创意后院：当前一处草叶空隙能走，现有地图显示信息可查看。你先怎样继续？',
       '去亲眼看看没走过的空隙后面是什么|亲手走跳一小段，喜欢输入与位置变化相连的反馈|先核对地图已显示位置与已有标记，再决定这一段往哪走|只给自己已经到过的位置补记记录',
       'w f navigation_information_review game_recording'),
      '不把无虫模式写成仍要打虫，不借续作Buggies；没精力、没新去向或被迫留在原处不计H。'),
    Q(7, '已有篮球和篮筐的一轮投掷',
      '你在创意后院已有篮筐，手中有能投的原作篮球；刚才两投落点不同，原因还没核清。当前可调整蓄力，周围也能停下重来。你先怎样投入？',
      '反复练瞄准与出手力度，专门把投篮操作练熟|亲手投一球，喜欢出手、球路、碰筐声音接连发生的反馈|怀疑落点变化与蓄力有关，固定站位与方向，只改力度检验猜想|只实际换一次已经会用的出手时点，亲手体验这一投怎样发生',
      't f p try_action_variant',
      '原生篮球蓄力与反馈，训练与未知规律单项检验分开；普通换一次出手0，不凭一个篮筐就算自创玩法。',
      'GR9L_13 GR9L_MODES',
      ('没投过篮球，可答实际只放过一件装饰的一段：当前装饰确实可放，也能选位置。你先怎样投入？',
       '反复练选物、转向与落位，专门让建造操作更熟|亲手摆一件，喜欢输入与位置变化相连的反馈|只调整这件装饰待放预览的位置，再实际放下查看结果|先核对已有放置操作说明，再继续实际尝试',
       't f creative_edit_trial tool_reference_first'),
      '不要求联机、官方排行榜或自动计分；个人投中目标不计k，普通改站位不计i，不造通用物理结论。'),
    Q(8, '已有箱子的标签与图标',
      '当前创意后院已有两个能用的储物箱，箱中有存放空间；手边有可取放小物、一件仍可保留的旧工具和当前可用的新工具，箱子标签与图标颜色能改。你先怎样整理这一角？',
      '给标签与图标选能表达自己想要家园感觉的配色|按我给少年设定的惜物习惯，先收好一件仍可留的旧工具，暂不另取新的一件|按已有物件实际调整一次携带或存放，再继续安排|只实际改一个当前可用图标颜色，看这次编辑结果',
      'a r item_handling_action creative_edit_trial',
      '创意也能取放物件，但无必然资源紧缺；风格、本人角色落实惜物选择与普通整理/改色0分开。',
      'GR9L_STORAGE GR9L_MODES',
      ('没用过箱子，可答实际只选过一种当前可放基础构件：现有位置能放，目录里也有其他已开放形状。你先怎样继续？',
       '把这一件放进自己想表达的住处轮廓|按我给少年设定的朴素定居者身份，先放眼前基本草墙，暂不加门面装饰|只实际放下一个当前可用构件，亲手体验操作发生|先比较已经开放的基础形状，再决定采用哪种',
       'a r available_operation_trial creative_option_review'),
      '不从箱多推经营或收集，不写资源采集是创意必做；改颜色0不泛化到开关、接线或任何菜单操作。'),
    Q(9, '真实反复完善的创意基地',
      '回想你在原作创意后院真实多次回来修改同一处基地的一段：哪种已做投入更贴近愿意保留的体验？',
      '继续完善同一住处，喜欢早先投入逐渐留在房间与门廊上|用现有轮廓、灯色和家具表达自己想要的微型家园风格|专门反复练选物、转向与落位，目的是让自己的建造操作更熟|只是给已放过的构件与实际步骤补记建设过程',
      'g a t construction_process_recording',
      '创意持续成长落在真实同一作品，不用已全开的突变或MilkMolar再计g；风格与刻意训练分别明确。',
      'GR9L_12 GR9L_MODES',
      ('没有反复改基地，可回想实际第一次摆过草墙的一段：哪种已做动作更贴近愿意保留的体验？',
       '把几块草墙排成自己想表达的住处轮廓|亲手放下一块，喜欢输入与墙面出现相连的反馈|只是实际放下一件当时可用构件，亲手看操作发生|只是先核对当时已出现的建造说明，再继续实际尝试',
       'a f available_operation_trial tool_reference_first'),
      '一次普通放置不算g；不把全开配方或制作时长误作角色能力，也不强迫所有人建大基地。'),
    Q(10, '真实用助手或少年施工的一轮',
      '回想你真实用HandyGnat或少年在已有门廊旁选构件、预览并放置的一段：曾见接缝与预期不一致，原因未明。哪种已做投入更贴近愿意保留的体验？',
      '反复练过靠近、对准与确认放置，专门让自己的工具操作更熟|亲手放下一件，喜欢输入与眼前构件变化相连的反馈|当时猜接缝不齐与待放件朝向有关，固定位置与其他构件，只改这一件预览朝向再放下观察，检验猜想|排清过那轮选件、调整朝向与落位的编辑先后，再照顺序动手完成',
      't f p creative_workflow_plan',
      '训练目的、即时反馈和未知原因单项检验各自明确；普通本轮步骤0，不把助手当真人。',
      'GR9L_12 GR9L_MODES GR9L_13',
      ('没有补门廊，可回想实际在创意后院投过篮球的一段：哪种已做投入更贴近愿意保留的体验？',
       '反复练瞄准与力度，专门让自己的投篮操作更熟|亲手投一球，喜欢出手、球路与声音接连发生的反馈|当时怀疑落点与力度有关，固定站位方向，只改力度检验猜想|只是实际换一次已经会用的出手时点，亲手体验这一投怎样发生',
       't f p try_action_variant'),
      '没有反复练不计t，已知教程结论不包装成p；不要求篮球官方计分或所有构件都能从远处放下。'),
    Q(11, '真实选过的创意家园外观',
      '回想你在原作创意后院真实选过墙形、可调灯色或现成家具的一段：哪种已做投入更贴近愿意保留的体验？',
      '让墙形、灯色和家具表达自己想要的微型家园感觉|列过自己想看齐的构件类别，专门补看当时还没见过的一类，想把这套类别看齐|按我给少年设定的朴素定居者身份，先放当时那面基本草墙，暂不另加门面装饰|只是先比较当时已经可用的构件或灯色方案，再决定采用哪种',
      'a c r creative_option_review',
      '明确风格、类别缺口与本人赋予角色身份的具体行动分开；普通可用方案比较0，不造官方全装饰图鉴奖励。',
      'GR9L_12 GR9L_WOOD GR9L_MODES',
      ('没有挑过外观，可回想实际只取放过一件小物的一段：哪种已做投入更贴近愿意保留的体验？',
       '亲手取放这一件，喜欢输入与物件变化相连的反馈|只是按当时已有物品调整一次携带或存放，再继续安排|只是先核对当时已经出现的取放说明，再继续实际尝试|只是给自己已经取得的物件与发现位置补记记录',
       'f item_handling_action tool_reference_first game_recording'),
      '已有全配方也不自动代表玩家有收藏动机，普通取用不因创意模式计i/a。'),
    Q(12, '真实和别人一起搭过的一角',
      '回想确有其他真人与你同在创意后院搭建的一段：当时几种构件都能用，有人想先补门廊，有人想先改房间配色。哪种真实做法更贴近愿意保留的投入？',
      '先谈清这轮一起想完成的样子，商量谁摆哪些已有构件、何时一起回看|陪同伴在熟悉小屋旁走走聊天，喜欢一起待在这里的陪伴|用现有构件和灯色做自己想表达的家园风格|只是给已经一起放过的构件与实际步骤补记建设过程',
      'q o a construction_process_recording',
      '真人共同安排、陪伴和个人视觉表达分开，建设过程记录0；免材料不等于免协商，也不是用NPC补真人。',
      'GR9L_STORE GR9L_12 GR9L_MODES',
      ('只有单人经历，可回想真实回到熟悉创意小屋的一段：此前已逐次完善过这处基地，当时自己精力够，还能去新地方或搭新部分。哪种已做投入更贴近愿意保留的体验？',
       '仍在熟悉小屋边慢慢走走，喜欢待在自己已经住惯的地方|去没看过的后院一角，想亲眼发现那里是什么|继续完善同一处基地，喜欢先前投入逐渐留下变化|只是先比较当时已开放的构件方案，再决定采用哪种',
       'h w g creative_option_review'),
      'HandyGnat、宠物与机器人均不是其他真人；不保证联机无连接问题。H排除玩家疲劳、无权限或无新事可做的被迫停留。'),
]

_GR_CREATIVE_THIRDS = [
    ('还没搭草墙时的基础目录',
     '整间屋和草墙放置都没体验过，可以答真实在原作创意建造目录看过基础构件：当前有几种可选墙形，能选中并进入建造预览。你先怎样投入？',
     '把想试看的构件类别列成自己的清单，先选还没看过的一类补看预览，专门想补齐这套|先比较当前已经可用的基础形状，再决定采用哪种|先核对已经出现的选物说明，再继续实际尝试|实际选中一个当前可用墙形，进入建造预览，亲手体验这项操作',
     'c creative_option_review tool_reference_first available_operation_trial',
     '第三真实较早目录操作，无完整施工前提。',
     'GR9L_MODES GR9L_12', '不造官方类别奖励或全部物件无制作站；这里是选择建筑配方与查看放置预览，不是从库存领取建筑成品。'),
    ('没用助手也没放块时的走路',
     '助手与基础构件放置都没经历过，可以答真实在原作创意后院走过的一小段：当前草叶空隙能走。你先怎样投入？',
     '去亲眼看看没走过的空隙后面是什么|亲手跑跳一小段，喜欢输入与位置变化相连的反馈|先核对已经出现的基础操作说明，再继续实际尝试|只给自己已经去过的位置补记记录',
     'w f tool_reference_first game_recording',
     '第三真实最早移动经历，助手、材料与活虫都不必需。',
     'GR9L_STORE GR9L_MODES', '普通移动不自动探索，须未知发现动机；不编无虫仍有敌人。'),
    ('没制作站也没搭墙时的选物',
     '制作站和草墙放置都没体验过，可以答真实在创意建造目录选过一种基础形状：当前这类构件可用。你先怎样继续？',
     '先比较已开放的基础形状，再决定采用哪种|反复练目录分类、选墙形与进入预览，专门把这项建造菜单操作练熟|实际选中一个当前可用墙形，进入建造预览，亲手体验操作发生|先核对已经出现的基础选物说明，再继续尝试',
     'creative_option_review t available_operation_trial tool_reference_first',
     '第三早期目录动作，不编尚未摆好的制作站。',
     'GR9L_MODES GR9L_12', '一次普通选物不计训练；配方免材料不替代站点条件。'),
    ('没调灯摆装饰时的基础墙形',
     '调灯与装饰摆放都没体验过，可以答实际只放过基础墙面：当前形状可选，也有能放位置。你先怎样投入？',
     '把几块墙排成自己想表达的住处轮廓|亲手放下一块，喜欢输入与墙面出现相连的反馈|只调整一块待放草墙预览的位置，再实际放下查看结果|先比较当前确实可用的基础墙形，再决定采用哪种',
     'a f creative_edit_trial creative_option_review',
     '第三真实基础建造经历，外观表达与普通改位置区分。',
     'GR9L_12 GR9L_MODES', '不假造任意材质或RGB；没有表达动机不因选一面墙计a。'),
    ('没复制墙面或放地板时的现有目录',
     '复制墙面与放地板都没体验过，可以答实际只浏览过创意基础构件的一段：当前几类墙形可查看，也能选中进入预览。你先怎样继续？',
     '先比较当前已开放的基础形状，再决定采用哪种|先核对已经出现的基础建造说明，再继续尝试|把想看全的构件类别列成自己的清单，先补看还没见过的一类，想把这套类别看齐|实际选中一款当前可用墙形，进入建造预览，亲手体验操作发生',
     'creative_option_review tool_reference_first c available_operation_trial',
     '第三真实观察经历，不要求结构故障或实际施工。',
     'GR9L_MODES GR9L_12', '不是读取整个数据库或官方全收集奖励；普通目录比较0。'),
    ('没逛后院时的基础选物',
     '熟悉小屋和后院走路都没经历过，可以答真实在原作创意目录选过基础墙形的一段：当前能选中，并进入建造预览。你先怎样投入？',
     '亲手切换一次当前墙形，喜欢输入与眼前预览变化相连的反馈|实际选中一个当前可用墙形，进入建造预览，亲手体验操作发生|先比较已经可用的基础形状，再决定采用哪种|先核对已经出现的选物说明，再继续尝试',
     'f available_operation_trial creative_option_review tool_reference_first',
     '第三真实最早菜单操作，不让未有熟悉家园者假答H。',
     'GR9L_MODES GR9L_12', '当前一个菜单操作0，不造身体资源压力或人物成长。'),
    ('没篮球装饰时的普通放置',
     '篮球与装饰都没用过，可以答实际放过一块基础墙：当前构件可用，有可放位置。你先怎样投入？',
     '反复练选块、转向与落位，专门把建造操作练熟|亲手放下一块，喜欢输入与形状出现相连的反馈|只实际放下当前这一块构件，亲手体验操作发生|先核对已有放置说明，再继续自己的实际尝试',
     't f available_operation_trial tool_reference_first',
     '第三真实基础建造，不靠尚未制作的篮球。',
     'GR9L_12 GR9L_MODES', '一次普通放置不计t/i，未有对手不造竞争。'),
    ('没箱子与基础建造时的现有小物',
     '箱子和基础草墙放置都没经历过，可以答实际拿过一件当前能取放的小物：现有物件已在手边。你先怎样继续？',
     '按已有物件实际调整一次携带或存放，再继续安排|亲手取放一件，喜欢输入与物件变化相连的反馈|只给已经取得的物品与发现位置补记记录|先核对已经出现的取放说明，再继续自己的实际尝试',
     'item_handling_action f game_recording tool_reference_first',
     '第三真实物件操作，不编尚未建造的容器。',
     'GR9L_STORE GR9L_MODES', '无材料压力不等于没有取放；物品变多不自动计收集或经营。'),
    ('真实没反复改家也没搭墙时',
     '反复修改基地与草墙放置都没经历过，可以回想实际在创意目录选过一件构件的一段：哪种已做投入更贴近愿意保留的体验？',
     '反复练过目录分类、选墙形与进入预览，专门把建造菜单操作练熟|亲手选中过一款墙形，喜欢输入与眼前预览变化相连的反馈|只是先比较当时已经可用的基础形状，再决定采用哪种|只是核对当时已出现的选物说明，再继续尝试',
     't f creative_option_review tool_reference_first',
     '第三真实较早菜单经历，无持续对象不逼答g。',
     'GR9L_12 GR9L_MODES', '已经全开配方也不是角色持续培养经历；普通点击不计训练。'),
    ('真实没补门廊投篮时的放置',
     '门廊和篮球都没体验过，可以回想实际放过一块基础构件的一段：哪种已做投入更贴近愿意保留的体验？',
     '把几块排成自己想表达的住处轮廓|亲手放一件，喜欢输入与眼前形状出现相连的反馈|只是实际放下当时一个可用构件，亲手体验操作发生|只是给当时已放过的构件与步骤补记建设过程',
     'a f available_operation_trial construction_process_recording',
     '第三真实基础动作，不因没高级工具而制造未见原因检验。',
     'GR9L_12 GR9L_MODES', '只在本人确实有表达动机时计a；普通编辑与过程记录0。'),
    ('真实未选外观取小物时',
     '家园外观与小物取放都没经历过，可以回想实际在原作创意目录看过基础构件的一段：哪种已做投入更贴近愿意保留的体验？',
     '列过自己想看齐的构件类别，专门补看当时还没见过的一类，想补齐这套类别|只是先比较当时已开放的基础形状，再决定采用哪种|只是先核对当时已有的基础建造说明，再继续实际尝试|实际选中一款当时可用墙形，查看它的建造预览',
     'c creative_option_review tool_reference_first available_operation_trial',
     '真实目录观察与分类选择，不冒充已取得物品或施工；个人类别补全动机c与工具说明、实际菜单选择、当前外观方案比较0分开。',
     'GR9L_MODES GR9L_12', '不让未取物者冒充已放置；目录浏览不自动计收藏或风格。'),
    ('真实没有同游安居时的最早建造',
     '真人同游与熟悉基地停留都没经历过，可以回想真实单人在创意后院搭过最早几块墙的一段：哪种已做投入更贴近愿意保留的体验？',
     '把几块墙排成自己想表达的住处轮廓|亲手放下一块，喜欢输入与墙面出现相连的反馈|排清过当时选墙形、转向与落位的编辑先后，再照顺序动手完成|只是核对当时已经出现的基础建造说明，再继续尝试',
     'a f creative_workflow_plan tool_reference_first',
     '第三真实单人施工，不以NPC助手冒充真人协作。',
     'GR9L_MODES GR9L_12', '未体验仍可继续换其他已核实专属情境；三种为当前容量起点，不是无限情境或所有玩家都适用的证明。'),
]
for _n, _row in enumerate(_GR_CREATIVE_THIRDS):
    GR_CREATIVE[_n]['variants'].append(_extra(*_row, reflection=_n >= 8))


SOURCES.append(source('GR9L_SHROOM', 'Obsidian：ShroomAndDoom蘑菇浆与烤炉实际正文',
    'https://grounded.obsidian.net/news/grounded/shroom-and-doom-update-out-now', 'developer_released_feature_targeted_returned_body',
    'Grinder将蘑菇磨浆|Oven将浆烤成砖|多种原生基础墙与草屋构件|部分构件可翻转|蓝图补料',
    '2026-10-31实际读检索返回TheShroom、NewCraftingStructures、Gardening、基础构件和BuildingWallReplacement段，另web打开返回中的20-60及147-184行作定向复核；不声称完整365行或视频。只取蘑菇磨浆、烤炉成砖与已发布的基础构件，不采用旧时期最坚固、全部蘑菇、宠物易死或配方/玩法数值。'))

GR_DESIGN = [
    Q(1, 'Grassbox里第一处自制场地',
      '你在原作Playgrounds的Design Mode里，当前可以摆放与旋转场景物件；Grassbox已有空地，也有可用的空实验室。不是普通后院生存，先怎样开始这一处？',
      '用现成草叶、墙面与道具表达自己想做的微缩场地风格|反复练选物、自由旋转与落位，专门把编辑工具操作练熟|排清这轮地面、入口与场景物件落位的编辑先后，再照顺序动手完成|先比较当前已开放的场景构件，再决定这一处用哪些',
      'a t creative_workflow_plan creative_option_review',
      '原生Grassbox场景编辑；风格与刻意工具训练分别明确，单轮施工和目录比较0。只摆一个布局不自动计新玩法。',
      'GR9L_13 GR9L_CURRENT',
      ('没用过Grassbox空实验室，可答实际在普通后院场景开过Playground设计的一段：当前一件现成道具可放，也能自由旋转。你先怎样投入？',
       '把这件道具与已有构件排成自己想表达的场地感觉|亲手转向再放下一件，喜欢输入与眼前位置变化相连的反馈|只实际改一件当前可编辑道具的位置或造型，看这轮结果|先核对已经出现的编辑工具说明，再继续自己的尝试',
       'a f creative_edit_trial tool_reference_first'),
      'Playground自由摆放和空中放置不是普通生存默认；不混Grounded2，不要求已解主线、MOD或在线发布。'),
    Q(2, '按钮按下后PlantLamp没亮',
      '你已有一个Button与一盏Plant Lamp，实际建了Link；这一轮试玩按下按钮，灯没出现预期变化，触发Event和Action都还没核清。回到Design后，先怎样处理？',
      '猜Link选到的Action不对，固定Event、其他连接与按钮和灯的位置，只改这一项Action再试玩检验|先查看当前已经显示的Link、Event与Action，核对实际连接状态|先核对已经出现的Link工具操作说明，再亲自继续这一轮调整|先切进Play Mode实际按一次当前按钮，亲手体验这条已建连接怎样响应',
      'p device_status_review tool_reference_first available_operation_trial',
      '开发者明确按钮可以切灯；现象和未知原因给足，单项测试p与静态状态查看0分开，不预告猜想为解答。',
      'GR9L_13',
      ('没连过按钮和灯，可答实际在Design里摆过一个Button：当前能放，位置可编辑，还没有开始连线。你先怎样继续？',
       '反复练选物、转向与落位，专门把编辑操作练熟|亲手放下一件，喜欢输入与位置变化相连的反馈|只实际改当前这个按钮的位置，看这轮编辑结果|先核对已出现的Link与按钮操作说明，再继续尝试',
       't f creative_edit_trial tool_reference_first'),
      '只查看76，真实改Action是操作而非静态状态0；尚未连线不假答因果检验，不要求编辑器所有事件都可互连。'),
    Q(3, 'Timer和LaserCannon的实际节奏',
      '你在Playground已有Timer与Laser Cannon的可用连接，能试玩并调整当前发射间隔；刚才两轮通过这段的情况不同，还没核清与间隔怎样有关。现在可以保持同一路线再试，先怎样投入？',
      '猜通过情况与发射间隔有关，固定路线、起步站位和起步时点，只改一项间隔，再以同样走法试玩检验|反复练观察发射、起步与停步，专门让这一段通过操作更熟|亲手试玩一小段，喜欢移动、光束和声音接连发生的反馈|只实际换一次已经会用的起步时点，体验这一轮怎样通过',
      'p t f try_action_variant',
      '开发者明确Timer可触发LaserCannon；未知规律单项检验、刻意训练与反馈分别表达，普通换一次时点0。',
      'GR9L_13',
      ('没做过定时激光，可答实际只连过按钮与灯：当前连接可用，按一下会让灯切换。你先怎样投入？',
       '亲手按一次，喜欢输入与灯光变化紧接着发生的反馈|实际用一次当前已连好的按钮，亲手体验操作发生|先在Design查看已显示的Link与当前装置状态，再决定这一轮怎样改|先核对已有Link操作说明，再继续实际尝试',
       'f available_operation_trial device_status_review tool_reference_first'),
      '不固定秒数、伤害、受伤或无敌设置；只问当前能试玩的连接，未说明的条件不能冒充已验证原因。'),
    Q(4, 'SuperBouncePad后的一段自制跑跳',
      '你已在Design里放好一个当前可用的Super Bounce Pad与Landing Pad，Play Mode能实际走这段；旁边还有可编辑的落脚物件。你先怎样处理？',
      '反复练靠近、踏上反弹垫与转向落脚，专门把这段操作练熟|把落脚物件与周围道具摆成自己想表达的场地风格|排清这轮起点、落点与转向的先后，再照路线安排亲手试玩|只实际调整一件当前可编辑落脚物的位置，看这轮改动结果',
      't a platform_route_plan creative_edit_trial',
      '原生反弹/落脚Gadgets的实际工具情境；刻意练习与风格分开，路线顺序和移动一个物件0。',
      'GR9L_13',
      ('没用过这些Gadgets，可答实际只摆过两块基础平台的一段：当前Play Mode能走、能跳并到达这处，Design里位置可编辑。你先怎样投入？',
       '亲手走跳一小段，喜欢输入与位置变化相连的反馈|排清这轮落脚、转向和动作衔接，再照路线安排尝试|只实际改一块当前可编辑平台的位置，看这轮结果|先核对已经出现的基础编辑说明，再继续尝试',
       'f platform_route_plan creative_edit_trial tool_reference_first'),
      '不固定弹力数值、落地无伤或任何位置必能跳过；只改平台间距不自动计自创玩法。'),
    Q(5, '投篮、计数与下一道门',
      '你在Playgrounds实际用过Basketball Hoop、Score Board、Counter with Condition与门的连接，这些工具当前确实可连；上轮试玩里门没按预期开，你还没核清原因。现在想给这一小段继续设计可玩的内容。你先怎样投入？',
      '设计自己定规则的投篮闯门小关：先用现有计数条件开门，再让进入者选择下一处投篮目标，并亲手试玩这套玩法|猜门没开与计数条件有关，固定其他连接和设置，用相同站位与投篮方式，只改当前一项条件再试玩检验|把篮筐、门框和已有道具排成自己想表达的微型球场外观|先查看当前已显示的计数、条件与连接状态，再决定怎样改',
      'i p a device_status_review',
      'I是本人设计有目标/规则/后续选择且亲测的新可玩小关，不是普通摆放或限制步数；开发者已证投篮可触发计数开门。',
      'GR9L_13',
      ('没做过计数开门，可答实际只试玩过自放篮筐和篮球的一段：当前能投，也能再试。你先怎样投入？',
       '反复练瞄准与力度，专门把投篮操作练熟|亲手投一次，喜欢球路、碰筐与声音接连发生的反馈|只是实际换一次已经会用的出手时点，体验这一轮怎样投|先核对当时已经出现的篮球操作说明，再继续尝试',
       't f try_action_variant tool_reference_first'),
      '不把普通篮球本身计i，不固定进球数、奖励或脚本字段；尚未有连接者不被迫假答调逻辑。'),
    Q(6, '已能试玩的自制昆虫竞技场',
      '你在Playground已有能用的Creature Spawner和实际可试玩场地；手里有仍可保留的旧武器，另有一组当前允许换用的装备与突变。不是普通后院首领考核，先怎样投入？',
      '比较这两组当前允许的装备与突变，亲自试玩检验组合效果|反复练观察起手与格挡时点，专门把自己的操作练熟|按我给少年设定的惜旧战士身份，先保留当前旧武器上场，暂不换新的一组|只先比较当前已经可用的装备和突变，再决定这一轮采用哪组',
      'b t r compare_available_setup',
      '刷出和配置以当前实际允许为前提；组合亲测b、刻意练习t和角色选择旧武器r分开，普通比较0。',
      'GR9L_13 GR9L_CURRENT GR9L_STORE',
      ('没做过昆虫竞技场，可答实际在Playground放过一件可拿武器的一段：当前能在试玩中拿起使用，手头还有一件仍可收好的旧工具。你先怎样投入？',
       '亲手试一次，喜欢出手、声音和眼前反应紧接着发生的反馈|实际换用这一件当前可用装备，亲手体验它怎样发挥|先核对已经出现的装备操作说明，再继续自己的尝试|按我给少年设定的惜物习惯，先收好当前仍能留的旧工具，再试这件装备',
       'f try_available_setup tool_reference_first r'),
      '不要求原作Boss召唤物、固定刷出数量/强度或所有配置都可用；生成昆虫、宠物与助手不是其他真人。'),
    Q(7, 'TimeOfDay与MusicChanger的一处气氛',
      '你在Design里已用过当前可用的Time of Day与Music Changer，场地里还有可编辑的墙面与现成道具；这次不赶普通生存食水。你先怎样布置？',
      '安排当前可选时段、声音和构件，让场地呈现自己想表达的微缩冒险气氛|亲手切一次当前可用时段或音乐，喜欢输入与场景回应紧接着发生的反馈|只实际使用一次当前可用的时段或音乐设置，亲手看操作发生|先比较当前已经开放的构件与气氛方案，再决定采用哪种',
      'a f available_operation_trial creative_option_review',
      '明确表达场景风格才a，直接切换0；不把所有音效/时段更换当发明或故事联系。',
      'GR9L_13',
      ('没用过这些Gizmos，可答实际摆过一件普通场景道具：当前能改位置和朝向。你先怎样投入？',
       '把它与现成墙面排成自己想表达的场地风格|亲手转一次再放下，喜欢输入与位置变化相连的反馈|只实际改这一件当前可编辑道具的位置，看这轮结果|先核对已经出现的基础编辑说明，再继续尝试',
       'a f creative_edit_trial tool_reference_first'),
      '不保证任意音乐导入、真人配音或当前没有的夜景；普通音频/时段切换不用只限尺寸位置造型颜色的creative_edit_trial。'),
    Q(8, '试玩回Design之后再改一处',
      '你此前逐次完善同一份小关，刚又在Play Mode试过并回到Design；试玩状态回到未玩时，现在准备改一处入口再试。先怎样继续？',
      '排清这轮入口构件选取、转向与摆放的编辑先后，再照顺序动手完成|只实际调整一个当前可编辑入口构件的位置，看这次编辑结果|先核对已经出现的设计/试玩切换说明，再继续尝试|继续完善同一份Playground，喜欢先前投入逐渐留在自己做的场地上',
      'creative_workflow_plan creative_edit_trial tool_reference_first g',
      '试玩返回Design重置是原生规则，不把一次改-试循环计生产系统；同一作品持续积累须明确动机才g。',
      'GR9L_13',
      ('还没切过Play Mode，可答实际在Design只摆过几件场景物：当前有可编辑位置，工具说明已经出现。你先怎样继续？',
       '排清本轮先选哪件、再怎样转向与摆放的编辑先后，再照顺序动手完成|把几件现成物排成自己想表达的场地风格|只实际改一个当前可编辑物件的位置，看这轮结果|先核对已经出现的基础编辑说明，再继续尝试',
       'creative_workflow_plan a creative_edit_trial tool_reference_first'),
      '不要把PlayMode临时状态当SharedWorld持久进度；不承诺试玩中所有改动回写或无限撤销。'),
    Q(9, '真实逐次完善的同一份Playground',
      '回想你真实多次回来改同一份Playground的一段：场地里已有篮球、篮筐、计数与门，曾布置连接并试玩开门。哪种已做投入更贴近愿意保留的体验？',
      '继续完善同一份场地，喜欢自己先前投入逐渐留在作品上|给已有投篮计数与门设计自己定规则的闯门小关，安排过门后选下一处投篮目标，再亲自试玩这套玩法|用已有道具、墙面和气氛设置表达自己想要的微缩场地感觉|只是给已编辑的构件、连接与实际步骤补记建设过程',
      'g i a construction_process_recording',
      '同一作品持续完善g、真正自制规则与目标玩法i、视觉气氛表达a分开；连接/步骤补记0。',
      'GR9L_13',
      ('没有多次改同一作品，可回想实际第一次在Design放过一件普通道具的一段：哪种已做动作更贴近愿意保留的体验？',
       '把它与已有物件排成自己想表达的场地风格|专门反复练选物、旋转与落位，目的是让编辑操作更熟|只是实际改一件当时可编辑道具的位置，看这次结果|只是核对当时已有的基础编辑说明，再继续尝试',
       'a t creative_edit_trial tool_reference_first'),
      '一次放置不算g，普通布局不计i；没有发布、没获得下载或赞也可答。'),
    Q(10, '真实排查过的一条Link',
      '回想你真实在Design连接按钮与灯、Timer与激光，或投篮计数与门，并到Play Mode试过的一段：哪种已做投入更贴近愿意保留的体验？',
      '当时有尚未确认的连接原因猜想，保持其他设置不变，只改一项Event或Action再试玩检验|反复练过操纵、对准与确认连接，专门把工具操作练熟|亲手触发一次，喜欢输入与灯光、声音或场地变化相连的反馈|先在Design查看当时已显示的Link与装置状态，再决定这一轮怎样调整',
      'p t f device_status_review',
      '未知原因单项测试、刻意工具练习和反馈分别明确；76只核对静态连接，不包含实际开关改变。',
      'GR9L_13',
      ('没有连过Link，可回想实际只在Play Mode走过自放平台的一段：哪种已做投入更贴近愿意保留的体验？',
       '反复练起步、转向与落脚，专门把这一段操作练熟|亲手走跳一段，喜欢输入与位置变化相连的反馈|只是排清落脚、转向与动作衔接，再照这轮路线安排试|只是核对当时已出现的移动说明，再继续尝试',
       't f platform_route_plan tool_reference_first'),
      '已知教程答案不是未知原因，单次点击不是训练；不把普通连接、操作顺序或已有设置比较强计i/y。'),
    Q(11, '真实建过的一处熟悉场地',
      '回想你真实再次回到自己已做熟的Playground场地的一段：当时精力够，另有一处可达但没仔细看过的空实验室，也能继续编辑当前场地。哪种已做投入更贴近愿意保留的体验？',
      '仍在自己熟悉的场地里慢慢走走，喜欢待在这片已经走熟的地方|去看一个当前能到但没仔细看过的空实验室，想亲眼知道内部空间|把现成道具与墙面改成自己想表达的场地风格|只是给自己已经摆过的构件与实际步骤补记建设过程',
      'h w a construction_process_recording',
      'H有精力与新可选内容仍主动熟悉停留；探索须未见内容，风格与普通建设记录0分开。',
      'GR9L_13',
      ('没有熟悉场地，可回想实际只在Design浏览过场景物目录的一段：哪种已做投入更贴近愿意保留的体验？',
       '列过自己想看齐的场景物类别，专门补看当时还没见过的一类，想补齐这套类别|只是先比较当时已经开放的道具外观，再决定采用哪种|只是核对当时已有的选物操作说明，再继续尝试|实际选中一件当时可用场景物，查看它的待放预览',
       'c creative_option_review tool_reference_first available_operation_trial'),
      '没有精力、无新去向或无编辑权限导致的停留不计H；目录大不是本人收藏动机。'),
    Q(12, '真实多人一起设计过的场地',
      '回想确有其他真人与你在原作Design Mode一起做Playground的一段：当时一边能布置跑跳平台，一边能改按钮与灯。哪种真实投入更贴近愿意保留的体验？',
      '先谈清这轮共同想做的可玩内容，商量谁摆平台、谁调现有连接与何时一起试玩|先陪同伴在正在做的场地边走走聊天，喜欢一起待在这里的陪伴|用现有道具与墙面表达自己想要的场地风格|只是给已经一起改过的构件、连接与步骤补记建设过程',
      'q o a construction_process_recording',
      '原生支持设计多人；共同安排与陪伴分开，个人风格和建设记录0不借真人人数计分。',
      'GR9L_13 GR9L_STORE',
      ('只有单人设计经历，可回想真实反复回来改同一份Playground的一段：此前几次投入已经留在这份场地上。哪种已做投入更贴近愿意保留的体验？',
       '继续完善同一场地，喜欢先前投入逐渐留在作品上|反复练选物、旋转与落位，专门把编辑操作练熟|用已有道具与墙面表达自己想要的场地风格|只是核对当时已出现的编辑操作说明，再继续尝试',
       'g t a tool_reference_first'),
      '不是下载玩家自动获得共同编辑权；不保证跨平台连接无障碍，不从发布和点赞或榜单排名推真人竞争。'),
]

_GR_DESIGN_THIRDS = [
    ('没摆场景物时的Design目录',
     'Grassbox和后院场景摆放都没体验过，可以答真实在Design看过物件目录：当前有可选基础道具。你先怎样投入？',
     '把想看全的场景物类别列成自己的清单，先补看还没见过的一类，想把这套类别看齐|先比较当前已开放的道具外观，再决定采用哪种|实际选出一件当前可用道具，亲手体验操作发生|先核对已有选物操作说明，再继续尝试',
     'c creative_option_review available_operation_trial tool_reference_first',
     '第三真实最早设计工具经历，不需整场地或高级逻辑。',
     'GR9L_13', '不造全部开发物件可用或官方收藏成就；一次普通目录选择0。'),
    ('没连接也没摆按钮时的普通道具',
     '按钮连接与摆放都没体验过，可以答实际在Design摆过一件普通场景道具：当前位置与朝向能改。你先怎样继续？',
     '把它与现成墙面排成自己想表达的场地风格|亲手转向再放一件，喜欢输入与位置变化相连的反馈|只实际改这一件当前可编辑道具的位置，看这轮结果|先核对已经出现的基础编辑说明，再继续尝试',
     'a f creative_edit_trial tool_reference_first',
     '第三真实普通摆放情境，不为未连线者编装置原因。',
     'GR9L_13', '普通换位置不计发明，风格须本人明确目的。'),
    ('没激光和按钮时的基础试玩',
     '定时激光与按钮灯都没经历过，可以答实际在自己Design出的空平台切过Play Mode的一段：当前能走、能跳，也能重试。你先怎样投入？',
     '亲手走跳一小段，喜欢输入与位置变化相连的反馈|反复练起步、转向与落脚，专门让这一段操作更熟|排清落脚、转向与动作衔接，再照本轮路线安排试|先核对已有移动操作说明，再继续尝试',
     'f t platform_route_plan tool_reference_first',
     '第三真实试玩操作，没逻辑装置也可回顾。',
     'GR9L_13', '不保证任意平台都可通过、试玩无伤或退回Design保留已玩进度。'),
    ('没跑跳试玩时的两块平台',
     '反弹装置与基础平台试玩都没体验过，可以答实际在Design放过两块基础构件：当前能改它们位置。你先怎样投入？',
     '用这两块与已有道具表达自己想要的场地风格|反复练选物、转向与落位，专门把编辑操作练熟|只实际改一块当前可编辑构件的位置，看这轮结果|先核对已出现的基础编辑说明，再继续尝试',
     'a t creative_edit_trial tool_reference_first',
     '第三真实设计而非试玩经历，不假答跑跳。',
     'GR9L_13', '移动两块位置不是自创规则，没实际试玩不推通过规律。'),
    ('没计数投篮时的普通构件',
     '计数开门与篮球都没体验过，可以答实际在Design摆过一个基础构件：当前可放，也能旋转。你先怎样投入？',
     '反复练选物、旋转与落位，专门把编辑操作练熟|亲手放下一件，喜欢输入与形状变化相连的反馈|只实际改一个当前可编辑构件的位置，看这轮结果|先核对已经出现的基础编辑说明，再继续尝试',
     't f creative_edit_trial tool_reference_first',
     '第三真实早期编辑，无复杂规则或逻辑前提。',
     'GR9L_13', '不为没有篮球经历者造关卡，不把普通摆放算i。'),
    ('没竞技场和试玩装备时的目录',
     '昆虫竞技场与试玩装备都没体验过，可以答实际在Design查看过当前物件目录：现有可用场景物能比较。你先怎样继续？',
     '先比较当前已开放的场景物外观，再决定采用哪种|把想看全的场景物类别列成自己的清单，先补看还没见过的一类，想把这套类别看齐|先核对当前已出现的工具说明，再继续尝试|实际选出一件当前可用道具，亲手体验这项操作',
     'creative_option_review c tool_reference_first available_operation_trial',
     '第三真实目录经历，不假装已刷出或用过敌人。',
     'GR9L_13', '目录存在不推角色熟练、配装检验或收藏动机。'),
    ('没气氛与摆物时的场地观察',
     '气氛工具和普通道具摆放都没体验过，可以答实际在Design查看过一个现成空实验室：当前能走进这处，也能看已存在物件。你先怎样投入？',
     '走进还没仔细看过的部分，想亲眼知道空间怎样展开|先查看当前能到的入口与现场，再决定这段怎样继续|只给自己已经看过的位置补记记录|先核对已经出现的基础编辑说明，再继续尝试',
     'w scene_inspection game_recording tool_reference_first',
     '第三真实现成空间观察，不需已动手改物。',
     'GR9L_13', '不造本体任务、未读剧情或每个空实验室必有相同道具。'),
    ('没试玩摆物时的Design选物',
     '切换试玩与实际摆场景物都没经历过，可以答真实在Design选过一个当前可用道具：菜单与操作说明已出现。你先怎样继续？',
     '先比较当前已开放的场景物外观，再决定采用哪种|实际选出一件当前可用道具，亲手体验操作发生|反复练目录分类、选物与查看待放预览，专门让这套编辑菜单操作更熟|先核对已经出现的选物说明，再继续尝试',
     'creative_option_review available_operation_trial t tool_reference_first',
     '第三真实最早工具经历，不冒充切换试玩已成功。',
     'GR9L_13', '一次普通选择不算训练，单轮操作不计生产系统。'),
    ('真实没有持续改场地摆物时',
     '反复改同一场地与实际摆放都没经历过，可以回想真实在Design目录看过道具的一段：哪种已做投入更贴近愿意保留的体验？',
     '列过自己想看齐的道具类别清单，专门补看还没见过的一类，想补齐这套类别|只是先比较当时已开放的场景物外观，再决定采用哪种|只是核对当时已出现的基础工具说明，再继续尝试|实际选中一件当时可用道具，查看它的待放预览',
     'c creative_option_review tool_reference_first available_operation_trial',
     '第三真实早期观察，无持续作品不逼答g/i。',
     'GR9L_13', '目录数量或单次选择不是持续完善和自创游戏的证据。'),
    ('真实没连线试玩时的普通放置',
     'Link与平台试玩都没体验过，可以回想实际在Design放过一件普通道具的一段：哪种已做投入更贴近愿意保留的体验？',
     '用它与现成墙面表达自己想要的场地风格|亲手转向再放下，喜欢输入与位置变化相连的反馈|只是实际改一件当时可编辑道具的位置，看这次结果|只是核对当时已出现的基础编辑说明，再继续尝试',
     'a f creative_edit_trial tool_reference_first',
     '第三真实编辑动作，不造未经历的连接试错。',
     'GR9L_13', '普通位置编辑不计因果研究，风格表达需本人明确动机。'),
    ('真实没熟悉场地看目录时',
     '熟悉场地与目录浏览都没经历过，可以回想真实只在Design空场景走过的一段：哪种已做动作更贴近愿意保留的体验？',
     '去看一处当时能到但没仔细看过的空间，想亲眼知道里面是什么|亲手走跳一小段，喜欢输入与位置变化相连的反馈|只是查看当时能到的入口与现场，再决定怎样继续|只是核对当时已经出现的基础操作说明，再继续尝试',
     'w f scene_inspection tool_reference_first',
     '第三真实移动阶段，无熟悉住处不硬计H。',
     'GR9L_13', '没有体力/新目标前提的停留不计H，不借生存资源压力解释Design。'),
    ('真实只有一次单人放置时',
     '多人和反复完善同一作品都没经历过，可以回想实际单人在Design放过一件道具的一段：哪种已做投入更贴近愿意保留的体验？',
     '用它与已有构件表达自己想要的场地风格|亲手放下一件，喜欢输入与形状变化相连的反馈|只是实际改一个当时可编辑道具的位置，看这次结果|只是给已经放过的构件与步骤补记建设过程',
     'a f creative_edit_trial construction_process_recording',
     '第三真实单人较早操作，不以NPC或未有同游补q/o。',
     'GR9L_13', '仍可继续换其他已核实专属情境，不提供跳过；三种仅当前草稿容量，不能承诺所有进度适用。'),
]
for _n, _row in enumerate(_GR_DESIGN_THIRDS):
    GR_DESIGN[_n]['variants'].append(_extra(*_row, reflection=_n >= 8))


SOURCES.append(source('GR9L_147', 'Obsidian：Patch1.4.7完整正文中的当前Playgrounds扩展',
    'https://steamstore-a.akamaihd.net/news/externalpost/steam_community_announcements/1797185861644717', 'developer_official_news_api_released_patch_body',
    'Playgrounds可启用原作StoryQuests|放置动物与装备可自订|原作当前逻辑仍维护|音乐新增曲目',
    '2026-10-31保存新闻API中实际完整6022字符已打印读完。只用于Playground是否能实际开放原作任务及设置边界；不将所有地图都视为已开剧情/装备自由切换，不采用REMIX.D层数、固定加成、动物/装备战力或Bug修复绝对保证。1.4.7.4815后续另证，不借Grounded2宣传。'))

GR_DOWNLOADED = [
    Q(1, '已有代码下载来的两份Playground',
      '你是原作Playground关卡的游玩者，已用真实代码下载可打开的关卡；一份熟悉跑跳关已玩过，另一份场地还没看过。这段精力够，两份现在都能玩，你先选哪种投入？',
      '打开没看过的那份，想亲眼知道作者把后院做成了什么|回熟悉那份慢慢走走，喜欢留在已经走熟的场地里|先核对已经出现的代码下载与游玩说明，再决定这轮打开哪份|先为自己已经玩过的地点与实际体验补记记录',
      'w h game_reference_first game_recording',
      '原生代码下载的真实玩家经历；未知发现与精力/新内容具备时主动熟悉停留分开，说明与已见信息记录0。',
      'GR9L_13',
      ('还没玩熟任何关卡，可答实际第一次打开一份已下载Playground：眼前有能到但没看过的入口，已有基本操作说明。你先怎样继续？',
       '走进去亲眼看看后面的空间是什么|亲手走这一小段，喜欢输入与位置变化相连的反馈|先核对已出现的基础操作说明，再继续尝试|先查看当前能到的入口与现场，再决定这段怎样继续',
       'w f tool_reference_first scene_inspection'),
      '不要求搜索网络热门榜、发布作品或拥有编辑权；代码只是原生下载机制，不承诺每份地图能连线/保存/改规则。'),
    Q(2, '作者搭好的一段跑跳平台',
      '你下载的这一关实际有一段能重试的跑跳平台，当前可走、可跳，也有两条已经可通行、落脚点可达的路线；你暂时不改关卡。先怎样投入？',
      '反复练起步、转向与落脚，专门让自己这段操作更熟|亲手跑跳这一段，享受输入、位移与落地反应接连发生的反馈|排清这轮落脚、转向与动作衔接，再照路线安排尝试|换走另一条已经能到的路线，亲手体验不同的行进方向',
      't f platform_route_plan route_variant',
      '玩家只能按当前关卡允许动作走，刻意练习与反馈分开；一次路线计划/换可达路线0，不当自创规则。',
      'GR9L_13',
      ('没玩过跑跳关，可答实际进入一份下载场地后走过的最初平地：前方有能到但没看过的空间。你先怎样继续？',
       '亲眼去看看没看过的空间里是什么|亲手走这一小段，喜欢输入与位置变化相连的反馈|先核对已出现的移动说明，再继续尝试|先查看当前能到的入口和现场，再决定这一段怎样继续',
       'w f tool_reference_first scene_inspection'),
      '不保证无限重生、无伤、计时暂停或每关都可跳；题面明确当前能重试，不要求进入Design改平台。'),
    Q(3, '逃脱关里还没弄清的按钮与灯',
      '你下载的逃脱小关实际有两个能按的按钮、一盏会变化的灯和一道尚未打开的门；还不清楚它们的关系，当前可以继续尝试。你先怎样做？',
      '猜左按钮会影响那盏灯，先不碰右按钮，只按左边观察一次，检验自己的猜想|先查看当前能到的按钮、灯与门口，核对眼前现场|先核对关卡已经给出的操作提示，再继续自己的尝试|按我给少年设定的记录员身份，先记下已经见过的灯与入口，再继续能做的尝试',
      'p scene_inspection game_reference_first r',
      '未知关系与只改一项动作才p；看现场/已给提示0，角色设定具体影响记录后继续r，不借编辑器连线面板。',
      'GR9L_13',
      ('没玩过逃脱关，可答实际在下载关卡按过一个按钮的一段：当前还能按，确实能看到机关反应，也已有操作说明；你还没开始推机关关系。你先怎样投入？',
       '亲手按一下，喜欢输入与眼前机关反应接连发生的反馈|只实际使用一次当前可用按钮，亲手体验操作发生|先核对已经出现的按钮操作说明，再继续尝试|先查看当前能到的按钮与现场，再决定这一段怎样继续',
       'f available_operation_trial tool_reference_first scene_inspection'),
      '这是明确当前地图具备的可见物，不宣称所有下载关都这样；Gizmos在PlayMode不可见，不让玩家偷看作者未开放的Link或条件。'),
    Q(4, '有投篮目标的一道闯关门',
      '你下载的一小关实际有可用篮球、篮筐与看得见的Score Board；已显示当前进门目标，投中后分数会变化，也允许继续投。你先怎样投入？',
      '反复练瞄准与出手力度，专门把自己的投篮操作练熟|亲手投一球，喜欢球路、碰筐和声音接连发生的反馈|按关卡已经显示的进门目标继续投，重点是推进这一项要求|先核对已经显示的目标和当前进度，再决定这一轮继续到哪一步',
      't f stated_objective_progress quest_progress_review',
      '原生投篮/ScoreBoard可接关卡目标；玩家训练、反馈与指定目标推进0分开，任务要求不是个人收藏动机。',
      'GR9L_13',
      ('没投过篮，可答实际在一份下载关卡看过当前目标与入口的一段：已有能执行的要求、当前进度和玩法说明。你先怎样继续？',
       '按当前已经显示的要求行动，先推进这一项目标|先核对已显示的目标与当前进度，再决定做到哪一步|先核对关卡已经给出的玩法说明，再继续尝试|先查看当前能到的入口与现场，再决定这一段怎样继续',
       'stated_objective_progress quest_progress_review game_reference_first scene_inspection'),
      '不固定投中数、门开启字段或任何奖励；只有已经显示的进度才可核对，普通个人目标不计对手竞争。'),
    Q(5, '作者允许换装的一段昆虫挑战',
      '你下载的这一关实际是昆虫挑战，作者当前允许使用手边两组装备与突变，眼前这段可以重试，也有退开恢复的空间。你先怎样投入？',
      '比较两组当前允许的装备与突变，亲自检验组合在这一关的效果|反复练观察起手与格挡时点，专门把自己的操作练熟|亲手交手一轮，喜欢出手、声音与昆虫反应接连发生的反馈|先排清攻击、耐力消耗与退开恢复的先后，再照这一轮循环尝试',
      'b t f combat_resource_cycle',
      '当前地图确实允许换装才问组合；角色数值由作者可改，不作统一战力评估。刻意训练和反馈各有明确动机。',
      'GR9L_13 GR9L_147 GR9L_CURRENT GR9L_STORE',
      ('没玩过昆虫挑战，可答实际在下载场地只走过一段跑跳路：当前能重试，也能查看基本操作说明。你先怎样投入？',
       '反复练起步、转向与落脚，专门让这一段操作更熟|亲手走跳一段，喜欢输入与位置变化相连的反馈|排清落脚、转向与动作衔接，再照本轮路线安排试|先核对已出现的移动说明，再继续尝试',
       't f platform_route_plan tool_reference_first'),
      '不要求首领、普通后院召唤物、固定配装与伤害；下载不自动拥有改装备数值权限，没允许重试者换其他情境。'),
    Q(6, '这份地图确实启用了原作剧情',
      '你玩的Playground确实已启用原作Story Quests，你已经在其中见过Oak Lab、与BURG.L交谈并读过实验室录音；有已显示目标可继续。先怎样投入？',
      '回看已得录音和已见对话，把缩小实验里已知人物与事件的先后接起来|按当前已经显示的任务要求行动，先推进这一项目标|先核对已显示目标与当前进度，再决定做到哪一步|按我给少年设定的记录员身份，先记下已知实验线索，再继续这段可走旅程',
      's stated_objective_progress quest_progress_review r',
      '1.4.7证实Playground可开启原作剧情，但本题必须玩家当前确有且已见；故事联系与任务推进0/进度查看0不同。',
      'GR9L_147 GR9L_STORY_FIX GR9L_13',
      ('没在Playground见过原作剧情，可答实际下载关卡里一项已显示目标：当前能执行，进度与基本操作说明都能看。你先怎样继续？',
       '按这项已经显示的要求行动，重点推进当前目标|先核对已显示目标与当前进度，再决定做到哪一步|先核对关卡已给出的玩法说明，再继续尝试|只给自己在这份关卡已经去过的位置补记记录',
       'stated_objective_progress quest_progress_review game_reference_first game_recording'),
      '不将StoryQuests当所有Playground默认开启，不编作者自创NPC台词或未读后续；BURG.L是NPC，不提供真人社交点。'),
    Q(7, '激光之间的一次起步',
      '你下载的关卡里，Laser Cannon实际按节奏发射；刚才两次走同一路段的通过情况不同，原因尚未核清。当前能观察、能重试，但不能改作者的Timer。你先怎样投入？',
      '猜通过情况与起步时点有关，固定路线、走法和其他当前条件，只换一次起步时点检验|反复练观察发射、起步与停步，专门让自己的这一段操作更熟|亲手试走一轮，喜欢移动、光束与声音接连发生的反馈|只实际换一次已经会用的起步时点，体验这轮怎样通过',
      'p t f try_action_variant',
      '同样动作的未知原因检验p与仅换一次做法0有明确目的差别；玩家不能偷改设计器计时设置。',
      'GR9L_13',
      ('没碰过激光关，可答实际在下载场地走过一段有转角的平路：当前两侧都能通行。你先怎样继续？',
       '去看一处能到但没看过的转角后面是什么|亲手走这一段，喜欢输入与位置变化相连的反馈|换走另一侧已能通行的路，亲手体验不同方向|先查看当前能到的入口与现场，再决定这段怎样继续',
       'w f route_variant scene_inspection'),
      '不预告激光必有固定周期、一定无伤或每次失败状态相同；真实有可重试条件才答，不用编辑器权限兜底。'),
    Q(8, '有真人比分的一轮友人挑战',
      '你与其他真人正在同一份已下载Playground里玩一轮投篮或跑跳比分挑战；当前规则确实显示可比较的玩家成绩，大家同意照这套规则比。你先怎样投入？',
      '以这一轮超过其他参与者的分数或名次为明确目标，反复尝试争取领先|反复练一小段出手或落脚，专门把自己的操作练熟，暂不以超过别人为重点|先谈清这轮共同采用的规则、如何看成绩与何时一起结束|陪同伴边试边聊天，喜欢一起待在这个场地的陪伴',
      'k t q o',
      '只有真实对手和已同意可比规则才k；刻意训练t、共同安排q、陪伴o明确区分。不是官方全球榜或现实能力排名。',
      'GR9L_13 GR9L_STORE',
      ('只有单人关卡经历，可答实际在下载的投篮场地挑战过自己的分数目标：篮球与篮筐可用，Score Board确实显示当前得分，也允许再投。你先怎样投入？',
       '为这一轮自己设定的得分目标再投一次|反复练瞄准与蓄力出手，专门让自己的投篮操作更熟|亲手投一轮，喜欢球路、碰筐声音与结果接连发生的反馈|先核对关卡已经给出的计分与篮球玩法说明，再继续自己的实际尝试',
       'score_goal_attempt t f game_reference_first'),
      '个人纪录不计k，不能用一人计时假造排名；不同作者改过数值的关卡成绩不作跨玩家能力比较。'),
    Q(9, '真实再次回到熟悉的下载关卡',
      '回想你真实再打开已经玩熟的一份Playground的一段：当时精力够，也有另一份没玩过且可打开的关卡。哪种已做投入更贴近愿意保留的体验？',
      '仍在熟悉场地里慢慢走走，喜欢留在已经走熟的地方|打开没看过的关卡，想亲眼知道作者把后院做成什么|专门反复练熟悉关里的一小段落脚或出手，目的是让自己的操作更熟|只是为自己已经玩过的位置与实际体验补记记录',
      'h w t game_recording',
      'H须精力与新内容均具备仍主动熟悉停留；发现新内容和刻意练习有各自动机，补记0。',
      'GR9L_13',
      ('没有玩熟任何关卡，可回想真实第一次打开下载场地的一段：哪种已做投入更贴近愿意保留的体验？',
       '走进当时能到但没看过的入口，想亲眼知道里面是什么|亲手走过一段，喜欢输入与位置变化相连的反馈|只是核对当时已出现的基础操作说明，再继续尝试|只是查看当时能到的入口与现场，再决定这一段怎样继续',
       'w f tool_reference_first scene_inspection'),
      '不以因疲劳/缺权限/只有一关可玩导致的停留计H；反复重开关卡不自动代表持续角色培养g。'),
    Q(10, '真实玩过的寻物小关',
      '回想你真实玩过Playground寻物关的一段：当时该轮指定目标已完成，还能在已开放场地继续走；自己确实拿到过几类可拿物件。哪种已做投入更贴近愿意保留的体验？',
      '把拿过的物件类别列成自己的补全清单，继续找还没拿到的一类，想补齐自己的这套|走进能到但没看过的地方，想亲眼知道那里是什么，暂不为指定奖励而走|按我给少年设定的记录员身份，先记下已见物件与位置，再继续能走路段|只是给自己已经取得的物件与发现位置补记记录',
      'c w r game_recording',
      '已完成指定目标后仍以自己类别缺口投入才c，不把作者让找物的任务本身计收藏；未知发现与身份行动分开。',
      'GR9L_13',
      ('没玩过寻物关，可回想实际在一份下载关卡看过并执行当前目标的一段：哪种已做投入更贴近愿意保留的体验？',
       '只是按当时已经显示的目标行动，重点推进那一项要求|只是核对当时已显示的目标和进度，再决定做到哪一步|亲手操作一轮，喜欢输入与眼前反应接连发生的反馈|只是给自己已到过的位置补记记录',
       'stated_objective_progress quest_progress_review f game_recording'),
      '不承诺寻物种类官方图鉴、奖励、物品跨地图保留或所有作者允许自由拿物。'),
    Q(11, '真实在关卡换过的已有配置',
      '回想下载关卡确实允许换已有武器与突变的一段：当时手里有仍可保留的旧武器与另一组可用搭配，你真的用过这两组。哪种已做投入更贴近愿意保留的体验？',
      '比较两组搭配，再实际检验组合在这一关的效果|专门反复练出手或格挡时点，想让自己的操作更熟|按我给少年设定的惜旧战士身份，先保留当时旧武器继续尝试，暂不换新的一组|只是先比较当时已经可用的装备和突变，再决定那轮采用哪组',
      'b t r compare_available_setup',
      '当前地图真允许且玩家真试过才b；练习与角色选择分开，普通比较0。不能只看物品就声称检验组合。',
      'GR9L_13 GR9L_147 GR9L_STORE',
      ('没有换过配置，可回想真实玩过的一段跑跳平台：哪种已做投入更贴近愿意保留的体验？',
       '反复练起步、转向与落脚，专门把这一段操作练熟|亲手跑跳一轮，喜欢输入与位置变化相连的反馈|只是排清落脚、转向与动作衔接，再照本轮路线安排试|只是核对当时已经出现的移动说明，再继续尝试',
       't f platform_route_plan tool_reference_first'),
      '装备能被作者定制不等于玩家可进Design改数值，不要求NG+突变或普通生存的完整进度。'),
    Q(12, '真实同游时先看哪一条路',
      '回想确有其他真人与你一起玩已下载Playground的一段：当时有人想继续关卡已显示目标，有人想先看看已开放岔路。哪种真实做法更贴近愿意保留的投入？',
      '先谈清这一轮共同想完成什么，商量谁先看哪条已开路与何时会合|先陪同伴边走边聊天，喜欢一起待在这个场地的陪伴|走近能到但没看过的空间，想亲眼知道里面是什么|给自己当时已经走过的位置补记记录',
      'q o w game_recording',
      '真实游玩同伴与共同安排q/陪伴o分开；探索不自动来自作者目标，已有信息记录0。',
      'GR9L_13 GR9L_STORE',
      ('只有单人下载关卡经历，可回想真实在一份场地看过入口与当前目标的一段：当时目标进度与玩法说明都已显示，另有能到但没看过的空间。哪种已做投入更贴近愿意保留的体验？',
       '走近能到但没看过的空间，想亲眼知道里面是什么|只是核对已经显示的目标和当前进度，再决定这一段怎样继续|只是查看当前能到的入口与现场，再决定下一步|只是核对关卡已经给出的玩法说明，再继续尝试',
       'w quest_progress_review scene_inspection game_reference_first'),
      '不以NPC、刷出昆虫或作者留言补真人同游，不默认下载者能编辑或任意关卡可联机。'),
]

_GR_DOWNLOADED_THIRDS = [
    ('还没走进入口时的代码游玩说明',
     '熟悉关卡和初次走进入口都没体验过，可以答真实在原作Playground输入有效代码并下载到可打开关卡的一段：当前目录与操作说明能看。你先怎样继续？',
     '先核对已经出现的代码下载与游玩说明，再决定这一轮怎样打开|实际打开这份当前可用关卡，亲手体验一次进入操作|把自己想体验的关卡种类列成清单，选定这次想下载来补进的一类|给自己已下载的这份关卡补记名称、代码与当时实际可见的信息',
     'game_reference_first available_operation_trial c downloaded_content_recording',
     '真实原生代码输入、下载与打开操作；个人类别补全动机c和已给玩法说明、实际打开、真实下载元信息记录0分开。',
     'GR9L_13', '不保证有效代码永久可下载或网络无问题，不假造全关卡奖励；记录已下载内容的信息不等于已经进入或游玩过场地。'),
    ('没平台平路时的已有玩法说明',
     '跑跳与平路移动都没体验过，可以答真实打开一份下载关卡后查看玩法说明的一段：当前已有说明、目标与进度可看，也确实有能用的开始操作。你先怎样继续？',
     '先核对已给的玩法说明，再继续自己的实际尝试|先核对已显示的目标与当前进度，再决定这一轮做到哪一步|给自己已下载的这份关卡补记名称、代码与当时实际可见的信息|实际用一次当前开放的开始操作，亲手体验它怎样发生',
     'game_reference_first quest_progress_review downloaded_content_recording available_operation_trial',
     '第三真实较早玩家信息/开始操作，不默认能编辑或已跑跳。',
     'GR9L_13', '只问真实已显示的说明与目标，不为没有提示的关卡凭空添UI。'),
    ('没机关按钮时的最初走路',
     '逃脱机关和单按钮都没体验过，可以答真实在下载场地走过最初一段：前方有能到但没看过的空间。你先怎样投入？',
     '走进去亲眼看看那处空间是什么|亲手走这一小段，喜欢输入与位置变化相连的反馈|先查看当前能到的入口与现场，再决定这段怎样继续|先核对已有移动说明，再继续自己的实际尝试',
     'w f scene_inspection tool_reference_first',
     '第三真实基础移动，无解谜或工具连线前提。',
     'GR9L_13', '没有未知原因就不强计p；普通移动不自动探索。'),
    ('没投篮目标时的普通入口',
     '篮球和已显示目标都没经历过，可以答实际在一份下载关卡看过入口的一段：当前能走到，也有基本操作说明。你先怎样继续？',
     '去亲眼看看尚未看过的入口里面是什么|先查看当前能到的入口与现场，再决定这段怎样继续|先核对已有基础操作说明，再继续尝试|只给自己已经去过的位置补记记录',
     'w scene_inspection tool_reference_first game_recording',
     '第三真实开放场地经历，不要求作者一定布置任务UI。',
     'GR9L_13', '不造正式剧情与当前得分，也不保证入口后安全或能保存。'),
    ('没交手平台时的一次按钮反馈',
     '昆虫挑战与跑跳平台都没体验过，可以答实际在一份下载关卡按过一个当前可用按钮：已有反应能看到。你先怎样投入？',
     '亲手按一次，喜欢输入与眼前反应紧接着发生的反馈|只实际使用一次当前可用按钮，亲手体验操作发生|先查看当前能到的按钮与现场，再决定这一段怎样继续|先核对已有按钮操作说明，再继续尝试',
     'f available_operation_trial scene_inspection tool_reference_first',
     '第三真实可见互动，不让未战斗者虚构配装比较。',
     'GR9L_13', '不知道反应关系才可能检验原因，普通按一下不计p/t/i。'),
    ('没剧情目标时的下载场地',
     '原作剧情和已显示目标都没体验过，可以答实际在下载场地走过的一段：当前有能到但没看过的空间。你先怎样继续？',
     '走近没看过的空间，想亲眼知道里面是什么|亲手走这一小段，喜欢输入与位置变化相连的反馈|先核对已有基础操作说明，再继续尝试|只给自己已经去过的位置补记记录',
     'w f tool_reference_first game_recording',
     '第三真实无剧情地图体验，不编所有关卡都启用本体StoryQuests。',
     'GR9L_13 GR9L_147', '作者可以启用不代表实际已开，未见角色与未读后续不放进解释。'),
    ('没激光转角时的当前操作说明',
     '激光和转角路线都没体验过，可以答实际在下载关卡入口看过移动说明的一段：入口当前可到，所在位置已经看过，说明能回看，也能继续移动。你先怎样继续？',
     '先核对已经出现的移动说明，再继续自己的实际尝试|实际用一次当前开放的移动操作，亲手体验它怎样发生|只给自己已去过的位置补记记录|先查看当前能到的入口与现场，再决定怎样继续',
     'tool_reference_first available_operation_trial game_recording scene_inspection',
     '第三真实较早操作，无计时激光或故障前提。',
     'GR9L_13', '不让玩家改作者Timer；没有未知因果就不装作机制研究。'),
    ('没有真人成绩和个人记分时',
     '真人比分与个人成绩目标都没体验过，可以答实际在下载关卡走过的一段平路：当前可走，基本操作说明已出现。你先怎样投入？',
     '亲手走这一小段，喜欢输入与位置变化相连的反馈|反复练起步、转向与停步，专门让自己的这一段移动操作更熟|先核对已经出现的移动说明，再继续尝试|先查看当前能到的入口与现场，再决定这段怎样继续',
     'f t tool_reference_first scene_inspection',
     '第三真实无记分游玩，不借不存在的榜单强计k。',
     'GR9L_13', '普通个人尝试不算与真人比较，反复走须明确训练动机才t。'),
    ('真实没熟悉关卡和移动时',
     '熟悉关卡与实际走进入口都没经历过，可以回想真实通过代码下载并打开过一份Playground的一段：哪种已做投入更贴近愿意保留的体验？',
     '列过自己想体验齐的关卡种类，专门选定当时想下载来补进的一类|只是核对当时已经出现的代码与游玩说明，再继续尝试|只是实际打开当时这份可用关卡，亲手体验进入操作|给自己当时已下载的关卡补记名称、代码与实际可见信息',
     'c game_reference_first available_operation_trial downloaded_content_recording',
     '第三真实早期下载经历，不制造H或持续角色成长。',
     'GR9L_13', '没有精力和可选新内容的停留不计H，下载数量不是收藏动机。'),
    ('真实没寻物目标时的入口',
     '寻物与执行已显示目标都没体验过，可以回想实际在下载场地看过入口的一段：哪种已做投入更贴近愿意保留的体验？',
     '走进能到但没看过的地方，想亲眼知道里面是什么|亲手走过一段，喜欢输入与位置变化相连的反馈|只是查看当时能到的入口与现场，再决定怎样继续|只是为自己已经去过的位置补记记录',
     'w f scene_inspection game_recording',
     '第三真实较早场地体验，不编作者任务与收藏品。',
     'GR9L_13', '普通目标推进不计收藏；没有未知内容动机不因走路计w。'),
    ('真实没换装跑跳时的按钮',
     '换装与跑跳都没体验过，可以回想实际在下载关卡按过一个按钮的一段：当时按钮能用、眼前反应确实能看见，也有操作说明。哪种已做投入更贴近愿意保留的体验？',
     '亲手按一次，喜欢输入与眼前反应接连发生的反馈|只是实际使用一次当时可用按钮，亲手体验操作发生|只是核对当时已出现的按钮说明，再继续尝试|只是查看当时能到的按钮与现场，再决定怎样继续',
     'f available_operation_trial tool_reference_first scene_inspection',
     '第三真实普通互动，无装备或作者编辑权限前提。',
     'GR9L_13', '一次普通按键不计训练或发明，不把未知反应保证成固定奖励。'),
    ('真实没有同游和目标时',
     '真人同游与当前目标都没经历过，可以回想实际单人打开下载关卡后走过的一段：哪种已做投入更贴近愿意保留的体验？',
     '走近能到但没看过的空间，想亲眼知道里面是什么|亲手走过一段，喜欢输入与位置变化相连的反馈|只是查看当时能到的入口与现场，再决定下一步|只是核对当时已有的移动说明，再继续尝试',
     'w f scene_inspection tool_reference_first',
     '第三真实单人较早经历，不把作者留言或刷出昆虫当同游真人。',
     'GR9L_13', '三种只是当前草稿容量，未体验仍继续换已核实专属情境，不提供跳过；不保证所有进度可完成。'),
]
for _n, _row in enumerate(_GR_DOWNLOADED_THIRDS):
    GR_DOWNLOADED[_n]['variants'].append(_extra(*_row, reflection=_n >= 8))


PACKS = [_paths('val9l', '英灵神殿', 'steam-892970',


    '原生PC本体；资源生存与Hammer/No Build Cost分开。各风险、地图、传送、死亡修正仅按题面当前确实可用的条件；不要求后期群落、MOD或控制台。',


    [('survival', '资源生存：采集、制作与探索（地图等以当前可用为准）', VAL_SURVIVAL),


     ('hammer', 'Hammer / No Build Cost：已解锁构件免建造材料', VAL_HAMMER)],


    ['每路12主题，每题当前3个手写情境；第三候选只是容量起点，不是无限换题保证。共享4题不在此修改。',


     '未体验航船、冶炼、圈养、物品架或真人合作时有早期/单人替换，不把NPC当真人。',


     '无材料建造不等于所有物品免费、全配方开启、无支撑规则或任意飞行。',


     '作者稿仍待逐项完整copy核对、独立审阅与主代理验收，未注册未构建。']),


    _paths('raft9l', '木筏求生', 'steam-648800',


        '原生PC：可航行的资源生存与保持静止的Creative分开。风险预设只采用题面当前可用条件，不保证任何复活、物品保留或敌人行为。',


        [('survival', '资源生存：漂流、研究与航行', RAFT_SURVIVAL),


         ('creative', 'Creative：静止木筏的自由建造', RAFT_CREATIVE)],


        ['每路12主题，每题当前3个手写情境；尚待完整copy逐字复核。共享4题不在此修改。',


         'Creative没有海上航行、漂流来流、故事岛采集或交易站必答；只用当下菜单实际可取物件。',


         '未到研究台、贸易站、故事地点或潜水/真人合作时有早期或单人替换。',


         '只看地图/接收器信息、身体补给、配方要求、单轮制作流程都用具体0描述；NPC不是q。',


         '原作者稿仍待逐项完整copy核对、独立审阅和主代理验收；未注册未构建。']),


    _paths('gh9l', '绿色地狱', 'steam-815370',


        '原生PC本体815370：Story/无尽的日常生存、免费前传SoA、主菜单七项单人Challenges分别适配；不是GreenHellVR。所有操作按题面当前实际开放和可用条件，不以特定危险或营养设置为普遍前提。',


        [('survival', '本体Story / 无尽生存：日常制作、身体与营地', GH_SURVIVAL),


         ('soa', '亚马逊之魂：部落、传奇与前传仪式', GH_SOA),


         ('challenges', 'Challenges：七项原生单人计时挑战', GH_CHALLENGES)],


        ['每路12主题，每题3个手写情境；本体Story的Mia通话、前传天线和Radio挑战部件互不混用。',


         '无尽世界Flamekeeper与SoA三种仪式、主菜单七项挑战分别限定；Story不制作Ritual of Flame Herbs。',


         'SoA见并交谈村长后才查信任；传奇解法题明确已读齐对应线索；猎人检查不假装精确材料单，渔民有真实工具蓝图。',


         '七项Challenges按单人，没有虚构联机、排行榜、暂停计时或中途保存；个人用时目标不计对手竞争。',


         '未体验继续换真实专属情境；3个是当前草稿容量，不是所有玩法进度可答保证。',


         '仅为第一完整草稿，尚待全部题面/ABCD/完整copy逐字自审、独立审阅和root验收；未注册未构建。']),


    _paths('pz9l', '僵尸毁灭工程', 'steam-108600',


        '原生PC：当前Build42稳定版与legacy41实际经历分开；Custom和各风险预设仅按题面当前可用条件，不使用MOD、预发布或计划NPC功能。',


        [('build42', 'Build42：工作站、动物、季节耕作与当前稳定版经历', PZ_42),


         ('legacy41', 'Build41 / legacy41：旧版实际生存经历', PZ_41)],


        ['每路12主题，每题3个手写情境，保持12专属+4共享；候选容量仍需逐项审查，不保证所有进度都能答。',


         '42使用已发布的42.20功能和当前42.21稳定边界，排除42.22预发布；41不借42动物、季节耕作、交互捕鱼、武器头柄和新工作站。',


         '41本来已有3D摆物、衣物防护、人台、地图、VHS和原生联机，不错误排除。',


         '不编NPC幸存者、Kate/Baldspot故事、狗伙伴或Steam成就为已实装；真人q/o只用于原生实际同游。',


         '普通状态查看、已有配方核对、背包取放和一轮操作精确0，角色数值成长不等于玩家操作熟练。',


         '第一完整草稿，全部完整题面/轮转ABCD/copy自审与独立复核仍待完成；未注册未构建。'])]


PACKS += [
    _paths('sev9l', '七日杀', 'steam-251570',
      '原生PC当前3.4；资源生存、已启用CreativeMenu的自由取物建造、原生PrefabEditor单独作品设计分别适配。世界风险/制作/任务按真实当前规则，不用MOD或控制台。',
      [('survival', '资源生存：当前世界已启用的制作、任务与探索', SEV_SURVIVAL),
       ('creative', 'CreativeMenu：当前已启用权限的自由取物建造', SEV_CREATIVE),
       ('prefab', 'PrefabEditor：单独作品、工具与原生试玩', SEV_PREFAB)],
      ['每玩法12主题，每槽3手写情境；三种仅草稿容量起点，不等于无限或全进度适用。',
       'AlmostCreative预设不等于CreativeMenu权限；免制作不自动无敌、飞行、无支撑或血月关闭。',
       'Prefab另开试玩不当生存存档，避旧按键、路径、自动进入RWG和全操作可撤销保证。',
       '首稿未完成逐项完整copy自审与独立验收，不注册不构建。']),
    _paths('gr9l', '禁闭求生', 'steam-962130',
      '原作Grounded962130原生PC：资源/任务后院、免配方材料的两种Creative共同建造、PlaygroundsDesign和下载关卡Play四种实际经历分开，不借Grounded2。',
      [('survival', '生存后院：资源、任务与装备培养', GR_SURVIVAL),
       ('creative', 'Creative / CreativeWithBugs：免材料建造共同情境', GR_CREATIVE),
       ('playground_design', 'Playgrounds设计：场地、Link与PlayMode试玩', GR_DESIGN),
       ('playground_play', '已下载Playground：按作者当前允许规则游玩', GR_DOWNLOADED)],
      ['每玩法12主题，每槽3个手写情境，保持12专属+4共享与最多2补问。未体验继续换已核实专属情境，不提供跳过；三种只是容量起点。',
       '共同Creative不问活虫/任务/身体生存或从全开突变再成长，免材料仍需当前制作站与制作时间。',
       'HandyGnat是原生工具，不算真人；生存开助手需真实Custom条件，创意默认助手不借给普通生存。',
       'Playgrounds从PlayMode回Design恢复未玩状态，不借SharedWorld进度保存承诺；下载玩家不默认有编辑权。',
       '1.4.7可让Playground实际开放本体剧情，但题面逐项给已开且已见，不能说所有地图都默认开StoryQuests。',
       '尚待全部ABCD与完整copy自审、独立复核和主代理验收，未注册未构建。'])
]


AUTHORING_PROGRESS = {'completed_native_question_paths': ['valheim_survival', 'valheim_hammer', 'raft_survival', 'raft_creative', 'greenhell_survival', 'greenhell_soa', 'greenhell_challenges', 'pz_build42', 'pz_legacy41', 'sevendays_survival', 'sevendays_creative', 'sevendays_prefab', 'grounded_survival', 'grounded_creative', 'grounded_playground_design', 'grounded_downloaded_play'], 'complete_games': ['steam-892970', 'steam-648800', 'steam-815370', 'steam-108600', 'steam-251570', 'steam-962130'], 'register_or_build': False, 'pending_native_question_paths': {}, 'editorial_self_review_complete': False, 'qualification': 'All576 scenes explicitly authored first drafts only; root only24canonicalValALT2 reviewed earlier;Cpeerfirst324 inprogress;new252requirecompletefinalABCD/fullcopyselfreview andindependentpeer. Not accepted or published.'}

for entry in SOURCES:


    entry['checked_at'] = '2026-10-31'


