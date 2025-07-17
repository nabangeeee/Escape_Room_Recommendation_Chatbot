import pandas as pd
import ast
import chromadb

df = pd.read_csv("Room_escape_data_with_embeddings.csv")
df['embedding'] = df['embedding'].apply(ast.literal_eval)
client = chromadb.PersistentClient(path="./chroma_db")

# 컬렉션 존재하면 get, 없으면 create (더 안전!)
collection_name = "my_collection"
try:
    collection = client.get_collection(name=collection_name)
except Exception:
    collection = client.create_collection(name=collection_name)

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
            embeddings=[row['embedding']]
        )
    except Exception as e:
        print(f"건너뜀({row['theme_name']}): {e}")

print("데이터 이관 완료! (총 등록된 데이터 개수:", collection.count(), ")")
