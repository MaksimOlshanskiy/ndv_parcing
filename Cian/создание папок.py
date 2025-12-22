import os
from datetime import datetime


def create_dated_folders(base_path, folder_names):
    """
    Создает папки с текущей датой в названии
    """
    current_date = datetime.now().strftime("%Y-%m-%d")

    for folder_name in folder_names:
        dated_folder_name = f"{current_date}_{folder_name}"
        folder_path = os.path.join(base_path, dated_folder_name)

        try:
            os.makedirs(folder_path, exist_ok=True)
            print(f"Папка создана: {folder_path}")
        except Exception as e:
            print(f"Ошибка при создании папки {dated_folder_name}: {e}")


# Пример использования
base_dir = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Cian\Вторичка"
folders = ["Москва", "Санкт-Петербург", "Новосибирск", "Казань", "Красноярск", "Нижний Новгород", "Челябинск", "Уфа", "Краснодар", "Самара", "Ростов-на-Дону", "Омск", "Воронеж", "Пермь", "Волгоград", "Екатеринбург"]

create_dated_folders(base_dir, folders)