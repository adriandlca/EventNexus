from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from datetime import datetime
from django.utils import timezone


class EventDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, event_id): 
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateEventAPIView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            title = request.data.get('title')
            fecha = request.data.get('date')
            time = request.data.get('time')
            price = request.data.get('price')
            location = request.data.get('location')
            image = request.FILES.get('image')

            datestr = f"{fecha} {time}"
            datestr2 = datetime.strptime(datestr,"%Y-%m-%d %H:%M")
            date = timezone.make_aware(datestr2)
        
            if not title or not date or not price or not location or not image:
                return Response(
                {'error':'Todos los campos deben de estar llenos'}
                )
        
            event = Event.objects.create(
                user = request.user,
                title = title,
                date = date,
                price = price,
                location = location,
                image = image
            )
            serializer = EventSerializer(event)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error detallado:", str(e))
            return Response(
                {'error': 'Error interno del servidor: ' + str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
