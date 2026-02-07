from rest_framework import viewsets
from .models import DailyReport
from .serializers import DailyReportSerializer

class DailyReportViewSet(viewsets.ModelViewSet):
    queryset = DailyReport.objects.all().order_by("-date", "-id")
    serializer_class = DailyReportSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return super().get_queryset()
        return super().get_queryset().filter(merchandiser=user)

    def perform_create(self, serializer):
        user = self.request.user
        # Merchandiser submits for themselves
        if user.role != "ADMIN":
            serializer.save(merchandiser=user)
        else:
            serializer.save()

