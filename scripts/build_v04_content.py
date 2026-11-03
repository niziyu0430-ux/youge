"""Author the reviewed four-choice instrument. All content is frozen into JSON."""
from copy import deepcopy
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=['wanderer','story_keeper','role_player','puzzle_breaker','practice_seeker','rank_worker','feedback_engine','build_alchemist','systems_builder','growth_keeper','collector','style_director','play_inventor','social_spark','quest_board','cozy_resident']


def o(label,*ids,habit=None,copy=None):
    return {'label':label,'weights':{i:2 if n==0 else 1 for n,i in enumerate(ids)},'habit':habit,'report':copy or label}


def q(id,text,options,scope='anchor',topic=None):
    return {'id':id,'text':text,'scope':scope,'topic':topic or id,'response_type':'single','options':[{'id':chr(65+i),**v} for i,v in enumerate(options)]}


PACKS={
'civ6':[
q('G01','一份《{game}》存档玩到中期，哪件事最容易让你继续按“下一回合”？',[o('把城市的区域和产出安排顺，让规划逐步成形','systems_builder'),o('沿着科技或市政路线，解锁一直想要的东西','growth_keeper'),o('调整兵种和作战安排，尝试攻下目标城市','build_alchemist','practice_seeker'),o('继续探开地图，寻找没见过的城邦和自然奇观','wanderer')]),
q('G02','《{game}》里一座新城市刚建起来，你最想接着安排哪件事？',[o('根据地形安排区域和改良设施','systems_builder'),o('把它接进已有的商业和资源网络','build_alchemist'),o('按想象中的帝国版图，慢慢把城市发展起来','role_player'),o('沿着附近地形继续探索，看看还有哪些落城点','wanderer')]),
q('G03','开一份新的《{game}》存档时，你最想尝试什么变化？',[o('换一个不熟悉的文明，试它的特殊玩法','play_inventor'),o('用熟悉的文明，挑战上次没做到的目标','practice_seeker'),o('把自己喜欢的文明一路发展得更完整','growth_keeper'),o('和朋友约好规则、分工和推进时间','quest_board','social_spark')]),
q('G04','《{game}》里，哪种发展过程最合你的心意？',[o('区域、产出和政策配合起来，逐渐形成运转顺畅的体系','systems_builder'),o('地图不断展开，总能发现新地形和新邻居','wanderer'),o('按自己的主题建设国家，让城市和帝国有自己的样子','style_director','role_player'),o('用熟悉的设置慢慢发展，节奏由自己掌握','cozy_resident')])],
'rdr2':[
q('G01','在《{game}》里，主线暂时不急着推进时，你最想做什么？',[o('骑去没到过的地方，看看路上会遇见什么','wanderer'),o('回营地听同伴聊天，留意他们最近的故事','story_keeper'),o('找特定猎物或藏品，把想收的东西补齐','collector'),o('走熟悉的路，骑马、钓鱼、看风景','cozy_resident')]),
q('G02','《{game}》里，一次路边偶遇打乱了原来的路线，你最在意什么？',[o('想看看这件事会怎样发展，原来的任务可以晚点再做','story_keeper'),o('这里可能还有没发现的事情，想在附近多看看','wanderer'),o('按自己心里亚瑟的行事方式作出选择','role_player'),o('记下位置，先完成这次已经安排好的事情','systems_builder')]),
q('G03','如果再打开一个《{game}》的旧存档，你最想回到哪种体验？',[o('重新经历一段记得很清楚的人物故事','story_keeper'),o('继续补齐猎物、藏品或挑战记录','collector'),o('重新搭配亚瑟的衣着和马具，留下自己的照片','style_director'),o('在熟悉的地方走走，不急着推动故事','cozy_resident')]),
q('G04','《{game}》里，哪种游玩记录最值得你留下？',[o('偶然遇见的人、景或一段没有预料到的经历','wanderer'),o('一句角色对白，或营地里让人记住的片段','story_keeper'),o('自己按角色设定作出的选择','role_player'),o('终于完成的一项收集或挑战','collector','practice_seeker')])],
'ds1':[
q('G01','《{game}》里，一份订单已经送达，接下来最吸引你的是什么？',[o('接着推进关键委托，看看山姆和其他人的故事','story_keeper'),o('回去补路、搭设施，把常用运输线整理起来','systems_builder'),o('换一条没走过的路线，看看不同的地形和风景','wanderer'),o('看看其他玩家留下的设施，给有用的点赞或补点材料','social_spark')]),
q('G02','《{game}》里，要去一个自己还不熟悉的配送地点，你最想先做什么？',[o('在地图上规划路线，准备对应的工具','build_alchemist'),o('先走一段，亲自看看地形再决定','wanderer'),o('先整理携带的货物，让装载和运送安排顺起来','systems_builder'),o('看看其他玩家留下的路线提示和设施','social_spark')]),
q('G03','《{game}》里，什么最容易让你自愿多送一份订单？',[o('想把和某个地点的连接继续提升','growth_keeper'),o('想试试另一种运输或装载安排','build_alchemist'),o('这条路已经熟悉，走完它本身就很舒服','cozy_resident'),o('想接着体验订单背后的人物和故事','story_keeper')]),
q('G04','《{game}》里，你更愿意长期投入哪件事？',[o('把多条常用配送路线连成顺手的运输网络','systems_builder'),o('找不同的穿越路线，看看世界还有什么样子','wanderer'),o('和同好分享设施位置，互相改善配送体验','social_spark','quest_board'),o('给自己安排不同工具或限制条件，试新的送货方式','play_inventor')])],
'dc':[
q('G01','《{game}》这次挑战结束后，哪件事最容易让你想再来一次？',[o('刚才有个招式没处理好，想再练练','practice_seeker'),o('一套武器和技能的配合还没试够','build_alchemist'),o('刚解锁一件新装备，想试试它的手感','feedback_engine'),o('还有一条分岔路线没走，想看看通向哪里','wanderer')]),
q('G02','《{game}》里拿到一件和平时打法不同的装备，你最想怎么处理？',[o('亲手试它的攻击节奏和操作手感','feedback_engine'),o('看看词条能否和现有装备形成配合','build_alchemist'),o('围绕它改变打法，试一套平时不用的组合','play_inventor'),o('先用熟悉的装备，把这次想练的内容打完','practice_seeker')]),
q('G03','《{game}》里，你更愿意为哪件事反复尝试？',[o('把一个Boss的招式处理得更熟','practice_seeker'),o('把一套装备和技能组合真正打通','build_alchemist'),o('补齐自己还想要的蓝图或解锁内容','collector'),o('试一套自己定的有趣限制或非惯用打法','play_inventor')]),
q('G04','回想《{game}》的体验，你最舍不得少掉哪种乐趣？',[o('动作、音效和反馈连在一起的畅快','feedback_engine'),o('对敌人越来越熟，自己逐渐能处理以前的难点','practice_seeker'),o('地图岔路和新区域带来的发现','wanderer'),o('每次得到不同装备，再重新组合打法','build_alchemist','play_inventor')])],
'sts':[
q('G01','《{game}》第一幕，牌组还没成形。奖励里有一张你很少用的牌，你通常先怎么考虑？',[o('看看它能和现有卡牌、遗物产生什么配合','build_alchemist'),o('这次就围绕它尝试一套不熟悉的打法','play_inventor'),o('先跳过，继续找自己常用的核心牌','cozy_resident'),o('找一份讲解，了解这张牌的用法再决定',habit='reference_first')]),
q('G02','《{game}》里，哪种战斗最容易让你玩得满足？',[o('卡牌与遗物形成连锁，牌组终于转起来','build_alchemist'),o('调整出牌顺序，打过了以前卡住的敌人','practice_seeker'),o('拿不熟悉的牌，打出没想到过的新用法','play_inventor'),o('熟悉的角色和打法，让自己按喜欢的节奏慢慢推进','cozy_resident')]),
q('G03','《{game}》一次爬塔结束后，你最想接着做什么？',[o('复盘几张牌和遗物的取舍，下次调整构筑','build_alchemist'),o('继续挑战自己还没通过的进阶或目标','practice_seeker'),o('换个角色，试一条不同的构筑路线','play_inventor'),o('补一项还没有完成的解锁或成就','collector')]),
q('G04','在《{game}》里，你更愿意把思考时间花在哪件事？',[o('比较几条路线和资源安排，让牌组有机会成形','systems_builder'),o('弄清某张牌或遗物为什么会这样结算','puzzle_breaker'),o('打磨一套自己熟悉的组合，看看能做到哪一步','practice_seeker'),o('找不常见的配合，哪怕这次走向和预想不同','play_inventor')])],
'bannerlord':[
q('G01','玩《{game}》时，哪部分最容易让你主动投入时间？',[o('亲自冲进战场，练骑战、射击或近战操作','practice_seeker','feedback_engine'),o('挑兵种、调位置，在战场上下指令','build_alchemist'),o('往返城镇跑商，安排队伍的日常开销','systems_builder'),o('带队四处走，接任务、结交不同领主','role_player','wanderer')]),
q('G02','《{game}》里，有了一支能参与战斗的队伍后，你最想继续做什么？',[o('培养自己喜欢的兵种和同伴，慢慢看他们成长','growth_keeper'),o('比较不同兵种和阵形在战场上的配合','build_alchemist'),o('经营收入与补给，让队伍能够持续行动','systems_builder'),o('按自己设想的领主身份，选择效忠、结盟或独立的道路','role_player')]),
q('G03','《{game}》里的一场战斗结束后，什么最值得你回味？',[o('自己亲手打出的一段骑战或近战操作','feedback_engine'),o('兵种、位置和指令配合出了想要的战果','build_alchemist'),o('队伍逐渐从最初的规模成长起来','growth_keeper'),o('这一场经历推进了自己这位领主的故事','role_player')]),
q('G04','再开一份《{game}》存档时，你最想换什么？',[o('换一种角色身份和阵营路线，经历另一种人生','role_player'),o('给自己定一种兵种、武器或规则限制','play_inventor'),o('保留喜欢的路线，把经营和队伍发展安排得更顺','systems_builder'),o('换个战斗目标，练以前没有掌握的作战方式','practice_seeker')])],
'kcd2':[
q('G01','在《{game}》里，你最愿意为了哪件事放慢主线进度？',[o('找人练剑，把战斗操作练得更顺手','practice_seeker'),o('练锻造，亲手做出自己想用的装备','growth_keeper'),o('追一条支线，了解相关人物的遭遇和后续','story_keeper'),o('按自己设想的亨利生活，搭配衣着和行事方式','role_player')]),
q('G02','《{game}》里，一个任务允许不同的解决方法时，你最想先体验哪条路？',[o('沿着人物对话和线索，弄清事情再行动','story_keeper','puzzle_breaker'),o('试试潜行、时机和物品能否形成另一种解法','play_inventor'),o('用自己正在练的战斗方式，亲自处理难点','practice_seeker'),o('选符合自己这次亨利人设的做法','role_player')]),
q('G03','《{game}》里暂时没有紧迫任务，你最想把这段游玩时间留给什么？',[o('去还不熟悉的地方，看看城镇和野外有什么','wanderer'),o('把锻造或炼金的过程练熟，看技能慢慢成长','growth_keeper'),o('为亨利搭配一套自己喜欢的衣着和装备外观','style_director'),o('在熟悉的村镇和道路上活动，按自己的节奏生活','cozy_resident')]),
q('G04','《{game}》的一段任务告一段落，你最常想继续了解什么？',[o('相关人物后来怎样了，有没有没看到的对话','story_keeper'),o('自己有没有漏掉可以拼起来的线索','puzzle_breaker'),o('同一件事能否用另一套行动方式完成','play_inventor'),o('这次经历是否符合自己想扮演的亨利','role_player')])],
'dave':[
q('G01','准备在《{game}》里再次下水时，你最想给这次潜水定什么目标？',[o('找一种鱼卡里还没有的鱼','collector'),o('按寿司店的菜单需要，定向准备食材','systems_builder'),o('去还没走过的海域，看看会遇见什么','wanderer'),o('完成手头委托，看看人物和故事接下来会怎样','story_keeper')]),
q('G02','《{game}》里准备开店时，你最愿意琢磨哪件事？',[o('食材和菜单怎样安排，才能让经营持续运转','systems_builder'),o('把自己喜欢的菜品继续强化和培养起来','growth_keeper'),o('店里的布局和装饰怎样更符合自己的风格','style_director'),o('期待今晚来访的人，看看有没有新故事','story_keeper')]),
q('G03','《{game}》里，有了新的装备或工具后，你最想用它做什么？',[o('去之前没能深入的海域，看看新内容','wanderer'),o('捕捉还没收进鱼卡的鱼种','collector'),o('改善潜水和取材安排，让需要的材料更好获得','build_alchemist'),o('试试新的操作或工具手感，看看实际用起来怎样','feedback_engine')]),
q('G04','回想《{game}》，哪种积累最让你想继续？',[o('鱼卡、食材或想做的收集逐渐补齐','collector'),o('装备、菜品和店铺一步步成长起来','growth_keeper'),o('潜水、取材和开店之间的安排越来越顺手','systems_builder'),o('蓝洞和人物故事不断出现新的发现','story_keeper','wanderer')])]
}

