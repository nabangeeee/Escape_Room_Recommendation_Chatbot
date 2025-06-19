import pandas as pd

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
