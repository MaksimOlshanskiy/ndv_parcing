import os

def extract_regions(folder_path):
    regions = []

    # Перебираем все файлы в папке
    for filename in os.listdir(folder_path):
        if "_" not in filename:
            continue  # пропускаем странные файлы

        # Убираем расширение
        name_without_ext = os.path.splitext(filename)[0]

        # Разделяем на части
        parts = name_without_ext.split("_")

        if len(parts) < 3:
            continue  # если формат неожиданный — пропускаем

        # Регион всегда между вторым и третьим _
        region = parts[1]
        regions.append(region)

    return regions


folder = r"C:\Users\m.olshanskiy\PycharmProjects\ndv_parsing\Cian\Вторичка продажа"

for i in extract_regions(folder):
    print(i)
