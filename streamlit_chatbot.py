import streamlit as st
from gpt_api import extract_user_preferences
from recommend import load_theme_data, filter_themes

st.title("방탈출 챗봇")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_message := st.chat_input("원하는 조건을 입력해 주세요! 저 방탈출 추천 챗봇이 재밌는 테마를 추천해 드릴게요! 🙌"):
    st.chat_message("user").markdown(user_message)
    try:
        prefs = extract_user_preferences(user_message)
        df = load_theme_data("Room_escape_data.csv")
        recommended = filter_themes(df, prefs)
        if not recommended.empty:
            bot_message = ("추천 테마를 찾아봤어요! 😊\n\n" + recommended[["theme_name", "store_name", "genre", "location", "rating", "reservation_link"]].to_markdown(index=False))
        else:
            bot_message = "조건에 맞는 테마가 없어요.😢 다른 조건으로 추천해드릴까요?"
    except Exception as e:
        bot_message = "조건에 맞는 테마가 아직 없어요.😅 관리자 이메일로 피드백을 보내주세요!"
    st.chat_message("assistant").markdown(bot_message)
    st.session_state.chat_history.append({"role": "user", "content": user_message})
    st.session_state.chat_history.append({"role": "assistant", "content": bot_message})






# 앱 맨 아래에 문의하기 버튼 추가
st.markdown("---")  # 구분선(선택)
st.subheader("문의하기")

# 예시: 이메일로 문의
contact_email = "paula11@naver.com"
st.link_button("이메일로 문의하기", f"mailto:{contact_email}")
message = "여기로 피드백 부탁드려요!🙌 이용해주셔서 감사합니다😊"
st.write(message)
