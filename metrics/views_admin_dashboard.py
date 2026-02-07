from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRebeccaOnly


# ✅ Adjust these imports to your actual model locations
from sales.models import Sale
from reports.models import DailyReport


def week_start_end(dt=None):
    """Monday -> next Monday (exclusive)."""
    dt = dt or timezone.localdate()
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=7)
    return start, end


class AdminDashboardSummary(APIView):
    permission_classes = [IsRebeccaOnly]  # lock further later

    def get(self, request):
        start, end = week_start_end()

        sales_qs = Sale.objects.all()

        # ✅ Total sales (fallback safely if your model differs)
        total_sales = 0.0
        for s in sales_qs:
            amt = getattr(s, "total_amount", None)
            if amt is None:
                qty = getattr(s, "quantity", 0) or 0
                unit = getattr(s, "unit_price", 0) or 0
                amt = qty * unit
            total_sales += float(amt or 0)

        # ✅ Paid/Pending (only if the field exists)
        paid_orders = 0
        pending_orders = 0
        if hasattr(Sale, "payment_status"):
            paid_orders = sales_qs.filter(payment_status="paid").count()
            pending_orders = sales_qs.filter(payment_status="pending").count()

        # ✅ Weekly visits
        week_reports = DailyReport.objects.filter(date__gte=start, date__lt=end)

        visited_map = {}  # {user_id: set(store_ids)}
        for r in week_reports:
            uid = getattr(r, "merchandiser_id", None) or getattr(r, "user_id", None)
            sid = getattr(r, "store_id", None)
            if not uid or not sid:
                continue
            visited_map.setdefault(uid, set()).add(sid)

        # ✅ Weekly conversions (simple rule: sale exists for that merchandiser+store in the week)
        converted_map = {}
        if hasattr(Sale, "merchandiser_id") and hasattr(Sale, "store_id") and hasattr(Sale, "date"):
            week_sales = Sale.objects.filter(date__gte=start, date__lt=end)
            for s in week_sales:
                uid = getattr(s, "merchandiser_id", None)
                sid = getattr(s, "store_id", None)
                if not uid or not sid:
                    continue
                converted_map.setdefault(uid, set()).add(sid)

        # ✅ Top merchandiser = highest weekly sales total
        top_user_id = None
        top_name = "-"
        top_total = -1.0

        if hasattr(Sale, "merchandiser_id") and hasattr(Sale, "date"):
            week_sales = Sale.objects.filter(date__gte=start, date__lt=end).select_related("merchandiser")
            totals = {}

            for s in week_sales:
                uid = s.merchandiser_id
                amt = getattr(s, "total_amount", None)
                if amt is None:
                    qty = getattr(s, "quantity", 0) or 0
                    unit = getattr(s, "unit_price", 0) or 0
                    amt = qty * unit
                totals[uid] = totals.get(uid, 0.0) + float(amt or 0)

            if totals:
                top_user_id = max(totals, key=totals.get)
                top_total = totals[top_user_id]

                one = week_sales.filter(merchandiser_id=top_user_id).first()
                if one and getattr(one, "merchandiser", None):
                    top_name = one.merchandiser.username

        return Response({
            "week_start": str(start),
            "week_end": str(end),
            "total_sales": total_sales,
            "paid_orders": paid_orders,
            "pending_orders": pending_orders,
            "top_merchandiser": {
                "id": top_user_id,
                "name": top_name,
                "stores_visited": len(visited_map.get(top_user_id, set())) if top_user_id else 0,
                "stores_converted": len(converted_map.get(top_user_id, set())) if top_user_id else 0,
            }
        })


# from rest_framework.views import APIView
# from rest_framework.response import Response

# from .permissions import IsRebeccaOnly

# class AdminDashboardSummary(APIView):
#     permission_classes = [IsRebeccaOnly]

#     def get(self, request):
#         return Response({
#             "total_sales": 127500,
#             "paid_orders": 8,
#             "pending_orders": 5,
#             "top_merchandiser": {
#                 "name": "Joy",
#                 "stores_visited": 42,
#                 "stores_converted": 6
#             }
#         })
