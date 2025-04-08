import pandas as pd

# Путь к папке, где находятся Excel файлы
folder_path = 'C:\\Users\\m.olshanskiy\\PycharmProjects\\ndv_parsing\\Cian\\2025-04-07'

df = pd.read_excel(file_path)  # Читаем Excel файл в DataFrame

all_data = all_data.drop_duplicates()       # убираем полные дубликаты

# Проверяем результат
print(all_data)
print(f'Число строк в датафрейме {len(all_data)}')

# Сохраняем объединённые данные в новый Excel файл
output_file = 'C:\\Users\\m.olshanskiy\\PycharmProjects\\ndv_parsing\\Cian\\2025-03-28\\Combined_data.xlsx'

all_data.to_excel(output_file, index=False)

print(f"Все данные сохранены в {output_file}")