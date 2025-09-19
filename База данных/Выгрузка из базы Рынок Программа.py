import pandas as pd
import numpy as np
import psycopg2
import time
import warnings
from Developer_dict import name_dict, developer_dict
year = input("Введите год: ")

# если нужно число, приводим к int
try:
    year = int(year)
    print(f"Вы ввели год: {year}")
except ValueError:
    print("Ошибка: нужно ввести число (год).")

year = input("Введите месяц: ")

# если нужно число, приводим к int
try:
    year = int(year)
    print(f"Вы ввели год: {year}")
except ValueError:
    print("Ошибка: нужно ввести число (год).")


year = 2025
previous_year = year-1
month = 8
if month == 1:
    previous_month = 12
else:
    previous_month = month - 1


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
    conn = psycopg2.connect('postgresql://postgres:ndv212XO@localhost:5432/postgres')
    print('Подключились к базе данных')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Ошибка подключения к базе данных')

sql_query = f"""
SELECT *
FROM ndv_data
WHERE (EXTRACT(YEAR from update_date) = {previous_year}
AND EXTRACT(MONTH from update_date) = {month})
OR (EXTRACT(YEAR from update_date) = {year}
AND EXTRACT(MONTH from update_date) = {previous_month})
OR (EXTRACT(YEAR from update_date) = {year}
AND EXTRACT(MONTH from update_date) = {month})
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

print(df.info())

# df["Название проекта"] = df["Название проекта"].replace(name_dict)
# df["Девелопер"] = df["Девелопер"].replace(developer_dict)
# df.to_csv(r"База Июль-Август>.csv", index=False, encoding='utf-8-sig')

df.to_excel("Выгрузка.xlsx", index=False)