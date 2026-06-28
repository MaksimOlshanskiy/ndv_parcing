import json

with open(r'C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\projects.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

id_map = {}

for project_dev, corps in data.items():
    project, developer = project_dev.split('_', 1)

    for corp, values in corps.items():
        domrf_id = values.get("ID дом.рф")

        if domrf_id:
            id_map[domrf_id] = {
                "Название проекта": project,
                "Застройщик": developer
            }

import pandas as pd

df = pd.read_excel(r'C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-06-23\НашДомРФ_глубже_080626_add.xlsx')


def update_row(row):
    domrf_id = str(row['ID дом.рф'])

    if domrf_id in id_map:
        row['Название проекта'] = id_map[domrf_id]["Название проекта"]
        row['Застройщик'] = id_map[domrf_id]["Застройщик"]

    return row


df = df.apply(update_row, axis=1)
df.to_excel(r'C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-06-23\НашДомРФ_глубже_23062026.xlsx', index=False)