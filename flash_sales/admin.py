from django.contrib import admin
from .models import FlashSaleItem

# Register your models here.
@admin.register(FlashSaleItem)
class FlashSalesAdmin(admin.ModelAdmin):
    list_display = ['product__name','allocate_stock','sold_stock',"reserved_stock","start_date","end_date",'status']
    list_filter = ['status','start_date','end_date']
    list_per_page = 10