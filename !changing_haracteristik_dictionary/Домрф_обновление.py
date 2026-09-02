import pandas as pd
import numpy as np

'''
проверять названия столбцов
'''

# Загружаем файлы
df1 = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\Рабочие для базы\База изменяемые данные.xlsx")
df2 = pd.read_excel(r"C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-08-24\Нашдомрф 08-24.xlsx", sheet_name='Sheet1')


df1["ID дом.рф"] = (
    df1["ID дом.рф"]
    .astype("Int64")      # убираем .0
    .astype(str)
)

df2["ID дом.рф"] = df2["ID дом.рф"].astype(str)

cols_to_update = [
    "Срок сдачи",
    'Распроданность квартир',
    'Количество квартир',
    'Жилая площадь, м²',
    'Готовность'
]

df2_src = df2[["ID дом.рф"] + cols_to_update].copy()

df_merged = df1.merge(
    df2_src,
    on="ID дом.рф",
    how="left",
    suffixes=("", "_new")
)



print(df_merged.info())


for col in cols_to_update:
    df_merged[col] = np.where(
        df_merged[f"{col}_new"].notna(),
        df_merged[f"{col}_new"],
        df_merged[col]
    )
    df_merged.drop(columns=f"{col}_new", inplace=True)


df1 = df_merged



df1.loc[
    df1["Готовность"] == "Сдан",
    "Стадия строительной готовности"
] = "введен"

print(df1.info())

# Сохраняем результат
df1.to_excel(r"C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\База изм хар август.xlsx", index=False)

print("Готово! Новый файл сохранён.")

