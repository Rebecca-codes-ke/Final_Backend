from django.contrib import admin
from .models import Target


@admin.register(Target)
class TargetAdmin(admin.ModelAdmin):
    list_display = ("id", "merchandiser", "period_type", "amount", "period_anchor")
    list_filter = ("period_type",)
    search_fields = ("merchandiser__username",)
    ordering = ("-period_anchor", "-id")

