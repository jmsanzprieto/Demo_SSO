from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer
import jwt
from django.conf import settings
from datetime import datetime

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data['username'])
            user_info = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
            response.data.update(user_info)
        return response

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"message": "Sesión cerrada exitosamente"}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({"error": "Se necesita el token de actualización"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Error al cerrar sesión"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.utils import timezone

class SSOLoginView(APIView):
    def post(self, request):
        print(request.data)  # Imprime los datos recibidos en la solicitud
        token = request.data.get("token")  # Obtiene el token de los datos de la solicitud
        print(token)  # Imprime el token recibido

        if not token:
            return Response({"error": "Token no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)  # Retorna un error si no se proporciona el token

        try:
            # Decodifica el token usando la misma clave secreta utilizada para firmar el token
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            user_id = decoded_token.get("sub")  # Obtiene el ID del usuario del token decodificado
            email = decoded_token.get("email")  # Obtiene el email del token decodificado
            username = decoded_token.get("name")  # Obtiene el nombre de usuario del token decodificado

            if not user_id or not email or not username:
                return Response({"error": "Token inválido: falta información necesaria"}, status=status.HTTP_400_BAD_REQUEST)  # Retorna un error si falta información necesaria en el token

            # Valida si el correo electrónico ya existe
            try:
                user = User.objects.get(email=email)  # Busca al usuario por correo electrónico
                # Actualiza la información del usuario
                user.username = username
                user.id = user_id
                user.save()
            except User.DoesNotExist:
                # Crea un nuevo usuario si no existe
                user = User(id=user_id, username=username, email=email)
                user.save()

            # Crea nuevos tokens para el usuario
            refresh = RefreshToken.for_user(user)  # Crea un token de refresco para el usuario
            access_token = refresh.access_token  # Crea un token de acceso para el usuario

            return Response({
                "refresh": str(refresh),
                "access": str(access_token),
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)  # Retorna los tokens y la información del usuario

        except jwt.ExpiredSignatureError:
            return Response({"error": "El token ha expirado"}, status=status.HTTP_400_BAD_REQUEST)  # Retorna un error si el token ha expirado
        except jwt.InvalidTokenError as invalid_token_error:
            return Response({"error": f"Token inválido: {invalid_token_error}"}, status=status.HTTP_400_BAD_REQUEST)  # Retorna un error si el token es inválido
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # Retorna un error genérico si ocurre otra excepción
