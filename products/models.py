from django.db import models

class Product(models.Model):
    class Category(models.TextChoices):
        VAPE_1500 = "VAPE_1500", "Vape 1500 Puffs"
        VAPE_3500 = "VAPE_3500", "Vape 3500 Puffs"
        NIC_POUCH = "NIC_POUCH", "Nicotine Pouch"

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=Category.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