# Generic families use only their actual broad mechanics. They never invent named characters or quests.
FAMILIES={
'action':(['练熟移动、攻击或回避的节奏','把装备和技能配合起来','尝试不常用的打法','找到以前没处理好的难点，再亲自试试'],['feedback_engine','build_alchemist','play_inventor','practice_seeker'],'一个操作环节反复没有处理好',['多试几次，把动作节奏练熟','调整可用的装备或技能安排','找一段操作讲解，看看自己漏了什么','先体验别的内容，之后再回来']),
'shooter':(['操作、瞄准和反馈连在一起的手感','为明确的对抗目标做准备','比较武器或战术的配合','和熟悉的同伴一起经历过程'],['feedback_engine','rank_worker','build_alchemist','social_spark'],'一个战斗环节反复没有达到目标',['回到相似场景，练自己想改善的操作','调整武器或行动方案，再验证效果','找针对这个环节的讲解或演示','先和同伴说明卡点，再商量下一步']),
'strategy':(['把资源、步骤和后续发展安排顺','比较不同单位、卡牌或规则的配合','亲自解决一个一直没想通的问题','换一种路线，看看系统会怎样变化'],['systems_builder','build_alchemist','puzzle_breaker','play_inventor'],'一个原定方案没有产生想要的结果',['重新看资源和步骤，调整整体安排','改变几个组合，比较实际的变化','参考一份讲解，弄清自己遗漏的规则','暂时换一条发展路线，试试别的可能']),
'management':(['让资源和工作流程持续运转起来','把正在培养的对象慢慢发展起来','让空间和布局呈现自己的风格','按自己的节奏进行熟悉的经营'],['systems_builder','growth_keeper','style_director','cozy_resident'],'一处流程反复出现短缺或堵塞',['沿着流程逐段查看，找出是哪一环影响了后续','换一种资源或布局安排，看看实际效果','参考一个示例，理解它怎样解决类似问题','先把规模保持住，换一件自己想做的小事']),
'life':(['用喜欢的节奏进行熟悉的活动','看培养的对象和成果慢慢成长','布置一个带有个人风格的空间','体验人物之间的关系和故事'],['cozy_resident','growth_keeper','style_director','story_keeper'],'一件事情的推进比预想慢',['给它留些时间，继续做自己喜欢的日常','调整资源和步骤，换个安排继续','查一份说明，看看还有什么条件没满足','先去体验别的活动，之后再回来']),
'creative':(['搭出带有自己风格的作品','试一种以前没做过的玩法或规则','把结构和运行方式安排顺','和同好分享各自做出来的东西'],['style_director','play_inventor','systems_builder','social_spark'],'一个搭建或实验没有出现预想的效果',['先拆开几个部分，逐步检查发生了什么','换一种材料、结构或规则继续试','参考一个现成示例，再按自己的需要调整','保留这次结果，先做另一个想法']),
'puzzle':(['把线索连起来，亲自弄清解法','发现环境里还没有注意过的细节','尝试一种看起来不寻常的解题方式','按自己的节奏，慢慢体验眼前的内容'],['puzzle_breaker','wanderer','play_inventor','cozy_resident'],'一个谜题卡住了',['把线索重新排一遍，再验证一个猜想','试一种之前没有尝试过的互动或顺序','找一条提示，暂时不看完整答案','先换到别的内容，过一会儿再想']),
'story':(['理解人物为什么这样选择','把自己带入角色的处境','找出故事线索怎样相互联系','回到熟悉的片段，再体验一次'],['story_keeper','role_player','puzzle_breaker','cozy_resident'],'一段人物行为或故事转折没看明白',['回看已经出现的对话与线索','沿着自己的理解继续体验，看看后续怎样解释','找只讨论已体验部分的分析','暂时记下疑问，先体验另一段内容']),
'rogue':(['操作与反馈连在一起的畅快','每次得到不同内容，再重新组合方案','逐渐掌握以前没有处理好的环节','新的路径或随机变化带来的发现'],['feedback_engine','build_alchemist','practice_seeker','wanderer'],'一次尝试在熟悉的难点结束了',['再试一次，练刚才没有处理好的环节','调整组合或资源的用法，换个方案','找针对这个难点的讲解，再自己尝试','换一种开局或路线，体验别的变化']),
'cards':(['卡牌或组件之间形成配合','弄清规则和结算为什么这样发生','尝试一套不常见的组合','和熟悉的同伴一起体验过程'],['build_alchemist','puzzle_breaker','play_inventor','social_spark'],'一种组合没有打出预想的效果',['重新看组件的先后顺序和条件','换几个组件，比较实际变化','找一份规则说明或示例','先试另一套自己也感兴趣的组合']),
'rhythm':(['动作、音乐和反馈对上的畅快','逐渐掌握曾经跟不上的段落','完成自己想补齐的曲目或目标','按喜欢的节奏重温熟悉内容'],['feedback_engine','practice_seeker','collector','cozy_resident'],'一段节奏或操作反复跟不上',['挑出那个段落，再练几次','换一种操作设置或练习安排','找演示，听听或看看别人怎样处理','先换一段喜欢的内容，之后再回来']),
'racing':(['驾驶操作与速度反馈的手感','逐渐改善自己在路线上的表现','比较可用的车辆或设置','和其他玩家直接较量的过程'],['feedback_engine','practice_seeker','build_alchemist','rank_worker'],'一个弯道或路段总是不顺手',['重复跑相似的路段，练操作节奏','调整可用设置，比较跑起来的变化','找路线或驾驶讲解，看看有哪些处理方法','先换一条路线，之后再回来']),
'sports':(['动作和反馈带来的畅快','把某个自己想练的环节掌握得更熟','围绕比赛胜负认真做准备','和熟悉的同伴一起参加过程'],['feedback_engine','practice_seeker','rank_worker','social_spark'],'一个比赛环节总是没有打出预想的表现',['回到相似情境，练那个动作或时机','换一种可用的配置或战术安排','找讲解，看看还可以怎样处理','先换一种自己也想体验的内容']),
'hidden':(['找出画面里原本没有注意到的物体','把想找的物体或目标逐项补齐','欣赏场景和画面的细节','在熟悉的规则里慢慢找一会儿'],['puzzle_breaker','collector','style_director','cozy_resident'],'有一个物体迟迟没有找到',['换一种查看顺序，把画面再看一遍','先找其他位置，之后再回来看','使用游戏提供的提示','暂时停在喜欢的场景里，不急着完成']),
'flight':(['操控飞行或航行时的手感','规划路线和途中需要的资源','去没到过的地方看看景色','逐渐掌握一个以前不熟悉的操作'],['feedback_engine','systems_builder','wanderer','practice_seeker'],'一个操控或路线环节没有按预想完成',['在相似条件下再练几次','重新检查路线和可用设置','找针对这个环节的说明或演示','先换个自己也感兴趣的目的地']),
'adventure':(['去不知道有什么的地方看看','经历人物与世界中的故事','让自己扮演的角色有一条自己的路','按喜欢的节奏重温熟悉的过程'],['wanderer','story_keeper','role_player','cozy_resident'],'一段推进暂时卡住了',['再观察附近的线索和可以尝试的互动','换一种可用的方式，看看能否继续','找一条针对当前进度的提示','先去体验其他可选内容，之后再回来'])
}


