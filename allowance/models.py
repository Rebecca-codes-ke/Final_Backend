from django.db import models
from django.conf import settings

class Allowance(models.Model):
    date = models.DateField()
    merchandiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="allowances")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=500)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("date", "merchandiser")

