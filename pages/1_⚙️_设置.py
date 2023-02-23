import copy
import streamlit as st
import yaml
import os
import shutil
from utils.streamlit_wrapper import w_selectbox, w_checkbox, w_number_input, w_text_input, del_button, w_multiselect
import pandas as pd

st.set_page_config(
    page_title="设置",
    page_icon="⚙️",
)
# st.sidebar.success("选择一项功能")
st.write("# 修改设置需要重新运行 👋")


# 进行初始化，以及读取配置文件
@st.cache_resource
def load_data():
    # 拷贝模板到data目录
    for root, dirs, files in os.walk("data_template"):
        for name in files:
            src_file = os.path.join(root, name)
            dst_file = src_file.replace("data_template", "data")

            # 无覆盖拷贝
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            if not os.path.exists(dst_file):
                shutil.copy(src_file, dst_file)

    # 加载用户当前设置
    with open("data/user_settings.yaml", "r", encoding="utf-8") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    with open("data/ship_names.yaml", "r", encoding="utf-8") as f:
        config["SHIP_NAME_PATH"] = "data/ship_names.yaml"
        ship_name = yaml.load(f, Loader=yaml.FullLoader)

    all_plans = {}
    for root, dirs, files in os.walk("data/plans"):
        for name in files:
            with open(os.path.join(root, name), "r", encoding="utf-8") as f:
                key_name = os.path.basename(root) + '/' + \
                    name.split(".")[0] if os.path.basename(root) != 'plans' else name.split(".")[0]
                all_plans[key_name] = yaml.load(f, Loader=yaml.FullLoader)

    return config, ship_name, all_plans


# 保存配置文件
def save_data(config, ship_name, all_plans):
    with open("data/user_settings.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True)
    with open("data/ship_names.yaml", "w", encoding="utf-8") as f:
        yaml.dump(ship_name, f, allow_unicode=True)

    for key in all_plans.keys():
        with open("data/plans/" + key + ".yaml", "w", encoding="utf-8") as f:
            yaml.dump(all_plans[key], f, allow_unicode=True)


config, ship_name, all_plans = load_data()

# 修改设置
with st.expander("模拟器设置", False):
    c = config["emulator"]
    w_selectbox("模拟器类型", ["雷电", "蓝叠 Hyper-V"], c, "type")
    w_text_input("模拟器路径", c, "start_cmd")
    if c["type"] == "蓝叠 Hyper-V":
        w_text_input("模拟器设置文件（仅蓝叠需要）", c, "config_file")

# with st.expander("自定义舰船名称", False):
#     st.text("暂未实现GUI，请在data/ship_names.yaml中修改")

with st.expander("出征计划库", True):
    st.info("配置自定义计划，等价于直接修改data/plans下的文件", icon="ℹ️")
    # st.write("### 全局默认值")
    # all_plans["default"]
    tabs = st.tabs(["战役", "常规战"])
    # with tabs[0]:
    #     choice = st.selectbox("选择战役", [i.split('/')[1] for i in all_plans.keys() if i.startswith("battle")])
    #     cols = st.columns([1, 1, 4])
    #     with cols[0]:
    #         w_selectbox("阵型", ["单纵", "复纵", "轮型", "梯形", "单横"], all_plans["battle/"+choice]["node_args"], "formation")
    #     with cols[1]:
    #         w_selectbox("夜战", [True, False], all_plans["battle/"+choice]["node_args"], "night")
    #     with cols[2]:
    #         w_text_input("维修方案（1中破，2大破。或单独指定6个位置，英文,隔开）", all_plans["battle/"+choice], "repair_mode")


    with tabs[1]:
        cols = st.columns([1, 3])
        with cols[0]:
            choice = st.selectbox("选择常规战", [i.split('/')[1] for i in all_plans.keys() if i.startswith("normal_fight")])
        with cols[1]:
            w_multiselect("选中节点", [chr(ord('A')+i) for i in range(16)], all_plans["normal_fight/"+choice], "selected_nodes")

        cols = st.columns([1, 1, 4])
        with cols[0]:
            w_selectbox("阵型", ["单纵", "复纵", "轮型", "梯形", "单横"], all_plans["normal_fight/"+choice]["node_args"], "formation")
        with cols[1]:
            w_selectbox("夜战", [True, False], all_plans["normal_fight/"+choice]["node_args"], "night")
        with cols[2]:
            w_text_input("维修方案（1中破，2大破。或单独指定6个位置，英文,隔开）", all_plans["normal_fight/"+choice], "repair_mode")


with st.expander("自动挂机设置", True):
    c = config["daily_automation"]
    w_checkbox("重复远征", c, "auto_expedition")
    w_checkbox("自动点击完成任务", c, "auto_gain_bonus")
    w_checkbox("空闲时澡堂修理", c, "auto_bath_repair")

    w_checkbox("船坞已满时全部分解，若设置为false则终止战斗", c, "dock_full_destroy")

    cols = st.columns([1, 1, 2])
    with cols[0]:
        w_checkbox("完成每日战役", c, "auto_battle")
    if c["auto_battle"]:
        with cols[1]:
            w_selectbox("战役选择", ["困难驱逐", "困难巡洋", "困难战列", "困难航母", "困难潜艇"], c, "battle_type")

    cols = st.columns([1, 1, 2])
    with cols[0]:
        w_checkbox("进行自动出征", c, "auto_normal_fight")
    with cols[1]:
        if st.button("添加"):
            c["normal_fight_tasks"].append(["", 1, 0])
    if c["auto_normal_fight"]:
        # cols = st.columns(4)
        # cols[0].write("任务")
        # cols[1].write("舰队")
        # cols[2].write("出征次数")

        if len(c["normal_fight_tasks"]) >= 0:
            for id in range(len(c["normal_fight_tasks"])):
                task = c["normal_fight_tasks"][id]
                cols = st.columns(4)
                with cols[0]:
                    w_text_input("任务", task, 0, f"任务{id}")
                with cols[1]:
                    w_number_input("舰队", task, 1, f"舰队{id}", min_value=1, max_value=4)
                with cols[2]:
                    w_number_input("出征次数", task, 2, f"出征次数{id}", min_value=0)
                with cols[3]:
                    del_button("删除", c["normal_fight_tasks"], id)


# save_data(config, ship_name, all_plans)
