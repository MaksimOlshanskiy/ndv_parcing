import pandas as pd
import re

# Загружаем файлы
df1 = pd.read_excel(r"C:\Users\Mi\Downloads\04062026_Города_миллионники_первичка (1).xlsx")  # первый файл (Город, ЖК)
df2 = pd.read_excel(r"C:\Users\Mi\Downloads\052026_Города-миллионники_классы.xlsx", sheet_name='все')  # второй файл (Город, ЖК, Класс)

def clean_jk(series):
    return (
        series.astype(str)
        .str.replace(r'жк', '', regex=True, flags=re.IGNORECASE)  # убрать ЖК
        .str.replace(r'[«»"“”]', '', regex=True)                  # убрать кавычки
        .str.strip()                                              # убрать пробелы
        .str.lower()                                              # всё в нижний регистр
        .str.capitalize()                                         # первая буква большая
    )

# Чистим столбец ЖК в обоих файлах
df1['Название проекта'] = clean_jk(df1['Название проекта'])
df2['Название проекта'] = clean_jk(df2['Название проекта'])

# Объединяем
result = df1.merge(
    df2[['Локация', 'Название проекта', 'Класс']],   # берём только нужные столбцы
    on=['Локация', 'Название проекта'],              # ключи
    how='left'                       # важно! left join
)

print(result.head())

result.to_excel(r"C:\Users\Mi\Downloads\04062026_Города_миллионники_первичка (2).xlsx", index=False)

