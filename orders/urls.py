from django.urls import path

from .views import place_order,get_order_details,get_orders_detail_by_user,cancel_order


urlpatterns = [
    path("", view=place_order, name="place_order"),
    path(
        "my-orders/", view=get_orders_detail_by_user, name="get_orders_detail_by_user"
    ),
    path("<str:pk>/", view=get_order_details, name="get_order_details"),
    path("<str:pk>/cancel/", view=cancel_order, name="cancel"),
]
