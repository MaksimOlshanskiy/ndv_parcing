import pandas as pd
import numpy as np
import psycopg2
import time


# localhost
try:
    # пытаемся подключиться к базе данных
    conn = psycopg2.connect('postgresql://postgres:ndv212XO@localhost:5432/postgres')
    print('Подключились к базе данных')
except:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('Ошибка подключения к базе данных')

projects_dict = {"'Скай Гарден'" : "'Sky Garden'", "'Ситизен'" : "'CITYZEN'", "'Сити Бэй'" : "'City Bay'"}
months_ru = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
             7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}

project_list = ["'Бусиновский парк'", "'Митинский лес'", "'Молжаниново'", "'Куркино 15'", "'Скай Гарден'", "'Ситизен'", "'Сити Бэй'"]
startrow = 0  # отслеживаем, куда писать следующий проект

with pd.ExcelWriter(r"C:\Users\m.olshanskiy\Desktop\SQL.xlsx", engine="xlsxwriter") as writer:
    workbook  = writer.book
    worksheet = None


    for i, project in enumerate(project_list):
        print(startrow)
        print(project)
        year = 2025
        previous_year = 2024
        month = 8
        previous_month = 7

        sql_query = f"""
        WITH
        prev_year AS (
                SELECT COUNT(id_jk) AS val
                FROM pipin
                WHERE jk_rus = {project}
                AND extract(YEAR from data_registratsii) = {previous_year}
                AND extract(MONTH from data_registratsii) = {month}
        ),
        prev_month AS (
                SELECT COUNT(id_jk) AS val
                FROM pipin
                WHERE jk_rus = {project}
                AND extract(YEAR from data_registratsii) = {year}
                AND extract(MONTH from data_registratsii) = {previous_month}
        ),
        now AS (
            SELECT COUNT(id_jk) AS val
                FROM pipin
                WHERE jk_rus = {project}
                AND extract(YEAR from data_registratsii) = {year}
                AND extract(MONTH from data_registratsii) = {month}
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val::numeric / prev_year.val - 1) AS year_to_year,
            (now.val::numeric / prev_month.val - 1) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        sql_query2 = f"""
        WITH
        prev_year AS (
                SELECT round((sum(price_total_discounted) / sum(area_sqm)) / 1000, 1) AS val
                from ndv.ndv_data
                WHERE project_name = {projects_dict.get(project, project)}
                and extract(year from update_date) = {previous_year}
                and extract(month from update_date) = {month}
        ),
        prev_month AS (
                SELECT round((sum(price_total_discounted) / sum(area_sqm)) / 1000, 1) AS val
                from ndv.ndv_data
                WHERE project_name = {projects_dict.get(project, project)}
                and extract(year from update_date) = {year}
                and extract(month from update_date) = {previous_month}
        ),
        now AS (
                SELECT round((sum(price_total_discounted) / sum(area_sqm)) / 1000, 1) AS val
                from ndv.ndv_data
                WHERE project_name = {projects_dict.get(project, project)}
                and extract(year from update_date) = {year}
                and extract(month from update_date) = {month}
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val::numeric / prev_year.val - 1) AS year_to_year,
            (now.val::numeric / prev_month.val - 1) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        sql_query3 = f"""
        WITH
        prev_year AS (SELECT round(AVG(area_sqm), 1) as val
                    from ndv.ndv_data
                    WHERE project_name = {projects_dict.get(project, project)}
                    and extract(YEAR from update_date) = {previous_year}
                    and extract(MONTH from update_date) = {month}
        ),
        prev_month AS (SELECT round(AVG(area_sqm), 1) as val
                    from ndv.ndv_data
                    WHERE project_name = {projects_dict.get(project, project)}
                    and extract(YEAR from update_date) = {year}
                    and extract(MONTH from update_date) = {previous_month}
        ),
        now AS ( SELECT round(AVG(area_sqm), 1) as val
                    from ndv.ndv_data
                    WHERE project_name = {projects_dict.get(project, project)}
                    and extract(YEAR from update_date) = {year}
                    and extract(MONTH from update_date) = {month}
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val::numeric / prev_year.val - 1) AS year_to_year,
            (now.val::numeric / prev_month.val - 1) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        sql_query4 = f"""
        WITH
        prev_year AS (SELECT round(AVG(price_total_discounted) / 1000000, 1) as val
                    from ndv.ndv_data
                    WHERE project_name = {projects_dict.get(project, project)}
                    and extract(YEAR from update_date) = {previous_year}
                    and extract(MONTH from update_date) = {month}
        ),
        prev_month AS (SELECT round(AVG(price_total_discounted) / 1000000, 1) as val
                    from ndv.ndv_data
                    WHERE project_name = {projects_dict.get(project, project)}
                    and extract(YEAR from update_date) = {year}
                    and extract(MONTH from update_date) = {previous_month}
        ),
        now AS ( SELECT round(AVG(price_total_discounted)/ 1000000, 1) as val
                    from ndv.ndv_data
                    WHERE project_name = {projects_dict.get(project, project)}
                    and extract(YEAR from update_date) = {year}
                    and extract(MONTH from update_date) = {month}
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val::numeric / prev_year.val - 1) AS year_to_year,
            (now.val::numeric / prev_month.val - 1) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        sql_query5 = f"""
        WITH
        prev_year AS (SELECT (
        SELECT COUNT(id_jk)
        from pipin
        WHERE jk_rus = {project}
        and extract(YEAR from data_registratsii) = {previous_year}
        and extract(MONTH from data_registratsii) = {month}
        and ipoteka = 1
        )::numeric / COUNT(id_jk) AS val
                    from pipin
                    WHERE jk_rus = {project}
                    and extract(YEAR from data_registratsii) = {previous_year}
                    and extract(MONTH from data_registratsii) = {month}
        
        ),
        prev_month AS (SELECT (
        SELECT COUNT(id_jk)
        from pipin
        WHERE jk_rus = {project}
        and extract(YEAR from data_registratsii) = {year}
        and extract(MONTH from data_registratsii) = {previous_month}
        and ipoteka = 1
        )::numeric / COUNT(id_jk) AS val
                    from pipin
                    WHERE jk_rus = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {previous_month}
        ),
        now AS ( SELECT (
        SELECT COUNT(id_jk)
        from pipin
        WHERE jk_rus = {project}
        and extract(YEAR from data_registratsii) = {year}
        and extract(MONTH from data_registratsii) = {month}
        and ipoteka = 1
        )::numeric / COUNT(id_jk) AS val
                    from pipin
                    WHERE jk_rus = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {month}
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val - prev_year.val) AS year_to_year,
            (now.val - prev_month.val) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        pd.set_option("display.float_format", "{:.2f}".format)
        chars = [
            "Кол-во,шт.",
            "СВЦ, тыс. руб.",
            "Средняя площадь, кв.м",
            "Средняя цена, млн руб.",
            "Доля ипотеки,%"
        ]
        df = pd.read_sql(sql_query, conn)
        df2 = pd.read_sql(sql_query2, conn)
        df3 = pd.read_sql(sql_query3, conn)
        df4 = pd.read_sql(sql_query4, conn)
        df5 = pd.read_sql(sql_query5, conn)

        result = pd.concat([df, df2, df3, df4, df5], ignore_index=True)
        result.insert(0, "Характеристика", chars)
        col_names = [
            project,
            f"{months_ru[month]} {previous_year}",
            f"{months_ru[previous_month]} {year}",
            f"{months_ru[month]} {year}",
            "год/год",
            "мес/мес"
        ]
        result.columns = col_names

        # Пишем заголовки только для первого блока
        result.to_excel(writer, sheet_name="Данные", index=False, startrow=startrow, header=True)

        # Получаем ссылку на worksheet один раз
        if worksheet is None:
            worksheet = writer.sheets["Данные"]

        # Формат процентов
        percent_fmt = workbook.add_format({"num_format": "0.0%"})

        # Индексы столбцов
        col_idx_year = result.columns.get_loc("год/год")
        col_idx_month = result.columns.get_loc("мес/мес")

        worksheet.set_column(col_idx_year, col_idx_year, 12, percent_fmt)
        worksheet.set_column(col_idx_month, col_idx_month, 12, percent_fmt)

        # Строка "Доля ипотеки,%"
        row_idx_ipoteka = result.index[result.iloc[:, 0] == "Доля ипотеки,%"][0]
        worksheet.set_row(startrow + row_idx_ipoteka + 1, None, percent_fmt)  # +1 из-за заголовка

        # Сдвигаем startrow вниз для следующего блока
        startrow += len(result) + 2

