from django.utils import timezone
from rest_framework import serializers
from uuid import uuid4
from .models import FlashSaleItem

class FlashSalesSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    class Meta:
        model = FlashSaleItem
        fields = [
            "product",
            "flash_price",
            "allocate_stock",
            "start_date",
            "end_date_time ",
            "status",
        ]
        read_only_fields = ["status"]
        extra_kwargs = {
            "product": {"required": True},
            "flash_price": {"required": True, "min_value": 0},
            "allocate_stock": {"required": True, "min_value": 0},
            "start_date": {"required": True},
            "end_date_time ": {"required": True},
        }

    def validate(self, validated_data):
        start_date_time = validated_data.get("start_date")
        end_date_time = validated_data.get("end_date_time ")
        if start_date_time and start_date_time < timezone.now():
            raise serializers.ValidationError(
                {"start_date": "Sales date not be before today date"}
            )

        if start_date_time and start_date_time >= end_date_time:
            raise serializers.ValidationError(
                {"end_date_time ": "Start date must be before End date"}
            )

        return validated_data
