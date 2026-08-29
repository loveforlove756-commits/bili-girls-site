import streamlit as st
import datetime
from bili_style import inject_css
from ui import get_img_src, render_cards, render_footer
from bili_banner import render_banner

# 1. 页面配置
# 注意：新版 Streamlit 已从 set_page_config 移除 theme 参数，
# 强制浅色主题改由仓库根目录 .streamlit/config.toml 的 [theme] base="light" 控制。
st.set_page_config(
    page_title="bili娘站",
    page_icon="B",
    layout="wide",
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


# 4. 活动提示栏（默认关闭）
render_banner()


# 5. 73 个 bili娘 数据库
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


# 6. 渲染卡片
render_cards(bili_girls, search_query)

# 7. 底部作者信息栏
render_footer()
