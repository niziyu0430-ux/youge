"""Compile reviewed authoring sources, retain every published pack snapshot."""
from copy import deepcopy
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from youge import v04
from question_variants_v05 import VARIANTS
from question_batches import additions
from question_authoring import validate as validate_authored

BEHAVIORS={
    'device_status_review': {'tag': '这次先核对装置状态', 'text': '在当前操作装置或设施的情境中，你愿意先查看已经显示的供能、分区、连接或结构状态，核对当前实际信息，再决定这一轮怎样调整。'},
    'quest_progress_review': {'tag': '这次先核对任务进度', 'text': '在当前任务情境中，你愿意先查看已经显示的目标、进度或当前提示，核对自己已经做到哪一步，再决定这一轮怎样继续。'},
    'material_stock_review': {'tag': '这次先核对现场物料', 'text': '在当前收集、搬运或建造的情境中，你愿意先查看眼前实际可见的物料与当前已知的存量，核对现有资源后再决定这一轮怎样处理。'},
    'navigation_information_review': {'tag': '这次先核对导航信息', 'text': '在当前可探索或移动的情境中，你愿意先查看已经可用的地图、定位器或信标，核对其中实际显示的位置、标记或路线信息，再决定这一段往哪里走。'},
    'survival_status_review': {'tag': '这次先核对生存现状', 'text': '在当前生存或探索情境中，你愿意先查看已经显示的身体状态、光照、氧气、工具电量或携带补给，核对当前实际受哪些条件影响，再决定这一轮怎样行动。'},
 'score_goal_attempt':{'tag': '这次先争取个人成绩目标', 'text': '在当前会记录得分、完成用时、资源用量或性能测试结果的情境中，你愿意按自己已经确定的个人成绩目标，实际尝试推进这一轮。'},
 'production_state_review':{'tag': '这次先核对生产现状', 'text': '在当前种植、养殖或制作情境中，你愿意先核对已经可见或已显示的地块、作物、动物、材料或产出状态，再决定这一轮怎样处理。'},
 'work_task_preparation_plan':{'tag':'这次亲手工作先排准备','text':'在当前亲手清理、维修或装配的情境中，你愿意按现有资金、工具或备件与已显示的任务条件，排清这一轮准备和动手处理的先后，再照安排实际推进。'},
 'objective_requirement_review':{'tag':'这次先核对已列目标要求','text':'在当前目标或交易情境中，你愿意先查看已经显示的材料要求、交付条件或奖励，核对现状后再决定这次是否执行。'},
 'environment_setting_options_review':{'tag':'这次先比较环境设置','text':'在当前环境编辑情境中，你愿意先查看已经开放的时刻、天气或光照设置方案，再决定这一轮是否切换。'},
 'work_task_process_recording':{'tag':'这段亲手工作愿意补记','text':'在当前亲手清理、维修或装配的情境中，你愿意为自己已经实际尝试或完成的工作步骤、部件处理与结果补上记录。'},
 'available_operation_trial':{'tag':'这次先试当前可用操作','text':'在当前游戏情境中，你愿意直接尝试一项已经可用且条件满足的具体操作，亲手体验这次操作怎样发生。'},
 'work_task_state_review':{'tag':'这次先核对工作当前状态','text':'在当前亲手清理、维修或装配的情境中，你愿意先查看已经显示的工作要求、部件状态或未完项目，核对现状后再决定这一轮怎样动手。'},
 'creative_preset_organize':{'tag':'这次先整理已有创作预设','text':'在当前创作情境中，你愿意使用已经可用的管理操作，实际调整已保存预设的名称或图标，或调整已有预设分类的名称，再继续自己的编辑。'},
 'unit_state_review':{'tag':'这次先核对可控单位状态','text':'在当前直接控制单位的情境中，你愿意先核对已经显示的单位位置、状态与周围可见情况，再决定这一段怎样下令。'},
 'unit_program_process_recording':{'tag':'这段单位程序愿意补记','text':'在当前可编程单位的情境中，你愿意为自己已经实际录制、修改或运行过的指令与单位执行过程补上记录。'},
 'unit_program_state_review':{'tag':'这次先查看单位程序状态','text':'在当前可编程单位的情境中，你愿意先查看已经显示的指令、搜索范围、手持物或目标状态，核对现状后再决定下一步怎样调整。'},
 'unit_program_workflow_plan':{'tag':'这次单位程序先排操作','text':'在当前可编程单位的情境中，你愿意先排清这一轮录制、修改或运行检查的操作先后，再照这个安排实际尝试。'},
 'unit_construction_plan':{'tag':'这次先安排单位建设','text':'在当前由可指派单位搬运和建设的情境中，你愿意按已有材料与可用单位，排清这一轮取料、交付和建设的先后，再照安排推进。'},
 'unit_movement_plan':{'tag':'这次单位移动先排步骤','text':'在当前直接控制单位的情境中，你愿意先按已有单位与可达地形，排清这一段集合、移动或交战的先后，再照这个安排实际下令。'},
 'known_resource_cache_retrieval':{'tag':'这次先取已发现的物料','text':'在当前游戏情境中，你愿意前往已经发现且当前可到达的资源存放处，实际取用其中现有可取的物料，再继续自己的安排。'},
 'surveillance_view_review':{'tag':'这次先查看已有监控画面','text':'在当前情境中，你愿意先查看已经接通可用的监控画面，核对其中已经显示的现场信息，再决定下一步行动。'},
 'item_handling_action':{'tag':'这次先处理手头物品','text':'在当前情境中，你愿意按已有物品和当前可用的存放、取出或丢弃操作，实际调整自己手头携带的东西，再继续行动。'},
 'physical_tool_action_sequence':{'tag':'这次实体工具先排动作','text':'在当前实体工具情境中，你愿意先按手边工具和材料，排清这一轮取放、操作、加工或收整的先后，再亲手照这个顺序尝试。'},
 'unit_command_sequence':{'tag':'这次单位下令先排顺序','text':'在当前可操控单位的情境中，你愿意先按已有单位与物料，排清这一轮采集、移动或交付的先后，再照这个顺序下令并实际尝试。'},
 'puzzle_program_edit_trial':{'tag':'这次愿意改动解谜程序','text':'在当前解谜情境中，你愿意实际改动已经可用的指令、连线或布局，再运行查看这次改动的结果。'},
 'puzzle_process_recording':{'tag':'这段解谜愿意补记','text':'在当前解谜情境中，你愿意为自己已经实际尝试的操作、程序或运行过程补上记录。'},
 'puzzle_state_review':{'tag':'这次先查看解谜当前状态','text':'在当前解谜情境中，你愿意先查看已经呈现的棋盘、输入输出要求或指令运行状态，核对现状，再决定这一轮怎样继续。'},
 'puzzle_action_plan':{'tag':'这次解谜先排可做步骤','text':'在当前解谜情境中，你愿意先按眼前可用的操作安排这一轮的步骤或取用顺序，再照这个安排实际尝试。'},
 'management_process_recording':{'tag':'这段经营愿意补记','text':'在当前经营情境中，你愿意为自己已经实际经历的收支、协议执行或部门安排补上记录。'},
 'simulation_process_observation':{'tag':'这次先看模拟运转','text':'在当前模拟经营情境中，你愿意先跟看居民出行、车辆运输或建设生产的实际运行，观察过程与变化，再决定下一步怎样调整。'},
 'simulation_process_recording':{'tag':'这段运转愿意补记','text':'在当前模拟经营情境中，你愿意为自己已经观察或安排过的居民活动、资源供给与运输过程补上记录。'},
 'stated_objective_progress':{'tag':'这次先推进已列出的目标','text':'在当前游戏情境中，你愿意按已经出现的任务或建设目标核对条件，实际推进这次目标，并把它的完成作为当前投入重点。'},
 'compare_management_options':{'tag':'这次先比较可用经营方案','text':'在当前经营情境中，你愿意先比较已经开放、当前可选的建设、供给或贸易方案，再决定下一步怎样安排。'},
 'creative_option_review':{'tag':'这次先看可用创作方案','text':'在当前创作情境中，你愿意先查看已经可选的素材、布景或外观方案，再决定这次采用哪一种。'},
 'creative_workflow_plan':{'tag':'这次创作先排编辑步骤','text':'在当前创作情境中，你愿意先排清这一轮布局、放置、移动或调整的编辑步骤，再照这个顺序动手完成。'},
 'management_status_review':{'tag':'这次先查看经营状态','text':'在当前经营情境中，你愿意先查看已经出现的访客、员工反馈或运行面板，核对当前状态，再决定这次怎样调整。'},
 'construction_process_recording':{'tag':'这段建设愿意补记','text':'在当前建设情境中，你愿意为已经搭建的建筑、已铺设的连接或已经实际投入的研究，补记自己的建设过程。'},
 'mission_briefing_review':{'tag':'这次出发先核对目标要求','text':'在当前出发准备情境中，你愿意先阅读已经出现的任务或地点说明，核对目标、交付条件和可选去向，再决定这次是否前往。'},
 'compare_production_options':{'tag':'这次先比较可做的生产选项','text':'在当前生产、种植或制作情境中，你愿意先比较已经开放且当前可做的配方、作物或材料条件，再决定这次采用哪一种。'},
 'construction_action_plan':{'tag':'这次建设先排步骤','text':'在当前建设情境中，你愿意先按已有材料和可用人员，排清搬运、施工或家具调整的先后，再照这次安排推进。'},
 'household_action_plan':{'tag':'这次家庭活动先排顺序','text':'在当前虚拟家庭情境中，你愿意先按已有时间、资金或空间，排清当前可做活动的先后，再照这次安排继续。'},
 'creative_save_local':{'tag':'这次先保存创作结果','text':'在当前创作情境中，你愿意先把已经具备保存条件的作品存入本机可用的资料库或预设，保留这次编辑结果。'},
 'creative_edit_trial':{'tag':'这次愿意动手试编辑','text':'在当前建造或人物编辑情境中，你愿意实际改动一项可用的尺寸、位置、造型或颜色设置，亲手查看结果。'},
 'game_reference_first':{'tag':'这次先核对玩法说明','text':'在当前游戏情境中，你愿意先核对已有的玩法说明或示范，再继续自己的实际尝试。'},
 'purchase_available_upgrade':{'tag':'这次先购入可用升级','text':'在当前情境中，你愿意先花已有资源购入一项已经开放且可支付的升级或动作。'},
 'tool_operation_plan':{'tag':'这次工具操作先排流程','text':'在当前工具操作情境中，你愿意先排清路线、动作和资源消耗或恢复的先后，再照这个安排继续。'},
 'optional_objective':{'tag':'这次愿意完成可选目标','text':'在当前任务里，你愿意主动处理已经明确的可选目标，并把这次目标的完成作为投入重点。'},
 'compare_available_setup':{'tag':'这次先比较可用配置','text':'在当前情境中，你愿意先比较已经拥有或当前可选的装备、技能、组件与升级方案，再决定下一步怎样安排。'},
 'tool_reference_first':{'tag':'这次先核对工具说明','text':'在当前工具操作情境中，你愿意先核对已有的操作说明或示范，再亲手继续自己的修改或试用。'},
 'scene_inspection':{'tag':'这段先查看可达现场','text':'在当前情境里，你愿意先查看已经可达的入口、装置、装备或停靠处，再继续眼前这段经历。'},
 'combat_resource_cycle':{'tag':'这次交手先理资源循环','text':'在当前交手情境中，你愿意先理清攻击、能量消耗与恢复的先后，再照这个资源循环继续尝试。'},
 'mission_preparation_plan':{'tag':'这次任务准备先排步骤','text':'在当前任务准备中，你愿意先排清已有资源、可做步骤和目的地的先后，再照这个安排继续。'},
 'platform_route_plan':{'tag':'这次平台路段先排落脚','text':'在当前平台情境中，你愿意先排清落脚、转向与动作衔接，再照这个安排亲手尝试。'},
 'try_available_setup':{'tag':'这次愿意试用已有配置','text':'在当前情境中，你愿意换用自己已经拥有或当前可用的一项配置，亲手体验它怎样发挥。'},
 'try_action_variant':{'tag':'这段操作想换个做法','text':'在当前情境里，你愿意换一次已经会用的动作次序或出手时点，亲手体验它怎样发生。'},
 'route_variant':{'tag':'这段经历想换条可走的路','text':'在当前情境里，你愿意从另一条已经可达的路线或另一侧经过，亲手体验不同的行进方向。'},
 'rhythm_workflow_plan':{'tag':'这次节奏内容先排尝试流程','text':'在当前节奏游戏的练习或关卡制作中，你愿意先排清分段尝试、测试与调整的步骤，再照这个流程继续。'},
 'route_choice':{'tag':'这次交火想换个进入方向','text':'在当前枪械情境中，你愿意从另一条可达路线或另一侧接近，试一次较少使用的进入方向。'},
 'practice_route_plan':{'tag':'这次枪法练习先排步骤','text':'在当前枪械练习里，你愿意先排清路段、观察点与动作的先后，再照这个安排亲手尝试。'},
 'crafting_action_sequence':{'tag': '这次制作先排操作顺序', 'text': '在当前使用制作界面的情境中，你愿意先按已有材料、当前可用设备与配方，排清这一轮确认用料、执行制作和整理产物的操作先后，再亲自照这个顺序尝试。'},
 'animal_care_process_recording':{'tag': '这段动物照料愿意补记', 'text': '在当前照料或培养游戏内动物的情境中，你愿意为自己已经实际做过的喂养、相处或训练操作，以及已经观察到的动物反应补上记录。'},
 'game_recording':{'tag':'这段经历愿意补记','text':'在当前情境里，你愿意为已经取得的物品或已经体验的地点、人物信息补上自己的记录。'},
 'rhythm_reference_first':{'tag':'这段演奏先核对操作提示','text':'在当前节奏情境里，你愿意先核对一小段操作说明或示范，再继续自己的尝试。'},
 'async_connection':{'tag':'这次配送感到了异步连接','text':'这次配送里，其他玩家留下的设施让独自行走多了一层与他人连接的感受。'},
 'guide_hint':{'tag':'当前卡点先要提示','text':'在这次卡点情境中，可以先给一小段提示，再为自己继续尝试留出空间。'},
 'guide_full_solution':{'tag':'当前卡点愿看完整做法','text':'在这次卡点情境中，你也愿意先看完整做法，把时间留给之后想体验的内容。'},
 'guide_completion':{'tag':'当前路线先查遗漏','text':'在这次路线情境中，你愿意先确认去向和遗漏内容，让想经历的部分能接着完成。'},
 'pace_flexible':{'tag':'当前线索可以稍后接上','text':'在这次线索情境中，可以先留着未完成的事，等新的发现出现时再把它接起来。'},
 'runes_retrieve_first':{'tag':'受挫后先回去处理','text':'这次受挫之后，你更愿意先返回当前一段，把眼前惦记的事处理完。'},
 'runes_prepare_return':{'tag':'受挫后先调整再试','text':'这次受挫之后，可以先为装备、路线或行动做一轮调整，再接着尝试。'},
 'runes_return_later':{'tag':'受挫后可以换个目标','text':'这次受挫之后，你愿意先体验另一件事，为之后是否返回保留空间。'},
 'runes_pause':{'tag':'当前难点可以下次继续','text':'这次受挫之后，你接受先停下来，下次再决定从哪里接着走。'},
 'accept_story_outcome':{'tag':'当前结果进入这次故事','text':'在这次结果分歧里，你愿意先看事情继续发展，让已经发生的结果成为当前旅程的一部分。'},
 'reload_preferred_branch':{'tag':'当前分支愿意再尝试','text':'在允许重新尝试的情境中，你也愿意再试原先惦记的分支，保留自己想体验的那条路。'},
 'inspect_check_rules':{'tag':'当前结果先看规则','text':'在这次结果分歧里，你愿意先弄清规则怎样结算，再决定接下来的行动。'},
 'seek_other_route':{'tag':'当前目标另找路径','text':'在这次结果分歧里，你愿意从仍能进行的行动中找另一条路，接着推进原本的目标。'},
 'festival_contest_goal':{'tag':'这次节庆想争取名次','text':'在这次节庆情境中，准备展品并争取一个满意名次，是你明确表达的目标。'}
,
 'downloaded_content_recording':{'tag': '这份下载内容愿意补记', 'text': '在当前下载或选择关卡的情境中，你愿意为自己已经下载的内容补记名称、代码或当时可见的实际信息，再继续自己的尝试。'},
 'scene_edit_process_recording':{'tag': '这段场景编辑愿意补记', 'text': '在当前场景编辑情境中，你愿意为自己已经实际做过的物件放置、移动、旋转、擦除、撤销或重做操作，以及当时已经看到的编辑结果补上记录。'},
 'text_color_edit_process_recording':{'tag': '这段文字与配色编辑愿意补记', 'text': '在当前文字、图案或配色编辑的情境中，你愿意为自己已经实际尝试的改字、涂画或颜色调整步骤，以及当时已经看到的呈现结果补上记录。'},
 'self_selected_goal_progress':{'tag': '这次先推进自选目标', 'text': '在当前有几项具体可做目标的游戏情境中，你愿意先选定其中一项，把这一轮可用的时间、材料或行进安排实际投入它的推进。'},
 'construction_contribution_recording':{'tag': '这段补料施工愿意补记', 'text': '在当前按蓝图施工的情境中，你愿意为自己已经实际投入的材料、已经做过的补料步骤，以及当时已经看到的施工进度补上记录。'},
 'known_gathering_site_action':{'tag': '这次先采已知地点的材料', 'text': '在当前能采集材料的游戏情境中，你愿意前往自己已经发现且当前可到达的采集地点，实际采集那里当前确有且可取用的材料，再继续自己的安排。'},
 'crafting_option_review':{'tag': '这次先比较可做物件', 'text': '在当前制作或搭建的情境中，你愿意先比较已有材料与当前已开放配方能够制作或搭成的物件方案，再决定这轮先投入哪一项。'},
}
SCENES={'gi': ['当前蒙德旅途路线', '当前元素与已有材料', '当前已有角色的使用', '当前材料路线与培养', '当前蒙德普通交火', '当前蒙德人物与取景', '当前蒙德街景停留', '当前近郊熟路', '真实单人蒙德旅程', '真实早期机关经历', '真实近郊熟悉停留', '已经走过的蒙德'], 'lol': ['当前基础英雄交火', '当前已有英雄的练习', '当前单人梳理交火', '当前无真人的准备', '当前单人练习目标', '当前兵线处理', '实际购买机会中的选择', '当前默认形象取景', '真实单人对局经历', '真实基础交火记忆', '真实重用英雄经历', '已经完成的基础投入'], 'cs2': ['当前持枪交火', '当前地图通道角度', '当前持枪后的出发准备', '当前枪械与遮挡', '当前基础交火练习', '当前刚结束交火的核对', '当前可用枪械的操作', '当前枪械与可达支路', '真实默认外观与地图经历', '真实单人枪械经历', '真实未达预期的交火', '已经完成的枪械投入'], 'sv': ['当前照料后的自由时间', '当前已有农场空间', '当前换季安排', '当前普通镇民问候', '当前基础工具的一天', '当前矿井外取材', '当前早期农场生活', '当前季节的家园行动', '真实基础农场整理', '真实单人农场日', '真实本季收获经历', '已经过过的农场日常'], 'er': ['当前宁姆格福路线', '当前普通敌人交手', '当前已有兵器与盾', '当前早期废墟岔路', '当前早期受挫后的安排', '当前早期出发准备', '当前铁砧与已有武器', '当前已交谈人物', '真实早期去向经历', '真实单人宁姆格福旅程', '真实早期装备经历', '已经走过的宁姆格福'], 'bg3': ['当前已有角色的行动', '当前检定之后的行动', '当前已有能力的准备', '当前早期人物来往', '当前早期战斗准备', '当前早期人物与取景', '当前回合的已有能力', '当前早期对话之后', '真实早期安全停留', '真实单人第一章探索', '真实第一章旅程经历', '已经玩过的第一章投入']}
CORE_SOURCES={'gi': ['GI_CORE', 'GI_GROWTH', 'GI_START_V5', 'GI_LOG_V5'], 'lol': ['LOL_CORE', 'LOL_MODES', 'LOL_ARAM_DEV_V5', 'LOL_ARAM_RULES_V5', 'LOL_CUSTOM_V5'], 'cs2': ['CS2_CORE', 'CS2_RULES', 'CS2_ARMS_V5', 'CS2_ARMS_MIRROR_V5', 'CS2_DM_V5'], 'sv': ['SV_CORE', 'SV_SKILLS_V5', 'SV_FRIEND_V5'], 'er': ['ER_START', 'ER_WORLD', 'ER_STORY', 'ER_COOP'], 'bg3': ['BG3_CORE', 'BG3_BUILD', 'BG3_CHOICES', 'BG3_REST', 'BG3_CHECK']}


