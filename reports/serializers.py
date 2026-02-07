from rest_framework import serializers
from .models import DailyReport
from stores.models import Store


class DailyReportSerializer(serializers.ModelSerializer):
    merchandiser_name = serializers.CharField(
        source="merchandiser.username", read_only=True
    )
    stores_visited = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Store.objects.all()
    )

    class Meta:
        model = DailyReport
        fields = [
            "id",
            "date",
            "merchandiser",
            "merchandiser_name",
            "stores_visited",
            "remarks",
            "submitted_at",
        ]
        read_only_fields = ["merchandiser", "submitted_at"]

    def create(self, validated_data):
        stores = validated_data.pop("stores_visited")
        report = DailyReport.objects.create(**validated_data)
        report.stores_visited.set(stores)
        return report
