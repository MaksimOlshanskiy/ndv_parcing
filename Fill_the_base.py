import pandas as pd
import pyxlsb  # если используется .xlsb, иначе можно не подключать
import win32com.client as win32
import os

# Загрузка Excel-файла
file_path = r"C:\Users\m.olshanskiy\Desktop\Свести\База июнь.xlsx"
df = pd.read_excel(file_path)   # sheet_name="массив"

# Столбцы, в которых нужно заполнить пропуски
columns_to_fill = ['на англ', 'промзона', 'Местоположение',
                   'Метро', 'Расстояние до метро, км',
                   'Время до метро, мин', 'МЦК/МЦД/БКЛ', 'Расстояние до МЦК/МЦД, км',
                   'Время до МЦК/МЦД, мин', 'БКЛ', 'Расстояние до БКЛ, км',
                   'Время до БКЛ, мин', 'старт', 'Комментарий',
                   'Округ', 'Район', 'Адрес', 'Эскроу', 'статус']   # без статуса

columns_to_fill_by_corpus = ['Конструктив', 'Класс', 'Срок сдачи', 'Старый срок сдачи', 'Договор']

df = df.sort_values(by=[])
df = df.sort_values(by=['Дата обновления','Название проекта', 'Девелопер', 'Корпус'])
df['Корпус'] = df['Корпус'].astype(str)

# Группируем по названию проекта и заполняем только нужные столбцы
for col in columns_to_fill:
    df[col] = df.groupby(['Название проекта', 'Девелопер'])[col].ffill()

for col in columns_to_fill_by_corpus:
    df[col] = df.groupby(['Название проекта', 'Девелопер', 'Корпус'])[col].ffill()

# Сохраняем результат
output_path = r"C:\Users\m.olshanskiy\Desktop\База_Июнь_Result.xlsx"
df.to_excel(output_path, index=False)
print(f"Готово! Заполненный файл сохранён как {output_path}")


