import jwt

def decode_jwt(token, secret_key):
    print("El token es: ", token)
    print("La clave es: ", secret_key)
    try:
        # Decodificar el token utilizando la clave secreta
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        
        # Imprimir el contenido decodificado del token
        print("Token decodificado:")
        print(decoded_token)
        
        # Comparar el token decodificado con el token original
        if token == jwt.encode(decoded_token, secret_key, algorithm="HS256"):
            print("El token decodificado es igual al token original.")
        else:
            print("El token decodificado es diferente al token original.")
        
        # Retornar el contenido decodificado para su posterior análisis si es necesario
        return decoded_token
        
    except jwt.ExpiredSignatureError:
        print("El token ha expirado")
    except jwt.InvalidTokenError:
        print("Token inválido")
    except Exception as e:
        print("Error al decodificar el token:", e)

# Token JWT a decodificar
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJKV1QiLCJhdWQiOiJQUlVFQkFTIiwic3ViIjoyLCJlbWFpbCI6InRlc3RAdGVzdC5lcyIsIm5hbWUiOiJ0ZXN0IiwiZXhwIjoxNzE1OTYwMTMwfQ.WBoSMowtsblMYheso237R4gLkWklq2JNv7mBpEjXGrI"

# Clave secreta utilizada para firmar el token (reemplaza 'YOUR_SECRET_KEY' con tu clave)
secret_key = '20512cba19a9f06ab018bde779185fc459245d86ff3cf635f58b3f980eaa422b'

# Llamar a la función para decodificar el token JWT
decode_jwt(token, secret_key)
