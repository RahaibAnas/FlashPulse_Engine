from django.contrib import admin
from .models import FlashSale

# Register your models here.
@admin.register(FlashSale)
class FlashSalesAdmin(admin.ModelAdmin):
    list_display = ['product__name','allocate_stock','sold_stock',"start_date","end_date",'status']
    list_filter = ['status','start_date','end_date']
    list_per_page = 10