# from rest_framework.routers import DefaultRouter
# from .views import SaleViewSet

# router = DefaultRouter()
# router.register(r"sales", SaleViewSet, basename="sales")
# urlpatterns = router.urls

# from rest_framework import viewsets, permissions
# from .models import Sale
# from .serializers import SaleSerializer

# class SaleViewSet(viewsets.ModelViewSet):
#     queryset = Sale.objects.all().order_by("-id")
#     serializer_class = SaleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)  # or created_by=self.request.user


from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet

router = DefaultRouter()
router.register(r"sales", SaleViewSet, basename="sales")

urlpatterns = [
    path("", include(router.urls)),
]
