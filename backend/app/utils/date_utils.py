from datetime import date


def month_label(value: date) -> str:
    return value.strftime("%B %Y")
