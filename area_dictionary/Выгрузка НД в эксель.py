import pandas as pd

# Загружаем исходный Excel
df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Сентябрь последняя.xlsx")

# Оставляем только нужные столбцы
df = df[["Название проекта", "Площадь, кв.м", "Кол-во комнат"]]

df["Название проекта"] = df["Название проекта"].str.lower()

# Фильтруем по условию "Кол-во комнат = Н/Д"
df = df[df["Кол-во комнат"] == "Н/Д"]

# Убираем дубликаты
df = df.drop_duplicates()

# Сохраняем результат
df.to_excel("projects_nd.xlsx", index=False)