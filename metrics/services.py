from datetime import date, timedelta
from django.db.models import Sum
from sales.models import Sale
from allowance.models import Allowance

def week_range(anchor: date):
    start = anchor - timedelta(days=anchor.weekday())  # Monday
    end = start + timedelta(days=6)
    return start, end

def month_range(anchor: date):
    start = anchor.replace(day=1)
    # naive next month:
    if start.month == 12:
        next_month = start.replace(year=start.year + 1, month=1, day=1)
    else:
        next_month = start.replace(month=start.month + 1, day=1)
    end = next_month - timedelta(days=1)
    return start, end

def roi_summary(merchandiser_id: int, start: date, end: date):
    sales_total = Sale.objects.filter(
        merchandiser_id=merchandiser_id, date__range=(start, end)
    ).aggregate(total=Sum("amount"))["total"] or 0

    cost_total = Allowance.objects.filter(
        merchandiser_id=merchandiser_id, date__range=(start, end)
    ).aggregate(total=Sum("amount"))["total"] or 0

    roi_ratio = (sales_total / cost_total) if cost_total else None
    roi_percent = (((sales_total - cost_total) / cost_total) * 100) if cost_total else None

    return {
        "sales_total": float(sales_total),
        "allowance_total": float(cost_total),
        "roi_ratio": float(roi_ratio) if roi_ratio is not None else None,
        "roi_percent": float(roi_percent) if roi_percent is not None else None,
    }
