import sqlite3
import pandas as pd

conn = sqlite3.connect("premier_league.db")

df_stat = pd.read_sql("SELECT Player FROM premier_league_stats", conn)
df_transfer = pd.read_sql("SELECT Player, Price FROM premier_league_transfer", conn)

# left join
df_merged = df_stat.merge(
    df_transfer,
    on="Player",
    how="left"
)

# Điền giá trị N/A nếu thiếu
df_merged["Price"] = df_merged["Price"].fillna("N/A")

df_merged.to_sql("player_with_price", conn, if_exists="replace", index=False)
conn.close()