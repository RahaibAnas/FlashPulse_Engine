from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone


from uuid import uuid4
from datetime import timedelta

from flash_sales.models import FlashSaleItem

User = get_user_model()


# Create your models here.
class Order(models.Model):

    def get_expire_time():
        return timezone.now() + timedelta(minutes=10)

    class OrderStatus(models.TextChoices):
        PENDING_PAYMENT = "PENDING_PAYMENT", "PENDING_PAYMENT"
        PAID = "PAID", "PAID"
        CANCELLED = "CANCELLED", "CANCELLED"
        EXPIRED = "EXPIRED", "EXPIRED"

    id = models.UUIDField(primary_key=True, editable=True, default=uuid4)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders",
    )
    flash_sale_item = models.ForeignKey(
        FlashSaleItem, on_delete=models.CASCADE, related_name="orders",
    )
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0)],default=0)
    status = models.CharField(
        max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING_PAYMENT
    )
    idempotency_key = models.CharField(max_length=100, unique=True, db_index=True)
    expires_at = models.DateTimeField(default=get_expire_time(),db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints =[models.UniqueConstraint(fields=["user", "flash_sale_item"],condition=~models.Q(status = "EXPIRED") & ~models.Q(status = "CANCELLED"),name="unique_user_flash_sale_item")]



   

    def save(self,*args,**kwargs):
        # self.expires_at = self.__expire_time()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.idempotency_key


class PaymentLog(models.Model):
    class PaymentLogStatus(models.TextChoices):
        INITIATED = "INITIATED", "INITIATED"
        SUCCESS = "SUCCESS", "SUCCESS"
        FAILED = "FAILED", "FAILED"

    id = models.UUIDField(primary_key=True, editable=True, default=uuid4)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="payment_log"
    )
    provider = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=100, db_index=True)
    status = models.CharField(
        max_length=10,
        choices=PaymentLogStatus.choices,
        default=PaymentLogStatus.INITIATED,
    )
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
