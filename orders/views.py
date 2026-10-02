from django.shortcuts import render, get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from uuid import UUID

from .serializers import OrderSerializer
from flash_sales.models import FlashSaleItem
from .permissions import UserPermission
from config.redis_cache import r
from flash_sales.services import cache_flash_item
from .models import Order

# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):
    data = request.data
    serializer = OrderSerializer(data=data)

    if not serializer.is_valid():
        return Response(
            {
                "message": False,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    flash_item_id = data.get("flash_sale_item")
    item_key = f"FlashSaleItem:{flash_item_id}"

    if not r.hexists(item_key, "flash_price"):
        cache_flash_item(id=flash_item_id)

    redis_cache_item = r.hgetall(item_key)

    if redis_cache_item:
        if r.ttl(name=item_key) < 15:
            r.expire(name=item_key, time=60)

        if (
            redis_cache_item.get("status") == FlashSaleItem.SaleStatus.SCHEDULED
            or redis_cache_item.get("status") == FlashSaleItem.SaleStatus.ENDED
            or redis_cache_item.get("status") == FlashSaleItem.SaleStatus.SOLD_OUT
        ):
            return Response(
                {
                    "success": False,
                    "message": "The Order is not Procced",
                    "product_status": redis_cache_item.get("status"),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(user=request.user)
        r.hincrby(item_key, "reserved_stock", serializer.validated_data.get("quantity"))
        if int(r.hget(item_key, "reserved_stock")) + int(
            r.hget(item_key, "sold_stock")
        ) == int(r.hget(item_key, "allocate_stock")):
            r.hset(item_key, "reserved_stock", FlashSaleItem.SaleStatus.SOLD_OUT)

        return Response(
            {
                "success": True,
                "message": "the order is proceed successfully.you have five minutes to pay this",
                "data": serializer.data,
            }
        )


@api_view(["GET"])
@permission_classes([UserPermission])
def get_order_details(request, pk: str):
    data = get_object_or_404(Order, id=UUID(pk))
    serializer = OrderSerializer(data)
    return Response(
        {
            "success": True,
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([UserPermission])
def get_orders_detail_by_user(request):
    user = request.user
    data = Order.objects.filter(user=user)
    serializer = OrderSerializer(data=data, many=True)
    serializer.is_valid()
    return Response(
        {"success": True, "data": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["PATCH"])
@permission_classes([UserPermission])
def cancel_order(request, pk: str):
    data = get_object_or_404(Order, id=UUID(pk))
    if (
        data.status == Order.OrderStatus.EXPIRED
        or data.status == Order.OrderStatus.CANCELLED
    ):
        return Response(
            {
                "success": False,
                "status": data.status,
                "message": f"Order already {data.status}.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    data.status = Order.OrderStatus.CANCELLED
    data.save(update_fields=["status"])
    item_key = f"FlashSaleItem:{pk}"
    r.hincrby(item_key, "reserved_stock", amount= -data.quantity)
    return Response(
        {"success": True, "message": "Order Cancelled"},
        status=status.HTTP_200_OK,
    )
