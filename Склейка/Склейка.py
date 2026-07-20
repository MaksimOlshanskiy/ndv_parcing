

import os
import glob
import pandas as pd

# Путь к папке, где находятся Excel файлы
folder_path = r"D:\НДВ\Коммерция с Нашего дома рф\Характеристики"

# Сохраняем объединённые данные в новый Excel файл
output_file_name = 'Характеристики.xlsx'

rename_dict = {
    "CITYZEN": "Ситизен",
    "Mod": "Мод",
    "Frank's house": "Дом Франка",
    "Clos 17": "Кло 17",
    "LUCE": "Люче",
    "Moments": "МОМЕНТС",
    "Nicole": "Николь",
    "PAVE": "ПЕЙВ",
    "Portland": "ПОРТЛЕНД",
    "Republic": "Репаблик",
    "Symphony 34": "Симфони 34",
    "Soul": "СОУЛ",
    "CRYSTAL Трилогия": "Трилогия Кристалл",
    "Famous": "Феймос",
    "SIGNAL": "Сигнал",
    "BESIDE 2.0": "Бисайд 2.0",
    "Nexus": "Нексус от Аквилон",
    "Indy Towers": "Инди Тауэрз от Аквилон",
    "BESIDE": "Бисайд",
    "Sky Garden": "Скай Гарден",
    "Rotterdam": "Роттердам",
    "Amber City": "Амбер Сити",
    "Sydney Prime": "Сидней Прайм",
    "The LAKE": "Лэйк",
    "Sydney City": "Сидней Сити",
    "City Bay": "Сити Бэй",
    "Jois": "Джойс",
    "VEER": "Веер",
    "SET": "Сет",
    "SLAVA": "Слава",
    "FORUM": "Форум",
    "One": "ОНЕ",
    "DOM": "Дом на Часовой",
    "Beluck Коломенское": "Гранель Коломенское",
    "MYPRIORITY Мневники": "Мнёвники от Гранель",
    "MYPRIORITY Нижегородская": "Нижегородская от Гранель",
    "MYPRIORITY Павелецкая": "Павелецкая от Гранель",
    "MYPRIORITY Дубровка": "Дубровка от Гранель",
    "MYPRIORITY Басманный": "Басманный от Гранель",
    "Very на Ботанической": "ВЭРИ на Ботанической",
    "Nametkin tower": "НАМЕТКИН ТАУЭР",
    "Foreville": "Форевиль",
    "Voice Towers": "ВОЙС",
    "ERA": "ЭРА",
    "Shagal": "Шагал",
    "Shagal Residence": "Резиденция Шагал",
    "Voxhall": "Воксхолл",
    "WAVE": "ВЕЙВ",
    "Injoy": "Инджой",
    "Дом MALEVICH": "Дом МАЛЕВИЧ",
    "Holland park": "Холланд парк",
    "NOVA": "НОВА",
    "DIUS": "Диус",
    "Deco Residence": "Деко Резиденс",
    "Legacy": "Легаси",
    "Stellar City": "Стеллар Сити",
    "West Tower": "Вест Тауэр",
    "Citi-Mix": "СИТИМИКС",
    "River Park Towers Кутузовский": "Ривер Парк Кутузовский",
    "Сокольники": "СТОУН Сокольники",
    "Stone Rise": "СТОУН Райз",
    "Twelve": "Твелв",
    "Симоновский вал": "Симоновский Вал",
    "Level Южнопортовая": "Левел Южнопортовая",
    "Level Павелецкая Сити": "Левел Павелецкая Сити",
    "Level Академическая": "Левел Академическая",
    "Level Бауманская": "Левел Бауманская",
    "Level Войковская": "Левел Войковская",
    "Level Звенигородская": "Левел Звенигородская",
    "Level Лесной": "Левел Лесной",
    "Level Мичуринский": "Левел Мичуринский",
    "Level Нагатинская": "Левел Нагатинская",
    "Level Нижегородская": "Левел Нижегородская",
    "Level Селигерская": "Левел Селигерская",
    "Level Причальный": "Левел Причальный",
    "Sky Sputnik": "Скай Спутник",
    "AURUS Residences": "АУРУС Резиденции",
    "balance": "баланс",
    "AHEAD": "АХЕД",
    "АХЭД": "АХЕД",
    "МУЗА": "Муза",
    "Five Towers": "Файв Тауэрс",
    "ARTEL": "АРТЕЛЬ",
    "KING & SONS": "КИНГ&САНС",
    "PHANTOM": "ФАНТОМ",
    "Stories на Мосфильмовской": "СТОРИС на Мосфильмовской",
    "Woods": "Вудс",
    'ultima' : 'УЛЬТИМА Сити',
    'Tate' : 'ТАТЕ',
    'Springs' : 'Спрингс',
    'Upside Towers' : 'Апсайд Тауэрс',
'Новая Алексеевская Роща' : 'Гранель Алексеевская Роща',
'Аникеевский' : 'Гранель Аникеевский',
'Бригантина' : 'Гранель Бригантина',
'Живописный' : 'Гранель Живописный',
'Ильинойс' : 'Гранель Ильинойс',
'Императорские Мытищи' : 'Гранель Мытищи',
'Пехра' : 'Гранель Пехра',
'Притяжение Сити' : 'Гранель Притяжение Сити',
'Тринити' : 'Гранель Тринити',
    'Ренессанс' : 'Ренессанс в Сокольниках'

}





# Создаём пустой DataFrame для накопления данных
all_data = pd.DataFrame()

# Используем glob для поиска всех Excel файлов в папке
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

# Проходим по каждому файлу и добавляем его данные в DataFrame
for file_path in excel_files:
    try:
        df = pd.read_excel(file_path)  # Читаем Excel файл в DataFrame
    except:
        print(file_path)
    df.columns = df.columns.str.capitalize()


    all_data = pd.concat([all_data, df], ignore_index=True)  # Добавляем данные в общий DataFrame



# all_data["Ссылка"] = (
#     all_data["Ссылка"]
#     .astype(str)
#     .str.split('/')
#     .str[-2]
# )

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

# all_data['Название проекта'] = all_data['Название проекта'].replace(rename_dict)
# all_data = all_data.drop_duplicates()       # убираем полные дубликаты
#  all_data = remove_share_sale(all_data)   # убираем доли в квартирах
# try:
#     all_data = clean_project_name(all_data, 'Название проекта') # убираем слова ЖК и кавычки в названии проектов
# except:
#     ''
# all_data = fill_missing_price(all_data)  # проставляем ценники в колонке старая цена

# all_data['Ссылка'] = all_data['Ссылка'].apply(str)

# all_data['Корпус'] = all_data['Корпус'].astype(str).replace(',', '.')
print(all_data)
print(f'Число строк в датафрейме {len(all_data)}')




output_file = f'{folder_path}\\{output_file_name}'

all_data.to_excel(output_file, index=False)

print(f"Все данные сохранены в {output_file}")