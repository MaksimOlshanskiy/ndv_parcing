import pandas as pd
import os
import datetime


def save_flats_to_excel_old_new(flats, project, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "old_new_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{project}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_old_new_all(flats, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "old_new_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_middle(flats, project, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "middle_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{project}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_middle_all(flats, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "middle_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_far(flats, project, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "far_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{project}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_far_all(flats, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "far_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_near(flats, project, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "near_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{project}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")

def save_flats_to_excel_near_all(flats, developer):
    df = pd.DataFrame(flats, columns=['Дата обновления',
                                      'Название проекта',
                                      'на англ',
                                      'промзона',
                                      'Местоположение',
                                      'Метро',
                                      'Расстояние до метро, км',
                                      'Время до метро, мин',
                                      'МЦК/МЦД/БКЛ',
                                      'Расстояние до МЦК/МЦД, км',
                                      'Время до МЦК/МЦД, мин',
                                      'БКЛ',
                                      'Расстояние до БКЛ, км',
                                      'Время до БКЛ, мин',
                                      'статус',
                                      'старт',
                                      'Комментарий',
                                      'Девелопер',
                                      'Округ',
                                      'Район',
                                      'Адрес',
                                      'Эскроу',
                                      'Корпус',
                                      'Конструктив',
                                      'Класс',
                                      'Срок сдачи',
                                      'Старый срок сдачи',
                                      'Стадия строительной готовности',
                                      'Договор',
                                      'Тип помещения',
                                      'Отделка',
                                      'Кол-во комнат',
                                      'Площадь, кв.м',
                                      'Цена кв.м, руб.',
                                      'Цена лота, руб.',
                                      'Скидка,%',
                                      'Цена кв.м со ск, руб.',
                                      'Цена лота со ск, руб.',
                                      'секция',
                                      'этаж',
                                      'номер'])

    current_date = datetime.date.today()
    project_root = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.join(project_root, "Date_files", "near_Moscow")
    folder_path = os.path.join(base_path, str(current_date))
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    filename = f"{developer}_{current_date}.xlsx"
    file_path = os.path.join(folder_path, filename)
    df.to_excel(file_path, index=False)
    print(f"Данные сохранены в файл: {file_path}")