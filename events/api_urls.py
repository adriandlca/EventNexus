from django.contrib import admin
from django.urls import path,include
from .api_views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'events_api'

urlpatterns = [
    path('',EventListCreateAPIView.as_view(),name='events_card'),
    path('<int:event_id>/',EventDetailAPIView.as_view(),name='api_detail'),
    path('create/',CreateEventAPIView.as_view(),name='create_events'),
]
