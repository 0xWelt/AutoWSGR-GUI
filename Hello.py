import streamlit as st

# ==================== 页面信息 ====================
st.set_page_config(
    page_title="AutoWSGR",
    page_icon="👋",
)


# ==================== 边栏 ====================
# with st.sidebar:
#     st.success("选择一项功能")


# ==================== 正文 ====================
st.write("# 欢迎来到 WSGR 控制台! 👋")
st.write("👈 请在左侧选择功能")
with open("Hello.md", "r", encoding="utf-8") as f:
    readme = f.read()
st.markdown(readme)
