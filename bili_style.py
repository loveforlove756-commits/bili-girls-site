import streamlit as st


def inject_css():
    """注入全局 CSS：强制浅色外壳、隐藏 Streamlit 默认顶栏/底标、卡片与弹窗样式。"""
    st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    /* 隐藏 Streamlit 默认外壳：顶栏（含登录头像）、底部 Made with Streamlit 标、状态/工具栏 */
    header[data-testid="stHeader"] { display: none !important; }
    footer[data-testid="stFooter"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stStatusWidget"] { display: none !important; }
    /* 隐藏顶栏后压缩主容器顶部留白，让内容整体上移（不影响弹窗） */
    .stApp > header { display: none !important; }
    [data-testid="stMainBlockContainer"], .block-container { padding-top: 1.85rem !important; }
    .stMain > div { padding-top: 0 !important; }
    /* 强制增加 st.dialog 弹窗的宽度 */
    div[data-testid="stDialog"] > div {
        max-width: 80vw !important;
        width: 80vw !important;
    }
    .bili-logo {
        color: #00A1D6; font-size: 28px; font-weight: 900;
        font-family: "SimHei", "Heiti SC", "Microsoft YaHei", sans-serif;
        line-height: 40px; user-select: none;
    }
    div[data-testid="stTextInput"] > label { display: none; }
    /* 压低弹窗顶部默认上边距 */
    div[data-testid="stDialog"] > div > div:first-child {
        padding-top: 10px !important;
    }
    /* 弹窗标题与关闭按钮下边距缩小 */
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
