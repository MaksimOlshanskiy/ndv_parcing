import pandas as pd

# Загрузка Excel-файла
file_path = r"C:\Users\m.olshanskiy\Desktop\Test.xlsx"  # Замени на путь к своему файлу
df = pd.read_excel(file_path, sheet_name="Лист1")
print(df)

projects = ["1-й Измайловский", "1-й Ленинградский", "1-й Лермонтовский", "1-й Донской"]

for i in projects:
    mask = df["Название проекта "] == i

    df.loc[mask] = df.loc[mask].ffill()


# Сохраняем результат в новый файл
output_path = r"C:\Users\m.olshanskiy\Desktop\Test_filled.xlsx"
df.to_excel(output_path, index=False)
print(f"Готово! Заполненный файл сохранён как {output_path}")
