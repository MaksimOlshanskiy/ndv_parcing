import json

import pandas as pd

# загружаем заполненный файл с базой недвижимости за последний месяц
df = pd.read_excel(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!haracteristik_dictionary\07.2025_рынок.xlsx")

df = df[['Название проекта',
         'На англ',
         'Промзона',
         'Местоположение',
         'Метро',
         'Расстояние до метро, км',
         'Время до метро, мин',
         'МЦК/МЦД/БКЛ',
         'МЦК/МЦД/БКЛ',
         'Расстояние до МЦК/МЦД, км',
         'Время до МЦК/МЦД, мин',
         'БКЛ',
         'Расстояние до БКЛ, км',
         'Время до БКЛ, мин',
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
with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(projects_dict, f, ensure_ascii=False, indent=4)