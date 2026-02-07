from rest_framework import viewsets
from accounts.permissions import IsAdmin
from .models import Target
from .serializers import TargetSerializer

class TargetViewSet(viewsets.ModelViewSet):
    queryset = Target.objects.all().order_by("-period_anchor", "-id")
    serializer_class = TargetSerializer
    permission_classes = [IsAdmin]
