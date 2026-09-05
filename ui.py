import streamlit as st
import os
import base64


# 解析本地图片或网络图片 URL
def get_img_src(path_or_url):
    if not path_or_url or not path_or_url.strip():
        return None
    if path_or_url.startswith(("https://", "http://")):
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


def render_cards(bili_girls, search_query):
    # 延迟导入，避免与 bili_dialog 形成循环依赖
    from bili_dialog import show_bili_dialog

    # 检索过滤
    filtered_girls = [
        girl for girl in bili_girls
        if search_query.strip().lower() in girl["name"].lower() or search_query.strip() in girl["id"]
    ]

    # 5 列卡片渲染
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


def render_footer():
    # 底部作者信息栏
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
        <div style="text-align: center; padding: 4px 0 15px 0; color: #61666D; font-size: 14px;">
            <span>更多内容详见</span><a href="https://www.bilibili.com/read/readlist/rl687141" target="_blank" style="color: #00A1D6; font-weight: bold; text-decoration: none;" onmouseover="this.style.color='#FF6699'" onmouseout="this.style.color='#00A1D6'">https://www.bilibili.com/read/readlist/rl687141</a>
        </div>
    """, unsafe_allow_html=True)