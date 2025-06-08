# recommend.py
import pandas as pd

def load_theme_data(csv_path="Room_escape_data.csv"):
    df = pd.read_csv(csv_path)
    return df

def filter_themes(df, conditions):
    # 조건 추출
    loc = conditions.get("location", "")
    people = conditions.get("people", 0)
    genre_pref = conditions.get("genre", [])
    fear_ok = conditions.get("fear_ok", True)

    def matches(row):
        return (
            (loc in row["location"]) and
            (row["min_people"] <= people <= row["max_people"]) and
            any(g in row["genre"] for g in genre_pref) and
            (fear_ok or row["fear"] == 0)
        )

    filtered = df[df.apply(matches, axis=1)]
    return filtered
