"""Reviewed clothing vocabulary. Longest phrases take precedence over single words."""
CATEGORIES = {
    "春": "春季", "夏": "夏季", "秋": "秋季", "冬": "冬季",
    "ランジェリー": "内衣", "パーティ": "派对礼服", "水着": "泳装", "セクシー": "性感服饰",
}

# kind: modifier / garment. Modifiers attach to the following garment; trailing
# modifiers remain visible because the upstream keyword list can be truncated.
WORDS = {
    "apron": ("围裙", "garment"), "bag": ("手袋", "garment"), "beanie": ("针织帽", "garment"),
    "beige": ("米色", "modifier"), "belt": ("腰带", "garment"), "beret": ("贝雷帽", "garment"),
    "black": ("黑色", "modifier"), "blouse": ("女式衬衫", "garment"), "blue": ("蓝色", "modifier"),
    "boots": ("靴子", "garment"), "bra": ("文胸", "garment"), "briefs": ("内裤", "garment"),
    "brown": ("棕色", "modifier"), "burgundy": ("酒红色", "modifier"), "camisole": ("吊带衫", "garment"),
    "cardigan": ("开衫", "garment"), "chiffon": ("雪纺", "modifier"), "choker": ("颈链", "garment"),
    "coat": ("大衣", "garment"), "corduroy": ("灯芯绒", "modifier"), "corset": ("束身衣", "garment"),
    "cream": ("奶油色", "modifier"), "denim": ("牛仔", "modifier"), "dress": ("连衣裙", "garment"),
    "floral": ("碎花", "modifier"), "frill": ("荷叶边", "modifier"), "fur": ("毛绒", "modifier"),
    "gloves": ("手套", "garment"), "gold": ("金色", "modifier"), "green": ("绿色", "modifier"),
    "grey": ("灰色", "modifier"), "hat": ("帽子", "garment"), "headband": ("发带", "garment"),
    "heels": ("高跟鞋", "garment"), "hoodie": ("连帽卫衣", "garment"), "ivory": ("象牙白", "modifier"),
    "jacket": ("夹克", "garment"), "jeans": ("牛仔裤", "garment"), "khaki": ("卡其色", "modifier"),
    "knit": ("针织衫", "garment"), "lace": ("蕾丝", "modifier"), "lavender": ("薰衣草紫", "modifier"),
    "leather": ("皮革", "modifier"), "loafers": ("乐福鞋", "garment"), "maxi": ("及踝", "modifier"),
    "mesh": ("网纱", "modifier"), "midi": ("中长款", "modifier"), "mini": ("迷你", "modifier"),
    "mint": ("薄荷色", "modifier"), "muffler": ("围巾", "garment"), "navy": ("藏蓝色", "modifier"),
    "necklace": ("项链", "garment"), "olive": ("橄榄绿", "modifier"), "orange": ("橙色", "modifier"),
    "pants": ("长裤", "garment"), "pink": ("粉色", "modifier"), "pleated": ("百褶", "modifier"),
    "polka-dot": ("波点", "modifier"), "pumps": ("浅口高跟鞋", "garment"), "purple": ("紫色", "modifier"),
    "red": ("红色", "modifier"), "ribbon": ("蝴蝶结", "garment"), "robe": ("睡袍", "garment"),
    "sandals": ("凉鞋", "garment"), "satin": ("缎面", "modifier"), "scarf": ("丝巾", "garment"),
    "shirt": ("衬衫", "garment"), "shorts": ("短裤", "garment"), "silver": ("银色", "modifier"),
    "skirt": ("半身裙", "garment"), "sneakers": ("运动鞋", "garment"), "socks": ("短袜", "garment"),
    "stockings": ("长筒袜", "garment"), "suede": ("麂皮", "modifier"), "sunglasses": ("太阳镜", "garment"),
    "sweater": ("毛衣", "garment"), "swimsuit": ("泳衣", "garment"), "tights": ("连裤袜", "garment"),
    "tote": ("托特包", "garment"), "tulle": ("薄纱", "modifier"), "turtleneck": ("高领衫", "garment"),
    "velvet": ("天鹅绒", "modifier"), "vest": ("马甲", "garment"), "white": ("白色", "modifier"),
    "wool": ("羊毛", "modifier"), "yellow": ("黄色", "modifier"),
}

PHRASES = {
    "mint green": ("薄荷绿", "modifier"),
    "knit cardigan": ("针织开衫", "garment"), "knit dress": ("针织连衣裙", "garment"),
    "knit vest": ("针织马甲", "garment"), "knit skirt": ("针织半身裙", "garment"),
    "mini skirt shorts": ("迷你裙裤", "garment"), "mini skirt": ("迷你半身裙", "garment"),
    "midi skirt": ("中长半身裙", "garment"), "maxi skirt": ("及踝长裙", "garment"),
    "mini dress": ("迷你连衣裙", "garment"), "midi dress": ("中长连衣裙", "garment"),
    "maxi dress": ("及踝连衣裙", "garment"), "shirt dress": ("衬衫裙", "garment"),
    "corset dress": ("束身连衣裙", "garment"), "ribbon shirt dress": ("蝴蝶结衬衫裙", "garment"),
    "ribbon chiffon camisole": ("蝴蝶结雪纺吊带衫", "garment"),
    "lace camisole": ("蕾丝吊带衫", "garment"), "floral camisole": ("碎花吊带衫", "garment"),
    "ribbon bag": ("蝴蝶结手袋", "garment"), "mini ribbon bag": ("迷你蝴蝶结手袋", "garment"),
    "mini tote": ("迷你托特包", "garment"), "mini bag": ("迷你手袋", "garment"),
    "satin ribbon": ("缎带", "garment"), "ribbon choker": ("蝴蝶结颈链", "garment"),
    "ribbon necklace": ("蝴蝶结项链", "garment"), "ribbon headband": ("蝴蝶结发带", "garment"),
    "ribbon blouse": ("蝴蝶结女式衬衫", "garment"), "ribbon bra": ("蝴蝶结文胸", "garment"),
    "denim pants": ("牛仔裤", "garment"), "denim shorts": ("牛仔短裤", "garment"),
    "denim jacket": ("牛仔夹克", "garment"), "fur coat": ("毛绒大衣", "garment"),
}


def translate_keywords(text):
    tokens = text.lower().split()
    parts, pending, index = [], "", 0
    while index < len(tokens):
        length = 1
        key = tokens[index]
        for count in range(min(4, len(tokens) - index), 1, -1):
            phrase = " ".join(tokens[index:index + count])
            if phrase in PHRASES:
                key, length = phrase, count
                break
        translation, kind = PHRASES[key] if key in PHRASES else WORDS[key]
        pending += translation
        if kind == "garment":
            parts.append(pending)
            pending = ""
        index += length
    if pending:
        parts.append(pending)
    return parts
