from django.contrib import admin
from django.urls import path,include
from .views import *

app_name= 'events'

urlpatterns = [
    path('',home_page,name = 'home'),
    path('events/<int:event_id>/detail/',detail_page,name='detail'),
    path('events/create/',create_events_page,name='create_events_page'),
]