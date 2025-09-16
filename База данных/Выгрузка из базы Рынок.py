import pandas as pd
import numpy as np
import psycopg2
import time
import warnings

year = 2025
previous_year = 2024
month = 8
previous_month = 7

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="pandas only supports SQLAlchemy connectable",
)

# localhost
try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect('postgresql://postgres:ndv212XO@localhost:5432/postgres')
    print('Подключились к базе данных')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Ошибка подключения к базе данных')

sql_query = f"""
SELECT * 
FROM ndv.ndv_data
WHERE (extract(YEAR from update_date) = 2024
OR extract(YEAR from update_date) = 2025)
AND extract(MONTH from update_date) = 8
AND district LIKE '%АО%'  
AND district NOT IN ('НАО', 'ТАО');
                    """


df = pd.read_sql(sql_query, conn)
print('SQL запрос выполнен успешно')

df.columns = [
    "Дата обновления",
    "Название проекта",
    "На англ",
    "Промзона",
    "Местоположение",
    "Метро",
    "Расстояние до метро, км",
    "Время до метро, мин",
    "Мцк/мцд/бкл",
    "Расстояние до мцк/мцд, км",
    "Время до мцк/мцд, мин",
    "Бкл",
    "Расстояние до бкл, км",
    "Время до бкл, мин",
    "Статус",
    "Старт",
    "Комментарий",
    "Девелопер",
    "Округ",
    "Район",
    "Адрес",
    "Эскроу",
    "Корпус",
    "Конструктив",
    "Класс",
    "Срок сдачи",
    "Старый срок сдачи",
    "Стадия строительной готовности",
    "Договор",
    "Тип помещения",
    "Отделка",
    "Кол-во комнат",
    "Площадь, кв.м",
    "Цена кв.м, руб.",
    "Цена лота, руб.",
    "Скидка,%",
    "Цена кв.м со ск, руб.",
    "Цена со скидкой, руб."
]

df.to_excel("output.xlsx", index=False)
