from django.contrib import admin
from django.urls import path,include
from .api_views import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

app_name = 'core_urls'

urlpatterns = [
    path('auth/register/',csrf_exempt(RegisterAPIView.as_view()),name='register'),
    path('auth/token/', LoginWebAPIView.as_view() ,name='login'),
    path('events/', EventListAPIView.as_view(), name='events_card'),
]
