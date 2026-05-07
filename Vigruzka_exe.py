import psycopg2
import pandas as pd
import warnings
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="pandas only supports SQLAlchemy connectable",
)

# =========================
# Функция выгрузки
# =========================

def export_data():

    year = year_entry.get().strip()
    month = month_entry.get().strip()
    project = project_entry.get().strip()

    if not year or not month:
        messagebox.showerror("Ошибка", "Введите год и месяц")
        return

    if project == "":
        project = None

    # выбор папки
    folder = filedialog.askdirectory(title="Выберите папку для сохранения")

    if not folder:
        return

    try:
        conn = psycopg2.connect(
            'postgresql://postgres:PassToPostgres$@192.168.252.134:5432/ndv_database'
        )

    except Exception as e:
        messagebox.showerror(
            "Ошибка подключения",
            str(e)
        )
        return

    sql_query = f"""
    SELECT *
    FROM ndv_data
    WHERE EXTRACT(YEAR FROM date) = {year}
      AND EXTRACT(MONTH FROM date) = {month}
    """

    if project:
        sql_query += f"\nAND project_name ILIKE '%{project}%'"

    try:

        df = pd.read_sql(sql_query, conn)

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
            'location_big': 'Локация'
        })

        if df.empty:
            messagebox.showwarning(
                "Нет данных",
                "По вашему запросу ничего не найдено"
            )
            return

        filename = f'Выгрузка_{year}_{month}.xlsx'

        if project:
            filename = f'Выгрузка_{project}_{year}_{month}.xlsx'

        full_path = f"{folder}/{filename}"

        df.to_excel(full_path, index=False)

        messagebox.showinfo(
            "Успешно",
            f"Файл сохранён:\n{full_path}"
        )

    except Exception as e:
        messagebox.showerror(
            "Ошибка SQL",
            str(e)
        )

    finally:
        conn.close()


# =========================
# GUI
# =========================

root = tk.Tk()
root.title("Выгрузка NDV")
root.geometry("400x320")
root.resizable(False, False)

# стиль
style = ttk.Style()
style.theme_use('clam')

# заголовок
title_label = ttk.Label(
    root,
    text="Выгрузка данных NDV",
    font=("Arial", 14, "bold")
)
title_label.pack(pady=15)

# год
year_label = ttk.Label(root, text="Год:")
year_label.pack()

year_entry = ttk.Entry(root, width=30)
year_entry.pack(pady=5)

# месяц
month_label = ttk.Label(root, text="Месяц:")
month_label.pack()

month_entry = ttk.Entry(root, width=30)
month_entry.pack(pady=5)

# проект
project_label = ttk.Label(
    root,
    text="Проект (необязательно):"
)
project_label.pack()

project_entry = ttk.Entry(root, width=30)
project_entry.pack(pady=5)

# кнопка
export_button = ttk.Button(
    root,
    text="Выгрузить Excel",
    command=export_data
)
export_button.pack(pady=20)

root.mainloop()