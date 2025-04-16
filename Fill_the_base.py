import pandas as pd
import pyxlsb

# Загрузка Excel-файла
file_path = r"C:\Users\m.olshanskiy\Desktop\Test.xlsx"
df = pd.read_excel(file_path, sheet_name="массив")    # sheet_name="название листа"  если нужен конкретный лист
print(df)

unique_projects = df['Название проекта '].unique()

# Преобразование в список (если нужно именно список)
projects = unique_projects.tolist()

for i in projects:
    mask = df["Название проекта "] == i

    df.loc[mask, :] = df.loc[mask, :].ffill()


# Сохраняем результат в новый файл
output_path = r"C:\Users\m.olshanskiy\Desktop\Test_filled.xlsx"
df.to_excel(output_path, index=False)
print(f"Готово! Заполненный файл сохранён как {output_path}")
