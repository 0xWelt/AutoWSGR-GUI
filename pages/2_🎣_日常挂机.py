import streamlit as st
import os

from AutoWSGR.scripts.daily_api import DailyOperation

st.set_page_config(
    page_title="日常挂机",
    page_icon="🎣",
)
# st.sidebar.success("选择一项功能")


# @st.cache_resource
def get_daily_operation(setting_file):
    return DailyOperation(setting_file)

if st.button("开始运行"):
    st.balloons()
    operation = get_daily_operation("data/user_settings.yaml")
    operation.run()
