import streamlit as st
from gpt_api import extract_user_preferences
from recommend import load_theme_data, recommend_by_embedding, filter_themes
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask",
    model_kwargs={'device': 'cpu'}
)
vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


# 모드 선택 UI (사이드바 or 본문 최상단)
mode = st.sidebar.radio("모드 선택", ("방탈출 추천 챗봇", "RAG 임베딩 검색"))


st.title("방탈출 & RAG 챗봇")

if mode == "RAG 임베딩 검색":


    # 2) 벡터DB 인스턴스화: 임베딩 함수 그대로!
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


    # RAG 검색 챗봇 모드
    user_query = st.text_input("궁금한 내용을 입력하세요! (예: 방탈출 매장 공략법, 정보 등)")
    if user_query:
        result_docs = vectordb.similarity_search(user_query, k=3)
        st.subheader("관련 정보")
        if result_docs:
            for i, doc in enumerate(result_docs, 1):
                st.write(f"**{i}.**")
                st.write(doc.page_content)
        else:
            st.info("검색 결과가 없습니다. 다른 단어로 시도해보세요!")
    else:
        st.info("질문 내용을 입력해 주세요!")


elif mode == "방탈출 추천 챗봇":

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)


    # 방탈출 추천 챗봇 모드 (기존 코드)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_message = st.chat_input("원하는 조건을 입력해 주세요! 저 방탈출 추천 챗봇이 재밌는 테마를 추천해 드릴게요! 🙌")
    if user_message:
        st.chat_message("user").markdown(user_message)
        try:
            prefs = extract_user_preferences(user_message)
            df = load_theme_data("Room_escape_data_with_embeddings.csv")
            filtered_df = filter_themes(df, prefs)
            recommended = recommend_by_embedding(filtered_df if not filtered_df.empty else df, user_message)

            if not recommended.empty:
                bot_message = ("추천 테마를 찾아봤어요! 😊\n\n" +
                            recommended[["theme_name", "store_name", "genre", "location", "rating", "reservation_link"]]
                            .to_markdown(index=False))
            else:
                bot_message = "조건에 맞는 테마가 없어요.😢 다른 조건으로 추천해드릴까요?"
        except Exception as e:
            print("[ERROR]", e)
            bot_message = "조건에 맞는 테마가 아직 없어요.😅 관리자 이메일로 피드백을 보내주세요!"
        
        st.chat_message("assistant").markdown(bot_message)
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        st.session_state.chat_history.append({"role": "assistant", "content": bot_message})

# 문의하기 UI는 공통으로 맨 아래에 유지
st.markdown("---")
st.subheader("문의하기")
contact_email = "paula11@naver.com"
st.link_button("이메일로 문의하기", f"mailto:{contact_email}")
message = "여기로 피드백 부탁드려요!🙌 이용해주셔서 감사합니다😊"
st.write(message)
