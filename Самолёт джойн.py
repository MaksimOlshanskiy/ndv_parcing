import pandas as pd

# читаем файлы
df1 = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Самолет_НОВА_2026-04-10-ешки.xlsx")  # первый файл
df2 = pd.read_excel(r'C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\1_FILES\2026-04-10\Самолет_НОВА_2026-04-10-ешки2.xlsx')  # второй файл

# оставляем только нужные столбцы из второго файла
df2_small = df2[['Старт', 'Кол-во комнат']]

# объединяем
result = df1.merge(df2_small, on='Старт', how='left')

# сохраняем результат
result.to_excel('Samolet.xlsx', index=False)