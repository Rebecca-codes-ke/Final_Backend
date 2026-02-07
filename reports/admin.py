from django.contrib import admin
from .models import DailyReport
from .models import Store


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ("id", "date", "merchandiser", "submitted_at")
    list_filter = ("date", "merchandiser")
    search_fields = (
        "merchandiser__username",
        "merchandiser__first_name",
        "merchandiser__last_name",
        "remarks",
    )
    ordering = ("-date", "-id")
    date_hierarchy = "date"


    autocomplete_fields = ("merchandiser", "stores_visited")


