from rest_framework import serializers
from .models import Allowance

class AllowanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = "__all__"
