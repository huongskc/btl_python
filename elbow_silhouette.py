import pandas as pd
import sqlite3
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

conn = sqlite3.connect("premier_league.db")
df = pd.read_sql("SELECT * FROM premier_league_stats", conn)
conn.close()

# Chọn các chỉ số chuyên môn để phân loại cầu thủ
cols = [
    "Gls", "Ast", "G-PK", "xG", "xAG", "npxG", "npxG+xAG",
    "PrgC", "PrgP", "PrgR",
    "Gls.Per90Min", "Ast.Per90Min",
    "xG.Per90Min", "xAG.Per90Min",
    "npxG.Per90Min", "npxG+xAG.Per90Min"
]

df_num = df[cols].dropna()

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_num)

# Tính Elbow & Silhouette
inertia = []
silhouette = []
K = range(2, 10)

for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette.append(silhouette_score(X_scaled, kmeans.labels_))

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(K, inertia, 'o-', color='blue')
plt.title('Biểu đồ Elbow')
plt.xlabel('Số cụm (k)')
plt.ylabel('Inertia')

plt.subplot(1,2,2)
plt.plot(K, silhouette, 'o-', color='green')
plt.title('Biểu đồ Silhouette')
plt.xlabel('Số cụm (k)')
plt.ylabel('Silhouette Score')

plt.tight_layout()
plt.show()