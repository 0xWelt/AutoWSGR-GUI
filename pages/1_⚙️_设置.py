import streamlit as st
import yaml
import os
import shutil
from utils.streamlit_wrapper import *


st.set_page_config(
    page_title="设置",
    page_icon="⚙️",
)
st.write("# 修改设置 ⚙️")
st.info("用户设置全部在data/下，不想用GUI可以直接改文件", icon="ℹ️")
st.info("修改设置后，为保证稳定建议重启GUI再执行挂机等功能", icon="ℹ️")
st.error("所有修改实时保存，不能撤回！测试版bug颇多，保险起见建议经常备份data/文件夹！", icon="🚨")
st.warning("如果GUI崩溃，请关闭GUI并手动修改文件来尝试恢复，并反馈bug", icon="🚨")


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

    # 不存在的plan删掉（改名或删除）
    for root, dirs, files in os.walk("data/plans"):
        for name in files:
            key_name = os.path.basename(root) + '/' + \
                name.split(".")[0] if os.path.basename(root) != 'plans' else name.split(".")[0]
            if key_name not in all_plans.keys():
                file_path = os.path.join(root, name)
                os.remove(file_path)

    # 存在的plan保存（覆盖或新增）
    for key in all_plans.keys():
        with open("data/plans/" + key + ".yaml", "w", encoding="utf-8") as f:
            yaml.dump(all_plans[key], f, allow_unicode=True)


config, ship_name, all_plans = load_data()

# 修改设置
with st.expander("模拟器设置", False):
    c = config["emulator"]
    selectbox("模拟器类型", ["雷电", "蓝叠 Hyper-V"], c, "type")
    text_input("模拟器路径", c, "start_cmd")
    if c["type"] == "蓝叠 Hyper-V":
        text_input("模拟器设置文件（仅蓝叠需要）", c, "config_file")

# with st.expander("自定义舰船名称", False):
#     st.text("暂未实现GUI，请在data/ship_names.yaml中修改")

