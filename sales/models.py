# from django.db import models
# from django.conf import settings
# from stores.models import Store
# from products.models import Product

# class Sale(models.Model):
#     date = models.DateField()
#     merchandiser = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="sales"
#     )
#     store = models.ForeignKey(Store, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     total_amount = models.DecimalField(max_digits=12, decimal_places=2)

#     created_at = models.DateTimeField(auto_now_add=True)

# def validate(self, attrs):
#     qty = attrs.get("quantity", 0)
#     price = attrs.get("price", 0)
#     attrs["total"] = qty * price
#     return attrs

from django.db import models
from django.conf import settings
from django.utils import timezone

class Sale(models.Model):
    store = models.ForeignKey("stores.Store", on_delete=models.PROTECT, related_name="sales")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT, related_name="sales")

    # ✅ Add this (your code expects it)
    merchandiser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales"
    )

    # ✅ Add this if you want a Date column in your table
    date = models.DateField(default=timezone.localdate)

    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # ✅ Add this so paid/pending works
    PAYMENT_CHOICES = (
        ("pending", "Pending"),
        ("paid", "Paid"),
    )
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale #{self.id}"
