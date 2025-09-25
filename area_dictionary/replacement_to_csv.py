import json
import pandas as pd


def load_json_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_csv_data(csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8')
    df.columns = df.columns.str.strip()

    required_cols = ['Название проекта', 'Площадь, кв.м']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Отсутствует нужная колонка: {col}")

    return df


def save_as_csv(df, output_path_csv):
    df.to_csv(output_path_csv, index=False, encoding='utf-8')


def is_studio(room_type):
    return room_type == 0 or (
            isinstance(room_type, str) and (
            'ст' in room_type.lower() or
            room_type.strip().lower() == 'st'
    )
    )


def find_closest_match(area, jk_dict):
    closest_area = None
    closest_room = None

    # Сначала снизу
    for json_area_str, room_type in jk_dict.items():
        try:
            json_area = round(float(json_area_str), 2)
            if area - 1.5 <= json_area < area:
                if closest_area is None or json_area > closest_area:
                    closest_area = json_area
                    closest_room = room_type
        except ValueError:
            continue

    # Потом сверху
    if closest_area is None:
        for json_area_str, room_type in jk_dict.items():
            try:
                json_area = round(float(json_area_str), 2)
                if area < json_area <= area + 1.0:
                    if closest_area is None or json_area < closest_area:
                        closest_area = json_area
                        closest_room = room_type
            except ValueError:
                continue

    return closest_room


def process_data(json_data, df):
    result_df = df.copy()
    total = len(result_df)

    for idx, row in result_df.iterrows():
        jk_name = str(row.get('Название проекта')).strip()
        area = row.get('Площадь, кв.м')

        if pd.isna(jk_name) or pd.isna(area):
            result_df.at[idx, 'Кол-во комнат'] = 'Н/Д'
            continue

        found = False
        area = round(float(area), 2)

        if jk_name in json_data:
            jk_dict = json_data[jk_name]

            # Точное совпадение
            for json_area_str, room_type in jk_dict.items():
                try:
                    json_area = round(float(json_area_str), 2)
                    if area == json_area:
                        result_df.at[idx, 'Кол-во комнат'] = 'студия' if is_studio(room_type) else room_type
                        found = True
                        break
                except ValueError:
                    continue

            # Поиск ближайшего, если не нашли точного
            if not found:
                closest_room = find_closest_match(area, jk_dict)
                if closest_room is not None:
                    result_df.at[idx, 'Кол-во комнат'] = 'студия' if is_studio(closest_room) else closest_room
                    found = True

        if not found:
            result_df.at[idx, 'Кол-во комнат'] = 'Н/Д'

        print(f"[{idx + 1}/{total}] Обработано: ЖК {jk_name}, площадь {area}")

    return result_df


# --- Запуск ---
json_path = 'normalized_output.json'
csv_input_path = '23-24.csv'
csv_output_path = '23-24_типология.csv'

json_data = load_json_data(json_path)
df = load_csv_data(csv_input_path)
result_df = process_data(json_data, df)
save_as_csv(result_df, csv_output_path)
