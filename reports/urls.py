from rest_framework.routers import DefaultRouter
from .views import DailyReportViewSet

router = DefaultRouter()
router.register(r"daily", DailyReportViewSet, basename="daily_reports")
urlpatterns = router.urls
