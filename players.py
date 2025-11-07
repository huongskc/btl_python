from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO
import sqlite3

def make_unique_columns(columns):
    seen = {}
    result = []
    for col in columns:
        if col not in seen:
            seen[col] = 0
            result.append(col)
        else:
            result.append(f"{col}.Per90Min")
    return result

options = Options()
options.add_argument("--start-maximized")
# Giả lập người dùng thật
options.add_argument("user-agent=Mozilla/5.0")
options.add_argument("--headless=new")

url = "https://fbref.com/en/comps/9/2024-2025/stats/2024-2025-Premier-League-Stats"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

try:
    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.ID, "stats_standard"))
    )
except:
    driver.quit()
    exit()

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table", {"id": "stats_standard"})

df = pd.read_html(StringIO(str(table)))[0]
# Làm phẳng các cột
df.columns = df.columns.droplevel(0)
# Đổi tên cột bị trùng do làm phẳng
df.columns = make_unique_columns(df.columns)
# Loại các hàng bị thừa
df = df[df["Rk"] != "Rk"]
# Chuyển các cột số liệu về dạng số
non_numeric = ["Player", "Nation", "Pos", "Squad", "Matches"]
for col in df.columns:
    if col not in non_numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
# Lọc player thi đấu > 90 phút
df = df[df["Min"] > 90]
# Chuyển các chỉ số không có về N/A
df = df.fillna("N/A")

# Ghi kết quả vào SQLite
conn = sqlite3.connect("premier_league.db")
df.to_sql("premier_league_stats", conn, if_exists="replace", index=False)
conn.close()

df.to_csv("premier_league_players.csv", index=False, encoding="utf-8-sig")