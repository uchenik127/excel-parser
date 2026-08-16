import pandas as pd
from bs4 import BeautifulSoup
import requests
url = "https://habr.com/ru/feed/"
try:
    response = requests.get(url,timeout= 5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("a", class_="tm-title__link")
    titles = []
    linkes = []
    for item in items:
        titles.append(item.text)
        linkes.append(item.get("href"))
    df = pd.DataFrame({
        "Заголовок" : titles,
        "Ссылка" : linkes
    })
    df_filtred = df[df["Заголовок"].str.contains('вайбкодим|правда',case = False)]
    df_sorted = df_filtred.sort_values("Заголовок",ascending= False)
    df_clean = df_sorted.drop_duplicates("Заголовок",keep= "first")
    df_clean.to_excel("habr_all_filtred.xlsx",index= False)
except requests.HTTPError:
    print("Ошибка сайт не отвечает")
except requests.Timeout:
    print("Ошибка сайт слишком долго грузит")
except requests.ConnectionError:
    print("Ошибка не удалось подключится к сайту")
except Exception as e:
    print(f"Ошибка {e}")
