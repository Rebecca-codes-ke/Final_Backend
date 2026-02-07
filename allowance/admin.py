from django.contrib import admin
from .models import Allowance


@admin.register(Allowance)
class AllowanceAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "merchandiser", "amount")
    list_filter = ("date",)
    search_fields = ("merchandiser__username",)
    date_hierarchy = "date"
    ordering = ("-date", "-id")

