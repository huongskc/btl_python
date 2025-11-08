import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

conn = sqlite3.connect("premier_league.db")
df = pd.read_sql("SELECT * FROM premier_league_stats", conn)
conn.close()

cols = [
    "Gls", "Ast", "G-PK", "xG", "xAG", "npxG", "npxG+xAG",
    "PrgC", "PrgP", "PrgR",
    "Gls.Per90Min", "Ast.Per90Min",
    "xG.Per90Min", "xAG.Per90Min",
    "npxG.Per90Min", "npxG+xAG.Per90Min"
]

df_num = df[cols].dropna()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_num)

# Dựa vào biểu đồ Elbow và Silhouette, ta sẽ phân ra thành 4 cụm
k_opt = 4 
kmeans = KMeans(n_clusters=k_opt, random_state=42)
df["Cluster"] = kmeans.fit_predict(X_scaled)

conn = sqlite3.connect("premier_league.db")
df.to_sql("player_clusters", conn, if_exists="replace", index=False)
conn.close()
df.to_csv("clustered_players.csv", index=False, encoding="utf-8-sig")

# Phân tích trung bình theo cụm
summary = df.groupby("Cluster")[cols].mean().round(2)
print("=== TRUNG BÌNH CHỈ SỐ THEO CỤM ===")
print(summary)

# Biểu đồ PCA 2D
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize=(8,6))
plt.scatter(X_pca[:, 0], X_pca[:, 1],
            c=df["Cluster"], cmap="tab10", s=50, alpha=0.8, edgecolor='k')

plt.title("Biểu đồ 2D K-Means Scatter (sau khi giảm chiều bằng PCA)", fontsize=13)

centers = kmeans.cluster_centers_
centers_pca = pca.transform(centers)
plt.scatter(centers_pca[:, 0], centers_pca[:, 1],
            c='black', s=50, marker='X', label='Tâm cụm')
plt.legend()
plt.tight_layout()
plt.show()

# Biểu đồ PCA 3D
pca_3d = PCA(n_components=3)
X_pca_3d = pca_3d.fit_transform(X_scaled)

fig = plt.figure(figsize=(9,7))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_pca_3d[:, 0], X_pca_3d[:, 1], X_pca_3d[:, 2],
           c=df["Cluster"], cmap="tab10", s=40, alpha=0.8, edgecolor='k')
ax.set_title("Biểu đồ PCA 3D K-Means Scatter", fontsize=13)

centers_3d = pca_3d.transform(kmeans.cluster_centers_)
ax.scatter(centers_3d[:, 0], centers_3d[:, 1], centers_3d[:, 2],
           c='black', s=50, marker='X', label='Tâm cụm')
ax.legend()
plt.show()