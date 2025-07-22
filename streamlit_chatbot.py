import streamlit as st
from gpt_api import extract_user_preferences
from recommend import load_theme_data, recommend_by_embedding, filter_themes
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from naver_api import naver_blog_search
import re

def get_fear_level(page_content):
    import re
    match = re.search(r"공포도: ([\d\.]+)", page_content)
    if match:
        return float(match.group(1))
    return None


embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask",
    model_kwargs={'device': 'cpu'}
)
vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 모드 선택 UI (사이드바 or 본문 최상단)
mode = st.sidebar.radio("모드 선택", ("방탈출 추천 챗봇", "RAG 임베딩 검색"))

st.title("방탈출 & RAG 챗봇")

if mode == "RAG 임베딩 검색":    # RAG 검색 챗봇 모드
    # 벡터DB 인스턴스화
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

    user_query = st.text_input("궁금한 내용을 입력하세요! (예: 강남 감성테마 추천해줘!)")
    if user_query:
        result_docs = vectordb.similarity_search(user_query, k=3)
        st.subheader("추천 테마 목록")

        shown = 0
        for i, doc in enumerate(result_docs, 1):
            lines = doc.page_content.split(", ")
            # 장르 확인
            genre_line = [x for x in lines if x.startswith("장르: ")][0]
            genre_name = genre_line.replace("장르: ","").strip()
            # 공포도 확인
            fear = get_fear_level(doc.page_content)

            # 쿼리에 조건에 따라 필터
            if "감성" in user_query and "감성" not in genre_name:
                continue
            if "공포" in user_query and (fear is None or fear < 1):  # 공포도 1 이상만 노출 등 원하는 기준 지정
                continue

            theme_name = lines[0].replace("테마: ", "")
            detail_text = ", ".join(lines[1:])
            st.markdown(f"""
            <div style="margin-bottom:18px;">
                <span style="font-size:2em; font-weight:bold;">{shown+1}. {theme_name}</span>
                <br>
                <span style="font-size:1em;">{detail_text}</span>
            </div>
            """, unsafe_allow_html=True)
            shown += 1
            if shown >= 3:
                break

            lines = doc.page_content.split(", ")

            # ----- 네이버 블로그 추가 정보 -----
            theme_title = doc.page_content.split(',')[0].replace("테마: ", "").strip()
            naver_items = naver_blog_search(theme_title)
            if naver_items:
                st.write("> 아래 블로그를 클릭하면 더 자세한 정보를 볼 수 있어요!")
                for item in naver_items:
                    st.markdown(f"- [{item['title']}]({item['link']})")
            else:
                st.write("> 네이버 블로그에 추가 정보 없음")
        else:
            st.info("방탈출 추천 목록이에요. 즐거운 방탈출 되세요!")
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
