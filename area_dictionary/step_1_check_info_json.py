import os
import json
import shutil
import pandas as pd
import pyxlsb

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Относительные пути
path = os.path.join('projects')
failed_dir = os.path.join('failed')
os.makedirs(failed_dir, exist_ok=True)

# Результаты
all_dicts = {}
failed_files = []  # (имя файла, причина)
failed_paths = []

# Возможные названия листов
tried_sheets = [
    'типология', 'тип.', 'Типология', 'комнатность',
    'типология ', 'типология новая', 'типология_абс', 'типология_новая', 'тип','типология_Бег2'
]

def process_excel_file(file_path):
    file_name = os.path.basename(file_path)
    file_dict_key = os.path.splitext(file_name)[0]

    for i, sheet in enumerate(tried_sheets):
        try:
            df = pd.read_excel(file_path, sheet_name=sheet, usecols="A:B", header=None)
            df = df.dropna(how='all')
            df = df.dropna(subset=[df.columns[0], df.columns[1]])

            if not df.empty:
                keys = df.iloc[:, 0].astype(str).str.strip()
                values = df.iloc[:, 1]
                file_dict = dict(zip(keys, values))
                all_dicts[file_dict_key] = file_dict
                print(f'✅ Успешно считан: {file_name} (лист "{sheet}")')
            break

        except ValueError:
            if i == len(tried_sheets) - 1:
                try:
                    sheets = pd.ExcelFile(file_path).sheet_names
                    msg = f'Листы не найдены. Доступные: {", ".join(sheets)}'
                    print(f'❌ {file_name}: {msg}')
                    failed_files.append((file_name, msg))
                    failed_paths.append(file_path)
                except Exception as ex:
                    msg = f'Ошибка при чтении листов: {ex}'
                    print(f'⚠️ {file_name}: {msg}')
                    failed_files.append((file_name, msg))
                    failed_paths.append(file_path)

        except Exception as e:
            msg = f'Ошибка при обработке листа "{sheet}": {e}'
            print(f'⚠️ {file_name}: {msg}')
            failed_files.append((file_name, msg))
            failed_paths.append(file_path)
            break

# Поиск и обработка Excel-файлов
if os.path.isdir(path):
    for fname in os.listdir(path):
        if fname.lower().endswith(('.xlsx', '.xlsb')):
            fpath = os.path.join(path, fname)
            if os.path.isfile(fpath):
                process_excel_file(fpath)
else:
    print(f'❌ Указанный путь не существует: {path}')

# Сохраняем результат
output_path = 'typology.json'
if all_dicts:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_dicts, f, ensure_ascii=False, indent=4)
    print(f'\n✅ Все словари сохранены в "{output_path}"')
else:
    print('\n⚠️ Нет данных для сохранения.')

# Перемещаем неудачные файлы
for fpath in failed_paths:
    try:
        shutil.move(fpath, os.path.join(failed_dir, os.path.basename(fpath)))
        print(f'📦 Перемещён: {os.path.basename(fpath)} → {failed_dir}')
    except Exception as e:
        print(f'⚠️ Не удалось переместить файл {fpath}: {e}')

# Итоговый отчёт
if failed_files:
    print('\n⚠️ Не удалось обработать следующие файлы:')
    for fname, reason in failed_files:
        print(f'❌ {fname}: {reason}')
