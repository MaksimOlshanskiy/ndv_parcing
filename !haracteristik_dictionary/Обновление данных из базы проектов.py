import pandas as pd
import json
import os
import numpy as np

def normalize_value(v):
    """Приведение значений к единому виду для корректного сравнения"""
    if pd.isna(v):   # NaN -> None
        return None
    if isinstance(v, str):
        return v.strip()
    if isinstance(v, (np.int64, np.float64)):
        if float(v).is_integer():
            return int(v)
        return float(v)
    return v

# загружаем Excel
df = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\Рабочие для базы\База проектов.xlsx")

lower_words = {'на', 'в', 'и', 'с', 'к', 'у', 'о', 'от', 'по', 'за', 'из', 'над', 'под', 'об', 'же', 'ли', 'бы'}

def correct_title(text):
    if not isinstance(text, str):
        return text
    # Разбиваем на слова
    words = text.lower().split()
    # Первое слово всегда с большой буквы
    result = [words[0].capitalize()]
    # Остальные слова: если в списке исключений -> оставляем маленькими, иначе с большой
    for word in words[1:]:
        if word in lower_words:
            result.append(word)
        else:
            result.append(word.capitalize())
    return ' '.join(result)


# создаем новый столбец-ключ = только Название проекта
df["primary_key"] = (
    df["Название проекта"]
        .astype(str)
        .apply(correct_title)
        .str.strip()
        .str.replace("«", "", regex=False)
        .str.replace("»", "", regex=False)
)

# нормализуем значения
try:
    df = df.map(normalize_value)  # pandas >= 2.2
except AttributeError:
    df = df.applymap(normalize_value)

df['id'] = df['id'].astype(str).str.replace(".0", "")

# формируем словарь из Excel (удаляем только Название проекта — теперь девелопер сохраняется)
projects_dict = (
    df
    .set_index("primary_key")
    .drop(columns=["Название проекта"])  # девелопер теперь НЕ участвует в ключе, но остаётся в данных
    .to_dict(orient="index")
)

# читаем старый JSON (если он есть)
old_projects = {}
if os.path.exists("projects.json"):
    with open("projects.json", "r", encoding="utf-8") as f:
        old_projects = json.load(f)

# считаем изменения
new_count = 0
updated_projects_count = 0
updated_cells_count = 0

for key, new_values in projects_dict.items():
    if key not in old_projects:
        new_count += 1
    else:
        old_values = {k: normalize_value(v) for k, v in old_projects[key].items()}
        changes_in_project = 0
        for col, new_val in new_values.items():
            old_val = old_values.get(col)
            if old_val != new_val:
                updated_cells_count += 1
                changes_in_project += 1
        if changes_in_project > 0:
            updated_projects_count += 1

# сохраняем новый JSON
with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(projects_dict, f, ensure_ascii=False, indent=4)

print("=== Неизменяемые характеристики ===")
print(f"✅ Новых проектов добавлено: {new_count}")
print(f"🔁 Проектов обновлено: {updated_projects_count}")
print(f"🔁 Ячеек обновлено: {updated_cells_count}")
print(f"✅ Всего проектов в базе: {len(projects_dict)}")