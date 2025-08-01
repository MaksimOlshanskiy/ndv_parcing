from Developer_dict import name_dict, developer_dict
import pandas as pd
import os
import pyxlsb

file_path = r"C:\Users\m.olshanskiy\Desktop\База Июль\Июль.xlsx"
df = pd.read_excel(file_path, sheet_name='Sheet1')

def strip_trailing_spaces(df):
    for col in ['Название проекта', 'Девелопер']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.rstrip()
    return df


# Замена значений в столбце "Название проекта "
# df['Дата обновления'] = pd.to_datetime(df['Дата обновления'], dayfirst=True, errors='coerce')
df["Название проекта"] = df["Название проекта"].replace(name_dict)
df["Девелопер"] = df["Девелопер"].replace(developer_dict)
df = strip_trailing_spaces(df)



folder_path = os.path.dirname(file_path)
file_name = os.path.basename(file_path)
file_name = os.path.splitext(file_name)[0]
# Сохраняем объединённые данные в новый Excel файл
output_file_name = f'{file_name}_changed.xlsx'
output_file_path = os.path.join(folder_path, output_file_name)
output_file = f'{folder_path}\\{output_file_name}'
df.to_excel(output_file, index=False)

print(f"Все данные сохранены в {output_file}")
