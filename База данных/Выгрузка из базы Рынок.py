import pandas as pd
import numpy as np
import psycopg2
import time
import warnings
from Developer_dict import name_dict, developer_dict

year = 2025
previous_year = 2024
month = 1
previous_month = 12
project = 'Берег'

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
select *
from ndv_data
where extract(year from date) = 2025 
and extract(month from date) = 4 

                    """


df = pd.read_sql(sql_query, conn)
print('SQL запрос выполнен успешно')


print(df.info())

# df["Название проекта"] = df["Название проекта"].replace(name_dict)
# df["Девелопер"] = df["Девелопер"].replace(developer_dict)
# df.to_csv(r"База Июль-Август>.csv", index=False, encoding='utf-8-sig')

df.to_excel("Выгрузка03-2025.xlsx", index=False)