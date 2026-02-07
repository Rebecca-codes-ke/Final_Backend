# from django.contrib import admin
# from .models import Sale


# @admin.register(Sale)
# class SaleAdmin(admin.ModelAdmin):
#     list_display = ("id", "date", "store", "merchandiser", "total_amount")
#     list_filter = ("date",)
#     search_fields = ("store__name", "merchandiser__username")
#     date_hierarchy = "date"
#     ordering = ("-date", "-id")

from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    # Show only fields that definitely exist in most Sale models
    list_display = ("id", "store", "product", "quantity", "total_amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("store__name", "product__name")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