def family_pack(name,data):
    activities,ids,problem,solutions=data
    opts=[o(a,p) for a,p in zip(activities,ids)]
    # A remedy is a contextual habit, not automatically motor practice or build interest.
    solution_weights={'action':[('practice_seeker',),('build_alchemist',),(),()], 'shooter':[('practice_seeker',),('build_alchemist',),(),()], 'strategy':[('systems_builder',),('build_alchemist',),(),('play_inventor',)]}.get(name,[(),(),(),()])
    return [q('G01','玩《{game}》时，哪部分最容易让你主动留下来？',opts),q('G02','《{game}》里，'+problem+'，你最常先怎么处理？',[o(t,*w) for t,w in zip(solutions,solution_weights)]),q('G03','回想《{game}》，你最想再次经历哪个过程？',[o('把原来不熟悉的内容逐渐掌握','practice_seeker'),o(activities[0],ids[0]),o(activities[1],ids[1]),o(activities[2],ids[2])]),q('G04','给《{game}》留一段自己的游玩记录，你最想记下什么？',[o('自己发现的新内容或不同走法','wanderer'),o('一套实际试过、想继续改进的安排','build_alchemist'),o('自己喜欢的画面或体验片段'),o('和同好交流后，让自己记住的经历','social_spark')])]


COMMON=[
q('G05','《{game}》里第一次接触一个没完全弄明白的机制，你通常先做什么？',[o('自己试几种用法，再看看发生了什么',habit='try_first'),o('先找规则说明，把基本用法看明白',habit='rules_first'),o('先参考一个成熟方案，实际体验后再改',habit='build_first'),o('向玩过的人提问，再自己试试',habit='ask_first')],topic='approach'),
q('G06','《{game}》里，一段内容反复没有按你希望的方式完成。你通常先怎么安排？',[o('继续尝试，留意刚才没有处理好的地方',habit='failure_retry'),o('先换一处配置或做法，再回来尝试',habit='failure_adjust'),o('先体验别的内容，之后再考虑回来',habit='failure_switch'),o('先暂停这段内容，下一次再继续',habit='failure_pause')],topic='failure'),
q('G07','如果要查《{game}》的游戏外资料，你最常为了什么去查？',[o('理解机制、规则或操作的具体用法',habit='guide_mechanics'),o('找到遗漏内容或收集目标的位置',habit='guide_completion'),o('卡住后拿到一个提示，再回来自己继续',habit='guide_hint'),o('通常更愿意自己尝试，不主动查资料',habit='guide_independent')],topic='guide'),
q('G08','有人准备提前介绍《{game}》中你还没体验的内容或解法，你会先怎么说？',[o('先别讲结果或完整解法，给一点提示就好',habit='spoiler_hint'),o('只讲通用规则，具体内容留给我自己体验',habit='spoiler_rules'),o('可以直接讲清楚，我想知道后再去体验',habit='spoiler_open'),o('先问我体验到哪里，再决定这次讲多少',habit='spoiler_ask')],topic='spoiler'),
q('G09','谈到《{game}》的重玩、重新开档或重温已有内容，哪项最符合你现在的情况？',[o('通常愿意重温，或换一种玩法再体验',habit='replay_willing'),o('想再体验，但目前可支配的时间不够',habit='replay_time_limited'),o('通常体验一次就够，更想把时间留给新作品',habit='replay_new_first'),o('还没体验到考虑重玩的阶段',habit='replay_not_yet')],topic='replay'),
q('G10','你实际玩《{game}》的平台或版本上，Mod对你是哪种情况？',[o('条件允许时会使用Mod',habit='mod_use'),o('有适用条件，但更想保留原版体验',habit='mod_original'),o('平台、版本或安装条件限制了使用',habit='mod_limited'),o('还没有了解或接触过这方面',habit='mod_unknown')],topic='mod'),
q('G11','有人刚开始玩《{game}》并向你询问建议，你更愿意怎样介绍？',[o('先问他想体验什么，再说对应的内容',habit='intro_ask'),o('把入门要做的事和容易忽略的步骤说清楚','quest_board',habit='intro_plan'),o('分享自己记得最深的片段，不提前揭晓后续','social_spark',habit='intro_share'),o('只说必要的信息，让他先自己发现',habit='intro_discover')],topic='sharing'),
q('G12','下一次打开《{game}》时，你通常怎样安排要做的事？',[o('接着已经排好的目标，按顺序推进',habit='pace_planned'),o('看眼前最想做什么，途中可以改变安排',habit='pace_flexible'),o('先围绕一件惦记的内容，继续把它弄明白',habit='pace_deep'),o('和同好约好体验或交流进度，再安排这次内容',habit='pace_shared')],topic='pace'),
q('X13','暂时放下本命作品，有四种新体验可以选，你最想先点开哪一种？',[o('地图上还有很多不知道会遇到什么的地方','wanderer'),o('人物的选择会展开一段值得追下去的故事','story_keeper'),o('操作、音效和反馈连起来十分畅快','feedback_engine'),o('角色或空间可以按自己的风格设计','style_director')],scope='cross',topic='cross_interest'),
q('X14','朋友准备和你一起安排游戏时间，你最期待哪种相处方式？',[o('一起体验和聊天，进度可以跟着大家的兴趣走','social_spark'),o('先说好共同目标和分工，再一起推进','quest_board'),o('各自玩也可以，保留自己的节奏，之后再分享','cozy_resident'),o('用自己扮演的角色身份，和大家共同经历故事','role_player')],scope='cross',topic='coop'),
q('X15','如果给一个游戏目标留出长期位置，你更想持续做哪件事？',[o('把以前处理不了的难点逐渐练会','practice_seeker'),o('补齐一直想收的图鉴、藏品或完成清单','collector'),o('培养角色、队伍或经营对象，看积累逐渐留下来','growth_keeper'),o('参与明确的对抗，争取更好的排名或胜负结果','rank_worker')],scope='cross',topic='long_goal'),
q('X16','再选一种能让你投入的游戏内容，你更想体验什么？',[o('把线索连起来，验证自己怎样解开谜题','puzzle_breaker'),o('把生产、资源和流程安排成持续运转的体系','systems_builder'),o('试不同寻常的玩法，看看规则还允许什么','play_inventor'),o('让卡牌、装备或阵容之间产生新的配合','build_alchemist')],scope='cross',topic='systems_interest')
]


