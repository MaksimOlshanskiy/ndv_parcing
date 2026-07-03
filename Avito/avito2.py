import pandas as pd

df1 = pd.read_excel(r'C:\PycharmProjects\ndv_parcing\avito.xlsx')
df2 = pd.read_excel(r'C:\PycharmProjects\ndv_parcing\avito_02-07-26.xlsx')

# Удаляем всё после ?
df1['Ссылка'] = df1['Ссылка'].str.split('?').str[0]
df2['Ссылка'] = df2['Ссылка'].str.split('?').str[0]

# Извлекаем ID (последовательность цифр после последнего "_")
df1['id'] = df1['Ссылка'].str.extract(r'_(\d+)$')
df2['id'] = df2['Ссылка'].str.extract(r'_(\d+)$')

# Удаляем из второго датафрейма строки с ID из первого
df2_unique = df2[~df2['id'].isin(df1['id'])].drop(columns='id')

# Сохраняем
df2_unique.to_excel('file2_unique.xlsx', index=False)