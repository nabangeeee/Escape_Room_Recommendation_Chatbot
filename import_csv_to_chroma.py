import pandas as pd
import chromadb # type: ignore
from chromadb.utils import embedding_functions  # 임베딩 함수 준비 (예시)

df = pd.read_csv("Room_escape_data.csv")
client = chromadb.PersistentClient(path="./chroma_db")

# 임베딩 함수(간단한 예시): 실제 서비스할 땐 많은 데이터면 OpenAI API 등 사용!
embedding_function = embedding_functions.DefaultEmbeddingFunction() 

collection_name = "my_collection"
try:
    collection = client.get_collection(name=collection_name)
except Exception:
    collection = client.create_collection(
        name=collection_name,
        embedding_function=embedding_function  # 임베딩 지정!
    )

for idx, row in df.iterrows():
    documents = (
        f"테마: {row['theme_name']} | 매장: {row['store_name']} | 지역: {row['location']} | 장르: {row['genre']} | "
        f"평점: {row['rating']} | 난이도: {row['difficulty']} | 공포도: {row['fear']}"
    )
    # id 중복 체크: 이미 있는 id라면 add에서 오류가 날 수 있습니다!
    try:
        collection.add(
            ids=[f"{row['theme_name']}_{row['store_name']}_{row['location']}"],
            documents=[documents],
            # embeddings 파라미터 삭제!
        )
    except Exception as e:
        print(f"건너뜀({row['theme_name']}): {e}")

print("데이터 이관 완료! (총 등록된 데이터 개수:", collection.count(), ")")
