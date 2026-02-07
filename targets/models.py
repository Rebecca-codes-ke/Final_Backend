from django.db import models
from django.conf import settings

class Target(models.Model):
    class Period(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        MONTHLY = "MONTHLY", "Monthly"

    merchandiser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="targets")
    period_type = models.CharField(max_length=10, choices=Period.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    # store a date within the week/month (we derive range in analytics)
    period_anchor = models.DateField()

    class Meta:
        unique_together = ("merchandiser", "period_type", "period_anchor")

