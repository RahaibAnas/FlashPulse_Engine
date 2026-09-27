from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializer
from flash_sales.models import FlashSaleItem
from config.redis_cache import r
from flash_sales.services import cache_flash_item

# Create your views here.
@api_view(["GET"])
def home(request):
    return Response(
        {
            "succcess": True,
            "message": "Orders apps Works",
        },
        status=status.HTTP_200_OK,
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    data = request.data
    serializer = OrderSerializer(data=data)

    if not serializer.is_valid():
        return Response({
            "message":False,
            "error":serializer.errors,

        },status=status.HTTP_400_BAD_REQUEST)

    flash_item_id = data.get("flash_sale_item")
    item_key = f"FlashSaleItem:{flash_item_id}"

    if not r.hexists(item_key,"flash_price"):
        cache_flash_item(id=flash_item_id) 

    redis_cache_item = r.hgetall(item_key)

    if redis_cache_item:
        if r.ttl(name=item_key) < 15:
            r.expire(name=item_key,time=60)

        if (
            redis_cache_item.get("status") == FlashSaleItem.SaleStatus.SCHEDULED
            or redis_cache_item.get("status") == FlashSaleItem.SaleStatus.ENDED
            or redis_cache_item.get("status") == FlashSaleItem.SaleStatus.SOLD_OUT
        ):
            return Response({
                "success":False,
                "message":"The Order is not Procced",
                "product_status": redis_cache_item.get('status'),
            },status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        r.hincrby(item_key,'reserved_stock',serializer.validated_data.get('quantity'))
        if r.hget(item_key,"reserved_stock")==0:
            r.hset(item_key, "reserved_stock",FlashSaleItem.SaleStatus.SOLD_OUT)

        return Response({
            "success":True,
            "message":"the order is proceed successfully.you have five minutes to pay this",
            "data":serializer.data
        })
