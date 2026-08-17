import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
base_url = "https://habr.com/ru/feed/"
titles = []
links = []
pages = []
dates = []
page = 1
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
while True:
    if page == 1:
        url = "https://habr.com/ru/feed/"
    else:
        url = f"https://habr.com/ru/feed/page{page}/"
    try:
        time.sleep(1)
        response = requests.get(url,timeout=5,headers = headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("a",class_ = "tm-title__link")
        next_button = soup.find_all("a",class_ = "tm-pagination__navigation-link-title",string="Туда")
        if not next_button:
            print("Страницы закончились")
            break
        if len(items) == 0:
            print("Страница пуста, парсинг завершён")
            break
        for item in items:
            time_tag = item.find("time")
            titles.append(item.text)
            links.append("https://habr.com" + item.get('href'))
            pages.append(page)
            if time_tag:
                dates.append(time_tag.get("datetime"))
            else:
                dates.append("")
                print(f"Ошибка вывода даты стр - {page}")
        page += 1
    except requests.Timeout:
        print("Ошибка сервер долго грузится")
        break
    except requests.ConnectionError:
        print("Ошибка не получилось загрузить сервер")
        break
    except Exception as e:
        print(f"Ошибка {e}")
        break
df = pd.DataFrame({
    "Страница" : pages,
    "Заголовок": titles,
    "Ссылка": links,
    "Дата" : dates
})
df_filtered = df[df["Заголовок"].str.contains("Код|Айти", case = False)]
df_clean = df_filtered.drop_duplicates("Заголовок",keep="first")
df_sorted =df_clean.sort_values("Заголовок",ascending= False)
df_sorted.to_excel("habr_page.xlsx",index=False)
df_sorted.to_csv("habr_page.csv",index=False,encoding="utf-8-sig")