def write_export(bank):
    sources={s['id']:s for s in bank['sources']}
    count=sum(len(s['variants']) for p in bank['packs'] for s in p['slots'])
    games=sum(len(p['game_ids']) for p in bank['packs'])
    lines=['# 游格已重写游戏题库','',
           f'更新日期：2026-10-30。当前接入{games}条游戏记录、{len(bank["packs"])}套作品题包，共{len(bank["packs"])*12}个基础专属题位，连同模式与换题情境共{count}个。每次回答12道适用专属题和4道跨游戏题，必要时最多2道补问。','',
           '以下为当前运行内容。替代情境只在对应题位展示一个，未体验不计分；可撤销换题。不同模式之间按实际玩法适配，不能把未体验默认为不喜欢。全库其余作品仍待逐款重写。','',
           '计分与报告属于原创探索版，尚未完成真人测量验证。旧答卷按旧题库读取；题包修订后保留原内容快照。','']
    for pack in bank['packs']:
        lines.extend(['## '+pack['title'],'',
                      '可选体验范围：'+'、'.join(m['label'] for m in pack['modes'])+'。',''])
        if pack.get('editorial_notes'):
            lines.extend(['编写说明：'+'；'.join(pack['editorial_notes']),''])
        mode_names={m['id']:m['label'] for m in pack['modes']}
        for slot in pack['slots']:
            lines.extend([f'### 第{slot["number"]}题',''])
            for index,q in enumerate(slot['variants']):
                context='、'.join(mode_names[m] for m in q.get('modes',[])) or '适用的基础体验'
                lines.extend([f'**{q["scene"]} · {context}**','',q['text'],''])
                lines.extend(f'- {o["id"]}. {o["label"]}' for o in q['options'])
                lines.extend(['','设计目的：'+q['design_purpose'],'',
                              '解释边界：'+q['interpretation_boundary'],'',
                              '机制资料：'+'、'.join(f'[{sources[k]["title"]}]({sources[k]["url"]})' for k in q['source_ids'])+'。',''])
    lines.extend(['## 四道跨游戏题',''])
    for q in bank['shared_questions']:
        lines.extend(['### '+q['text'],''])
        lines.extend(f'- {o["id"]}. {o["label"]}' for o in q['options']);lines.append('')
    (ROOT/'exports/游格-已重写游戏题库.md').write_text('\n'.join(lines),encoding='utf-8')


