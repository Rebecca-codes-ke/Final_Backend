from rest_framework import viewsets
from accounts.permissions import IsAdmin
from .models import Allowance
from .serializers import AllowanceSerializer

class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = Allowance.objects.all().order_by("-date", "-id")
    serializer_class = AllowanceSerializer
    permission_classes = [IsAdmin]
