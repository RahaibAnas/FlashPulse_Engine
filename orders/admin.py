from django.contrib import admin

from .models import Order,PaymentLog


# Register your models here.
@admin.register(Order)
class FlashSalesAdmin(admin.ModelAdmin):
    list_display = [
        "get_user_name",
        "get_item_name",
        "quantity",
        "status",
        "created_at",
        "expires_at",
    ]
    list_filter = ["status", "created_at", "expires_at"]
    list_per_page = 10

    list_select_related = ['user','flash_sale_item']

    @admin.display(ordering="user__name",description="User")
    def get_user_name(self,obj):
        return obj.user.first_name

    @admin.display(ordering="flash_sale_item__name",description="Flash Sale item Name")
    def get_item_name(self,obj):
        return obj.flash_sale_item.product.name
