import streamlit as st
import pandas as pd
# from numpy import isnan
review_data_name = "data/reviews.csv"
result_file_name = "data/label_result.csv"

labels = ("无关信息", "中性信息", "真", "假", "不确定")
if "all_labels" not in st.session_state:
    st.session_state.all_labels = pd.read_csv(result_file_name).label

all_labels = st.session_state.all_labels

def _to_the_final_label_idx(all_labels):
    st.session_state.last_time_idx = all_labels.size - 1
    for i, v in enumerate(reversed(all_labels.values)):
        if v != 4:
            st.session_state.last_time_idx -= (i - 1)
            break

    st.session_state.this_label = labels[st.session_state.all_labels[st.session_state.last_time_idx]]
    st.session_state.this_idx = st.session_state.last_time_idx

def _cover_origin_labels(user_labels):
    if "label" in user_labels.columns:
        if user_labels.iloc[0].values[0] in labels:
            user_labels.label = user_labels.label.apply(lambda v: labels.index(v))
        st.session_state.all_labels = user_labels.label
        if "is_user_upload" not in st.session_state:
            st.session_state.is_user_upload = True
            _to_the_final_label_idx(st.session_state.all_labels)
    else:
        st.info("'label'列不在便签文件中!请上传正确标签文件")

def upload_file():
    user_labels = st.file_uploader("用户可上传标签数据以覆盖当前数据", type=["csv"])
    if user_labels:
        user_labels = pd.read_csv(user_labels)
        _cover_origin_labels(user_labels)


def format_info(idx):
    info = data.loc[idx]
    return "> " + info["review"]


@st.experimental_memo
def get_data():
    return pd.read_csv(review_data_name)


def select():
    idx = st.session_state.this_idx
    all_labels[idx] = labels.index(st.session_state.this_label)
    # to next idx
    st.session_state.this_idx += 1
    radio_change()


def radio_change():
    idx = st.session_state.this_idx
    st.session_state.this_label = labels[st.session_state.all_labels[idx]]


data = get_data()
max_idx = data.shape[0] - 1


# st.write(pd.concat([data, all_labels], axis=1).head())
upload_file()

card = st.empty()
if "last_time_idx" not in st.session_state:
    _to_the_final_label_idx(all_labels)

idx = st.number_input("to idx", key="this_idx",
                      step=1, min_value=0, max_value=max_idx, on_change=radio_change)
# if idx != -1:
info = format_info(idx)
card.info(info)
new_label = st.radio("labels:", labels, key="this_label", on_change=select)

btn1, _, btn2 = st.columns((1, 2, 1))
save_btn = btn1.button("save")
download_btn = btn2.download_button(label="Download Result",
                                    data=all_labels.apply(lambda row: labels[row]).to_csv(index=False).encode('utf-8'),
                                    file_name="labels.csv",
                                    mime="text/csv")

if save_btn:
    result = all_labels.to_frame()
    result.to_csv(result_file_name, index=False)
    st.balloons()



# import leancloud
# @st.experimental_memo(allow_output_mutation=True,
# hash_funcs={"_thread.RLock": lambda _: None, "builtins.weakref": lambda _:None})
# @st.experimental_memo
# def init_leancloud():
#     leancloud.init(**st.secrets["leancloud"])
# init_leancloud()

# # 构建对象
# todo = Todo()

# # 为属性赋值
# todo.set('title',   '工程师周会')
# todo.set('content', '周二两点，全体成员')

# # 将对象保存到云端
# todo.save()
