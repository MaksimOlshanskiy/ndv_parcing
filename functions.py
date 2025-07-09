import re
import pandas as pd
import os
import glob

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
        df['Цена лота, руб.'] = df['Цена лота, руб.'].fillna(df['Цена лота со ск, руб.'])
        df.loc[df['Цена лота, руб.'] == 0, 'Цена лота, руб.'] = df.loc[df['Цена лота, руб.'] == 0, 'Цена лота со ск, руб.']

        return df



    all_data = all_data.drop_duplicates()       # убираем полные дубликаты
    #  all_data = remove_share_sale(all_data)   # убираем доли в квартирах
    try:
        all_data = clean_project_name(all_data, 'Название проекта') # убираем слова ЖК и кавычки в названии проектов
    except:
        ''
    #  all_data = fill_missing_price(all_data)  # проставляем ценники в колонке старая цена
    # Проверяем результат
    print(all_data)
    print(f'Число строк в датафрейме {len(all_data)}')


    # Сохраняем объединённые данные в новый Excel файл
    output_file = f'{folder_path}\\{output_file_name}'
    all_data.to_excel(output_file, index=False)

    print(f"Все данные сохранены в {output_file}")

    file_to_keep = output_file_name

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # удаляем за собой все лишние файлы в папке
        if os.path.isfile(file_path) and filename != file_to_keep:
            os.remove(file_path)
            print(f'Удалён файл: {filename}')