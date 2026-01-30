
def update_all_base():

    import pandas as pd
    import json
    import os
    import numpy as np

    def normalize_value(v):
        """Приведение значений к единому виду для корректного сравнения"""
        if pd.isna(v):  # NaN -> None
            return None
        if isinstance(v, str):
            return v.strip()  # убираем пробелы
        if isinstance(v, (np.int64, np.float64)):
            # если число без дробной части -> int
            if float(v).is_integer():
                return int(v)
            return float(v)
        return v

    # загружаем Excel
    df = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\База проектов.xlsx")

    # создаем новый столбец-ключ = Название проекта + "_" + Девелопер
    df["primary_key"] = df["Название проекта"].astype(str).str.strip() + "_" + df["Девелопер"].astype(str).str.strip()

    # нормализуем значения в датафрейме
    try:
        df = df.map(normalize_value)  # pandas >= 2.2
    except AttributeError:
        df = df.applymap(normalize_value)  # старые версии pandas

    df['id'] = df['id'].astype(str).str.replace(".0", "")

    # формируем словарь из Excel
    projects_dict = df.set_index("primary_key").drop(columns=["Название проекта", "Девелопер"]).to_dict(orient="index")

    # читаем старый JSON (если он существует)
    old_projects = {}
    if os.path.exists("!haracteristik_dictionary/projects.json"):
        with open("!haracteristik_dictionary/projects.json", "r", encoding="utf-8") as f:
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
    with open("!haracteristik_dictionary/projects.json", "w", encoding="utf-8") as f:
        json.dump(projects_dict, f, ensure_ascii=False, indent=4)

    print("=== Неизменяемые характеристики ===")
    print(f"✅ Новых проектов добавлено: {new_count}")
    print(f"🔁 Проектов обновлено: {updated_projects_count}")
    print(f"🔁 Ячеек обновлено: {updated_cells_count}")
    print(f"✅ Всего проектов в базе: {len(projects_dict)}")


    # читаем файл
    df = pd.read_excel(r"\\192.168.252.25\аналитики\ОТЧЕТЫ\База изменяемые данные.xlsx")

    # удаляем дубликаты по ключам
    df = df.drop_duplicates(subset=["Название проекта", "Девелопер", "Корпус", "Договор"])

    # пробуем загрузить старый JSON (если он есть)
    if os.path.exists(r"/!changing_haracteristik_dictionary/projects_old.json"):
        with open(r"/!changing_haracteristik_dictionary/projects_old.json", "r", encoding="utf-8") as f:
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

        # если проект новый
        if project_key not in new_result:
            new_result[project_key] = {
                corpus: {"Срок сдачи": srok, "Стадия строительной готовности": stage, "Договор": ddu}
            }
            stats["projects_added"] += 1
            stats["corpus_added"] += 1
            continue

        # если корпус новый
        if corpus not in new_result[project_key]:
            new_result[project_key][corpus] = {
                "Срок сдачи": srok,
                "Стадия строительной готовности": stage,
                "Договор": ddu
            }
            stats["corpus_added"] += 1
            stats["projects_updated"] += 1
            continue

        # если корпус есть, но данные изменились
        old_data = new_result[project_key][corpus]
        if old_data["Срок сдачи"] != srok or old_data["Стадия строительной готовности"] != stage:
            new_result[project_key][corpus]["Срок сдачи"] = srok
            new_result[project_key][corpus]["Стадия строительной готовности"] = stage
            new_result[project_key][corpus]["Договор"] = ddu
            stats["corpus_updated"] += 1
            stats["projects_updated"] += 1

    # сохраняем новый JSON
    with open(r"!changing_haracteristik_dictionary/projects_old.json", "w", encoding="utf-8") as f:
        json.dump(new_result, f, ensure_ascii=False, indent=4)

    # выводим логи
    print("=== Изменяемые характеристики ===")
    print(f"✅ Добавлено проектов: {stats['projects_added']}")
    print(f"🔁 Обновлено проектов: {stats['projects_updated']}")
    print(f"🔁 Добавлено корпусов: {stats['corpus_added']}")
    print(f"✅ Обновлено корпусов: {stats['corpus_updated']}")

update_all_base()