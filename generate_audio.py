#!/usr/bin/env python3
"""
批量生成英语单词音频文件
使用 Edge TTS（微软免费 TTS 服务）
"""

import asyncio
import edge_tts
import os
import json
from pathlib import Path

# 音频输出目录
AUDIO_DIR = Path("audio")

# 人教版小学英语单词（从游戏代码中提取）
VOCABULARY = {
    "1": [
        ("apple", "苹果"), ("book", "书"), ("cat", "猫"), ("dog", "狗"),
        ("egg", "鸡蛋"), ("fish", "鱼"), ("girl", "女孩"), ("hand", "手"),
        ("ice cream", "冰淇淋"), ("juice", "果汁"), ("kite", "风筝"), ("lion", "狮子"),
        ("milk", "牛奶"), ("nose", "鼻子"), ("orange", "橙子"), ("pencil", "铅笔"),
        ("queen", "女王"), ("ruler", "尺子"), ("school", "学校"), ("teacher", "老师"),
        ("umbrella", "雨伞"), ("violin", "小提琴"), ("water", "水"), ("box", "盒子"),
        ("yellow", "黄色"), ("zoo", "动物园"), ("bag", "书包"), ("pen", "钢笔"),
        ("red", "红色"), ("blue", "蓝色"), ("green", "绿色"), ("black", "黑色"),
        ("white", "白色"), ("one", "一"), ("two", "二"), ("three", "三"),
        ("four", "四"), ("five", "五"), ("six", "六"), ("seven", "七"),
        ("eight", "八"), ("nine", "九"), ("ten", "十"), ("face", "脸"),
        ("eye", "眼睛"), ("ear", "耳朵"), ("mouth", "嘴巴"), ("arm", "手臂"),
        ("leg", "腿"), ("foot", "脚"), ("head", "头"), ("bird", "鸟"),
        ("duck", "鸭子"), ("pig", "猪"), ("bear", "熊"), ("elephant", "大象"),
        ("monkey", "猴子"), ("tiger", "老虎"), ("panda", "熊猫"), ("bread", "面包"),
        ("rice", "米饭"), ("cake", "蛋糕"), ("noodles", "面条"), ("chicken", "鸡肉"),
        ("beef", "牛肉"), ("vegetables", "蔬菜"), ("fruits", "水果"), ("banana", "香蕉"),
        ("grape", "葡萄"), ("watermelon", "西瓜"), ("strawberry", "草莓"), ("pear", "梨"),
        ("peach", "桃子"), ("run", "跑"), ("jump", "跳"), ("swim", "游泳"),
        ("fly", "飞"), ("walk", "走"), ("sing", "唱歌"), ("dance", "跳舞"),
        ("draw", "画画"), ("read", "读"), ("write", "写")
    ],
    "2": [
        ("father", "爸爸"), ("mother", "妈妈"), ("brother", "兄弟"), ("sister", "姐妹"),
        ("grandpa", "爷爷"), ("grandma", "奶奶"), ("man", "男人"), ("woman", "女人"),
        ("family", "家庭"), ("friend", "朋友"), ("student", "学生"), ("doctor", "医生"),
        ("nurse", "护士"), ("driver", "司机"), ("farmer", "农民"), ("cook", "厨师"),
        ("morning", "早上"), ("afternoon", "下午"), ("evening", "晚上"), ("night", "夜晚"),
        ("today", "今天"), ("tomorrow", "明天"), ("yesterday", "昨天"), ("week", "星期"),
        ("Monday", "星期一"), ("Tuesday", "星期二"), ("Wednesday", "星期三"), ("Thursday", "星期四"),
        ("Friday", "星期五"), ("Saturday", "星期六"), ("Sunday", "星期日"), ("spring", "春天"),
        ("summer", "夏天"), ("autumn", "秋天"), ("winter", "冬天"), ("sunny", "晴朗的"),
        ("cloudy", "多云的"), ("rainy", "下雨的"), ("windy", "有风的"), ("snowy", "下雪的"),
        ("hot", "热的"), ("cold", "冷的"), ("warm", "温暖的"), ("cool", "凉爽的"),
        ("big", "大的"), ("small", "小的"), ("long", "长的"), ("short", "短的"),
        ("tall", "高的"), ("short", "矮的"), ("fat", "胖的"), ("thin", "瘦的"),
        ("new", "新的"), ("old", "旧的"), ("happy", "开心的"), ("sad", "难过的"),
        ("angry", "生气的"), ("tired", "累的"), ("hungry", "饿的"), ("thirsty", "渴的"),
        ("beautiful", "美丽的"), ("nice", "好的"), ("good", "好的"), ("bad", "坏的"),
        ("bedroom", "卧室"), ("living room", "客厅"), ("kitchen", "厨房"), ("bathroom", "浴室"),
        ("door", "门"), ("window", "窗户"), ("desk", "书桌"), ("chair", "椅子"),
        ("table", "桌子"), ("bed", "床"), ("sofa", "沙发"), ("fridge", "冰箱"),
        ("TV", "电视"), ("phone", "电话"), ("computer", "电脑"), ("picture", "图画"),
        ("clock", "时钟"), ("hat", "帽子"), ("coat", "外套"), ("shirt", "衬衫"),
        ("skirt", "裙子"), ("dress", "连衣裙"), ("pants", "裤子"), ("shoes", "鞋子"),
        ("socks", "袜子"), ("gloves", "手套"), ("scarf", "围巾"), ("umbrella", "雨伞"),
        ("toy", "玩具"), ("ball", "球"), ("doll", "玩偶"), ("car", "汽车"),
        ("bus", "公交车"), ("bike", "自行车"), ("plane", "飞机"), ("ship", "船"),
        ("train", "火车"), ("subway", "地铁"), ("taxi", "出租车"), ("boat", "小船")
    ],
    "3": [
        ("UK", "英国"), ("Canada", "加拿大"), ("USA", "美国"), ("Australia", "澳大利亚"),
        ("China", "中国"), ("where", "哪里"), ("from", "来自"), ("about", "关于"),
        ("he", "他"), ("she", "她"), ("pupil", "学生"), ("student", "学生"),
        ("teacher", "教师"), ("this", "这"), ("that", "那"), ("nice", "愉快的"),
        ("meet", "遇见"), ("grandfather", "祖父"), ("grandmother", "祖母"), ("father", "父亲"),
        ("mother", "母亲"), ("brother", "兄/弟"), ("sister", "姐/妹"), ("thin", "瘦的"),
        ("fat", "胖的"), ("tall", "高的"), ("short", "矮的"), ("long", "长的"),
        ("small", "小的"), ("big", "大的"), ("giraffe", "长颈鹿"), ("so", "这么"),
        ("children", "儿童"), ("tail", "尾巴"), ("on", "在...上"), ("in", "在...里"),
        ("under", "在...下"), ("chair", "椅子"), ("desk", "书桌"), ("cap", "帽子"),
        ("ball", "球"), ("car", "小汽车"), ("boat", "小船"), ("map", "地图"),
        ("toy", "玩具"), ("box", "盒"), ("buy", "买"), ("fruit", "水果"),
        ("pear", "梨"), ("apple", "苹果"), ("orange", "橙子"), ("banana", "香蕉"),
        ("watermelon", "西瓜"), ("grape", "葡萄"), ("strawberry", "草莓"), ("eleven", "十一"),
        ("twelve", "十二"), ("thirteen", "十三"), ("fourteen", "十四"), ("fifteen", "十五"),
        ("sixteen", "十六"), ("seventeen", "十七"), ("eighteen", "十八"), ("nineteen", "十九"),
        ("twenty", "二十"), ("beautiful", "美丽的"), ("kite", "风筝"), ("mouth", "嘴"),
        ("nose", "鼻子"), ("eye", "眼睛"), ("ear", "耳朵"), ("face", "脸"),
        ("head", "头"), ("arm", "手臂"), ("hand", "手"), ("body", "身体"),
        ("leg", "腿"), ("foot", "脚"), ("school", "学校"), ("classroom", "教室"),
        ("library", "图书馆"), ("playground", "操场"), ("art room", "美术室"), ("music room", "音乐室"),
        ("computer room", "电脑室"), ("bathroom", "卫生间"), ("gym", "体育馆"), ("first", "第一"),
        ("second", "第二"), ("third", "第三"), ("floor", "楼层"), ("homework", "作业"),
        ("class", "课"), ("lunch", "午餐"), ("breakfast", "早餐"), ("dinner", "晚餐"),
        ("English class", "英语课"), ("music class", "音乐课"), ("PE class", "体育课"), ("art class", "美术课")
    ],
    "4": [
        ("classroom", "教室"), ("window", "窗户"), ("blackboard", "黑板"), ("light", "电灯"),
        ("picture", "图画"), ("door", "门"), ("teacher's desk", "讲台"), ("computer", "计算机"),
        ("fan", "风扇"), ("wall", "墙壁"), ("floor", "地板"), ("really", "真的"),
        ("near", "距离近"), ("TV", "电视"), ("clean", "打扫"), ("help", "帮助"),
        ("schoolbag", "书包"), ("maths book", "数学书"), ("English book", "英语书"), ("Chinese book", "语文书"),
        ("storybook", "故事书"), ("candy", "糖果"), ("notebook", "笔记本"), ("toy", "玩具"),
        ("key", "钥匙"), ("wow", "哇"), ("lost", "丢失"), ("cute", "可爱的"),
        ("strong", "强壮的"), ("friendly", "友好的"), ("hair", "头发"), ("quiet", "安静的"),
        ("shoe", "鞋"), ("glasses", "眼镜"), ("his", "他的"), ("or", "或者"),
        ("right", "正确的"), ("hat", "帽子"), ("her", "她的"), ("bedroom", "卧室"),
        ("living room", "客厅"), ("study", "书房"), ("kitchen", "厨房"), ("bathroom", "浴室"),
        ("phone", "电话"), ("bed", "床"), ("sofa", "沙发"), ("fridge", "冰箱"),
        ("table", "桌子"), ("dinner", "晚餐"), ("beef", "牛肉"), ("chicken", "鸡肉"),
        ("noodles", "面条"), ("soup", "汤"), ("vegetable", "蔬菜"), ("chopsticks", "筷子"),
        ("bowl", "碗"), ("fork", "叉子"), ("knife", "刀"), ("spoon", "勺子"),
        ("parents", "父母"), ("uncle", "叔叔"), ("aunt", "阿姨"), ("baby", "婴儿"),
        ("cousin", "表兄弟"), ("doctor", "医生"), ("cook", "厨师"), ("driver", "司机"),
        ("farmer", "农民"), ("nurse", "护士"), ("people", "人"), ("but", "但是"),
        ("little", "小的"), ("puppy", "小狗"), ("football player", "足球运动员"), ("job", "工作"),
        ("basketball", "篮球"), ("player", "运动员"), ("scientist", "科学家"), ("police officer", "警察"),
        ("postman", "邮递员"), ("businessman", "商人"), ("fisherman", "渔民"), ("pilot", "飞行员"),
        ("coach", "教练"), ("reporter", "记者"), ("singer", "歌手"), ("dancer", "舞蹈家"),
        ("artist", "艺术家"), ("writer", "作家"), ("actor", "演员"), ("actress", "女演员"),
        ("waiter", "服务员"), ("waitress", "女服务员"), ("engineer", "工程师"), ("accountant", "会计"),
        ("worker", "工人"), ("cleaner", "清洁工"), ("salesperson", "售货员"), ("baseball", "棒球"),
        ("volleyball", "排球"), ("ping-pong", "乒乓球"), ("badminton", "羽毛球"), ("tennis", "网球")
    ],
    "5": [
        ("young", "年轻的"), ("old", "年老的"), ("funny", "滑稽的"), ("kind", "和蔼的"),
        ("strict", "严格的"), ("polite", "有礼貌的"), ("hard-working", "勤奋的"), ("helpful", "有用的"),
        ("clever", "聪明的"), ("shy", "害羞的"), ("know", "知道"), ("our", "我们的"),
        ("Ms", "女士"), ("will", "将要"), ("sometimes", "有时"), ("robot", "机器人"),
        ("him", "他"), ("speak", "说"), ("finish", "完成"), ("Monday", "星期一"),
        ("Tuesday", "星期二"), ("Wednesday", "星期三"), ("Thursday", "星期四"), ("Friday", "星期五"),
        ("Saturday", "星期六"), ("Sunday", "星期日"), ("weekend", "周末"), ("schedule", "日程表"),
        ("wash my clothes", "洗衣服"), ("watch TV", "看电视"), ("do homework", "做作业"), ("read books", "看书"),
        ("play football", "踢足球"), ("play sports", "做运动"), ("play ping-pong", "打乒乓球"), ("play basketball", "打篮球"),
        ("play the pipa", "弹琵琶"), ("draw cartoons", "画漫画"), ("cook", "烹饪"), ("swim", "游泳"),
        ("speak English", "说英语"), ("play games", "玩游戏"), ("do kung fu", "练功夫"), ("sing English songs", "唱英文歌"),
        ("dance", "跳舞"), ("sandwich", "三明治"), ("salad", "沙拉"), ("hamburger", "汉堡包"),
        ("ice cream", "冰淇淋"), ("tea", "茶"), ("fresh", "新鲜的"), ("healthy", "健康的"),
        ("delicious", "美味的"), ("hot", "辣的"), ("sweet", "甜的"), ("drink", "喝"),
        ("thirsty", "渴的"), ("favourite", "最喜欢的"), ("food", "食物"), ("onion", "洋葱"),
        ("milk", "牛奶"), ("bread", "面包"), ("beef noodles", "牛肉面"), ("fish sandwich", "鱼肉三明治"),
        ("tomato soup", "西红柿汤"), ("sing", "唱"), ("song", "歌曲"), ("sing songs", "唱歌"),
        ("party", "聚会"), ("next", "下一个"), ("wonderful", "极好的"), ("learn", "学习"),
        ("any", "任何的"), ("problem", "问题"), ("no problem", "没问题"), ("want", "想要"),
        ("send", "发送"), ("email", "电子邮件"), ("at", "在"), ("clock", "时钟"),
        ("plant", "植物"), ("bottle", "瓶子"), ("water bottle", "水瓶"), ("bike", "自行车"),
        ("photo", "照片"), ("in front of", "在...前面"), ("beside", "在旁边"), ("behind", "在...后面"),
        ("above", "在...上面"), ("between", "在...之间"), ("grandparents", "祖父母"), ("their", "他们的"),
        ("house", "房子"), ("lots of", "大量"), ("flower", "花"), ("move", "移动"),
        ("dirty", "脏的"), ("everywhere", "到处"), ("mouse", "老鼠"), ("live", "住"),
        ("nature", "自然界"), ("forest", "森林"), ("river", "河流"), ("lake", "湖泊"),
        ("mountain", "高山"), ("hill", "小山"), ("tree", "树"), ("bridge", "桥"),
        ("building", "建筑物"), ("village", "村庄"), ("city", "城市"), ("house", "房子"),
        ("road", "道路"), ("street", "街道"), ("path", "小路"), ("go boating", "去划船"),
        ("go fishing", "去钓鱼"), ("go hiking", "去远足"), ("go shopping", "去购物"), ("go swimming", "去游泳")
    ],
    "6": [
        ("science", "科学"), ("museum", "博物馆"), ("post office", "邮局"), ("bookstore", "书店"),
        ("cinema", "电影院"), ("hospital", "医院"), ("crossing", "十字路口"), ("turn", "转弯"),
        ("left", "左"), ("straight", "笔直地"), ("right", "右"), ("ask", "问"),
        ("sir", "先生"), ("interesting", "有趣的"), ("Italian", "意大利的"), ("restaurant", "餐馆"),
        ("pizza", "比萨饼"), ("street", "街道"), ("get", "到达"), ("GPS", "导航"),
        ("gave", "提供"), ("feature", "特点"), ("follow", "跟着"), ("far", "较远的"),
        ("tell", "告诉"), ("on foot", "步行"), ("by", "乘"), ("bus", "公共汽车"),
        ("plane", "飞机"), ("taxi", "出租车"), ("ship", "轮船"), ("subway", "地铁"),
        ("train", "火车"), ("slow", "慢的"), ("down", "减少"), ("slow down", "慢下来"),
        ("stop", "停下"), ("wait", "等待"), ("traffic lights", "交通信号灯"), ("pay attention to", "注意"),
        ("must", "必须"), ("wear", "戴"), ("helmet", "头盔"), ("sled", "雪橇"),
        ("fast", "快的"), ("ferry", "轮渡"), ("visit", "拜访"), ("film", "电影"),
        ("see a film", "看电影"), ("trip", "旅行"), ("take a trip", "去旅行"), ("supermarket", "超市"),
        ("go to the supermarket", "去超市"), ("evening", "晚上"), ("tonight", "在今晚"), ("tomorrow", "明天"),
        ("next week", "下周"), ("dictionary", "词典"), ("comic book", "漫画书"), ("word book", "单词书"),
        ("postcard", "明信片"), ("lesson", "课"), ("space", "太空"), ("travel", "旅行"),
        ("half price", "半价"), ("mooncake", "月饼"), ("poem", "诗"), ("mid-autumn", "中秋"),
        ("together", "一起"), ("get together", "聚会"), ("moon", "月亮"), ("puzzle", "谜"),
        ("hiking", "远足"), ("dear", "亲爱的"), ("festival", "节日"), ("Spring Festival", "春节"),
        ("Dragon Boat Festival", "端午节"), ("Double Ninth Festival", "重阳节"), ("National Day", "国庆节"), ("New Year's Day", "元旦"),
        ("Children's Day", "儿童节"), ("Teachers' Day", "教师节"), ("Mother's Day", "母亲节"), ("Father's Day", "父亲节"),
        ("Thanksgiving", "感恩节"), ("Christmas", "圣诞节"), ("Halloween", "万圣节"), ("Easter", "复活节"),
        ("angry", "生气的"), ("afraid", "害怕"), ("sad", "难过的"), ("worried", "担心的"),
        ("happy", "高兴的"), ("ill", "有病"), ("wrong", "有毛病"), ("see a doctor", "看病"),
        ("do more exercise", "多做运动"), ("wear warm clothes", "穿暖和的衣服"), ("deep breath", "深呼吸"), ("count to ten", "数到十"),
        ("chase", "追赶"), ("mice", "老鼠"), ("bad", "邪恶的"), ("hurt", "受伤"),
        ("should", "应该"), ("feel", "觉得"), ("well", "健康"), ("sit", "坐"),
        ("grass", "草坪"), ("hear", "听见"), ("ant", "蚂蚁"), ("worry", "担心"),
        ("stuck", "陷住"), ("mud", "泥"), ("pull", "拉"), ("everyone", "每人"),
        ("stadium", "体育场"), ("gym", "体育馆"), ("dining hall", "饭厅"), ("grass", "草坪"),
        ("gymnasium", "体育馆"), ("cycling", "骑自行车运动"), ("go cycling", "去骑自行车"), ("ice-skate", "滑冰"),
        ("badminton", "羽毛球运动"), ("star", "星"), ("easy", "容易的"), ("look up", "查阅"),
        ("Internet", "互联网"), ("different", "不同的"), ("active", "积极的"), ("race", "赛跑"),
        ("nothing", "没有什么"), ("thought", "想"), ("felt", "感觉"), ("cheetah", "猎豹"),
        ("trip", "绊倒"), ("woke", "醒"), ("dream", "梦"), ("yesterday", "昨天")
    ]
}

