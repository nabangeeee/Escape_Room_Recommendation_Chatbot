import requests
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('NAVER_CLIENT_ID')
client_secret = os.getenv('NAVER_CLIENT_SECRET')

query = "방탈출"
url = f"https://openapi.naver.com/v1/search/blog?query={query}"
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}
response = requests.get(url, headers=headers)
print(response.json())
