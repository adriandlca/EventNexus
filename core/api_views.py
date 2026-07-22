from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from events.models import Event
from events.serializers import EventSerializer
from .models import *
from .serializers import *
from django.contrib.auth import logout,login
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username','').strip()
        email = request.data.get('email','').strip()
        password = request.data.get('password','')

        if not username or not email or not password:
            return Response(
                {'error':'Todos los campos son obligatorios'},
                status = status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=username).exists():
            return Response(
                {'error':'El username ya esta en uso'},
                status = status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {'error':'El email ya existe'},
                status = status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username = username,
            email=email,
            password = password
        )

        login(request, user)

        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    

class LoginWebAPIView(TokenObtainPairView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
             return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.user
        login(request, user)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class EventListAPIView(APIView):
    permission_classes = [AllowAny]

    DIAS_ES = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    def get(self, request):
        events = Event.objects.all().order_by('-date')
        serializer = EventSerializer(events, many=True, context={'request': request})
        data = serializer.data
        for item in data:
            if 'date_text' in item and item['date_text']:
                for en, es in self.DIAS_ES.items():
                    item['date_text'] = item['date_text'].replace(en, es)
        return Response(data, status=status.HTTP_200_OK)
