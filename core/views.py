from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from sales.models import Sale
from reports.models import DailyReport

from .serializers import SaleSerializer, DailyReportSerializer
from .permissions import IsAdminUserRole


# -------------------------
# GET/POST /api/me/sales/
# -------------------------
class MeSalesListCreateView(generics.ListCreateAPIView):
    serializer_class = SaleSerializer

    def get_queryset(self):
        return Sale.objects.filter(merchandiser=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(merchandiser=self.request.user)


# -----------------------------------
# GET/POST /api/me/daily-reports/
# -----------------------------------
class MeDailyReportListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyReportSerializer

    def get_queryset(self):
        return DailyReport.objects.filter(merchandiser=self.request.user).order_by("-date", "-created_at")

    def perform_create(self, serializer):
        serializer.save(merchandiser=self.request.user)


# -------------------------------
# GET /api/admin/analytics/?period=daily|weekly|monthly
# ROI = sales_total / allowance_cost
# -------------------------------
class AdminAnalyticsView(APIView):
    permission_classes = [IsAdminUserRole]

    def get(self, request):
        period = request.query_params.get("period", "daily").lower()
        now = timezone.now()

        # Define time window + allowance cost (your business rules)
        if period == "daily":
            start = now - timedelta(days=1)
            allowance_cost = 500
        elif period == "weekly":
            start = now - timedelta(days=7)
            allowance_cost = 2500
        elif period == "monthly":
            start = now - timedelta(days=30)
            allowance_cost = 10000
        else:
            return Response({"detail": "Invalid period. Use daily, weekly, or monthly."}, status=400)

        User = get_user_model()

        # Treat non-staff as merchandisers (until you add a role field)
        merchandisers = User.objects.filter(is_staff=False, is_superuser=False)

        results = []
        for u in merchandisers:
            total_sales = (
                Sale.objects.filter(merchandiser=u, created_at__gte=start)
                .aggregate(total=Sum("amount"))
                .get("total")
                or 0
            )

            total_sales = float(total_sales)
            roi = (total_sales / allowance_cost) if allowance_cost else 0

            results.append(
                {
                    "name": u.username,
                    "sales_total": total_sales,
                    "allowance_cost": allowance_cost,
                    "roi": round(roi, 4),
                }
            )

        results.sort(key=lambda x: x["sales_total"], reverse=True)

        return Response({"period": period, "results": results})
