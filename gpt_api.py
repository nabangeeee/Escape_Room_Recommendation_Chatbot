# gpt_api.py
import openai
import openai_config  # API 키 로딩
import pandas as pd
import os

def get_embedding(text: str, model="text-embedding-3-small"):
    """
    텍스트 임베딩 벡터를 반환합니다.
    """
    # 환경변수에서 API 키 불러오기 (이미 openai_config 등에서 설정되어 있으면 이 줄은 생략 가능)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

# CSV 기반으로 가능한 옵션 추출
def get_available_options(csv_path="Room_escape_data_with_embeddings.csv"):
    df = pd.read_csv(csv_path)
    locations = sorted(set(df['location'].dropna()))
    genres = sorted(set(g for genre in df['genre'].dropna() for g in genre.split(',')))
    return locations, genres

import pandas as pd

# CSV 기반으로 가능한 옵션 추출
def get_available_options(csv_path="Room_escape_data_with_embeddings.csv"):
    df = pd.read_csv(csv_path)
    locations = sorted(set(df['location'].dropna()))
    genres = sorted(set(g for genre in df['genre'].dropna() for g in genre.split(',')))
    return locations, genres

def extract_user_preferences(user_input: str) -> dict:
    locations, genres = get_available_options("Room_escape_data_with_embeddings.csv")

    system_prompt = f"""
    너는 방탈출 추천 AI야. 사용자의 대화를 기반으로 추천 조건을 JSON으로 추출해줘.
    다음은 가능한 지역과 장르야:

    - 가능한 지역: {locations}
    - 가능한 장르: {genres}
    - 인원수는 정수형 숫자야. 공포가 괜찮다면 fear_ok=true, 싫다면 false로 해줘.

    아래 형식으로 JSON 응답을 줘:
    {{
      "location": "홍대",
      "people": 3,
      "genre": ["공포"],
      "fear_ok": true
    }}

    사용자가 명확하게 말하지 않은 경우엔 추론해줘. 예를 들어 '무서운 건 싫어' → fear_ok: false, '혼자 갈 거야' → people: 1
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.5, #창의성 정도를 조절. 0.0: 정직하고 예측 가능한 답변, 0.5: 균형잡힌 창의성과 일관성(보통 자주 쓰임), 1.0: 더욱 창의적이고 다양하게 말함.
        request_timeout=30
    )

    result = response.choices[0].message.content.strip() #답변 후보들 중에 가장 첫번째꺼를 선택. 후보는 기본적으로 1개만 생성. 그러나 여려개 생성 가능.

    # GPT 응답이 JSON 문자열로 오도록 유도했지만, 실제로는 파싱 로직이 더 필요할 수도 있음
    import json
    try:
        return json.loads(result)
    except json.JSONDecodeError:
        print("[ERROR] GPT 응답을 JSON으로 파싱할 수 없습니다:\n", result)
        return {}

# def extract_user_preferences(user_input: str) -> dict:
#     return {
#         "location": "홍대",
#         "people": 2,
#         "genre": ["감성"],
#         "fear_ok": False
#     }