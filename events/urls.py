from django.contrib import admin
from django.urls import path,include
from .views import *

app_name= 'events'

urlpatterns = [
    path('events/<int:event_id>/detail/',detail_page,name='detail'),
    path('events/create/',create_events_page,name='create_events_page'),
]
