import streamlit as st
from gpt_api import extract_user_preferences
from recommend import load_theme_data, filter_themes

st.title("방탈출 챗봇")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("원하는 조건을 입력하세요!"):
    st.chat_message("user").markdown(user_message)
    try:
        prefs = extract_user_preferences(user_message)
        df = load_theme_data("Room_escape_data.csv")
        recommended = filter_themes(df, prefs)
        if not recommended.empty:
            bot_message = recommended[["theme_name", "store_name", "genre", "location", "rating", "reservation_link"]].to_markdown(index=False)
        else:
            bot_message = "조건에 맞는 테마가 없습니다."
    except Exception as e:
        bot_message = f"오류 발생: {e}"
    st.chat_message("assistant").markdown(bot_message)
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    st.session_state.chat_history.append({"role": "assistant", "content": bot_message})
