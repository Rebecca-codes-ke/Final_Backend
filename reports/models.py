
from django.db import models
from django.conf import settings
from stores.models import Store  

class DailyReport(models.Model):
    date = models.DateField()
    merchandiser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_reports"
    )

    stores_visited = models.ManyToManyField(
        Store,
        blank=True,
        related_name="daily_reports"
    )

    remarks = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.merchandiser}"
