import pandas as pd
import re

# Замените на путь к вашему файлу
файл_вход = r"C:\Users\m.olshanskiy\Desktop\Апрель_итог2.xlsx"
файл_выход = r"C:\Users\m.olshanskiy\Desktop\очищенный_файл3.xlsx"

# Загрузка файла
df = pd.read_excel(файл_вход)

# Удаление слова "Корпус" (в любом регистре, с/без пробела)

# df["Корпус"] = (
#     df["Корпус"]
#     .astype(str)  # приводим всё к строкам
#     .str.replace(r'(?i)\bкорпус\b\.?\s*', '', regex=True)  # удаляем "корпус"
#     .str.strip()  # убираем лишние пробелы
#     .replace(['', '-', 'nan', 'NaN'], '1')  # заменяем пустые строки и текстовые NaN на "1"
# )

# ⬇️ Вот здесь — обновлённая строка преобразования:
df['Дата обновления'] = pd.to_datetime(df['Дата обновления'], format='mixed', dayfirst=True, errors='coerce')

# # Сохранение результата
# df.to_excel(файл_выход, index=False)
#
# print("Готово! Файл сохранён как", файл_выход)

# Экспорт в Excel с нужным форматированием
with pd.ExcelWriter('отчет.xlsx', engine='xlsxwriter', date_format='dd.mm.yyyy') as writer:
    df.to_excel(writer, index=False, sheet_name='Данные')

    workbook  = writer.book
    worksheet = writer.sheets['Данные']

    # Формат для даты
    date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})

    # Установим ширину колонок и применим формат к столбцу с датой
    for i, column in enumerate(df.columns):
        # Примерная автоширина по длине названия и данных
        column_len = max(df[column].astype(str).map(len).max(), len(column)) + 2
        worksheet.set_column(i, i, column_len)

        # Применим формат даты к нужному столбцу
        if column == 'Дата обновления':
            worksheet.set_column(i, i, column_len, date_format)

    # Включим автофильтр по всем столбцам
    worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)