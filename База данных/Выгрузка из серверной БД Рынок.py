import pandas as pd
import numpy as np
import psycopg2
import time
import warnings
from Developer_dict import name_dict, developer_dict

year = 2026
month = 4
project = None

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="pandas only supports SQLAlchemy connectable",
)

# localhost
# 192.168.100.88
# postgres:ndv212XO
# readonly_user:1234
try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect('postgresql://postgres:PassToPostgres$@192.168.252.134:5432/ndv_database')
    print('Подключились к базе данных')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Ошибка подключения к базе данных')

sql_query = f"""
select *
from ndv_data
where extract(year from date) = {year}
and extract(month from date) = {month} 

                    """

if project:
    sql_query += f" AND project_name = '{project}'"


df = pd.read_sql(sql_query, conn)
print('SQL запрос выполнен успешно')

df = df.rename(columns={
    'date': 'Дата обновления',
    'project_name': 'Название проекта',
    'project_name_en': 'На англ',
    'industrial_zone': 'Промзона',
    'location': 'Местоположение',
    'metro': 'Метро',
    'dist_to_metro': 'Расстояние до метро, км',
    'time_to_metro': 'Время до метро, мин',
    'rail_line': 'Мцк/мцд/бкл',
    'dist_to_rail': 'Расстояние до мцк/мцд, км',
    'time_to_rail': 'Время до мцк/мцд, мин',
    'bkl_station': 'Бкл',
    'dist_to_bkl': 'Расстояние до бкл, км',
    'time_to_bkl': 'Время до бкл, мин',
    'status': 'Статус',
    'start_date': 'Старт',
    'comment': 'Комментарий',
    'developer': 'Девелопер',
    'district': 'Округ',
    'area': 'Район',
    'address': 'Адрес',
    'escrow': 'Эскроу',
    'korpus': 'Корпус',
    'structure_type': 'Конструктив',
    'class': 'Класс',
    'finish_date': 'Срок сдачи',
    'old_finish_date': 'Старый срок сдачи',
    'construction_stage': 'Стадия строительной готовности',
    'contract_type': 'Договор',
    'unit_type': 'Тип помещения',
    'finishing': 'Отделка',
    'rooms': 'Кол-во комнат',
    'area_sqm': 'Площадь, кв.м',
    'price_per_sqm': 'Цена кв.м, руб.',
    'price_total': 'Цена лота, руб.',
    'discount_pct': 'Скидка,%',
    'price_per_sqm_discounted': 'Цена кв.м со ск, руб.',
    'price_total_discounted': 'Цена со скидкой, руб.',
    'location_big' : 'Локация'
})



print(df.info())

# df["Название проекта"] = df["Название проекта"].replace(name_dict)
# df["Девелопер"] = df["Девелопер"].replace(developer_dict)
# df.to_csv(r"База Июль-Август>.csv", index=False, encoding='utf-8-sig')

df.to_excel("Выгрузка0426.xlsx", index=False)