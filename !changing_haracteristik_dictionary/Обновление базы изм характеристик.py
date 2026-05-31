import pandas as pd
import json
import os
from datetime import datetime

'''
Скрипт для обновления json файла из базы изменяемых характеристик
'''

# читаем файл
df = pd.read_excel(r"C:\PycharmProjects\ndv_parcing\!changing_haracteristik_dictionary\База изм хар май.xlsx")



df["id"] = (
    df["id"]
    .dropna()
    .astype("int64")
    .astype(str)
    .reindex(df.index)
)

df["ID дом.рф"] = (
    df["ID дом.рф"]
    .dropna()
    .astype("int64")
    .astype(str)
    .reindex(df.index)
)

df["Распроданность квартир"] = (
    df["Распроданность квартир"]
    .astype(str)
    .str.replace("%", "", regex=False)  # убираем %
    .str.replace(",", ".", regex=False) # если вдруг 50,5%
)

# df["Распроданность квартир"] = pd.to_numeric(
#     df["Распроданность квартир"],
#     errors="coerce"
# ) / 100


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
    "corpus_updated": 0,

}
today = pd.Timestamp(datetime.today().date())

quarter_map = {
    "1": "03-31",
    "2": "06-30",
    "3": "09-30",
    "4": "12-31"
}

tmp = df["Срок сдачи"].astype(str).str.extract(
    r"(?P<quarter>[1-4])\s*кв\s*(?P<year>\d{4})"
)

df["Дата сдачи"] = pd.to_datetime(
    tmp["year"] + "-" + tmp["quarter"].map(quarter_map),
    errors="coerce"
)


# # заполнение дат смены статуса, там где не заполнено
# mask_base = (
#     df["Дата сдачи"].notna() &
#     df["stage_2_date"].isna() &
#     df["stage_3_date"].isna()
# )
#
# mask_initial = mask_base & (df["Стадия строительной готовности"] == "начальный цикл")
# mask_монтаж = mask_base & (df["Стадия строительной готовности"] == "монтажные работы")
#
# days_to_finish_initial = (
#     (df.loc[mask_initial, "Дата сдачи"] - today)
#     .dt.days
#     .div(3)
#     .round()
#     .astype("Int64")
# )
#
# df.loc[mask_initial, "stage_2_date"] = today + pd.to_timedelta(
#     days_to_finish_initial, unit="D"
# )
#
# df.loc[mask_initial, "stage_3_date"] = (
#     df.loc[mask_initial, "stage_2_date"] +
#     pd.to_timedelta(days_to_finish_initial, unit="D")
# )
#
# days_to_finish_монтаж = (
#     (df.loc[mask_монтаж, "Дата сдачи"] - today)
#     .dt.days
#     .div(2)
#     .round()
#     .astype("Int64")
# )
#
# df.loc[mask_монтаж, "stage_3_date"] = today + pd.to_timedelta(
#     days_to_finish_монтаж, unit="D"
# )

# обновляем Договор
df['Договор'] = df['Стадия строительной готовности'].apply(
    lambda x: 'ДКП' if x == 'введен' else 'ДДУ')


# for idx, row in df.iterrows():
#     stage_2_date = row.get("stage_2_date")
#     stage_3_date = row.get("stage_3_date")
#
#     stage = row["Стадия строительной готовности"]
#
#     if stage != "введен":
#         if pd.notna(stage_3_date) and today >= stage_3_date:
#             stage = "завершающий цикл"
#         elif pd.notna(stage_2_date) and today >= stage_2_date:
#             stage = "монтажные работы"
#
#     # 🔥 ОБНОВЛЯЕМ DATAFRAME
#     df.loc[idx, "Стадия строительной готовности"] = stage

for _, row in df.iterrows():
    project_key = f"{row['Название проекта']}_{row['Девелопер']}"
    corpus = str(row['Корпус'])
    srok = str(row['Срок сдачи'])
    stage_2_date = row.get("stage_2_date")
    stage_3_date = row.get("stage_3_date")
    stage = str(row['Стадия строительной готовности'])
    ddu = str(row['Договор'])
    id = str(row['id'])
    id_domrf = str(row['ID дом.рф'])

    # 🔥 Новые поля
    status = str(row.get("Статус", ""))
    sold = row.get("Распроданность квартир")

    if pd.isna(sold):
        sold = None

    flats = str(row.get("Количество квартир", ""))
    area = str(row.get("Жилая площадь, м²", ""))


    today = pd.Timestamp(datetime.today().date())

    new_fields = {
        "Срок сдачи": srok,
        "Стадия строительной готовности": stage,
        "Договор": ddu,
        "id": id,
        "ID дом.рф": id_domrf,
        "Статус": status,
        "Распроданность квартир": sold,
        "Количество квартир": flats,
        "Жилая площадь, м²": area,
        "stage_2_date": stage_2_date.isoformat() if pd.notna(stage_2_date) else None,
        "stage_3_date": stage_3_date.isoformat() if pd.notna(stage_3_date) else None
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

print(df.info())

# обновляем ссылку на дом.рф

BASE_URL = (
    "https://xn--80az8a.xn--d1aqf.xn--p1ai/"
    "%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/"
    "%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3-%D0%BD%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D1%80%D0%BE%D0%B5%D0%BA/"
    "%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82/"
)

mask_link = df["ID дом.рф"].notna()

df.loc[mask_link, "Ссылка"] = (
    BASE_URL + df.loc[mask_link, "ID дом.рф"].astype(str)
)

# сохраняем новый JSON
with open("projects.json", "w", encoding="utf-8") as f:
    json.dump(new_result, f, ensure_ascii=False, indent=4)

df.to_excel(
    r"\\192.168.252.25\аналитики\ОТЧЕТЫ\База изменяемые данные temp.xlsx",
    index=False
)

# выводим логи
print("=== Изменяемые характеристики ===")
print(f"✅ Добавлено проектов: {stats['projects_added']}")
print(f"🔁 Обновлено проектов: {stats['projects_updated']}")
print(f"🔁 Добавлено корпусов: {stats['corpus_added']}")
print(f"✅ Обновлено корпусов: {stats['corpus_updated']}")