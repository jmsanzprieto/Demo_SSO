from django.contrib import admin
from .models import Contraseñas

class ContraseñasAdmin(admin.ModelAdmin):
    # Define los campos que deseas mostrar en la lista de objetos
    list_display = ('user', 'service','password')

# Registra el modelo Mensajes con su administrador personalizado
admin.site.register(Contraseñas, ContraseñasAdmin)