# These substitutions keep the same habits/scoring key while grounding the action in the selected work.
ANCHOR_CONTEXT={
'civ6':{
'G05':('《{game}》里，第一次接触还没弄懂的区域相邻加成，你通常先怎么做？',['在地图上试着摆一摆，看看产出怎样变化','先看文明百科，弄清地形与区域的加成规则','参考一份区域布局，再按自己的地图调整','问玩过的人这处地形可以怎样安排']),
'G06':('《{game}》里，原本想发展的城市迟迟没有达到预期产出。你通常先怎么安排？',['继续看几个回合，找出具体卡在哪一步','改一处区域、政策或资源安排，再看结果','先发展其他城市，之后再回来看这里','先放下这份存档，下次接着处理']),
'G07':('如果查《{game}》的资料，你最常想解决哪件事？',['弄懂区域、政策或资源怎样影响产出','找到遗漏的要素或自己想完成的内容','拿到一点针对卡点的提示，再回存档尝试','通常先自己试，不主动查资料']),
'G12':('下一次打开《{game}》存档，你通常从哪里接着玩？',['接着之前排好的建造和发展目标推进','看看地图上新出现了什么，再决定去做哪件事','继续琢磨一座城市或一条路线，暂时不换目标','先和一起玩的同好确认进度，再接着安排'])},
'rdr2':{
'G05':('《{game}》里，刚开始接触还没弄明白的狩猎要领，你通常先怎么做？',['亲自试几次，看看猎物和装备有什么不同','先看游戏提示，弄清基本规则','先参考一套狩猎做法，再边玩边改','先问玩过的人，再自己去试']),
'G06':('《{game}》里，一段自己想完成的任务反复没有顺利通过。你通常先怎么安排？',['再尝试一次，留意刚才没处理好的地方','换一下装备或行动方式，再试这段任务','先骑去做点别的，之后再回来','先停在这里，下次打开游戏再继续']),
'G07':('如果查《{game}》的资料，你最常为了什么去查？',['理解狩猎、装备或操作的具体规则','找还缺的猎物、藏品或遗漏内容','只拿到当前任务的一点提示，再自己继续','通常更愿意自己寻找，不主动查资料']),
'G12':('下一次打开《{game}》时，你通常先怎样安排亚瑟的去向？',['接着之前想推进的任务或目标走','骑出去看看，遇到什么再决定','继续追一件惦记的事，暂时不换目标','先和同好交流进度，再决定体验到哪里'])},
'ds1':{
'G05':('《{game}》里，刚接触还没弄懂的新运输工具，你通常先怎么做？',['带它走一小段，亲自试出使用方式','先看说明，弄清载重和使用规则','参考一套运输安排，实际送过后再改','问玩过的人适合怎样使用，再自己试']),
'G06':('《{game}》里，一份订单反复没能按你希望的方式送达。你通常先怎么安排？',['再走一次，留意刚才出问题的地形','换一下工具、装载或路线，再送这份订单','先送其他订单，之后再回来处理','先暂停配送，下次再接着送']),
'G07':('如果查《{game}》的资料，你最常想知道什么？',['工具、设施或运输规则的具体用法','遗漏的订单、地点或收集内容在哪里','当前路段的一点提示，剩下由自己走','通常先亲自找路线，不主动查资料']),
'G12':('下一次打开《{game}》时，你通常先怎样安排配送？',['接着已经排好的订单或修建目标推进','看看手头和路上的情况，随时改变安排','继续处理一条惦记的路线或订单','先和同好约好交流的订单或路段，再行动'])},
'dc':{
'G05':('《{game}》里，第一次拿到还没弄懂用法的武器，你通常先怎么做？',['找机会挥几下，试试攻击和移动的节奏','先看武器说明，弄懂基本用法','先参考一套武器搭配，打过后再调整','问玩过的人这件武器怎样用，再自己试']),
'G06':('《{game}》里，同一个Boss反复挡住了这次挑战。你通常先怎么安排？',['再尝试一次，留意刚才没处理好的招式','换一下装备或应对方式，再回来打','先换条路线体验别的内容','先暂停挑战，下次再继续']),
'G07':('如果查《{game}》的资料，你最常为了什么去查？',['弄懂武器、技能或敌人招式的用法','寻找缺少的蓝图、路线或解锁内容','只看当前卡点的一点提示，再自己打','通常更愿意亲自尝试，不主动查资料']),
'G12':('下一次打开《{game}》时，你通常先安排什么？',['接着之前想打的路线或目标继续','看看这次得到的装备，再临时决定打法','继续琢磨一个惦记的武器或Boss','先和同好约好挑战或交流进度，再开始'])},
'sts':{
'G05':('《{game}》里，第一次遇到还没弄懂的卡牌效果，你通常先怎么做？',['实际打出去，看看它会怎样结算','先读卡面与说明，弄清基本规则','先参考一套带这张牌的构筑，体验后再改','向玩过的人提问，再自己试这张牌']),
'G06':('《{game}》里，几次爬塔都停在相近的地方。你通常先怎么安排？',['再试一次，留意刚才没处理好的出牌环节','改一处选牌或路线做法，再开始尝试','先换个角色或体验别的内容','先暂停爬塔，下次再继续']),
'G07':('如果查《{game}》的资料，你最常想弄清什么？',['卡牌、遗物和敌人规则怎样结算','自己遗漏的解锁、成就或事件内容','当前卡点的一点提示，剩下自己判断','通常先自己打，不主动查资料']),
'G12':('下一次打开《{game}》时，你通常先安排什么？',['接着之前想尝试的角色、进阶或构筑目标','看看这次拿到的卡和遗物，再临时改变路线','继续琢磨一张牌、一套配合或一个敌人','先和同好约好爬塔或交流进度，再开始'])},
'bannerlord':{
'G05':('《{game}》里，刚接触还没弄懂的兵种与阵形指令，你通常先怎么做？',['亲自下几次指令，观察部队怎样移动和作战','先看指令说明，弄清各个命令的用法','参考一套部队安排，打过后再调整','向玩过的人提问，再自己带队试']),
'G06':('《{game}》里，几次相近的交战都没打出想要的结果。你通常先怎么安排？',['接着尝试，留意刚才没处理好的操作或时机','调整兵种、位置或指令，再找机会交战','先跑商、做任务或发展队伍，之后再回来','先放下这份存档，下次接着处理']),
'G07':('如果查《{game}》的资料，你最常为了什么去查？',['理解兵种、阵形、经济或操作的具体规则','找到遗漏内容或自己想完成的目标','拿到当前卡点的一点提示，再自己试','通常更愿意自己带队摸索，不主动查资料']),
'G12':('下一次打开《{game}》存档，你通常先怎样安排行动？',['接着之前排好的征战、经营或任务目标','看看路上和各方势力的情况，再临时决定','继续琢磨一支队伍、一种兵种或一条路线','先和同好交流各自进度，再安排这次内容'])},
'kcd2':{
'G05':('《{game}》里，刚接触还没弄懂的锻造步骤，你通常先怎么做？',['亲手做几次，看看每一步有什么变化','先看教学说明，弄清基本步骤','参考一段完整演示，再自己做和调整','先向玩过的人提问，再自己试']),
'G06':('《{game}》里，一段自己想完成的任务反复不顺利。你通常先怎么安排？',['再尝试一次，留意刚才没处理好的地方','换一下装备或解决方法，再来试','先做别的任务或活动，之后再回来','先暂停这段任务，下次再继续']),
'G07':('如果查《{game}》的资料，你最常想解决哪件事？',['弄懂战斗、锻造或炼金的具体规则','寻找遗漏的物品、支线或完成目标','只拿到当前任务的一点提示，再自己解决','通常先自己在世界里找，不主动查资料']),
'G12':('下一次打开《{game}》时，你通常怎样安排亨利的去向？',['接着之前排好的任务或生活目标','看看镇上和路上发生了什么，再决定','继续琢磨一条支线、一项手艺或一个难点','先和同好交流任务进度，再决定体验到哪里'])},
'dave':{
'G05':('《{game}》里，刚拿到还没弄懂的新捕捉工具，你通常先怎么做？',['带它下水，亲自试试怎样使用','先看工具说明，弄清基本用法','参考一套工具和潜水安排，用过后再改','问玩过的人适合怎样使用，再自己试']),
'G06':('《{game}》里，几次潜水都没能完成想做的捕捉目标。你通常先怎么安排？',['再下去一次，留意刚才没处理好的地方','调整工具或潜水安排，再去试','先捕别的鱼或处理店铺内容，之后再回来','先暂停潜水，下次再继续这个目标']),
'G07':('如果查《{game}》的资料，你最常为了什么去查？',['理解工具、潜水或店铺经营的具体规则','寻找缺少的鱼种、物品或任务内容','只拿到当前卡点的一点提示，再自己试','通常更愿意亲自下水找，不主动查资料']),
'G12':('下一次打开《{game}》时，你通常先怎样安排？',['接着之前的取材、菜单或委托目标推进','看看手头食材和新情况，再临时决定','继续追一条惦记的鱼或琢磨一道菜','先和同好约好交流的内容或进度，再开始'])}
}


