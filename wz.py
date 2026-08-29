import streamlit as st
import datetime
from bili_style import inject_css
from ui import get_img_src, render_cards, render_footer

# 1. 页面配置：强制浅色主题，无论浏览器/系统偏好如何都不会变成深色
st.set_page_config(
    page_title="bili娘站",
    page_icon="B",
    layout="wide",
    theme={
        "base": "light",
        "primaryColor": "#00A1D6",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F4F5F7",
        "textColor": "#18191C",
    },
)


# 2. CSS 样式设置（含隐藏 Streamlit 默认外壳）
inject_css()


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
from bili_data_a import bili_girls_part as _girls_a
from bili_data_b import bili_girls_part as _girls_b
bili_girls = _girls_a + _girls_b


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


# 5. 渲染卡片
render_cards(bili_girls, search_query)

# 6. 底部作者信息栏
render_footer()