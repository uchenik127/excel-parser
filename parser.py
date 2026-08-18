import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
base_url = "https://habr.com/ru/feed/"
titles = []
links = []
pages = []
dates = []
pages = 3
pages_num = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
for page in range(1,pages):
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
        next_button = soup.find("a",class_ = "tm-pagination__navigation-link")
        if not next_button:
            print("Страницы закончились")
            break
        if len(items) == 0:
            print("Страница пуста, парсинг завершён")
            break
        for item in items:
            time_tags = soup.find_all("time")
            time_tag = None
            for t in time_tags:
                if t.find_parent("article") and t.find_parent("article").find("a", class_="tm-title__link") == item:
                    time_tag = t
                    break
            titles.append(item.text)
            links.append("https://habr.com" + item.get('href'))
            pages_num.append(page)
            if time_tag:
                dates.append(time_tag.get("datetime"))
            else:
                dates.append("")
                print(f"Ошибка вывода даты стр - {page}")
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
    "Страница" : pages_num,
    "Заголовок": titles,
    "Ссылка": links,
    "Дата" : dates
})
df["Заголовок"] = df["Заголовок"].fillna("")
df["Заголовок"] = df["Заголовок"].astype(str)
df_clean = df.drop_duplicates("Заголовок",keep="first")
df_sorted =df_clean.sort_values("Заголовок",ascending= False)

def telegram_send(message):
    token = "8936642415:AAEAKjoyk1jABLp7T_8VTr-epoUeFZ0pPps"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_id = "1232862626"
    requests.post(url,data={"chat_id": chat_id, "text": message})
    return
message= "📰 Сегодня на Habr (первые 3 страницы):\n"
limit = 10
for string in range(min(limit,len(df_sorted))):
    row = df_sorted.iloc[string]
    message += f"{string+1}. {row['Заголовок']} - {row['Дата']} - {row['Ссылка']}\n"
df_sorted.to_excel("data.xlsx",index = False)
telegram_send(message)

