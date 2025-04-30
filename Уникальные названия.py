import pandas as pd

# Путь к вашему Excel-файлу
файл = r"C:\Users\Mi\OneDrive\Desktop\База\Февраль.xlsx"

# Загрузка файла
df = pd.read_excel(файл)

# Получение уникальных значений
уникальные_проекты = df["Девелопер"].dropna().unique().tolist()

# Вывод на экран
print(уникальные_проекты)
