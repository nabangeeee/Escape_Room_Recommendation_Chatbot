import pandas as pd
from embedding_utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def load_theme_data(csv_path="Room_escape_data.csv"):
    df = pd.read_csv(csv_path)
    return df

def filter_themes(df, conditions):
    loc = conditions.get("location", "")
    people = conditions.get("people", 0)
    genre_pref = conditions.get("genre", [])
    fear_ok = conditions.get("fear_ok", True)

    def matches(row):
        genre_list = [g.strip() for g in row["genre"].split(",")]

        fear_condition = True
        if not fear_ok:
            # row["fear"] 값이 없으면 기본값 "0"
            fear_condition = (str(row.get("fear", "0")) == "0")

        return (
            (loc in row["location"]) and
            (row["min_people"] <= people <= row["max_people"]) and
            any(g in genre_list for g in genre_pref) and
            fear_condition
        )

    return df[df.apply(matches, axis=1)]


def recommend_by_embedding(df, user_input, top_k=3):
    # 사용자 입력 임베딩
    user_embedding = np.array(get_embedding(user_input)).reshape(1, -1)

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
