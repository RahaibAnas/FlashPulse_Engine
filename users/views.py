from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer

User = get_user_model()


# Create your views here.
@api_view(["GET"])
def home(request):
    return Response(
        {
            "succcess": True,
            "message": "Users apps Works",
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def register(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return Response(
            {
                "success": False,
                "error": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer.save()
    return Response(
        {
            "success": True,
            "message": "User Registered Successfully",
            "data": serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def login(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")
    user = authenticate(request, username=email, password=password)
    user.token_verified = True
    user.save(update_fields=['token_verified'])
    if user is None:
        return Response(
            {"success": False, "message": "invalid Credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    refresh = RefreshToken.for_user(user)
    refresh["token_verified"] = user.token_verified
    print(refresh["token_verified"])
    return Response(
        {
            "success": True,
            "message": "User login Successfully",
            "access token": str(refresh.access_token),
            "refresh token": str(refresh),
        },
        status=status.HTTP_202_ACCEPTED,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)

    return Response(
        {
            "success": True,
            "data": serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh = request.data.get("refresh")
    if not refresh:
        return Response(
            {"success": False, "message": "Refresh token required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        token = RefreshToken(refresh)
        token.blacklist()

        request.user.token_verified = False
        request.user.save(update_fields=["token_verified"])

        return Response(
            {"success": True, "message": "User successfully Logout"},
            status=status.HTTP_202_ACCEPTED,
        )
    except Exception:

        return Response(
            {"success": False, "message": "invalid or expired token"},
            status=status.HTTP_400_BAD_REQUEST,
        )
