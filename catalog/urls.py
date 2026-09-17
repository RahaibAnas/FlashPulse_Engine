from django.urls import path

from .views import home
from .views import (
    CatagoryListCreateApi,
    CatagoryDetails,
    ProductListCreateApi,
    ProductDetails,
)

urlpatterns = [
    path("", view=home, name="home"),
    path("categories/", CatagoryListCreateApi.as_view()),
    path("categories/<str:pk>", CatagoryDetails.as_view()),
    path("products/",ProductListCreateApi.as_view()),
    path("products/<str:pk>",ProductDetails.as_view())
]
