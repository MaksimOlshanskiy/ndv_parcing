import pandas as pd
import json

def load_excel(excel_path):
    df = pd.read_excel(excel_path, sheet_name='Sheet1')
    df.columns = df.columns.str.strip()
    return df


def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def enrich_projects(df, projects_dict):
    df = df.copy()

    df["project_key"] = (
        df["Название проекта"].astype(str)
        .str.replace("«", "", regex=False)
        .str.replace("»", "", regex=False)
    )

    for idx, row in df.iterrows():
        key = row["project_key"]
        if key in projects_dict:
            for col, value in projects_dict[key].items():
                if col in df.columns:
                    df.at[idx, col] = value

    return df.drop(columns=["project_key"])

def enrich_corpus(df, corpus_dict):
    df = df.copy()

    required_columns = [
        "Срок сдачи",
        "Стадия строительной готовности",
        "Договор",
        "Статус",
        "Распроданность квартир",
        "Количество квартир",
        "Жилая площадь, м²"
    ]

    for col in required_columns:
        if col not in df.columns:
            df[col] = None

    df["Корпус"] = df["Корпус"].astype(str).str.replace(",", ".", regex=False)

    for idx, row in df.iterrows():
        project_key = f"{row['Название проекта']}_{row['Девелопер']}"
        corpus = str(row["Корпус"])

        if project_key in corpus_dict and corpus in corpus_dict[project_key]:
            record = corpus_dict[project_key][corpus]
            for col in required_columns:
                df.at[idx, col] = record.get(col)

    for col in ["Количество квартир", "Жилая площадь, м²"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(r"[^\d\.]", "", regex=True)
            .replace("", None)
            .astype(float)
            .astype("Int64")
        )

    return df

def enrich_area_typology(df, area_json):
    df = df.copy()

    df['Площадь, кв.м'] = (
        df['Площадь, кв.м']
        .astype(str)
        .str.replace(',', '.')
        .str.replace(' ', '')
        .astype(float)
    )

    developers_to_skip = {'московские кварталы'}
    jk_name_to_skip = {'гармония парк', 'мишино-2'}
    jk_name_to_skip2 = {'серебро', 'берег'}

    for idx, row in df.iterrows():
        jk_name = str(row['Название проекта']).strip().lower()
        area = row['Площадь, кв.м']
        developer = str(row['Девелопер']).strip().lower()

        if pd.isna(jk_name) or pd.isna(area):
            df.at[idx, 'Кол-во комнат'] = 'Н/Д'
            continue

        if area <= 28 and jk_name not in jk_name_to_skip2:
            df.at[idx, 'Кол-во комнат'] = 'студия'
            continue

        if developer in developers_to_skip or jk_name in jk_name_to_skip:
            continue

        found = False

        if jk_name in area_json:
            jk_dict = area_json[jk_name]
            area = round(area, 2)

            for json_area_str, room_type in jk_dict.items():
                try:
                    if area == round(float(json_area_str), 2):
                        df.at[idx, 'Кол-во комнат'] = (
                            'студия' if str(room_type).lower() in ['0', 'st', 'ст'] else room_type
                        )
                        found = True
                        break
                except ValueError:
                    pass

            if not found:
                candidates = []

                for json_area_str, room_type in jk_dict.items():
                    try:
                        json_area = round(float(json_area_str), 2)
                        if abs(area - json_area) <= 3:
                            candidates.append((abs(area - json_area), room_type))
                    except ValueError:
                        pass

                if candidates:
                    _, closest_room = min(candidates, key=lambda x: x[0])
                    df.at[idx, 'Кол-во комнат'] = (
                        'студия' if str(closest_room).lower() in ['0', 'st', 'ст'] else closest_room
                    )
                    found = True

        if not found:
            df.at[idx, 'Кол-во комнат'] = 'Н/Д'

    return df

def main():
    excel_path = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Глоракс\2025-07-01\Glorax_GloraX Premium Белорусская_2025-07-01.xlsx"

    df = load_excel(excel_path)

    projects_dict = load_json(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!haracteristik_dictionary\projects.json")
    corpus_dict = load_json(r"/!changing_haracteristik_dictionary/projects_old.json")
    area_dict = load_json(r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\area_dictionary\output.json")

    df = enrich_projects(df, projects_dict)
    df = enrich_corpus(df, corpus_dict)
    df = enrich_area_typology(df, area_dict)

    df.to_excel(excel_path, index=False)
    print("✅ Готово. Файл обработан за один проход.")

if __name__ == "__main__":
    main()


def enrich_dataframe(
    df: pd.DataFrame,
    projects_dict: dict | None = None,
    corpus_dict: dict | None = None,
    area_dict: dict | None = None
) -> pd.DataFrame:
    """
    Обогащает DataFrame всеми этапами.
    НЕ читает и НЕ пишет файлы.
    """
    if projects_dict is not None:
        df = enrich_projects(df, projects_dict)
    if corpus_dict is not None:
        df = enrich_corpus(df, corpus_dict)
    if area_dict is not None:
        df = enrich_area_typology(df, area_dict)

    return df

def process_excel(
    excel_path: str,
    projects_json_path: str,
    corpus_json_path: str,
    area_json_path: str,
    output_path: str | None = None
) -> pd.DataFrame:
    """
    Загружает Excel → обогащает → сохраняет.
    """

    if output_path is None:
        output_path = excel_path

    df = load_excel(excel_path)

    projects_dict = load_json(projects_json_path)
    corpus_dict = load_json(corpus_json_path)
    area_dict = load_json(area_json_path)

    df = enrich_dataframe(df, projects_dict, corpus_dict, area_dict)

    df.to_excel(output_path, index=False)
    print(f"✅ Excel обработан: {output_path}")

    return df