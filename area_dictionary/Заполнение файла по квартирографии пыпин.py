import json
import pandas as pd

json_path = r'C:\PycharmProjects\ndv_parcing\area_dictionary\output.json' # база квартирографии

excel_path = r"D:\Ricci\archive\Pipin-04-2026-2.csv"   # загружаемый файл
output_path = r"D:\Ricci\archive\Pipin-04-2026-kvartirografia.csv"  # сохраняемый файл


def load_json_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_excel_data(excel_path):
    df = pd.read_csv(excel_path)
    df.columns = df.columns.str.strip()
    return df


def process_data(json_data, excel_df):
    result_df = excel_df.copy()
    result_df['Площадь'] = result_df['Площадь'].astype(str).str.replace(',', '.').str.replace(' ', '').astype(float)

    total = len(result_df)

    # Список застройщиков, у которых не надо менять типологию
    developers_to_skip = {'фонд реновации'}
    # Список проектов, у которых не надо менять типологию
    jk_name_to_skip = {'гармония парк', 'мишино-2'}
    jk_name_to_skip2 = {'серебро', 'берег'}

    for idx, row in result_df.iterrows():

        jk_name = str(row.get('Название проекта')).strip().lower()
        area = row.get('Площадь')
        developer = str(row.get('Девелопер')).strip().lower()

        if pd.isna(jk_name) or pd.isna(area):
            result_df.at[idx, 'Кол-во комнат'] = 'Н/Д'
            continue

        # Условие: если площадь <= 28 — это студия
        if area <= 28 and jk_name not in jk_name_to_skip2:
            result_df.at[idx, 'Кол-во комнат'] = 'студия'
            if __name__ == "__main__":
                print(f"[{idx + 1}/{total}] Назначено как студия по площади <= 28: ЖК {jk_name}, площадь {area}")
            continue


        found = False

        if jk_name in json_data:
            jk_dict = json_data[jk_name]
            area = round(float(area), 2)

            # Ищем точное совпадение
            for json_area_str, room_type in jk_dict.items():
                try:
                    json_area = round(float(json_area_str), 2)
                    if area == json_area:
                        result_df.at[idx, 'Кол-во комнат'] = (
                            'студия' if room_type == 0 or
                            (isinstance(room_type, str) and (
                                'ст' in room_type.lower() or
                                room_type.strip().lower() == 'st' or
                                'СТ' in room_type
                            ))
                            else room_type
                        )
                        found = True
                        break
                except ValueError:
                    continue

            if not found:
                closest_area = None
                closest_room = None

                # Ищем ближайшее СНИЗУ
                for json_area_str, room_type in jk_dict.items():
                    try:
                        json_area = round(float(json_area_str), 2)
                        if area - 3 <= json_area < area:
                            if closest_area is None or json_area > closest_area:
                                closest_area = json_area
                                closest_room = room_type
                    except ValueError:
                        continue

                # Если не нашли — ищем СВЕРХУ
                if closest_area is None:
                    for json_area_str, room_type in jk_dict.items():
                        try:
                            json_area = round(float(json_area_str), 2)
                            if area < json_area <= area + 3:
                                if closest_area is None or json_area < closest_area:
                                    closest_area = json_area
                                    closest_room = room_type
                        except ValueError:
                            continue

                if closest_area is not None:
                    result_df.at[idx, 'Кол-во комнат'] = (
                        'студия' if closest_room == 0 or
                        (isinstance(closest_room, str) and (
                            'ст' in closest_room.lower() or
                            closest_room.strip().lower() == 'st' or
                            'СТ' in closest_room
                        ))
                        else closest_room
                    )
                    found = True


        if __name__ == "__main__":
            print(f"[{idx + 1}/{total}] Обработано: ЖК {jk_name}, площадь {area}")

    return result_df


def save_as_xlsx(df, output_path_xlsx, sheet_name='Sheet1'):
    df.to_csv(output_path_xlsx, index=False)


# --- Запуск ---
if __name__ == "__main__":



    json_data = load_json_data(json_path)
    excel_df = load_excel_data(excel_path)

    result_df = process_data(json_data, excel_df)
    save_as_xlsx(result_df, output_path)


