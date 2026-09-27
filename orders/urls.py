from django.urls import path

from .views import home
from .views import place_order

urlpatterns = [
    path("", view=home, name="home"),
    path("order/", view=place_order, name="place_order"),
]
