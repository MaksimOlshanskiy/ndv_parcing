import pandas as pd

# Загрузка Excel-файла
file_path = r"C:\Users\m.olshanskiy\Desktop\База по годам\2024\2024_старая МСК+НАО-new.xlsx"
excel_data = pd.read_excel(file_path)

# Отображение первых строк и списка колонок
excel_data.head(), excel_data.columns.tolist()



# Словарь для переименования колонок
column_mapping = {
    'Дата обновления': 'update_date',
    'Название проекта': 'project_name',
    'на англ': 'project_name_en',
    'промзона': 'industrial_zone',
    'Местоположение': 'location',
    'Метро': 'metro',
    'Расстояние до метро, км': 'dist_to_metro',
    'Время до метро, мин': 'time_to_metro',
    'МЦК/МЦД/БКЛ': 'rail_line',
    'Расстояние до МЦК/МЦД, км': 'dist_to_rail',
    'Время до МЦК/МЦД, мин': 'time_to_rail',
    'БКЛ': 'bkl_station',
    'Расстояние до БКЛ, км': 'dist_to_bkl',
    'Время до БКЛ, мин': 'time_to_bkl',
    'статус': 'status',
    'старт': 'start_date',
    'Комментарий': 'comment',
    'Девелопер': 'developer',
    'Округ': 'district',
    'Район': 'area',
    'Адрес': 'address',
    'Эскроу': 'escrow',
    'Корпус': 'building_block',
    'Конструктив': 'structure_type',
    'Класс': 'class',
    'Срок сдачи': 'finish_date',
    'Старый срок сдачи': 'old_finish_date',
    'Стадия строительной готовности': 'construction_stage',
    'Договор': 'contract_type',
    'Тип помещения': 'unit_type',
    'Отделка': 'finishing',
    'Кол-во комнат': 'rooms',
    'Площадь, кв.м': 'area_sqm',
    'Цена кв.м, руб.': 'price_per_sqm',
    'Цена лота, руб.': 'price_total',
    'Скидка,%': 'discount_pct',
    'Цена кв.м со ск, руб.': 'price_per_sqm_discounted',
    'Цена со скидкой, руб.': 'price_total_discounted',
    'Секция': 'section',
    'Этаж': 'floor',
    'Номер': 'unit_number'
}

# Переименование колонок
excel_data_renamed = excel_data.rename(columns=column_mapping)
excel_data_renamed[['dist_to_metro', 'time_to_metro', 'dist_to_rail', 'time_to_rail', 'dist_to_bkl','time_to_bkl', 'area_sqm', 'price_per_sqm', 'price_total', 'discount_pct', 'price_per_sqm_discounted', 'price_total_discounted']] = excel_data_renamed[['dist_to_metro', 'time_to_metro', 'dist_to_rail', 'time_to_rail', 'dist_to_bkl','time_to_bkl', 'area_sqm', 'price_per_sqm', 'price_total', 'discount_pct', 'price_per_sqm_discounted', 'price_total_discounted']].round(1)

# Сохранение в CSV
csv_path = "C:/Users/m.olshanskiy/Desktop/База по годам/2024/2024_msk.csv"
excel_data_renamed.to_csv(csv_path, index=False, sep=';')

print(csv_path)  # Путь к файлу для загрузки в PostgreSQL
