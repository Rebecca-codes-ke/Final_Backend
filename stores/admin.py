from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    search_fields = ("name",)  # change "name" to your Store field
