import pandas as pd
import json
import os

'''
Скрипт для обновления json файла из базы изменяемых характеристик
'''

# читаем файл
df = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\База изменяемые данные_NEWW.xlsx")

# удаляем дубликаты по ключам
print(df.columns.tolist())
df = df.drop_duplicates(subset=["Название проекта", "Девелопер", "Корпус", "Договор", "id", "ID дом.рф"])

# пробуем загрузить старый JSON (если он есть)
if os.path.exists("projects.json"):
    with open("projects.json", "r", encoding="utf-8") as f:
        old_result = json.load(f)
else:
    old_result = {}

new_result = dict(old_result)  # копия, чтобы обновлять

# статистика
stats = {
    "projects_added": 0,
    "projects_updated": 0,
    "corpus_added": 0,
    "corpus_updated": 0
}

for _, row in df.iterrows():
    project_key = f"{row['Название проекта']}_{row['Девелопер']}"
    corpus = str(row['Корпус'])
    srok = str(row['Срок сдачи'])
    stage = str(row['Стадия строительной готовности'])
    ddu = str(row['Договор'])
    id = str(row['id'])
    id_domrf = str(row['ID дом.рф'])

    # 🔥 Новые поля
    status = str(row.get("Статус", ""))
    sold = str(row.get("Распроданность квартир", ""))
    flats = str(row.get("Количество квартир", ""))
    area = str(row.get("Жилая площадь, м²", ""))

    new_fields = {
        "Срок сдачи": srok,
        "Стадия строительной готовности": stage,
        "Договор": ddu,
        "id": id,
        "ID дом.рф": id_domrf,
        "Статус": status,
        "Распроданность квартир": sold,
        "Количество квартир": flats,
        "Жилая площадь, м²": area
    }

    # если проект новый
    if project_key not in new_result:
        new_result[project_key] = {corpus: new_fields}
        stats["projects_added"] += 1
        stats["corpus_added"] += 1
        continue

    # если корпус новый
    if corpus not in new_result[project_key]:
        new_result[project_key][corpus] = new_fields
        stats["corpus_added"] += 1
        stats["projects_updated"] += 1
        continue

    # если корпус есть, но данные изменились
    old_data = new_result[project_key][corpus]
    if any(old_data.get(k) != v for k, v in new_fields.items()):
        new_result[project_key][corpus] = new_fields
        stats["corpus_updated"] += 1
        stats["projects_updated"] += 1

# сохраняем новый JSON
with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(new_result, f, ensure_ascii=False, indent=4)

# выводим логи
print("=== Изменяемые характеристики ===")
print(f"✅ Добавлено проектов: {stats['projects_added']}")
print(f"🔁 Обновлено проектов: {stats['projects_updated']}")
print(f"🔁 Добавлено корпусов: {stats['corpus_added']}")
print(f"✅ Обновлено корпусов: {stats['corpus_updated']}")