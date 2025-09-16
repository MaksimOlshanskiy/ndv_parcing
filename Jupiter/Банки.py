import pandas as pd
import numpy as np
import psycopg2
import time
import warnings

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

projects_dict = {"'Скай Гарден'": "'Sky Garden'", "'Ситизен'": "'CITYZEN'", "'Сити Бэй'": "'City Bay'",
                 "'Первый Шереметьевский'": "'1-й Шереметьевский'", "'Левел Лесной'": "'Level Лесной'",
                 "'Пятницкие луга'": "'Пятницкие Луга'"}
months_ru = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
             7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}

project_list = ["'Планерный квартал'"]
startrow = 0  # отслеживаем, куда писать следующий проект
startrow2 = 0

with pd.ExcelWriter(r"C:\Users\m.olshanskiy\Desktop\SQL2.xlsx", engine="xlsxwriter") as writer:
    workbook = writer.book
    worksheet = None

    for i, project in enumerate(project_list):
        print(startrow)
        print(startrow2)
        print(project)
        year = 2025
        previous_year = 2024
        month = 8
        previous_month = 7

        sql_query_banks = f"""
        WITH filter AS (
            SELECT *       
            FROM pipin
            WHERE jk_rus = 'Планерный квартал'
              AND tip_pomescheniya IN ('квартира', 'апартамент')
              AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
              AND kupil_lotov_v_jk BETWEEN 1 AND 5
              AND (tip_obremeneniya = 'ипотека' or tip_obremeneniya = 'Ипотека')
        
            ORDER BY otsenka_ceny
              ),
        
        curent_month AS (SELECT zalogoderzhatel, round(count(jk_rus)::numeric /
        (SELECT count(jk_rus) from filter WHERE extract(YEAR from data_registratsii) = 2025
              AND extract(MONTH from data_registratsii) = 8), 3) AS cur_procent,
              ROUND(AVG(ploshchad)::numeric,1) AS cur_ploshchad
        FROM filter
        WHERE extract(YEAR from data_registratsii) = 2025
              AND extract(MONTH from data_registratsii) = 8
        GROUP BY zalogoderzhatel
        ORDER BY count(jk_rus) desc
        LIMIT 5),
        
        prev_month AS (SELECT zalogoderzhatel, round(count(jk_rus)::numeric /
        (SELECT count(jk_rus) from filter WHERE extract(YEAR from data_registratsii) = 2025
              AND extract(MONTH from data_registratsii) = 7), 3) AS prev_procent,
              ROUND(AVG(ploshchad)::numeric,1) AS prev_ploshchad
        FROM filter
        WHERE extract(YEAR from data_registratsii) = 2025
              AND extract(MONTH from data_registratsii) = 7
        GROUP BY zalogoderzhatel
        ORDER BY count(jk_rus) desc
        )
        
        SELECT cm.zalogoderzhatel, pm.prev_procent, pm.prev_ploshchad, cur_procent, cur_ploshchad
        FROM curent_month AS cm
        LEFT JOIN prev_month AS pm ON cm.zalogoderzhatel = pm.zalogoderzhatel
        """


        df = pd.read_sql(sql_query_banks, conn)
        print('SQL запрос выполнен успешно')
        df['Динамика - Доля, %'] = np.where(
            (df['prev_procent'].isna()) | (df['prev_procent'] == 0),
            df['cur_procent'],
            df['cur_procent'] - df['prev_procent']
        )
        df['Динамика - Сред. площадь, кв.м'] = (df['cur_ploshchad']/ df['prev_ploshchad']-1)
        col_names = [
            'Банки',
            f"{months_ru[previous_month]} {year}, доля",
            f"{months_ru[previous_month]} {year}, средняя площадь, кв.м",
            f"{months_ru[month]} {year}, доля",
            f"{months_ru[month]} {year}, средняя площадь, кв.м",
            'Динамика: доля, %',
            'Динамика: ср. площадь, кв.м'
        ]
        df.columns = col_names

        # Заголовки многоуровневые



        df.insert(0, "Рейтинг", range(1, len(df) + 1))
        # Считаем взвешенные средние
        perc_prev_avg = (df["Июль 2025, доля"] * df["Июль 2025, средняя площадь, кв.м"]).sum() / df["Июль 2025, доля"].sum()
        perc_cur_avg = (df["Август 2025, доля"] * df["Август 2025, средняя площадь, кв.м"]).sum() / df[
            "Август 2025, доля"].sum()



        # Формируем строку "Итого"
        total_row = {
            "Рейтинг": "Итого",
            "Банки": "",
            "Июль 2025, доля": df["Июль 2025, доля"].sum(),
            "Июль 2025, средняя площадь, кв.м": round(perc_prev_avg, 1),
            "Август 2025, доля": df["Август 2025, доля"].sum(),
            "Август 2025, средняя площадь, кв.м": round(perc_cur_avg, 1),
            "Динамика: ср. площадь, кв.м": round((perc_cur_avg / perc_prev_avg) - 1, 3)
        }



        # Добавляем строку в DataFrame
        df = pd.concat([df, pd.DataFrame([total_row])], ignore_index=True)
        # Добавляем рейтинг 1–5

        print(df)



        # Пишем заголовки только для первого блока
        df.to_excel(writer, sheet_name="Банки", index=False, startrow=startrow, header=True)

        # Получаем ссылку на worksheet один раз
        if worksheet is None:
            worksheet = writer.sheets["Банки"]

        # Формат процентов
        percent_fmt = workbook.add_format({"num_format": "0.0%"})

        # Индексы столбцов
        col_idx_prev = df.columns.get_loc(f"{months_ru[previous_month]} {year}, доля")
        col_idx_current = df.columns.get_loc(f"{months_ru[month]} {year}, доля")
        col_idx_dynamic = df.columns.get_loc("Динамика: ср. площадь, кв.м")

        worksheet.set_column(col_idx_prev, col_idx_prev, 12, percent_fmt)
        worksheet.set_column(col_idx_current, col_idx_current, 12, percent_fmt)
        worksheet.set_column(col_idx_dynamic, col_idx_dynamic, 12, percent_fmt)



