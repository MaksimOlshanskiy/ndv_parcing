import json
import pandas as pd
from Developer_dict import name_dict, developer_dict

df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Прогнать.xlsx")

df["Название проекта"] = df["Название проекта"].replace(name_dict)
df["Девелопер"] = df["Девелопер"].replace(developer_dict)

# Загружаем JSON с характеристиками проектов
with open(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!haracteristik_dictionary\projects.json", "r",
          encoding="utf-8") as f:
    projects_dict = json.load(f)

# создаем ключ из Названия проекта и Девелопера
df["primary_key"] = (
        df["Название проекта"].astype(str)
        .str.replace("«", "", regex=False)
        .str.replace("»", "", regex=False)
        + "_" +
        df["Девелопер"].astype(str)
)

# заполняем характеристиками из JSON
for idx, row in df.iterrows():
    key = row["primary_key"]
    if key in projects_dict:
        for col, value in projects_dict[key].items():
            # заполняем только если колонка есть в df
            if col in df.columns:
                df.at[idx, col] = value

df.drop(columns=["primary_key"], inplace=True)

df.to_excel(r"C:\Users\m.olshanskiy\Desktop\Прогнать2.xlsx")