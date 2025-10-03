import pandas as pd

# Загружаем исходный файл
df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Новая папка (4)\База 08-09 newest-4.xlsx")

# Фильтрация строк
filtered_df = df[
    df["Срок сдачи"].isna() &
    df["Тип помещения"].isin(["Квартиры", "Апартаменты"])
]

# Оставляем только нужные столбцы
filtered_df = filtered_df[[
    "Название проекта",
    "Девелопер",
    "Корпус",
    "Срок сдачи",
    "Стадия строительной готовности"
]]

# Убираем дубликаты
unique_df = filtered_df.drop_duplicates()


# Сохраняем результат в новый Excel
unique_df.to_excel(r"C:\Users\m.olshanskiy\Desktop\Недостающее.xlsx", index=False)

print("Файл сохранен как output.xlsx")
