import pandas as pd

# Đọc file và bỏ dòng chứa 'mean, median, std'
df = pd.read_csv("team_stats_summary.csv", skiprows=[1])

# Lấy các cột trung bình (mean)
mean_cols = [df.columns[i] for i in range(1, len(df.columns), 3)]

# Giữ lại tên đội và các chỉ số trung bình
df_mean = df[["Squad"] + mean_cols].copy()

print("Đội có chỉ số trung bình cao nhất từng hạng mục")

# In ra đội có điểm cao nhất ở mỗi chỉ số
best_per_stat = {}
for col in mean_cols:
    top_idx = df_mean[col].idxmax()
    top_team = df_mean.loc[top_idx, "Squad"]
    top_value = df_mean.loc[top_idx, col]
    best_per_stat[col] = {"Team": top_team, "Value": top_value}
    print(f"{col:<25} {top_team:<20} ({top_value})")

# Lấy danh sách đội đứng đầu từng cột
leaders = [df_mean.loc[df_mean[col].idxmax(), "Squad"] for col in mean_cols]

# Đếm số lần xuất hiện mỗi đội
df_top = pd.Series(leaders).value_counts().reset_index()

print(f"Đội có phong độ tốt nhất: {df_top.iloc[0,0]} (dẫn đầu {df_top.iloc[0,1]} chỉ số)")
