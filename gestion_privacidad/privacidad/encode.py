import jwt
from datetime import datetime, timedelta

def create_jwt(payload, secret_key):
    try:
        # Calcula el tiempo actual
        current_time = datetime.utcnow()

        # Calcula el tiempo de expiración (1 hora desde el tiempo actual)
        expiration_time = current_time + timedelta(hours=1)

        # Actualiza el campo "exp" en el payload
        payload['exp'] = expiration_time

        # Genera el token JWT con el payload actualizado
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        
        # Retornar el token JWT generado
        return token
        
    except Exception as e:
        print("Error al generar el token JWT:", e)

# Contenido para el payload del token JWT
payload = {
    "iss": "JWT",
    "aud": "PRUEBAS",
    # "iat": datetime.utcnow(),
    # "nbf": datetime.utcnow(),
    # "exp": datetime.utcnow() + timedelta(hours=1),
    "sub": 2,
    "email": "test@test.es",
    "name": "test"
}

# Clave secreta utilizada para firmar el token (reemplaza 'YOUR_SECRET_KEY' con tu clave)
secret_key = '20512cba19a9f06ab018bde779185fc459245d86ff3cf635f58b3f980eaa422b'

# Llama a la función para crear el token JWT
jwt_token = create_jwt(payload, secret_key)

print("Token JWT generado:")
print(jwt_token)
