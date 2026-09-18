from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .models import FlashSale
from .serializers import FlashSalesSerializer


# Create your views here.
@api_view(["GET"])
def home(request):
    return Response(
        {
            "succcess": True,
            "message": "FLashSales apps Works",
        },
        status=status.HTTP_200_OK,
    )

class FlashSalesListCreateApiView(ListCreateAPIView):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSalesSerializer


class FlashSalesDetailsApiView(RetrieveUpdateDestroyAPIView):
    queryset = FlashSale.objects.all()
    serializer_class = FlashSalesSerializer
