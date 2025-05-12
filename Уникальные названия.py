import pandas as pd
import pyxlsb

# Путь к вашему Excel-файлу
файл = r"C:\Users\m.olshanskiy\Desktop\Feb-april_filled.xlsb"

# Загрузка файла
df = pd.read_excel(файл)

# Получение уникальных значений
уникальные_проекты = df["Название проекта "].dropna().unique().tolist()

# Вывод на экран
print(уникальные_проекты)
