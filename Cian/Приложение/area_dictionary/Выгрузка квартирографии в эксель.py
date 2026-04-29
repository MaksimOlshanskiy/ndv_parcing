import json
import pandas as pd

# Загружаем JSON из файла
with open("normalized_output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []
for project, flats in data.items():
    for area, rooms in flats.items():
        # Пропускаем, если площадь или количество комнат равны '*'
        if area == "*" or rooms == "*":
            continue

        # Пробуем преобразовать площадь в число
        try:
            area_val = float(area)
        except ValueError:
            continue

        rows.append({
            "Название проекта": project,
            "Площадь, кв.м": area_val,
            "Кол-во комнат": rooms
        })

df = pd.DataFrame(rows)

# Сохраняем в Excel
df.to_excel("Квартирография.xlsx", index=False)