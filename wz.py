import streamlit as st
import os
import base64
import datetime

# 1. 页面配置
st.set_page_config(page_title="bili娘站", page_icon="B", layout="wide")


# 解析本地图片或网络图片 URL
def get_img_src(path_or_url):
    if not path_or_url or not path_or_url.strip():
        return None
    if path_or_url.startswith(("https://", "https://")):
        return path_or_url
    if os.path.exists(path_or_url):
        ext = path_or_url.split(".")[-1].lower()
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        with open(path_or_url, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{encoded}"
    # 部署后备：读取同目录下 <文件名>.b64 文本（图片以 base64 文本形式随仓库分发）
    b64_path = path_or_url + ".b64"
    if os.path.exists(b64_path):
        ext = path_or_url.split(".")[-1].lower()
        mime = "image/jpeg" if ext in ["jpg", "jpeg"] else "image/png"
        try:
            with open(b64_path, "r") as f:
                return f"data:{mime};base64,{f.read().strip()}"
        except Exception:
            pass
    return None


# 解析文本（支持直接文字 或 .txt 文件路径）
def get_desc_text(desc_or_path):
    if not desc_or_path or not str(desc_or_path).strip():
        return "暂无详细介绍信息。"
    # 如果填的是 txt 文件名并且本地存在，则读取文件内容
    if str(desc_or_path).endswith(".txt") and os.path.exists(desc_or_path):
        try:
            with open(desc_or_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            pass
    return str(desc_or_path)


# 2. CSS 样式设置
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    /* 强制增加 st.dialog 弹窗的宽度 */
    div[data-testid="stDialog"] > div {
        max-width: 80vw !important;  /* 80vw 表示占屏幕宽度的 80%，可按需调整（如 85vw 或 1200px） */
        width: 80vw !important;
}
    .bili-logo {
        color: #00A1D6; font-size: 28px; font-weight: 900;
        font-family: "SimHei", "Heiti SC", "Microsoft YaHei", sans-serif;
        line-height: 40px; user-select: none;
    }
    div[data-testid="stTextInput"] > label { display: none; }
    /* 1. 压低弹窗顶部的默认上边距 (Padding) */
    div[data-testid="stDialog"] > div > div:first-child {
        padding-top: 10px !important;
}

    /* 2. 让弹窗标题 "bili娘详情" 和关闭按钮的下边距变小 */
    div[data-testid="stDialog"] h2 {
        margin-bottom: 0px !important;
        padding-bottom: 0px !important;
}

    /* 基础卡片样式 */
    .bili-sq-card {
        width: 100%; aspect-ratio: 1 / 1.05; background-color: #FFFFFF;
        border-radius: 12px; overflow: hidden;
        display: flex; flex-direction: column; margin-bottom: 8px;
        transition: all 0.2s ease-in-out;
    }

    /* B站蓝普通边框 */
    .bili-card-blue {
        border: 1px solid #00A1D6;
        box-shadow: 0 2px 8px rgba(0, 161, 214, 0.08);
    }
    .bili-card-blue:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 16px rgba(0, 161, 214, 0.25);
    }

    /* 22和33重点标记：B站粉加粗边框 */
    .bili-card-pink {
        border: 2px solid #FF6699;
        box-shadow: 0 2px 10px rgba(255, 102, 153, 0.2);
    }
    .bili-card-pink:hover {
        transform: translateY(-4px);
        box-shadow: 0 6px 18px rgba(255, 102, 153, 0.4);
    }

    .bili-card-img-box {
        height: 70%; width: 100%; background-color: #F4F5F7;
        display: flex; align-items: center; justify-content: center;
        overflow: hidden; text-align: center; padding: 6px; box-sizing: border-box;
    }
    .bili-card-img-box img { width: 100%; height: 100%; object-fit: cover; }
    .bili-card-placeholder-text {
        font-size: 12px; color: #9499A0; font-weight: bold; line-height: 1.4; user-select: none;
    }
    .bili-card-info-box {
        height: 30%; width: 100%; background-color: #FFFFFF;
        display: flex; align-items: center; justify-content: space-between;
        padding: 6px 12px; border-top: 1px solid #F1F2F3; box-sizing: border-box;
    }
    .bili-no-text { color: #00A1D6; font-size: 15px; font-weight: 800; font-family: monospace; }
    .bili-detail-box { text-align: right; display: flex; flex-direction: column; justify-content: center; }
    .bili-name-text { color: #18191C; font-size: 13px; font-weight: bold; line-height: 1.2; }
    .bili-vote-text { color: #9499A0; font-size: 11px; margin-top: 2px; }

    /* 详情弹窗自定义 CSS */
    .modal-header {
        display: flex; justify-content: space-between; align-items: center;
        padding-bottom: 10px; border-bottom: 1px solid #E3E5E7; margin-bottom: 15px;
    }
    .modal-title {
        font-size: 20px; font-weight: bold; color: #00A1D6;
    }
    .modal-divider {
        border-right: 1px solid #E3E5E7; height: 100%; min-height: 320px;
    }
    .img-caption {
        text-align: center; font-size: 12px; color: #61666D; margin-top: 4px; margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 顶部导航栏
col_logo, col_search, col_right = st.columns([1.2, 4, 1.2])
with col_logo:
    st.markdown('<div class="bili-logo">bili娘</div>', unsafe_allow_html=True)
with col_search:
    search_query = st.text_input(label="搜索框", placeholder="请输入bili娘的编号或名称（1~73)", key="top_search")
with col_right:
    st.write("")

st.divider()

# =================【活动提示栏配置与渲染】=================
BANNER_MODE = "off"  # 模式: "off"(关闭), "on"(手动常开), "date"(仅指定日期), "datetime"(按时间段)
TARGET_DATE = (8, 16)
START_TIME = datetime.datetime(2026, 8, 16, 0, 0)
END_TIME = datetime.datetime(2026, 8, 18, 0, 0)

BANNER_TEXT = "🎉 2233生日快乐！哔哩哔哩(゜-゜)つロ干杯~-bilibili"
BANNER_IMG = ""
BANNER_BG_IMG = ""
BANNER_LINK = "https://www.bilibili.com/blackboard/era/2233birthdayweb.html"

BANNER_BG_COLOR = "#00AEEC"
BANNER_TEXT_COLOR = "#FF6699"
BANNER_BORDER_COLOR = "#FF6699"

show_banner = False
now = datetime.datetime.now()

if BANNER_MODE == "on":
    show_banner = True
elif BANNER_MODE == "date":
    if (now.month, now.day) == TARGET_DATE:
        show_banner = True
elif BANNER_MODE == "datetime":
    if START_TIME <= now <= END_TIME:
        show_banner = True

if show_banner:
    img_html = ""
    if BANNER_IMG and BANNER_IMG.strip():
        resolved_banner_img = get_img_src(BANNER_IMG) or BANNER_IMG
        img_html = f'<img src="{resolved_banner_img}" style="max-height: 40px; margin-right: 10px; border-radius: 4px; vertical-align: middle;" />'

    text_html = ""
    if BANNER_TEXT and BANNER_TEXT.strip():
        text_html = f'<span style="font-weight: bold; color: {BANNER_TEXT_COLOR}; vertical-align: middle;">{BANNER_TEXT}</span>'

    inner_content = f'{img_html}{text_html}'

    if BANNER_LINK and BANNER_LINK.strip():
        banner_body = f'<a href="{BANNER_LINK}" target="_blank" style="text-decoration: none; display: flex; align-items: center; justify-content: center; width: 100%;">{inner_content}</a>'
    else:
        banner_body = f'<div style="display: flex; align-items: center; justify-content: center; width: 100%;">{inner_content}</div>'

    bg_style = f"background-color: {BANNER_BG_COLOR};"
    if BANNER_BG_IMG and BANNER_BG_IMG.strip():
        resolved_bg = get_img_src(BANNER_BG_IMG) or BANNER_BG_IMG
        bg_style = f"background-image: url('{resolved_bg}'); background-size: cover; background-position: center;"

    st.markdown(f"""
        <div style="
            {bg_style}
            border: 1px solid {BANNER_BORDER_COLOR};
            border-radius: 8px;
            padding: 12px 15px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            {banner_body}
        </div>
    """, unsafe_allow_html=True)
# =========================================================

# 4. 73 个 bili娘 数据库
# 字段说明：
# id: 编号, name: 名字, img: 主卡片封面, votes: 得票数, desc: 详细文字介绍
# gallery: 图片列表，格式为 [{"url": "图片文件名或链接", "title": "自定义图片标题"}]
bili_girls = [
    {
        "id": "No.01",
        "name": "暂无",
        "designer": "船长No_2",
        "img": "",
        "votes": "3",
        "desc": """设定：
【bilibili娘】
身高160cm
40KG
B cup
内在能量型
正常人格和战斗人格
平时很大姐姐，惹恼了就会变修罗
待在家里当然最喜欢了
不喜欢别人在自己面前讨论兄贵，因为要自己一个人的时候才偷偷看""",
        "gallery": []
    },
    {
        "id": "No.02",
        "name":"暂无",
        "designer":"伪音姬XSK （3.0）",
        "img": "",
        "votes": "13",
        "desc":"""设定：
BL娘
称号：兄贵的大狂热
生日：7月29日（暂定）
星座：狮子座（当然跟着上面）
年龄：18（比AC娘小2年）
身高：163CM
体重：43KG
能力：使用静电什么的
性格：腹黑，并且经常会想得太多（和猫猫一样的好奇心大异想天开）。
特征：静电手环，能产生强大静电的围巾，藏着不少鱼干的小袍子
爱好：看兄贵摔交动作大片新日幕里
崇拜的偶像：“森之妖精”比利海灵顿，“加州州长”阿诺
擅长运动：果然还是摔交
喜欢的食物：鱼干，冻的东西
关系：AC娘（劲敌，但有爱慕之意），TD娘（情敌），NICO娘（憧憬的前辈），四次君（一辈子是好朋友），YC娘（一直想百合的对象）
人物背景：迟点再补充~~""",
    },
    {
        "id": "No.06",
        "name": "鹿瞳",
        "img": "",
        "votes": "暂未搜集",
        "desc": "鹿瞳的详细角色设定与介绍说明。",
        "gallery": [{"url": "", "title": "官方立绘"}]
    },
    {
        "id": "No.18",
        "name": "夭八",
        "img": "",
        "votes": "暂未收集",
        "desc": "夭八的详细角色设定与介绍说明。",
        "gallery": [{"url": "", "title": "形象设计图"}]
    },
    {
        "id": "No.22",
        "name": "22",
        "designer": "ハオ",
        "img": "22图.jpg",
        "votes": "1824",
        "desc": """22娘是哔哩哔哩的站娘之一，性格阳光、活泼、神经大条。作为姐姐，经常照顾33娘，但有时也会闹出笑话。
设定：
身长：162cm
体重：48kg
BWH: 无可奉告
星座: 天枰
能力: 使目标感电的能力
体质: 间歇性放电(危险度略高)
喜欢的事物: 当然是A.C.G啦
讨厌的事物: 审批什么的最讨厌了!""",
        "gallery": [
            {"url": "22图.jpg", "title": "22娘 经典主视觉"}
        ]
    },
    {
        "id": "No.33",
        "name": "33",
        "img": "",
        "votes": "1824",
        "desc": """33娘是哔哩哔哩的站娘之一，性格沉默寡言、面瘫、机智超群。作为妹妹，具备强大的计算能力与机娘属性。
身高:165CM
年龄:13-14岁左右
体重:200KG(望着某战斗娘...)
性格:无口属性,平常不爱说话,但是很喜欢和人类交流重口味的笑话,喜欢美式英语(粗口),无聊的时候会在视频上乱播.
爱好:啃插座/森之妖精/美式英语/无聊/发呆.
讨厌:电视以及其它品种的播放产品/严寒/啮齿动物/H.
能力:立体播放/模仿任何声音/流利的英文.
     看上去是个女孩子一样的机械,有着女孩的身体和音线.
     不过实际上身体却很沉重,爱好也很奇怪,而且会模仿更奇怪的声音,无聊的时候还会一边哼着小调一边播放粗口英语或者兄贵洗脑.
     以方便实用为理念开发的视听娘-bilibili,在各方面有着出色的成绩.
     全息立体播放以及远程操控,超长的使用时间以及人性化的功能.
     但不代表这是没缺陷的产品-比方说她爱啃插座之类的小型供电设施,因为里面带电的铜味会很吸引她.在就是很多播放产品都是她的敌人,会被她很流利的破坏掉-商品竞争嘛.在就是怕啮齿动物和严寒,虽然是机械,不过呢体温是有的-这样可以保持线路的耐久和零件的咬合正常.
     虽然不会有任何线啊什么的东西露在外面可以让老鼠拿来磨牙齿,但是设定是这样还是小心的点好-她是这样想的.
     设定上是全年龄向产品,所以不喜欢播放H.但是要求的话,还是会照办的,只是下次还要提醒她一次.因为是全年龄向的嘛.
     服装是完全可着脱的方便类型,当然在出厂的时候会穿着紧身服.如果没要求的话她就会穿上制服(这个制服我想让它简洁明快些,不过对裙子有点不满意就是了...),当然也可以是紧身服.因为是完全可着脱类型,所以可以换自己喜欢的衣服来满足一些制服爱好者.
     即使是太阳能充电的类型,不过在没有太阳的时候还是让她啃插座吧-这样也是可以充电的,或者咬电池什么的,只是准备的量要多些.
     因为是机械,所以表情会比较稀薄,但不代表她是个无感情的家伙.因为是"女孩子'所以让她做些奇怪的事-戴猫耳或者穿女仆装什么的她也会害羞.只是表情很细微罢了,会通过头上的成像仪来弥补.
     不要因她喜欢说粗口就认为她是个坏孩子,毕竟她也不完全了解这些词汇的意思,只是把它们按照指令组合在一起然后播放罢了,不过她的数据库里也尽是这些,到底是谁的错呢...
     """,
        "gallery": [
            {"url": "", "title": "33娘 经典主视觉"},
            {"url": "", "title": "33娘 拜年纪设定图"}
        ]
    },
    {
        "id": "No.73",
        "name": "暂无",
        "img": "",
        "votes": "0 (迟到)",
        "desc": "迟到提交的作品。",
        "gallery": []
    }
]

# 补全其余未配置的编号，保证展示 73 个卡片
existing_ids = {g["id"] for g in bili_girls}
for i in range(1, 74):
    formatted_id = f"No.{i:02d}"
    if formatted_id not in existing_ids:
        bili_girls.append({
            "id": formatted_id,
            "name": "暂无",
            "img": "",
            "votes": "暂未搜集" if i != 73 else "0 (迟到)",
            "desc": "暂无详细介绍信息。",
            "gallery": []
        })

# 排序保证按 No.01 ~ No.73 顺序排列
bili_girls.sort(key=lambda x: x["id"])


# 5. 弹窗函数 (st.dialog)
@st.dialog("bili娘详情", width="large")
def show_bili_dialog(girl):
    # 顶部栏：名字、画师、编号、最终得票数（左侧多行）+ 返回键（右侧）
    col_t1, col_t2 = st.columns([5, 1])

    with col_t1:
        designer_name = girl.get("designer", "暂无")
        votes_count = girl.get("votes", "暂无")

        # 🌟 四行垂直排版：名字(上) -> 画师 -> 编号 -> 最终得票数(下)
        st.markdown(f"""
                <div style="line-height: 1.4; margin-top: -10px">
                    <div style="font-size: 22px; font-weight: bold; color: #00A1D6;">{girl['name']}</div>
                    <div style="font-size: 13px; color: #61666D;">原画师：{designer_name}</div>
                    <div style="font-size: 15px; font-weight: bold; color: #FF6699; font-family: monospace; margin-top: 2px;">{girl['id']}</div>
                    <div style="font-size: 13px; color: #9499A0;">最终得票数：<span style="color: #00A1D6; font-weight: bold;">{votes_count}</span></div>
                </div>
            """, unsafe_allow_html=True)

    with col_t2:
        if st.button("返回主页面", key="dialog_back_btn"):
            st.rerun()

    st.markdown("<hr style='margin: 10px 0 15px 0; border-color: #E3E5E7;'>", unsafe_allow_html=True)

    # 内容区域：左侧图片（可拉条），中间分隔，右侧文字介绍（可拉条）
    col_left, col_mid, col_right = st.columns([1, 0.05, 1])

    # 左侧：图片列表区
    with col_left:
        st.markdown("**形象展示**")
        with st.container(height=500):  # 限制高度，多图自动出现垂直拉条
            gallery = girl.get("gallery", [])
            if gallery:
                for img_item in gallery:
                    img_url = img_item.get("url", "")
                    img_title = img_item.get("title", "未命名图片")
                    resolved = get_img_src(img_url)

                    if resolved:
                        st.image(resolved, use_container_width=True)
                    else:
                        st.info("图片资料暂未搜集")

                    st.markdown(f"<div class='img-caption'>{img_title}</div>", unsafe_allow_html=True)
            else:
                # 默认显示封面图或占位
                resolved_main = get_img_src(girl["img"])
                if resolved_main:
                    st.image(resolved_main, use_container_width=True)
                    st.markdown(f"<div class='img-caption'>{girl['name']} 主视觉图</div>", unsafe_allow_html=True)
                else:
                    st.info("暂无更多图片资料")

    # 中间：细分隔线
    with col_mid:
        st.markdown("<div class='modal-divider'></div>", unsafe_allow_html=True)

    # 右侧：文字介绍区
    with col_right:
        st.markdown("**角色介绍**")
        with st.container(height=500):  # 限制高度，多字自动出现垂直拉条
            desc = get_desc_text(girl.get("desc"))

            # 保留换行并优化颜色与排版
            st.markdown(
                f'<div style="white-space: pre-line; line-height: 1.6; color: #18191C; font-size: 14px;">{desc}</div>',
                unsafe_allow_html=True
            )


# 6. 检索过滤
filtered_girls = [
    girl for girl in bili_girls
    if search_query.strip().lower() in girl["name"].lower() or search_query.strip() in girl["id"]
]

# 7. 5 列卡片渲染
if not filtered_girls:
    st.warning("未检索到对应的 bili娘！")
else:
    cols = st.columns(5)
    for idx, girl in enumerate(filtered_girls):
        with cols[idx % 5]:
            resolved_img = get_img_src(girl["img"])
            if resolved_img:
                img_content = f'<img src="{resolved_img}" alt="{girl["name"]}"/>'
            else:
                img_content = '<div class="bili-card-placeholder-text">图片资料暂未搜集</div>'

            is_highlight = girl["id"] in ["No.22", "No.33"] or girl["name"] in ["22", "33"]
            card_class = "bili-sq-card bili-card-pink" if is_highlight else "bili-sq-card bili-card-blue"

            # 渲染卡片
            st.markdown(f"""
                <div class="{card_class}">
                    <div class="bili-card-img-box">
                        {img_content}
                    </div>
                    <div class="bili-card-info-box">
                        <span class="bili-no-text">{girl['id']}</span>
                        <div class="bili-detail-box">
                            <span class="bili-name-text">{girl['name']}</span>
                            <span class="bili-vote-text">票数: {girl['votes']}</span>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # 点击查看详情按钮（触发弹窗）
            if st.button("查看详情", key=f"btn_{girl['id']}", use_container_width=True):
                show_bili_dialog(girl)

# 8. 底部作者信息栏
st.divider()

MY_NAME = "忆人摘星"
MY_SPACE_URL = "https://space.bilibili.com/3546929877224366"
MY_AVATAR_PATH = "忆人摘星头像.png"

resolved_my_avatar = get_img_src(MY_AVATAR_PATH) or "https://i0.hdslb.com/bfs/face/member/noface.jpg"

st.markdown(f"""
    <div style="text-align: center; padding: 15px 0 10px 0; color: #61666D; font-size: 14px;">
        <span>本网站作者为</span>
        <a href="{MY_SPACE_URL}" target="_blank" style="text-decoration: none;">
            <img src="{resolved_my_avatar}" style="width: 28px; height: 28px; border-radius: 50%; vertical-align: middle; margin: 0 6px; border: 1px solid #E3E5E7; object-fit: cover; cursor: pointer;">
        </a>
        <a href="{MY_SPACE_URL}" target="_blank" style="color: #00A1D6; font-weight: bold; text-decoration: none;" onmouseover="this.style.color='#FF6699'" onmouseout="this.style.color='#00A1D6'">
            {MY_NAME}
        </a>
    </div>
""", unsafe_allow_html=True)