TIES={
'wanderer':['去没有明确奖励的未知角落，看看会发现什么','放下既定路线，追一个途中突然出现的新发现'],
'story_keeper':['留下来听完人物对话，看看这段故事怎样继续','回看已经经历的情节，弄清人物前后选择的联系'],
'role_player':['按自己给角色设定的身份来选择行动','换一种角色身份，体验另一种行事方式'],
'puzzle_breaker':['把现有线索重新拼起来，验证一个猜想','自己解释一个没想明白的规则或谜题'],
'practice_seeker':['回到同一个难点，把刚才没掌握的环节练熟','回看刚才失败的片段，下一次换一种操作时机再试'],
'rank_worker':['参与一次明确的较量，围绕胜负做准备','为更好的对抗结果或排名调整自己的准备'],
'feedback_engine':['重温一段操作和反馈连起来很畅快的内容','拿起手感喜欢的操作，再享受一次直接的反馈'],
'build_alchemist':['比较几个组件的配合，把方案实际试出来','换几张卡、装备或阵容，看看组合效果怎样变化'],
'systems_builder':['把资源和步骤理顺，让后续内容持续运转','调整一处瓶颈，让整个流程更符合自己的安排'],
'growth_keeper':['继续培养喜欢的对象，让长期投入留下成长','推进一条养成路线，看看角色或队伍怎样变化'],
'collector':['找出清单上还缺的一项，把它补齐','回到已有内容，收齐自己一直想要的一组东西'],
'style_director':['调整角色或空间的外观，让它更有自己的风格','围绕一个主题，把自己的作品或搭配继续完善'],
'play_inventor':['试一套不同寻常的规则或组合，看看会发生什么','换一种平时不玩的方式，让这次体验走向新结果'],
'social_spark':['找熟悉的同伴一起体验，过程里发生什么都想分享','和同好聊聊各自的经历，把共同体验接着延续'],
'quest_board':['和同伴说清目标、分工和推进节奏','把大家想做的事整理成可以一起执行的安排'],
'cozy_resident':['按自己的节奏重温熟悉的活动，不急着追目标','留在一个安稳熟悉的过程中，从容体验一会儿']
}


