from django.utils import timezone
from rest_framework import serializers

from .models import FlashSale

class FlashSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlashSale
        fields = ['product','flash_price','allocate_stock','start_date','end_date','status']
        read_only_fields = ['status']
        extra_kwargs = {
            'product':{'required':True},
            'flash_price':{'required':True,'min_value':0},
            'allocate_stock':{'required':True,'min_value':0},
            'start_date':{'required':True},
            'end_date':{'required':True},
        }

    def validate(self, validated_data):
        start_date = validated_data.get('start_date')
        end_date = validated_data.get('end_date')
        if start_date and start_date < timezone.now():
            raise serializers.ValidationError({"start_date":"Sales date not be before today date"})

        if start_date and start_date >= end_date:
            raise serializers.ValidationError({"end_date":"Start date must be before End date"})

        return validated_data