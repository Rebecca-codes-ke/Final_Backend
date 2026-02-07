from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MERCH = "MERCH", "Merchandiser"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.MERCH)

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_merch(self):
        return self.role == self.Role.MERCH
