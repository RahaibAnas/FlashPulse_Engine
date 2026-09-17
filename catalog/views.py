from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework. generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .models import Catagory,Product
from .serializers import CategorySerialiser,ProductSerialiser
from .paginations import PagePagination


# Create your views here.
@api_view(["GET"])
def home(request):
    return Response(
        {
            "succcess": True,
            "message": "Catalog apps Works",
        },
        status=status.HTTP_200_OK,
    )

class CatagoryListCreateApi(ListCreateAPIView):
    queryset = Catagory.objects.all()
    serializer_class = CategorySerialiser
    pagination_class = PagePagination

class CatagoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Catagory.objects.all()
    serializer_class = CategorySerialiser

class ProductListCreateApi(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialiser
    pagination_class = PagePagination


class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerialiser
