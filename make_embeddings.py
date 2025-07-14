import pandas as pd
from tqdm import tqdm
from embedding_utils import get_embedding # 이미 정의한 함수 사용

# 1. 데이터 불러오기
df = pd.read_csv("Room_escape_data.csv")

# 2. 임베딩 생성용 텍스트 조합 (네 데이터 컬럼명 기준)
def make_embedding_text(row):
    # 주요 특징을 자연스럽게 이어붙임
    return (
        f"{row['theme_name']} "
        f"{row['store_name']} "
        f"{row['location']} "
        f"{row['genre']} "
        f"최소인원 {row['min_people']}명 최대인원 {row['max_people']}명 "
        f"난이도 {row['difficulty']} "
        f"공포도 {row['fear']} "
        f"평점 {row['rating']} "
        f"{row['address']}"
    )

df['embedding_text'] = df.apply(make_embedding_text, axis=1)

# 3. 모든 행에 대해 임베딩 생성 및 저장
embeddings = []
for text in tqdm(df['embedding_text']):
    embeddings.append(get_embedding(text))  # OpenAI API 호출

df['embedding'] = embeddings

# 4. 임베딩 추가된 데이터 저장
df.to_csv("Room_escape_data_with_embeddings.csv", index=False)
