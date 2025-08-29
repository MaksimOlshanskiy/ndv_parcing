import pandas as pd
import json

# читаем excel
df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\База проектов2.xlsx")

# создаем новый столбец-ключ = Название проекта + "_" + Девелопер
df["primary_key"] = df["Название проекта"].astype(str) + "_" + df["Девелопер"].astype(str)

# формируем словарь: ключ = primary_key, значение = все остальные колонки (кроме primary_key)
projects_dict = df.set_index("primary_key").drop(columns=["Название проекта", "Девелопер"]).to_dict(orient="index")

# сохраняем в JSON
with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(projects_dict, f, ensure_ascii=False, indent=4)