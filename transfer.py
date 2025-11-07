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
import time

def clean_name(name): 
    list = str(name).split()
    if len(list) < 2:
        return name
    index = list.index(list[0], 1)
    return ' '.join(list[:index])


options = Options()
options.add_argument("--start-maximized")
# Giả lập người dùng thật
options.add_argument("user-agent=Mozilla/5.0")
options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

base_url = "https://www.footballtransfers.com/en/transfers/confirmed/most-recent/2024-2025/uk-premier-league/{}"
all_data = []
page = 1

while True:
    url = base_url.format(page)
    driver.get(url)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "transfer-table"))
        )
    except:
        break

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", {"class":"transfer-table"})
    if not table:
        break

    df = pd.read_html(StringIO(str(table)))[0]
    # Chuẩn hóa tên
    df["Player"] = df["Player"].apply(clean_name)
    all_data.append(df)
    page += 1
    time.sleep(1.5)

driver.quit()
# Chuyển all_data thành DataFrame
df_transfer = pd.concat(all_data, ignore_index=True)

conn = sqlite3.connect("premier_league.db")
df_transfer.to_sql("premier_league_transfer", conn, if_exists="replace", index=False)
conn.close()

df_transfer.to_csv("premier_league_transfers_2024_2025.csv", index=False, encoding="utf-8-sig")