DETAILS={
'wanderer':'你愿意让一条没体验过的路线或线索，成为继续玩的理由。新的发现会牵动接下来的安排。',
'story_keeper':'你愿意把注意力留给人物和事件的后续，故事展开本身就是继续体验的理由。',
'role_player':'你会把角色身份带进行动选择，让经历连成自己想扮演的那种人生。',
'puzzle_breaker':'你愿意围绕线索或规则继续推敲，想亲自弄清一个解释能否成立。',
'practice_seeker':'亲手处理以前没有掌握的难点，会让你愿意再次尝试；这里说的是练会它的兴趣。',
'rank_worker':'有明确对手、胜负或排名的较量，会给你一个值得投入的目标。',
'feedback_engine':'操作、声音与即时反馈连起来的感觉，会直接影响你想不想继续体验。',
'build_alchemist':'你愿意比较组件之间怎样配合，再用实际效果检验搭配是否合意。',
'systems_builder':'你关心资源和步骤怎样接起来，愿意让零散的安排形成能继续运转的体系。',
'growth_keeper':'看着自己持续投入的角色、队伍或其他对象逐步成长，是你愿意留下来的理由。',
'collector':'一个惦记的缺项被补齐，会给你明确的完成感；收集目标本身就能牵动安排。',
'style_director':'你愿意调整角色、空间或作品的呈现，让最后留下的样子符合自己的风格。',
'play_inventor':'不熟悉的组合和不同寻常的限制，会让你想看看规则还能带出什么结果。',
'social_spark':'把经历分享给同好，或与同伴共同体验，会成为游戏吸引力的一部分。',
'quest_board':'和同伴约好目标、分工或推进节奏，会让你更愿意进入共同的安排。',
'cozy_resident':'能按自己的节奏待在熟悉的活动里，本身就值得投入，不一定要再增加目标。'
}


