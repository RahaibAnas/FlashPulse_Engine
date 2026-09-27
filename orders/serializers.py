from rest_framework import serializers

from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id','total_amount','status','expires_at','created_at','updated_at','user']
        extra_kwargs = {
            'flash_sale_item':{'required':True},
            'quantity':{'required':True},
            'idempotency_key':{'required':True}
        }
    def validate(self,validated_data):
        quantity = validated_data.get('quantity')
        if quantity and quantity > 5:
            raise serializers.ValidationError({"quantity":"only 5 item are allowed to buy"})

        return validated_data

