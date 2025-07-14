from gpt_api import extract_user_preferences
from recommend import load_theme_data, recommend_by_embedding, filter_themes

user_message = "3명이 홍대에서 공포테마 하고 싶어"
prefs = extract_user_preferences(user_message)
print("사용자 조건:", prefs)


df = load_theme_data("Room_escape_data_with_embeddings.csv")
filtered_df = filter_themes(df, prefs)
recommended = recommend_by_embedding(filtered_df if not filtered_df.empty else df, user_message)

print("\n 추천 테마:")
print(recommended[["theme_name", "store_name", "genre", "location", "rating", "reservation_link"]])

import tabulate
print(tabulate.__version__)


