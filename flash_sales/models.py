from django.db import models
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.utils import timezone
from uuid import uuid4

from catalog.models import Product

# Create your models here.
class FlashSale(models.Model):
    class SaleStatus(models.TextChoices):
        SOLD_OUT = "SOLD_OUT","SOLD_OUT"
        SCHEDULED = "SCHEDULED","SCHEDULED"
        ACTIVE = "ACTIVE","ACTIVE"
        ENDED = "ENDED","ENDED"

    id = models.UUIDField(default=uuid4,editable=False,primary_key=True)
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name="Flash_sales")
    flash_price = models.DecimalField(max_digits=10,decimal_places=2)
    allocate_stock = models.PositiveIntegerField()
    reserved_stock = models.PositiveIntegerField(default=0)
    sold_stock = models.PositiveIntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=12,choices=SaleStatus.choices,default=SaleStatus.SCHEDULED)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self,*args,**kwargs):

        if self.allocate_stock > self.product.base_stock:
            raise ValidationError({"allocate_stock":"No Enough stock is avaliable"})

        if self.flash_price > self.product.base_price:
            raise ValidationError({"flash_price":"Flash price must be less and equal to base price"})

        if self.start_date > self.end_date:
            raise ValidationError({"end_date":"Sales End date must be after Start date"})

        if self.allocate_stock < (self.reserved_stock+self.sold_stock):
            raise ValidationError(
                "Allocated stock cannot be less than reserved + sold stock."
            )
    def update_status(self):
        now = timezone.now

        if self.sold_stock >= self.allocate_stock:
            return self.SaleStatus.SOLD_OUT
        elif now < self.start_date:
            return self.SaleStatus.SCHEDULED
        elif now > self.end_date:
            return self.SaleStatus.ENDED
        else:
            return self.SaleStatus.ACTIVE

    def save(self,*args,**kwargs):
        self.full_clean()
        self.status = self.update_status()
        super.save(*args,**kwargs)

    def __str__(self):
        return self.product.name
