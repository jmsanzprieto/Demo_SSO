import jwt

# Clave secreta utilizada para decodificar el token
secret_key = '20512cba19a9f06ab018bde779185fc459245d86ff3cf635f58b3f980eaa422b'

# Token JWT a decodificar (debes reemplazarlo con tu token real)
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ5b3VyX2lzc3VlciIsImF1ZCI6InlvdXJfYXVkaWVuY2UiLCJpYXQiOjE3MTU5NTc1NTAsIm5iZiI6MTcxNTk1NzU1MCwiZXhwIjoxNzE1OTYxMTUwLCJzdWIiOjIsImVtYWlsIjoidGVzdEB0ZXN0LmVzIiwibmFtZSI6InRlc3QifQ.mDttuxP-uyDoMa9bpBoeeSCkm1QJuMu"

try:
    # Decodificar el token utilizando la clave secreta, sin validar la audiencia
    decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"], options={"verify_aud": False})
    print("La decodificación funciona correctamente:")
    print(decoded_token)
except jwt.ExpiredSignatureError:
    print("El token ha expirado")
except jwt.InvalidTokenError:
    print("Token inválido")
except Exception as e:
    print("Error:", e)
