import pandas as pd
import pyxlsb

# Путь к вашему Excel-файлу
файл = r"C:\Users\m.olshanskiy\Desktop\03-04.2025_РЫНОК.xlsb"

# Загрузка файла
df = pd.read_excel(файл, sheet_name='массив')

# Получение уникальных значений
уникальные_проекты = df["Девелопер"].dropna().unique().tolist()

# Вывод на экран
print(уникальные_проекты)