def snapshot(pack,history):
    pack=deepcopy(pack)
    digest=hashlib.sha256(json.dumps(pack,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:12]
    pack['version']='0.5.0+'+digest
    relative=f'config/question-packs-history/{pack["id"]}-{digest}.json'
    path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True)
    serialized=json.dumps(pack,ensure_ascii=False,indent=2)+'\n'
    if path.exists():assert path.read_text(encoding='utf-8')==serialized
    else:path.write_text(serialized,encoding='utf-8')
    entry={'game_ids':pack['game_ids'],'version':pack['version'],'path':relative}
    if entry not in history:history.append(entry)
    return pack


def initial_packs(draft,people):
    """Compile the six original authoring records without publishing a snapshot."""
    packs=[]
    for original in draft['packs']:
        identifier=original['id'];slots=[]
        for item in original['questions']:
            number=item['number'];slot_id=item['id'];variants=[]
            base={'id':slot_id+'.V1','text':item['text'],'scene':item['scene'],
                  'question_type':item['question_type'],'source_ids':item['source_ids'],
                  'options':[{'id':o['id'],'label':o['label'],'signal':o['proposed_signal']} for o in item['options']],
                  'modes':['rift'] if identifier=='lol' else ['defusal'] if identifier=='cs2' else [],
                  'design_purpose':item['design_purpose'],'interpretation_boundary':item['interpretation_boundary']}
            variants.append(base)
            for n,alt in enumerate(item['alternatives'],1):
                variants.append({'id':slot_id+f'.DRAFTALT{n}','text':alt['text'],'scene':'较早的基础情境',
                    'question_type':item['question_type'],'source_ids':alt['source_ids'],'modes':[],
                    'options':[{'id':o['id'],'label':o['label'],'signal':o['proposed_signal']} for o in alt['options']],
                    'design_purpose':alt['design_purpose'],'interpretation_boundary':'按当前情境解释；不假定与原题统计等值。'})
            for alt in VARIANTS[identifier][number]:
                core_sources=CORE_SOURCES[identifier]
                variants.append({'id':slot_id+'.'+alt['key'],'text':alt['text'],
                    'scene':('大乱斗中的'+item['scene']) if alt['key']=='ARAM' else SCENES[identifier][number-1],
                    'question_type':item['question_type'],'source_ids':core_sources,
                    'modes':alt['modes'],'options':[{'id':chr(65+i),'label':label,'signal':signal} for i,(label,signal) in enumerate(zip(alt['labels'],alt['signals']))],
                    'design_purpose':alt['note'],'interpretation_boundary':'只依据这次实际选择；不由未体验或替换次数推断动机。'})
            for q in variants:
                assert 2<=len(q['options'])<=4 and len({o['label'] for o in q['options']})==len(q['options'])
                assert all(o['signal'] in people or o['signal'] in BEHAVIORS for o in q['options'])
            slots.append({'id':slot_id,'number':number,'variants':variants})
        modes=[{'id':'default','label':'按自己熟悉的体验回答','initial_variants':{}}]
        if identifier=='lol':
            modes=[{'id':'rift','label':'召唤师峡谷','initial_variants':{}},
                   {'id':'aram','label':'普通极地大乱斗','initial_variants':{s['id']:s['id']+'.ARAM' for s in slots}}]
        if identifier=='cs2':
            modes=[{'id':'defusal','label':'拆弹玩法','initial_variants':{}},
                   {'id':'gunplay','label':'死斗／军备竞赛','initial_variants':{s['id']:s['id']+'.CORE' for s in slots}}]
        pack={'id':identifier,'title':original['title'],'game_ids':original['game_ids'],
              'author_review':'source_checked_and_editorially_revised','player_trial':'not_performed',
              'status':'released_exploratory','modes':modes,'slots':slots}
        packs.append(pack)
    return packs


