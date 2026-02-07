from rest_framework.routers import DefaultRouter
from .views import AllowanceViewSet

router = DefaultRouter()
router.register(r"allowance", AllowanceViewSet, basename="allowance")
urlpatterns = router.urls
