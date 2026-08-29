import streamlit as st
import datetime
from ui import get_img_src


def render_banner():
    # =================【活动提示栏配置】=================
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
    # ====================================================

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
