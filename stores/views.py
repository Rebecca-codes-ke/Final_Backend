from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Store
from .serializers import StoreSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all().order_by("-id")
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # Merchandisers can: list, retrieve, create
        if self.action in ["list", "retrieve", "create"]:
            return [IsAuthenticated()]
        # Only admin can: update, partial_update, destroy
        return [IsAuthenticated()]  # keep auth, then block below

    def perform_update(self, serializer):
        user = self.request.user
        if getattr(user, "role", "") != "ADMIN":
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only admin can update stores.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if getattr(user, "role", "") != "ADMIN":
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only admin can delete stores.")
        instance.delete()
