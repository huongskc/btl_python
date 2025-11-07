import sqlite3
import pandas as pd

conn = sqlite3.connect("premier_league.db")
df = pd.read_sql("SELECT * FROM premier_league_stats", conn)
conn.close()

# Loại bỏ cột không phải dữ liệu
non_numeric = ["Player", "Nation", "Pos", "Squad", "Rk", "Born", "Matches"]
cols_numeric = [c for c in df.columns if c not in non_numeric]

# Nhóm theo đội và thống kê
# mean: trung bình   median: trung vị   std: độ lệch chuẩn
summary = (
    df.groupby("Squad")[cols_numeric]
    .agg(["mean", "median", "std"])
    .round(2)
)

summary.reset_index(inplace=True)

summary.to_csv("team_stats_summary.csv", index=False, encoding="utf-8-sig")