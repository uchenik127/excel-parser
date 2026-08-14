import requests
from bs4 import BeautifulSoup
import pandas as pd
response = requests.get("https://news.ycombinator.com/")
if response.status_code != 200:
    print(f"Ошибка {response.status_code}")
    exit()
soup = BeautifulSoup(response.text,"html.parser")
items = soup.find_all("span", class_ = "titleline")
titles = []
linkes = []
for item in items:
    if item.find("a"):
        titles.append(item.find("a").text)
        linkes.append(item.find("a").get("href"))

df = pd.DataFrame({
    "Заголовок" : titles,
    "Ссылка" : linkes
})
for title in titles:
    if not("AI" in title or "Python" in title):
        titles.pop(title)
df_sorted = df.sort_values("Заголовок", ascending=False)
df_clean = df_sorted.drop_duplicates("Заголовок", keep="first")