async def generate_audio(word, output_path):
    """使用 Edge TTS 生成单个单词的音频"""
    try:
        # 使用美国英语女声
        voice = "en-US-AriaNeural"
        communicate = edge_tts.Communicate(word, voice)
        await communicate.save(str(output_path))
        print(f"[OK] Generated: {word}")
        return True
    except Exception as e:
        print(f"[FAIL] Failed: {word} - {e}")
        return False

async def main():
    """主函数：批量生成所有音频"""
    # 创建音频目录
    AUDIO_DIR.mkdir(exist_ok=True)
    
    # 统计
    total = 0
    success = 0
    failed = []
    
    # 按年级生成
    for grade, words in VOCABULARY.items():
        grade_dir = AUDIO_DIR / f"grade{grade}"
        grade_dir.mkdir(exist_ok=True)
        
        print(f"\n=== Grade {grade} ({len(words)} words) ===")
        
        for word, meaning in words:
            total += 1
            # 文件名：小写，空格替换为下划线
            filename = word.lower().replace(" ", "_") + ".mp3"
            output_path = grade_dir / filename
            
            # 如果已存在则跳过
            if output_path.exists():
                print(f"  [SKIP] {word} (exists)")
                success += 1
                continue
            
            # 生成音频
            if await generate_audio(word, output_path):
                success += 1
            else:
                failed.append((grade, word))
            
            # 短暂延迟，避免请求过快
            await asyncio.sleep(0.3)
    
    # 输出统计
    print(f"\n=== Summary ===")
    print(f"Total: {total}")
    print(f"Success: {success}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed words:")
        for grade, word in failed:
            print(f"  Grade {grade}: {word}")

if __name__ == "__main__":
    asyncio.run(main())
