from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = 'core'

urlpatterns = [
    path('login/',login_page,name='login_page'),
    path('register/',register_page,name='register_page'),
    path('logout/',logout_page,name='logout'),
]
