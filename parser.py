import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
base_url = "https://habr.com/ru/feed/"
all_page = 6
titeles = []
links = []
pages = []
for page in range(1,all_page):
    if page == 1:
        url = "https://habr.com/ru/feed/"
    else:
        url = f"https://habr.com/ru/feed/page{page}/"
    try:
        time.sleep(1)
        response = requests.get(url,timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("a",class_ = "tm-title__link")
        for item in items:
            titeles.append(item.text)
            links.append(item.get("href"))
            pages.append(page)

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
    "Заголовок": titeles,
    "Ссылка": links
})
df_filtered = df[df["Заголовок"].str.contains("Код|Айти", case = False)]
df_clean = df_filtered.drop_duplicates("Заголовок",keep="first")
df_sorted =df_clean.sort_values("Заголовок",ascending= False)
df_sorted.to_excel("habr_page.xlsx",index=False)