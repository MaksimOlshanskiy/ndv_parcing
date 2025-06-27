import os
import glob
import pandas as pd

# Путь к папке, где находятся Excel файлы
path1 = r"C:\Users\m.olshanskiy\Desktop\Нашдом глубже\НашДом.xlsx"
path2 = r"C:\Users\m.olshanskiy\Desktop\Нашдом глубже\НашДомГлубже.xlsx"


df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)
print(df1.info())
print(df2.info())
result = pd.merge(df1, df2, on='id', how='left')



# Сохраняем объединённые данные в новый Excel файл

result.to_excel('C:/Users/m.olshanskiy/PycharmProjects/ndv_parsing/НашДомРФ/2025-06-17/НашДомRes.xlsx', index=False)
