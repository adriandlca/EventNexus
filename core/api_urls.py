from django.contrib import admin
from django.urls import path,include
from .api_views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

app_name = 'core_urls'

urlpatterns = [
    #path('token/',csrf_exempt(TokenObtainPairView.as_view()),name='login'),
    path('register/',csrf_exempt(RegisterAPIView.as_view()),name='register'),
    path('token/', LoginWebAPIView.as_view() ,name='login'),
]
