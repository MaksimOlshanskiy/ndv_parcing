import json
import pandas as pd
from Developer_dict import name_dict, developer_dict

df = pd.read_excel(r"C:\Users\m.olshanskiy\Desktop\Ноябрь\База11.xlsx")

# df["Название проекта"] = df["Название проекта"].replace(name_dict)
# df["Девелопер"] = df["Девелопер"].replace(developer_dict)

# Загружаем JSON с характеристиками проектов
with open(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!haracteristik_dictionary\projects.json", "r",
          encoding="utf-8") as f:
    projects_dict = json.load(f)

## Готовим название проекта к сопоставлению (убираем «»)
df["project_key"] = (
    df["Название проекта"].astype(str)
        .str.replace("«", "", regex=False)
        .str.replace("»", "", regex=False)
)

# Заполняем характеристики ТОЛЬКО по совпадению Названия проекта
for idx, row in df.iterrows():
    key = row["project_key"]
    if key in projects_dict:
        for col, value in projects_dict[key].items():
            if col in df.columns:
                df.at[idx, col] = value

df.drop(columns=["project_key"], inplace=True)

df.to_excel(r"C:\Users\m.olshanskiy\Desktop\Ноябрь\База11.xlsx", index=False)