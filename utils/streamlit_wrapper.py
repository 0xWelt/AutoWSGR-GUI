import streamlit as st


# 统一 字典、列表 的修改方式
def value_assign(father_item, key_or_index, st_key):
    def assign():
        value = st.session_state[st_key]
        try:
            value = eval(value)
        except:
            pass
        father_item[key_or_index] = value
    return assign


# TODO：检查是否都是 1-based index
def index_assign(options, father_item, key_or_index, st_key):
    def assign():
        value = st.session_state[st_key]
        try:
            value = eval(value)
        except:
            pass
        father_item[key_or_index] = options.index(value) + 1
    return assign


def item_delete(father_list, index, st_key):
    def delete():
        if st.session_state[st_key]:
            father_list.pop(index)
    return delete


# ==================== 以下为封装的 streamlit 组件 ====================
def w_selectbox(label, options, father_item, key_or_index, st_key=None, **kwargs):
    st_key = label if st_key is None else st_key
    try:
        default_value = father_item[key_or_index]
    except:
        default_value = 0
    # 默认值可以是索引，也可以是选项
    if default_value not in options:
        default_value = options[default_value-1]  # TODO：检查是否都是 1-based index
        callback_fn = index_assign(options, father_item, key_or_index, st_key)
    else:
        callback_fn = value_assign(father_item, key_or_index, st_key)
    return st.selectbox(label, options, options.index(default_value), key=st_key, on_change=callback_fn, **kwargs)

def w_multiselect(label, options, father_item, key_or_index, st_key=None, **kwargs):
    st_key = label if st_key is None else st_key
    try:
        default_value = father_item[key_or_index]
    except:
        default_value = None
    callback_fn = value_assign(father_item, key_or_index, st_key)
    return st.multiselect(label, options, default_value, key=st_key, on_change=callback_fn, **kwargs)

def w_checkbox(label, father_item, key_or_index, st_key=None, **kwargs):
    st_key = label if st_key is None else st_key
    try:
        default_value = father_item[key_or_index]
    except:
        default_value = False
    callback_fn = value_assign(father_item, key_or_index, st_key)
    return st.checkbox(label, default_value, key=st_key, on_change=callback_fn, **kwargs)


def w_text_input(label, father_item, key_or_index, st_key=None, **kwargs):
    st_key = label if st_key is None else st_key
    try:
        default_value = father_item[key_or_index]
    except:
        default_value = ""
    callback_fn = value_assign(father_item, key_or_index, st_key)
    return st.text_input(label, default_value, key=st_key, on_change=callback_fn, **kwargs)


def w_number_input(label, father_item, key_or_index, st_key=None, **kwargs):
    st_key = label if st_key is None else st_key
    try:
        default_value = father_item[key_or_index]
    except:
        default_value = None
    callback_fn = value_assign(father_item, key_or_index, st_key)
    return st.number_input(label, value=default_value, key=st_key, on_change=callback_fn, **kwargs)


def del_button(label, father_list, index, st_key=None, **kwargs):
    st_key = label+str(index) if st_key is None else st_key
    callback_fn = item_delete(father_list, index, st_key)
    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)
