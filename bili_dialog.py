import streamlit as st
from ui import get_img_src, get_desc_text


@st.dialog("bili娘详情", width="large")
def show_bili_dialog(girl):
    # 顶部栏：名字、画师、编号、最终得票数（左侧多行）+ 返回键（右侧）
    col_t1, col_t2 = st.columns([5, 1])

    with col_t1:
        designer_name = girl.get("designer", "暂无")
        votes_count = girl.get("votes", "暂无")

        # 四行垂直排版：名字(上) -> 画师 -> 编号 -> 最终得票数(下)
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
        with st.container(height=500):
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
        with st.container(height=500):
            desc = get_desc_text(girl.get("desc"))

            # 保留换行并优化颜色与排版
            st.markdown(
                f'<div style="white-space: pre-line; line-height: 1.6; color: #18191C; font-size: 14px;">{desc}</div>',
                unsafe_allow_html=True
            )