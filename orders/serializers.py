from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id','total_amount','status','expires_at','created_at','updated_at']
        extra_kwargs = {
            'user':{'required':True},
            'flash_sale_item':{'required':True},
            'quantity':{'required':True},
            'idempotency_key':{'required':True}
        }

