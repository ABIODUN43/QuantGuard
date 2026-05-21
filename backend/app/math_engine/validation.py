REQUIRED_COLUMNS = {
    "date",
    "revenue",
    "operating_expenses",
    "cost_of_goods_sold",
    "inventory_value",
    "debt_payment",
    "cash_balance",
    "fuel_logistics_cost",
}


def missing_columns(columns: set[str]) -> set[str]:
    return REQUIRED_COLUMNS - columns
