import pandas as pd
import os
os.makedirs("input",exist_ok = True)
os.makedirs("output",exist_ok = True)
files = [f for f in os.listdir("input") if f.endswith(".xlsx")]
if not files:
    print("❌ В папке input нет .xlsx файлов!")
    print("Положите файлы и запустите снова.")
else:
    print(f"📁 Найдено файлов: {len(files)}")
    all_data = []
    for file in files:
        input_path = os.path.join("input",file)
        print(f"  📄 Читаю: {file}")
        df = pd.read_excel(input_path)
        df["Источник"] = file
        all_data.append(df)
    merged_df = pd.concat(all_data,ignore_index = True)
    merged_df = merged_df[(merged_df["Статус"] != "Отменен") | (merged_df["Город"] != "Омск")]
    output_path = os.path.join("output","merged_report.xlsx")
    merged_df.to_excel(output_path,index = False)
    print(f"\n✅ Готово! Объединено {len(files)} файлов.")
    print(f"✅ Всего строк: {len(merged_df)}")
    print(f"✅ Сохранено: {output_path}")