from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Contraseñas
from .serializers import ContraseñasSerializer
from rest_framework.permissions import IsAuthenticated
from cryptography.fernet import Fernet, InvalidToken

# Genera una clave única para la encriptación/desencriptación de contraseñas
clave_secreta = Fernet.generate_key()
cipher_suite = Fernet(clave_secreta)

class ContraseñasListCreate(generics.ListCreateAPIView):
    queryset = Contraseñas.objects.all()
    serializer_class = ContraseñasSerializer
    permission_classes = [IsAuthenticated]  # Establecer el permiso de autenticación

class ContraseñasRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contraseñas.objects.all()
    serializer_class = ContraseñasSerializer
    permission_classes = [IsAuthenticated]  # Establecer el permiso de autenticación

class ContraseñasUsuarioList(generics.ListAPIView):
    serializer_class = ContraseñasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Obtener el ID del usuario desde la solicitud
        usuario_id = self.kwargs['usuario_id']
        # Filtrar las contraseñas por el ID del usuario
        contraseñas = Contraseñas.objects.filter(user=usuario_id)
        
        # Desencriptar las contraseñas antes de enviarlas
        for contraseña in contraseñas:
            try:
                decrypted_password = cipher_suite.decrypt(contraseña.password.encode()).decode()
                contraseña.password = decrypted_password
            except InvalidToken:
                # Manejar el caso en el que el token no es válido
                contraseña.password = "Contraseña inválida"
        
        return contraseñas
    
class NuevaContraseña(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ContraseñasSerializer(data=request.data)
        if serializer.is_valid():
            # Obtener la contraseña sin encriptar desde la solicitud
            contraseña = serializer.validated_data.get('password')
            
            # Encriptar la contraseña utilizando Fernet
            encrypted_password = cipher_suite.encrypt(contraseña.encode()).decode()
            
            # Asignar la contraseña encriptada al objeto serializer
            serializer.validated_data['password'] = encrypted_password
            
            # Agregar el ID de usuario al objeto de contraseña antes de guardarlo
            serializer.validated_data['user_id'] = request.user.id
            
            # Guardar la contraseña en la base de datos
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
