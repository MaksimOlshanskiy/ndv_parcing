import re
import numpy as np
import pandas as pd
import os
import glob
import datetime
from Developer_dict import name_dict, developer_dict
from area_dictionary.Старая_квартирография.step_4_replacement_to_excel import process_data, load_json_data
import json
from enrich.main2 import enrich_dataframe, load_json
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

def get_unique_filepath(folder_path: str, filename: str) -> str:
    """
    Если файл существует — добавляет _1, _2, _3 ...
    """
    base, ext = os.path.splitext(filename)
    file_path = os.path.join(folder_path, filename)

    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(folder_path, f"{base}_{counter}{ext}")
        counter += 1

    return file_path

def save_flats_to_excel(flats, project, developer, kvartirografia=True, drop_columns=False, change_dates=False):

    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'На англ',
                                      'Промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'Статус',
                                      'Старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена со скидкой, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    df["Корпус"] = (
         df["Корпус"]
         .astype(str)  # приводим всё к строкам
         .str.replace(r'(?i)\bкорпус\b\.?\s*', '', regex=True)  # удаляем "корпус"
         .str.strip()  # убираем лишние пробелы
         .replace(['', '-', 'nan', 'NaN'], '1')  # заменяем пустые строки и текстовые NaN на "1"
     )

    # В столбце Корпус, если номер корпуса идёт в скобках, то удаляем всё за скобками, оставляем только то,
    # что в скобках. Если в скобках есть слово очередь, то ничего не трогаем
    df['Корпус'] = df['Корпус'].astype(str)
    # Выделим текст в скобках
    bracket_content = df['Корпус'].str.extract(r'\((.*?)\)', expand=False)
    # Маска: строка содержит скобки
    has_brackets = df['Корпус'].str.contains(r'\(.*?\)', na=False)
    # Маска: в строке есть слово "очередь" где угодно (внутри или снаружи скобок)
    contains_ochered = df['Корпус'].str.contains(r'очередь', case=False, na=False)
    # Маска: есть скобки, но НЕТ "очередь" вообще
    mask = has_brackets & ~contains_ochered
    # Заменяем только те строки, которые соответствуют маске
    df.loc[mask, 'Корпус'] = bracket_content[mask].str.strip()

    # 1. Удаляем текст 'Жилой дом № ' (всё равно на NaN это не повлияет)
    df['Корпус'] = df['Корпус'].replace('Жилой дом № ', '', regex=True)
    # Заменяем строку 'nan' и пустые строки на np.nan
    df['Корпус'] = df['Корпус'].replace(['nan', r'^\s*$'], np.nan, regex=True)
    # 3. Заполняем NaN единицами
    df['Корпус'] = df['Корпус'].fillna('1')

    df["Корпус"] = df["Корпус"].astype(str).str.replace(",", ".", regex=False)

    def clean_name(name: str) -> str:
        name = name.replace('ЖК ', '')
        name = re.sub(r'[\\:*?"<>|«»]', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    developer = clean_name(developer)
    df['Название проекта'] = df['Название проекта'].apply(clean_name)
    df["Название проекта"] = df["Название проекта"].replace(name_dict)
    print(df['Девелопер'].unique())
    df['Девелопер'] = df['Девелопер'].apply(clean_name)
    df["Девелопер"] = df["Девелопер"].replace(developer_dict)
    print(df['Девелопер'].unique())


    projects_dict = load_json(
        r'C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!haracteristik_dictionary\projects.json'
    )
    corpus_dict = load_json(
        r'C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\!changing_haracteristik_dictionary\projects.json'
    )
    if kvartirografia:
        area_dict = load_json(r'C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\area_dictionary\output.json')
    else:
        area_dict = None

    df = enrich_dataframe(
        df,
        projects_dict,
        corpus_dict,
        area_dict
    )

    if drop_columns:
        df = df.drop(columns=['секция', 'этаж', 'номер'], errors='ignore')
    # --- 1. Приводим цены к числу ПЕРЕД всеми вычислениями ---

    for col in ['Цена лота, руб.', 'Цена со скидкой, руб.']:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(' ', '', regex=False)
            .str.replace('\xa0', '', regex=False)
            .replace(['', 'None', 'nan'], np.nan)
        )
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # --- 2. Приводим площадь ---
    df['Площадь, кв.м'] = pd.to_numeric(df['Площадь, кв.м'], errors='coerce')

    # --- 3. Цена со скидкой ---
    df['Цена со скидкой, руб.'] = (
        df['Цена со скидкой, руб.']
        .replace(0, np.nan)
        .fillna(df['Цена лота, руб.'])
    )

    # --- 4. Безопасное деление ---
    df['Цена кв.м, руб.'] = np.where(
        df['Площадь, кв.м'] > 0,
        df['Цена лота, руб.'] / df['Площадь, кв.м'],
        np.nan
    )

    df['Цена кв.м со ск, руб.'] = np.where(
        df['Площадь, кв.м'] > 0,
        df['Цена со скидкой, руб.'] / df['Площадь, кв.м'],
        np.nan
    )

    df['Скидка,%'] = np.where(
        df['Цена лота, руб.'] > 0,
        1 - (df['Цена со скидкой, руб.'] / df['Цена лота, руб.']),
        np.nan
    )

    # --- 5. Округление ---
    df['Цена кв.м, руб.'] = df['Цена кв.м, руб.'].round(2)
    df['Цена кв.м со ск, руб.'] = df['Цена кв.м со ск, руб.'].round(2)
    df['Скидка,%'] = df['Скидка,%'].round(2)


    print(df[['Корпус', 'Кол-во комнат', 'Площадь, кв.м', 'Цена лота, руб.', 'Цена со скидкой, руб.']].info())
    print(f'')
    print(f'Число лотов: {len(df)}')
    print(f'')
    print(f'Типы отделки: {df['Отделка'].value_counts()}')
    print(f'')
    print(f'Проекты: {df['Название проекта'].value_counts()}')
    print(f'')


    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "1_FILES")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    project = re.sub(r'[<>:"/\\|?*]', '_', project)
    filename = f"{developer}_{project}_{current_date}.xlsx"
    file_path = get_unique_filepath(folder_path, filename)
    df.to_excel(file_path, index=False)
    # открываем файл и применяем выравнивание
    wb = load_workbook(file_path)
    ws = wb.active

    center_alignment = Alignment(horizontal='center', vertical='center')

    for row in ws.iter_rows():
        for cell in row:
            cell.alignment = center_alignment

    # Автоподбор ширины колонок
    for col in ws.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)  # Получаем буквенное обозначение колонки

        for cell in col:
            try:
                if cell.value:
                    # Учитываем длину текста в ячейке
                    cell_length = len(str(cell.value))
                    if cell_length > max_length:
                        max_length = cell_length
            except:
                pass

        # Устанавливаем ширину колонки (добавляем 2 для отступов)
        adjusted_width = max_length + 2
        ws.column_dimensions[col_letter].width = adjusted_width

    wb.save(file_path)
    print(f"✅ Данные сохранены в файл: {file_path}")