def main():
    draft=json.loads((ROOT/'config/question-packs.v0.5.draft.json').read_text(encoding='utf-8'))
    extra_packs,extra_sources=additions()
    sources=json.loads((ROOT/'research/question-design-v0.5/sources.json').read_text(encoding='utf-8'))['sources']+deepcopy(extra_sources)
    people={p['id'] for p in v04.config()['personas']}
    packfile=ROOT/'config/question-packs.v0.5.0.json'
    previous=json.loads(packfile.read_text(encoding='utf-8')) if packfile.exists() else {}
    history=deepcopy(previous.get('pack_history',[]))
    packs=[]
    compiled_initial=initial_packs(draft,people)
    validate_authored(compiled_initial+deepcopy(extra_packs),sources,people|set(BEHAVIORS))
    packs=[snapshot(p,history) for p in compiled_initial]
    packs.extend(snapshot(pack,history) for pack in extra_packs)
    shared=deepcopy(draft['shared_questions'])
    for q in shared:
        for o in q['options']:
            o['signal']=next(iter(o['weights']))
            for key in ('weights','habit','report'):o.pop(key,None)
    result={'version':'0.5.0','checked_at':datetime.now(timezone(timedelta(hours=8))).date().isoformat(),
            'scoring_policy':{'anchor_points_per_signal':2,'max_anchor_contexts_per_persona':2,
                              'shared_points_per_signal':2,'tie_bonus':4,'max_extra':2,
                              'qualification':'exploratory_product_rule_not_psychometric_equating'},
            'behavior_copy':BEHAVIORS,'shared_questions':shared,'sources':sources,'packs':packs,'pack_history':history}
    temp=packfile.with_suffix('.tmp');temp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');temp.replace(packfile)
    write_export(result)
    print(json.dumps({'packs':len(packs),'game_records':sum(len(p['game_ids']) for p in packs),'base_questions':len(packs)*12,
                      'authored_scenes':sum(len(s['variants']) for p in packs for s in p['slots']),
                      'shared_questions':len(shared)},ensure_ascii=False))


if __name__=='__main__':main()
