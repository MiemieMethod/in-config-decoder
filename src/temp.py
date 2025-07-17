import os
import json
import csv


I_N_DATA_PATH = r'D:\工作区\I-N-Data' # change here to your path
PATH = os.path.join(I_N_DATA_PATH, r'X6Game/Content/config_output')

minor_types = {
    101: "钻石",
    102: "金币",
    103: "银币",
    104: "经验",
    105: "能量点",
    106: "体力",
    107: "紫币",
    108: "月亮",
    109: "风散花种体力",
    110: "声望",
    111: "共鸣货币",
    112: "充值货币",
    113: "家园币",
    114: "家园经验",
    115: "奇迹之冠货币",
    116: "奇想气球",
    117: "焰光结晶",
    210: "发型",
    220: "外套",
    230: "上衣",
    241: "裤子",
    242: "裙子",
    250: "袜子",
    260: "鞋子",
    270: "臂饰",
    271: "发饰",
    272: "帽子",
    273: "耳饰",
    274: "颈饰",
    275: "腕饰",
    276: "项圈",
    277: "手套",
    278: "手持物",
    279: "特殊",
    280: "全妆",
    281: "底妆",
    282: "眉妆",
    283: "睫毛",
    284: "美瞳",
    285: "唇妆",
    286: "肤色",
    290: "连衣裙",
    291: "换装场景",
    292: "面饰",
    293: "胸饰",
    294: "挂饰",
    295: "背饰",
    296: "戒指",
    299: "套装",
    301: "任务道具",
    302: "书信",
    401: "投掷物",
    402: "刀剑",
    403: "弓箭",
    404: "法杖",
    405: "特殊工具",
    406: "食物",
    407: "经验道具",
    408: "温度消耗道具",
    409: "鱼类",
    410: "凭证",
    411: "共鸣消耗",
    412: "心得",
    501: "宝箱",
    502: "钥匙",
    503: "多选一宝箱",
    601: "称号",
    701: "头像",
    702: "头像框",
    704: "名片",
    705: "成就徽章",
    801: "语音",
    901: "拍照动作",
    902: "拍照滤镜",
    903: "拍照光照",
    904: "相机升级包",
    1001: "背包",
    1002: "好友数量",
    1101: "制作材料",
    1102: "设计图纸",
    1103: "采集副产物",
    1104: "普通怪物材料",
    1105: "中型Boss材料",
    1106: "世界Boss材料",
    1107: "留香喷雾材料",
    1108: "护发精油材料",
    1109: "护手香粉材料",
    1110: "进化材料",
    1111: "服装升级材料",
    1112: "奇迹套装制作材料",
    1201: "衣灵",
    1202: "升级材料",
    1203: "突破材料",
    1204: "衣灵装备",
    1205: "衣灵武器",
    1206: "衣灵皮肤",
    1207: "衣灵装备升级材料",
    1301: "特效球",
    1302: "特效球升级材料",
    1303: "特效球头部",
    1304: "特效球手部",
    1305: "特效球脚部",
    1401: "无限之心突破材料",
    1500: "体力回复道具",
    1610: "大喵斗篷",
    1700: "家具",
    1800: "留香喷雾",
    1801: "护发精油",
    1802: "护手香粉",
    1900: "留香喷雾设计图",
    1901: "护发精油设计图",
    1902: "护手香粉设计图",
    2003: "初级徽章",
    2004: "中级徽章",
    2005: "高级徽章",
    2100: "战斗道具",
    2103: "换装糖",
    2104: "美妆瓶",
    2200: "月卡",
    2201: "周卡",
    2202: "BP卡",
    2301: "通用自选",
    2501: "烟花弹",
    2601: "烟花弹设计图"
}

props = {
    None: "无",
    0: "典雅",
    1: "清新",
    2: "甜美",
    3: "性感",
    4: "帅气",
    5: "优雅",
    6: "清纯",
    7: "简约",
    8: "清凉",
    9: "保暖",
}

if __name__ == '__main__':
    with open( r'cfg/config_output/item/TbItem.json', 'r', encoding='utf-8') as f:
        item_table = json.load(f)
    with open( r'cfg/config_output/item/TbItemExtra.json', 'r', encoding='utf-8') as f:
        item_extra_table = json.load(f)
    with open( r'cfg/config_output/magic_ball/TbMagicBallInfo.json', 'r', encoding='utf-8') as f:
        magic_ball_table = json.load(f)
    with open( r'cfg/config_output/clothes/TbSuit.json', 'r', encoding='utf-8') as f:
        suits_table = json.load(f)

    with open( r'cfg/config_output/item/TbDisplayTypeInfo.json', 'r', encoding='utf-8') as f:
        display_type_table = json.load(f)
    with open( r'cfg/config_output/clothes/TbClothersTagInfo.json', 'r', encoding='utf-8') as f:
        tags = json.load(f)

    with open( r'cfg/pieces.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'quality', 'minor_type', 'display', 'major_style', 'minor_style', 'elegant', 'fresh', 'sweet', 'sexy', 'cool', 'tags', 'desc'])
        for item_id, item in item_table.items():
            if item['major_type'] != 2:
                continue
            extra = item_extra_table.get(item_id, {})

            show_tags = []
            for tag in extra['clothers_tags']:
                show_tags.append(tags[str(tag)]['show_name'])
            writer.writerow([item_id, item['name'], extra['clothers_quality'], minor_types[item['minor_type']], display_type_table[str(item['display_type'])]['displaytype_name'], props[extra['major_prop']], props[extra['minor_prop']], extra['cloth_props'][0], extra['cloth_props'][1], extra['cloth_props'][2], extra['cloth_props'][3], extra['cloth_props'][4], ';'.join(show_tags), item['desc']])

    with open( r'cfg/magic_ball.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'desc'])
        for item_id, item in magic_ball_table.items():
            _item = item_table.get(str(item_id), {})
            writer.writerow([item_id, _item['name'], _item['desc']])

    with open( r'cfg/suits.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'desc'])
        for item_id, item in suits_table.items():
            show_parts = []
            for part in item['components']:
                show_parts.append(item_table[str(part)]['name'])
            writer.writerow([item_id, item['suit_name'], item['quality'], props[item['clothers_prop']], ';'.join(show_parts), item['describe']])

    text = ''
    for id, name in minor_types.items():
        if id > 200 and id < 300:
            text += f'\t{name}'
    text += '\n'
    for id, name in minor_types.items():
        if id > 200 and id < 300:
            text += f'\t=FILTER(B:B, D:D="{name}")'
    print(text)