def save_cian_to_excel(flats, project, developer, drop_columns = True):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена со скидкой, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    df["Корпус"] = (
         df["Корпус"]
         .astype(str)  # приводим всё к строкам
         .str.replace(r'(?i)\bкорпус\b\.?\s*', '', regex=True)  # удаляем "корпус"
         .str.strip()  # убираем лишние пробелы
         .replace(['', '-', 'nan', 'NaN'], '1') # заменяем пустые строки и текстовые NaN на "1"
     )

    # В столбце Корпус, если номер корпуса идёт в скобках, то удаляем всё за скобками, оставляем только то,
    # что в скобках. Если в скобках есть слово очередь, то ничего не трогаем
    df['Корпус'] = df['Корпус'].astype(str)
    # Выделим текст в скобках
    bracket_content = df['Корпус'].str.extract(r'\((.*?)\)', expand=False)
    # Маска: строка содержит скобки
    has_brackets = df['Корпус'].str.contains(r'\(.*?\)', na=False)
    # Маска: в строке есть слово "очередь" где угодно (внутри или снаружи скобок)
    contains_ochered = df['Корпус'].str.contains(r'очередь', case=False, na=False)
    # Маска: есть скобки, но НЕТ "очередь" вообще
    mask = has_brackets & ~contains_ochered
    # Заменяем только те строки, которые соответствуют маске
    df.loc[mask, 'Корпус'] = bracket_content[mask].str.strip()

    # 1. Удаляем текст 'Жилой дом № ' (всё равно на NaN это не повлияет)
    df['Корпус'] = df['Корпус'].replace('Жилой дом № ', '', regex=True)
    # Заменяем строку 'nan' и пустые строки на np.nan
    df['Корпус'] = df['Корпус'].replace(['nan', r'^\s*$'], np.nan, regex=True)
    # 3. Заполняем NaN единицами
    df['Корпус'] = df['Корпус'].fillna('1')

    df["Корпус"] = df["Корпус"].astype(str).str.replace(",", ".", regex=False)

    def clean_name(name: str) -> str:
        name = name.replace('ЖК ', '')
        name = re.sub(r'[\\/:*?"<>|]', '', name)
        name = re.sub(r'\s+', ' ', name).strip()
        return name

    developer = clean_name(developer)
    df['Название проекта'] = df['Название проекта'].apply(clean_name)
    df["Название проекта"] = df["Название проекта"].replace(name_dict)
    print(df['Девелопер'].unique())
    df['Девелопер'] = df['Девелопер'].apply(clean_name)
    df["Девелопер"] = df["Девелопер"].replace(developer_dict)
    print(df['Девелопер'].unique())

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

    print(f'Число лотов: {len(df)}')

    if drop_columns:
        df = df.drop(columns=['секция', 'этаж', 'номер'], errors='ignore')


    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = r""
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    project = re.sub(r'[<>:"/\\|?*]', '_', project)
    developer = re.sub(r'[<>:"/\\|?*]', '_', developer)
    filename = f"{developer}_{project}_{current_date}.xlsx"
    file_path = get_unique_filepath(folder_path, filename)
    df.to_excel(file_path, index=False)


    try:
        print(f"✅ Данные сохранены в файл: {file_path}")
    except:
        ''

