import pandas as pd
import json



# Загружаем Excel
df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Ноябрь\База12.xlsx")

# Загружаем JSON
with open("projects.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Добавляем колонки, если их нет
if "Срок сдачи" not in df.columns:
    df["Срок сдачи"] = None
if "Стадия строительной готовности" not in df.columns:
    df["Стадия строительной готовности"] = None

# статистика
rows_updated = 0
rows_skipped = 0

df['Корпус'] = df['Корпус'].astype(str)
df['Корпус'] = df['Корпус'].str.replace(',', '.')

# Заполняем значения
for idx, row in df.iterrows():
    project_key = f"{row['Название проекта']}_{row['Девелопер']}"
    corpus = str(row['Корпус'])

    if project_key in data and corpus in data[project_key]:
        df.at[idx, "Срок сдачи"] = data[project_key][corpus]["Срок сдачи"]
        df.at[idx, "Стадия строительной готовности"] = data[project_key][corpus]["Стадия строительной готовности"]
        df.at[idx, "Договор"] = data[project_key][corpus]["Договор"]
        rows_updated += 1
    else:
        rows_skipped += 1

# сохраняем результат
df.to_excel(r"C:\Users\m.olshanskiy\Desktop\Ноябрь\База13.xlsx", index=False)

# выводим логи
print("=== ЛОГИ ===")
print(f"Всего строк: {len(df)}")
print(f"Обновлено строк: {rows_updated}")
print(f"Пропущено строк (нет в JSON): {rows_skipped}")
print("✅ Файл сохранён")