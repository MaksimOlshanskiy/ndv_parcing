import os
import glob
import pandas as pd

# Путь к папке, где находятся Excel файлы
folder_path = 'C:\\Users\\m.olshanskiy\\Desktop\\01.04'

# Создаём пустой DataFrame для накопления данных
all_data = pd.DataFrame()

# Используем glob для поиска всех Excel файлов в папке
excel_files = glob.glob(os.path.join(folder_path, "*.xlsx"))

# Проходим по каждому файлу и добавляем его данные в DataFrame
for file_path in excel_files:
    df = pd.read_excel(file_path)  # Читаем Excel файл в DataFrame
    all_data = pd.concat([all_data, df], ignore_index=True)  # Добавляем данные в общий DataFrame


def clean_project_name(df, column_name):
    """
    Очищает названия проектов в указанной колонке DataFrame.
    Убирает 'ЖК ' в начале и кавычки вокруг названия.

    :param df: DataFrame pandas
    :param column_name: str, название столбца с проектами
    :return: DataFrame с изменённой колонкой
    """
    def clean_name(name):
        name = name.replace('ЖК ', '')  # Убираем 'ЖК '
        name = name.strip('«»"')  # Убираем кавычки «», ""
        return name

    df[column_name] = df[column_name].apply(clean_name)
    return df



# all_data = all_data.drop_duplicates()       # убираем полные дубликаты

# Проверяем результат
print(all_data)
print(f'Число строк в датафрейме {len(all_data)}')

all_data = clean_project_name(all_data, 'Название проекта')

# Сохраняем объединённые данные в новый Excel файл
output_file_name = 'Combined_data.xlsx'
output_file = f'{folder_path}\\{output_file_name}'

all_data.to_excel(output_file, index=False)

print(f"Все данные сохранены в {output_file}")