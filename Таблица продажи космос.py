import pandas as pd
import numpy as np
import psycopg2
import time
import warnings
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font, Alignment

'''
Заполняем id проектов из нашей базы
Указываем 
'''

project_list = ["'6921'", "'6923'", "'7074'", "'4836'", "'1012'", "'5610'", "'5139'", "'6760'", "'1982'",
                "'1830'", "'1989'", "'1955'", "'4622'"]

year = 2025
previous_year = 2024
month = 9
previous_month = 8
file_name = 'Продажи конкурентов Космос'

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

months_ru = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель", 5: "Май", 6: "Июнь",
             7: "Июль", 8: "Август", 9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}



startrow0 = 0
startrow = 0  # отслеживаем, куда писать следующий проект
startrow2 = 0
startrow3 = 0

with pd.ExcelWriter(rf"C:\Users\m.olshanskiy\Desktop\{file_name}.xlsx", engine="xlsxwriter") as writer:
    workbook = writer.book
    worksheet0 = None
    worksheet = None
    worksheet2 = None
    worksheet3 = None
    worksheet4 = None



    sql_query_itog_sales = f"""
                    WITH prev_year_count AS (SELECT region, COUNT(id) AS py_count     
                    FROM pipin
                    WHERE tip_pomescheniya IN ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 2
                    AND EXTRACT(YEAR FROM data_registratsii) = {previous_year}
                    AND EXTRACT(MONTH FROM data_registratsii) = {month}
                    GROUP BY region 
                    ),

                    prev_month_count AS(SELECT region, COUNT(id) as pm_count       
                    FROM pipin
                    WHERE tip_pomescheniya IN ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 2
                    AND EXTRACT(YEAR FROM data_registratsii) = {year}
                    AND EXTRACT(MONTH FROM data_registratsii) = {previous_month}
                    GROUP BY region 
                    ),

                    current_month_count AS(SELECT region, COUNT(id) AS cur_count     
                    FROM pipin
                    WHERE tip_pomescheniya IN ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 2
                    AND EXTRACT(YEAR FROM data_registratsii) = {year}
                    AND EXTRACT(MONTH FROM data_registratsii) = {month}
                    GROUP BY region
                    )

                    SELECT current_month_count.region, py_count, pm_count, cur_count, (cur_count::numeric/py_count-1) AS year_to_year,
                    (cur_count::numeric/pm_count-1) AS month_to_month
                    FROM current_month_count
                    JOIN prev_year_count ON current_month_count.region = prev_year_count.region
                    JOIN prev_month_count ON current_month_count.region = prev_month_count.region

                    UNION ALL

                    SELECT
                        'Итого' AS region,
                        SUM(py_count) AS py_count,
                        SUM(pm_count) AS pm_count,
                        SUM(cur_count) AS cur_count,
                        (SUM(cur_count)::numeric / SUM(py_count) - 1) AS year_to_year,
                        (SUM(cur_count)::numeric / SUM(pm_count) - 1) AS month_to_month
                    FROM current_month_count
                    JOIN prev_year_count ON current_month_count.region = prev_year_count.region
                    JOIN prev_month_count ON current_month_count.region = prev_month_count.region
                    ;
                    """

    sql_query_itog_ipoteka = f'''
                    WITH prev_year AS (
                    SELECT
                        region,
                        COUNT(*) FILTER (WHERE ipoteka = 1)::numeric / COUNT(*) AS val
                    FROM pipin
                    WHERE extract(YEAR from data_registratsii) = {previous_year}
                      AND extract(MONTH from data_registratsii) = {month}
                      AND tip_pomescheniya IN ('квартира', 'апартамент')
                      AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                      AND kupil_lotov_v_jk BETWEEN 1 AND 5
                      AND otsenka_ceny IS NOT NULL
                    GROUP BY region
                ),
                prev_month AS (
                    SELECT
                        region,
                        COUNT(*) FILTER (WHERE ipoteka = 1)::numeric / COUNT(*) AS val
                    FROM pipin
                    WHERE extract(YEAR from data_registratsii) = {year}
                      AND extract(MONTH from data_registratsii) = {previous_month}
                      AND tip_pomescheniya IN ('квартира', 'апартамент')
                      AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                      AND kupil_lotov_v_jk BETWEEN 1 AND 5
                      AND otsenka_ceny IS NOT NULL
                    GROUP BY region
                ),
                now AS (
                    SELECT
                        region,
                        COUNT(*) FILTER (WHERE ipoteka = 1)::numeric / COUNT(*) AS val
                    FROM pipin
                    WHERE extract(YEAR from data_registratsii) = {year}
                      AND extract(MONTH from data_registratsii) = {month}
                      AND tip_pomescheniya IN ('квартира', 'апартамент')
                      AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                      AND kupil_lotov_v_jk BETWEEN 1 AND 5
                      AND otsenka_ceny IS NOT NULL
                    GROUP BY region
                ),
                totals AS (
                    SELECT 
                        (SELECT COUNT(*) FILTER (WHERE ipoteka = 1)::numeric / COUNT(*)
                         FROM pipin
                         WHERE extract(YEAR from data_registratsii) = {previous_year}
                           AND extract(MONTH from data_registratsii) = {month}
                           AND tip_pomescheniya IN ('квартира', 'апартамент')
                           AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                           AND kupil_lotov_v_jk BETWEEN 1 AND 5
                           AND otsenka_ceny IS NOT NULL) AS prev_year,
                        (SELECT COUNT(*) FILTER (WHERE ipoteka = 1)::numeric / COUNT(*)
                         FROM pipin
                         WHERE extract(YEAR from data_registratsii) = {year}
                           AND extract(MONTH from data_registratsii) = {previous_month}
                           AND tip_pomescheniya IN ('квартира', 'апартамент')
                           AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                           AND kupil_lotov_v_jk BETWEEN 1 AND 5
                           AND otsenka_ceny IS NOT NULL) AS prev_month,
                        (SELECT COUNT(*) FILTER (WHERE ipoteka = 1)::numeric / COUNT(*)
                         FROM pipin
                         WHERE extract(YEAR from data_registratsii) = {year}
                           AND extract(MONTH from data_registratsii) = {month}
                           AND tip_pomescheniya IN ('квартира', 'апартамент')
                           AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                           AND kupil_lotov_v_jk BETWEEN 1 AND 5
                           AND otsenka_ceny IS NOT NULL) AS now
                )
                SELECT *
                FROM (
                    SELECT
                        n.region,
                        py.val  AS prev_year,
                        pm.val  AS prev_month,
                        n.val   AS now,
                        (n.val - py.val) AS year_to_year,
                        (n.val - pm.val) AS month_to_month
                    FROM now n
                    LEFT JOIN prev_month pm ON n.region = pm.region
                    LEFT JOIN prev_year py  ON n.region = py.region
                
                    UNION ALL
                
                    SELECT
                        'Итого' AS region,
                        t.prev_year,
                        t.prev_month,
                        t.now,
                        (t.now - t.prev_year),
                        (t.now - t.prev_month)
                    FROM totals t
                ) q
                ORDER BY CASE WHEN region = 'Итого' THEN 1 ELSE 0 END, region; 
    
    '''

    try:
        df_itog = pd.read_sql(sql_query_itog_sales, conn)
        print('SQL запрос df_itog выполнен успешно')
    except:
        print('Ошибка. SQL запрос df_itog не выполнен')
    try:
        df_itog_ipoteka = pd.read_sql(sql_query_itog_ipoteka, conn)
        print('SQL запрос df_itog_ipoteka выполнен успешно')
    except:
        print('Ошибка. SQL запрос df_itog_ipoteka не выполнен')

    df_itog_columns = [
        'Регион',
        f"{months_ru[month]} {previous_year}",
        f"{months_ru[previous_month]} {year}",
        f"{months_ru[month]} {year}",
        "год/год",
        'месяц/месяц'
    ]
    df_itog.columns = df_itog_columns
    df_itog_ipoteka.columns = df_itog_columns

    # список столбцов с процентами
    cols_df_itog_ipoteka = [f'{months_ru[month]} {previous_year}', f'{months_ru[previous_month]} {year}',
                            f'{months_ru[month]} {year}', 'год/год', 'месяц/месяц']
    cols_df_itog = ['год/год', 'месяц/месяц']

    worksheet0 = workbook.add_worksheet("Итоги реализации")

    # Форматы
    format_title = workbook.add_format({'bold': True, 'font_size': 16})
    format_subtitle = workbook.add_format({'bold': True, 'font_size': 12})

    startrow0 = 0

    # Крупный заголовок
    worksheet0.write(startrow0, 0, f"Итоги реализации в Московской агломерации, {months_ru[month]} {year} г.",
                     format_title)
    startrow0 += 2  # отступ после заголовка

    # Подзаголовок для первой таблицы
    worksheet0.write(startrow0, 0, "Количество реализованных лотов, шт.", format_subtitle)
    startrow0 += 1

    # Первая таблица
    df_itog.to_excel(writer, sheet_name="Итоги реализации", startrow=startrow0, index=False, header=True)
    startrow0 += len(df_itog) + 3  # оставляем отступ

    # Заголовок перед второй таблицей
    worksheet0.write(startrow0, 0, "Доля ипотечных сделок, %", format_subtitle)
    startrow0 += 1

    # Вторая таблица
    df_itog_ipoteka.to_excel(writer, sheet_name="Итоги реализации", startrow=startrow0, index=False, header=True)

    for i, project in enumerate(project_list):

        project_name_sql = f"""
            select distinct project_name
            from pipin
            where id = {project}
            """
        cur = conn.cursor()
        # Выполняем запрос
        cur.execute(project_name_sql)

        # Получаем одно значение
        project_name_text = cur.fetchone()[0]
        print(project_name_text)

        sql_query = f"""
        WITH
        prev_year AS (
                SELECT COUNT(id) AS val
                FROM pipin
                WHERE id = {project}
                AND extract(YEAR from data_registratsii) = {previous_year}
                AND extract(MONTH from data_registratsii) = {month}
                AND tip_pomescheniya in ('квартира', 'апартамент')
                AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                AND kupil_lotov_v_jk BETWEEN 1 AND 5
                AND otsenka_ceny is not NULL
        ),
        prev_month AS (
                SELECT COUNT(id) AS val
                FROM pipin
                WHERE id = {project}
                AND extract(YEAR from data_registratsii) = {year}
                AND extract(MONTH from data_registratsii) = {previous_month}
                AND tip_pomescheniya in ('квартира', 'апартамент')
                AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                AND kupil_lotov_v_jk BETWEEN 1 AND 5
                AND otsenka_ceny is not NULL
        ),
        now AS (
            SELECT COUNT(id) AS val
                FROM pipin
                WHERE id = {project}
                AND extract(YEAR from data_registratsii) = {year}
                AND extract(MONTH from data_registratsii) = {month}
                AND tip_pomescheniya in ('квартира', 'апартамент')
                AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                AND kupil_lotov_v_jk BETWEEN 1 AND 5
                AND otsenka_ceny is not NULL
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val::numeric / NULLIF(prev_year.val, 0) - 1) AS year_to_year,
            (now.val::numeric / NULLIF(prev_month.val, 0) - 1) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        sql_query2 = f"""
        WITH
        prev_year AS (
                SELECT round((sum(price_total_discounted) / sum(area_sqm)) / 1000, 1) AS val
                from ndv_data
                Join ids ON ndv_data.project_name = ids.project_name
                WHERE id = {project}
                and extract(year from date) = {previous_year}
                and extract(month from date) = {month}
                
        ),
        prev_month AS (
                SELECT round((sum(price_total_discounted) / sum(area_sqm)) / 1000, 1) AS val
                from ndv_data
                Join ids ON ndv_data.project_name = ids.project_name
                WHERE id = {project}
                and extract(year from date) = {year}
                and extract(month from date) = {previous_month}
        ),
        now AS (
                SELECT round((sum(price_total_discounted) / sum(area_sqm)) / 1000, 1) AS val
                from ndv_data
                Join ids ON ndv_data.project_name = ids.project_name
                WHERE id = {project}
                and extract(year from date) = {year}
                and extract(month from date) = {month}
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
        prev_year AS (SELECT round(AVG(area_sqm)::numeric, 1) as val
                    from pipin
                    WHERE id = {project}
                    AND extract(YEAR from data_registratsii) = {previous_year}
                    AND extract(MONTH from data_registratsii) = {month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        ),
        prev_month AS (SELECT round(AVG(area_sqm)::numeric, 1) as val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {previous_month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        ),
        now AS ( SELECT round(AVG(area_sqm)::numeric, 1) as val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
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
        prev_year AS (SELECT round(AVG(otsenka_ceny) / 1000000, 1) as val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {previous_year}
                    and extract(MONTH from data_registratsii) = {month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        ),
        prev_month AS (SELECT round(AVG(otsenka_ceny) / 1000000, 1) as val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {previous_month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        ),
        now AS ( SELECT round(AVG(otsenka_ceny)/ 1000000, 1) as val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
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
        SELECT COUNT(id)
        from pipin
        WHERE id = {project}
        and extract(YEAR from data_registratsii) = {previous_year}
        and extract(MONTH from data_registratsii) = {month}
        and ipoteka = 1
        AND tip_pomescheniya in ('квартира', 'апартамент')
        AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
        AND kupil_lotov_v_jk BETWEEN 1 AND 5
        AND otsenka_ceny is not NULL
        )::numeric / NULLIF(COUNT(id), 0) AS val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {previous_year}
                    and extract(MONTH from data_registratsii) = {month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        
        ),
        prev_month AS (SELECT (
        SELECT COUNT(id)
        from pipin
        WHERE id = {project}
        and extract(YEAR from data_registratsii) = {year}
        and extract(MONTH from data_registratsii) = {previous_month}
        and ipoteka = 1
        AND tip_pomescheniya in ('квартира', 'апартамент')
        AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
        AND kupil_lotov_v_jk BETWEEN 1 AND 5
        AND otsenka_ceny is not NULL
        )::numeric / NULLIF(COUNT(id), 0) AS val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {previous_month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        ),
        now AS ( SELECT (
        SELECT COUNT(id)
        from pipin
        WHERE id = {project}
        and extract(YEAR from data_registratsii) = {year}
        and extract(MONTH from data_registratsii) = {month}
        and ipoteka = 1
        AND tip_pomescheniya in ('квартира', 'апартамент')
        AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
        AND kupil_lotov_v_jk BETWEEN 1 AND 5
        AND otsenka_ceny is not NULL
        )::numeric / NULLIF(COUNT(id), 0) AS val
                    from pipin
                    WHERE id = {project}
                    and extract(YEAR from data_registratsii) = {year}
                    and extract(MONTH from data_registratsii) = {month}
                    AND tip_pomescheniya in ('квартира', 'апартамент')
                    AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                    AND kupil_lotov_v_jk BETWEEN 1 AND 5
                    AND otsenka_ceny is not NULL
        )
        
        SELECT
            prev_year.val  AS prev_year,
            prev_month.val AS prev_month,
            now.val        AS now,
            (now.val - prev_year.val) AS year_to_year,
            (now.val - prev_month.val) AS month_to_month
        
        FROM now, prev_month, prev_year;
        """

        sql_query_tip_komnatnosti = f"""
WITH flats AS (
    SELECT 
        tip_komnatnosti,
        area_sqm,
        EXTRACT(YEAR FROM data_registratsii) AS yy,
        EXTRACT(MONTH FROM data_registratsii) AS mm
    FROM pipin
    WHERE id = {project}
      AND tip_pomescheniya IN ('квартира', 'апартамент')
      AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
      AND kupil_lotov_v_jk BETWEEN 1 AND 5
      AND otsenka_ceny IS NOT NULL
),
flat_count AS (
    SELECT yy, mm, COUNT(*) AS total_count
    FROM flats
    GROUP BY yy, mm
),
stats AS (
    SELECT 
        f.tip_komnatnosti,
        f.yy,
        f.mm,
        ROUND(COUNT(*)::numeric / fc.total_count, 2) AS percent,
        ROUND(AVG(f.area_sqm)::numeric, 1) AS avg_metr
    FROM flats f
    JOIN flat_count fc ON f.yy = fc.yy AND f.mm = fc.mm
    GROUP BY f.tip_komnatnosti, f.yy, f.mm, fc.total_count
),
joined AS (
    SELECT 
        cur.tip_komnatnosti,
        prev.percent AS percent_prev,
        cur.avg_metr AS avg_metr_now,
        cur.percent AS percent_now,        
        prev.avg_metr AS avg_metr_prev
        
    FROM stats cur
    LEFT JOIN stats prev 
           ON cur.tip_komnatnosti = prev.tip_komnatnosti
          AND (cur.yy * 12 + cur.mm - 1) = (prev.yy * 12 + prev.mm)
    WHERE cur.yy = {year} AND cur.mm = {month}
),
total AS (
    SELECT
        'Общий итог' AS tip_komnatnosti,
        1.00 AS percent_now,
        -- реальная средняя по всем квартирам текущего месяца
        (SELECT ROUND(AVG(area_sqm)::numeric,1)
         FROM pipin
         WHERE id = {project}
           AND EXTRACT(YEAR FROM data_registratsii) = {year}
           AND EXTRACT(MONTH FROM data_registratsii) = {month}
           AND tip_pomescheniya IN ('квартира','апартамент')
           AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
           AND kupil_lotov_v_jk BETWEEN 1 AND 5
           AND otsenka_ceny IS NOT NULL) AS avg_metr_now,
        1.00 AS percent_prev,
        -- реальная средняя по всем квартирам предыдущего месяца
        (SELECT ROUND(AVG(area_sqm)::numeric,1)
         FROM pipin
         WHERE id = {project}
           AND EXTRACT(YEAR FROM data_registratsii) = {year}
           AND EXTRACT(MONTH FROM data_registratsii) = {previous_month}
           AND tip_pomescheniya IN ('квартира','апартамент')
           AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
           AND kupil_lotov_v_jk BETWEEN 1 AND 5
           AND otsenka_ceny IS NOT NULL) AS avg_metr_prev
)
SELECT * FROM (
    SELECT * FROM joined
    UNION ALL
    SELECT * FROM total
) AS final
ORDER BY
    CASE 
        WHEN tip_komnatnosti = 'ст' THEN 1
        WHEN tip_komnatnosti ~ '^[0-9]+$' THEN 2
        WHEN tip_komnatnosti = 'Общий итог' THEN 3
        ELSE 4
    END,
    CASE 
        WHEN tip_komnatnosti ~ '^[0-9]+$' THEN tip_komnatnosti::int
    END;
        """

        sql_query_banks = f"""
                WITH filter AS (
                    SELECT *       
                    FROM pipin
                    WHERE id = {project}
                      AND tip_pomescheniya IN ('квартира', 'апартамент')
                      AND (pokupatel_yul IS NULL OR pokupatel_yul = '')
                      AND kupil_lotov_v_jk BETWEEN 1 AND 5
                      AND (tip_obremeneniya = 'ипотека' or tip_obremeneniya = 'Ипотека')

                    ORDER BY otsenka_ceny
                      ),

                curent_month AS (SELECT zalogoderzhatel, round(count(id)::numeric /
                (SELECT count(id) from filter WHERE extract(YEAR from data_registratsii) = {year}
                      AND extract(MONTH from data_registratsii) = {month}), 3) AS cur_procent,
                      ROUND(AVG(area_sqm)::numeric,1) AS cur_ploshchad
                FROM filter
                WHERE extract(YEAR from data_registratsii) = {year}
                      AND extract(MONTH from data_registratsii) = {month}
                GROUP BY zalogoderzhatel
                ORDER BY count(id) desc
                LIMIT 5),

                prev_month AS (SELECT zalogoderzhatel, round(count(id)::numeric /
                (SELECT count(id) from filter WHERE extract(YEAR from data_registratsii) = {year}
                      AND extract(MONTH from data_registratsii) = {previous_month}), 3) AS prev_procent,
                      ROUND(AVG(area_sqm)::numeric,1) AS prev_ploshchad
                FROM filter
                WHERE extract(YEAR from data_registratsii) = {year}
                      AND extract(MONTH from data_registratsii) = {previous_month}
                GROUP BY zalogoderzhatel
                ORDER BY count(id) desc
                )

                SELECT cm.zalogoderzhatel, pm.prev_procent, pm.prev_ploshchad, cur_procent, cur_ploshchad
                FROM curent_month AS cm
                LEFT JOIN prev_month AS pm ON cm.zalogoderzhatel = pm.zalogoderzhatel
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
        print('SQL запрос выполнен успешно')
        df2 = pd.read_sql(sql_query2, conn)
        print('SQL запрос выполнен успешно')
        df3 = pd.read_sql(sql_query3, conn)
        print('SQL запрос выполнен успешно')
        df4 = pd.read_sql(sql_query4, conn)
        print('SQL запрос выполнен успешно')
        df5 = pd.read_sql(sql_query5, conn)
        print('SQL запрос выполнен успешно')
        df6 = pd.read_sql(sql_query_tip_komnatnosti, conn)
        print('SQL запрос выполнен успешно')
        df_banks = pd.read_sql(sql_query_banks, conn)
        print('SQL запрос df_banks выполнен успешно')

        result = pd.concat([df, df2, df3, df4, df5], ignore_index=True)
        result.insert(0, "Характеристика", chars)
        col_names = [
            project_name_text,
            f"{months_ru[month]} {previous_year}",
            f"{months_ru[previous_month]} {year}",
            f"{months_ru[month]} {year}",
            "год/год",
            "мес/мес"
        ]
        col_names_komnatnost = [
            project_name_text,
            f"Доля,% {months_ru[previous_month]} {year}",
            f"Средняя площадь,кв.м {months_ru[previous_month]} {year}",
            f"Доля,% {months_ru[month]} {year}",
            f"Средняя площадь,кв.м {months_ru[month]} {year}"
        ]
        result.columns = col_names
        df6.columns = col_names_komnatnost

        df_banks['Динамика - Доля, %'] = np.where(
            (df_banks['prev_procent'].isna()) | (df_banks['prev_procent'] == 0),
            df_banks['cur_procent'],
            df_banks['cur_procent'] - df_banks['prev_procent']
        )
        df_banks['Динамика - Сред. площадь, кв.м'] = (df_banks['cur_ploshchad'] / df_banks['prev_ploshchad'] - 1)
        col_names = [
            'Банки',
            f"{months_ru[previous_month]} {year}, доля",
            f"{months_ru[previous_month]} {year}, средняя площадь, кв.м",
            f"{months_ru[month]} {year}, доля",
            f"{months_ru[month]} {year}, средняя площадь, кв.м",
            'Динамика: доля, %',
            'Динамика: ср. площадь, кв.м'
        ]
        df_banks.columns = col_names

        df_banks.insert(0, project_name_text, range(1, len(df_banks) + 1))
        # Считаем взвешенные средние
        # Взвешенное среднее за прошлый месяц
        if df_banks[f"{months_ru[previous_month]} {year}, доля"].sum() != 0:
            perc_prev_avg = (
                    (df_banks[f"{months_ru[previous_month]} {year}, доля"] * df_banks[
                        f"{months_ru[previous_month]} {year}, средняя площадь, кв.м"]).sum()
                    / df_banks[f"{months_ru[previous_month]} {year}, доля"].sum()
            )
        else:
            perc_prev_avg = 0  # или np.nan, если хочешь именно пропуск

        # Взвешенное среднее за текущий месяц
        if df_banks[f"{months_ru[month]} {year}, доля"].sum() != 0:
            perc_cur_avg = (
                    (df_banks[f"{months_ru[month]} {year}, доля"] * df_banks[
                        f"{months_ru[month]} {year}, средняя площадь, кв.м"]).sum()
                    / df_banks[f"{months_ru[month]} {year}, доля"].sum()
            )
        else:
            perc_cur_avg = 0  # или np.nan

        if perc_prev_avg != 0:
            dinamika_total = round((perc_cur_avg / perc_prev_avg) - 1, 3)
        else:
            dinamika_total = 0  # или np.nan

        # Формируем строку "Итого"
        total_row = {
            project_name_text: "Итого",
            "Банки": "",
            f"{months_ru[previous_month]} {year}, доля": df_banks[f"{months_ru[previous_month]} {year}, доля"].sum(),
            f"{months_ru[previous_month]} {year}, средняя площадь, кв.м": round(perc_prev_avg, 1),
            f"{months_ru[month]} {year}, доля": df_banks[f"{months_ru[month]} {year}, доля"].sum(),
            f"{months_ru[month]} {year}, средняя площадь, кв.м": round(perc_cur_avg, 1),
            "Динамика: ср. площадь, кв.м": dinamika_total
        }

        # Добавляем строку в DataFrame
        df_banks = pd.concat([df_banks, pd.DataFrame([total_row])], ignore_index=True)

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

        # Записываем сам df6, начиная с текущего startrow2
        df6.to_excel(writer, sheet_name="Тип комнатности", index=False, startrow=startrow2, header=True)

        if worksheet2 is None:
            # временно записываем пустой DataFrame, чтобы создать лист
            pd.DataFrame().to_excel(writer, sheet_name="Тип комнатности", index=False)
            worksheet2 = writer.sheets["Тип комнатности"]

        # Формат процентов
        percent_fmt = workbook.add_format({"num_format": "0.0%"})

        # Индексы столбцов
        col_idx_year = df6.columns.get_loc(f"Доля,% {months_ru[previous_month]} {year}")
        col_idx_month = df6.columns.get_loc(f"Доля,% {months_ru[month]} {year}")

        worksheet2.set_column(col_idx_year, col_idx_year, 12, percent_fmt)
        worksheet2.set_column(col_idx_month, col_idx_month, 12, percent_fmt)

        # Пишем название проекта жирным шрифтом
        # bold_fmt = workbook.add_format({"bold": True})
        # worksheet2.write(startrow2, 0, project, bold_fmt)

        # Сдвигаем startrow2 вниз для следующего проекта
        startrow2 += len(df6) + 2

        # Пишем заголовки только для первого блока
        df_banks.to_excel(writer, sheet_name="Банки", index=False, startrow=startrow3, header=True)

        # Получаем ссылку на worksheet один раз
        if worksheet3 is None:
            worksheet3 = writer.sheets["Банки"]

        # Формат процентов
        percent_fmt = workbook.add_format({"num_format": "0.0%"})

        # Индексы столбцов
        col_idx_prev = df_banks.columns.get_loc(f"{months_ru[previous_month]} {year}, доля")
        col_idx_current = df_banks.columns.get_loc(f"{months_ru[month]} {year}, доля")
        dolya_dynamic = df_banks.columns.get_loc("Динамика: доля, %")
        area_dynamic = df_banks.columns.get_loc("Динамика: ср. площадь, кв.м")

        worksheet3.set_column(col_idx_prev, col_idx_prev, 12, percent_fmt)
        worksheet3.set_column(col_idx_current, col_idx_current, 12, percent_fmt)
        worksheet3.set_column(dolya_dynamic, dolya_dynamic, 12, percent_fmt)
        worksheet3.set_column(area_dynamic, area_dynamic, 12, percent_fmt)

        # Сдвигаем startrow2 вниз для следующего проекта
        startrow3 += len(df_banks) + 2
