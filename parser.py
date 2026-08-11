import pandas as pd
import os
os.makedirs("input",exist_ok=True)
os.makedirs("output",exist_ok=True)
files = [f for f in os.listdir("input") if f.endswith(".xlsx")]
if files == 0 :
    print("❌ В папке input нет .xlsx файлов!")
    print("Пожалуйста, положите файл(ы) .xlsx в папку input/")
    print("Работа программы завершена досрочно.")
else:
    print("найдено ",len(files)," файлов")
    for file in files:
        try:
            input_path =  os.path.join("input",file)
            output_name = file.replace(".xlsx","_clean.xlsx")
            output_path = os.path.join("output", output_name)
            print("обработка ",file)
            df = pd.read_excel(input_path)
            if "Статус" not in df.columns:
                print(f"  ⚠️ Предупреждение: в файле '{file}' нет колонки 'Статус'!")
                print(f"  ⚠️ Файл скопирован без изменений")
                df.to_excel(output_path,index = False)
                continue
            original_count = len(df)
            df_clean = df[df["Статус"] != "Отменен"]
            removed_count = original_count - len(df_clean)
            df_clean.to_excel(output_path,index=False)
            print(f" ✅ Удалено строк: {removed_count}")
            print(f" ✅ Осталось строк: {len(df_clean)}")
            print(f" ✅ Сохранено: {output_path}")
        except Exception as e:
            print(f"  ❌ Ошибка при обработке файла '{file}': {e}")
