from copy import deepcopy


def apply_scenario(records: list[dict], changes: dict) -> list[dict]:
    adjusted = deepcopy(records)
    for index, row in enumerate(adjusted):
        row["revenue"] = float(row["revenue"]) * (1 + changes.get("sales_change_percent", 0) / 100)
        row["fuel_logistics_cost"] = float(row["fuel_logistics_cost"]) * (
            1 + changes.get("fuel_price_increase_percent", 0) / 100
        )
        fuel_delta = float(row["fuel_logistics_cost"]) - float(records[index]["fuel_logistics_cost"])
        row["operating_expenses"] = (
            float(row["operating_expenses"]) * (1 + changes.get("operating_expenses_change_percent", 0) / 100)
            + fuel_delta
        )
        row["inventory_value"] = float(row["inventory_value"]) * (
            1 + changes.get("inventory_level_change_percent", 0) / 100
        )
        if changes.get("new_loan_amount", 0):
            row["debt_payment"] = float(row["debt_payment"]) + changes["new_loan_amount"] * 0.03
    return adjusted
