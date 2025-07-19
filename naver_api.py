import requests
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()



client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')

query = urllib.parse.quote("방탈출")
url = f"https://openapi.naver.com/v1/search/blog?query={query}"
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print("네이버 API 호출 에러:", response.text)