def main():
    personas=json.loads((ROOT/'config/personas.v0.4.draft.json').read_text(encoding='utf-8'))['personas']
    for p in personas:p['portrait']='/assets/personas/'+p['id']+'.png'
    config={'versions':{'instrument':'0.4.0','scoring':'0.4.0','report_rules':'0.4.0','catalog':'0.4.0'},'status':'原创探索版，待真人试测','personas':personas,'packs':PACKS,'families':{name:family_pack(name,data) for name,data in FAMILIES.items()},'common':COMMON,'tie_actions':TIES,'rules':{'base_count':16,'max_extra':2,'close_gap_points':2,'tie_bonus':4,'scoring':'sum_selected_semantic_weights_only','tie_order':['points','anchor_support_count','last_discriminator_choice','persona_order'],'mod_replay_spoiler_no_persona_points':True},'reference':'回想你通常怎样玩；选最符合自己的一个做法，没有更好的答案。'}
    config['report_copy']={'persona_details':DETAILS,'multi_context_min_evidence':2,'single_evidence_prefix':'在这道题给出的情境里，你选择了：','cross_echo_template':'在本命作品和跨游戏选择中，都出现了“{pull}”相关体验。'}
    report_source=json.loads((ROOT/'config/report-copy.v0.4.0.json').read_text(encoding='utf-8'))
    config['report_copy'].update({k:v for k,v in report_source.items() if k!='version'})
    portrait_source=json.loads((ROOT/'config/personality-portraits.v0.4.1.json').read_text(encoding='utf-8'))
    config['versions']['report_rules']=portrait_source['version']
    config['personality_portraits']=portrait_source
    config['compatible_report_versions']=['0.4.0',portrait_source['version']]
    config['anchor_context']=ANCHOR_CONTEXT
    (ROOT/'config/youge.v0.4.0.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Frozen v0.4: 8 game packs, '+str(len(FAMILIES))+' mechanic families, 16 single-choice items per form')


if __name__=='__main__':main()
