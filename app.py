
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
入力された質問に対してすでに読み込んだ以下の外部ファイルからわかる情報だけを
優秀な総務担当として適切に解釈した上で回答してください。

# example1.txt
# example2.txt
# example3.txt

尚、回答は丁寧且つわかりやすく答え、どのファイルに記載されている情報化は質問者には答えないでください。


尚、ファイルからわかる情報で回答できない質問に対しては絶対に勝手な推測で回答しないでください。
その場合は「その質問に対してはルールがないので回答できません」
とは一言一句変更せずに答えてください。
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
st.markdown("<p style='font-size:14px;'><br>知りたい会社のルールに関する質問を入力してください。<br>尚、現在は「PC利用に関するルール」「交通費に関するルール」「経費に関するルール」しか学習していない為、それ以外には答えられません。<br>※このルールは一般のIT会社を想定したAIが作ったダミーのルールです。</p>", unsafe_allow_html=True)


user_input = st.text_input("", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
