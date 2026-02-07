
# from rest_framework import viewsets, permissions
# from .models import Sale
# from .serializers import SaleSerializer

# class SaleViewSet(viewsets.ModelViewSet):
#     serializer_class = SaleSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         qs = Sale.objects.all().order_by("-created_at", "-id")

#         # Admin sees all
#         if user.is_staff or user.is_superuser or getattr(user, "role", "") == "admin":
#             return qs

#         # Merchandiser sees only theirs
#         return qs.filter(merchandiser=user)

#     def perform_create(self, serializer):
#         serializer.save(merchandiser=self.request.user)

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Sale.objects.select_related("store", "product", "merchandiser").order_by("-created_at")

        # ✅ Admin sees all, merchandiser sees their own
        if getattr(user, "role", "") == "admin":
            return qs
        return qs.filter(merchandiser=user)

    def perform_create(self, serializer):
        # ✅ Force ownership to logged-in user
        serializer.save(merchandiser=self.request.user)
