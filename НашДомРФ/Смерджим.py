import pandas as pd

# Пути к файлам
file_1 = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\НашДомРФ\2026-01-13\Список ЖК по классам.xlsx"
file_2 = r"C:\НашДомРФ\2026-01-13\Мо_НашДомРФ_2026-01-13.xlsx"

# Читаем файлы
df1 = pd.read_excel(file_1)
df2 = pd.read_excel(file_2)

# На всякий случай проверим типы
df1["id"] = df1["id"].astype(str)
df2["id"] = df2["id"].astype(str)

# Merge по id
df_merged = df1.merge(
    df2,
    on="id",
    how="inner"   # можно поменять на 'inner' или 'outer'
)

df_merged = df_merged.drop_duplicates(
    subset=["id", "devEmail", "devPhoneNum"],
    keep="first"   # можно 'last'
)

# Сохранение результата
output_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\НашДомРФ\2026-01-13\Результат.xlsx"
df_merged.to_excel(output_path, index=False)

print("Merged file saved to:", output_path)