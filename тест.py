import pandas as pd

df1 = pd.read_excel(r'C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-06-11\НашДомРФ_Москва_2026-06-11.xlsx')
df2 = pd.read_excel(r'C:\PycharmProjects\ndv_parcing\НашДомРФ\Хар-ки_18062026.xlsx')

df_merged = df1.merge(df2, on='id', how='left')
df_merged.to_excel(r'C:\PycharmProjects\ndv_parcing\НашДомРФ\2026-06-11\RNS_2026-06-18.xlsx')