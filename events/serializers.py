from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    month = serializers.ReadOnlyField()
    day = serializers.ReadOnlyField()
    date_text = serializers.ReadOnlyField()
    class Meta:     
        model = Event
        fields = [
            'id',
            'user',
            'title',
            'date',
            'location',
            'price',
            'month',
            'image',
            'day',
            'date_text',
        ]
    