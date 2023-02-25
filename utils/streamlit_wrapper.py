import streamlit as st


# 统一 字典、列表 的修改方式
def value_assign(dic_or_list, key_or_index, st_key):
    def assign():
        value = st.session_state[st_key]
        try:
            value = eval(value)
        except:
            pass
        dic_or_list[key_or_index] = value
    return assign


# TODO：检查是否都是 1-based index
def index_assign(options, dic_or_list, key_or_index, st_key):
    def assign():
        value = st.session_state[st_key]
        try:
            value = eval(value)
        except:
            pass
        dic_or_list[key_or_index] = options.index(value) + 1
    return assign


# ==================== 以下为封装的 streamlit 组件 ====================
def selectbox(label, options, dic_or_list, key_or_index, tag='', option_to_index=False, **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except:
        default_value = 1 if option_to_index else options[0]
    
    # 可以设置None来表示默认值
    if default_value is None:
        default_value = 1 if option_to_index else options[0]

    if option_to_index:  # 默认值是索引
        default_value -= 1  # TODO：检查是否都是 1-based index
        callback_fn = index_assign(options, dic_or_list, key_or_index, st_key)
        return st.selectbox(label, options, default_value, key=st_key, on_change=callback_fn, **kwargs)
    else:  # 默认值就是选项
        callback_fn = value_assign(dic_or_list, key_or_index, st_key)
        return st.selectbox(label, options, options.index(default_value), key=st_key, on_change=callback_fn, **kwargs)


def multiselect(label, options, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except:
        default_value = None
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.multiselect(label, options, default_value, key=st_key, on_change=callback_fn, **kwargs)


def checkbox(label, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except:
        default_value = False
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.checkbox(label, default_value, key=st_key, on_change=callback_fn, **kwargs)


def text_input(label, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except:
        default_value = ""
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.text_input(label, default_value, key=st_key, on_change=callback_fn, **kwargs)


def rename_text_input(label, father_dic, father_key, prefix='', tag='', **kwargs):
    def item_rename(father_dict, father_key, prefix, st_key):
        def rename():
            new_key = prefix + st.session_state[st_key]
            father_dict[new_key] = father_dict.pop(prefix + father_key)
            st.session_state[st_key] = ''
        return rename
    st_key = label + str(tag)
    callback_fn = item_rename(father_dic, father_key, prefix, st_key)
    return st.text_input(label, key=st_key, on_change=callback_fn, **kwargs)


def number_input(label, dic_or_list, key_or_index, tag='', **kwargs):
    st_key = label + str(tag)
    try:
        default_value = dic_or_list[key_or_index]
    except:
        default_value = None
    callback_fn = value_assign(dic_or_list, key_or_index, st_key)
    return st.number_input(label, value=default_value, key=st_key, on_change=callback_fn, **kwargs)


def add_button(label, father_list, value, tag='', **kwargs):
    def item_add(father_list, value):
        def add():
            if type(father_list) == list:
                father_list.append(value)
            elif type(father_list) == dict:
                father_list.update(value)
        return add
    st_key = label + str(tag)
    callback_fn = item_add(father_list, value)
    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)


def del_button(label, father_list, index, tag='', **kwargs):
    def item_delete(father_list, index):
        def delete():
            father_list.pop(index)
        return delete
    st_key = label + str(tag) + str(index)
    callback_fn = item_delete(father_list, index)
    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)


def move_up_button(label, father_list, index, tag='', **kwargs):
    def item_move_up(father_list, index):
        def move_up():
            if index >= 1:
                father_list[index], father_list[index-1] = father_list[index-1], father_list[index]
        return move_up

    st_key = label + str(tag) + str(index)
    callback_fn = item_move_up(father_list, index)

    return st.button(label, key=st_key, on_click=callback_fn, **kwargs)
