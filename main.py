# main.py
from gpt_api import extract_user_preferences
from recommend import load_theme_data, filter_themes

user_input = "공포는 싫고 2명이 홍대에서 감성 테마 하고 싶어"
prefs = extract_user_preferences(user_input)

print("🎯 사용자 조건:", prefs)

df = load_theme_data("Room_escape_data.csv")
recommended = filter_themes(df, prefs)

print("\n🔍 추천 테마:")
print(recommended[["theme_name", "store_name", "genre", "location", "rating", "reservation_link"]])
