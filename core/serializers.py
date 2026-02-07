from rest_framework import serializers

from sales.models import Sale
from reports.models import DailyReport


class SaleSerializer(serializers.ModelSerializer):
    merchandiser_name = serializers.CharField(source="merchandiser.username", read_only=True)

    class Meta:
        model = Sale
        fields = [
            "id",
            "merchandiser",          # read-only (set automatically)
            "merchandiser_name",     # read-only
            "store_name",
            "amount",
            "payment_status",
            "delivery_notes",
            "created_at",
        ]
        read_only_fields = ["id", "merchandiser", "merchandiser_name", "created_at"]


class DailyReportSerializer(serializers.ModelSerializer):
    merchandiser_name = serializers.CharField(source="merchandiser.username", read_only=True)

    class Meta:
        model = DailyReport
        fields = [
            "id",
            "merchandiser",          # read-only (set automatically)
            "merchandiser_name",     # read-only
            "date",
            "stores_visited",
            "contacts",
            "remarks",
            "created_at",
        ]
        read_only_fields = ["id", "merchandiser", "merchandiser_name", "created_at"]
