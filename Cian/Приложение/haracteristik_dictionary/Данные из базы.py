import json

import pandas as pd

# загружаем заполненный файл с базой недвижимости за последний месяц
df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\База по годам\2025 новая\07-08.2025_рынок.xlsx")

df = df[['Название проекта',
         'На англ',
         'Промзона',
         'Местоположение',
         'Метро',
         'Расстояние до метро, км',
         'Время до метро, мин',
         'Мцк/мцд/бкл',
         'Расстояние до мцк/мцд, км',
         'Время до мцк/мцд, мин',
         'Бкл',
         'Расстояние до бкл, км',
         'Время до бкл, мин',
         'Статус',
         'Девелопер',
         'Округ',
         'Район',
         'Эскроу',
         'Конструктив',
         'Класс']].drop_duplicates()

# создаем новый столбец-ключ = Название проекта + "_" + Девелопер
df["primary_key"] = df["Название проекта"].astype(str) + "_" + df["Девелопер"].astype(str)

# формируем словарь: ключ = primary_key, значение = все остальные колонки (кроме primary_key)
projects_dict = df.set_index("primary_key").drop(columns=["Название проекта", "Девелопер"]).to_dict(orient="index")

# сохраняем в JSON
with open("projects_new.json", "w", encoding="utf-8") as f:
    json.dump(projects_dict, f, ensure_ascii=False, indent=4)