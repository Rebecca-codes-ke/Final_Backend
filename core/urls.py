from django.urls import path
from .views import MeSalesListCreateView, MeDailyReportListCreateView, AdminAnalyticsView

urlpatterns = [
    path("me/sales/", MeSalesListCreateView.as_view(), name="me-sales"),
    path("me/daily-reports/", MeDailyReportListCreateView.as_view(), name="me-daily-reports"),
    path("admin/analytics/", AdminAnalyticsView.as_view(), name="admin-analytics"),
]
