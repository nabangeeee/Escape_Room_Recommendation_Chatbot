# gpt_api.py
import openai
import openai_config  # API 키 로딩

def extract_user_preferences(user_input: str) -> dict:
    system_prompt = """
    너는 방탈출 추천 AI야. 사용자의 대화를 기반으로 추천 조건을 추출해줘.
    다음 형식의 JSON으로 응답해:
    {"location": ..., "people": ..., "genre": [...], "fear_ok": true/false}
    """


    messages = [
        {"role": "system", "content": system_prompt}, # 해당 딕셔너리는 챗봇에서 거의 필수로 쓰임. 역할을 부여. role:누가 말하는지, content: 무슨 말을 하는지
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