from django.contrib import admin
from .models import Catagory,Product
# Register your models here.
# admin.site.register(Catagory)
# admin.site.register(Product)


@admin.register(Catagory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    search_fields = ['name','slug']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','base_price','base_stock']
    search_fields = ['name','slug','description','category__name']
    list_filter = ['base_price','base_stock','created_at','updated_at','catagory__name']
    readonly_fields = ['created_at','updated_at']
    list_per_page = 20
    ordering = ['-created_at','-base_price']