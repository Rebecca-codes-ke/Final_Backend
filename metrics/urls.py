from django.urls import path
from .views import WeeklySummaryView, MonthlySummaryView
from .views_admin_dashboard import AdminDashboardSummary

urlpatterns = [
    path("weekly/", WeeklySummaryView.as_view()),
    path("monthly/", MonthlySummaryView.as_view()),
    path("admin/dashboard/", AdminDashboardSummary.as_view(), name="admin-dashboard"),
]
