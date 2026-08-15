import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Базовый URL
hacker_url = "https://news.ycombinator.com"
bbs_url = "https://www.bbc.com/news/technology"
def get_news_from_page(url):
    """Парсит одну страницу Hacker News, возвращает списки заголовков и ссылок"""
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return [], []

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("span", class_="titleline")

    titles = []
    links = []

    for item in items:
        link = item.find("a")
        if link:
            titles.append(link.text)
            links.append(link.get("href"))

    return titles, links

# 1. Парсим первую страницу
titles_1, links_1 = get_news_from_page(hacker_url)
print(f"Страница 1: собрано {len(titles_1)} новостей")
titles_2, links_2 = get_news_from_page(bbs_url)
print(f"Страница 2: собрано {len(titles_2)} новостей")
df1 = pd.DataFrame({
    "Заголовок" : titles_1,
    "Ссылка" : links_1,
    "Источник" : "Hacker news"
})
df2 = pd.DataFrame({
    "Заголовок" : titles_2,
    "Ссылка" : links_2,
    "Источник" : "BBC news"
})
df = pd.concat([df1,df2], ignore_index= True)

# 7. Фильтрация по ключевым словам
df_filtered = df[df["Заголовок"].str.contains("AI|Python", case=False)]

# 8. Удаление дубликатов
df_clean = df_filtered.drop_duplicates("Заголовок", keep="first")

# 9. Сортировка
df_sorted = df_clean.sort_values("Заголовок", ascending=False)

# 10. Сохранение
df_sorted.to_excel("hackernews_pagination.xlsx", index=False)

print(f"✅ Собрано новостей с двух страниц: {len(df_sorted)}")
print("✅ Сохранено в hackernews_pagination.xlsx")