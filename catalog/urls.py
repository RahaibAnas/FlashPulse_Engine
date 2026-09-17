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
    path("catagories/", CatagoryListCreateApi.as_view()),
    path("catagories/<str:pk>", CatagoryDetails.as_view()),
    path("products/",ProductListCreateApi.as_view()),
    path("products/<str:pk>",ProductDetails.as_view())
]
