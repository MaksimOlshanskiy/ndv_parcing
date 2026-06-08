import pandas as pd
import numpy as np

# Загружаем файлы
df1 = pd.read_excel(r"C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\База изм хар май.xlsx")
df2 = pd.read_excel(r"C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-06-08\НашДомРФ_глубже_080626_add.xlsx")


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
df1.to_excel(r"C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\База изм хар июнь.xlsx", index=False)

print("Готово! Новый файл сохранён.")