def classify_renovation(description: str) -> str:

    description = description.lower()

    # Категории ремонтов
    has_renovation = [
        "с отделкой", "свежий ремонт", "качественный ремонт", "с ремонтом",
        "евроремонт", "под ключ", "дизайнерский ремонт", "новый ремонт",
        "капитальный ремонт", "современный ремонт", "полностью отремонтирована",
        "после ремонта", "отличный ремонт", "хороший ремонт", "недавно сделан ремонт",
        "люкс ремонт", "высококачественная отделка", "эксклюзивный ремонт",
        "стильный ремонт", "авторский дизайн", "ремонт класса люкс",
        "дорогой ремонт", "ремонт бизнес-класса", "реновация",
        "квартира в идеальном состоянии", "хорошем жилом состоянии",
        "хорошем состоянии", "отличном состоянии", "меблирован", "с мебелью", "с техникой", 'чистовой отделкой',
        'чистовая отделка', 'отделка апартаментов выполнена', 'отделка квартир выполнена', 'отделка осуществляется',
        'отделка выполнена'
    ]

    no_renovation = [
        "без отделки", "без ремонта", "требуется ремонт", "нужен ремонт",
        "под ремонт", "нежилое состояние", "убитая квартира", "старый ремонт",
        "состояние от застройщика", "плохой ремонт", "оригинальное состояние",
        "под замену", "надо делать ремонт", "под восстановление",
        "обветшалый ремонт", "ремонт отсутствует", "разрушенное состояние",
        "без отделочных работ", "голые стены", "стены без отделки"
    ]

    rough_finishing = [
        "черновая отделка", "предчистовая отделка", "white box", "предчистовой ремонт",
        "стройвариант", "под чистовую отделку", "без чистовой отделки", "без ремонта от застройщика",
        "в бетоне", "без финишной отделки", "предчистовая подготовка",
        "стены под покраску", "готово к отделке", "штукатурка стен",
        "без напольного покрытия", "стяжка и штукатурка", 'предчистовой отделкой', 'white-box', 'получистовая'
    ]

    # Проверяем ключевые слова
    for phrase in has_renovation:
        if re.search(rf"\b{phrase}\b", description):
            return "С отделкой"

    for phrase in no_renovation:
        if re.search(rf"\b{phrase}\b", description):
            return "Без отделки"

    for phrase in rough_finishing:
        if re.search(rf"\b{phrase}\b", description):
            return "Предчистовая"

    return "Не удалось определить"

def clean_filename(name: str, max_length: int = 255) -> str:
    # Удаляем запрещённые символы для Windows
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # Зарезервированные имена (например, CON.xlsx)
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}
    # Удаляем пробелы в начале и конце
    name = name.strip()
    # Удаляем расширение перед проверкой имени
    base = name.rsplit('.', 1)[0]
    # Переименовываем зарезервированные
    if base.upper() in reserved:
        base = f"{base}_safe"
    # Возвращаем с ограничением длины

    base = base.replace('ЖК ', '')  # Убираем 'ЖК '
    base = base.strip('«»"')  # Убираем кавычки «», ""

    return f"{base[:max_length - 5]}.xlsx"  # 5 символов под ".xlsx"

