import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os
def clean_log_if_large(log_path = "parser.log",max_lines = 50):
    if not os.path.exists(log_path):
        return
    with open(log_path,"r",encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > max_lines:
        with open(log_path,"w",encoding="utf-8") as f:
            f.write(" Лог очищен (было слишком много строк). Последние записи:\n")
            f.writelines(lines[-20:])
def format_habr_date(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime("%d.%m.%Y %H:%M")
    except:
        return date_str
def split_message(text,max_length=4096):
    result = []
    if len(text) <= max_length:
        result.append(text)
    else:
        while len(text) > 0:
            result.append(text[:max_length])
            text = text[max_length:]
    return result
def telegram_send(message,has_new_posts):
    token = "8936642415:AAEAKjoyk1jABLp7T_8VTr-epoUeFZ0pPps"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_id = "1232862626"
    if has_new_posts:
        for chunk in split_message(message):
            if chunk.strip():
                time.sleep(1)
                requests.post(url,data={"chat_id": chat_id, "text": chunk})
    else:
        requests.post(url, data={"chat_id": chat_id, "text": "Новых постов нет"})
    return

log_file = open("parser.log","a", encoding="utf-8")
preservation_file_r= open("sent_posts.txt","r", encoding="utf-8")
preservation_file_a= open("sent_posts.txt","a", encoding="utf-8")
files_in_the_archive = set()
base_url = "https://habr.com/ru/feed/"
titles = []
links = []
pages = []
dates = []
pages_num = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
for headline_title in preservation_file_r:
    files_in_the_archive.add(headline_title.strip())
for page in range(1,3):
    if page == 1:
        url = "https://habr.com/ru/feed/"
    else:
        url = f"https://habr.com/ru/feed/page{page}/"
    try:
        response = requests.get(url,timeout=5,headers = headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("a",class_ = "tm-title__link")
        next_button = soup.find("a",class_ = "tm-pagination__navigation-link")
        if len(items) == 0:
            print("Страница пуста, парсинг завершён")
            log_file.write(f"Страница пуста, парсинг завершён в {datetime.now().strftime('%Y-%m-%d %H:%M')} \n")
            break
        if not next_button:
            print("Страницы закончились")
            log_file.write(f"Страницы закончились в {datetime.now().strftime('%Y-%m-%d %H:%M')} \n")
            break
        for item in items:
            parent = item.find_parent("article") or item.find_parent("div", class_="tm-articles-list__item")
            time_tag = None
            if parent:
                time_tag = parent.find("time", recursive=True)
            titles.append(item.text)
            links.append("https://habr.com" + item.get('href'))
            pages_num.append(page)
            if time_tag:
                dates.append(format_habr_date(time_tag.get("datetime")))
            else:
                time_tag = item.find_next("time") or item.find_previous("time")
                if time_tag:
                    dates.append(format_habr_date(time_tag.get("datetime")))
                else:
                    print(f"Нет даты у поста: {item.text[:50]}...")
                    log_file.write(f"Нет даты у поста: {item.text[:50]}... в {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                    dates.append("")
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


message= "📰 Сегодня на Habr (первые 3 страницы):\n"
limit = 10
new_posts_count = 0
for string in range(min(limit,len(df_sorted))):
    row = df_sorted.iloc[string]
    if row['Ссылка'] not in files_in_the_archive:
        message += f"{string+1}. {row['Заголовок']} - {row['Дата']} - {row['Ссылка']}\n"
        preservation_file_a.write(f"{row['Ссылка']}\n")
        files_in_the_archive.add(f"{row['Ссылка']}")
        new_posts_count += 1
df_sorted.to_excel("data.xlsx",index = False)
df_sorted.to_csv("data.csv",index = False , encoding= "utf-8")
telegram_send(message, new_posts_count > 0)
log_file.close()
preservation_file_r.close()
preservation_file_a.close()

