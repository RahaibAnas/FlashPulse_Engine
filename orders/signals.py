from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.db.models import F
from django.utils import timezone

from .models import Order
from flash_sales.models import FlashSaleItem

@receiver(pre_save,sender=Order)
def update_total_amount(sender,instance,**kwargs):
    quantity = instance.quantity
    flash_price = instance.flash_sale_item.flash_price
    if quantity:
        instance.total_amount = quantity*flash_price


# @receiver(pre_save, sender=Order)
# def track_previous_status(sender, instance, **kwargs):
#     if not instance.id:
#         instance._previous_status = None
#         return 
#     try:
#         order = Order.objects.get(pk=instance.id)
#         instance._previous_status = order.status
#     except Order.DoesNotExist:
#         instance._previous_status = None


# @receiver(post_save,sender=Order)
# def update_flashSaleItem_quantity(sender,instance,created,**kwargs):
#     id = instance.flash_sale_item.id
#     quantity = instance.quantity
#     previous_status = instance._previous_status
#     if created:
#         if instance.status == Order.OrderStatus.PENDING_PAYMENT and previous_status is None:
#             FlashSaleItem.objects.filter(id=id).update(reserved_stock=F("reserved_stock")+quantity)

#     if previous_status == Order.OrderStatus.PENDING_PAYMENT and instance.status == Order.OrderStatus.PAID:
#         FlashSaleItem.objects.filter(id=id).update(
#             sold_stock=F("sold_stock") + quantity,
#             reserved_stock=F("reserved_stock") - quantity,
#         )

#     elif previous_status == Order.OrderStatus.PENDING_PAYMENT and (instance.status == Order.OrderStatus.EXPIRED or Order.OrderStatus.CANCELLED):
#         FlashSaleItem.objects.filter(id=id).update(reserved_stock=F("reserved_stock")-quantity)
