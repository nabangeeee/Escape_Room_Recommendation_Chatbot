import os
from dotenv import load_dotenv #.env 파일에 저장된 환경 변수를 로드하는데 사용
from openai import OpenAI

load_dotenv()  # .env 파일 로드
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # 환경변수에서 "OPENAI_AI_KEY" 값을 읽어와 OPENAI API키로 설정

def get_embedding(text: str, model="text-embedding-3-small"): # 입력값으로 text(문자열), model받음
    response = client.embeddings.create( #openai라이브러리의 embeddings기능에서 create메서드를 호출
        input=[text],
        model=model
    )
    return response.data[0].embedding # 데이터의 0번 인덱스를 선택하고 그 인덱스의 임베딩벡터를 리턴

# embeddings: Openai API에서 임베딩을 생성하는 메서드 이름
# embedding: 임베딩 벡터(숫자 배열). 나중에 텍스트 의미, 유사성 등을 수치적으로 계산할 때 사용