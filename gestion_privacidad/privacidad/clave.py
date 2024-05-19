import secrets

# Generar una clave secreta aleatoria de 32 bytes (256 bits)
secret_key = secrets.token_hex(32)

print("Clave secreta generada:")
print(secret_key)
