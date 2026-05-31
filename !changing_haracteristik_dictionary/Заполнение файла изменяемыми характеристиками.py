import pandas as pd
import json

# Загружаем Excel
df = pd.read_excel(r"C:\Users\Mi\OneDrive\Desktop\База апрель\База Апрель.xlsx")

# Загружаем JSON
with open(r"C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\projects.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Добавляем колонки, если их нет
required_columns = [
    "Срок сдачи",
    "Стадия строительной готовности",
    "Договор",
    "Статус",
    "Распроданность квартир",
    "Количество квартир",
    "Жилая площадь, м²"
]

for col in required_columns:
    if col not in df.columns:
        df[col] = None

# статистика
rows_updated = 0
rows_skipped = 0

# Нормализация корпуса
df['Корпус'] = df['Корпус'].astype(str)
df['Корпус'] = df['Корпус'].str.replace(',', '.', regex=False)

# Заполняем значения
for idx, row in df.iterrows():
    project_key = f"{row['Название проекта']}_{row['Девелопер']}"
    corpus = str(row['Корпус'])

    if project_key in data and corpus in data[project_key]:

        record = data[project_key][corpus]

        df.at[idx, "Срок сдачи"] = record.get("Срок сдачи")
        df.at[idx, "Стадия строительной готовности"] = record.get("Стадия строительной готовности")
        df.at[idx, "Договор"] = record.get("Договор")
        df.at[idx, "Статус"] = record.get("Статус")
        df.at[idx, "Распроданность квартир"] = record.get("Распроданность квартир")
        df.at[idx, "Количество квартир"] = record.get("Количество квартир")
        df.at[idx, "Жилая площадь, м²"] = record.get("Жилая площадь, м²")

        rows_updated += 1
    else:
        rows_skipped += 1

df["Количество квартир"] = (
    df["Количество квартир"]
    .astype(str)
    .str.replace(r"[^\d\.]", "", regex=True)  # убираем всё лишнее
    .replace("", None)
    .astype(float)
    .astype("Int64")  # целое число без .0 (поддерживает NaN)
)

# Преобразуем "Жилая площадь, м²"
df["Жилая площадь, м²"] = (
    df["Жилая площадь, м²"]
    .astype(str)
    .str.replace(r"[^\d\.]", "", regex=True)
    .replace("", None)
    .astype(float)
    .astype("Int64")
)

# сохраняем результат
df.to_excel(r"C:\Users\Mi\OneDrive\Desktop\База апрель\База Апрель.xlsx", index=False)

# выводим логи
print("=== 🔥 ЛОГИ 🔥 ===")
print(f"Всего строк: {len(df)}")
print(f"Обновлено строк: {rows_updated}")
print(f"Пропущено строк (нет в JSON): {rows_skipped}")
print("✅ Файл сохранён")