with st.expander("出征计划库", False):
    st.markdown("> 配置说明")
    st.caption("""1. 配置优先级：当直接编辑配置文件时，节点设置 > 地图默认 > 全局默认。当采用GUI时，默认值不起效，节点需要设置齐全。目前暂未想到较好的用UI设置默认值的格式，如果你有想法欢迎反馈。""")
    st.caption("""2. 维修方案：1代表中破就修，2代表大破才修。支持两种指定方式，直接指定一个数字代表所有位置都按这个条件修理，指定一个长度为6的列表（用 **英文逗号**隔开的6个数字）可单独设置每个位置的修理条件。""")
    st.caption("""3. 节点设置：(1) 所有选项只有**存在时**起效，设置了不存在的选项（迂回、战况等）不会有影响。(2) 前进：打完这个点后是否前进，脚本不知道下一个点是不是你要打的点，只能在走到超出选中节点列表时SL。所以如果知道一个点是一次出征的终点，选择不前进可直接返港节约时间。""")

    tabs = st.tabs(["战役", "常规战"])
    with tabs[0]:
        tag = "战役"
        cols = st.columns([1, 4])
        with cols[0]:
            choice = st.selectbox("选择战役", [i.split('/')[1] for i in all_plans if i.startswith("battle")])

        cols = st.columns([1, 1, 4])
        with cols[0]:
            selectbox("阵型", ["单纵", "复纵", "轮型", "梯形", "单横"], all_plans["battle/"+choice]
                        ["node_args"], "formation",  tag, True)
        with cols[1]:
            selectbox("夜战", [True, False], all_plans["battle/"+choice]["node_args"], "night", tag)
        with cols[2]:
            text_input("维修方案", all_plans["battle/"+choice], "repair_mode", tag)

    with tabs[1]:
        tag = "常规战"
        # 地图级别设置
        with st.container():
            cols = st.columns([2, 1.1, 1.1, 1.9, 1.9, 1, 1])
            with cols[0]:
                plan = st.selectbox("选择方案", [i.split('/')[1] for i in sorted(all_plans.keys()) if i.startswith("normal_fight")])
                c = all_plans["normal_fight/"+plan]
            with cols[1]:
                selectbox("章节", list(range(1, 10)), c, "chapter", tag)
            with cols[2]:
                selectbox("地图", list(range(1, 7)), c, "map", tag)
            with cols[3]:
                text_input("维修方案", c, "repair_mode", tag)
            with cols[4]:
                selectbox("战况", ["稳步前进", "火力万岁", "小心翼翼", "瞄准", "搜索阵型"], c, "fight_condition", tag, True)
            with cols[-2]:
                rename_text_input("改名", all_plans, plan, "normal_fight/")
            with cols[-1]:
                add_button("增", all_plans, {"normal_fight/tmp": {"chapter": 1}})
                del_button("删", all_plans, "normal_fight/"+plan)

        # 节点选择
        with st.container():
            cols = st.columns([2, 9])
            with cols[1]:
                multiselect("所有要打的节点", [chr(ord('A')+i) for i in range(16)],
                              all_plans["normal_fight/"+plan], "selected_nodes", tag)
                if "node_args" not in all_plans["normal_fight/"+plan] or type(all_plans["normal_fight/"+plan]["node_args"]) != dict:
                    all_plans["normal_fight/"+plan]["node_args"] = {}
                # 补充没有的节点
                for i in all_plans["normal_fight/"+plan]["selected_nodes"]:
                    if i not in all_plans["normal_fight/"+plan]["node_args"]:
                        all_plans["normal_fight/"+plan]["node_args"].update({i: {"formation": 4}})
                # 删除无效节点
                for i in list(all_plans["normal_fight/"+plan]["node_args"].keys()):
                    if i not in all_plans["normal_fight/"+plan]["selected_nodes"]:
                        del all_plans["normal_fight/"+plan]["node_args"][i]
            with cols[0]:
                node = st.selectbox("待配置节点", sorted(all_plans["normal_fight/"+plan]["selected_nodes"]))
                c = all_plans["normal_fight/"+plan]["node_args"]
                # 插入一个新节点的情况
                if node not in c:
                    c.update({node: {"formation": 4}})
                c = c[node]

        # 节点级别设置
        with st.container():
            cols = st.columns([1.5, 1.5, 2, 2, 1.7, 1.3])
            with cols[0]:
                selectbox("正常阵型", ["单纵", "复纵", "轮型", "梯形", "单横"], c, "formation", tag, True)
            with cols[1]:
                selectbox("索敌失败阵型", ["单纵", "复纵", "轮型", "梯形", "单横"], c, "formation_when_spot_enemy_fails", tag, True)
            with cols[2]:
                checkbox("迂回", c, "detour", tag)
                checkbox("迂回失败SL", c, "SL_when_detour_fails", tag)
            with cols[3]:
                checkbox("索敌失败SL", c, "SL_when_spot_enemy_fails", tag)
                checkbox("进入战斗SL", c, "SL_when_enter_fight", tag)
            with cols[4]:
                checkbox("没补给舰就SL", c, "supply_ship_mode", tag)
            with cols[5]:
                checkbox("夜战", c, "night", tag)
                checkbox("前进", c, "proceed", tag)


with st.expander("日常挂机设置", False):
    c = config["daily_automation"]
    checkbox("重复远征", c, "auto_expedition")
    checkbox("自动点击完成任务", c, "auto_gain_bonus")
    checkbox("空闲时澡堂修理", c, "auto_bath_repair")

    checkbox("船坞已满时全部分解，否则则终止战斗进入收远征模式", c, "dock_full_destroy")

    cols = st.columns([1, 1, 2])
    with cols[0]:
        checkbox("完成每日战役", c, "auto_battle")
        if c["auto_battle"]:
            with cols[1]:
                selectbox("战役选择", ["困难驱逐", "困难巡洋", "困难战列", "困难航母", "困难潜艇"], c, "battle_type")

    cols = st.columns([1, 1, 2])
    with cols[0]:
        checkbox("进行自动出征", c, "auto_normal_fight")

    if c["auto_normal_fight"]:
        with cols[0]:
            add_button("添加计划", c["normal_fight_tasks"], [None, 1, 0])

        if len(c["normal_fight_tasks"]) >= 0:
            for id in range(len(c["normal_fight_tasks"])):
                task = c["normal_fight_tasks"][id]
                cols = st.columns(4)
                with cols[0]:
                    selectbox(
                        "任务",
                        [
                            i.split('/')[1]
                            for i in all_plans
                            if i.startswith("normal_fight")
                        ],
                        task,
                        0,
                        f"任务{id}",
                    )
                with cols[1]:
                    number_input("舰队", task, 1, f"舰队{id}", min_value=1, max_value=4)
                with cols[2]:
                    number_input("出征次数", task, 2, f"出征次数{id}", min_value=0)
                with cols[3]:
                    move_up_button("🔼", c["normal_fight_tasks"], id)
                    del_button("❌", c["normal_fight_tasks"], id)


save_data(config, ship_name, all_plans)
