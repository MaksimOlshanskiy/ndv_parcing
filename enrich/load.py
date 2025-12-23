import pandas as pd
import json

def load_excel(excel_path):
    df = pd.read_excel(excel_path, sheet_name='Sheet1')
    df.columns = df.columns.str.strip()
    return df


def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)