def merge_and_clean(folder_path, output_file_name):
    # Создаём пустой DataFrame для накопления данных
    all_data = pd.DataFrame()

    # Используем glob для поиска всех Excel файлов в папке
    excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

    # Проходим по каждому файлу и добавляем его данные в DataFrame
    for file_path in excel_files:
        df = pd.read_excel(file_path)  # Читаем Excel файл в DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)  # Добавляем данные в общий DataFrame


    def clean_project_name(df, column_name):
        """
        Очищает названия проектов в указанной колонке DataFrame.
        Убирает 'ЖК ' в начале и кавычки вокруг названия.

        :param df: DataFrame pandas
        :param column_name: str, название столбца с проектами
        :return: DataFrame с изменённой колонкой
        """
        def clean_name(name):
            name = name.replace('ЖК ', '')  # Убираем 'ЖК '
            name = name.strip('«»"')  # Убираем кавычки «», ""
            return name

        df[column_name] = df[column_name].apply(clean_name)
        return df

    def remove_share_sale(df, column="Описание"):
        """
        Удаляет строки, содержащие ключевые слова, связанные с продажей доли в квартире.

        Аргументы:
            df (pd.DataFrame): DataFrame с данными.
            column (str): Название столбца, в котором искать ключевые слова (по умолчанию "Описание").

        Возвращает:
            pd.DataFrame: DataFrame без строк, содержащих ключевые слова.
        """
        keywords = ["доля", "доли", 'долей', "продаётся комната", "продаю комнату", "продажа комнаты",
                    "часть квартиры", "1/2", "1/3", "1/4", "комната в квартире"]

        # Фильтруем DataFrame, удаляя строки с ключевыми словами
        mask = df[column].str.lower().str.contains("|".join(keywords), regex=True, na=False)
        df_cleaned = df[~mask]  # Оставляем только строки, где ключевые слова не найдены

        return df_cleaned

    def fill_missing_price(df):
        """
        Заполняет пустые значения в колонке 'Цена лота, руб.'
        значениями из колонки 'Цена лота со ск, руб.'
        """
        df['Цена лота, руб.'] = df['Цена лота, руб.'].fillna(df['Цена со скидкой, руб.'])
        df.loc[df['Цена лота, руб.'] == 0, 'Цена лота, руб.'] = df.loc[df['Цена лота, руб.'] == 0, 'Цена со скидкой, руб.']

        return df



    # all_data = all_data.drop_duplicates()       # убираем полные дубликаты
    #  all_data = remove_share_sale(all_data)   # убираем доли в квартирах
    try:
        all_data = clean_project_name(all_data, 'Название проекта') # убираем слова ЖК и кавычки в названии проектов
    except:
        ''
    #  all_data = fill_missing_price(all_data)  # проставляем ценники в колонке старая цена
    try:
        all_data["Цена лота, руб."] = pd.to_numeric(
            all_data["Цена лота, руб."].astype(str).str.replace(r"[^\d,\.]", "", regex=True).str.replace(",", "."),
            errors="coerce"
        )
    except:
        ''
    try:
        all_data["Цена со скидкой, руб."] = pd.to_numeric(
        all_data["Цена со скидкой, руб."].astype(str).str.replace(r"[^\d,\.]", "", regex=True).str.replace(",", "."),
        errors="coerce"
    )
    except:
        ''
    if 'Отделка' in all_data.columns:
        all_data['Отделка'] = all_data['Отделка'].replace({
            'без отделки': 'Без отделки',
            'с отделкой': 'С отделкой'
        })




    # Сохраняем объединённые данные в новый Excel файл
    output_file = f'{folder_path}\\{output_file_name}'
    all_data.to_excel(output_file, index=False)

    print(f"✅ Все данные сохранены в {output_file}")

    file_to_keep = output_file_name

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # удаляем за собой все лишние файлы в папке
        if os.path.isfile(file_path) and filename != file_to_keep:
            os.remove(file_path)
            print(f'Удалён файл: {filename}')

    print(f'📦 Число строк в датафрейме {len(all_data)}')


import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # радиус Земли в км
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c