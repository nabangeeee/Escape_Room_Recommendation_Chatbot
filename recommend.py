import pandas as pd
from embedding_utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import ast

def load_theme_data(csv_path="Room_escape_data_with_embeddings.csv"):
    df = pd.read_csv(csv_path)
        # 문자열로 저장된 embedding을 리스트로 변환
    if 'embedding' in df.columns:
        df['embedding'] = df['embedding'].apply(ast.literal_eval)
    return df


def filter_themes(df, prefs):
    filtered = df[
        (df['location'] == prefs['location']) &
        (df['min_people'] <= prefs['people']) &
        (df['max_people'] >= prefs['people'])
    ]

    if not prefs.get('fear_ok', True):  # 공포 싫어하면 제거
        filtered = filtered[~filtered['genre'].str.contains("공포")]

    if prefs.get('genre'):  # 선호 장르 필터링
        for g in prefs['genre']:
            filtered = filtered[filtered['genre'].str.contains(g)]

    return filtered


def recommend_by_embedding(df, user_message, top_k=3):
    # 사용자 입력 임베딩
    user_embedding = np.array(get_embedding(user_message)).reshape(1, -1)

    # 테마 데이터 내 텍스트 정보 준비
    if "embedding" not in df.columns:
        df["embedding_input"] = df.apply(lambda row: f"{row['theme_name']} {row['description']} {row['genre']}", axis=1)
        df["embedding"] = df["embedding_input"].apply(get_embedding)

    # 테마 임베딩들을 numpy 배열로
    theme_embeddings = np.stack(df["embedding"].to_numpy())

    # 코사인 유사도 계산
    similarities = cosine_similarity(user_embedding, theme_embeddings)[0]
    df["similarity"] = similarities

    # 유사도 기준 정렬하여 상위 K개 추천
    return df.sort_values(by="similarity", ascending=False).head(top_k)

