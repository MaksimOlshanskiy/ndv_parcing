from Developer_dict import name_dict, developer_dict
import pandas as pd
import pyxlsb

file_path = r"C:\Users\m.olshanskiy\Desktop\2024_старая МСК+НАО_fixed.xlsb"
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

# Сохранение результата в новый файл
df.to_excel("2024_fixed.xlsx", index=False)
