from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import home,register,login,profile,logout


urlpatterns = [
    path("", view=home, name="home"),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path('logout/',logout,name='logout'),
    path("profile/", profile, name="profile"),

    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair_view"),
    path("token/refresh/", TokenRefreshView.as_view(), name="Token_refresh_view"),
]
