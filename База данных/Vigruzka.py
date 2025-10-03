import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import psycopg2

def load_values():
    """Подгрузка списков проектов и застройщиков из БД"""
    try:
        conn = psycopg2.connect('postgresql://postgres:ndv212XO@localhost:5432/postgres')
        cur = conn.cursor()

        cur.execute("SELECT DISTINCT lower(project_name) FROM ndv_data ORDER BY 1")
        projects = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT lower(developer) FROM ndv_data ORDER BY 1")
        developers = [row[0] for row in cur.fetchall()]

        conn.close()
        return projects, developers
    except Exception as e:
        messagebox.showerror("Ошибка подключения", f"Не удалось загрузить списки: {e}")
        return [], []

def run_query():
    try:
        year = int(year_var.get())
        month = int(month_var.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Год и месяц должны быть числами")
        return

    previous_year = year - 1
    previous_month = 12 if month == 1 else month - 1

    # --- выбор SQL-запроса по периоду ---
    period_mode = period_var.get()
    if period_mode == "one_month":
        sql_query = f"""
        SELECT *
        FROM ndv_data
        WHERE (EXTRACT(YEAR from update_date) = {year}
        AND EXTRACT(MONTH from update_date) = {month})
        """
    elif period_mode == "month_to_month":
        sql_query = f"""
        SELECT *
        FROM ndv_data
        WHERE (EXTRACT(YEAR from update_date) = {previous_year}
        AND EXTRACT(MONTH from update_date) = {month})
        OR (EXTRACT(YEAR from update_date) = {year}
        AND EXTRACT(MONTH from update_date) = {previous_month})
        """
    elif period_mode == "month_year_compare":
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
    else:
        messagebox.showerror("Ошибка", "Выберите режим периода")
        return

    # --- фильтр по проекту / застройщику ---
    filter_mode = filter_var.get()
    if filter_mode == "project":
        value = project_combo.get().strip().lower()
        if not value:
            messagebox.showerror("Ошибка", "Выберите проект")
            return
        sql_query += f" AND lower(project_name) = '{value}'"
    elif filter_mode == "developer":
        value = developer_combo.get().strip().lower()
        if not value:
            messagebox.showerror("Ошибка", "Выберите застройщика")
            return
        sql_query += f" AND lower(developer) = '{value}'"

    # --- подключение ---
    try:
        conn = psycopg2.connect('postgresql://postgres:ndv212XO@localhost:5432/postgres')
    except Exception as e:
        messagebox.showerror("Ошибка подключения", str(e))
        return

    try:
        df = pd.read_sql(sql_query, conn)
    except Exception as e:
        messagebox.showerror("Ошибка SQL", str(e))
        return

    df.columns = [
        "Дата обновления", "Название проекта", "На англ", "Промзона", "Местоположение", "Метро",
        "Расстояние до метро, км", "Время до метро, мин", "Мцк/мцд/бкл", "Расстояние до мцк/мцд, км",
        "Время до мцк/мцд, мин", "Бкл", "Расстояние до бкл, км", "Время до бкл, мин", "Статус",
        "Старт", "Комментарий", "Девелопер", "Округ", "Район", "Адрес", "Эскроу", "Корпус",
        "Конструктив", "Класс", "Срок сдачи", "Старый срок сдачи", "Стадия строительной готовности",
        "Договор", "Тип помещения", "Отделка", "Кол-во комнат", "Площадь, кв.м", "Цена кв.м, руб.",
        "Цена лота, руб.", "Скидка,%", "Цена кв.м со ск, руб.", "Цена со скидкой, руб."
    ]

    # --- сохранение ---
    save_path = filedialog.asksaveasfilename(
        title="Сохранить как...",
        defaultextension=".xlsx",
        filetypes=[("Excel файлы", "*.xlsx"), ("Все файлы", "*.*")]
    )
    if not save_path:
        return

    try:
        df.to_excel(save_path, index=False)
        messagebox.showinfo("Готово", f"Файл сохранён:\n{save_path}")
    except Exception as e:
        messagebox.showerror("Ошибка сохранения", str(e))


# --- GUI ---
root = tk.Tk()
root.title("Выгрузка из базы PostgreSQL")
root.geometry("500x500")

# Год
tk.Label(root, text="Введите год:").pack(pady=5)
year_var = tk.StringVar(value="2025")
tk.Entry(root, textvariable=year_var).pack(pady=5)

# Месяц
tk.Label(root, text="Введите месяц:").pack(pady=5)
month_var = tk.StringVar(value="9")
tk.Entry(root, textvariable=month_var).pack(pady=5)

# --- блок выбора фильтра ---
tk.Label(root, text="Что выгружать:").pack(pady=5)
filter_var = tk.StringVar(value="all")

tk.Radiobutton(root, text="Всё", variable=filter_var, value="all",
               command=lambda: show_filter("all")).pack(anchor="w", padx=20)
tk.Radiobutton(root, text="По проекту", variable=filter_var, value="project",
               command=lambda: show_filter("project")).pack(anchor="w", padx=20)
tk.Radiobutton(root, text="По застройщику", variable=filter_var, value="developer",
               command=lambda: show_filter("developer")).pack(anchor="w", padx=20)

# Combobox для проектов и застройщиков
projects, developers = load_values()
project_combo = ttk.Combobox(root, values=projects, state="readonly", width=40)
developer_combo = ttk.Combobox(root, values=developers, state="readonly", width=40)

def show_filter(mode):
    project_combo.pack_forget()
    developer_combo.pack_forget()
    if mode == "project":
        project_combo.pack(pady=5)
    elif mode == "developer":
        developer_combo.pack(pady=5)

# --- блок выбора периода ---
tk.Label(root, text="Режим периода:").pack(pady=5)
period_var = tk.StringVar(value="")
tk.Radiobutton(root, text="За один месяц", variable=period_var, value="one_month").pack(anchor="w", padx=20)
tk.Radiobutton(root, text="Месяц к месяцу", variable=period_var, value="month_to_month").pack(anchor="w", padx=20)
tk.Radiobutton(root, text="Месяц к месяцу и год к году", variable=period_var, value="month_year_compare").pack(anchor="w", padx=20)

# Кнопка запуска
tk.Button(root, text="Запустить выгрузку", command=run_query, bg="lightgreen").pack(pady=20)

root.mainloop()
