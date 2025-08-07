# Параметры для расчета
initial_assets = 67600
bond_price = 1120
monthly_coupon_per_bond = 20

# Рассчитаем сколько облигаций можно купить на старте
initial_bonds = initial_assets // bond_price
cash = initial_assets % bond_price  # остаток после покупки

# Общий срок — 12 месяцев
months = 12
current_bonds = initial_bonds

# Лог для отслеживания
reinvest_log = []

for month in range(months):
    # Купонный доход
    coupon_income = current_bonds * monthly_coupon_per_bond
    cash += coupon_income

    # Покупка новых облигаций
    new_bonds = floor(cash / bond_price)
    cash -= new_bonds * bond_price
    current_bonds += new_bonds

    reinvest_log.append({
        'Month': month + 1,
        'Total Bonds': current_bonds,
        'Coupon Income': coupon_income,
        'New Bonds Bought': new_bonds,
        'Remaining Cash': round(cash, 2)
    })

# Финальная стоимость портфеля
final_assets = current_bonds * bond_price + cash
total_profit = final_assets - initial_assets
effective_yield = (total_profit / initial_assets) * 100

current_bonds, final_assets, total_profit, effective_yield