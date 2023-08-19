
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# 複数の外部ファイルを読み込む
file_names = ["example1.txt", "example2.txt", "example3.txt"]
external_data = ""

for file_name in file_names:
    with open(file_name, "r") as f:
        external_data += f.read() + "\n"

system_prompt = """
あなたは経験豊富な会社の総務担当です。

以下のルールにのっとり会社のルールに関する質問に答えてください。

質問に対してすでに読み込んだ以下のの3つのテキストファイルからからわかる情報を回答してください。

# example1.txt
# example2.txt
# example3.txt

ファイルの内容で回答できない質問の場合は「その質問に対してはルールがないので回答できません」
と答えてください。ファイルの内容で回答できない場合の回答は一言一句変更しないでください。
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# カスタムスタイルを適用するためのHTMLコード
custom_css = """
<style>
    .reportview-container .main .block-container {
        background-color: #689F91; /* ここで背景色を指定 */
    }
    .stTextInput input {
        color: black;
    }
</style>
"""

# カスタムスタイルを適用
st.markdown(custom_css, unsafe_allow_html=True)

# ユーザーインターフェイスの構築
st.image("company_policy.gif")
st.markdown("<p style='font-size:14px;'>知りたい会社のルールに対して質問してください。<br>尚、現在は「PC利用に関するルール」「交通費に関するルール」「経費に関するルール」しか学習していない為、それ以外には答えられません。<br>※このルールはダミーです。</p>", unsafe_allow_html=True)


user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
