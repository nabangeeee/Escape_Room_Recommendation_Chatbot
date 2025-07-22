import requests
import urllib.parse
import os
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")




def naver_blog_search(keyword, display=2):
    query = urllib.parse.quote(keyword)
    url = f"https://openapi.naver.com/v1/search/blog?query={query}&display={display}"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.json().get('items', [])
    else:
        return []