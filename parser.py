import pandas as pd
from bs4 import BeautifulSoup
import requests
url1 = "https://habr.com/ru/feed/"
url2 = "https://habr.com/ru/feed/page2/"
def all_titels_and_links(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка")
        return [],[]
    soup = BeautifulSoup(response.text)
    items = soup.find_all( "h2",class_="tm-title tm-title_h2 title")
    titles = []
    linkes = []
    for item in items:
        find = item.find("a")
        if find:
            titles.append(find.text)
            linkes.append(find.get("href"))
    return titles, linkes
titles1,linkes1 = all_titels_and_links(url1)
print(f'Получено {len(titles1)} строк')
titles2,linkes2 = all_titels_and_links(url2)
print(f'Получено {len(titles2)} строк')
titles1.extend(titles2)
linkes1.extend(linkes2)
df = pd.DataFrame({
    "Заголовок" : titles1,
    "Ссылка" : linkes1
})
df_filtred = df[df["Заголовок"].str.contains("Рынок|Цены",case = False)]
df_sorted =df_filtred.sort_values("Заголовок",ascending=False)
df_clean = df_sorted.drop_duplicates("Заголовок",keep="first")
df_clean.to_excel("habr.xlsx",index=False)