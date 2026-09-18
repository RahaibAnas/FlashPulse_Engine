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
        "products/<uuid:pk>/",
        view=FlashSalesDetailsApiView.as_view(),
        name="FlashSalesDetailsApiView",
    ),
]
