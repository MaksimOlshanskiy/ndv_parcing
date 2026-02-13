import pandas as pd
import re

# Загружаем файлы
df1 = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\032025_Города-миллионники.xlsx")  # первый файл (Город, ЖК)
df2 = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\11022026_Города-миллионники_классы.xlsx")  # второй файл (Город, ЖК, Класс)

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
df1['ЖК'] = clean_jk(df1['ЖК'])
df2['ЖК'] = clean_jk(df2['ЖК'])

# Объединяем
result = df1.merge(
    df2[['Город', 'ЖК', 'Класс']],   # берём только нужные столбцы
    on=['Город', 'ЖК'],              # ключи
    how='left'                       # важно! left join
)

print(result.head())

result.to_excel(r'C:\Users\m.olshanskiy\Desktop\11022026_Города-миллионники_классы_result.xlsx', index=False)

