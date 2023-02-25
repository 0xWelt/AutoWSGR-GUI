import streamlit as st
import os

from AutoWSGR.scripts.daily_api import DailyOperation

st.set_page_config(
    page_title="日常挂机",
    page_icon="🎣",
)
# st.sidebar.success("选择一项功能")

if st.button("开始运行"):
    st.balloons()
    # 指定采用本地设置
    
    operation = DailyOperation("data/user_settings.yaml")
    operation.run()
