from rest_framework import serializers

from .models import Catagory,Product

class CategorySerialiser(serializers.ModelSerializer):
    class Meta:
        model= Catagory
        fields = "__all__"
        read_only_fields = ['id','slug']
        extra_kwargs = {
            "name":{"required":True,'min_length':3},
            
        }

class ProductSerialiser(serializers.ModelSerializer):
    catagory = serializers.StringRelatedField()
    class Meta:
        model= Product 
        fields = "__all__"
        read_only_fields = ['id','slug','created_at','updated_at','is_active']
        extra_kwargs = {
            'name':{"required":True,"min_length":3},
            "category":{"required":True},
            "base_price":{"required":True,"min_value":0},
            "base_stock":{"required":True,"min_value":0},
        }