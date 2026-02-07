def format_number(num: float) -> str:
    """Форматирование числа с пробелами"""
    return f"{num:,.0f}".replace(",", " ")


def get_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Прогресс-бар"""
    filled = int((current / total) * length)
    bar = "█" * filled + "░" * (length - filled)
    percentage = int((current / total) * 100)
    return f"{bar} {percentage}%"


def calculate_roi(investment: float, monthly_saving: float) -> dict:
    """Расчёт ROI"""
    if monthly_saving == 0:
        return {
            'payback_days': 0,
            'yearly_saving': 0,
            'roi_percent': 0
        }

    payback_days = round((investment / monthly_saving) * 30)
    yearly_saving = monthly_saving * 12
    roi_percent = round(((yearly_saving - investment) / investment) * 100)

    return {
        'payback_days': payback_days,
        'yearly_saving': yearly_saving,
        'roi_percent': roi_percent
    }
