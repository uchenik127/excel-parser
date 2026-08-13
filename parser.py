import pandas as pd
df = pd.read_excel("parsing_Otdelka_fasada_kamnem.xlsx")
def include_words(text):
    text = str(text).lower()
    if "натуральный" in text and "камень" in text:
        return True
    else:
        return False

df.to_excel("parsing_Otdelka_fasada_kamnem.xlsx")

df["Целевая"]=df["Запрос"].apply(include_words)
df_target = df[df["Целевая"] == True]
df_target = df_target.drop(columns=["Целевая"])
df_target["Длина запроса"] = df_target["Запрос"].str.len()
df_sorted = df_target.sort_values("Длина запроса",ascending=False)
df_sorted.to_excel("filtered_by_natural.xlsx",index=False)
print(f"✅ Осталось запросов: {len(df_sorted)}")
print("✅ Сохранено в filtered_by_natural.xlsx")