from django.urls import path

from .views import home,FlashSalesListCreateApiView,FlashSalesDetailsApiView

urlpatterns = [
    path("", view=home, name="home"),
    path(
        "products/",
        view=FlashSalesListCreateApiView.as_view(),
        name="FlashSalesListCreateApiView",
    ),
    path(
        "products/<str:id>/",
        view=FlashSalesDetailsApiView.as_view(),
        name="FlashSalesDetailsApiView",
    ),
]
