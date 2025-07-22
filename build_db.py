import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. 데이터 불러오기
df = pd.read_csv("Room_escape_data.csv")
docs = [
    f"테마: {row['theme_name']}, 설명: {row['description'] if 'description' in row else ''}, "
    f"장르: {row['genre']}, 지역: {row['location']}, 난이도: {row['difficulty']}, 평점: {row['rating']}"
    for _, row in df.iterrows()
]

# 2. 허깅페이스 임베딩 함수 생성 (예시)
embeddings = HuggingFaceEmbeddings(
    model_name="jhgan/ko-sroberta-multitask",   # 한국어 의미 임베딩용 추천
    model_kwargs={'device': 'cpu'}              # GPU 있으면 'cuda'
)

# 3. ChromaDB 벡터DB 재구축
vectordb = Chroma.from_texts(
    docs,
    embeddings,
    persist_directory="./chroma_db"
)
vectordb.persist()
print("DB 재구축 완료! 문서 수:", vectordb._collection.count())
