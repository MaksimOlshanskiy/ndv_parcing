import numpy as np
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# --- Входные данные ---
target = 1_500_000  # цель накоплений (руб.)
initial = 61_711  # стартовый капитал (руб.)
annual_rate = 0.14  # 14% годовых
years = 9  # срок накоплений в годах
months = years * 12  # срок в месяцах

# --- Расчёт месячной доходности ---
monthly_rate = (1 + annual_rate) ** (1 / 12) - 1

# --- Рассчёт будущей стоимости стартового капитала ---
future_initial = initial * (1 + monthly_rate) ** months

# --- Сколько нужно накопить за счет ежемесячных взносов ---
needed_from_contributions = target - future_initial

# --- Ежемесячный взнос ---
monthly_contribution = 6000

print(f"Необходимо ежемесячно откладывать: {monthly_contribution:,.2f} руб.")

# --- Построение таблицы накоплений ---
balance = []
amount = initial
start_date = datetime(2025, 8, 1)  # Август 2025 как старт

for m in range(1, months + 1):
    # начисляем проценты
    interest = amount * monthly_rate
    amount += interest

    # пополняем
    contribution = monthly_contribution
    amount += contribution

    # дата
    current_date = start_date + relativedelta(months=m - 1)

    balance.append((
        m,
        current_date.month,
        current_date.year,
        round(amount, 2),
        round(contribution, 2),
        round(interest, 2),
        f"{annual_rate * 100:.2f}%"
    ))

df = pd.DataFrame(
    balance,
    columns=["Номер месяца", "Месяц", "Год", "Сумма на счёте", "Пополнение", "Проценты", "Ставка"]
)

# --- Итоговая строка ---
total_contributions = df["Пополнение"].sum()
total_interest = df["Проценты"].sum()
final_amount = df["Сумма на счёте"].iloc[-1]

summary_row = pd.DataFrame([[
    "ИТОГО",
    "",
    "",
    round(final_amount, 2),
    round(total_contributions, 2),
    round(total_interest, 2),
    f"{annual_rate * 100:.2f}%"
]], columns=df.columns)

df = pd.concat([df, summary_row], ignore_index=True)

# --- Сохраняем в Excel ---
df.to_excel("накопления.xlsx", index=False)

print("Таблица сохранена в файл 'накопления.xlsx'")
