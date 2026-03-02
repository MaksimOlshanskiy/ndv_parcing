import pandas as pd
import numpy as np

# Загружаем файлы
df1 = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\База изменяемые данные.xlsx")
df2 = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\НашДомРФ2.xlsx")

df1["ID дом.рф"] = (
    df1["ID дом.рф"]
    .astype("Int64")      # убираем .0
    .astype(str)
)

df2["ID дом.рф"] = df2["ID дом.рф"].astype(str)




cols_to_update = [
    'Распроданность квартир',
    'Количество квартир',
    'Жилая площадь, м²',
    'Дата публикации проекта'
]

df2_src = df2[["ID дом.рф"] + cols_to_update].copy()

df_merged = df1.merge(
    df2_src,
    on="ID дом.рф",
    how="left",
    suffixes=("", "_new")
)

for col in cols_to_update:
    df_merged[col] = np.where(
        df_merged[f"{col}_new"].notna(),
        df_merged[f"{col}_new"],
        df_merged[col]
    )
    df_merged.drop(columns=f"{col}_new", inplace=True)

df1 = df_merged

df1.loc[
    df1["Дата публикации проекта"] == "Сдан",
    "Стадия строительной готовности"
] = "введен"

# Сохраняем результат
df1.to_excel(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!changing_haracteristik_dictionary\База изм хар temp.xlsx", index=False)

print("Готово! Новый файл сохранён.")

